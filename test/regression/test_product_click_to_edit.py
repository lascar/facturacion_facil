#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour s'assurer que le clic sur un produit
le charge automatiquement pour édition
"""

import sys
import os
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_product_click_loads_for_editing():
    """Test que cliquer sur un produit le charge pour édition"""
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
        
        # Vérifier qu'il y a des produits
        tree = productos_window.productos_tree
        items = tree.get_children()
        
        assert len(items) > 0, "Should have products in the list"
        
        # Sélectionner le premier produit
        first_item = items[0]
        tree.selection_set(first_item)
        tree.focus(first_item)
        tree.event_generate("<<TreeviewSelect>>")
        productos_window.window.update()
        
        # Vérifier que le produit est sélectionné
        assert productos_window.selected_producto is not None, "Product should be selected"
        
        # Vérifier que le formulaire est chargé
        selected_product = productos_window.selected_producto
        form_name = productos_window.nombre_entry.get()
        form_ref = productos_window.referencia_entry.get()
        form_price = productos_window.precio_entry.get()
        
        assert form_name == selected_product.nombre, f"Form name should match: {form_name} != {selected_product.nombre}"
        assert form_ref == selected_product.referencia, f"Form reference should match: {form_ref} != {selected_product.referencia}"
        assert form_price == str(selected_product.precio), f"Form price should match: {form_price} != {selected_product.precio}"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_product_selection_change_updates_form():
    """Test que changer de sélection met à jour le formulaire"""
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
        
        # Vérifier qu'il y a au moins 2 produits
        tree = productos_window.productos_tree
        items = tree.get_children()
        
        assert len(items) >= 2, "Should have at least 2 products for this test"
        
        # Sélectionner le premier produit
        first_item = items[0]
        tree.selection_set(first_item)
        tree.focus(first_item)
        tree.event_generate("<<TreeviewSelect>>")
        productos_window.window.update()
        
        first_product = productos_window.selected_producto
        first_name = productos_window.nombre_entry.get()
        
        assert first_product is not None, "First product should be selected"
        assert first_name == first_product.nombre, "Form should show first product name"
        
        # Sélectionner le deuxième produit
        second_item = items[1]
        tree.selection_set(second_item)
        tree.focus(second_item)
        tree.event_generate("<<TreeviewSelect>>")
        productos_window.window.update()
        
        second_product = productos_window.selected_producto
        second_name = productos_window.nombre_entry.get()
        
        assert second_product is not None, "Second product should be selected"
        assert second_name == second_product.nombre, "Form should show second product name"
        assert second_name != first_name, "Form should have changed to show second product"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_product_double_click_functionality():
    """Test que le double-clic fonctionne sans erreur"""
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
        
        # Vérifier qu'il y a des produits
        tree = productos_window.productos_tree
        items = tree.get_children()
        
        assert len(items) > 0, "Should have products in the list"
        
        # Sélectionner un produit
        first_item = items[0]
        tree.selection_set(first_item)
        tree.focus(first_item)
        tree.event_generate("<<TreeviewSelect>>")
        productos_window.window.update()
        
        # Vérifier que le produit est sélectionné
        assert productos_window.selected_producto is not None, "Product should be selected"
        
        # Tester le double-clic
        productos_window.on_producto_double_click(None)
        
        # Vérifier que le produit est toujours sélectionné après double-clic
        assert productos_window.selected_producto is not None, "Product should still be selected after double-click"
        
        # Nettoyer
        productos_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_treeview_selection_event_binding():
    """Test que les événements de sélection sont correctement liés"""
    try:
        import customtkinter as ctk
        from ui.productos import ProductosWindow
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer ProductosWindow
        productos_window = ProductosWindow(root)
        productos_window.window.withdraw()
        
        # Vérifier que les méthodes existent
        assert hasattr(productos_window, 'on_producto_select'), "Should have on_producto_select method"
        assert hasattr(productos_window, 'on_producto_double_click'), "Should have on_producto_double_click method"
        assert hasattr(productos_window, 'load_producto_to_form'), "Should have load_producto_to_form method"
        
        # Vérifier que le TreeView existe
        assert hasattr(productos_window, 'productos_tree'), "Should have productos_tree"
        
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
        test_product_click_loads_for_editing,
        test_product_selection_change_updates_form,
        test_product_double_click_functionality,
        test_treeview_selection_event_binding
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
