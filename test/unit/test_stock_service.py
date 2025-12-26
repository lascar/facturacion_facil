# -*- coding: utf-8 -*-
"""
Tests unitaires pour StockService
"""

import unittest
import tempfile
import os
from services.stock_service import StockService
from database.database import Database
from utils.exceptions import (
    ProductValidationError,
    ProductNotFoundError,
    DatabaseError
)


class TestStockService(unittest.TestCase):
    """Tests pour StockService"""

    def setUp(self):
        """Configuration avant chaque test"""
        # Créer une base de données temporaire
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()

        # Initialiser la base de données avec un produit de test
        db = Database(self.temp_db.name)
        self.producto_id = db.add_product({
            'nombre': 'Producto Test 1',
            'referencia': 'REF-001',
            'precio': 100.0,
            'iva_recomendado': 21.0,
            'stock': 100,
            'stock_minimo': 10
        })

        # Créer le service
        self.stock_service = StockService(self.temp_db.name)

    def tearDown(self):
        """Nettoyer après les tests"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_get_all_stock(self):
        """Test récupération de tous les stocks"""
        productos = self.stock_service.get_all_stock()

        self.assertIsInstance(productos, list)
        self.assertGreater(len(productos), 0)

        # Vérifier qu'on a bien le produit de test
        nombres = [p['nombre'] for p in productos]
        self.assertIn('Producto Test 1', nombres)
    
    def test_get_stock_by_product_id(self):
        """Test récupération du stock d'un produit"""
        producto = self.stock_service.get_stock_by_product_id(self.producto_id)

        self.assertIsNotNone(producto)
        self.assertEqual(producto['id'], self.producto_id)
        self.assertIn('stock_actual', producto)

    def test_get_stock_by_product_id_invalid(self):
        """Test récupération avec ID invalide"""
        with self.assertRaises(ProductValidationError):
            self.stock_service.get_stock_by_product_id(0)

        with self.assertRaises(ProductValidationError):
            self.stock_service.get_stock_by_product_id(-1)
    
    def test_update_stock(self):
        """Test mise à jour du stock"""
        nuevo_stock = 150
        success = self.stock_service.update_stock(self.producto_id, nuevo_stock)

        self.assertTrue(success)

        # Vérifier que le stock a été mis à jour
        producto = self.stock_service.get_stock_by_product_id(self.producto_id)
        self.assertEqual(producto['stock_actual'], nuevo_stock)

    def test_update_stock_negative(self):
        """Test mise à jour avec stock négatif"""
        with self.assertRaises(ProductValidationError) as context:
            self.stock_service.update_stock(self.producto_id, -10)

        self.assertIn("no puede ser negativo", str(context.exception))

    def test_update_stock_invalid_id(self):
        """Test mise à jour avec ID invalide"""
        with self.assertRaises(ProductValidationError):
            self.stock_service.update_stock(0, 100)
    
    def test_adjust_stock_positive(self):
        """Test ajustement positif du stock"""
        # Récupérer le stock initial
        producto = self.stock_service.get_stock_by_product_id(self.producto_id)
        stock_initial = producto['stock_actual']

        # Ajuster le stock
        ajuste = 50
        success = self.stock_service.adjust_stock(self.producto_id, ajuste)

        self.assertTrue(success)

        # Vérifier que le stock a été ajusté
        producto = self.stock_service.get_stock_by_product_id(self.producto_id)
        self.assertEqual(producto['stock_actual'], stock_initial + ajuste)

    def test_adjust_stock_negative(self):
        """Test ajustement négatif du stock"""
        # Récupérer le stock initial
        producto = self.stock_service.get_stock_by_product_id(self.producto_id)
        stock_initial = producto['stock_actual']

        # Ajuster le stock
        ajuste = -20
        success = self.stock_service.adjust_stock(self.producto_id, ajuste)

        self.assertTrue(success)

        # Vérifier que le stock a été ajusté
        producto = self.stock_service.get_stock_by_product_id(self.producto_id)
        self.assertEqual(producto['stock_actual'], stock_initial + ajuste)

    def test_adjust_stock_invalid_id(self):
        """Test ajustement avec ID invalide"""
        with self.assertRaises(ProductValidationError):
            self.stock_service.adjust_stock(0, 10)
    
    # Note: Les tests pour update_stock_minimo sont désactivés car la table stock
    # n'a pas encore de colonne stock_minimo. Cette fonctionnalité sera ajoutée plus tard.

