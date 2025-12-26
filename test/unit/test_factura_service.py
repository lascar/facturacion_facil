# -*- coding: utf-8 -*-
"""
Tests unitaires pour FacturaService
"""

import unittest
import tempfile
import os
from datetime import datetime
from services.factura_service import FacturaService
from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from utils.exceptions import (
    InvoiceValidationError, InvoiceNotFoundError,
    DatabaseError, InsufficientStockError
)


class TestFacturaService(unittest.TestCase):
    """Tests pour FacturaService"""
    
    def setUp(self):
        """Préparer les tests"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.service = FacturaService(self.temp_db.name)
        self.producto_service = ProductoService(self.temp_db.name)
        self.cliente_service = ClienteService(self.temp_db.name)
        
        # Créer un client de test
        self.cliente_id = self.cliente_service.create_cliente({
            'nombre': 'Cliente Test',
            'nif': '12345678A',
            'email': 'test@example.com',
            'direccion': 'Calle Test 123'
        })
        
        # Créer un produit de test
        self.producto_id = self.producto_service.create_producto({
            'nombre': 'Producto Test',
            'precio_venta': 10.50,
            'iva_recomendado': 21.0,
            'stock': 100
        })
    
    def tearDown(self):
        """Nettoyer après les tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_create_factura_success(self):
        """Test création d'une facture avec succès"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.50,
            'iva_total': 2.21,
            'total': 12.71,
            'estado': 'Borrador',
            'lineas': [
                {
                    'producto_id': self.producto_id,
                    'cantidad': 1,
                    'precio_unitario': 10.50,
                    'iva': 21.0
                }
            ]
        }
        
        factura_id = self.service.create_factura(factura_data)
        self.assertIsNotNone(factura_id)
        self.assertGreater(factura_id, 0)
    
    def test_create_factura_missing_numero(self):
        """Test création d'une facture sans numéro"""
        factura_data = {
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'}
        }
        
        with self.assertRaises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_missing_fecha(self):
        """Test création d'une facture sans date"""
        factura_data = {
            'numero': 'FAC-0001',
            'cliente': {'nombre': 'Cliente Test'}
        }
        
        with self.assertRaises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_invalid_cliente(self):
        """Test création d'une facture avec client invalide"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {}  # Sans nom
        }
        
        with self.assertRaises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_negative_total(self):
        """Test création d'une facture avec total négatif"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'},
            'total': -10.50
        }
        
        with self.assertRaises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_invalid_linea_missing_producto(self):
        """Test création avec ligne sans producto_id"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'},
            'lineas': [
                {
                    'cantidad': 1,
                    'precio_unitario': 10.50
                }
            ]
        }
        
        with self.assertRaises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_create_factura_invalid_linea_zero_cantidad(self):
        """Test création avec ligne à quantité zéro"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {'nombre': 'Cliente Test'},
            'lineas': [
                {
                    'producto_id': self.producto_id,
                    'cantidad': 0,  # Invalide
                    'precio_unitario': 10.50
                }
            ]
        }
        
        with self.assertRaises(InvoiceValidationError):
            self.service.create_factura(factura_data)
    
    def test_calculate_totals_empty(self):
        """Test calcul des totaux avec liste vide"""
        totals = self.service.calculate_totals([])
        self.assertEqual(totals['subtotal'], 0.0)
        self.assertEqual(totals['iva_total'], 0.0)
        self.assertEqual(totals['total'], 0.0)
    
    def test_calculate_totals_success(self):
        """Test calcul des totaux avec succès"""
        lineas = [
            {
                'cantidad': 2,
                'precio_unitario': 10.0,
                'iva': 21.0
            },
            {
                'cantidad': 1,
                'precio_unitario': 5.0,
                'iva': 10.0
            }
        ]
        
        totals = self.service.calculate_totals(lineas)
        self.assertEqual(totals['subtotal'], 25.0)  # 20 + 5
        self.assertEqual(totals['iva_total'], 4.7)  # 4.2 + 0.5
        self.assertEqual(totals['total'], 29.7)  # 25 + 4.7

    def test_generate_factura_number_first(self):
        """Test génération du premier numéro de facture"""
        numero = self.service.generate_factura_number()
        self.assertEqual(numero, 'FAC-0001')

    def test_generate_factura_number_increment(self):
        """Test incrémentation du numéro de facture"""
        # Créer une facture
        self.service.create_factura({
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': []
        })

        # Générer le prochain numéro
        numero = self.service.generate_factura_number()
        self.assertEqual(numero, 'FAC-0002')

    def test_get_all_facturas(self):
        """Test récupération de toutes les factures"""
        # Créer quelques factures
        for i in range(3):
            self.service.create_factura({
                'numero': f'FAC-000{i+1}',
                'fecha': datetime.now().strftime('%Y-%m-%d'),
                'cliente': {
                    'id': self.cliente_id,
                    'nombre': 'Cliente Test',
                    'nif': '12345678A',
                    'direccion': 'Calle Test 123'
                },
                'subtotal': 10.0,
                'iva_total': 2.1,
                'total': 12.1,
                'lineas': []
            })

        facturas = self.service.get_all_facturas()
        self.assertIsInstance(facturas, list)
        self.assertGreaterEqual(len(facturas), 3)

    def test_get_factura_by_id_success(self):
        """Test récupération d'une facture par ID"""
        # Créer une facture
        factura_id = self.service.create_factura({
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': []
        })

        # Récupérer la facture
        factura = self.service.get_factura_by_id(factura_id)
        self.assertIsNotNone(factura)
        self.assertEqual(factura['numero'], 'FAC-0001')

    def test_get_factura_by_id_not_found(self):
        """Test récupération d'une facture inexistante"""
        with self.assertRaises(InvoiceNotFoundError):
            self.service.get_factura_by_id(99999)

    def test_delete_factura_success(self):
        """Test suppression d'une facture"""
        # Créer une facture
        factura_id = self.service.create_factura({
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': []
        })

        # Supprimer
        success = self.service.delete_factura(factura_id)
        self.assertTrue(success)

        # Vérifier la suppression
        with self.assertRaises(InvoiceNotFoundError):
            self.service.get_factura_by_id(factura_id)

    def test_update_factura_without_id(self):
        """Test update_factura sans ID - doit lever InvoiceValidationError"""
        factura_data = {
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'lineas': []
        }

        with self.assertRaises(InvoiceValidationError) as context:
            self.service.update_factura(factura_data)

        self.assertIn("ID de factura requerido", str(context.exception))

    def test_update_factura_not_found(self):
        """Test update_factura avec ID inexistant - doit lever InvoiceNotFoundError"""
        factura_data = {
            'id': 99999,
            'numero': 'FAC-0001',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 0.0,
            'iva_total': 0.0,
            'total': 0.0,
            'lineas': []
        }

        with self.assertRaises(InvoiceNotFoundError):
            self.service.update_factura(factura_data)

    def test_calculate_totals_empty_lineas(self):
        """Test calculate_totals avec liste vide"""
        result = self.service.calculate_totals([])

        self.assertEqual(result['subtotal'], 0.0)
        self.assertEqual(result['iva_total'], 0.0)
        self.assertEqual(result['total'], 0.0)

    def test_calculate_totals_invalid_data(self):
        """Test calculate_totals avec données invalides"""
        lineas = [
            {'cantidad': 'invalid', 'precio_unitario': 10.0, 'iva': 21.0}
        ]

        with self.assertRaises(InvoiceValidationError) as context:
            self.service.calculate_totals(lineas)

        self.assertIn("Error calculando totales", str(context.exception))

    def test_generate_factura_number_with_existing(self):
        """Test generate_factura_number avec factures existantes"""
        # Créer une facture
        factura_data = {
            'numero': 'FAC-0005',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': {
                'id': self.cliente_id,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Calle Test 123'
            },
            'subtotal': 10.0,
            'iva_total': 2.1,
            'total': 12.1,
            'lineas': [{
                'producto_id': self.producto_id,
                'cantidad': 1,
                'precio_unitario': 10.0,
                'iva': 21.0
            }]
        }
        self.service.create_factura(factura_data)

        # Générer le prochain numéro
        next_number = self.service.generate_factura_number()
        self.assertEqual(next_number, 'FAC-0006')

    def test_generate_factura_number_no_existing(self):
        """Test generate_factura_number sans factures existantes"""
        # Créer un nouveau service avec une DB vide
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()

        try:
            service = FacturaService(temp_db.name)
            number = service.generate_factura_number()
            self.assertEqual(number, 'FAC-0001')
        finally:
            if os.path.exists(temp_db.name):
                os.unlink(temp_db.name)

    def test_validate_linea_precio_negativo(self):
        """Test validation d'une ligne avec prix négatif"""
        linea = {
            'producto_id': self.producto_id,
            'cantidad': 1,
            'precio_unitario': -10.0,
            'iva': 21.0
        }

        with self.assertRaises(InvoiceValidationError) as context:
            self.service._validate_linea(linea, 0)

        self.assertIn("precio_unitario no puede ser negativo", str(context.exception))

    def test_validate_linea_precio_invalido(self):
        """Test validation d'une ligne avec prix invalide"""
        linea = {
            'producto_id': self.producto_id,
            'cantidad': 1,
            'precio_unitario': 'invalid',
            'iva': 21.0
        }

        with self.assertRaises(InvoiceValidationError) as context:
            self.service._validate_linea(linea, 0)

        self.assertIn("precio_unitario inválido", str(context.exception))

    def test_validate_stock_producto_not_found(self):
        """Test validation stock avec produit inexistant"""
        lineas = [{
            'producto_id': 99999,
            'cantidad': 1,
            'precio_unitario': 10.0,
            'iva': 21.0
        }]

        with self.assertRaises(InvoiceValidationError) as context:
            self.service._validate_stock_availability(lineas)

        self.assertIn("Producto 99999 no encontrado", str(context.exception))

    def test_validate_stock_insufficient(self):
        """Test validation stock insuffisant"""
        # Le produit a un stock de 100
        lineas = [{
            'producto_id': self.producto_id,
            'cantidad': 200,  # Plus que le stock disponible
            'precio_unitario': 10.0,
            'iva': 21.0
        }]

        with self.assertRaises(InsufficientStockError):
            self.service._validate_stock_availability(lineas)


if __name__ == '__main__':
    unittest.main()

