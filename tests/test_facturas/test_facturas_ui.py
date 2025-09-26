# -*- coding: utf-8 -*-
"""
Tests para la interfaz de usuario de facturas
"""
import pytest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
from ui.producto_factura_dialog import ProductoFacturaDialog
from database.models import Producto

class TestProductoFacturaDialog:
    """Tests para ProductoFacturaDialog"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.root = tk.Tk()
        self.root.withdraw()
    
    def teardown_method(self):
        """Cleanup después de cada test"""
        if self.root:
            self.root.destroy()
    
    @pytest.fixture
    def sample_productos(self):
        """Productos de ejemplo para tests"""
        productos = []
        for i in range(3):
            producto = Mock(spec=Producto)
            producto.id = i + 1
            producto.nombre = f"Producto {i + 1}"
            producto.referencia = f"PROD-{i + 1:03d}"
            producto.precio = 10.0 * (i + 1)
            producto.categoria = "Test"
            producto.iva_recomendado = 21.0
            producto.descripcion = f"Descripción {i + 1}"
            productos.append(producto)
        return productos
    
    @patch('customtkinter.CTkToplevel')
    @patch('utils.logger.get_logger')
    @patch.object(ProductoFacturaDialog, 'create_widgets')
    def test_dialog_creation(self, mock_create_widgets, mock_get_logger, mock_toplevel, sample_productos):
        """Test creación del diálogo"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_window = Mock()
        mock_toplevel.return_value = mock_window

        dialog = ProductoFacturaDialog(self.root, sample_productos)
        
        # Verificar configuración básica
        mock_toplevel.assert_called_once_with(self.root)
        mock_window.title.assert_called_once_with("Agregar/Editar Producto")
        mock_window.geometry.assert_called_once_with("500x600")
        mock_window.transient.assert_called_once_with(self.root)
        mock_window.grab_set.assert_called_once()
        
        assert dialog.parent == self.root
        assert dialog.productos_disponibles == sample_productos
        assert dialog.result is None
    
    @patch('customtkinter.CTkToplevel')
    @patch('utils.logger.get_logger')
    def test_dialog_with_initial_values(self, mock_get_logger, mock_toplevel, sample_productos):
        """Test creación del diálogo con valores iniciales"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_window = Mock()
        mock_toplevel.return_value = mock_window
        
        producto_inicial = sample_productos[0]
        
        with patch.object(ProductoFacturaDialog, 'create_widgets'), \
             patch.object(ProductoFacturaDialog, 'load_producto_data') as mock_load:
            
            dialog = ProductoFacturaDialog(
                self.root, 
                sample_productos,
                producto_seleccionado=producto_inicial,
                cantidad_inicial=5,
                precio_inicial=15.0,
                iva_inicial=10.0,
                descuento_inicial=5.0
            )
            
            assert dialog.producto_seleccionado == producto_inicial
            assert dialog.cantidad_inicial == 5
            assert dialog.precio_inicial == 15.0
            assert dialog.iva_inicial == 10.0
            assert dialog.descuento_inicial == 5.0
            mock_load.assert_called_once()
    
    def test_validate_form_valid_data(self, sample_productos):
        """Test validación con datos válidos"""
        with patch('customtkinter.CTkToplevel'), \
             patch('utils.logger.get_logger'), \
             patch.object(ProductoFacturaDialog, 'create_widgets'):

            dialog = ProductoFacturaDialog(self.root, sample_productos)
            dialog.producto_seleccionado = sample_productos[0]

            # Mock de los campos del formulario
            dialog.cantidad_entry = Mock()
            dialog.cantidad_entry.get.return_value = "2"

            dialog.precio_entry = Mock()
            dialog.precio_entry.get.return_value = "15.50"

            dialog.iva_entry = Mock()
            dialog.iva_entry.get.return_value = "21.0"

            dialog.descuento_entry = Mock()
            dialog.descuento_entry.get.return_value = "10.0"

            with patch('common.ui_components.FormHelper.get_entry_value') as mock_get_value, \
                 patch('database.models.Stock.get_by_product', return_value=10) as mock_stock:
                mock_get_value.side_effect = ["2", "15.50", "21.0", "10.0"]

                errors = dialog.validate_form()
                assert len(errors) == 0
    
    def test_validate_form_invalid_data(self, sample_productos):
        """Test validación con datos inválidos"""
        with patch('customtkinter.CTkToplevel'), \
             patch('utils.logger.get_logger'), \
             patch.object(ProductoFacturaDialog, 'create_widgets'):

            dialog = ProductoFacturaDialog(self.root, sample_productos)
            dialog.producto_seleccionado = None  # Sin producto seleccionado

            # Mock de los campos del formulario
            dialog.cantidad_entry = Mock()
            dialog.precio_entry = Mock()
            dialog.iva_entry = Mock()
            dialog.descuento_entry = Mock()

            with patch('common.ui_components.FormHelper.get_entry_value') as mock_get_value:
                mock_get_value.side_effect = ["-1", "abc", "150", "200"]  # Valores inválidos

                errors = dialog.validate_form()
                assert len(errors) > 0

                # Verificar que hay error por no seleccionar producto
                assert any("seleccionar un producto" in error.lower() for error in errors)
    
    def test_update_preview(self, sample_productos):
        """Test actualización del preview de totales"""
        with patch('customtkinter.CTkToplevel'), \
             patch('utils.logger.get_logger'), \
             patch.object(ProductoFacturaDialog, 'create_widgets'):

            dialog = ProductoFacturaDialog(self.root, sample_productos)

            # Mock de los campos del formulario
            dialog.cantidad_entry = Mock()
            dialog.precio_entry = Mock()
            dialog.iva_entry = Mock()
            dialog.descuento_entry = Mock()

            # Mock de los labels de preview
            dialog.subtotal_preview = Mock()
            dialog.descuento_preview = Mock()
            dialog.iva_preview = Mock()
            dialog.total_preview = Mock()
            
            with patch('common.ui_components.FormHelper.get_entry_value') as mock_get_value:
                mock_get_value.side_effect = ["2", "10.0", "21.0", "10.0"]
                
                with patch('common.validators.CalculationHelper.calculate_line_total') as mock_calc:
                    mock_calc.return_value = {
                        'subtotal': 18.0,
                        'descuento_amount': 2.0,
                        'iva_amount': 3.78,
                        'total': 21.78
                    }
                    
                    with patch('common.validators.CalculationHelper.format_currency') as mock_format:
                        mock_format.side_effect = ["18.00 €", "2.00 €", "3.78 €", "21.78 €"]
                        
                        dialog.update_preview()
                        
                        # Verificar que se actualizaron los labels
                        dialog.subtotal_preview.configure.assert_called_with(text="18.00 €")
                        dialog.descuento_preview.configure.assert_called_with(text="2.00 €")
                        dialog.iva_preview.configure.assert_called_with(text="3.78 €")
                        dialog.total_preview.configure.assert_called_with(text="21.78 €")
    
    def test_accept_valid_form(self, sample_productos):
        """Test aceptar diálogo con formulario válido"""
        with patch('customtkinter.CTkToplevel') as mock_toplevel, \
             patch('utils.logger.get_logger'), \
             patch.object(ProductoFacturaDialog, 'create_widgets'):

            mock_window = Mock()
            mock_toplevel.return_value = mock_window

            dialog = ProductoFacturaDialog(self.root, sample_productos)
            dialog.producto_seleccionado = sample_productos[0]

            # Mock de los campos del formulario
            dialog.cantidad_entry = Mock()
            dialog.precio_entry = Mock()
            dialog.iva_entry = Mock()
            dialog.descuento_entry = Mock()

            with patch.object(dialog, 'validate_form', return_value=[]), \
                 patch('common.ui_components.FormHelper.get_entry_value') as mock_get_value:

                mock_get_value.side_effect = ["3", "25.0", "21.0", "5.0"]

                dialog.accept()
                
                # Verificar resultado
                expected_result = (sample_productos[0].id, 3, 25.0, 21.0, 5.0)
                assert dialog.result == expected_result
                mock_window.destroy.assert_called_once()
    
    def test_accept_invalid_form(self, sample_productos):
        """Test aceptar diálogo con formulario inválido"""
        with patch('customtkinter.CTkToplevel') as mock_toplevel, \
             patch('utils.logger.get_logger'), \
             patch.object(ProductoFacturaDialog, 'create_widgets'):
            
            mock_window = Mock()
            mock_toplevel.return_value = mock_window
            
            dialog = ProductoFacturaDialog(self.root, sample_productos)
            
            with patch.object(dialog, 'validate_form', return_value=["Error de validación"]), \
                 patch('tkinter.messagebox.showerror') as mock_error:
                
                dialog.accept()
                
                # Verificar que se mostró error y no se cerró el diálogo
                mock_error.assert_called_once()
                assert dialog.result is None
                mock_window.destroy.assert_not_called()
    
    def test_cancel(self, sample_productos):
        """Test cancelar diálogo"""
        with patch('customtkinter.CTkToplevel') as mock_toplevel, \
             patch('utils.logger.get_logger'), \
             patch.object(ProductoFacturaDialog, 'create_widgets'):
            
            mock_window = Mock()
            mock_toplevel.return_value = mock_window
            
            dialog = ProductoFacturaDialog(self.root, sample_productos)
            
            dialog.cancel()
            
            assert dialog.result is None
            mock_window.destroy.assert_called_once()
    
    def test_on_producto_selected(self, sample_productos):
        """Test selección de producto"""
        with patch('customtkinter.CTkToplevel'), \
             patch('utils.logger.get_logger'), \
             patch.object(ProductoFacturaDialog, 'create_widgets'):
            
            dialog = ProductoFacturaDialog(self.root, sample_productos)
            
            # Mock de los widgets
            dialog.producto_combo = Mock()
            dialog.producto_combo.get.return_value = f"{sample_productos[0].nombre} ({sample_productos[0].referencia}) - 10.00 €"
            
            dialog.info_label = Mock()
            dialog.precio_entry = Mock()
            dialog.iva_entry = Mock()
            
            with patch.object(dialog, 'update_preview') as mock_update, \
                 patch('common.ui_components.FormHelper.set_entry_value') as mock_set_value:
                
                dialog.precio_inicial = None
                dialog.iva_inicial = None
                
                dialog.on_producto_selected(dialog.producto_combo.get.return_value)
                
                # Verificar que se seleccionó el producto
                assert dialog.producto_seleccionado == sample_productos[0]
                
                # Verificar que se actualizó la información
                dialog.info_label.configure.assert_called_once()
                
                # Verificar que se establecieron valores por defecto
                assert mock_set_value.call_count == 2  # precio e iva
                mock_update.assert_called_once()

class TestFacturasUI:
    """Tests para componentes UI de facturas"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.root = tk.Tk()
        self.root.withdraw()
    
    def teardown_method(self):
        """Cleanup después de cada test"""
        if self.root:
            self.root.destroy()
    
    @patch('ui.facturas.FacturasWindow.__init__', return_value=None)
    def test_facturas_window_import(self, mock_init):
        """Test que se puede importar FacturasWindow"""
        from ui.facturas import FacturasWindow
        
        # Verificar que la clase existe
        assert FacturasWindow is not None
        
        # Intentar crear instancia (mock)
        window = FacturasWindow.__new__(FacturasWindow)
        assert window is not None
    
    def test_facturas_methods_mixin_import(self):
        """Test que se puede importar FacturasMethodsMixin"""
        from ui.facturas_methods import FacturasMethodsMixin
        
        # Verificar que la clase existe
        assert FacturasMethodsMixin is not None
        
        # Verificar que tiene los métodos esperados
        expected_methods = [
            'validate_factura_form',
            'agregar_producto',
            'editar_producto_factura',
            'eliminar_producto_factura',
            'update_productos_tree',
            'update_totales',
            'guardar_factura'
        ]
        
        for method_name in expected_methods:
            assert hasattr(FacturasMethodsMixin, method_name), f"Método {method_name} no encontrado"
    
    @patch('customtkinter.CTkToplevel')
    @patch('utils.logger.get_logger')
    def test_base_window_inheritance(self, mock_get_logger, mock_toplevel):
        """Test que BaseWindow se puede usar como clase base"""
        from common.ui_components import BaseWindow
        
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_window = Mock()
        mock_toplevel.return_value = mock_window
        
        # Crear instancia de BaseWindow
        base_window = BaseWindow(self.root, "Test Window")
        
        # Verificar que tiene los métodos esperados
        assert hasattr(base_window, '_show_message')
        assert hasattr(base_window, 'setup_scrollable_frame')
        assert hasattr(base_window, 'configure_mousewheel_scrolling')
        assert hasattr(base_window, 'bind_mousewheel_to_scrollable')
        
        # Verificar configuración inicial
        assert base_window.imagen_path == ""
