# -*- coding: utf-8 -*-
"""
Tests de base pour QTest et PyQt5 - sans interface graphique complète
"""

import pytest
import sys
import os
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.logger import get_logger


class TestQTestBasic:
    """Tests de base pour QTest sans interface complète"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self):
        """Configuration pour chaque test"""
        self.logger = get_logger(self.__class__.__name__)
        
        # Créer une application Qt si elle n'existe pas
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        
        yield
        
        # Nettoyage
        if hasattr(self, 'widget'):
            self.widget.close()
    
    def test_qtest_button_click(self):
        """Test de clic sur bouton avec QTest"""
        self.logger.info("🧪 Test: Clic bouton avec QTest")
        
        # Créer un widget simple
        self.widget = QWidget()
        layout = QVBoxLayout()
        
        button = QPushButton("Test Button")
        layout.addWidget(button)
        
        self.widget.setLayout(layout)
        self.widget.show()
        
        # Variable pour vérifier le clic
        clicked = False
        
        def on_button_clicked():
            nonlocal clicked
            clicked = True
        
        button.clicked.connect(on_button_clicked)
        
        # Attendre que le widget soit visible
        QTest.qWait(100)
        self.app.processEvents()
        
        # Cliquer avec QTest
        QTest.mouseClick(button, Qt.LeftButton)
        QTest.qWait(50)
        self.app.processEvents()
        
        # Vérifier que le clic a fonctionné
        assert clicked, "Le bouton n'a pas été cliqué"
        self.logger.info("✅ Test clic bouton réussi")
    
    def test_qtest_text_input(self):
        """Test de saisie de texte avec QTest"""
        self.logger.info("🧪 Test: Saisie texte avec QTest")
        
        # Créer un widget simple
        self.widget = QWidget()
        layout = QVBoxLayout()
        
        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        
        self.widget.setLayout(layout)
        self.widget.show()
        
        # Attendre que le widget soit visible
        QTest.qWait(100)
        self.app.processEvents()
        
        # Donner le focus au champ
        line_edit.setFocus()
        QTest.qWait(50)
        
        # Saisir du texte avec QTest
        test_text = "Hello QTest!"
        QTest.keyClicks(line_edit, test_text)
        QTest.qWait(50)
        self.app.processEvents()
        
        # Vérifier que le texte a été saisi
        assert line_edit.text() == test_text, f"Texte incorrect: {line_edit.text()}"
        self.logger.info("✅ Test saisie texte réussi")
    
    def test_qtest_key_sequence(self):
        """Test de séquence de touches avec QTest"""
        self.logger.info("🧪 Test: Séquence touches avec QTest")
        
        # Créer un widget simple
        self.widget = QWidget()
        layout = QVBoxLayout()
        
        line_edit = QLineEdit()
        layout.addWidget(line_edit)
        
        self.widget.setLayout(layout)
        self.widget.show()
        
        # Attendre que le widget soit visible
        QTest.qWait(100)
        self.app.processEvents()
        
        # Donner le focus au champ
        line_edit.setFocus()
        QTest.qWait(50)
        
        # Saisir du texte
        QTest.keyClicks(line_edit, "Test Selection")
        QTest.qWait(50)
        
        # Sélectionner tout avec Ctrl+A
        QTest.keyClick(line_edit, Qt.Key_A, Qt.ControlModifier)
        QTest.qWait(50)
        
        # Vérifier que le texte est sélectionné
        assert line_edit.hasSelectedText(), "Texte non sélectionné"
        assert line_edit.selectedText() == "Test Selection", "Sélection incorrecte"
        
        # Remplacer par nouveau texte
        QTest.keyClicks(line_edit, "Replaced Text")
        QTest.qWait(50)
        
        # Vérifier le remplacement
        assert line_edit.text() == "Replaced Text", f"Remplacement incorrect: {line_edit.text()}"
        self.logger.info("✅ Test séquence touches réussi")
    
    def test_qtest_widget_properties(self):
        """Test de vérification des propriétés de widget"""
        self.logger.info("🧪 Test: Propriétés widget avec QTest")
        
        # Créer un widget simple
        self.widget = QWidget()
        self.widget.setWindowTitle("Test Widget")
        self.widget.resize(300, 200)
        self.widget.show()
        
        # Attendre que le widget soit visible
        QTest.qWait(100)
        self.app.processEvents()
        
        # Vérifier les propriétés
        assert self.widget.isVisible(), "Widget non visible"
        assert self.widget.windowTitle() == "Test Widget", "Titre incorrect"
        assert self.widget.width() == 300, f"Largeur incorrecte: {self.widget.width()}"
        assert self.widget.height() == 200, f"Hauteur incorrecte: {self.widget.height()}"
        
        self.logger.info("✅ Test propriétés widget réussi")
    
    def test_qtest_timing_and_events(self):
        """Test de timing et traitement d'événements"""
        self.logger.info("🧪 Test: Timing et événements QTest")
        
        # Créer un widget simple
        self.widget = QWidget()
        button = QPushButton("Timer Test")
        layout = QVBoxLayout()
        layout.addWidget(button)
        self.widget.setLayout(layout)
        self.widget.show()
        
        # Variable pour compter les clics
        click_count = 0
        
        def on_clicked():
            nonlocal click_count
            click_count += 1
        
        button.clicked.connect(on_clicked)
        
        # Attendre que le widget soit prêt
        QTest.qWait(100)
        self.app.processEvents()
        
        # Effectuer plusieurs clics avec timing
        for i in range(3):
            QTest.mouseClick(button, Qt.LeftButton)
            QTest.qWait(50)  # Attendre entre les clics
            self.app.processEvents()
        
        # Vérifier que tous les clics ont été traités
        assert click_count == 3, f"Nombre de clics incorrect: {click_count}"
        
        self.logger.info("✅ Test timing et événements réussi")
