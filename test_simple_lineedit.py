#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test avec un QLineEdit simple pour comparer
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_simple_lineedit():
    """Test avec un QLineEdit simple"""
    print("📝 TEST AVEC QLINEEDIT SIMPLE")
    print("="*50)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel
        from PyQt6.QtCore import Qt
        
        # Créer l'application PyQt6
        app = QApplication(sys.argv)
        
        # Créer une fenêtre simple
        window = QMainWindow()
        window.setWindowTitle("Test QLineEdit Simple")
        window.resize(400, 200)
        
        # Widget central
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Label
        label = QLabel("Test de saisie - QLineEdit simple :")
        layout.addWidget(label)
        
        # QLineEdit simple
        simple_edit = QLineEdit()
        simple_edit.setPlaceholderText("Tapez ici...")
        simple_edit.setMinimumHeight(35)
        layout.addWidget(simple_edit)
        
        # Label pour notre widget
        label2 = QLabel("Test de saisie - Notre widget d'autocomplétion :")
        layout.addWidget(label2)
        
        # Notre widget d'autocomplétion
        from ui.widgets.client_autocomplete import ClientAutoCompleteWidget
        
        autocomplete_edit = ClientAutoCompleteWidget()
        layout.addWidget(autocomplete_edit)
        
        # Charger quelques clients de test
        test_clients = [
            {"id": 1, "nombre": "Juan Pérez", "nif": "12345678A", "direccion": "Calle Mayor, 1"},
            {"id": 2, "nombre": "María García", "nif": "87654321B", "direccion": "Avenida Principal, 25"},
        ]
        autocomplete_edit.load_clients(test_clients)
        
        # Afficher la fenêtre
        window.show()
        
        print("✅ Fenêtre de test créée")
        print("\n📝 INSTRUCTIONS :")
        print("1. Testez la saisie dans le QLineEdit simple (en haut)")
        print("2. Testez la saisie dans notre widget (en bas)")
        print("3. Comparez le comportement")
        print("4. Fermez la fenêtre quand terminé")
        
        # Donner le focus au premier champ
        simple_edit.setFocus()
        
        # Lancer la boucle d'événements
        result = app.exec()
        
        print("\n✅ Test de comparaison terminé")
        return result == 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_simple_lineedit()
        
        print("\n" + "="*50)
        print("RÉSUMÉ DU TEST DE COMPARAISON")
        print("="*50)
        
        if success:
            print("🎉 TEST DE COMPARAISON TERMINÉ !")
            print("\n🔍 ANALYSE :")
            print("   • Si le QLineEdit simple fonctionne mais pas notre widget,")
            print("     le problème vient de notre implémentation")
            print("   • Si les deux ne fonctionnent pas, le problème est plus général")
            print("   • Si les deux fonctionnent, le problème est dans l'intégration")
            
            return 0
        else:
            print("❌ TEST DE COMPARAISON ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 0
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
