# -*- coding: utf-8 -*-
"""
Tests para el sistema de ordenación de TreeView
"""
import pytest
import tkinter as tk
from tkinter import ttk
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.treeview_sorter import TreeViewSorter, add_sorting_to_treeview

class TestTreeViewSorter:
    """Tests para la clase TreeViewSorter"""
    
    @pytest.fixture
    def root_window(self):
        """Fixture para crear una ventana root de tkinter"""
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana
        yield root
        root.destroy()
    
    @pytest.fixture
    def sample_treeview(self, root_window):
        """Fixture para crear un TreeView de ejemplo"""
        columns = ('nombre', 'precio', 'fecha', 'cantidad')
        tree = ttk.Treeview(root_window, columns=columns, show='headings')
        
        # Configurar encabezados
        tree.heading('nombre', text='Nombre')
        tree.heading('precio', text='Precio')
        tree.heading('fecha', text='Fecha')
        tree.heading('cantidad', text='Cantidad')
        
        # Datos de ejemplo
        sample_data = [
            ('Producto A', '€25.50', '2024-01-15', '10'),
            ('Producto B', '€15.75', '2024-02-20', '5'),
            ('Producto C', '€35.00', '2024-01-10', '20'),
            ('Producto D', '€8.25', '2024-03-05', '2'),
            ('Producto E', '€45.99', '2024-02-28', '15')
        ]
        
        for data in sample_data:
            tree.insert('', 'end', values=data)
        
        return tree
    
    def test_sorter_initialization(self, sample_treeview):
        """Test que el sorter se inicializa correctamente"""
        sorter = TreeViewSorter(sample_treeview)
        
        assert sorter.treeview == sample_treeview
        assert len(sorter.sort_columns) == 4  # 4 columnas
        
        # Verificar que todas las columnas tienen configuración inicial
        for col in ['nombre', 'precio', 'fecha', 'cantidad']:
            assert col in sorter.sort_columns
            assert sorter.sort_columns[col]['reverse'] == False
            assert 'type' in sorter.sort_columns[col]
    
    def test_data_type_detection(self, sample_treeview):
        """Test que la detección de tipos de datos funciona"""
        sorter = TreeViewSorter(sample_treeview)
        
        # Obtener datos de ejemplo para cada columna
        items = [(sample_treeview.set(item, 'precio'), item) for item in sample_treeview.get_children('')]
        
        # Test detección de moneda
        data_type = sorter.detect_data_type(items, 'precio')
        assert data_type == 'currency'
        
        # Test detección de texto
        items_text = [(sample_treeview.set(item, 'nombre'), item) for item in sample_treeview.get_children('')]
        data_type = sorter.detect_data_type(items_text, 'nombre')
        assert data_type == 'text'
        
        # Test detección de fecha
        items_date = [(sample_treeview.set(item, 'fecha'), item) for item in sample_treeview.get_children('')]
        data_type = sorter.detect_data_type(items_date, 'fecha')
        assert data_type == 'date'
        
        # Test detección de número
        items_numeric = [(sample_treeview.set(item, 'cantidad'), item) for item in sample_treeview.get_children('')]
        data_type = sorter.detect_data_type(items_numeric, 'cantidad')
        assert data_type == 'numeric'
    
    def test_currency_parsing(self, sample_treeview):
        """Test que el parsing de moneda funciona correctamente"""
        sorter = TreeViewSorter(sample_treeview)
        
        assert sorter.parse_currency('€25.50') == 25.50
        assert sorter.parse_currency('€15.75') == 15.75
        assert sorter.parse_currency('$100.00') == 100.00
        assert sorter.parse_currency('invalid') == 0.0
    
    def test_numeric_parsing(self, sample_treeview):
        """Test que el parsing numérico funciona correctamente"""
        sorter = TreeViewSorter(sample_treeview)
        
        assert sorter.parse_numeric('10') == 10.0
        assert sorter.parse_numeric('25.5') == 25.5
        assert sorter.parse_numeric('1,234.56') == 1234.56
        assert sorter.parse_numeric('invalid') == 0.0
    
    def test_date_parsing(self, sample_treeview):
        """Test que el parsing de fechas funciona correctamente"""
        sorter = TreeViewSorter(sample_treeview)
        
        from datetime import datetime
        
        # Test formato YYYY-MM-DD
        result = sorter.parse_date('2024-01-15')
        expected = datetime(2024, 1, 15)
        assert result == expected
        
        # Test formato DD/MM/YYYY
        result = sorter.parse_date('15/01/2024')
        expected = datetime(2024, 1, 15)
        assert result == expected
        
        # Test fecha inválida
        result = sorter.parse_date('invalid')
        assert result == datetime.min
    
    def test_sorting_by_text(self, sample_treeview):
        """Test ordenación por texto"""
        sorter = TreeViewSorter(sample_treeview)
        
        # Obtener orden inicial
        initial_order = [sample_treeview.set(item, 'nombre') for item in sample_treeview.get_children('')]
        
        # Ordenar por nombre
        sorter.sort_by_column('nombre')
        
        # Obtener orden después de ordenar
        sorted_order = [sample_treeview.set(item, 'nombre') for item in sample_treeview.get_children('')]
        
        # Verificar que el orden cambió y está ordenado
        assert sorted_order != initial_order
        assert sorted_order == sorted(initial_order, key=str.lower)
    
    def test_sorting_by_currency(self, sample_treeview):
        """Test ordenación por moneda"""
        sorter = TreeViewSorter(sample_treeview)
        
        # Ordenar por precio
        sorter.sort_by_column('precio')
        
        # Obtener precios ordenados
        sorted_prices = [sample_treeview.set(item, 'precio') for item in sample_treeview.get_children('')]
        
        # Convertir a números para verificar orden
        numeric_prices = [sorter.parse_currency(price) for price in sorted_prices]
        
        # Verificar que están ordenados ascendentemente
        assert numeric_prices == sorted(numeric_prices)
    
    def test_reverse_sorting(self, sample_treeview):
        """Test ordenación inversa"""
        sorter = TreeViewSorter(sample_treeview)
        
        # Primera ordenación (ascendente)
        sorter.sort_by_column('nombre')
        first_sort = [sample_treeview.set(item, 'nombre') for item in sample_treeview.get_children('')]
        
        # Segunda ordenación (descendente)
        sorter.sort_by_column('nombre')
        second_sort = [sample_treeview.set(item, 'nombre') for item in sample_treeview.get_children('')]
        
        # Verificar que el segundo orden es el inverso del primero
        assert second_sort == list(reversed(first_sort))
    
    def test_column_indicators(self, sample_treeview):
        """Test que los indicadores de columna se actualizan correctamente"""
        sorter = TreeViewSorter(sample_treeview)
        
        # Verificar indicadores iniciales
        for col in ['nombre', 'precio', 'fecha', 'cantidad']:
            header_text = sample_treeview.heading(col, 'text')
            assert header_text.endswith(' ↕')
        
        # Ordenar por una columna
        sorter.sort_by_column('nombre')
        
        # Verificar que la columna ordenada tiene indicador de ascendente
        nombre_header = sample_treeview.heading('nombre', 'text')
        assert nombre_header.endswith(' ↑')
        
        # Verificar que otras columnas mantienen indicador neutral
        for col in ['precio', 'fecha', 'cantidad']:
            header_text = sample_treeview.heading(col, 'text')
            assert header_text.endswith(' ↕')
    
    def test_add_sorting_function(self, sample_treeview):
        """Test que la función de conveniencia funciona"""
        sorter = add_sorting_to_treeview(sample_treeview)
        
        assert isinstance(sorter, TreeViewSorter)
        assert sorter.treeview == sample_treeview
        
        # Verificar que el sorting funciona
        initial_order = [sample_treeview.set(item, 'nombre') for item in sample_treeview.get_children('')]
        sorter.sort_by_column('nombre')
        sorted_order = [sample_treeview.set(item, 'nombre') for item in sample_treeview.get_children('')]
        
        assert sorted_order != initial_order

if __name__ == "__main__":
    # Ejecutar tests si se ejecuta directamente
    pytest.main([__file__, "-v"])
