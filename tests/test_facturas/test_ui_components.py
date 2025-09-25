# -*- coding: utf-8 -*-
"""
Tests para los componentes UI comunes
"""
import pytest
import tkinter as tk
import customtkinter as ctk
from unittest.mock import Mock, patch, MagicMock
from common.ui_components import BaseWindow, ImageSelector, FormHelper

class TestFormHelper:
    """Tests para FormHelper"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana
    
    def teardown_method(self):
        """Cleanup después de cada test"""
        if self.root:
            self.root.destroy()
    
    def test_clear_entry(self):
        """Test limpiar campo de entrada"""
        entry = tk.Entry(self.root)
        entry.insert(0, "texto inicial")
        
        FormHelper.clear_entry(entry)
        assert entry.get() == ""
    
    def test_clear_entry_with_default(self):
        """Test limpiar campo con valor por defecto"""
        entry = tk.Entry(self.root)
        entry.insert(0, "texto inicial")
        
        FormHelper.clear_entry(entry, "valor por defecto")
        assert entry.get() == "valor por defecto"
    
    def test_clear_entry_invalid_widget(self):
        """Test limpiar campo con widget inválido"""
        # No debería lanzar excepción
        FormHelper.clear_entry(None)
        FormHelper.clear_entry("not a widget")
    
    def test_clear_text_widget(self):
        """Test limpiar widget de texto"""
        text = tk.Text(self.root)
        text.insert("1.0", "texto inicial")
        
        FormHelper.clear_text_widget(text)
        assert text.get("1.0", tk.END).strip() == ""
    
    def test_clear_text_widget_invalid(self):
        """Test limpiar widget de texto inválido"""
        # No debería lanzar excepción
        FormHelper.clear_text_widget(None)
        FormHelper.clear_text_widget("not a widget")
    
    def test_get_entry_value(self):
        """Test obtener valor de entrada"""
        entry = tk.Entry(self.root)
        entry.insert(0, "  valor con espacios  ")
        
        value = FormHelper.get_entry_value(entry)
        assert value == "valor con espacios"
    
    def test_get_entry_value_empty(self):
        """Test obtener valor de entrada vacía"""
        entry = tk.Entry(self.root)
        
        value = FormHelper.get_entry_value(entry, "default")
        assert value == "default"
    
    def test_get_entry_value_invalid_widget(self):
        """Test obtener valor de widget inválido"""
        value = FormHelper.get_entry_value(None, "default")
        assert value == "default"
    
    def test_get_text_value(self):
        """Test obtener valor de texto"""
        text = tk.Text(self.root)
        text.insert("1.0", "  texto con espacios  \n")
        
        value = FormHelper.get_text_value(text)
        assert value == "texto con espacios"
    
    def test_get_text_value_empty(self):
        """Test obtener valor de texto vacío"""
        text = tk.Text(self.root)
        
        value = FormHelper.get_text_value(text, "default")
        assert value == "default"
    
    def test_set_entry_value(self):
        """Test establecer valor de entrada"""
        entry = tk.Entry(self.root)
        entry.insert(0, "valor inicial")
        
        FormHelper.set_entry_value(entry, "nuevo valor")
        assert entry.get() == "nuevo valor"
    
    def test_set_entry_value_number(self):
        """Test establecer valor numérico"""
        entry = tk.Entry(self.root)
        
        FormHelper.set_entry_value(entry, 123.45)
        assert entry.get() == "123.45"
    
    def test_set_entry_value_invalid_widget(self):
        """Test establecer valor en widget inválido"""
        # No debería lanzar excepción
        FormHelper.set_entry_value(None, "value")
        FormHelper.set_entry_value("not a widget", "value")
    
    def test_set_text_value(self):
        """Test establecer valor de texto"""
        text = tk.Text(self.root)
        text.insert("1.0", "valor inicial")
        
        FormHelper.set_text_value(text, "nuevo valor")
        assert text.get("1.0", tk.END).strip() == "nuevo valor"
    
    def test_set_text_value_invalid_widget(self):
        """Test establecer valor en widget de texto inválido"""
        # No debería lanzar excepción
        FormHelper.set_text_value(None, "value")
        FormHelper.set_text_value("not a widget", "value")

class TestBaseWindow:
    """Tests para BaseWindow"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.root = tk.Tk()
        self.root.withdraw()
    
    def teardown_method(self):
        """Cleanup después de cada test"""
        if self.root:
            self.root.destroy()
    
    @patch('customtkinter.CTkToplevel')
    def test_base_window_creation(self, mock_toplevel):
        """Test creación de BaseWindow"""
        mock_window = Mock()
        mock_toplevel.return_value = mock_window
        
        base_window = BaseWindow(self.root, "Test Window", "800x600")
        
        # Verificar que se configuró correctamente
        mock_toplevel.assert_called_once_with(self.root)
        mock_window.title.assert_called_once_with("Test Window")
        mock_window.geometry.assert_called_once_with("800x600")
        mock_window.transient.assert_called_once_with(self.root)
        
        assert base_window.imagen_path == ""
    
    @patch('customtkinter.CTkToplevel')
    def test_base_window_show_message_info(self, mock_toplevel):
        """Test mostrar mensaje de información"""
        mock_window = Mock()
        mock_window.winfo_exists.return_value = True
        mock_toplevel.return_value = mock_window
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            base_window = BaseWindow(self.root, "Test")
            base_window._show_message("info", "Título", "Mensaje")
            
            mock_showinfo.assert_called_once_with("Título", "Mensaje", parent=mock_window)
    
    @patch('customtkinter.CTkToplevel')
    def test_base_window_show_message_error(self, mock_toplevel):
        """Test mostrar mensaje de error"""
        mock_window = Mock()
        mock_window.winfo_exists.return_value = True
        mock_toplevel.return_value = mock_window
        
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            base_window = BaseWindow(self.root, "Test")
            base_window._show_message("error", "Error", "Mensaje de error")
            
            mock_showerror.assert_called_once_with("Error", "Mensaje de error", parent=mock_window)
    
    @patch('customtkinter.CTkToplevel')
    def test_base_window_show_message_yesno(self, mock_toplevel):
        """Test mostrar mensaje de confirmación"""
        mock_window = Mock()
        mock_window.winfo_exists.return_value = True
        mock_toplevel.return_value = mock_window
        
        with patch('tkinter.messagebox.askyesno', return_value=True) as mock_askyesno:
            base_window = BaseWindow(self.root, "Test")
            result = base_window._show_message("yesno", "Confirmar", "¿Continuar?")
            
            mock_askyesno.assert_called_once_with("Confirmar", "¿Continuar?", parent=mock_window)
            assert result is True
    
    @patch('customtkinter.CTkToplevel')
    @patch('customtkinter.CTkScrollableFrame')
    def test_setup_scrollable_frame(self, mock_scrollable_frame, mock_toplevel):
        """Test configuración de frame scrollable"""
        mock_window = Mock()
        mock_toplevel.return_value = mock_window
        mock_frame = Mock()
        mock_scrollable_frame.return_value = mock_frame
        
        base_window = BaseWindow(self.root, "Test")
        result = base_window.setup_scrollable_frame(1200, 800)
        
        # Verificar que se creó el frame scrollable
        mock_scrollable_frame.assert_called_once_with(mock_window)
        mock_frame.pack.assert_called_once_with(fill="both", expand=True, padx=10, pady=10)
        mock_frame.configure.assert_called_once_with(width=1200, height=800)
        
        assert result == mock_frame
        assert base_window.main_frame == mock_frame
    
    @patch('customtkinter.CTkToplevel')
    def test_bind_mousewheel_to_scrollable(self, mock_toplevel):
        """Test vinculación de scroll de rueda del ratón"""
        mock_window = Mock()
        mock_toplevel.return_value = mock_window
        mock_widget = Mock()
        
        base_window = BaseWindow(self.root, "Test")
        base_window.bind_mousewheel_to_scrollable(mock_widget)
        
        # Verificar que se vincularon los eventos
        expected_calls = [
            (("<MouseWheel>",), {}),
            (("<Button-4>",), {}),
            (("<Button-5>",), {})
        ]
        
        # Verificar que bind fue llamado 3 veces
        assert mock_widget.bind.call_count == 3

class TestImageSelector:
    """Tests para ImageSelector"""
    
    def setup_method(self):
        """Setup para cada test"""
        self.root = tk.Tk()
        self.root.withdraw()
    
    def teardown_method(self):
        """Cleanup después de cada test"""
        if self.root:
            self.root.destroy()
    
    @patch('utils.logger.get_logger')
    def test_image_selector_creation(self, mock_get_logger):
        """Test creación de ImageSelector"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        selector = ImageSelector(self.root, mock_logger)
        
        assert selector.parent_window == self.root
        assert selector.logger == mock_logger
        assert selector.imagen_path == ""
        assert selector.imagen_display is None
        assert selector.imagen_label is None
    
    @patch('utils.logger.get_logger')
    def test_quitar_imagen(self, mock_get_logger):
        """Test quitar imagen"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        
        selector = ImageSelector(self.root, mock_logger)
        selector.imagen_path = "/path/to/image.jpg"
        selector.imagen_label = Mock()
        selector.update_image_display = Mock()
        
        selector.quitar_imagen()
        
        assert selector.imagen_path == ""
        selector.imagen_label.configure.assert_called_once_with(text="Ninguna imagen seleccionada")
        selector.update_image_display.assert_called_once()
    
    @patch('utils.logger.get_logger')
    @patch('os.path.exists')
    def test_update_image_display_no_image(self, mock_exists, mock_get_logger):
        """Test actualizar display sin imagen"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_exists.return_value = False
        
        selector = ImageSelector(self.root, mock_logger)
        selector.imagen_path = ""
        selector.imagen_display = Mock()
        selector.quitar_imagen_btn = Mock()
        
        selector.update_image_display()
        
        selector.imagen_display.configure.assert_called_once_with(image="", text="Sin imagen")
        selector.quitar_imagen_btn.configure.assert_called_once_with(state="disabled")
