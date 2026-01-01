# -*- coding: utf-8 -*-
"""
Tests unitaires pour ProductoService
"""

import pytest
import tempfile
import os
from services.producto_service import ProductoService
from utils.exceptions import (
    ProductValidationError, ProductNotFoundError,
    DatabaseError
)


class TestProductoService:
    """Tests pour ProductoService"""
    
    @pytest.fixture(autouse=True)
    def setup(self, unit_db):
        """Préparer les tests"""
        # Désactiver temporairement TEST_DATABASE_PATH
        old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
        os.environ.pop('TEST_DATABASE_PATH', None)
        
        self.service = ProductoService(unit_db.db_path)
        
        # Restaurer TEST_DATABASE_PATH
        if old_test_db_path:
            os.environ['TEST_DATABASE_PATH'] = old_test_db_path
        
        yield
        # Le nettoyage est géré par la fixture unit_db


    def test_create_producto_success(self):
        """Test création d'un produit avec succès"""
        producto_data = {
            'nombre': 'Producto Test',
            'referencia': 'REF001',
            'precio_venta': 10.50,
            'iva_recomendado': 21.0,
            'stock': 100,
            'categoria': 'Test',
            'descripcion': 'Producto de prueba'
        }
        
        producto_id = self.service.create_producto(producto_data)
        assert producto_id is not None
        assert producto_id > 0
    
    def test_create_producto_missing_nombre(self):
        """Test création d'un produit sans nom"""
        producto_data = {
            'precio_venta': 10.50
        }
        
        with pytest.raises(ProductValidationError):
            self.service.create_producto(producto_data)
    
    def test_create_producto_negative_price(self):
        """Test création d'un produit avec prix négatif"""
        producto_data = {
            'nombre': 'Producto Test',
            'precio_venta': -10.50
        }
        
        with pytest.raises(ProductValidationError):
            self.service.create_producto(producto_data)
    
    def test_create_producto_invalid_iva(self):
        """Test création d'un produit avec IVA invalide"""
        producto_data = {
            'nombre': 'Producto Test',
            'precio_venta': 10.50,
            'iva_recomendado': 150.0  # > 100
        }
        
        with pytest.raises(ProductValidationError):
            self.service.create_producto(producto_data)
    
    def test_create_producto_negative_stock(self):
        """Test création d'un produit avec stock négatif"""
        producto_data = {
            'nombre': 'Producto Test',
            'precio_venta': 10.50,
            'stock': -5
        }
        
        with pytest.raises(ProductValidationError):
            self.service.create_producto(producto_data)
    
    def test_get_all_productos(self):
        """Test récupération de tous les produits"""
        # Créer quelques produits
        for i in range(3):
            self.service.create_producto({
                'nombre': f'Producto {i}',
                'precio_venta': 10.0 + i
            })
        
        productos = self.service.get_all_productos()
        assert isinstance(productos, list)
        assert len(productos) >= 3
    
    def test_get_producto_by_id_success(self):
        """Test récupération d'un produit par ID"""
        # Créer un produit
        producto_id = self.service.create_producto({
            'nombre': 'Producto Test',
            'precio_venta': 10.50
        })
        
        # Récupérer le produit
        producto = self.service.get_producto_by_id(producto_id)
        assert producto is not None
        assert producto['nombre'] == 'Producto Test'
    
    def test_get_producto_by_id_not_found(self):
        """Test récupération d'un produit inexistant"""
        with pytest.raises(ProductNotFoundError):
            self.service.get_producto_by_id(99999)
    
    def test_get_producto_by_id_invalid_id(self):
        """Test récupération avec ID invalide"""
        with pytest.raises(ProductValidationError):
            self.service.get_producto_by_id(-1)
    
    def test_update_producto_success(self):
        """Test mise à jour d'un produit"""
        # Créer un produit
        producto_id = self.service.create_producto({
            'nombre': 'Producto Original',
            'precio_venta': 10.50
        })
        
        # Mettre à jour
        success = self.service.update_producto({
            'id': producto_id,
            'nombre': 'Producto Actualizado',
            'precio_venta': 15.75
        })
        
        assert success
        
        # Vérifier la mise à jour
        producto = self.service.get_producto_by_id(producto_id)
        assert producto['nombre'] == 'Producto Actualizado'
    
    def test_update_producto_missing_id(self):
        """Test mise à jour sans ID"""
        with pytest.raises(ProductValidationError):
            self.service.update_producto({
                'nombre': 'Producto Test'
            })
    
    def test_delete_producto_success(self):
        """Test suppression d'un produit"""
        # Créer un produit
        producto_id = self.service.create_producto({
            'nombre': 'Producto Test',
            'precio_venta': 10.50
        })
        
        # Supprimer
        success = self.service.delete_producto(producto_id)
        assert success
        
        # Vérifier la suppression
        with pytest.raises(ProductNotFoundError):
            self.service.get_producto_by_id(producto_id)

    def test_update_producto_not_found(self):
        """Test mise à jour d'un produit inexistant - devrait réussir sans erreur"""
        # update_product ne lève pas d'erreur si le produit n'existe pas (comportement SQLite)
        success = self.service.update_producto({
            'id': 99999,
            'nombre': 'Producto Test',
            'precio_venta': 10.50
        })
        assert success

    def test_delete_producto_not_found(self):
        """Test suppression d'un produit inexistant - devrait réussir sans erreur"""
        # delete_product ne lève pas d'exception si le produit n'existe pas
        success = self.service.delete_producto(99999)
        assert success

    def test_create_producto_zero_price(self):
        """Test création d'un produit avec prix zéro (devrait passer)"""
        producto_data = {
            'nombre': 'Producto Gratis',
            'precio_venta': 0.0
        }

        producto_id = self.service.create_producto(producto_data)
        assert producto_id is not None


if __name__ == '__main__':
    unittest.main()

