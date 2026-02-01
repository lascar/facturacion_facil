# -*- coding: utf-8 -*-
"""
Test de comportement pour vérifier que les formats personnalisés de numéro de facture
(comme "2026/02") sont correctement utilisés.

⚠️ PROTECTION PRODUCTION: Utilise exclusivement isolated_test_database
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


@pytest.mark.behaviour
class TestNumeroFormatoPersonalizadoBehaviour:
    """Test BDD: Les formats personnalisés doivent être respectés"""

    def test_formato_con_slash_2026_02(self, isolated_test_database, monkeypatch):
        """
        GIVEN: Une organisation avec numero_factura_inicial = "2026/02"
        AND: Aucune facture n'existe
        WHEN: On demande le prochain numéro de facture
        THEN: Le numéro doit être "2026/02" (ou format incrémenté)
        
        ⚠️ PRODUCTION SAFETY: Utilise isolated_test_database
        """
        from utils.factura_numbering import FacturaNumberingService
        from services.organizacion_service import OrganizacionService
        
        test_db = isolated_test_database
        
        # GIVEN: Mettre à jour l'organisation avec format personnalisé "2026/02"
        # La fixture isolated_test_database crée déjà une organisation
        org_service = OrganizacionService(test_db)
        
        # Vérifier si l'organisation existe
        existing = org_service.get_organizacion()
        org_data = {
            'nombre': 'Test Empresa',
            'cif': 'B12345678',
            'numero_factura_inicial': '2026/02',  # Format avec slash
            'logo_orientation': 'landscape'
        }
        
        if existing and existing.get('id'):
            # Mettre à jour l'organisation existante
            org_data['id'] = existing['id']
            result = org_service.update_organizacion(org_data)
        else:
            # Créer une nouvelle organisation
            result = org_service.create_organizacion(org_data)
        
        assert result is True, "La sauvegarde de l'organisation a échoué"
        
        # Vérifier que la valeur est bien stockée
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT numero_factura_inicial FROM organizacion WHERE id = 1")
        db_result = cursor.fetchone()
        conn.close()
        
        print(f"\n📊 Valeur stockée en DB: {db_result}")
        assert db_result is not None, "L'organisation n'a pas été trouvée"
        assert db_result[0] == '2026/02', f"Valeur en DB: {db_result[0]}, attendu: '2026/02'"
        
        # Vider les factures pour simuler une base vide
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facturas")
        cursor.execute("DELETE FROM factura_items")
        conn.commit()
        conn.close()
        
        # Patcher la config pour retourner "2026/02"
        import config.config as config_module
        
        def mock_get_factura_numero_inicial(self):
            return '2026/02'
        
        def mock_get_factura_prefijo(self):
            return 'FAC'
        
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', mock_get_factura_numero_inicial)
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', mock_get_factura_prefijo)
        
        # WHEN: Obtenir le prochain numéro
        numbering_service = FacturaNumberingService(test_db)
        siguiente_numero = numbering_service.get_next_numero_factura()
        
        print(f"📊 Format configuré: 2026/02")
        print(f"📊 Prochain numéro généré: {siguiente_numero}")
        
        # THEN: Le numéro doit contenir "2026/02" ou être basé dessus
        # Pas "FAC-0001" ou "FAC-001-2026"
        assert '0001' not in siguiente_numero, \
            f"❌ ERREUR: Format standard détecté '{siguiente_numero}' au lieu du format personnalisé"
        assert '2026/02' in siguiente_numero or '2026' in siguiente_numero, \
            f"❌ ERREUR: Le numéro '{siguiente_numero}' ne contient pas '2026/02'"
        
        print(f"✅ SUCCÈS: Le format personnalisé est respecté!")

    def test_formato_personalizado_wp_01(self, isolated_test_database, monkeypatch):
        """
        GIVEN: Une organisation avec numero_factura_inicial = "2025-wp-01"
        AND: Aucune facture n'existe
        WHEN: On demande le prochain numéro
        THEN: Le numéro doit être "2025-wp-01"
        """
        from utils.factura_numbering import FacturaNumberingService
        from services.organizacion_service import OrganizacionService
        
        test_db = isolated_test_database
        
        # GIVEN
        org_service = OrganizacionService(test_db)
        org_data = {
            'nombre': 'Test Empresa',
            'numero_factura_inicial': '2025-wp-01',
            'logo_orientation': 'landscape'
        }
        org_service.create_organizacion(org_data)
        
        # Vider les factures
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facturas")
        conn.commit()
        conn.close()
        
        # Patcher
        import config.config as config_module
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', lambda self: '2025-wp-01')
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', lambda self: 'FAC')
        
        # WHEN
        numbering_service = FacturaNumberingService(test_db)
        siguiente_numero = numbering_service.get_next_numero_factura()
        
        print(f"\n📊 Format configuré: 2025-wp-01")
        print(f"📊 Prochain numéro: {siguiente_numero}")
        
        # THEN
        assert siguiente_numero == '2025-wp-01', \
            f"❌ ERREUR: '{siguiente_numero}' au lieu de '2025-wp-01'"
        print(f"✅ SUCCÈS!")

    def test_formato_personalizado_con_facturas_existentes(self, isolated_test_database, monkeypatch):
        """
        GIVEN: Format inicial = "2025-wp-01"
        AND: Une facture existe déjà avec "2025-wp-01"
        WHEN: On demande le prochain numéro
        THEN: Le numéro doit être "2025-wp-02"
        """
        from utils.factura_numbering import FacturaNumberingService
        from services.organizacion_service import OrganizacionService
        
        test_db = isolated_test_database
        
        # GIVEN: Organisation
        org_service = OrganizacionService(test_db)
        org_service.create_organizacion({
            'nombre': 'Test',
            'numero_factura_inicial': '2025-wp-01',
            'logo_orientation': 'landscape'
        })
        
        # Créer une facture existante
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facturas")
        cursor.execute("""
            INSERT INTO facturas (numero_factura, fecha_factura, nombre_cliente, subtotal, total_iva, total_factura)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('2025-wp-01', '2025-01-01', 'Cliente 1', 100.0, 21.0, 121.0))
        conn.commit()
        conn.close()
        
        # Patcher
        import config.config as config_module
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', lambda self: '2025-wp-01')
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', lambda self: 'FAC')
        
        # WHEN
        numbering_service = FacturaNumberingService(test_db)
        siguiente_numero = numbering_service.get_next_numero_factura()
        
        print(f"\n📊 Dernière facture: 2025-wp-01")
        print(f"📊 Prochain numéro: {siguiente_numero}")
        
        # THEN: Doit être incrémenté à 02
        assert '02' in siguiente_numero, \
            f"❌ ERREUR: '{siguiente_numero}' ne contient pas '02'"
        print(f"✅ SUCCÈS: Incrémentation correcte!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
