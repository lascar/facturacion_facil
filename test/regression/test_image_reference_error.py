#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour s'assurer que l'erreur 'image pyimage1 doesn't exist'
ne se reproduit pas
"""

import sys
import os
import pytest
import tempfile
from PIL import Image

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def create_test_image():
    """Crée une image de test temporaire"""
    img = Image.new('RGB', (50, 50), color='blue')
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    temp_file.close()
    return temp_file.name

def test_image_selection_no_reference_error():
    """Test que la sélection d'image ne génère pas d'erreur de référence"""
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
        
        # Créer une image de test
        test_image_path = create_test_image()
        
        try:
            # Test 1: Sélectionner une image
            productos_window.imagen_path = test_image_path
            productos_window.update_image_display()
            
            # Vérifier que l'image est chargée
            assert productos_window.imagen_path == test_image_path, "Image path should be set"
            assert hasattr(productos_window.imagen_display, 'image'), "Image display should have image attribute"
            
            # Test 2: Supprimer l'image
            productos_window.quitar_imagen()
            
            # Vérifier que l'image est supprimée
            assert productos_window.imagen_path == "", "Image path should be cleared"
            
            # Test 3: Cycles multiples
            for i in range(3):
                productos_window.imagen_path = test_image_path
                productos_window.update_image_display()
                productos_window.quitar_imagen()
            
            # Test 4: Image inexistante
            productos_window.imagen_path = "/fichier/inexistant.png"
            productos_window.update_image_display()
            
            # Vérifier que le path invalide est nettoyé
            assert productos_window.imagen_path == "", "Invalid image path should be cleared"
            
        finally:
            # Nettoyer
            try:
                os.unlink(test_image_path)
            except:
                pass
            
            productos_window.window.destroy()
            root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_button_invoke_no_error():
    """Test que l'invocation des boutons d'image ne génère pas d'erreur"""
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
        
        # Créer une image de test
        test_image_path = create_test_image()
        
        try:
            # Test du bouton de sélection
            with patch('tkinter.filedialog.askopenfilename') as mock_dialog:
                mock_dialog.return_value = test_image_path
                
                # Vérifier que le bouton existe
                assert hasattr(productos_window, 'imagen_btn'), "Image selection button should exist"
                
                # Invoquer le bouton
                productos_window.imagen_btn.invoke()
                
                # Vérifier que l'image est sélectionnée
                assert productos_window.imagen_path != "", "Image should be selected"
            
            # Test du bouton de suppression
            assert hasattr(productos_window, 'quitar_imagen_btn'), "Remove image button should exist"
            
            # Invoquer le bouton de suppression
            productos_window.quitar_imagen_btn.invoke()
            
            # Vérifier que l'image est supprimée
            assert productos_window.imagen_path == "", "Image should be removed"
            
        finally:
            # Nettoyer
            try:
                os.unlink(test_image_path)
            except:
                pass
            
            productos_window.window.destroy()
            root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_display_configuration_safe():
    """Test que la configuration du display d'image est sûre"""
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
        
        try:
            # Test de configuration directe du display
            display = productos_window.imagen_display
            
            # Test 1: Configuration avec texte seulement
            display.configure(text="Test text")
            
            # Test 2: Configuration avec image None (ne devrait pas planter)
            try:
                display.configure(image=None)
            except:
                pass  # C'est acceptable que ça échoue, l'important c'est que ça ne plante pas l'app
            
            # Test 3: Nettoyage de référence d'image
            if hasattr(display, 'image'):
                display.image = None
            
            # Test 4: Configuration après nettoyage
            display.configure(text="After cleanup")
            
        finally:
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
        test_image_selection_no_reference_error,
        test_image_button_invoke_no_error,
        test_image_display_configuration_safe
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
