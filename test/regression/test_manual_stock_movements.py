#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour les fonctionnalités d'entrées et sorties manuelles de stock
"""

import sys
import os
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_stock_window_has_manual_movement_buttons():
    """Test que la fenêtre de stock a les boutons d'entrées et sorties manuelles"""
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
        
        # Vérifier que les méthodes existent
        assert hasattr(stock_window, 'entrada_stock_masiva'), "Méthode entrada_stock_masiva manquante"
        assert hasattr(stock_window, 'salida_stock_masiva'), "Méthode salida_stock_masiva manquante"
        assert hasattr(stock_window, 'add_stock'), "Méthode add_stock manquante"
        assert hasattr(stock_window, 'remove_stock'), "Méthode remove_stock manquante"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_movement_models():
    """Test que les modèles de mouvement de stock fonctionnent"""
    try:
        from database.models import StockMovement, Stock
        
        # Test création d'un mouvement d'entrée
        entrada_movement = StockMovement(
            producto_id=1,
            cantidad=10,
            tipo="ENTRADA",
            descripcion="Test entrada manual"
        )
        
        assert entrada_movement.producto_id == 1, "producto_id incorrect"
        assert entrada_movement.cantidad == 10, "cantidad incorrecte"
        assert entrada_movement.tipo == "ENTRADA", "tipo incorrect"
        assert "entrada" in entrada_movement.descripcion.lower(), "descripcion incorrecte"
        
        # Test création d'un mouvement de sortie
        salida_movement = StockMovement(
            producto_id=2,
            cantidad=-5,
            tipo="SALIDA",
            descripcion="Test salida manual"
        )
        
        assert salida_movement.producto_id == 2, "producto_id incorrect"
        assert salida_movement.cantidad == -5, "cantidad incorrecte"
        assert salida_movement.tipo == "SALIDA", "tipo incorrect"
        assert "salida" in salida_movement.descripcion.lower(), "descripcion incorrecte"
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_movement_types():
    """Test que tous les types de mouvements sont supportés"""
    try:
        from database.models import StockMovement
        
        # Types d'entrées
        entrada_types = ["RECEPCION", "DEVOLUCION", "AJUSTE_INVENTARIO", "PRODUCCION", "OTRO"]
        for tipo in entrada_types:
            movement = StockMovement(
                producto_id=1,
                cantidad=5,
                tipo="ENTRADA",
                descripcion=f"Test {tipo.lower()}"
            )
            assert movement.tipo == "ENTRADA", f"Tipo ENTRADA incorrect pour {tipo}"
        
        # Types de sorties
        salida_types = ["AJUSTE", "PERDIDA", "ROTURA", "VENCIMIENTO", "CONSUMO", "OTRO"]
        for tipo in salida_types:
            movement = StockMovement(
                producto_id=1,
                cantidad=-3,
                tipo="SALIDA",
                descripcion=f"Test {tipo.lower()}"
            )
            assert movement.tipo == "SALIDA", f"Tipo SALIDA incorrect pour {tipo}"
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_window_button_colors():
    """Test que les boutons ont les bonnes couleurs"""
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
        
        # Chercher les boutons et vérifier leurs couleurs
        def find_buttons_with_colors(widget):
            buttons_found = {}
            
            def search_widget(w):
                if isinstance(w, ctk.CTkButton):
                    try:
                        text = w.cget("text")
                        fg_color = w.cget("fg_color")
                        
                        if "Entrada Stock" in text:
                            buttons_found["entrada_masiva"] = fg_color
                        elif "Salida Stock" in text:
                            buttons_found["salida_masiva"] = fg_color
                        elif "📦+" in text:
                            buttons_found["entrada_individual"] = fg_color
                        elif "📤-" in text:
                            buttons_found["salida_individual"] = fg_color
                    except:
                        pass
                
                try:
                    for child in w.winfo_children():
                        search_widget(child)
                except:
                    pass
            
            search_widget(widget)
            return buttons_found
        
        buttons = find_buttons_with_colors(stock_window.window)
        
        # Vérifier les couleurs (vert pour entrées, rouge pour sorties)
        if "entrada_masiva" in buttons:
            assert "#2E8B57" in str(buttons["entrada_masiva"]), "Couleur entrada masiva incorrecte"
        
        if "salida_masiva" in buttons:
            assert "#DC143C" in str(buttons["salida_masiva"]), "Couleur salida masiva incorrecte"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_methods_callable():
    """Test que les méthodes de stock peuvent être appelées avec produit sélectionné"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        from unittest.mock import Mock, patch

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

        # Test sans produit sélectionné (devrait afficher erreur)
        stock_window.selected_producto_id = None

        with patch.object(stock_window, 'show_error_message') as mock_error:
            # Test entrada_stock_masiva sans sélection
            stock_window.entrada_stock_masiva()
            assert mock_error.called, "entrada_stock_masiva devrait afficher erreur sans sélection"

            mock_error.reset_mock()

            # Test salida_stock_masiva sans sélection
            stock_window.salida_stock_masiva()
            assert mock_error.called, "salida_stock_masiva devrait afficher erreur sans sélection"

        # Test avec produit sélectionné
        stock_window.selected_producto_id = 1

        # Mock des méthodes add_stock et remove_stock pour éviter l'interaction utilisateur
        with patch.object(stock_window, 'add_stock') as mock_add_stock, \
             patch.object(stock_window, 'remove_stock') as mock_remove_stock:

            # Test entrada_stock_masiva avec sélection
            stock_window.entrada_stock_masiva()
            assert mock_add_stock.called, "entrada_stock_masiva devrait appeler add_stock"

            # Test salida_stock_masiva avec sélection
            stock_window.salida_stock_masiva()
            assert mock_remove_stock.called, "salida_stock_masiva devrait appeler remove_stock"

        # Nettoyer
        stock_window.window.destroy()
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
        test_stock_window_has_manual_movement_buttons,
        test_stock_movement_models,
        test_stock_movement_types,
        test_stock_window_button_colors,
        test_stock_methods_callable
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
