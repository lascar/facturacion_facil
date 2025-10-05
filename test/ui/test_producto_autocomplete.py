# -*- coding: utf-8 -*-
"""
Tests para el componente de autocompletado de productos
"""
import pytest
import tkinter as tk
import customtkinter as ctk
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.producto_autocomplete import ProductoAutocomplete
from database.models import Producto
from test.conftest import temp_db

class TestProductoAutocomplete:
    """Tests para ProductoAutocomplete"""
    
    @pytest.fixture
    def root_window(self):
        """Fixture para crear una ventana root"""
        ctk.set_appearance_mode("light")
        root = ctk.CTk()
        root.withdraw()  # Ocultar la ventana
        yield root
        root.destroy()
    
    @pytest.fixture
    def sample_productos(self, temp_db):
        """Fixture para crear productos de ejemplo"""
        productos = []
        
        # Crear productos de ejemplo
        producto1 = Producto(
            nombre="Laptop Dell Inspiron",
            referencia="DELL001",
            precio=899.99,
            categoria="Informática",
            descripcion="Laptop para oficina",
            iva_recomendado=21.0
        )
        producto1.save()
        productos.append(producto1)
        
        producto2 = Producto(
            nombre="Mouse Logitech",
            referencia="LOG001",
            precio=25.50,
            categoria="Periféricos",
            descripcion="Mouse óptico",
            iva_recomendado=21.0
        )
        producto2.save()
        productos.append(producto2)
        
        producto3 = Producto(
            nombre="Teclado Mecánico",
            referencia="TEC001",
            precio=75.00,
            categoria="Periféricos",
            descripcion="Teclado gaming",
            iva_recomendado=21.0
        )
        producto3.save()
        productos.append(producto3)
        
        return productos
    
    def test_autocomplete_initialization(self, root_window, sample_productos):
        """Test que el autocompletado se inicializa correctamente"""
        autocomplete = ProductoAutocomplete(root_window)
        
        assert autocomplete is not None
        assert hasattr(autocomplete, 'entry')
        assert hasattr(autocomplete, 'dropdown_frame')
        assert hasattr(autocomplete, 'suggestions_listbox')
        
        # Verificar que se cargaron los productos
        assert len(autocomplete.suggestions_data) == 3
    
    def test_search_by_name(self, root_window, sample_productos):
        """Test búsqueda por nombre de producto"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Simular búsqueda por "laptop"
        autocomplete.filter_suggestions("laptop")
        
        assert len(autocomplete.filtered_suggestions) == 1
        assert autocomplete.filtered_suggestions[0]['nombre'] == "Laptop Dell Inspiron"
    
    def test_search_by_reference(self, root_window, sample_productos):
        """Test búsqueda por referencia"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Simular búsqueda por "LOG"
        autocomplete.filter_suggestions("LOG")
        
        assert len(autocomplete.filtered_suggestions) == 1
        assert autocomplete.filtered_suggestions[0]['referencia'] == "LOG001"
    
    def test_search_by_category(self, root_window, sample_productos):
        """Test búsqueda por categoría"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Simular búsqueda por "Periféricos"
        autocomplete.filter_suggestions("Periféricos")
        
        assert len(autocomplete.filtered_suggestions) == 2
        categorias = [item['categoria'] for item in autocomplete.filtered_suggestions]
        assert all(cat == "Periféricos" for cat in categorias)
    
    def test_case_insensitive_search(self, root_window, sample_productos):
        """Test que la búsqueda es insensible a mayúsculas"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Búsqueda en minúsculas
        autocomplete.filter_suggestions("dell")
        assert len(autocomplete.filtered_suggestions) == 1
        
        # Búsqueda en mayúsculas
        autocomplete.filter_suggestions("DELL")
        assert len(autocomplete.filtered_suggestions) == 1
        
        # Búsqueda mixta
        autocomplete.filter_suggestions("DeLl")
        assert len(autocomplete.filtered_suggestions) == 1
    
    def test_min_chars_filter(self, root_window, sample_productos):
        """Test que respeta el mínimo de caracteres"""
        autocomplete = ProductoAutocomplete(root_window, min_chars=3)
        
        # Con menos de 3 caracteres no debe filtrar
        autocomplete.filter_suggestions("de")
        assert len(autocomplete.filtered_suggestions) == 0
        
        # Con 3 o más caracteres debe filtrar
        autocomplete.filter_suggestions("del")
        assert len(autocomplete.filtered_suggestions) == 1
    
    def test_max_suggestions_limit(self, root_window, sample_productos):
        """Test que respeta el límite máximo de sugerencias"""
        autocomplete = ProductoAutocomplete(root_window, max_suggestions=2)
        
        # Crear más productos para probar el límite
        for i in range(5):
            producto = Producto(
                nombre=f"Producto Test {i}",
                referencia=f"TEST{i:03d}",
                precio=10.0 + i,
                categoria="Test"
            )
            producto.save()
        
        # Recargar datos
        autocomplete.refresh_data()
        
        # Buscar por "Test" debería devolver máximo 2 resultados
        autocomplete.filter_suggestions("Test")
        assert len(autocomplete.filtered_suggestions) <= 2
    
    def test_selection_by_id(self, root_window, sample_productos):
        """Test selección de producto por ID"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Seleccionar primer producto por ID
        producto_id = sample_productos[0].id
        success = autocomplete.set_producto_by_id(producto_id)
        
        assert success == True
        assert autocomplete.get_selected_producto_id() == producto_id
        assert autocomplete.get_selected_producto().nombre == "Laptop Dell Inspiron"
    
    def test_selection_by_reference(self, root_window, sample_productos):
        """Test selección de producto por referencia"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Seleccionar producto por referencia
        success = autocomplete.set_producto_by_referencia("LOG001")
        
        assert success == True
        assert autocomplete.get_selected_producto().referencia == "LOG001"
        assert autocomplete.get_selected_producto().nombre == "Mouse Logitech"
    
    def test_validation(self, root_window, sample_productos):
        """Test validación de selección"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Sin selección debe fallar validación
        assert autocomplete.validate_selection() == False
        assert "Debe seleccionar un producto" in autocomplete.get_validation_error()
        
        # Con selección válida debe pasar validación
        autocomplete.set_producto_by_id(sample_productos[0].id)
        assert autocomplete.validate_selection() == True
        assert autocomplete.get_validation_error() == ""
    
    def test_clear_selection(self, root_window, sample_productos):
        """Test limpiar selección"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Seleccionar un producto
        autocomplete.set_producto_by_id(sample_productos[0].id)
        assert autocomplete.get_selected_producto() is not None
        
        # Limpiar selección
        autocomplete.clear()
        assert autocomplete.get_selected_producto() is None
        assert autocomplete.get_value() == ""
    
    def test_refresh_data(self, root_window, sample_productos):
        """Test refrescar datos"""
        autocomplete = ProductoAutocomplete(root_window)
        
        initial_count = len(autocomplete.suggestions_data)
        
        # Añadir un nuevo producto
        nuevo_producto = Producto(
            nombre="Producto Nuevo",
            referencia="NEW001",
            precio=50.0,
            categoria="Nueva"
        )
        nuevo_producto.save()
        
        # Refrescar datos
        autocomplete.refresh_data()
        
        # Debe tener un producto más
        assert len(autocomplete.suggestions_data) == initial_count + 1
        
        # Debe poder encontrar el nuevo producto
        autocomplete.filter_suggestions("Nuevo")
        assert len(autocomplete.filtered_suggestions) == 1
        assert autocomplete.filtered_suggestions[0]['nombre'] == "Producto Nuevo"
    
    def test_callback_execution(self, root_window, sample_productos):
        """Test que se ejecuta el callback al seleccionar"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Variable para capturar el callback
        callback_data = {}
        
        def test_callback(producto_data):
            callback_data['called'] = True
            callback_data['producto'] = producto_data
        
        # Configurar callback
        autocomplete.set_on_select_callback(test_callback)
        
        # Seleccionar producto
        autocomplete.set_producto_by_id(sample_productos[0].id)
        
        # Verificar que se ejecutó el callback
        assert callback_data.get('called') == True
        assert callback_data.get('producto') is not None
        assert callback_data['producto']['nombre'] == "Laptop Dell Inspiron"
    
    def test_display_text_format(self, root_window, sample_productos):
        """Test formato del texto de display"""
        autocomplete = ProductoAutocomplete(root_window)
        
        # Obtener primer producto
        producto_data = autocomplete.suggestions_data[0]
        
        # Verificar formato del display text
        display_text = producto_data['display_text']
        
        # Debe contener nombre, referencia y precio
        assert producto_data['nombre'] in display_text
        assert producto_data['referencia'] in display_text
        assert "€" in display_text
        
        # Verificar formato del texto de selección
        selected_text = autocomplete.get_selected_display_text(producto_data)
        assert producto_data['nombre'] in selected_text
        assert producto_data['referencia'] in selected_text

if __name__ == "__main__":
    # Ejecutar tests si se ejecuta directamente
    pytest.main([__file__, "-v"])
