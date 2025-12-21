#!/usr/bin/env python3
"""
Test simple pour vérifier que les boîtes de dialogue ne bloquent plus
"""

import os
import sys
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_window():
    """Test simple d'ouverture et fermeture de fenêtre"""
    
    # Activer le mode test
    os.environ['PYTEST_RUNNING'] = '1'
    
    # Patcher QMessageBox
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from ui.main_window_pyqt5 import MainWindowPyQt5
    
    original_question = QMessageBox.question
    
    def mock_question(*args, **kwargs):
        print("🔄 Dialog intercepté - Réponse automatique: Yes")
        return QMessageBox.Yes
    
    QMessageBox.question = mock_question
    
    try:
        print("🚀 Création de l'application...")
        
        # Créer l'application
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        print("🏠 Création de la fenêtre principale...")
        
        # Créer la fenêtre principale
        main_window = MainWindowPyQt5()
        
        print("👁️ Affichage de la fenêtre...")
        
        # Afficher la fenêtre
        main_window.show()
        
        # Traiter les événements
        app.processEvents()
        
        print("⏱️ Attente 2 secondes...")
        time.sleep(2)
        
        print("🔒 Fermeture de la fenêtre...")
        
        # Fermer la fenêtre (devrait déclencher closeEvent)
        main_window.close()
        
        # Traiter les événements
        app.processEvents()
        
        print("✅ Test terminé avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restaurer l'original
        QMessageBox.question = original_question
        
        # Nettoyer l'environnement
        os.environ.pop('PYTEST_RUNNING', None)

if __name__ == "__main__":
    print("🧪 TEST SIMPLE DE COMPORTEMENT")
    print("=" * 50)
    
    success = test_simple_window()
    
    print("=" * 50)
    if success:
        print("🎉 SUCCÈS: Aucune boîte de dialogue n'a bloqué !")
    else:
        print("💥 ÉCHEC: Le test a échoué")
    
    sys.exit(0 if success else 1)
