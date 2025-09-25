import pytest
import os
import sys
from unittest.mock import Mock, patch

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestUIImprovements:
    """Tests de régression pour les améliorations de l'interface"""
    
    def test_config_system_exists(self):
        """Test de régression: système de configuration existe"""
        from utils.config import app_config
        
        # Vérifier que les méthodes principales existent
        assert hasattr(app_config, 'get_default_image_directory')
        assert hasattr(app_config, 'set_default_image_directory')
        assert hasattr(app_config, 'get_assets_directory')
        assert hasattr(app_config, 'get_image_display_size')
        assert hasattr(app_config, 'get_supported_formats')
        
        # Vérifier que les méthodes retournent des valeurs valides
        default_dir = app_config.get_default_image_directory()
        assert isinstance(default_dir, str)
        assert len(default_dir) > 0
        
        assets_dir = app_config.get_assets_directory()
        assert isinstance(assets_dir, str)
        assert "images" in assets_dir
        
        display_size = app_config.get_image_display_size()
        assert isinstance(display_size, tuple)
        assert len(display_size) == 2
        
        formats = app_config.get_supported_formats()
        assert isinstance(formats, list)
        assert ".png" in formats
    
    def test_new_ui_methods_exist(self):
        """Test de régression: nouvelles méthodes UI existent"""
        from ui.productos import ProductosWindow
        
        # Vérifier que les nouvelles méthodes existent
        new_methods = [
            'update_image_display',
            'quitar_imagen',
            'configurar_directorio_imagenes'
        ]
        
        for method_name in new_methods:
            assert hasattr(ProductosWindow, method_name), f"Méthode {method_name} manquante"
            method = getattr(ProductosWindow, method_name)
            assert callable(method), f"Méthode {method_name} n'est pas callable"
    
    def test_new_translations_exist(self):
        """Test de régression: nouvelles traductions existent"""
        from utils.translations import get_text
        
        new_translations = [
            "quitar_imagen",
            "configurar_directorio"
        ]
        
        for key in new_translations:
            value = get_text(key)
            assert value != key, f"Traduction manquante pour {key}"
            assert len(value) > 0, f"Traduction vide pour {key}"
    
    def test_pil_import_available(self):
        """Test de régression: PIL est disponible"""
        try:
            from PIL import Image, ImageTk
            # Test de création d'une image simple
            img = Image.new('RGB', (100, 100), color='red')
            assert img.size == (100, 100)
        except ImportError:
            pytest.fail("PIL n'est pas disponible")
    
    @patch('utils.config.app_config.get_default_image_directory')
    def test_config_integration_in_file_dialog(self, mock_get_dir):
        """Test de régression: intégration de la config dans le dialog"""
        mock_get_dir.return_value = "/test/directory"
        
        from ui.productos import ProductosWindow
        from unittest.mock import Mock
        
        # Créer une instance mock
        window = Mock(spec=ProductosWindow)
        window.imagen_path = ""
        window.imagen_label = Mock()
        window.update_image_display = Mock()
        window.logger = Mock()  # Ajouter le logger mock

        # Appliquer la vraie méthode
        ProductosWindow.seleccionar_imagen(window)
        
        # Vérifier que get_default_image_directory a été appelé
        mock_get_dir.assert_called()
    
    def test_image_display_update_method(self):
        """Test de régression: méthode update_image_display"""
        from ui.productos import ProductosWindow
        from unittest.mock import Mock

        # Créer une instance mock avec les attributs nécessaires
        window = Mock(spec=ProductosWindow)
        window.imagen_path = ""
        window.imagen_display = Mock()
        window.quitar_imagen_btn = Mock()
        window.logger = Mock()  # Ajouter le logger mock
        window.window = Mock()  # Ajouter le window mock
        window.window.winfo_exists.return_value = True

        # La méthode ne devrait pas lever d'exception même sans image
        try:
            ProductosWindow.update_image_display(window)
        except Exception as e:
            pytest.fail(f"update_image_display a levé une exception: {e}")
    
    def test_quitar_imagen_method(self):
        """Test de régression: méthode quitar_imagen"""
        from ui.productos import ProductosWindow
        from unittest.mock import Mock
        
        # Créer une instance mock
        window = Mock(spec=ProductosWindow)
        window.imagen_path = "test/path"
        window.imagen_label = Mock()
        window.update_image_display = Mock()
        
        # Appeler la méthode
        ProductosWindow.quitar_imagen(window)
        
        # Vérifications
        assert window.imagen_path == ""
        window.imagen_label.configure.assert_called_with(text="Ninguna imagen seleccionada")
        window.update_image_display.assert_called_once()
    
    @patch('tkinter.filedialog.askdirectory')
    @patch('utils.config.app_config.set_default_image_directory')
    @patch('utils.config.app_config.get_default_image_directory')
    def test_configurar_directorio_method(self, mock_get_dir, mock_set_dir, mock_askdir):
        """Test de régression: méthode configurar_directorio_imagenes"""
        from ui.productos import ProductosWindow
        from unittest.mock import Mock

        # Configuration des mocks
        mock_askdir.return_value = "/new/directory"
        mock_set_dir.return_value = True
        mock_get_dir.return_value = "/current/directory"

        # Créer une instance mock avec tous les attributs nécessaires
        window = Mock(spec=ProductosWindow)
        window.logger = Mock()
        window.window = Mock()
        window.window.winfo_exists.return_value = True
        window.window.lift = Mock()
        window.window.focus_force = Mock()
        window._show_message = Mock()

        # Appeler la méthode
        ProductosWindow.configurar_directorio_imagenes(window)

        # Vérifications
        mock_askdir.assert_called_once()
        mock_set_dir.assert_called_once_with("/new/directory")
        window._show_message.assert_called()
    
    def test_improved_error_handling(self):
        """Test de régression: gestion d'erreurs améliorée"""
        from ui.productos import ProductosWindow
        from unittest.mock import Mock, patch

        # Créer une instance mock avec tous les attributs nécessaires
        window = Mock(spec=ProductosWindow)
        window.imagen_path = ""
        window.imagen_label = Mock()
        window.update_image_display = Mock()
        window.logger = Mock()
        window.window = Mock()
        window.window.winfo_exists.return_value = True
        window.window.lift = Mock()
        window.window.focus_force = Mock()
        window._show_message = Mock()

        # Mock de app_config
        with patch('ui.productos.app_config') as mock_config:
            mock_config.get_default_image_directory.return_value = "/test/dir"
            mock_config.get_supported_formats.return_value = ['.png', '.jpg']

            # Test avec exception dans filedialog
            with patch('tkinter.filedialog.askopenfilename') as mock_filedialog:
                mock_filedialog.side_effect = Exception("Test error")

                # Ne devrait pas lever d'exception
                try:
                    ProductosWindow.seleccionar_imagen(window)
                except Exception:
                    pytest.fail("seleccionar_imagen ne devrait pas lever d'exception")

                # Vérifier que l'erreur est gérée via _show_message
                window._show_message.assert_called()
    
    def test_button_reorganization_regression(self):
        """Test de régression: réorganisation des boutons"""
        # Ce test vérifie que les méthodes nécessaires pour les boutons existent
        from ui.productos import ProductosWindow
        
        # Vérifier que les méthodes des boutons existent toujours
        button_methods = [
            'nuevo_producto',
            'guardar_producto', 
            'eliminar_producto',
            'limpiar_formulario'
        ]
        
        for method_name in button_methods:
            assert hasattr(ProductosWindow, method_name), f"Méthode de bouton {method_name} manquante"
            method = getattr(ProductosWindow, method_name)
            assert callable(method), f"Méthode de bouton {method_name} n'est pas callable"
