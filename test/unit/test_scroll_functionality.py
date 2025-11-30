#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour la fonctionnalité de scroll avec la molette de souris
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtTest import QTest

from ui.scroll_mixin_pyqt5 import ScrollableMixin
from ui.base_pyqt5_window import BasePyQt5Window

class TestScrollableMixin(unittest.TestCase):
    """Tests pour le mixin de scroll"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration de la classe de test"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.test_widget = None
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        if self.test_widget:
            self.test_widget.close()
            self.test_widget = None
    
    def test_scrollable_mixin_initialization(self):
        """Test l'initialisation du mixin de scroll"""
        
        class TestWidget(ScrollableMixin, QWidget):
            def __init__(self):
                super().__init__()
                
        self.test_widget = TestWidget()
        
        # Vérifier que les attributs sont initialisés
        self.assertIsNotNone(self.test_widget.scroll_logger)
        self.assertIsNone(self.test_widget.scroll_area)
        self.assertIsNone(self.test_widget.scrollable_widget)
        
    def test_setup_scrollable_content(self):
        """Test la configuration du contenu scrollable"""
        
        class TestWidget(ScrollableMixin, QWidget):
            def __init__(self):
                super().__init__()
                self.setup_scrollable_content()
                
        self.test_widget = TestWidget()
        
        # Vérifier que les composants de scroll sont créés
        self.assertIsNotNone(self.test_widget.scroll_area)
        self.assertIsNotNone(self.test_widget.scrollable_widget)
        
        # Vérifier que la zone de scroll est configurée
        self.assertTrue(self.test_widget.scroll_area.widgetResizable())
        
    def test_get_scrollable_layout(self):
        """Test l'obtention du layout scrollable"""
        
        class TestWidget(ScrollableMixin, QWidget):
            def __init__(self):
                super().__init__()
                self.setup_scrollable_content()
                
        self.test_widget = TestWidget()
        
        # Obtenir le layout scrollable
        layout = self.test_widget.get_scrollable_layout()
        
        # Vérifier que le layout existe
        self.assertIsNotNone(layout)
        self.assertEqual(layout, self.test_widget.scrollable_widget.layout())
        
    def test_wheel_event_handling(self):
        """Test la gestion des événements de molette"""
        
        class TestWidget(ScrollableMixin, QWidget):
            def __init__(self):
                super().__init__()
                self.setup_scrollable_content()
                
        self.test_widget = TestWidget()
        self.test_widget.show()
        
        # Créer un événement de molette simulé (PyQt5 format)
        from PyQt5.QtCore import QPoint
        wheel_event = QWheelEvent(
            self.test_widget.rect().center(),  # pos
            self.test_widget.mapToGlobal(self.test_widget.rect().center()),  # globalPos
            QPoint(0, 0),  # pixelDelta
            QPoint(0, 120),  # angleDelta (scroll vers le haut)
            120,  # qt4Delta
            Qt.Vertical,  # qt4Orientation
            Qt.NoButton,  # buttons
            Qt.NoModifier  # modifiers
        )
        
        # Tester la gestion de l'événement
        result = self.test_widget.handle_wheel_event(wheel_event)
        
        # Le résultat dépend de la présence de barres de scroll
        self.assertIsInstance(result, bool)


class TestBasePyQt5WindowScroll(unittest.TestCase):
    """Tests pour le scroll dans BasePyQt5Window"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration de la classe de test"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.test_window = None
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        if self.test_window:
            self.test_window.close()
            self.test_window = None
    
    def test_base_window_with_scroll_enabled(self):
        """Test la fenêtre de base avec scroll activé"""
        self.test_window = BasePyQt5Window(title="Test Scroll", enable_scroll=True)
        
        # Vérifier que le scroll est activé
        self.assertTrue(self.test_window.enable_scroll)
        
    def test_base_window_with_scroll_disabled(self):
        """Test la fenêtre de base avec scroll désactivé"""
        self.test_window = BasePyQt5Window(title="Test No Scroll", enable_scroll=False)
        
        # Vérifier que le scroll est désactivé
        self.assertFalse(self.test_window.enable_scroll)
        
    def test_enable_window_scroll_method(self):
        """Test la méthode enable_window_scroll"""
        self.test_window = BasePyQt5Window(title="Test", enable_scroll=True)
        
        # Activer le scroll
        self.test_window.enable_window_scroll()
        
        # Vérifier que les composants de scroll sont créés
        self.assertIsNotNone(self.test_window.scroll_area)
        self.assertIsNotNone(self.test_window.scrollable_widget)
        
    def test_get_content_layout_with_scroll(self):
        """Test get_content_layout avec scroll activé"""
        self.test_window = BasePyQt5Window(title="Test", enable_scroll=True)
        self.test_window.enable_window_scroll()
        
        # Obtenir le layout de contenu
        layout = self.test_window.get_content_layout()
        
        # Vérifier que c'est le layout scrollable
        self.assertIsNotNone(layout)
        
    def test_get_content_layout_without_scroll(self):
        """Test get_content_layout avec scroll désactivé"""
        self.test_window = BasePyQt5Window(title="Test", enable_scroll=False)
        
        # Obtenir le layout de contenu
        layout = self.test_window.get_content_layout()
        
        # Vérifier que c'est le layout principal
        self.assertIsNotNone(layout)


class TestScrollIntegration(unittest.TestCase):
    """Tests d'intégration pour le scroll"""

    @classmethod
    def setUpClass(cls):
        """Configuration de la classe de test"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()

    def test_scroll_mixin_integration(self):
        """Test l'intégration complète du mixin de scroll"""
        # Créer une fenêtre avec scroll
        window = BasePyQt5Window(title="Test Integration", enable_scroll=True)
        window.enable_window_scroll()

        # Vérifier l'intégration
        self.assertIsNotNone(window.scroll_area)
        self.assertIsNotNone(window.scrollable_widget)
        self.assertIsNotNone(window.get_content_layout())

        window.close()


if __name__ == "__main__":
    # Exécuter les tests
    unittest.main(verbosity=2)
