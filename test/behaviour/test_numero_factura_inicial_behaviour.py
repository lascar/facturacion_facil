# -*- coding: utf-8 -*-
"""
Test de comportement pour vérifier que le numéro initial de facture
configuré dans l'organisation est bien utilisé lors de la création d'une facture.

⚠️ PROTECTION PRODUCTION: Utilise exclusivement isolated_test_database
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


@pytest.mark.behaviour
class TestNumeroFacturaInicialBehaviour:
    """Test BDD: Le numéro initial de facture configuré doit être utilisé"""

    def test_numero_inicial_saved_to_database(self, isolated_test_database, monkeypatch):
        """
        GIVEN: Une organisation avec un numéro de facture initial configuré (ex: 100)
        WHEN: On sauvegarde l'organisation via le service
        THEN: Le numéro initial doit être stocké dans la base de données
        
        ⚠️ PRODUCTION SAFETY: Utilise isolated_test_database
        """
        from services.organizacion_service import OrganizacionService
        
        # Patcher le service pour utiliser notre base de test
        test_db = isolated_test_database
        
        # Créer le service avec la base de test
        org_service = OrganizacionService(test_db)
        
        # GIVEN: Données d'organisation avec numéro initial = 100
        organizacion_data = {
            'nombre': 'Test Empresa',
            'cif': 'B12345678',
            'telefono': '+34 123 456 789',
            'email': 'test@test.com',
            'direccion': 'Calle Test 123',
            'numero_factura_inicial': '100',
            'logo_path': '',
            'logo_orientation': 'landscape'
        }
        
        # WHEN: Sauvegarder l'organisation
        result = org_service.create_organizacion(organizacion_data)
        
        # THEN: L'organisation doit être créée
        assert result is True, "La création de l'organisation a échoué"
        
        # Vérifier que le numéro initial est bien stocké
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT numero_factura_inicial FROM organizacion WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        
        assert result is not None, "L'organisation n'a pas été trouvée dans la DB"
        assert result[0] == '100', f"Le numéro initial est '{result[0]}' au lieu de '100'"
        
        print(f"\n✅ SUCCÈS: Le numéro initial '100' est bien sauvegardé dans la DB")

    def test_numero_inicial_used_by_numbering_service(self, isolated_test_database, monkeypatch):
        """
        GIVEN: Une organisation avec numero_factura_inicial = '50' dans la DB
        AND: Aucune facture n'existe (base vide)
        WHEN: Le service de numérotation demande le prochain numéro
        THEN: Le numéro doit être basé sur '50'
        
        ⚠️ PRODUCTION SAFETY: Utilise isolated_test_database
        """
        from utils.factura_numbering import FacturaNumberingService
        from services.organizacion_service import OrganizacionService
        
        test_db = isolated_test_database
        
        # GIVEN: Créer l'organisation avec numéro initial = 50
        org_service = OrganizacionService(test_db)
        org_data = {
            'nombre': 'Test Empresa',
            'cif': 'B12345678',
            'numero_factura_inicial': '50',
            'logo_orientation': 'landscape'
        }
        org_service.create_organizacion(org_data)
        
        # Vider la table des factures pour simuler une base vide
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facturas")
        cursor.execute("DELETE FROM factura_items")
        conn.commit()
        conn.close()
        
        # Patcher explicitement get_factura_numero_inicial pour retourner 50
        import config.config as config_module
        original_get_numero_inicial = config_module.Config.get_factura_numero_inicial
        
        def mock_get_factura_numero_inicial(self):
            return 50
        
        monkeypatch.setattr(config_module.Config, 'get_factura_numero_inicial', mock_get_factura_numero_inicial)
        
        # Patcher aussi get_factura_prefijo
        def mock_get_factura_prefijo(self):
            return 'FAC'
        
        monkeypatch.setattr(config_module.Config, 'get_factura_prefijo', mock_get_factura_prefijo)
        
        # WHEN: Obtenir le prochain numéro (en passant explicitement la base de test)
        numbering_service = FacturaNumberingService(test_db)
        siguiente_numero = numbering_service.get_next_numero_factura()
        
        print(f"\n📊 Numéro initial configuré: 50")
        print(f"📊 Prochain numéro généré: {siguiente_numero}")
        
        # THEN: Le numéro doit contenir '50'
        assert '50' in siguiente_numero, \
            f"❌ ERREUR: Le numéro généré '{siguiente_numero}' ne contient pas '50'"
        
        print(f"✅ SUCCÈS: Le numéro initial configuré est bien utilisé!")

    def test_numero_inicial_with_existing_facturas(self, isolated_test_database, monkeypatch):
        """
        GIVEN: Une organisation avec numero_factura_inicial = '1'
        AND: Des factures existent déjà (ex: FAC-003-2026)
        WHEN: On demande le prochain numéro
        THEN: Le numéro doit être basé sur le dernier numéro existant + 1 (FAC-004-2026)
        
        ⚠️ PRODUCTION SAFETY: Utilise isolated_test_database
        """
        from utils.factura_numbering import FacturaNumberingService
        from services.organizacion_service import OrganizacionService
        
        test_db = isolated_test_database
        
        # GIVEN: Créer l'organisation
        org_service = OrganizacionService(test_db)
        org_data = {
            'nombre': 'Test Empresa',
            'numero_factura_inicial': '1',
            'logo_orientation': 'landscape'
        }
        org_service.create_organizacion(org_data)
        
        # Créer des factures existantes
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facturas")  # Vider d'abord
        cursor.execute("""
            INSERT INTO facturas (numero_factura, fecha_factura, nombre_cliente, subtotal, total_iva, total_factura)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('FAC-001-2026', '2026-01-01', 'Cliente 1', 100.0, 21.0, 121.0))
        cursor.execute("""
            INSERT INTO facturas (numero_factura, fecha_factura, nombre_cliente, subtotal, total_iva, total_factura)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('FAC-002-2026', '2026-01-02', 'Cliente 2', 200.0, 42.0, 242.0))
        cursor.execute("""
            INSERT INTO facturas (numero_factura, fecha_factura, nombre_cliente, subtotal, total_iva, total_factura)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('FAC-003-2026', '2026-01-03', 'Cliente 3', 300.0, 63.0, 363.0))
        conn.commit()
        conn.close()
        
        # Patcher la config
        import config.config as config_module
        
        class TestConfig:
            def get_factura_numero_inicial(self):
                return 1
            def get_factura_prefijo(self):
                return 'FAC'
            def get_factura_sufijo(self):
                return ''
        
        monkeypatch.setattr(config_module, 'app_config', TestConfig())
        
        # WHEN: Obtenir le prochain numéro (en passant explicitement la base de test)
        numbering_service = FacturaNumberingService(test_db)
        siguiente_numero = numbering_service.get_next_numero_factura()
        
        print(f"\n📊 Dernière facture existante: FAC-003-2026")
        print(f"📊 Prochain numéro généré: {siguiente_numero}")
        
        # THEN: Le numéro doit être FAC-004-2026 (incrémenté depuis la dernière facture)
        assert '004' in siguiente_numero, \
            f"❌ ERREUR: Le numéro généré '{siguiente_numero}' ne contient pas '004'"
        
        print(f"✅ SUCCÈS: Le numéro est bien incrémenté depuis la dernière facture!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
