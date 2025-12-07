#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour le problème "Nueva Factura apparaît en second plan"
Ce test s'assure que le problème résolu ne revient pas dans les futures versions
"""

import pytest
import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


class TestNuevaFacturaPositioningRegression:
    """Tests de régression pour le positionnement de Nueva Factura"""
    
    @pytest.fixture(autouse=True)
    def setup_app(self):
        """Setup de l'application Qt pour les tests"""
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        yield
        # Cleanup
        if hasattr(self, 'main_window'):
            try:
                if hasattr(self.main_window, 'facturas_window') and self.main_window.facturas_window:
                    if hasattr(self.main_window.facturas_window, 'crear_dialog') and self.main_window.facturas_window.crear_dialog:
                        self.main_window.facturas_window.crear_dialog.close()
                    self.main_window.facturas_window.close()
                self.main_window.close()
            except:
                pass
    
    def test_regression_nueva_factura_never_behind(self):
        """
        Test de régression principal: Nueva Factura ne doit JAMAIS apparaître en second plan
        
        Ce test reproduit le problème original et vérifie qu'il est résolu:
        - Ouvrir l'application
        - Ouvrir Facturas
        - Cliquer Nueva Factura
        - Vérifier que le dialog apparaît AU PREMIER PLAN
        """
        # Reproduire le scénario problématique original
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.app.processEvents()
        
        # Ouvrir facturas (comme dans le problème original)
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # S'assurer que facturas est bien au premier plan (condition du problème)
        facturas_window.raise_()
        facturas_window.activateWindow()
        facturas_window.setFocus()
        self.app.processEvents()
        time.sleep(0.5)
        
        # MOMENT CRITIQUE: Clic sur Nueva Factura (où le problème se manifestait)
        facturas_window.new_factura()
        
        # Vérification IMMÉDIATE (ce que l'utilisateur voit)
        self.app.processEvents()
        time.sleep(0.2)
        
        # ASSERTIONS CRITIQUES pour éviter la régression
        dialog = facturas_window.crear_dialog
        assert dialog is not None, "RÉGRESSION: Dialog Nueva Factura ne se crée pas"
        assert dialog.isVisible(), "RÉGRESSION: Dialog Nueva Factura n'est pas visible"
        assert dialog.isActiveWindow(), "RÉGRESSION: Dialog Nueva Factura n'est pas au premier plan"
        
        # Vérifier que les flags de forçage sont appliqués
        flags = dialog.windowFlags()
        has_forcing_flags = any([
            bool(flags & Qt.WindowStaysOnTopHint),
            bool(flags & Qt.X11BypassWindowManagerHint),
            bool(flags & Qt.Tool),
            bool(flags & Qt.FramelessWindowHint)
        ])
        assert has_forcing_flags, "RÉGRESSION: Aucun flag de forçage appliqué"
    
    def test_regression_multiple_attempts(self):
        """
        Test de régression: Multiples tentatives d'ouverture Nueva Factura
        
        Vérifie que le problème ne revient pas même après plusieurs ouvertures/fermetures
        """
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Tester 3 ouvertures/fermetures successives
        for i in range(3):
            # Ouvrir Nueva Factura
            facturas_window.new_factura()
            self.app.processEvents()
            time.sleep(0.2)
            
            dialog = facturas_window.crear_dialog
            assert dialog is not None, f"RÉGRESSION tentative {i+1}: Dialog ne se crée pas"
            assert dialog.isVisible(), f"RÉGRESSION tentative {i+1}: Dialog pas visible"
            assert dialog.isActiveWindow(), f"RÉGRESSION tentative {i+1}: Dialog pas au premier plan"
            
            # Fermer le dialog
            dialog.close()
            self.app.processEvents()
            time.sleep(0.1)
    
    def test_regression_with_window_manager_interference(self):
        """
        Test de régression avec interférence du gestionnaire de fenêtres
        
        Simule les conditions où le gestionnaire de fenêtres pourrait interférer
        """
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Forcer facturas au premier plan de manière agressive
        for _ in range(3):
            facturas_window.raise_()
            facturas_window.activateWindow()
            facturas_window.setFocus()
            self.app.processEvents()
            time.sleep(0.1)
        
        # Maintenant ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        assert dialog is not None, "RÉGRESSION: Dialog ne résiste pas à l'interférence WM"
        assert dialog.isVisible(), "RÉGRESSION: Dialog pas visible malgré forçage"
        
        # Vérifier que le dialog résiste aux tentatives de masquage
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.2)
        
        # Le dialog doit toujours être accessible
        assert dialog.isVisible(), "RÉGRESSION: Dialog masqué par interférence WM"
    
    def test_regression_solution_components(self):
        """
        Test de régression des composants de la solution
        
        Vérifie que tous les éléments de la solution de forçage maximal sont présents
        """
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.2)
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier que le dialog est créé sans parent (solution sans parent)
        parent = dialog.parent()
        assert parent is None, "RÉGRESSION: Dialog a un parent (problème de hiérarchie)"
        
        # Vérifier les flags de la solution de forçage maximal
        flags = dialog.windowFlags()
        
        # Au moins WindowStaysOnTopHint doit être présent
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        assert has_stay_on_top, "RÉGRESSION: WindowStaysOnTopHint manquant"
        
        # Window flag doit être présent
        has_window = bool(flags & Qt.Window)
        assert has_window, "RÉGRESSION: Window flag manquant"
        
        # Vérifier que le dialog a une politique de focus forte
        focus_policy = dialog.focusPolicy()
        assert focus_policy == Qt.StrongFocus, "RÉGRESSION: Politique de focus faible"
    
    def test_regression_timing_stability(self):
        """
        Test de régression de la stabilité temporelle
        
        Vérifie que la solution reste stable dans le temps
        """
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier la stabilité à différents moments
        time_points = [0.1, 0.5, 1.0, 2.0, 3.0]  # secondes
        
        for t in time_points:
            time.sleep(t - (time_points[time_points.index(t) - 1] if time_points.index(t) > 0 else 0))
            self.app.processEvents()
            
            assert dialog.isVisible(), f"RÉGRESSION: Dialog instable à t={t}s"
            
            # À partir de 2 secondes, vérifier que le nettoyage a eu lieu mais que le dialog reste stable
            if t >= 2.0:
                # Le dialog doit toujours être visible même après nettoyage
                assert dialog.isVisible(), f"RÉGRESSION: Dialog disparu après nettoyage à t={t}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
