#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration de la solution QTest pour les tests de comportement PyQt5
Remplace Selenium pour tester les applications PyQt5
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.logger import get_logger


class DemoQTestSolution:
    """Démonstration de la solution QTest pour PyQt5"""
    
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        
        # Créer l'application Qt
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
    
    def demo_basic_interactions(self):
        """Démonstration des interactions de base avec QTest"""
        self.logger.info("🎯 DÉMONSTRATION: Interactions de base QTest")
        
        # Créer un widget de démonstration
        widget = QWidget()
        widget.setWindowTitle("Démo QTest - Interactions de Base")
        widget.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Ajouter des éléments
        label = QLabel("Démonstration QTest pour PyQt5")
        input_field = QLineEdit()
        input_field.setPlaceholderText("Tapez quelque chose ici...")
        button = QPushButton("Cliquez-moi!")
        result_label = QLabel("Résultat: En attente...")
        
        layout.addWidget(label)
        layout.addWidget(input_field)
        layout.addWidget(button)
        layout.addWidget(result_label)
        
        widget.setLayout(layout)
        widget.show()
        
        # Fonction de callback pour le bouton
        def on_button_clicked():
            text = input_field.text()
            result_label.setText(f"Résultat: Vous avez tapé '{text}'")
        
        button.clicked.connect(on_button_clicked)
        
        # Attendre que le widget soit visible
        QTest.qWait(200)
        self.app.processEvents()
        
        self.logger.info("✅ Widget créé et affiché")
        
        # === DÉMONSTRATION DES INTERACTIONS QTEST ===
        
        # 1. Saisie de texte avec QTest
        self.logger.info("🔤 Test: Saisie de texte avec QTest.keyClicks()")
        input_field.setFocus()
        QTest.qWait(100)
        
        test_text = "Hello QTest!"
        QTest.keyClicks(input_field, test_text)
        QTest.qWait(100)
        self.app.processEvents()
        
        assert input_field.text() == test_text
        self.logger.info(f"✅ Texte saisi: '{input_field.text()}'")
        
        # 2. Clic de bouton avec QTest
        self.logger.info("🖱️ Test: Clic de bouton avec QTest.mouseClick()")
        QTest.mouseClick(button, Qt.LeftButton)
        QTest.qWait(100)
        self.app.processEvents()
        
        expected_result = f"Résultat: Vous avez tapé '{test_text}'"
        assert result_label.text() == expected_result
        self.logger.info(f"✅ Bouton cliqué, résultat: '{result_label.text()}'")
        
        # 3. Séquence de touches avancée
        self.logger.info("⌨️ Test: Séquence de touches avancée")
        input_field.setFocus()
        QTest.qWait(50)
        
        # Sélectionner tout le texte (Ctrl+A)
        QTest.keyClick(input_field, Qt.Key_A, Qt.ControlModifier)
        QTest.qWait(50)
        
        # Remplacer par nouveau texte
        new_text = "QTest est génial!"
        QTest.keyClicks(input_field, new_text)
        QTest.qWait(100)
        self.app.processEvents()
        
        assert input_field.text() == new_text
        self.logger.info(f"✅ Texte remplacé: '{input_field.text()}'")
        
        # 4. Nouveau clic pour tester le nouveau texte
        QTest.mouseClick(button, Qt.LeftButton)
        QTest.qWait(100)
        self.app.processEvents()
        
        expected_result = f"Résultat: Vous avez tapé '{new_text}'"
        assert result_label.text() == expected_result
        self.logger.info(f"✅ Nouveau résultat: '{result_label.text()}'")
        
        # Fermer le widget
        QTest.qWait(1000)  # Laisser visible 1 seconde
        widget.close()
        
        self.logger.info("🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
        
        return True
    
    def demo_advantages_over_selenium(self):
        """Démonstration des avantages de QTest par rapport à Selenium"""
        self.logger.info("🎯 AVANTAGES DE QTEST PAR RAPPORT À SELENIUM")
        
        advantages = [
            "✅ QTest est le framework officiel de Qt pour les tests GUI",
            "✅ Accès direct aux objets PyQt5 (pas de sélecteurs CSS/XPath)",
            "✅ Tests plus rapides (pas de communication réseau)",
            "✅ Tests plus fiables (pas de problèmes de timing web)",
            "✅ Intégration native avec PyQt5 (événements, signaux, slots)",
            "✅ Support complet des interactions clavier/souris",
            "✅ Pas besoin de serveur web ou de driver externe",
            "✅ Tests en mode headless avec QT_QPA_PLATFORM=offscreen",
            "✅ Capture d'écran native pour le débogage",
            "✅ Gestion automatique des événements Qt"
        ]
        
        for advantage in advantages:
            self.logger.info(advantage)
        
        self.logger.info("🎉 QTest est la solution parfaite pour PyQt5!")
    
    def run_demo(self):
        """Exécuter la démonstration complète"""
        self.logger.info("🚀 DÉMARRAGE DE LA DÉMONSTRATION QTEST")
        self.logger.info("=" * 60)
        
        try:
            # Démonstration des interactions
            success = self.demo_basic_interactions()
            
            if success:
                self.logger.info("")
                self.demo_advantages_over_selenium()
                
                self.logger.info("")
                self.logger.info("🎉 DÉMONSTRATION COMPLÈTE RÉUSSIE!")
                self.logger.info("✅ QTest remplace parfaitement Selenium pour PyQt5")
                return True
            else:
                self.logger.error("❌ Échec de la démonstration")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erreur durant la démonstration: {e}")
            return False


def main():
    """Point d'entrée principal"""
    print("🎯 Démonstration: QTest remplace Selenium pour PyQt5")
    print("=" * 60)
    
    # Configurer l'environnement pour les tests
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Mode headless
    
    # Créer et exécuter la démonstration
    demo = DemoQTestSolution()
    success = demo.run_demo()
    
    if success:
        print("\n🎉 SUCCÈS: QTest est la solution parfaite pour tester PyQt5!")
        print("📚 Consultez test/behaviour/ pour voir tous les tests implémentés")
        return 0
    else:
        print("\n❌ ÉCHEC: Problème durant la démonstration")
        return 1


if __name__ == "__main__":
    sys.exit(main())
