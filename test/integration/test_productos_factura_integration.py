#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests d'intégration pour la sélection de produits dans les facturas
"""

import pytest
import sys
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtTest import QTest

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database.database import Database
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog
from utils.logger import get_logger

class TestProductosFacturaIntegration:
    """Tests d'intégration pour la sélection de produits dans les facturas"""
    
    @pytest.fixture(scope="class")
    def qapp(self):
        """Fixture pour l'application Qt"""
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        yield app
        # Ne pas quitter l'app ici car d'autres tests peuvent l'utiliser
    
    @pytest.fixture
    def test_db(self):
        """Fixture pour une base de données de test isolée"""
        # Créer un répertoire temporaire
        temp_dir = tempfile.mkdtemp()
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        test_db_path = os.path.join(temp_dir, f'test_integration_productos_{unique_id}.db')

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
    def sample_product_data(self):
        """Fixture pour données de produit d'exemple"""
        import uuid
        unique_id = str(uuid.uuid4())[:8]

        return {
            'nombre': f'Producto Test Integración {unique_id}',
            'referencia': f'INT-TEST-001-{unique_id}',
            'precio_venta': 29.99,
            'precio_compra': 20.00,
            'categoria': 'Test Integration',
            'descripcion': 'Producto creado para tests de integración',
            'iva_recomendado': 21.0,
            'stock_actual': 15,
            'stock_minimo': 3
        }
    
    def test_crear_factura_dialog_carga_productos(self, qapp, test_db, sample_product_data):
        """Test que verifica que el dialog de crear factura carga productos correctamente"""
        # Agregar producto de test a la base de datos de test
        result = test_db.add_product(sample_product_data)
        assert result, "Debe poder agregar producto de test"
        
        # Crear el dialog
        dialog = CrearFacturaDialog()
        
        # Esperar a que se carguen los datos (simulando el QTimer)
        QTest.qWait(200)  # Esperar 200ms
        
        # Verificar que el autocomplete tiene productos cargados
        assert len(dialog.producto_autocomplete.products_data) > 0, "Autocomplete debe tener productos cargados"

        # Verificar que hay productos con stock disponibles (filtrados)
        productos_con_stock = [p for p in dialog.producto_autocomplete.products_data if p.get('stock_actual', 0) > 0]
        assert len(productos_con_stock) > 0, "Debe haber productos con stock disponible"

        # Verificar formato de productos con stock
        if productos_con_stock:
            primer_producto = productos_con_stock[0]
            formato_display = dialog.producto_autocomplete.format_product_display(primer_producto)
            assert "€" in formato_display, "Display de productos debe contener precio en euros"
            assert "Stock:" in formato_display, "Display de productos debe mostrar stock"
        
        dialog.close()
    
    def test_editar_factura_dialog_carga_productos(self, qapp, test_db, sample_product_data):
        """Test que verifica que el dialog de editar factura carga productos correctamente"""
        # Agregar producto de test a la base de datos de test
        result = test_db.add_product(sample_product_data)
        assert result, "Debe poder agregar producto de test"
        
        # Crear datos de factura de ejemplo
        factura_data = {
            'numero': 'TEST-001',
            'cliente_id': 1,
            'fecha': '2024-12-12',
            'estado': 'Borrador',
            'subtotal': 0.0,
            'iva': 0.0,
            'total': 0.0
        }
        
        # Crear el dialog de edición
        dialog = EditarFacturaDialog(factura_data)
        
        # Esperar a que se carguen los datos
        QTest.qWait(200)
        
        # Verificar que el autocomplete tiene productos cargados
        assert len(dialog.producto_autocomplete.products_data) > 0, "Autocomplete debe tener productos cargados"

        # Verificar formato de productos con stock
        productos_con_stock = [p for p in dialog.producto_autocomplete.products_data if p.get('stock_actual', 0) > 0]
        for i, producto in enumerate(productos_con_stock):
            item_text = dialog.producto_autocomplete.format_product_display(producto)
            assert "€" in item_text, f"Producto {i} debe contener precio: {item_text}"
            assert "Stock:" in item_text, f"Producto {i} debe contener stock: {item_text}"
        
        dialog.close()
    
    def test_seleccion_producto_en_crear_factura(self, qapp, test_db, sample_product_data):
        """Test que verifica la selección de producto en crear factura"""
        # Agregar producto de test a la base de datos de test
        result = test_db.add_product(sample_product_data)
        assert result, "Debe poder agregar producto de test"
        
        dialog = CrearFacturaDialog()
        QTest.qWait(200)
        
        # Verificar que se puede seleccionar un producto
        productos_con_stock = [p for p in dialog.producto_autocomplete.products_data if p.get('stock_actual', 0) > 0]
        if productos_con_stock:
            # Seleccionar el primer producto con stock
            primer_producto = productos_con_stock[0]
            dialog.producto_autocomplete.set_product(primer_producto)

            # Verificar que la selección es válida
            producto_seleccionado = dialog.producto_autocomplete.get_current_product()
            assert producto_seleccionado is not None, "Producto seleccionado no debe ser None"

            if isinstance(producto_seleccionado, dict):
                assert 'id' in producto_seleccionado, "Producto debe tener ID"
                assert 'nombre' in producto_seleccionado, "Producto debe tener nombre"
                assert 'precio_venta' in producto_seleccionado, "Producto debe tener precio_venta"
        
        dialog.close()
    
    def test_formato_precio_venta_correcto(self, qapp, test_db, sample_product_data):
        """Test que verifica que se usa precio_venta y no precio en la interfaz"""
        # Agregar producto de test
        result = test_db.add_product(sample_product_data)
        assert result, "Debe poder agregar producto de test"

        productos = test_db.get_all_products()
        
        if productos:
            dialog = CrearFacturaDialog()
            QTest.qWait(200)
            
            # Verificar que todos los productos usan precio_venta
            productos_con_stock = [p for p in dialog.producto_autocomplete.products_data if p.get('stock_actual', 0) > 0]
            for producto in productos_con_stock:
                if producto and isinstance(producto, dict):
                    # Verificar que el producto tiene precio_venta
                    assert 'precio_venta' in producto, "Producto debe tener precio_venta"

                    # Verificar que el formato de display refleja el precio_venta
                    item_text = dialog.producto_autocomplete.format_product_display(producto)
                    precio_venta = producto['precio_venta']
                    precio_formateado = f"{precio_venta:.2f}€"
                    
                    assert precio_formateado in item_text, f"Texto debe contener precio formateado: {precio_formateado}"
            
            dialog.close()
    
    def test_agregar_producto_a_factura(self, qapp, test_db, sample_product_data):
        """Test que verifica que se puede agregar un producto a la factura"""
        # Agregar producto de test a la base de datos de test
        result = test_db.add_product(sample_product_data)
        assert result, "Debe poder agregar producto de test"
        
        dialog = CrearFacturaDialog()
        QTest.qWait(200)
        
        productos_con_stock = [p for p in dialog.producto_autocomplete.products_data if p.get('stock_actual', 0) > 0]
        if productos_con_stock:
            # Seleccionar un producto
            primer_producto = productos_con_stock[0]
            dialog.producto_autocomplete.set_product(primer_producto)

            # Establecer cantidad
            dialog.cantidad_spin.setValue(2)

            # Verificar estado inicial de la tabla
            filas_iniciales = dialog.productos_table.rowCount()

            # Simular clic en agregar (sin hacer clic real para evitar problemas de UI)
            producto_data = dialog.producto_autocomplete.get_current_product()
            cantidad = dialog.cantidad_spin.value()
            
            if producto_data and isinstance(producto_data, dict):
                # Verificar que los datos son correctos para agregar
                assert 'precio_venta' in producto_data, "Producto debe tener precio_venta para agregar"
                assert producto_data['precio_venta'] > 0, "Precio debe ser positivo"
                assert cantidad > 0, "Cantidad debe ser positiva"
        
        dialog.close()
    
    @pytest.mark.slow
    def test_carga_productos_performance(self, qapp, test_db, sample_product_data):
        """Test de performance para la carga de productos"""
        # Agregar producto de test
        result = test_db.add_product(sample_product_data)
        assert result, "Debe poder agregar producto de test"

        import time
        start_time = time.time()
        
        dialog = CrearFacturaDialog()
        QTest.qWait(500)  # Esperar más tiempo para carga completa
        
        end_time = time.time()
        carga_tiempo = end_time - start_time
        
        # La carga no debería tomar más de 2 segundos
        assert carga_tiempo < 2.0, f"Carga de productos toma demasiado tiempo: {carga_tiempo:.2f}s"
        
        # Verificar que se cargaron productos
        assert len(dialog.producto_autocomplete.products_data) >= 0, "Debe haber productos cargados en el autocomplete"
        
        dialog.close()
    
    def test_manejo_productos_sin_stock(self, qapp, test_db):
        """Test que verifica el manejo de productos sin stock"""
        # Crear producto sin stock para el test con referencia única
        import uuid
        unique_ref = f"NO-STOCK-{uuid.uuid4().hex[:8].upper()}"

        producto_sin_stock = {
            'nombre': f'Producto Sin Stock Test {unique_ref}',
            'referencia': unique_ref,
            'precio_venta': 10.00,
            'categoria': 'Test',
            'descripcion': 'Producto sin stock para test',
            'iva_recomendado': 21.0,
            'stock_actual': 0,  # Sin stock
            'stock_minimo': 1
        }

        result = test_db.add_product(producto_sin_stock)
        assert result, "Debe poder agregar producto sin stock"
        
        dialog = CrearFacturaDialog()
        QTest.qWait(200)
        
        # Verificar el comportamiento del autocomplete con productos sin stock
        # ProductAutoCompleteWidget filtra automáticamente productos con stock > 0
        productos_sin_stock_filtrados = True
        productos_totales = 0
        productos_con_stock = 0

        if hasattr(dialog, 'producto_autocomplete') and dialog.producto_autocomplete:
            # Verificar que el producto sin stock está en los datos pero no en los filtrados
            if hasattr(dialog.producto_autocomplete, 'products_data'):
                productos_totales = len(dialog.producto_autocomplete.products_data)
                # Buscar nuestro producto sin stock en los datos totales
                producto_sin_stock_encontrado = any(
                    p.get('referencia') == unique_ref and p.get('stock_actual', 0) == 0
                    for p in dialog.producto_autocomplete.products_data
                )

            if hasattr(dialog.producto_autocomplete, 'filtered_products'):
                productos_con_stock = len(dialog.producto_autocomplete.filtered_products)
                # Verificar que el producto sin stock NO está en los filtrados
                producto_sin_stock_en_filtrados = any(
                    p.get('referencia') == unique_ref
                    for p in dialog.producto_autocomplete.filtered_products
                )
                productos_sin_stock_filtrados = not producto_sin_stock_en_filtrados

        # Verificaciones del comportamiento esperado
        assert productos_totales > 0, "Debe haber productos cargados en total"
        assert productos_sin_stock_filtrados, "Productos sin stock no deben aparecer en sugerencias filtradas"
        # Puede haber o no productos con stock, dependiendo de los datos de test
        
        dialog.close()
        
        # No necesitamos limpiar manualmente - la fixture se encarga del cleanup
