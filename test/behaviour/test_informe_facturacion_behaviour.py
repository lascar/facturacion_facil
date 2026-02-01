# -*- coding: utf-8 -*-
"""
Tests de comportement pour l'informe de facturación

⚠️ PROTECTION PRODUCTION: Ce test utilise exclusivement isolated_test_database
pour garantir l'isolation complète de la base de données de production.
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.informes_service import InformesService


@pytest.mark.behaviour
class TestInformeFacturacionBehaviour:
    """Tests BDD pour l'informe de facturación"""

    @pytest.fixture(autouse=True)
    def setup(self, isolated_test_database):
        """
        Configuration pour chaque test utilisant la base de test isolée.
        
        ⚠️ OBLIGATOIRE: Utilise isolated_test_database pour l'isolation complète.
        """
        # Utiliser la base de test fournie par la fixture
        self.db = isolated_test_database
        self.db_path = isolated_test_database.test_db_path
        self.informes_service = InformesService(self.db_path)

        yield
        
        # Le nettoyage est géré par la fixture isolated_test_database

    def test_informe_facturas_include_desglose_iva(self):
        """
        GIVEN une facture avec plusieurs items à différents taux d'IVA
        WHEN je génère un informe de facturación
        THEN chaque facture doit avoir son desglose_iva
        """
        # Générer des identifiants uniques
        import time
        import random
        unique_id = int(time.time() * 1000) % 100000 + random.randint(1, 1000)

        # Créer un client
        cliente_id = self.db.add_client({
            'nombre': f'Cliente Test {unique_id}',
            'dni_nie': f'{unique_id:08d}A',
            'email': f'test{unique_id}@test.com'
        })

        # Créer un produit
        producto_id = self.db.add_product({
            'nombre': f'Producto Test {unique_id}',
            'referencia': f'TEST-{unique_id}',
            'precio': 100.0,
            'categoria': 'Test'
        })

        # Créer une facture
        today = datetime.now().strftime('%Y-%m-%d')
        factura_id = self.db.add_invoice({
            'numero': f'F-{unique_id}',
            'fecha': today,
            'cliente': {'id': cliente_id, 'nombre': f'Cliente Test {unique_id}', 'nif': f'{unique_id:08d}A'},
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0,
            'lineas': []
        })

        # Ajouter un item à la facture
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factura_items
            (factura_id, producto_id, cantidad, precio_unitario, iva_aplicado, descuento, subtotal, iva_amount, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (factura_id, producto_id, 1, 100.0, 21.0, 0.0, 100.0, 21.0, 121.0))
        conn.commit()
        conn.close()

        # Générer l'informe
        fecha_inicio = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        fecha_fin = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        informe = self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)

        # Vérifier que la facture a un desglose_iva
        assert 'facturas' in informe
        assert len(informe['facturas']) >= 1, "Il doit y avoir au moins une facture"

        # Trouver notre facture créée (la dernière)
        factura = informe['facturas'][-1]
        assert 'desglose_iva' in factura, "Chaque facture doit avoir un desglose_iva"
        assert len(factura['desglose_iva']) > 0, "Le desglose_iva ne doit pas être vide"

        # Vérifier le contenu du desglose_iva
        desglose = factura['desglose_iva'][0]
        assert 'iva_aplicado' in desglose
        assert 'base_imponible' in desglose
        assert 'total_iva' in desglose
        assert desglose['iva_aplicado'] == 21.0
        assert desglose['base_imponible'] == 100.0
        assert desglose['total_iva'] == 21.0

    def test_informe_desglose_iva_global(self):
        """
        GIVEN plusieurs factures avec différents taux d'IVA
        WHEN je génère un informe de facturación
        THEN l'informe doit avoir un desglose_iva global
        """
        # Générer des identifiants uniques
        import time
        import random
        unique_id = int(time.time() * 1000) % 100000 + random.randint(1, 1000)

        # Créer un client
        cliente_id = self.db.add_client({
            'nombre': f'Cliente Test {unique_id}',
            'dni_nie': f'{unique_id:08d}A',
            'email': f'test{unique_id}@test.com'
        })

        # Créer des produits
        producto1_id = self.db.add_product({
            'nombre': f'Producto 1 {unique_id}',
            'referencia': f'P1-{unique_id}',
            'precio': 100.0,
            'categoria': 'Test'
        })

        producto2_id = self.db.add_product({
            'nombre': f'Producto 2 {unique_id}',
            'referencia': f'P2-{unique_id}',
            'precio': 50.0,
            'categoria': 'Test'
        })

        # Créer des factures
        today = datetime.now().strftime('%Y-%m-%d')

        factura1_id = self.db.add_invoice({
            'numero': f'F-{unique_id}-001',
            'fecha': today,
            'cliente': {'id': cliente_id, 'nombre': f'Cliente Test {unique_id}', 'nif': f'{unique_id:08d}A'},
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0,
            'lineas': []
        })

        factura2_id = self.db.add_invoice({
            'numero': f'F-{unique_id}-002',
            'fecha': today,
            'cliente': {'id': cliente_id, 'nombre': f'Cliente Test {unique_id}', 'nif': f'{unique_id:08d}A'},
            'subtotal': 50.0,
            'iva_total': 5.0,
            'total': 55.0,
            'lineas': []
        })

        # Ajouter des items aux factures
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Item avec IVA 21%
        cursor.execute("""
            INSERT INTO factura_items
            (factura_id, producto_id, cantidad, precio_unitario, iva_aplicado, descuento, subtotal, iva_amount, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (factura1_id, producto1_id, 1, 100.0, 21.0, 0.0, 100.0, 21.0, 121.0))

        # Item avec IVA 10%
        cursor.execute("""
            INSERT INTO factura_items
            (factura_id, producto_id, cantidad, precio_unitario, iva_aplicado, descuento, subtotal, iva_amount, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (factura2_id, producto2_id, 1, 50.0, 10.0, 0.0, 50.0, 5.0, 55.0))

        conn.commit()
        conn.close()

        # Générer l'informe
        fecha_inicio = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        fecha_fin = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        informe = self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)

        # Vérifier le desglose_iva global
        assert 'desglose_iva' in informe
        assert len(informe['desglose_iva']) == 2, "Il doit y avoir 2 taux d'IVA différents"

        # Vérifier que les taux sont corrects
        taux = [d['iva_aplicado'] for d in informe['desglose_iva']]
        assert 10.0 in taux
        assert 21.0 in taux
