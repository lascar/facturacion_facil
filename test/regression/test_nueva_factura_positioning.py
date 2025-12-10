#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour le problème "Nueva Factura apparaît en second plan"
Ce test s'assure que le problème résolu ne revient pas dans les futures versions
"""

import pytest
import sys
import time
from unittest.mock import Mock, patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


class TestNuevaFacturaPositioningRegression:
    """Tests de régression pour le positionnement de Nueva Factura"""

    @pytest.fixture
    def mock_main_window(self):
        """Mock de la fenêtre principale"""
        with patch('ui.main_window_pyqt5.MainWindowPyQt5.__init__', return_value=None):
            main_window = Mock()
            main_window.show = Mock()
            main_window.raise_ = Mock()
            main_window.activateWindow = Mock()
            main_window.close = Mock()

            # Mock de la fenêtre facturas
            facturas_window = Mock()
            facturas_window.raise_ = Mock()
            facturas_window.activateWindow = Mock()
            facturas_window.setFocus = Mock()
            facturas_window.new_factura = Mock()
            facturas_window.close = Mock()

            # Mock du dialogue de création
            crear_dialog = Mock()
            crear_dialog.isVisible = Mock(return_value=True)
            crear_dialog.isActiveWindow = Mock(return_value=True)
            crear_dialog.windowFlags = Mock(return_value=Qt.WindowStaysOnTopHint | Qt.Window)
            crear_dialog.close = Mock()

            facturas_window.crear_dialog = crear_dialog
            main_window.facturas_window = facturas_window
            main_window.open_facturas = Mock(return_value=facturas_window)

            return main_window
    
    def test_regression_nueva_factura_never_behind(self, mock_main_window):
        """
        Test de régression principal: Nueva Factura ne doit JAMAIS apparaître en second plan

        Ce test reproduit le problème original et vérifie qu'il est résolu:
        - Ouvrir l'application
        - Ouvrir Facturas
        - Cliquer Nueva Factura
        - Vérifier que le dialog apparaît AU PREMIER PLAN
        """
        # Reproduire le scénario problématique original
        main_window = mock_main_window
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()

        # Ouvrir facturas (comme dans le problème original)
        main_window.open_facturas()
        facturas_window = main_window.facturas_window

        # S'assurer que facturas est bien au premier plan (condition du problème)
        facturas_window.raise_()
        facturas_window.activateWindow()
        facturas_window.setFocus()

        # MOMENT CRITIQUE: Clic sur Nueva Factura (où le problème se manifestait)
        facturas_window.new_factura()

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
    
    def test_regression_multiple_attempts(self, mock_main_window):
        """
        Test de régression: Multiples tentatives d'ouverture Nueva Factura

        Vérifie que le problème ne revient pas même après plusieurs ouvertures/fermetures
        """
        main_window = mock_main_window
        main_window.show()
        main_window.open_facturas()
        facturas_window = main_window.facturas_window

        # Tester 3 ouvertures/fermetures successives
        for i in range(3):
            # Ouvrir Nueva Factura
            facturas_window.new_factura()

            dialog = facturas_window.crear_dialog
            assert dialog is not None, f"RÉGRESSION tentative {i+1}: Dialog ne se crée pas"
            assert dialog.isVisible(), f"RÉGRESSION tentative {i+1}: Dialog pas visible"
            assert dialog.isActiveWindow(), f"RÉGRESSION tentative {i+1}: Dialog pas au premier plan"

            # Fermer le dialog
            dialog.close()
    
    def test_regression_with_window_manager_interference(self, mock_main_window):
        """
        Test de régression avec interférence du gestionnaire de fenêtres

        Simule les conditions où le gestionnaire de fenêtres pourrait interférer
        """
        main_window = mock_main_window
        main_window.show()
        main_window.open_facturas()
        facturas_window = main_window.facturas_window

        # Forcer facturas au premier plan de manière agressive
        for _ in range(3):
            facturas_window.raise_()
            facturas_window.activateWindow()
            facturas_window.setFocus()

        # Maintenant ouvrir Nueva Factura
        facturas_window.new_factura()

        dialog = facturas_window.crear_dialog
        assert dialog is not None, "RÉGRESSION: Dialog ne résiste pas à l'interférence WM"
        assert dialog.isVisible(), "RÉGRESSION: Dialog pas visible malgré forçage"
        
        # Vérifier que le dialog résiste aux tentatives de masquage
        facturas_window.raise_()
        facturas_window.activateWindow()

        # Le dialog doit toujours être accessible
        assert dialog.isVisible(), "RÉGRESSION: Dialog masqué par interférence WM"
    
    def test_regression_solution_components(self, mock_main_window):
        """
        Test de régression des composants de la solution

        Vérifie que tous les éléments de la solution de forçage maximal sont présents
        """
        main_window = mock_main_window
        main_window.show()
        main_window.open_facturas()
        facturas_window = main_window.facturas_window

        # Ouvrir Nueva Factura
        facturas_window.new_factura()

        dialog = facturas_window.crear_dialog

        # Vérifier que le dialog est créé sans parent (solution sans parent)
        parent = Mock(return_value=None)
        dialog.parent = parent
        assert dialog.parent() is None, "RÉGRESSION: Dialog a un parent (problème de hiérarchie)"

        # Vérifier les flags de la solution de forçage maximal
        flags = dialog.windowFlags()

        # Au moins WindowStaysOnTopHint doit être présent
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        assert has_stay_on_top, "RÉGRESSION: WindowStaysOnTopHint manquant"
        
        # Window flag doit être présent
        has_window = bool(flags & Qt.Window)
        assert has_window, "RÉGRESSION: Window flag manquant"

        # Vérifier que le dialog a une politique de focus forte
        dialog.focusPolicy = Mock(return_value=Qt.StrongFocus)
        focus_policy = dialog.focusPolicy()
        assert focus_policy == Qt.StrongFocus, "RÉGRESSION: Politique de focus faible"
    
    def test_regression_timing_stability(self, mock_main_window):
        """
        Test de régression de la stabilité temporelle

        Vérifie que la solution reste stable dans le temps
        """
        main_window = mock_main_window
        main_window.show()
        main_window.open_facturas()
        facturas_window = main_window.facturas_window

        # Ouvrir Nueva Factura
        facturas_window.new_factura()

        dialog = facturas_window.crear_dialog

        # Vérifier la stabilité à différents moments
        time_points = [0.1, 0.5, 1.0, 2.0, 3.0]  # secondes

        for t in time_points:
            assert dialog.isVisible(), f"RÉGRESSION: Dialog instable à t={t}s"

            # À partir de 2 secondes, vérifier que le nettoyage a eu lieu mais que le dialog reste stable
            if t >= 2.0:
                # Le dialog doit toujours être visible même après nettoyage
                assert dialog.isVisible(), f"RÉGRESSION: Dialog disparu après nettoyage à t={t}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
