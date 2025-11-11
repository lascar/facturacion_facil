#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour s'assurer que les erreurs de stock sont corrigées
"""

import sys
import os
import pytest

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def test_stock_window_has_modify_stock_method():
    """Test que StockWindow a la méthode modify_stock et pas actualizar_stock"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()
        
        # Vérifier que modify_stock existe
        assert hasattr(stock_window, 'modify_stock'), "Méthode modify_stock manquante"
        
        # Vérifier que actualizar_stock n'existe pas (pour éviter la confusion)
        assert not hasattr(stock_window, 'actualizar_stock'), "Méthode actualizar_stock ne devrait pas exister"
        
        # Vérifier que actualizar_stock_selected existe
        assert hasattr(stock_window, 'actualizar_stock_selected'), "Méthode actualizar_stock_selected manquante"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_window_dialog_methods_exist():
    """Test que toutes les méthodes de diálogo existent"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()
        
        # Vérifier que toutes les méthodes de diálogo existent
        required_methods = [
            'entrada_stock_masiva',
            'salida_stock_masiva',
            'add_stock',
            'remove_stock',
            'modify_stock'
        ]
        
        for method_name in required_methods:
            assert hasattr(stock_window, method_name), f"Méthode {method_name} manquante"
            assert callable(getattr(stock_window, method_name)), f"Méthode {method_name} n'est pas callable"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_window_safe_grab_set():
    """Test que les diálogos gèrent grab_set de façon sécurisée"""
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

        # Sélectionner un produit pour que les méthodes puissent fonctionner
        stock_window.selected_producto_id = 1

        # Test que les méthodes peuvent être appelées sans erreur de grab_set
        # Mock des méthodes add_stock et remove_stock pour éviter l'interaction utilisateur
        with patch.object(stock_window, 'add_stock') as mock_add_stock, \
             patch.object(stock_window, 'remove_stock') as mock_remove_stock:

            # Test entrada_stock_masiva avec produit sélectionné
            try:
                stock_window.entrada_stock_masiva()
                # Vérifier que add_stock a été appelé
                assert mock_add_stock.called, "entrada_stock_masiva devrait appeler add_stock"
            except Exception as e:
                # Ne devrait pas y avoir d'erreur
                assert False, f"entrada_stock_masiva a échoué: {e}"

            # Test salida_stock_masiva avec produit sélectionné
            try:
                stock_window.salida_stock_masiva()
                # Vérifier que remove_stock a été appelé
                assert mock_remove_stock.called, "salida_stock_masiva devrait appeler remove_stock"
            except Exception as e:
                # Ne devrait pas y avoir d'erreur
                assert False, f"salida_stock_masiva a échoué: {e}"

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

        # Nettoyer
        stock_window.window.destroy()
        root.destroy()

        return True

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_window_logger_exists():
    """Test que StockWindow a un logger fonctionnel"""
    try:
        import customtkinter as ctk
        from ui.stock import StockWindow
        
        # Créer une fenêtre racine (cachée)
        root = ctk.CTk()
        root.withdraw()
        
        # Créer StockWindow
        stock_window = StockWindow(root)
        stock_window.window.withdraw()
        
        # Vérifier que le logger existe
        assert hasattr(stock_window, 'logger'), "Logger manquant"
        
        # Vérifier que le logger peut être utilisé
        try:
            stock_window.logger.info("Test de régression logger")
            assert True, "Logger fonctionnel"
        except Exception as e:
            assert False, f"Logger non fonctionnel: {e}"
        
        # Nettoyer
        stock_window.window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_models_importable():
    """Test que les modèles de stock peuvent être importés"""
    try:
        from database.models import Stock, StockMovement
        
        # Test création d'objets
        stock = Stock(producto_id=1, cantidad=10)
        assert stock.producto_id == 1, "Stock producto_id incorrect"
        assert stock.cantidad == 10, "Stock cantidad incorrecte"
        
        movement = StockMovement(
            producto_id=1,
            cantidad=5,
            tipo="ENTRADA",
            descripcion="Test"
        )
        assert movement.producto_id == 1, "StockMovement producto_id incorrect"
        assert movement.cantidad == 5, "StockMovement cantidad incorrecte"
        assert movement.tipo == "ENTRADA", "StockMovement tipo incorrect"
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Exécuter les tests
    tests = [
        test_stock_window_has_modify_stock_method,
        test_stock_window_dialog_methods_exist,
        test_stock_window_safe_grab_set,
        test_stock_window_logger_exists,
        test_stock_models_importable
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
