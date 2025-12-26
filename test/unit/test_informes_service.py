# -*- coding: utf-8 -*-
"""
Tests unitaires pour InformesService
"""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
from services.informes_service import InformesService
from database.database import Database
from utils.exceptions import ValidationError, DatabaseError


class TestInformesService(unittest.TestCase):
    """Tests pour InformesService"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        # Créer une base de données temporaire
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Initialiser la base de données avec des données de test
        self.db = Database(self.temp_db.name)
        
        # Créer une organisation
        self.db.create_organization({
            'nombre': 'Test Org',
            'cif': '12345678A',
            'direccion': 'Test Address',
            'telefono': '123456789',
            'email': 'test@test.com'
        })
        
        # Créer un client
        self.cliente_id = self.db.add_client({
            'nombre': 'Cliente Test',
            'cif': 'B87654321',
            'direccion': 'Calle Test 123',
            'telefono': '987654321',
            'email': 'cliente@test.com'
        })
        
        # Créer des produits
        self.producto1_id = self.db.add_product({
            'nombre': 'Producto Test 1',
            'referencia': 'REF-001',
            'precio': 100.0,
            'iva_recomendado': 21.0,
            'categoria': 'Categoría A'
        })
        
        self.producto2_id = self.db.add_product({
            'nombre': 'Producto Test 2',
            'referencia': 'REF-002',
            'precio': 50.0,
            'iva_recomendado': 21.0,
            'categoria': 'Categoría B'
        })
        
        # Actualizar stock
        self.db.update_product_stock(self.producto1_id, 100)
        self.db.update_product_stock(self.producto2_id, 50)
        
        # Créer des factures
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # Factura 1
        factura1_data = {
            'numero': 'F-001',
            'fecha': today,
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': 'B87654321',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 200.0,
            'iva_total': 42.0,
            'total': 242.0,
            'lineas': [
                {
                    'producto_id': self.producto1_id,
                    'cantidad': 2,
                    'precio_unitario': 100.0,
                    'iva_aplicado': 21.0,
                    'descuento': 0.0,
                    'subtotal': 200.0,
                    'descuento_amount': 0.0,
                    'iva_amount': 42.0,
                    'total': 242.0
                }
            ]
        }
        self.factura1_id = self.db.add_invoice(factura1_data)

        # Factura 2
        factura2_data = {
            'numero': 'F-002',
            'fecha': yesterday,
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': 'B87654321',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 150.0,
            'iva_total': 31.5,
            'total': 181.5,
            'lineas': [
                {
                    'producto_id': self.producto2_id,
                    'cantidad': 3,
                    'precio_unitario': 50.0,
                    'iva_aplicado': 21.0,
                    'descuento': 0.0,
                    'subtotal': 150.0,
                    'descuento_amount': 0.0,
                    'iva_amount': 31.5,
                    'total': 181.5
                }
            ]
        }
        self.factura2_id = self.db.add_invoice(factura2_data)
        
        # Créer le service
        self.informes_service = InformesService(self.temp_db.name)
    
    def tearDown(self):
        """Nettoyer après les tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_get_informe_facturacion_valid_period(self):
        """Test: Générer un informe de facturation pour une période valide"""
        # Période de 7 jours
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fecha_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        informe = self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)
        
        # Vérifier la structure
        self.assertIn('periodo', informe)
        self.assertIn('resumen', informe)
        self.assertIn('facturas', informe)
        self.assertIn('desglose_iva', informe)
        self.assertIn('productos_mas_vendidos', informe)
        
        # Vérifier le résumé
        self.assertEqual(informe['resumen']['num_facturas'], 2)
        self.assertGreater(informe['resumen']['total'], 0)
        
        # Vérifier les factures
        self.assertEqual(len(informe['facturas']), 2)
    
    def test_get_informe_facturacion_invalid_dates(self):
        """Test: Erreur si la date de début est après la date de fin"""
        fecha_inicio = datetime.now().strftime('%Y-%m-%d')
        fecha_fin = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        with self.assertRaises(ValidationError):
            self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)
    
    def test_get_informe_facturacion_invalid_format(self):
        """Test: Erreur si le format de date est invalide"""
        with self.assertRaises(ValidationError):
            self.informes_service.get_informe_facturacion('invalid', '2024-12-25')
    
    def test_get_informe_stock_all_products(self):
        """Test: Générer un informe de stock pour tous les produits"""
        informe = self.informes_service.get_informe_stock()
        
        # Vérifier la structure
        self.assertIn('resumen', informe)
        self.assertIn('productos', informe)
        self.assertIn('por_categoria', informe)
        
        # Vérifier le résumé
        self.assertEqual(informe['resumen']['total_productos'], 2)
        self.assertGreater(informe['resumen']['valor_total_stock'], 0)
        
        # Vérifier les produits
        self.assertEqual(len(informe['productos']), 2)

    def test_get_informe_stock_selected_products(self):
        """Test: Générer un informe de stock pour des produits sélectionnés"""
        informe = self.informes_service.get_informe_stock([self.producto1_id])

        # Vérifier que seul le produit sélectionné est inclus
        self.assertEqual(informe['resumen']['total_productos'], 1)
        self.assertEqual(len(informe['productos']), 1)
        self.assertEqual(informe['productos'][0]['id'], self.producto1_id)

    def test_get_informe_stock_empty_selection(self):
        """Test: Informe de stock avec liste vide retourne tous les produits"""
        informe = self.informes_service.get_informe_stock([])

        # Liste vide devrait retourner tous les produits
        self.assertEqual(informe['resumen']['total_productos'], 2)

    def test_informe_facturacion_desglose_iva(self):
        """Test: Vérifier le désglose par IVA"""
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fecha_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        informe = self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)

        # Vérifier qu'il y a un désglose par IVA
        self.assertGreater(len(informe['desglose_iva']), 0)

        # Vérifier que tous les IVA sont à 21%
        for item in informe['desglose_iva']:
            self.assertEqual(item['iva'], 21.0)

    def test_informe_facturacion_productos_mas_vendidos(self):
        """Test: Vérifier les produits les plus vendus"""
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        fecha_inicio = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        informe = self.informes_service.get_informe_facturacion(fecha_inicio, fecha_fin)

        # Vérifier qu'il y a des produits vendus
        self.assertGreater(len(informe['productos_mas_vendidos']), 0)

        # Vérifier la structure
        for producto in informe['productos_mas_vendidos']:
            self.assertIn('nombre', producto)
            self.assertIn('referencia', producto)
            self.assertIn('cantidad', producto)
            self.assertIn('importe', producto)

    def test_informe_stock_por_categoria(self):
        """Test: Vérifier le désglose par catégorie"""
        informe = self.informes_service.get_informe_stock()

        # Vérifier qu'il y a des catégories
        self.assertGreater(len(informe['por_categoria']), 0)

        # Vérifier la structure
        for categoria in informe['por_categoria']:
            self.assertIn('categoria', categoria)
            self.assertIn('num_productos', categoria)
            self.assertIn('stock_total', categoria)
            self.assertIn('valor_total', categoria)


if __name__ == '__main__':
    unittest.main()

