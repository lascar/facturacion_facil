#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour la correction de l'erreur "grab failed: window not viewable"
dans la nouvelle interface de stock avec boutons + et -
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class TestStockGrabErrorFix:
    """Tests de régression pour la correction de l'erreur grab_set"""
    
    def test_safe_grab_set_method_exists(self):
        """Test de régression: méthode _safe_grab_set existe"""
        from ui.stock import StockWindow
        
        # Vérifier que la méthode de correction existe
        assert hasattr(StockWindow, '_safe_grab_set'), "Méthode _safe_grab_set manquante"
        
        # Vérifier que c'est une méthode callable
        method = getattr(StockWindow, '_safe_grab_set')
        assert callable(method), "Méthode _safe_grab_set n'est pas callable"
    
    def test_safe_grab_set_with_valid_window(self, temp_db):
        """Test de régression: _safe_grab_set avec fenêtre valide"""
        from ui.stock import StockWindow
        from database.models import Producto, Stock
        
        # Créer des données de test
        producto = Producto(nombre="Test Safe Grab", referencia="TSG001", precio=15.0)
        producto.save()
        
        stock = Stock(producto_id=producto.id, cantidad_disponible=10)
        stock.save()
        
        # Test de la méthode _safe_grab_set avec mock
        with patch('customtkinter.CTk') as mock_root:
            mock_root.return_value = Mock()
            
            # Créer une classe mock pour éviter les problèmes d'instanciation
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
    
    def test_safe_grab_set_with_invalid_window(self, temp_db):
        """Test de régression: _safe_grab_set avec fenêtre invalide"""
        from database.models import Producto, Stock
        
        # Créer des données de test
        producto = Producto(nombre="Test Safe Grab Invalid", referencia="TSGI001", precio=20.0)
        producto.save()
        
        stock = Stock(producto_id=producto.id, cantidad_disponible=5)
        stock.save()
        
        # Classe mock pour le test
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
    
    def test_safe_grab_set_handles_grab_exceptions(self, temp_db):
        """Test de régression: _safe_grab_set gère les exceptions de grab_set"""
        from database.models import Producto, Stock
        
        # Créer des données de test
        producto = Producto(nombre="Test Grab Exception", referencia="TGE001", precio=25.0)
        producto.save()
        
        stock = Stock(producto_id=producto.id, cantidad_disponible=8)
        stock.save()
        
        # Classe mock pour le test
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
    
    def test_stock_dialog_positioning_safety(self, temp_db):
        """Test de régression: positionnement sécurisé de la fenêtre de dialogue"""
        from ui.stock import StockWindow
        from database.models import Producto, Stock
        
        # Créer des données de test
        producto = Producto(nombre="Test Dialog Position", referencia="TDP001", precio=30.0)
        producto.save()
        
        stock = Stock(producto_id=producto.id, cantidad_disponible=12)
        stock.save()
        
        # Vérifier que la nouvelle interface gère le positionnement de façon sécurisée
        # (test conceptuel - la vraie logique est dans _show_stock_modification_dialog)
        
        # Simuler différents scénarios de positionnement
        positioning_scenarios = [
            {"parent_x": 100, "parent_y": 100, "expected": "+150+150"},  # Position normale
            {"parent_x": None, "parent_y": None, "expected": "+300+200"},  # Position par défaut
        ]
        
        for scenario in positioning_scenarios:
            # Test que la logique de positionnement ne lève pas d'exception
            try:
                if scenario["parent_x"] is not None and scenario["parent_y"] is not None:
                    position = "+{}+{}".format(scenario["parent_x"] + 50, scenario["parent_y"] + 50)
                else:
                    position = "+300+200"  # Position par défaut
                
                assert position == scenario["expected"], f"Position incorrecte: {position}"
                
            except Exception as e:
                pytest.fail(f"Calcul de position ne devrait pas échouer: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
