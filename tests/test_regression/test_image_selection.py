import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ui.productos import ProductosWindow

class TestImageSelectionRegression:
    """Tests de régression pour la sélection d'images"""
    
    @pytest.fixture
    def mock_parent(self):
        """Mock de la fenêtre parent"""
        parent = Mock()
        parent.winfo_exists.return_value = True
        return parent
    
    @pytest.fixture
    def temp_image_file(self):
        """Crée un fichier image temporaire pour les tests"""
        # Créer un fichier temporaire avec extension image
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        temp_file.write(b'fake_image_data')
        temp_file.close()
        
        yield temp_file.name
        
        # Nettoyer après le test
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
    
    @pytest.fixture
    def productos_window_mock(self, mock_parent):
        """Fixture pour créer une fenêtre de produits avec mocks"""
        with patch('customtkinter.CTkToplevel'), \
             patch('ui.productos.ProductosWindow.create_widgets'), \
             patch('ui.productos.ProductosWindow.load_productos'):
            
            window = ProductosWindow(mock_parent)
            
            # Mock des widgets nécessaires
            window.imagen_label = Mock()
            window.imagen_label.configure = Mock()
            
            # Variables d'état
            window.imagen_path = ""
            
            return window
    
    def test_seleccionar_imagen_method_exists(self, productos_window_mock):
        """Test de régression: vérifier que la méthode seleccionar_imagen existe"""
        assert hasattr(productos_window_mock, 'seleccionar_imagen')
        assert callable(productos_window_mock.seleccionar_imagen)
    
    @patch('tkinter.filedialog.askopenfilename')
    def test_seleccionar_imagen_no_file_selected(self, mock_filedialog, productos_window_mock):
        """Test de régression: comportement quand aucun fichier n'est sélectionné"""
        # Simuler qu'aucun fichier n'est sélectionné
        mock_filedialog.return_value = ""
        
        # Appeler la méthode
        productos_window_mock.seleccionar_imagen()
        
        # Vérifier que filedialog a été appelé
        mock_filedialog.assert_called_once()
        
        # Vérifier que l'état n'a pas changé
        assert productos_window_mock.imagen_path == ""
        productos_window_mock.imagen_label.configure.assert_not_called()
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    def test_seleccionar_imagen_file_selected_success(self, mock_copy, mock_makedirs, 
                                                     mock_filedialog, productos_window_mock, 
                                                     temp_image_file):
        """Test de régression: sélection d'image réussie"""
        # Simuler la sélection d'un fichier
        mock_filedialog.return_value = temp_image_file
        
        # Appeler la méthode
        productos_window_mock.seleccionar_imagen()
        
        # Vérifications - ahora incluye initialdir y múltiples filetypes
        mock_filedialog.assert_called_once()
        call_kwargs = mock_filedialog.call_args[1]
        assert call_kwargs['title'] == "Seleccionar Imagen"

        # Verificar que hay múltiples opciones de filetypes
        filetypes = call_kwargs['filetypes']
        assert len(filetypes) >= 6  # Al menos 6 opciones
        assert any("Imágenes" in ft[0] for ft in filetypes)
        assert any("PNG" in ft[0] for ft in filetypes)
        assert any("*.*" in ft[1] for ft in filetypes)
        assert 'initialdir' in call_kwargs  # Nueva funcionalidad
        
        # Vérifier que le répertoire est créé
        mock_makedirs.assert_called_once_with("assets/images", exist_ok=True)
        
        # Vérifier que le fichier est copié
        expected_dest = os.path.join("assets/images", os.path.basename(temp_image_file))
        mock_copy.assert_called_once_with(temp_image_file, expected_dest)
        
        # Vérifier que l'état est mis à jour
        assert productos_window_mock.imagen_path == expected_dest
        productos_window_mock.imagen_label.configure.assert_called_once_with(
            text=f"Imagen: {os.path.basename(temp_image_file)}"  # Nuevo formato
        )
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    @patch('tkinter.messagebox.showerror')
    def test_seleccionar_imagen_copy_error(self, mock_showerror, mock_copy, mock_makedirs,
                                          mock_filedialog, productos_window_mock, temp_image_file):
        """Test de régression: erreur lors de la copie du fichier"""
        # Simuler la sélection d'un fichier
        mock_filedialog.return_value = temp_image_file
        
        # Simuler une erreur lors de la copie
        mock_copy.side_effect = PermissionError("Permission denied")
        
        # Appeler la méthode
        productos_window_mock.seleccionar_imagen()
        
        # Vérifier que l'erreur est gérée
        mock_showerror.assert_called_once()
        error_call = mock_showerror.call_args
        assert "Error" in error_call[0][0]  # Titre de l'erreur
        assert "Permission denied" in error_call[0][1]  # Message d'erreur
        
        # Vérifier que l'état n'est pas mis à jour en cas d'erreur
        assert productos_window_mock.imagen_path == ""
    
    @patch('tkinter.filedialog.askopenfilename')
    def test_seleccionar_imagen_filedialog_parameters(self, mock_filedialog, productos_window_mock):
        """Test de régression: vérifier les paramètres du filedialog"""
        mock_filedialog.return_value = ""
        
        productos_window_mock.seleccionar_imagen()
        
        # Vérifier que filedialog est appelé avec les bons paramètres (maintenant avec initialdir et múltiples filetypes)
        mock_filedialog.assert_called_once()
        call_kwargs = mock_filedialog.call_args[1]
        assert call_kwargs['title'] == "Seleccionar Imagen"

        # Verificar múltiples opciones de filetypes
        filetypes = call_kwargs['filetypes']
        assert len(filetypes) >= 6  # Al menos 6 opciones
        assert any("Imágenes" in ft[0] for ft in filetypes)
        assert any("PNG" in ft[0] for ft in filetypes)
        assert any("*.*" in ft[1] for ft in filetypes)
        assert 'initialdir' in call_kwargs  # Nueva funcionalidad
    
    def test_imagen_path_initialization(self, productos_window_mock):
        """Test de régression: vérifier l'initialisation de imagen_path"""
        # La variable imagen_path doit être initialisée
        assert hasattr(productos_window_mock, 'imagen_path')
        assert productos_window_mock.imagen_path == ""
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    def test_seleccionar_imagen_different_file_types(self, mock_copy, mock_makedirs,
                                                    mock_filedialog, productos_window_mock):
        """Test de régression: différents types de fichiers image"""
        file_types = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        
        for file_type in file_types:
            # Créer un fichier temporaire avec l'extension
            temp_file = tempfile.NamedTemporaryFile(suffix=file_type, delete=False)
            temp_file.write(b'fake_image_data')
            temp_file.close()
            
            try:
                # Simuler la sélection du fichier
                mock_filedialog.return_value = temp_file.name
                
                # Réinitialiser les mocks
                mock_copy.reset_mock()
                productos_window_mock.imagen_label.configure.reset_mock()
                productos_window_mock.imagen_path = ""
                
                # Appeler la méthode
                productos_window_mock.seleccionar_imagen()
                
                # Vérifications
                expected_dest = os.path.join("assets/images", os.path.basename(temp_file.name))
                mock_copy.assert_called_once_with(temp_file.name, expected_dest)
                assert productos_window_mock.imagen_path == expected_dest
                productos_window_mock.imagen_label.configure.assert_called_once_with(
                    text=f"Imagen: {os.path.basename(temp_file.name)}"  # Nuevo formato
                )
                
            finally:
                # Nettoyer
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    def test_seleccionar_imagen_assets_directory_creation(self, mock_copy, mock_makedirs,
                                                         mock_filedialog, productos_window_mock,
                                                         temp_image_file):
        """Test de régression: création du répertoire assets/images"""
        mock_filedialog.return_value = temp_image_file
        
        productos_window_mock.seleccionar_imagen()
        
        # Vérifier que le répertoire est créé avec les bons paramètres
        mock_makedirs.assert_called_once_with("assets/images", exist_ok=True)
    
    def test_integration_with_translation_system(self, productos_window_mock):
        """Test de régression: intégration avec le système de traductions"""
        from utils.translations import get_text
        
        # Vérifier que les traductions nécessaires existent
        assert get_text("seleccionar_imagen") == "Seleccionar Imagen"
        assert get_text("imagen") == "Imagen"
        assert get_text("error") == "Error"
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    def test_seleccionar_imagen_filename_with_spaces(self, mock_copy, mock_makedirs,
                                                    mock_filedialog, productos_window_mock):
        """Test de régression: nom de fichier avec espaces"""
        # Créer un fichier avec des espaces dans le nom
        temp_file = tempfile.NamedTemporaryFile(suffix=' test image.png', delete=False)
        temp_file.write(b'fake_image_data')
        temp_file.close()
        
        try:
            mock_filedialog.return_value = temp_file.name
            
            productos_window_mock.seleccionar_imagen()
            
            # Vérifier que le fichier avec espaces est géré correctement
            expected_dest = os.path.join("assets/images", os.path.basename(temp_file.name))
            mock_copy.assert_called_once_with(temp_file.name, expected_dest)
            assert productos_window_mock.imagen_path == expected_dest
            
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    def test_seleccionar_imagen_unicode_filename(self, mock_copy, mock_makedirs,
                                                mock_filedialog, productos_window_mock):
        """Test de régression: nom de fichier avec caractères Unicode"""
        # Créer un fichier avec des caractères Unicode
        temp_file = tempfile.NamedTemporaryFile(suffix='_café_ñoño.png', delete=False)
        temp_file.write(b'fake_image_data')
        temp_file.close()
        
        try:
            mock_filedialog.return_value = temp_file.name
            
            productos_window_mock.seleccionar_imagen()
            
            # Vérifier que les caractères Unicode sont gérés correctement
            expected_dest = os.path.join("assets/images", os.path.basename(temp_file.name))
            mock_copy.assert_called_once_with(temp_file.name, expected_dest)
            assert productos_window_mock.imagen_path == expected_dest
            
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_button_command_method_exists(self, productos_window_mock):
        """Test de régression: vérifier que la méthode du bouton existe et est callable"""
        # Vérifier que la méthode existe
        assert hasattr(productos_window_mock, 'seleccionar_imagen')
        assert callable(productos_window_mock.seleccionar_imagen)

        # Vérifier que la méthode peut être appelée sans erreur (avec mocks)
        with patch('tkinter.filedialog.askopenfilename') as mock_filedialog:
            mock_filedialog.return_value = ""

            # Ne devrait pas lever d'exception
            try:
                productos_window_mock.seleccionar_imagen()
            except Exception as e:
                pytest.fail(f"La méthode seleccionar_imagen a levé une exception: {e}")

    def test_widget_initialization_requirements(self):
        """Test de régression: vérifier les exigences d'initialisation des widgets"""
        # Vérifier que les imports nécessaires sont disponibles
        try:
            import customtkinter as ctk
            import tkinter as tk
            from tkinter import filedialog, messagebox
            import os
            import shutil
        except ImportError as e:
            pytest.fail(f"Import manquant: {e}")

        # Vérifier que les méthodes nécessaires existent
        assert hasattr(filedialog, 'askopenfilename')
        assert hasattr(messagebox, 'showerror')
        assert hasattr(os, 'makedirs')
        assert hasattr(os.path, 'basename')
        assert hasattr(os.path, 'join')
        assert hasattr(shutil, 'copy2')

    def test_error_handling_in_seleccionar_imagen(self, productos_window_mock):
        """Test de régression: gestion d'erreurs améliorée"""
        with patch('tkinter.filedialog.askopenfilename') as mock_filedialog:
            # Simuler une exception dans filedialog
            mock_filedialog.side_effect = Exception("Erreur de système")

            with patch('tkinter.messagebox.showerror') as mock_showerror:
                # Appeler la méthode
                productos_window_mock.seleccionar_imagen()

                # Vérifier que l'erreur est gérée
                mock_showerror.assert_called_once()
                error_call = mock_showerror.call_args
                assert "Error" in error_call[0][0]
                assert "Erreur de système" in error_call[0][1]

    @patch('tkinter.filedialog.askopenfilename')
    def test_debug_messages(self, mock_filedialog, productos_window_mock, caplog):
        """Test de régression: vérifier les messages de debug via logging"""
        # Test 1: Aucun fichier sélectionné
        mock_filedialog.return_value = ""

        # Configurer le niveau de logging pour capturer DEBUG
        import logging
        caplog.set_level(logging.DEBUG)

        productos_window_mock.seleccionar_imagen()

        # Vérifier que le message de debug apparaît dans les logs
        debug_messages = [record.message for record in caplog.records if record.levelname == 'DEBUG']
        assert any("Usuario canceló la selección de imagen" in msg for msg in debug_messages), \
               f"Message de debug manquant. Messages trouvés: {debug_messages}"

    def test_new_image_display_methods(self, productos_window_mock):
        """Test de régression: nouvelles méthodes pour l'affichage d'image"""
        # Vérifier que les nouvelles méthodes existent
        assert hasattr(productos_window_mock, 'update_image_display')
        assert callable(productos_window_mock.update_image_display)

        assert hasattr(productos_window_mock, 'quitar_imagen')
        assert callable(productos_window_mock.quitar_imagen)

        assert hasattr(productos_window_mock, 'configurar_directorio_imagenes')
        assert callable(productos_window_mock.configurar_directorio_imagenes)

    @patch('utils.config.app_config.get_default_image_directory')
    @patch('tkinter.filedialog.askopenfilename')
    def test_default_directory_usage(self, mock_filedialog, mock_get_dir, productos_window_mock):
        """Test de régression: utilisation du répertoire par défaut"""
        mock_get_dir.return_value = "/home/user/Pictures"
        mock_filedialog.return_value = ""

        productos_window_mock.seleccionar_imagen()

        # Vérifier que le répertoire par défaut est utilisé
        mock_get_dir.assert_called_once()
        mock_filedialog.assert_called_once()

        # Vérifier que initialdir est passé au filedialog
        call_kwargs = mock_filedialog.call_args[1]
        assert 'initialdir' in call_kwargs
        assert call_kwargs['initialdir'] == "/home/user/Pictures"

    @patch('tkinter.filedialog.askdirectory')
    @patch('utils.config.app_config.set_default_image_directory')
    @patch('tkinter.messagebox.showinfo')
    def test_configure_directory(self, mock_showinfo, mock_set_dir, mock_askdir, productos_window_mock):
        """Test de régression: configuration du répertoire par défaut"""
        mock_askdir.return_value = "/new/directory"
        mock_set_dir.return_value = True

        productos_window_mock.configurar_directorio_imagenes()

        # Vérifications
        mock_askdir.assert_called_once()
        mock_set_dir.assert_called_once_with("/new/directory")
        mock_showinfo.assert_called_once()

    def test_quitar_imagen_functionality(self, productos_window_mock):
        """Test de régression: fonctionnalité de suppression d'image"""
        # Simuler qu'une image est sélectionnée
        productos_window_mock.imagen_path = "test/path/image.png"

        # Mock des méthodes nécessaires
        productos_window_mock.update_image_display = Mock()

        # Appeler quitar_imagen
        productos_window_mock.quitar_imagen()

        # Vérifications
        assert productos_window_mock.imagen_path == ""
        productos_window_mock.imagen_label.configure.assert_called_with(text="Ninguna imagen seleccionada")
        productos_window_mock.update_image_display.assert_called_once()

    def test_config_integration(self):
        """Test de régression: intégration avec le système de configuration"""
        from utils.config import app_config

        # Vérifier que les méthodes de configuration existent
        assert hasattr(app_config, 'get_default_image_directory')
        assert hasattr(app_config, 'set_default_image_directory')
        assert hasattr(app_config, 'get_assets_directory')
        assert hasattr(app_config, 'get_image_display_size')
        assert hasattr(app_config, 'get_supported_formats')

        # Tester les valeurs par défaut
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

    def test_update_image_display_safety(self):
        """Test de régression: update_image_display es seguro sin widgets"""
        from ui.productos import ProductosWindow

        # Crear una instancia sin widgets inicializados
        instance = object.__new__(ProductosWindow)
        instance.imagen_path = ""

        # Estos métodos no deberían fallar
        try:
            instance.update_image_display()
            instance.quitar_imagen()
        except AttributeError as e:
            if "imagen_display" in str(e):
                pytest.fail("update_image_display no es seguro sin widgets inicializados")
        except Exception:
            # Otras excepciones son aceptables
            pass

    def test_widget_attribute_verification(self, productos_window_mock):
        """Test de régression: verificación de atributos en métodos"""
        # Mock sin los atributos necesarios
        mock_instance = Mock()
        mock_instance.imagen_path = ""

        # Aplicar los métodos reales
        ProductosWindow.update_image_display(mock_instance)
        ProductosWindow.quitar_imagen(mock_instance)

        # No debería haber errores de AttributeError

    def test_filedialog_shows_files_not_directories(self, productos_window_mock):
        """Test de régression: filedialog muestra archivos, no solo directorios"""
        with patch('tkinter.filedialog.askopenfilename') as mock_filedialog:
            mock_filedialog.return_value = ""

            productos_window_mock.seleccionar_imagen()

            # Verificar que se llama con filetypes correctos
            call_kwargs = mock_filedialog.call_args[1]
            filetypes = call_kwargs['filetypes']

            # Debe haber múltiples opciones de filetypes
            assert len(filetypes) >= 6, "Debe haber al menos 6 opciones de filetypes"

            # Verificar opciones específicas
            filetype_names = [ft[0] for ft in filetypes]
            filetype_patterns = [ft[1] for ft in filetypes]

            assert any("Imágenes" in name for name in filetype_names), "Debe haber opción 'Imágenes'"
            assert any("PNG" in name for name in filetype_names), "Debe haber opción 'PNG'"
            assert any("JPEG" in name for name in filetype_names), "Debe haber opción 'JPEG'"
            assert any("GIF" in name for name in filetype_names), "Debe haber opción 'GIF'"
            assert any("BMP" in name for name in filetype_names), "Debe haber opción 'BMP'"
            assert any("*.*" in pattern for pattern in filetype_patterns), "Debe haber opción 'Todos los archivos'"

            # Verificar que los patrones son correctos
            for pattern in filetype_patterns:
                if pattern != "*.*":
                    assert pattern.startswith("*"), f"Patrón {pattern} debe empezar con *"

    def test_filedialog_multiple_extensions_support(self, productos_window_mock):
        """Test de régression: soporte para múltiples extensiones"""
        with patch('tkinter.filedialog.askopenfilename') as mock_filedialog:
            mock_filedialog.return_value = ""

            productos_window_mock.seleccionar_imagen()

            call_kwargs = mock_filedialog.call_args[1]
            filetypes = call_kwargs['filetypes']

            # Buscar la opción "Imágenes" que debe incluir todas las extensiones
            imagenes_option = None
            for name, pattern in filetypes:
                if "Imágenes" in name:
                    imagenes_option = pattern
                    break

            assert imagenes_option is not None, "Debe existir opción 'Imágenes'"

            # Verificar que incluye todas las extensiones principales
            required_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
            for ext in required_extensions:
                assert ext in imagenes_option, f"Extensión {ext} debe estar en la opción Imágenes"
