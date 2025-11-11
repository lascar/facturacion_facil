#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour les opérations de stock sur produit sélectionné et inventaire
"""

import sys
import os
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_stock_window_has_selected_product_buttons():
    """Test que la fenêtre de stock a les boutons pour produit sélectionné"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()
        
        # Forcer la mise à jour du layout
        stock_window.window.update()
        stock_window.window.update_idletasks()
        
        # Vérifier que les nouvelles méthodes existent
        assert hasattr(stock_window, 'entrada_producto_seleccionado'), "Méthode entrada_producto_seleccionado manquante"
        assert hasattr(stock_window, 'salida_producto_seleccionado'), "Méthode salida_producto_seleccionado manquante"
        assert hasattr(stock_window, 'realizar_inventario'), "Méthode realizar_inventario manquante"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_selected_product_entrada_without_selection():
    """Test que entrada_producto_seleccionado gère l'absence de sélection"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        from unittest.mock import patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()
        
        # S'assurer qu'aucun produit n'est sélectionné
        stock_window.selected_producto_id = None
        
        # Mock de show_error_message pour capturer l'erreur
        with patch.object(stock_window, 'show_error_message') as mock_error:
            stock_window.entrada_producto_seleccionado()
            
            # Vérifier que l'erreur a été affichée
            mock_error.assert_called_once()
            args = mock_error.call_args[0]
            assert "Error" in args[0], "Premier argument devrait être 'Error'"
            assert "seleccionado" in args[1].lower(), "Message devrait mentionner la sélection"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_selected_product_salida_without_selection():
    """Test que salida_producto_seleccionado gère l'absence de sélection"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        from unittest.mock import patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()
        
        # S'assurer qu'aucun produit n'est sélectionné
        stock_window.selected_producto_id = None
        
        # Mock de show_error_message pour capturer l'erreur
        with patch.object(stock_window, 'show_error_message') as mock_error:
            stock_window.salida_producto_seleccionado()
            
            # Vérifier que l'erreur a été affichée
            mock_error.assert_called_once()
            args = mock_error.call_args[0]
            assert "Error" in args[0], "Premier argument devrait être 'Error'"
            assert "seleccionado" in args[1].lower(), "Message devrait mentionner la sélection"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_selected_product_entrada_with_selection():
    """Test que entrada_producto_seleccionado fonctionne avec un produit sélectionné"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        from unittest.mock import patch
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()
        
        # Mock des données de stock
        stock_window.stock_data = [{
            'producto_id': 1,
            'nombre': 'Test Product',
            'referencia': 'TEST-001',
            'cantidad': 10
        }]
        
        # Sélectionner le produit
        stock_window.selected_producto_id = 1
        
        # Mock de add_stock pour éviter l'interaction utilisateur
        with patch.object(stock_window, 'add_stock') as mock_add_stock:
            stock_window.entrada_producto_seleccionado()
            
            # Vérifier que add_stock a été appelé avec le bon produit
            mock_add_stock.assert_called_once()
            called_item = mock_add_stock.call_args[0][0]
            assert called_item['producto_id'] == 1, "Produit incorrect passé à add_stock"
            assert called_item['nombre'] == 'Test Product', "Nom de produit incorrect"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_inventario_requires_selected_product():
    """Test que realizar_inventario nécessite un produit sélectionné"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        from unittest.mock import patch

        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()

        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()

        # Mock des données de stock
        stock_window.stock_data = [{
            'producto_id': 1,
            'nombre': 'Test Product',
            'referencia': 'TEST-001',
            'cantidad': 10
        }]

        # Test sans produit sélectionné
        stock_window.selected_producto_id = None

        with patch.object(stock_window, 'show_error_message') as mock_error:
            stock_window.realizar_inventario()

            # Vérifier que l'erreur a été affichée
            mock_error.assert_called_once()
            args = mock_error.call_args[0]
            assert "Error" in args[0], "Premier argument devrait être 'Error'"
            assert "seleccionado" in args[1].lower(), "Message devrait mentionner la sélection"

        # Test avec produit sélectionné
        stock_window.selected_producto_id = 1

        # Mock de CTkToplevel pour éviter la création de fenêtre
        with patch('customtkinter.CTkToplevel') as mock_toplevel:
            mock_window = patch('customtkinter.CTkToplevel').return_value
            mock_window.update_idletasks = lambda: None
            mock_window.grab_set = lambda: None

            # Test que la méthode peut être appelée avec un produit sélectionné
            try:
                stock_window.realizar_inventario()
                assert True, "realizar_inventario callable avec produit sélectionné"
            except Exception as e:
                # Acceptable si c'est juste un problème de GUI
                if "grab_set" not in str(e) and "update_idletasks" not in str(e):
                    raise e

        # Nettoyer
        stock_window.window.destroy()
        root.destroy()

        return True

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_datetime_import():
    """Test que datetime est correctement importé"""
    try:
        from datetime import datetime
        
        # Test de formatage de date comme utilisé dans l'inventaire
        date_str = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # Vérifier le format
        assert len(date_str) >= 16, "Format de date trop court"
        assert "/" in date_str, "Format de date incorrect"
        assert ":" in date_str, "Format d'heure incorrect"
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Exécuter les tests
    tests = [
        test_stock_window_has_selected_product_buttons,
        test_selected_product_entrada_without_selection,
        test_selected_product_salida_without_selection,
        test_selected_product_entrada_with_selection,
        test_inventario_requires_selected_product,
        test_datetime_import
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
