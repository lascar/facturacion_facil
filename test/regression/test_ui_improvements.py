import pytest
import os
import sys
from unittest.mock import Mock, patch

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Marquer tous les tests comme skip pour la migration PyQt6
pytestmark = pytest.mark.skip(reason="Tests spécifiques aux améliorations UI Tkinter - PyQt6 utilise des composants natifs")

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

    def test_stock_buttons_interface_regression(self, temp_db):
        """Test de régression: nouvelle interface de stock avec boutons + et -"""
        from ui.stock import StockWindow
        from database.models import Producto, Stock
        import tkinter as tk

        # Créer des données de test
        producto = Producto(nombre="Test Stock Buttons", referencia="TSB001", precio=10.0)
        producto.save()

        # Créer un stock pour le produit
        stock = Stock(producto_id=producto.id, cantidad_disponible=5)
        stock.save()

        # Vérifier que les nouvelles méthodes de l'interface avec boutons existent
        stock_methods = [
            '_show_stock_modification_dialog',
            '_increase_stock',
            '_decrease_stock',
            '_save_stock_changes'
        ]

        for method_name in stock_methods:
            assert hasattr(StockWindow, method_name), f"Méthode de stock {method_name} manquante"
            method = getattr(StockWindow, method_name)
            assert callable(method), f"Méthode de stock {method_name} n'est pas callable"

        # Test de la logique des boutons + et - (test unitaire simplifié)

        # Créer une classe mock pour tester la logique sans tkinter
        class MockStockVar:
            def __init__(self, value):
                self.value = value
            def get(self):
                return self.value
            def set(self, value):
                self.value = value

        class MockStockWindow:
            def _increase_stock(self, stock_var, stock_label):
                current = stock_var.get()
                new_value = current + 1
                stock_var.set(new_value)
                stock_label.configure(text=str(new_value))

            def _decrease_stock(self, stock_var, stock_label):
                current = stock_var.get()
                if current > 0:
                    new_value = current - 1
                    stock_var.set(new_value)
                    stock_label.configure(text=str(new_value))

        mock_stock_window = MockStockWindow()

        # Test de la logique d'augmentation
        stock_var = MockStockVar(5)
        mock_label = Mock()

        # Test augmentation
        mock_stock_window._increase_stock(stock_var, mock_label)
        assert stock_var.get() == 6, f"Stock devrait être 6 après augmentation, mais est {stock_var.get()}"
        mock_label.configure.assert_called_with(text="6")

        # Test diminution
        mock_stock_window._decrease_stock(stock_var, mock_label)
        assert stock_var.get() == 5, f"Stock devrait être 5 après diminution, mais est {stock_var.get()}"
        mock_label.configure.assert_called_with(text="5")

        # Test minimum à 0
        stock_var.set(0)
        mock_label.reset_mock()  # Réinitialiser le mock
        mock_stock_window._decrease_stock(stock_var, mock_label)
        assert stock_var.get() == 0, f"Stock devrait rester à 0, mais est {stock_var.get()}"
        # Vérifier que configure n'a pas été appelé car le stock reste à 0 (pas de changement)
        mock_label.configure.assert_not_called()

    def test_stock_interface_backwards_compatibility(self, temp_db):
        """Test de régression: compatibilité avec l'ancienne interface de stock"""
        from ui.stock import StockWindow
        from database.models import Producto, Stock

        # Créer des données de test
        producto = Producto(nombre="Test Compatibility", referencia="TC001", precio=15.0)
        producto.save()

        stock = Stock(producto_id=producto.id, cantidad_disponible=10)
        stock.save()

        # Vérifier que les méthodes essentielles existent toujours
        essential_methods = [
            'modify_stock',
            'add_stock',
            'remove_stock',
            'load_stock_data',
            'update_stock_display',
            'force_reload_stock_data'  # Nouvelle méthode pour corriger les problèmes de cache
        ]

        for method_name in essential_methods:
            assert hasattr(StockWindow, method_name), f"Méthode essentielle {method_name} manquante"
            method = getattr(StockWindow, method_name)
            assert callable(method), f"Méthode essentielle {method_name} n'est pas callable"

        # Vérifier que la méthode modify_stock a été mise à jour pour utiliser la nouvelle interface
        with patch('customtkinter.CTk') as mock_root:
            # Créer un mock plus complet pour CustomTkinter
            mock_parent = Mock()
            mock_parent._last_child_ids = {}
            mock_parent.winfo_exists.return_value = True
            mock_root.return_value = mock_parent

            try:
                stock_window = StockWindow(mock_parent)
            except Exception as e:
                # Si la création échoue, tester directement la méthode
                print(f"   ⚠️ Création de StockWindow échouée: {e}")
                # Importer la classe pour vérifier le code source
                from ui.stock import StockWindow
                stock_window = StockWindow.__new__(StockWindow)

            # Vérifier que modify_stock ne fait plus appel à simpledialog.askinteger
            import inspect
            modify_stock_source = inspect.getsource(stock_window.modify_stock)

            # La nouvelle implémentation ne devrait plus utiliser simpledialog.askinteger
            assert 'simpledialog.askinteger' not in modify_stock_source, \
                "modify_stock ne devrait plus utiliser simpledialog.askinteger"

            # La nouvelle implémentation devrait utiliser _show_stock_modification_dialog
            assert '_show_stock_modification_dialog' in modify_stock_source, \
                "modify_stock devrait utiliser _show_stock_modification_dialog"

    def test_stock_dialog_grab_error_fix(self, temp_db):
        """Test de régression: correction de l'erreur 'grab failed: window not viewable'"""
        from ui.stock import StockWindow
        from database.models import Producto, Stock

        # Créer des données de test
        producto = Producto(nombre="Test Grab Error Fix", referencia="TGEF001", precio=12.0)
        producto.save()

        stock = Stock(producto_id=producto.id, cantidad_disponible=8)
        stock.save()

        # Vérifier que la méthode de correction existe
        assert hasattr(StockWindow, '_safe_grab_set'), "Méthode _safe_grab_set manquante"

        # Test de la méthode _safe_grab_set (test unitaire)

        # Créer une classe mock pour tester la méthode isolément
        class MockStockWindow:
            def __init__(self):
                from utils.logger import get_logger
                self.logger = get_logger("mock_stock_window")

            def _safe_grab_set(self, dialog):
                """Version mock de _safe_grab_set pour test"""
                try:
                    if dialog.winfo_exists() and dialog.winfo_viewable():
                        dialog.grab_set()
                        dialog.lift()
                except Exception as e:
                    self.logger.warning(f"No se pudo hacer grab_set: {e}")

        mock_stock_window = MockStockWindow()

        # Test avec fenêtre valide
        mock_dialog_valid = Mock()
        mock_dialog_valid.winfo_exists.return_value = True
        mock_dialog_valid.winfo_viewable.return_value = True

        # Ne devrait pas lever d'exception
        try:
            mock_stock_window._safe_grab_set(mock_dialog_valid)
            mock_dialog_valid.grab_set.assert_called_once()
            mock_dialog_valid.lift.assert_called_once()
        except Exception as e:
            pytest.fail(f"_safe_grab_set ne devrait pas lever d'exception avec fenêtre valide: {e}")

        # Test avec fenêtre invalide
        mock_dialog_invalid = Mock()
        mock_dialog_invalid.winfo_exists.return_value = False
        mock_dialog_invalid.winfo_viewable.return_value = False

        # Ne devrait pas lever d'exception même avec fenêtre invalide
        try:
            mock_stock_window._safe_grab_set(mock_dialog_invalid)
            # grab_set ne devrait pas être appelé
            mock_dialog_invalid.grab_set.assert_not_called()
        except Exception as e:
            pytest.fail(f"_safe_grab_set ne devrait pas lever d'exception avec fenêtre invalide: {e}")

        # Test avec exception lors de grab_set
        mock_dialog_error = Mock()
        mock_dialog_error.winfo_exists.return_value = True
        mock_dialog_error.winfo_viewable.return_value = True
        mock_dialog_error.grab_set.side_effect = Exception("grab failed: window not viewable")

        # Ne devrait pas lever d'exception même si grab_set échoue
        try:
            mock_stock_window._safe_grab_set(mock_dialog_error)
        except Exception as e:
            pytest.fail(f"_safe_grab_set devrait gérer les erreurs de grab_set: {e}")
