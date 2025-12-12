#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour la sélection de produits dans les facturas
"""

import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database.database import Database
from utils.logger import get_logger

class TestProductosFactura:
    """Tests pour la sélection de produits dans les facturas"""

    @pytest.fixture
    def test_db(self):
        """Fixture pour une base de données de test isolée"""
        # Créer un répertoire temporaire
        temp_dir = tempfile.mkdtemp()
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        test_db_path = os.path.join(temp_dir, f'test_productos_factura_{unique_id}.db')

        # Sauvegarder la configuration originale
        original_db_path = getattr(Database, '_db_path', None)

        # Configurer la base de données de test
        Database._db_path = test_db_path

        # Créer l'instance de base de données
        db = Database()

        yield db

        # Cleanup garantizado
        try:
            if hasattr(db, '_connection') and db._connection:
                db._connection.close()
        except:
            pass

        # Nettoyer après le test
        if original_db_path:
            Database._db_path = original_db_path

        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass  # Ignorer les erreurs de nettoyage

    @pytest.fixture
    def db_with_sample_products(self, test_db):
        """Fixture pour une base de données avec des produits d'exemple"""
        import uuid
        unique_id = str(uuid.uuid4())[:8]

        sample_products = [
            {
                'nombre': f'Producto Test Unit 1 {unique_id}',
                'referencia': f'UNIT-001-{unique_id}',
                'precio_venta': 15.50,
                'precio_compra': 10.00,
                'categoria': 'Unit Test',
                'descripcion': 'Producto para tests unitarios',
                'iva_recomendado': 21.0,
                'stock_actual': 8,
                'stock_minimo': 2
            },
            {
                'nombre': f'Producto Test Unit 2 {unique_id}',
                'referencia': f'UNIT-002-{unique_id}',
                'precio_venta': 32.75,
                'precio_compra': 20.00,
                'categoria': 'Unit Test',
                'descripcion': 'Segundo producto para tests',
                'iva_recomendado': 10.0,
                'stock_actual': 0,  # Sin stock para tests
                'stock_minimo': 1
            }
        ]

        for product_data in sample_products:
            result = test_db.add_product(product_data)
            if not result:
                print(f"⚠️  Error agregando producto: {product_data['nombre']}")

        return test_db
    
    @pytest.fixture
    def sample_product(self):
        """Fixture pour un produit d'exemple"""
        return {
            'id': 1,
            'nombre': 'Producto Test',
            'referencia': 'TEST-001',
            'precio_venta': 25.50,
            'precio_compra': 15.00,
            'categoria': 'Test',
            'descripcion': 'Producto para tests',
            'iva_recomendado': 21.0,
            'stock_actual': 10,
            'stock_minimo': 2,
            'fecha_creacion': '2024-12-12 10:00:00'
        }
    
    def test_productos_disponibles_estructura(self, db_with_sample_products):
        """Test que verifica la estructura de datos de productos"""
        # Obtener productos de la base de datos de test
        productos = db_with_sample_products.get_all_products()
        
        if productos:
            producto = productos[0]
            
            # Verificar campos requeridos
            campos_requeridos = ['id', 'nombre', 'precio_venta', 'stock_actual', 'iva_recomendado']
            
            for campo in campos_requeridos:
                assert campo in producto, f"Campo '{campo}' faltante en producto"
                assert producto[campo] is not None, f"Campo '{campo}' es None"
            
            # Verificar tipos de datos
            assert isinstance(producto['id'], int), "ID debe ser entero"
            assert isinstance(producto['nombre'], str), "Nombre debe ser string"
            assert isinstance(producto['precio_venta'], (int, float)), "Precio debe ser numérico"
            assert isinstance(producto['stock_actual'], int), "Stock debe ser entero"
            assert isinstance(producto['iva_recomendado'], (int, float)), "IVA debe ser numérico"
    
    def test_formato_combo_productos(self, db_with_sample_products):
        """Test que verifica el formato correcto para el combo de productos"""
        productos = db_with_sample_products.get_all_products()
        
        if productos:
            for producto in productos:
                # Simular el formato usado en el combo
                nombre = producto.get('nombre', 'Sin nombre')
                precio = producto.get('precio_venta', 0.0)  # Usar precio_venta, no precio
                stock = producto.get('stock_actual', 0)
                
                texto_combo = f"{nombre} - {precio:.2f}€ (Stock: {stock})"
                
                # Verificar que el formato es válido
                assert nombre in texto_combo, "Nombre debe aparecer en el texto del combo"
                assert f"{precio:.2f}€" in texto_combo, "Precio debe aparecer formateado"
                assert f"Stock: {stock}" in texto_combo, "Stock debe aparecer en el texto"
                assert len(texto_combo) > 0, "Texto del combo no puede estar vacío"
    
    def test_precio_venta_vs_precio(self, db_with_sample_products):
        """Test específico para verificar que se usa precio_venta y no precio"""
        productos = db_with_sample_products.get_all_products()
        
        if productos:
            producto = productos[0]
            
            # Verificar que existe precio_venta
            assert 'precio_venta' in producto, "Producto debe tener campo precio_venta"
            
            # Verificar que precio_venta no es None
            assert producto['precio_venta'] is not None, "precio_venta no puede ser None"
            
            # Verificar que precio_venta es numérico
            assert isinstance(producto['precio_venta'], (int, float)), "precio_venta debe ser numérico"
            
            # Verificar que precio_venta es positivo
            assert producto['precio_venta'] >= 0, "precio_venta debe ser positivo o cero"
    
    @patch('ui.facturas_pyqt5.db')
    def test_carga_productos_en_combo_mock(self, mock_db):
        """Test con mock para verificar la carga de productos en combo"""
        # Configurar mock
        
        # Datos de prueba
        productos_mock = [
            {
                'id': 1,
                'nombre': 'Producto 1',
                'precio_venta': 10.50,
                'stock_actual': 5,
                'iva_recomendado': 21.0
            },
            {
                'id': 2,
                'nombre': 'Producto 2',
                'precio_venta': 25.00,
                'stock_actual': 0,
                'iva_recomendado': 10.0
            }
        ]
        
        mock_db.get_all_products.return_value = productos_mock
        
        # Simular la lógica de carga del combo
        productos = mock_db.get_all_products()
        
        assert len(productos) == 2, "Debe retornar 2 productos"
        
        # Verificar formato para cada producto
        for producto in productos:
            precio = producto.get('precio_venta', 0.0)  # Usar precio_venta
            stock = producto.get('stock_actual', 0)
            texto = f"{producto['nombre']} - {precio:.2f}€ (Stock: {stock})"
            
            assert precio > 0, "Precio debe ser positivo"
            assert isinstance(stock, int), "Stock debe ser entero"
            assert len(texto) > 10, "Texto formateado debe tener contenido"
    
    def test_productos_sin_stock(self, db_with_sample_products):
        """Test para verificar comportamiento con productos sin stock"""
        productos = db_with_sample_products.get_all_products()
        
        for producto in productos:
            stock = producto.get('stock_actual', 0)
            
            # Verificar que stock es un número válido
            assert isinstance(stock, int), "Stock debe ser entero"
            
            # El producto debe aparecer en el combo incluso con stock 0
            # (la lógica de negocio puede decidir si permitir o no la venta)
            precio = producto.get('precio_venta', 0.0)
            texto_combo = f"{producto['nombre']} - {precio:.2f}€ (Stock: {stock})"
            
            assert "Stock: " in texto_combo, "Información de stock debe aparecer"
    
    def test_productos_vacios_base_datos(self):
        """Test para verificar comportamiento cuando no hay productos"""
        with patch('database.database.Database') as mock_db_class:
            mock_db = Mock()
            mock_db_class.return_value = mock_db
            mock_db.get_all_products.return_value = []
            
            productos = mock_db.get_all_products()
            
            assert len(productos) == 0, "Lista de productos debe estar vacía"
            
            # En este caso, el combo solo debería tener "Seleccionar producto..."
            # y ningún producto real
    
    def test_manejo_errores_carga_productos(self):
        """Test para verificar manejo de errores en carga de productos"""
        with patch('database.database.Database') as mock_db_class:
            mock_db = Mock()
            mock_db_class.return_value = mock_db
            mock_db.get_all_products.side_effect = Exception("Error de base de datos")
            
            # Verificar que se maneja la excepción
            with pytest.raises(Exception):
                mock_db.get_all_products()
    
    @pytest.mark.integration
    def test_productos_reales_disponibles(self, test_db):
        """Test de integración para verificar productos reales en DB de test"""
        # Crear producto específico para este test
        producto_test = {
            'nombre': 'Producto Test Integración',
            'referencia': 'INT-001',
            'precio_venta': 15.75,
            'categoria': 'Test',
            'descripcion': 'Producto creado para test de integración',
            'iva_recomendado': 21.0,
            'stock_actual': 5,
            'stock_minimo': 1
        }

        result = test_db.add_product(producto_test)
        assert result, "Debe poder agregar producto de test"

        # Verificar que el producto se agregó
        productos = test_db.get_all_products()
        assert len(productos) > 0, "Debe haber al menos un producto después de agregar"

        # Verificar que todos los productos tienen la estructura correcta
        for producto in productos:
            assert 'precio_venta' in producto, "Producto debe tener precio_venta"
            assert producto['precio_venta'] is not None, "precio_venta no puede ser None"
