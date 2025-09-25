# -*- coding: utf-8 -*-
"""
Tests de regresión para la corrección del scroll en ProductoFacturaDialog
"""
import pytest
from unittest.mock import Mock, patch
import tkinter as tk

class TestDialogScrollRegression:
    """Tests de regresión para el scroll en diálogos"""
    
    def test_producto_factura_dialog_has_scroll_methods(self):
        """Verifica que ProductoFacturaDialog tiene métodos de scroll"""
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Verificar que los métodos de scroll existen
        assert hasattr(ProductoFacturaDialog, 'bind_mousewheel_to_scrollable')
        assert hasattr(ProductoFacturaDialog, 'configure_mousewheel_scrolling')
        
        # Verificar que son métodos callable
        assert callable(getattr(ProductoFacturaDialog, 'bind_mousewheel_to_scrollable'))
        assert callable(getattr(ProductoFacturaDialog, 'configure_mousewheel_scrolling'))
    
    def test_dialog_uses_scrollable_frame(self):
        """Verifica que el diálogo usa CTkScrollableFrame"""
        import inspect
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Obtener el código fuente del método create_widgets
        source = inspect.getsource(ProductoFacturaDialog.create_widgets)
        
        # Verificar que usa CTkScrollableFrame
        assert 'CTkScrollableFrame' in source
        assert 'main_scrollable_frame' in source
    
    def test_scroll_configuration_in_constructor(self):
        """Verifica que la configuración de scroll se llama en el constructor"""
        import inspect
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Obtener el código fuente del constructor
        source = inspect.getsource(ProductoFacturaDialog.__init__)
        
        # Verificar que se llama configure_mousewheel_scrolling
        assert 'configure_mousewheel_scrolling' in source
    
    def test_mousewheel_binding_logic(self):
        """Verifica la lógica de binding del scroll"""
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Crear una instancia mock para probar el método
        dialog = Mock(spec=ProductoFacturaDialog)
        dialog.main_scrollable_frame = Mock()
        dialog.main_scrollable_frame.winfo_exists.return_value = True
        dialog.main_scrollable_frame._parent_canvas = Mock()
        
        # Obtener el método real
        method = ProductoFacturaDialog.bind_mousewheel_to_scrollable
        
        # Crear un widget mock
        widget = Mock()
        
        # Llamar al método
        method(dialog, widget)
        
        # Verificar que se configuraron los bindings (ahora con parámetro "+")
        assert widget.bind.call_count >= 3  # Al menos 3 bindings (MouseWheel, Button-4, Button-5)

        # Verificar que se llamaron los bindings correctos
        call_args_list = [call[0][0] for call in widget.bind.call_args_list]
        assert "<MouseWheel>" in call_args_list
        assert "<Button-4>" in call_args_list
        assert "<Button-5>" in call_args_list
    
    def test_scroll_event_handling(self):
        """Verifica que los eventos de scroll se manejan correctamente"""
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Crear una instancia mock
        dialog = Mock(spec=ProductoFacturaDialog)
        dialog.main_scrollable_frame = Mock()
        dialog.main_scrollable_frame.winfo_exists.return_value = True
        dialog.main_scrollable_frame._parent_canvas = Mock()
        
        # Obtener el método real
        method = ProductoFacturaDialog.bind_mousewheel_to_scrollable
        
        # Crear un widget mock
        widget = Mock()
        
        # Llamar al método para configurar el binding
        method(dialog, widget)
        
        # Obtener la función de callback que se registró
        callback = widget.bind.call_args_list[0][0][1]
        
        # Crear un evento mock con delta (Windows/Mac)
        event_delta = Mock()
        event_delta.delta = 120
        event_delta.widget = widget
        
        # Llamar al callback
        callback(event_delta)
        
        # Verificar que se llamó yview_scroll
        dialog.main_scrollable_frame._parent_canvas.yview_scroll.assert_called_once()
    
    def test_scroll_event_handling_linux(self):
        """Verifica que los eventos de scroll se manejan correctamente en Linux"""
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Crear una instancia mock
        dialog = Mock(spec=ProductoFacturaDialog)
        dialog.main_scrollable_frame = Mock()
        dialog.main_scrollable_frame.winfo_exists.return_value = True
        dialog.main_scrollable_frame._parent_canvas = Mock()
        
        # Obtener el método real
        method = ProductoFacturaDialog.bind_mousewheel_to_scrollable
        
        # Crear un widget mock
        widget = Mock()
        
        # Llamar al método para configurar el binding
        method(dialog, widget)
        
        # Obtener la función de callback que se registró
        callback = widget.bind.call_args_list[0][0][1]
        
        # Crear un evento mock sin delta (Linux)
        event_linux = Mock()
        event_linux.delta = None
        event_linux.num = 4  # Scroll up
        event_linux.widget = widget
        
        # Llamar al callback
        callback(event_linux)
        
        # Verificar que se llamó yview_scroll
        dialog.main_scrollable_frame._parent_canvas.yview_scroll.assert_called_once()
    
    def test_scroll_error_handling(self):
        """Verifica que los errores de scroll se manejan correctamente"""
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Crear una instancia mock sin frame scrollable
        dialog = Mock(spec=ProductoFacturaDialog)
        dialog.main_scrollable_frame = None
        
        # Obtener el método real
        method = ProductoFacturaDialog.bind_mousewheel_to_scrollable
        
        # Crear un widget mock
        widget = Mock()
        
        # Llamar al método - no debería fallar
        method(dialog, widget)
        
        # Obtener la función de callback
        callback = widget.bind.call_args_list[0][0][1]
        
        # Crear un evento mock
        event = Mock()
        event.delta = 120
        event.widget = widget
        
        # Llamar al callback - no debería fallar aunque no haya frame
        try:
            callback(event)
            # Si llegamos aquí, el manejo de errores funciona
            assert True
        except Exception as e:
            # Si hay excepción, el manejo de errores no funciona
            assert False, f"El manejo de errores de scroll no funciona correctamente: {e}"
    
    def test_configure_mousewheel_scrolling_method(self):
        """Verifica que el método configure_mousewheel_scrolling funciona"""
        from ui.producto_factura_dialog import ProductoFacturaDialog
        
        # Crear mocks
        dialog = Mock(spec=ProductoFacturaDialog)
        dialog.dialog = Mock()
        dialog.dialog.winfo_children.return_value = []
        dialog.bind_mousewheel_to_scrollable = Mock()
        dialog.logger = Mock()
        
        # Obtener el método real
        method = ProductoFacturaDialog.configure_mousewheel_scrolling
        
        # Llamar al método - no debería fallar
        try:
            method(dialog)
            # Verificar que se llamó bind_mousewheel_to_scrollable
            dialog.bind_mousewheel_to_scrollable.assert_called()
            assert True
        except Exception as e:
            assert False, f"configure_mousewheel_scrolling falló: {e}"
    
    def test_regression_scroll_focus_issue(self):
        """Test de regresión específico para el problema de scroll con foco"""
        # Este test verifica que la corrección aborda el problema original:
        # "el scroll del ratón no funciona cuando un elemento tiene foco"

        from ui.producto_factura_dialog import ProductoFacturaDialog

        # Verificar que el diálogo ahora tiene capacidades de scroll
        # main_scrollable_frame es una variable de instancia, no de clase
        assert hasattr(ProductoFacturaDialog, 'bind_mousewheel_to_scrollable')
        assert hasattr(ProductoFacturaDialog, 'configure_mousewheel_scrolling')
        
        # Verificar que el código fuente contiene las correcciones
        import inspect
        
        # Verificar create_widgets usa CTkScrollableFrame
        create_widgets_source = inspect.getsource(ProductoFacturaDialog.create_widgets)
        assert 'CTkScrollableFrame' in create_widgets_source
        assert 'main_scrollable_frame' in create_widgets_source
        
        # Verificar __init__ configura el scroll
        init_source = inspect.getsource(ProductoFacturaDialog.__init__)
        assert 'configure_mousewheel_scrolling' in init_source
        
        # Verificar bind_mousewheel_to_scrollable maneja el scroll correctamente
        bind_source = inspect.getsource(ProductoFacturaDialog.bind_mousewheel_to_scrollable)
        assert 'main_scrollable_frame' in bind_source
        assert '_parent_canvas.yview_scroll' in bind_source
        assert 'return "break"' in bind_source  # Prevención de propagación
        assert 'FocusIn' in bind_source  # Manejo de foco

    def test_global_mousewheel_handler_implementation(self):
        """Verifica que el manejador global de scroll está implementado"""
        from ui.producto_factura_dialog import ProductoFacturaDialog

        # Verificar que el método existe
        assert hasattr(ProductoFacturaDialog, '_global_mousewheel_handler')
        assert callable(getattr(ProductoFacturaDialog, '_global_mousewheel_handler'))

        # Verificar el código fuente
        import inspect
        source = inspect.getsource(ProductoFacturaDialog._global_mousewheel_handler)
        assert '_is_event_in_dialog' in source
        assert 'main_scrollable_frame' in source
        assert '_parent_canvas.yview_scroll' in source

    def test_event_detection_in_dialog(self):
        """Verifica que la detección de eventos en diálogo funciona"""
        from ui.producto_factura_dialog import ProductoFacturaDialog

        # Verificar que el método existe
        assert hasattr(ProductoFacturaDialog, '_is_event_in_dialog')
        assert callable(getattr(ProductoFacturaDialog, '_is_event_in_dialog'))

        # Verificar el código fuente
        import inspect
        source = inspect.getsource(ProductoFacturaDialog._is_event_in_dialog)
        assert 'winfo_rootx' in source
        assert 'winfo_rooty' in source
        assert 'x_root' in source
        assert 'y_root' in source

    def test_cleanup_bindings_implementation(self):
        """Verifica que la limpieza de bindings está implementada"""
        from ui.producto_factura_dialog import ProductoFacturaDialog

        # Verificar que el método existe
        assert hasattr(ProductoFacturaDialog, '_cleanup_bindings')
        assert callable(getattr(ProductoFacturaDialog, '_cleanup_bindings'))

        # Verificar el código fuente
        import inspect
        source = inspect.getsource(ProductoFacturaDialog._cleanup_bindings)
        assert 'unbind_all' in source
        assert 'MouseWheel' in source
        assert 'Button-4' in source
        assert 'Button-5' in source

    def test_bind_all_configuration(self):
        """Verifica que se usa bind_all para capturar eventos globalmente"""
        from ui.producto_factura_dialog import ProductoFacturaDialog

        # Verificar el código fuente del método configure_mousewheel_scrolling
        import inspect
        source = inspect.getsource(ProductoFacturaDialog.configure_mousewheel_scrolling)

        # Verificar que usa bind_all con el manejador global
        assert 'bind_all' in source
        assert '_global_mousewheel_handler' in source
        assert 'MouseWheel' in source
        assert 'Button-4' in source
        assert 'Button-5' in source

    def test_focus_issue_regression_complete(self):
        """Test de regresión completo para el problema de scroll con foco"""
        from ui.producto_factura_dialog import ProductoFacturaDialog

        # Verificar que todas las correcciones están implementadas
        methods_required = [
            '_global_mousewheel_handler',
            '_is_event_in_dialog',
            '_cleanup_bindings',
            '_ensure_scroll_binding'
        ]

        for method in methods_required:
            assert hasattr(ProductoFacturaDialog, method), f"Método {method} no encontrado"
            assert callable(getattr(ProductoFacturaDialog, method)), f"Método {method} no es callable"

        # Verificar que el código fuente contiene las correcciones clave
        import inspect

        # Verificar bind_all en configure_mousewheel_scrolling
        config_source = inspect.getsource(ProductoFacturaDialog.configure_mousewheel_scrolling)
        assert 'bind_all' in config_source

        # Verificar return "break" en bind_mousewheel_to_scrollable
        bind_source = inspect.getsource(ProductoFacturaDialog.bind_mousewheel_to_scrollable)
        assert 'return "break"' in bind_source

        # Verificar limpieza en accept y cancel
        accept_source = inspect.getsource(ProductoFacturaDialog.accept)
        cancel_source = inspect.getsource(ProductoFacturaDialog.cancel)
        assert '_cleanup_bindings' in accept_source
        assert '_cleanup_bindings' in cancel_source
