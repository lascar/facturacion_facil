#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour s'assurer que les boutons de sélection d'images
fonctionnent correctement et ouvrent les bons dialogues
"""

import sys
import os
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_image_selector_opens_file_dialog():
    """Test que le bouton de sélection d'image ouvre un dialogue de fichiers"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        from unittest.mock import patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Test avec mock
        with patch('tkinter.filedialog.askopenfilename') as mock_file_dialog:
            mock_file_dialog.return_value = ""
            
            # Appeler la méthode
            productos_window.seleccionar_imagen()
            
            # Vérifier que askopenfilename a été appelé (pas askdirectory)
            mock_file_dialog.assert_called_once()
            
            # Vérifier les arguments
            call_kwargs = mock_file_dialog.call_args.kwargs
            assert 'filetypes' in call_kwargs, "Should have filetypes for file selection"
            
            # Vérifier qu'il y a des types d'images
            filetypes = call_kwargs['filetypes']
            has_images = any('Imágenes' in ft[0] or 'PNG' in ft[0] for ft in filetypes)
            assert has_images, f"Should have image file types. Got: {filetypes}"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_directory_config_opens_directory_dialog():
    """Test que le bouton de configuration ouvre un dialogue de répertoires"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        from unittest.mock import patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Test avec mock
        with patch('tkinter.filedialog.askdirectory') as mock_dir_dialog:
            mock_dir_dialog.return_value = ""
            
            # Appeler la méthode
            productos_window.configurar_directorio_imagenes()
            
            # Vérifier que askdirectory a été appelé (pas askopenfilename)
            mock_dir_dialog.assert_called_once()
            
            # Vérifier les arguments
            call_kwargs = mock_dir_dialog.call_args.kwargs
            assert 'title' in call_kwargs, "Should have title for directory selection"
            
            # Vérifier que le titre mentionne les répertoires
            title = call_kwargs['title']
            assert 'directorio' in title.lower(), f"Title should mention directory. Got: {title}"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_dialogs_used():
    """Test que les deux boutons utilisent des dialogues différents"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        from unittest.mock import patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Test avec les deux mocks
        with patch('tkinter.filedialog.askopenfilename') as mock_file, \
             patch('tkinter.filedialog.askdirectory') as mock_dir:
            
            mock_file.return_value = ""
            mock_dir.return_value = ""
            
            # Appeler les deux méthodes
            productos_window.seleccionar_imagen()
            productos_window.configurar_directorio_imagenes()
            
            # Vérifier que les deux dialogues différents ont été appelés
            mock_file.assert_called_once()
            mock_dir.assert_called_once()
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_filetypes_configuration():
    """Test que les types de fichiers d'images sont correctement configurés"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        from unittest.mock import patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Test avec mock
        with patch('tkinter.filedialog.askopenfilename') as mock_file_dialog:
            mock_file_dialog.return_value = ""
            
            # Appeler la méthode
            productos_window.seleccionar_imagen()
            
            # Vérifier les filetypes
            call_kwargs = mock_file_dialog.call_args.kwargs
            filetypes = call_kwargs['filetypes']
            
            # Vérifier qu'on a les types d'images essentiels
            filetype_strings = [ft[1] for ft in filetypes]
            all_types = " ".join(filetype_strings)
            
            assert "*.png" in all_types, "Should support PNG files"
            assert "*.jpg" in all_types, "Should support JPG files"
            assert "*.jpeg" in all_types, "Should support JPEG files"
            assert "*.*" in all_types, "Should have 'all files' option"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Exécuter les tests
    tests = [
        test_image_selector_opens_file_dialog,
        test_directory_config_opens_directory_dialog,
        test_different_dialogs_used,
        test_image_filetypes_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        print(f"Running {test.__name__}...")
        if test():
            print(f"✅ {test.__name__} PASSED")
            passed += 1
        else:
            print(f"❌ {test.__name__} FAILED")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
