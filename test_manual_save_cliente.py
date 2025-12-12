#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manuel pour vérifier qu'il n'y a qu'un seul popup lors de la sauvegarde
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from ui.clientes_pyqt5 import ClientesPyQt5Window
from utils.logger import get_logger

class TestClienteWindow(ClientesPyQt5Window):
    """Version de test qui compte les popups"""
    
    def __init__(self, parent=None):
        self.popup_count = 0
        super().__init__(parent)
        
    def show_info(self, title, message):
        """Override pour compter les popups"""
        self.popup_count += 1
        self.logger.info(f"🔔 Popup #{self.popup_count}: {title} - {message}")
        
        # Afficher le popup normalement
        super().show_info(title, message)

def test_save_popup_count():
    """Test pour compter les popups lors de la sauvegarde"""
    logger = get_logger("TestSavePopup")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de test
        logger.info("🚀 Ouverture de la fenêtre de test...")
        window = TestClienteWindow()
        window.show()
        
        # Remplir le formulaire automatiquement
        logger.info("📝 Remplissage automatique du formulaire...")
        window.nombre_edit.setText("Cliente Test Automatico")
        window.email_edit.setText("test@example.com")
        window.telefono_edit.setText("123456789")
        window.direccion_edit.setPlainText("Dirección de prueba")
        
        # Fonction pour simuler la sauvegarde après un délai
        def simulate_save():
            logger.info("💾 Simulation de la sauvegarde...")
            initial_count = window.popup_count
            
            # Déclencher la sauvegarde
            window.save_cliente()
            
            # Vérifier le nombre de popups
            final_count = window.popup_count
            popup_diff = final_count - initial_count
            
            logger.info(f"📊 Résultat: {popup_diff} popup(s) affiché(s)")
            
            if popup_diff == 1:
                logger.info("✅ SUCCÈS: Un seul popup affiché (correct)")
            elif popup_diff == 2:
                logger.error("❌ ÉCHEC: Deux popups affichés (problème de double connexion)")
            else:
                logger.warning(f"⚠️ INATTENDU: {popup_diff} popups affichés")
            
            # Fermer après 2 secondes
            QTimer.singleShot(2000, app.quit)
        
        # Lancer la simulation après 1 seconde
        QTimer.singleShot(1000, simulate_save)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test de comptage des popups - Sauvegarde Client")
    print("=" * 55)
    print("📋 Ce test va:")
    print("   • Ouvrir la fenêtre de gestion de clients")
    print("   • Remplir automatiquement le formulaire")
    print("   • Simuler une sauvegarde")
    print("   • Compter le nombre de popups affichés")
    print("   • Vérifier qu'il n'y en a qu'un seul")
    print()
    
    exit_code = test_save_popup_count()
    
    print()
    if exit_code == 0:
        print("✅ Test terminé!")
        print("🔍 Vérifiez les logs pour voir le résultat du comptage")
    else:
        print("❌ Test échoué")
    
    sys.exit(exit_code)
