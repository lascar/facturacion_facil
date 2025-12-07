#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests d'intégration avancés pour l'interface utilisateur
Tests spécifiques pour la solution de forçage maximal Nueva Factura
"""

import pytest
import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


class TestUIIntegrationAdvanced:
    """Tests d'intégration avancés pour l'interface utilisateur"""
    
    @pytest.fixture(autouse=True)
    def setup_app(self):
        """Setup de l'application Qt"""
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
    
    def test_integration_nueva_factura_workflow_complet(self):
        """
        Test d'intégration complet du workflow Nueva Factura
        
        Teste l'intégration complète de la solution de forçage maximal
        dans le contexte de l'application complète
        """
        # Initialisation complète de l'application
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.5)
        
        # Test du workflow complet Facturas -> Nueva Factura
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        assert facturas_window is not None, "Fenêtre Facturas doit être créée"
        assert facturas_window.isVisible(), "Fenêtre Facturas doit être visible"
        
        # Simulation d'utilisation réelle
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(1.0)
        
        # Ouverture Nueva Factura (point critique)
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        # Vérifications d'intégration
        dialog = facturas_window.crear_dialog
        assert dialog is not None, "Dialog Nueva Factura doit être créé"
        assert dialog.isVisible(), "Dialog doit être visible"
        assert dialog.isActiveWindow(), "Dialog doit être au premier plan"
        
        # Test d'intégration avec les flags
        flags = dialog.windowFlags()
        has_forcing_flags = any([
            bool(flags & Qt.WindowStaysOnTopHint),
            bool(flags & Qt.X11BypassWindowManagerHint),
            bool(flags & Qt.Tool),
            bool(flags & Qt.FramelessWindowHint)
        ])
        assert has_forcing_flags, "Flags de forçage doivent être intégrés"
        
        # Test d'intégration de la résistance
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.3)
        
        assert dialog.isVisible(), "Dialog doit résister aux changements de focus"
        
        # Test d'intégration de la stabilité long terme
        time.sleep(2.5)
        self.app.processEvents()
        
        assert dialog.isVisible(), "Dialog doit rester stable dans l'intégration complète"
    
    def test_integration_multiple_windows_interaction(self):
        """
        Test d'intégration des interactions entre multiples fenêtres
        
        Vérifie que la solution de forçage n'interfère pas avec les autres fenêtres
        """
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        
        # Ouvrir plusieurs fenêtres
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier que les autres fenêtres restent fonctionnelles
        assert self.main_window.isVisible(), "Fenêtre principale doit rester visible"
        assert facturas_window.isVisible(), "Fenêtre Facturas doit rester visible"
        assert dialog.isVisible(), "Dialog Nueva Factura doit être visible"
        
        # Test d'interaction entre fenêtres
        self.main_window.raise_()
        self.app.processEvents()
        time.sleep(0.2)
        
        # Toutes les fenêtres doivent rester accessibles
        assert self.main_window.isVisible(), "Fenêtre principale doit rester accessible"
        assert facturas_window.isVisible(), "Fenêtre Facturas doit rester accessible"
        assert dialog.isVisible(), "Dialog doit rester accessible malgré les interactions"
    
    def test_integration_solution_components_ensemble(self):
        """
        Test d'intégration de tous les composants de la solution ensemble
        
        Vérifie que tous les éléments de la solution de forçage maximal
        fonctionnent ensemble harmonieusement
        """
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        
        # Composant 1: Dialog sans parent
        assert dialog.parent() is None, "Composant sans parent doit être intégré"
        
        # Composant 2: Flags de forçage maximal
        flags = dialog.windowFlags()
        assert bool(flags & Qt.WindowStaysOnTopHint), "WindowStaysOnTopHint doit être intégré"
        assert bool(flags & Qt.Window), "Window flag doit être intégré"
        
        # Composant 3: Politique de focus forte
        assert dialog.focusPolicy() == Qt.StrongFocus, "Focus policy doit être intégrée"
        
        # Composant 4: État de fenêtre actif
        assert dialog.isActiveWindow(), "État actif doit être intégré"
        
        # Composant 5: Visibilité garantie
        assert dialog.isVisible(), "Visibilité doit être garantie"
        
        # Test d'intégration temporelle (maintien + nettoyage)
        time.sleep(2.2)
        self.app.processEvents()
        
        # Après nettoyage, le dialog doit rester fonctionnel
        assert dialog.isVisible(), "Dialog doit rester fonctionnel après nettoyage intégré"
    
    def test_integration_performance_impact(self):
        """
        Test d'intégration de l'impact sur les performances
        
        Vérifie que la solution de forçage maximal n'impacte pas négativement
        les performances de l'application
        """
        import time
        
        # Mesurer le temps d'ouverture sans forçage (baseline)
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Mesurer le temps d'ouverture avec forçage maximal
        start_time = time.time()
        facturas_window.new_factura()
        self.app.processEvents()
        end_time = time.time()
        
        dialog = facturas_window.crear_dialog
        assert dialog is not None, "Dialog doit être créé malgré les optimisations"
        assert dialog.isVisible(), "Dialog doit être visible malgré les optimisations"
        
        # Le temps d'ouverture ne doit pas être excessif (< 1 seconde)
        opening_time = end_time - start_time
        assert opening_time < 1.0, f"Temps d'ouverture trop long: {opening_time}s"
        
        # Vérifier que l'application reste responsive
        self.app.processEvents()
        assert self.main_window.isVisible(), "Application doit rester responsive"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
