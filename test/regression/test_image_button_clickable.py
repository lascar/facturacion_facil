#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour s'assurer que le bouton de sélection d'image
reste cliquable et visible
"""

import sys
import os
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_image_button_is_visible_and_mapped():
    """Test que le bouton de sélection d'image est visible et mappé"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Forcer la mise à jour du layout
        productos_window.window.update()
        productos_window.window.update_idletasks()
        
        # Chercher le bouton de sélection d'image
        def find_image_button(widget):
            if isinstance(widget, ctk.CTkButton):
                try:
                    text = widget.cget("text")
                    if "🖼️" in text and "Seleccionar" in text:
                        return widget
                except:
                    pass
            
            try:
                for child in widget.winfo_children():
                    result = find_image_button(child)
                    if result:
                        return result
            except:
                pass
            return None
        
        image_button = find_image_button(productos_window.window)
        
        # Vérifier que le bouton existe
        assert image_button is not None, "Image selection button should exist"
        
        # Vérifier les propriétés du bouton
        text = image_button.cget("text")
        state = image_button.cget("state")
        width = image_button.cget("width")
        height = image_button.cget("height")
        
        assert "🖼️" in text, f"Button should have image icon. Got: {text}"
        assert "Seleccionar" in text, f"Button should have 'Seleccionar' text. Got: {text}"
        assert state == "normal", f"Button should be enabled. Got state: {state}"
        assert width == 200, f"Button should have width 200. Got: {width}"
        assert height == 40, f"Button should have height 40. Got: {height}"
        
        # Forcer la mise à jour et vérifier la visibilité
        image_button.update_idletasks()
        
        geometry = image_button.winfo_geometry()
        visible = image_button.winfo_viewable()
        mapped = image_button.winfo_ismapped()
        
        # Vérifier que le bouton a une géométrie valide (pas 1x1+0+0)
        assert geometry != "1x1+0+0", f"Button should have valid geometry. Got: {geometry}"
        
        # Vérifier que le bouton est visible et mappé
        assert visible, f"Button should be visible. Geometry: {geometry}"
        assert mapped, f"Button should be mapped. Geometry: {geometry}"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_button_is_clickable():
    """Test que le bouton de sélection d'image est cliquable"""
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
        
        # Forcer la mise à jour du layout
        productos_window.window.update()
        productos_window.window.update_idletasks()
        
        # Chercher le bouton de sélection d'image
        def find_image_button(widget):
            if isinstance(widget, ctk.CTkButton):
                try:
                    text = widget.cget("text")
                    if "🖼️" in text and "Seleccionar" in text:
                        return widget
                except:
                    pass
            
            try:
                for child in widget.winfo_children():
                    result = find_image_button(child)
                    if result:
                        return result
            except:
                pass
            return None
        
        image_button = find_image_button(productos_window.window)
        assert image_button is not None, "Image selection button should exist"
        
        # Test de clic avec mock
        with patch('tkinter.filedialog.askopenfilename') as mock_dialog:
            mock_dialog.return_value = ""  # Simuler annulation
            
            # Simuler un clic sur le bouton
            image_button.invoke()
            
            # Vérifier que le dialogue a été appelé
            assert mock_dialog.called, "File dialog should be called when button is clicked"
            
            # Vérifier les arguments du dialogue
            call_kwargs = mock_dialog.call_args.kwargs
            assert 'filetypes' in call_kwargs, "Dialog should have filetypes"
            assert 'title' in call_kwargs, "Dialog should have title"
            assert 'parent' in call_kwargs, "Dialog should have parent"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_button_has_correct_command():
    """Test que le bouton de sélection d'image a la bonne commande"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Vérifier que la méthode seleccionar_imagen existe
        assert hasattr(productos_window, 'seleccionar_imagen'), "ProductosWindow should have seleccionar_imagen method"
        assert callable(productos_window.seleccionar_imagen), "seleccionar_imagen should be callable"
        
        # Chercher le bouton de sélection d'image
        def find_image_button(widget):
            if isinstance(widget, ctk.CTkButton):
                try:
                    text = widget.cget("text")
                    if "🖼️" in text and "Seleccionar" in text:
                        return widget
                except:
                    pass
            
            try:
                for child in widget.winfo_children():
                    result = find_image_button(child)
                    if result:
                        return result
            except:
                pass
            return None
        
        image_button = find_image_button(productos_window.window)
        assert image_button is not None, "Image selection button should exist"
        
        # Vérifier que le bouton a la bonne commande
        command = image_button.cget("command")
        assert command is not None, "Button should have a command"
        
        # Vérifier que la commande est la méthode seleccionar_imagen
        assert command == productos_window.seleccionar_imagen, "Button command should be seleccionar_imagen method"
        
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
        test_image_button_is_visible_and_mapped,
        test_image_button_is_clickable,
        test_image_button_has_correct_command
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
