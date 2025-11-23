# -*- coding: utf-8 -*-
"""
Tests para los componentes UI comunes (refactorizados para PyQt6)
"""
import pytest
import sys
import os

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from unittest.mock import Mock, patch, MagicMock

# Configurer PyQt6 comme framework par défaut pour les tests
from gui import set_gui_framework
set_gui_framework('pyqt6')

# Importar las clases abstractas refactorizadas
from common.ui_components_abstract import AbstractFormHelper, AbstractBaseWindow, AbstractImageSelector

# También importar las clases desde ui_components (que ahora son alias)
from common.ui_components import FormHelper, BaseWindow, ImageSelector

# Verificar que los alias funcionan correctamente
assert FormHelper == AbstractFormHelper
assert BaseWindow == AbstractBaseWindow
assert ImageSelector == AbstractImageSelector

class MockWidget:
    """Mock widget que simula tanto PyQt6 como Tkinter"""

    def __init__(self, initial_text=""):
        self._text = initial_text
        self._plain_text = initial_text

    # Métodos PyQt6
    def text(self):
        return self._text

    def setText(self, text):
        self._text = str(text)

    def clear(self):
        self._text = ""
        self._plain_text = ""

    def toPlainText(self):
        return self._plain_text

    def setPlainText(self, text):
        self._plain_text = str(text)

    # Métodos Tkinter (para compatibilidad)
    def get(self, start=None, end=None):
        if start == "1.0" and end == "end":
            return self._plain_text
        return self._text

    def delete(self, start, end=None):
        self._text = ""
        self._plain_text = ""

    def insert(self, pos, text):
        if pos == 0 or pos == "1.0":
            self._text = str(text)
            self._plain_text = str(text)

class MockAbstractWidget:
    """Mock para widgets abstractos"""

    def __init__(self, native_widget=None):
        self.native_widget = native_widget or MockWidget()

    def get_native_widget(self):
        return self.native_widget

class TestFormHelper:
    """Tests para FormHelper"""
    
    def setup_method(self):
        """Setup para cada test"""
        # Usar mocks en lugar de GUI real para evitar problemas en entorno de test
        pass

    def teardown_method(self):
        """Cleanup después de cada test"""
        pass
    
    def test_clear_entry(self):
        """Test limpiar campo de entrada"""
        mock_widget = MockAbstractWidget(MockWidget("texto inicial"))

        FormHelper.clear_entry(mock_widget)
        assert mock_widget.get_native_widget().text() == ""
    
    def test_clear_entry_with_default(self):
        """Test limpiar campo con valor por defecto"""
        mock_widget = MockAbstractWidget(MockWidget("texto inicial"))

        FormHelper.clear_entry(mock_widget, "valor por defecto")
        assert mock_widget.get_native_widget().text() == "valor por defecto"
    
    def test_clear_entry_invalid_widget(self):
        """Test limpiar campo con widget inválido"""
        # No debería lanzar excepción
        FormHelper.clear_entry(None)
        FormHelper.clear_entry("not a widget")
    
    def test_clear_text_widget(self):
        """Test limpiar widget de texto"""
        mock_widget = MockAbstractWidget(MockWidget("texto inicial"))

        FormHelper.clear_text_widget(mock_widget)
        assert mock_widget.get_native_widget().toPlainText().strip() == ""
    
    def test_clear_text_widget_invalid(self):
        """Test limpiar widget de texto inválido"""
        # No debería lanzar excepción
        FormHelper.clear_text_widget(None)
        FormHelper.clear_text_widget("not a widget")
    
    def test_get_entry_value(self):
        """Test obtener valor de entrada"""
        mock_widget = MockAbstractWidget(MockWidget("  valor con espacios  "))

        value = FormHelper.get_entry_value(mock_widget)
        assert value == "valor con espacios"

    def test_get_entry_value_empty(self):
        """Test obtener valor de entrada vacía"""
        mock_widget = MockAbstractWidget(MockWidget(""))

        value = FormHelper.get_entry_value(mock_widget, "default")
        assert value == "default"
    
    def test_get_entry_value_invalid_widget(self):
        """Test obtener valor de widget inválido"""
        value = FormHelper.get_entry_value(None, "default")
        assert value == "default"
    
    def test_get_text_value(self):
        """Test obtener valor de texto"""
        mock_widget = MockAbstractWidget(MockWidget())
        mock_widget.get_native_widget().setPlainText("  texto con espacios  \n")

        value = FormHelper.get_text_value(mock_widget)
        assert value == "texto con espacios"

    def test_get_text_value_empty(self):
        """Test obtener valor de texto vacío"""
        mock_widget = MockAbstractWidget(MockWidget(""))

        value = FormHelper.get_text_value(mock_widget, "default")
        assert value == "default"
    
    def test_set_entry_value(self):
        """Test establecer valor de entrada"""
        mock_widget = MockAbstractWidget(MockWidget("valor inicial"))

        FormHelper.set_entry_value(mock_widget, "nuevo valor")
        assert mock_widget.get_native_widget().text() == "nuevo valor"

    def test_set_entry_value_number(self):
        """Test establecer valor numérico"""
        mock_widget = MockAbstractWidget(MockWidget(""))

        FormHelper.set_entry_value(mock_widget, 123.45)
        assert mock_widget.get_native_widget().text() == "123.45"
    
    def test_set_entry_value_invalid_widget(self):
        """Test establecer valor en widget inválido"""
        # No debería lanzar excepción
        FormHelper.set_entry_value(None, "value")
        FormHelper.set_entry_value("not a widget", "value")
    
    def test_set_text_value(self):
        """Test establecer valor de texto"""
        mock_widget = MockAbstractWidget(MockWidget())
        mock_widget.get_native_widget().setPlainText("valor inicial")

        FormHelper.set_text_value(mock_widget, "nuevo valor")
        assert mock_widget.get_native_widget().toPlainText().strip() == "nuevo valor"
    
    def test_set_text_value_invalid_widget(self):
        """Test establecer valor en widget de texto inválido"""
        # No debería lanzar excepción
        FormHelper.set_text_value(None, "value")
        FormHelper.set_text_value("not a widget", "value")

class TestBaseWindow:
    """Tests para BaseWindow (AbstractBaseWindow)"""

    def setup_method(self):
        """Setup para cada test"""
        # Usar mocks para evitar problemas de GUI en entorno de test
        pass

    def teardown_method(self):
        """Cleanup después de cada test"""
        pass
    
    @patch('common.ui_components_abstract.get_gui_factory')
    def test_base_window_creation(self, mock_factory):
        """Test creación de BaseWindow"""
        # Mock de la factory
        mock_factory.return_value = Mock()
        mock_factory.return_value.create_window.return_value = Mock()

        base_window = BaseWindow(None, "Test Window", "800x600")

        # Verificar que se inicializó correctamente
        assert hasattr(base_window, 'imagen_path')
        assert base_window.imagen_path == ""
    
    @patch('common.ui_components_abstract.get_gui_factory')
    def test_base_window_show_message_info(self, mock_factory):
        """Test mostrar mensaje de información"""
        # Mock de la factory
        mock_gui_factory = Mock()
        mock_gui_factory.create_window.return_value = Mock()
        mock_gui_factory.show_message.return_value = None
        mock_factory.return_value = mock_gui_factory

        base_window = BaseWindow(None, "Test")
        result = base_window._show_message("info", "Título", "Mensaje")

        # Verificar que se llamó al método correcto
        mock_gui_factory.show_message.assert_called_once_with("info", "Título", "Mensaje")
    
    @patch('common.ui_components_abstract.get_gui_factory')
    def test_base_window_show_message_error(self, mock_factory):
        """Test mostrar mensaje de error"""
        mock_gui_factory = Mock()
        mock_gui_factory.create_window.return_value = Mock()
        mock_gui_factory.show_message.return_value = None
        mock_factory.return_value = mock_gui_factory

        base_window = BaseWindow(None, "Test")
        base_window._show_message("error", "Error", "Mensaje de error")

        mock_gui_factory.show_message.assert_called_once_with("error", "Error", "Mensaje de error")

    @patch('common.ui_components_abstract.get_gui_factory')
    def test_base_window_show_message_yesno(self, mock_factory):
        """Test mostrar mensaje de confirmación"""
        mock_gui_factory = Mock()
        mock_gui_factory.create_window.return_value = Mock()
        mock_gui_factory.show_message.return_value = True
        mock_factory.return_value = mock_gui_factory

        base_window = BaseWindow(None, "Test")
        result = base_window._show_message("yesno", "Confirmar", "¿Continuar?")

        mock_gui_factory.show_message.assert_called_once_with("yesno", "Confirmar", "¿Continuar?")
        assert result is True

    @patch('common.ui_components_abstract.get_gui_factory')
    def test_setup_scrollable_frame(self, mock_factory):
        """Test configuración de frame scrollable"""
        mock_gui_factory = Mock()
        mock_gui_factory.create_window.return_value = Mock()
        mock_scrollable_frame = Mock()
        mock_gui_factory.create_scrollable_frame.return_value = mock_scrollable_frame
        mock_factory.return_value = mock_gui_factory

        base_window = BaseWindow(None, "Test")
        result = base_window.setup_scrollable_frame(1200, 800)

        mock_gui_factory.create_scrollable_frame.assert_called_once()
        assert result == mock_scrollable_frame
        assert base_window.main_frame == mock_scrollable_frame

    @patch('common.ui_components_abstract.get_gui_factory')
    def test_bind_mousewheel_to_scrollable(self, mock_factory):
        """Test vinculación de scroll de rueda del ratón"""
        mock_gui_factory = Mock()
        mock_gui_factory.create_window.return_value = Mock()
        mock_factory.return_value = mock_gui_factory

        base_window = BaseWindow(None, "Test")
        mock_widget = Mock()

        # Este método debería ejecutarse sin errores
        base_window.bind_mousewheel_to_scrollable(mock_widget)
        # No hay mucho que verificar aquí ya que es una implementación básica

class TestImageSelector:
    """Tests para ImageSelector (AbstractImageSelector)"""

    def setup_method(self):
        """Setup para cada test"""
        # Usar mocks para evitar problemas de GUI
        pass

    def teardown_method(self):
        """Cleanup después de cada test"""
        pass
    
    @patch('common.ui_components_abstract.get_gui_factory')
    @patch('utils.logger.get_logger')
    def test_image_selector_creation(self, mock_get_logger, mock_factory):
        """Test creación de ImageSelector"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_factory.return_value = Mock()

        mock_parent = Mock()
        selector = ImageSelector(mock_parent, mock_logger)

        assert selector.parent_window == mock_parent
        assert selector.logger == mock_logger
        assert selector.imagen_path == ""
        assert selector.imagen_display is None
        assert selector.imagen_label is None
    
    @patch('common.ui_components_abstract.get_gui_factory')
    @patch('utils.logger.get_logger')
    def test_quitar_imagen(self, mock_get_logger, mock_factory):
        """Test quitar imagen"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_factory.return_value = Mock()

        mock_parent = Mock()
        selector = ImageSelector(mock_parent, mock_logger)
        selector.imagen_path = "/path/to/image.jpg"
        selector.imagen_label = Mock()
        selector.update_image_display = Mock()

        selector.quitar_imagen()

        assert selector.imagen_path == ""
        selector.imagen_label.configure.assert_called_once_with(text="Ninguna imagen seleccionada")
        selector.update_image_display.assert_called_once()

    @patch('common.ui_components_abstract.get_gui_factory')
    @patch('utils.logger.get_logger')
    @patch('os.path.exists')
    def test_update_image_display_no_image(self, mock_exists, mock_get_logger, mock_factory):
        """Test actualizar display sin imagen"""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        mock_factory.return_value = Mock()
        mock_exists.return_value = False

        mock_parent = Mock()
        selector = ImageSelector(mock_parent, mock_logger)
        selector.imagen_path = ""

        # Mock del widget de display con API abstracta
        mock_display = Mock()
        mock_native_display = Mock()
        mock_display.get_native_widget.return_value = mock_native_display
        selector.imagen_display = mock_display
        selector.quitar_imagen_btn = Mock()

        selector.update_image_display()

        # Verificar que se llamó clear en el widget nativo
        mock_native_display.clear.assert_called_once()
        selector.quitar_imagen_btn.configure.assert_called_once_with(state="disabled")
