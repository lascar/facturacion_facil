# -*- coding: utf-8 -*-
"""
Tests de comportement pour l'informe de facturación
"""

import pytest
import sys
import os
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database.database import Database
from services.informes_service import InformesService


class TestInformeFacturacionBehaviour:
    """Tests BDD pour l'informe de facturación"""

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Configuration pour chaque test"""
        # Créer une base de données temporaire
        self.db_path = str(tmp_path / "test_informe_facturacion.db")
        self.db = Database(self.db_path)
        # La base de données est initialisée automatiquement dans __init__
        self.informes_service = InformesService(self.db_path)

        yield

        # Nettoyage
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_informe_includes_lista_clientes(self):
        """
        GIVEN des factures avec différents clients
        WHEN je génère un informe de facturación
        THEN l'informe doit inclure une liste unique de clients
        """
        # Créer des clients
        cliente1_id = self.db.add_client({
            'nombre': 'Cliente 1',
            'dni_nie': '11111111A',
            'email': 'cliente1@test.com'
        })

        cliente2_id = self.db.add_client({
            'nombre': 'Cliente 2',
            'dni_nie': '22222222B',
            'email': 'cliente2@test.com'
        })

        # Créer des factures
        today = datetime.now().strftime('%Y-%m-%d')

        self.db.add_invoice({
            'numero_factura': 'F-001',
            'fecha_factura': today,
            'cliente_id': cliente1_id,
            'nombre_cliente': 'Cliente 1',
            'dni_nie_cliente': '11111111A',
            'subtotal': 100.0,
            'total_iva': 21.0,
            'total_factura': 121.0,
            'estado': 'Pagada'
        })

        self.db.add_invoice({
            'numero_factura': 'F-002',
            'fecha_factura': today,
            'cliente_id': cliente2_id,
            'nombre_cliente': 'Cliente 2',
            'dni_nie_cliente': '22222222B',
            'subtotal': 200.0,
            'total_iva': 42.0,
            'total_factura': 242.0,
            'estado': 'Pagada'
        })

        # Générer l'informe
        fecha_inicio = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        fecha_fin = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        informe = self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)

        # Vérifier que lista_clientes existe
        assert 'lista_clientes' in informe, "L'informe doit inclure lista_clientes"
        assert len(informe['lista_clientes']) == 2, "Il doit y avoir 2 clients uniques"

        # Vérifier que les clients ont un nom et un DNI
        for cliente in informe['lista_clientes']:
            assert 'nombre' in cliente
            assert 'dni_nie' in cliente

    def test_informe_facturas_include_desglose_iva(self):
        """
        GIVEN une facture avec plusieurs items à différents taux d'IVA
        WHEN je génère un informe de facturación
        THEN chaque facture doit avoir son desglose_iva
        """
        # Créer un client
        cliente_id = self.db.add_client({
            'nombre': 'Cliente Test',
            'dni_nie': '11111111A',
            'email': 'test@test.com'
        })

        # Créer un produit
        producto_id = self.db.add_product({
            'nombre': 'Producto Test',
            'referencia': 'TEST-001',
            'precio': 100.0,
            'categoria': 'Test'
        })

        # Créer une facture
        today = datetime.now().strftime('%Y-%m-%d')
        factura_id = self.db.add_invoice({
            'numero_factura': 'F-001',
            'fecha_factura': today,
            'cliente_id': cliente_id,
            'nombre_cliente': 'Cliente Test',
            'dni_nie_cliente': '11111111A',
            'subtotal': 100.0,
            'total_iva': 21.0,
            'total_factura': 121.0,
            'estado': 'Pagada'
        })

        # Ajouter un item à la facture
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO factura_items
            (factura_id, producto_id, nombre_producto, cantidad, precio_unitario, iva_aplicado, descuento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (factura_id, producto_id, 'Producto Test', 1, 100.0, 21.0, 0.0))
        conn.commit()

        # Générer l'informe
        fecha_inicio = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        fecha_fin = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        informe = self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)


        # Vérifier que la facture a un desglose_iva
        assert 'facturas' in informe
        assert len(informe['facturas']) == 1

        factura = informe['facturas'][0]
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
        # Créer un client
        cliente_id = self.db.add_client({
            'nombre': 'Cliente Test',
            'dni_nie': '11111111A',
            'email': 'test@test.com'
        })

        # Créer des produits
        producto1_id = self.db.add_product({
            'nombre': 'Producto 1',
            'referencia': 'P1',
            'precio': 100.0,
            'categoria': 'Test'
        })

        producto2_id = self.db.add_product({
            'nombre': 'Producto 2',
            'referencia': 'P2',
            'precio': 50.0,
            'categoria': 'Test'
        })

        # Créer des factures
        today = datetime.now().strftime('%Y-%m-%d')

        factura1_id = self.db.add_invoice({
            'numero_factura': 'F-001',
            'fecha_factura': today,
            'cliente_id': cliente_id,
            'nombre_cliente': 'Cliente Test',
            'dni_nie_cliente': '11111111A',
            'subtotal': 100.0,
            'total_iva': 21.0,
            'total_factura': 121.0,
            'estado': 'Pagada'
        })

        factura2_id = self.db.add_invoice({
            'numero_factura': 'F-002',
            'fecha_factura': today,
            'cliente_id': cliente_id,
            'nombre_cliente': 'Cliente Test',
            'dni_nie_cliente': '11111111A',
            'subtotal': 50.0,
            'total_iva': 5.0,
            'total_factura': 55.0,
            'estado': 'Pagada'
        })

        # Ajouter des items aux factures
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Item avec IVA 21%
        cursor.execute("""
            INSERT INTO factura_items
            (factura_id, producto_id, nombre_producto, cantidad, precio_unitario, iva_aplicado, descuento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (factura1_id, producto1_id, 'Producto 1', 1, 100.0, 21.0, 0.0))

        # Item avec IVA 10%
        cursor.execute("""
            INSERT INTO factura_items
            (factura_id, producto_id, nombre_producto, cantidad, precio_unitario, iva_aplicado, descuento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (factura2_id, producto2_id, 'Producto 2', 1, 50.0, 10.0, 0.0))

        conn.commit()

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

