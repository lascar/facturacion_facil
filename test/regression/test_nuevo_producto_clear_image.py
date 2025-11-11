#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour s'assurer que "Nuevo Producto" nettoie l'image
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
    img = Image.new('RGB', (50, 50), color='red')
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(temp_file.name, 'PNG')
    temp_file.close()
    return temp_file.name

def test_nuevo_producto_clears_image_path():
    """Test que nuevo_producto nettoie le chemin d'image"""
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
            # Simuler qu'une image est sélectionnée
            productos_window.imagen_path = test_image_path
            productos_window.update_image_display()
            
            # Vérifier que l'image est définie
            assert productos_window.imagen_path == test_image_path, "Image path should be set"
            
            # Appeler nuevo_producto
            productos_window.nuevo_producto()
            
            # Vérifier que l'image est nettoyée
            assert productos_window.imagen_path == "", "Image path should be cleared after nuevo_producto"
            
            # Vérifier que le produit sélectionné est nettoyé
            assert productos_window.selected_producto is None, "Selected product should be None after nuevo_producto"
            
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

def test_nuevo_producto_clears_form_fields():
    """Test que nuevo_producto nettoie tous les champs du formulaire"""
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
        
        # Remplir les champs avec des données de test
        productos_window.nombre_entry.insert(0, "Test Product")
        productos_window.referencia_entry.insert(0, "TEST-001")
        productos_window.precio_entry.insert(0, "99.99")
        productos_window.categoria_entry.insert(0, "Test Category")
        productos_window.descripcion_text.insert("1.0", "Test description")
        
        # Vérifier que les champs sont remplis
        assert productos_window.nombre_entry.get() == "Test Product", "Name field should be filled"
        assert productos_window.referencia_entry.get() == "TEST-001", "Reference field should be filled"
        assert productos_window.precio_entry.get() == "99.99", "Price field should be filled"
        
        # Appeler nuevo_producto
        productos_window.nuevo_producto()
        
        # Vérifier que tous les champs sont nettoyés
        assert productos_window.nombre_entry.get() == "", "Name field should be cleared"
        assert productos_window.referencia_entry.get() == "", "Reference field should be cleared"
        assert productos_window.precio_entry.get() == "", "Price field should be cleared"
        assert productos_window.categoria_entry.get() == "", "Category field should be cleared"
        assert productos_window.descripcion_text.get("1.0", "end-1c") == "", "Description field should be cleared"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_nuevo_producto_calls_limpiar_formulario():
    """Test que nuevo_producto appelle limpiar_formulario"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        from unittest.mock import Mock, patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Mock de limpiar_formulario
        with patch.object(productos_window, 'limpiar_formulario') as mock_limpiar:
            # Appeler nuevo_producto
            productos_window.nuevo_producto()
            
            # Vérifier que limpiar_formulario a été appelé
            mock_limpiar.assert_called_once()
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_limpiar_formulario_clears_image_display():
    """Test que limpiar_formulario nettoie le display d'image"""
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
            # Simuler qu'une image est chargée
            productos_window.imagen_path = test_image_path
            productos_window.update_image_display()
            
            # Vérifier que l'image est chargée
            assert productos_window.imagen_path != "", "Image path should be set"
            
            # Appeler limpiar_formulario directement
            productos_window.limpiar_formulario()
            
            # Vérifier que l'image est nettoyée
            assert productos_window.imagen_path == "", "Image path should be cleared"
            
            # Vérifier que la référence d'image est nettoyée
            if hasattr(productos_window.imagen_display, 'image'):
                assert productos_window.imagen_display.image is None, "Image display reference should be None"
            
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

if __name__ == "__main__":
    # Exécuter les tests
    tests = [
        test_nuevo_producto_clears_image_path,
        test_nuevo_producto_clears_form_fields,
        test_nuevo_producto_calls_limpiar_formulario,
        test_limpiar_formulario_clears_image_display
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
