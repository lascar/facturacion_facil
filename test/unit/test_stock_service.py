# -*- coding: utf-8 -*-
"""
Tests unitaires pour StockService
"""

import pytest
import tempfile
import os
from services.stock_service import StockService
from database.database import Database
from utils.exceptions import (
    ProductValidationError,
    ProductNotFoundError,
    DatabaseError
)


class TestStockService:
    """Tests pour StockService"""

    @pytest.fixture(autouse=True)
    def setup(self, unit_db):
        """Préparer les tests"""
        # Désactiver temporairement TEST_DATABASE_PATH
        old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
        os.environ.pop('TEST_DATABASE_PATH', None)

        self.service = StockService(unit_db.db_path)

        # Créer des produits de test
        from services.producto_service import ProductoService
        producto_service = ProductoService(unit_db.db_path)

        self.producto_id = producto_service.create_producto({
            'nombre': 'Producto Test 1',
            'precio_venta': 10.0,
            'iva_recomendado': 21.0,
            'stock': 100
        })

        self.producto_id_2 = producto_service.create_producto({
            'nombre': 'Producto Test 2',
            'precio_venta': 20.0,
            'iva_recomendado': 21.0,
            'stock': 50
        })

        # Restaurer TEST_DATABASE_PATH
        if old_test_db_path:
            os.environ['TEST_DATABASE_PATH'] = old_test_db_path

        yield
        # Le nettoyage est géré par la fixture unit_db


    def test_get_all_stock(self):
        """Test récupération de tous les stocks"""
        productos = self.service.get_all_stock()

        assert isinstance(productos, list)
        assert len(productos) > 0

        # Vérifier qu'on a bien le produit de test
        nombres = [p['nombre'] for p in productos]
        assert 'Producto Test 1' in nombres
    
    def test_get_stock_by_product_id(self):
        """Test récupération du stock d'un produit"""
        producto = self.service.get_stock_by_product_id(self.producto_id)

        assert producto is not None
        assert producto['id'] == self.producto_id
        assert 'stock_actual' in producto

    def test_get_stock_by_product_id_invalid(self):
        """Test récupération avec ID invalide"""
        with pytest.raises(ProductValidationError):
            self.service.get_stock_by_product_id(0)

        with pytest.raises(ProductValidationError):
            self.service.get_stock_by_product_id(-1)
    
    def test_update_stock(self):
        """Test mise à jour du stock"""
        nuevo_stock = 150
        success = self.service.update_stock(self.producto_id, nuevo_stock)

        assert success

        # Vérifier que le stock a été mis à jour
        producto = self.service.get_stock_by_product_id(self.producto_id)
        assert producto['stock_actual'] == nuevo_stock

    def test_update_stock_negative(self):
        """Test mise à jour avec stock négatif"""
        with pytest.raises(ProductValidationError) as context:
            self.service.update_stock(self.producto_id, -10)

        assert "no puede ser negativo" in str(context.value)

    def test_update_stock_invalid_id(self):
        """Test mise à jour avec ID invalide"""
        with pytest.raises(ProductValidationError):
            self.service.update_stock(0, 100)
    
    def test_adjust_stock_positive(self):
        """Test ajustement positif du stock"""
        # Récupérer le stock initial
        producto = self.service.get_stock_by_product_id(self.producto_id)
        stock_initial = producto['stock_actual']

        # Ajuster le stock
        ajuste = 50
        success = self.service.adjust_stock(self.producto_id, ajuste)

        assert success

        # Vérifier que le stock a été ajusté
        producto = self.service.get_stock_by_product_id(self.producto_id)
        assert producto['stock_actual'] == stock_initial + ajuste

    def test_adjust_stock_negative(self):
        """Test ajustement négatif du stock"""
        # Récupérer le stock initial
        producto = self.service.get_stock_by_product_id(self.producto_id)
        stock_initial = producto['stock_actual']

        # Ajuster le stock
        ajuste = -20
        success = self.service.adjust_stock(self.producto_id, ajuste)

        assert success

        # Vérifier que le stock a été ajusté
        producto = self.service.get_stock_by_product_id(self.producto_id)
        assert producto['stock_actual'] == stock_initial + ajuste

    def test_adjust_stock_invalid_id(self):
        """Test ajustement avec ID invalide"""
        with pytest.raises(ProductValidationError):
            self.service.adjust_stock(0, 10)
    
    # Note: Les tests pour update_stock_minimo sont désactivés car la table stock
    # n'a pas encore de colonne stock_minimo. Cette fonctionnalité sera ajoutée plus tard.

