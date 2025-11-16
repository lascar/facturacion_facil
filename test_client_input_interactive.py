#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test interactif de l'input client - ouvre une fenêtre pour tester manuellement
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_client_input_interactive():
    """Test interactif de l'input client"""
    print("🖱️ TEST INTERACTIF DE L'INPUT CLIENT")
    print("="*60)
    print("Ce test va ouvrir l'éditeur de factures.")
    print("Vous pourrez tester manuellement la saisie dans le champ client.")
    print("Fermez la fenêtre quand vous avez terminé le test.")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
        
        # Créer l'application PyQt6
        app = QApplication(sys.argv)
        
        print("✅ Application créée")
        
        # Créer l'éditeur de factures
        editor = FacturaEditorPyQt6Window()
        editor.show()
        
        print("✅ Éditeur de factures ouvert")
        print("\n📝 INSTRUCTIONS DE TEST :")
        print("1. Cliquez dans le champ 'Cliente'")
        print("2. Tapez du texte (ex: 'Juan', 'María', 'Nouveau Client')")
        print("3. Vérifiez que les suggestions apparaissent")
        print("4. Testez la sélection d'un client existant")
        print("5. Testez la saisie d'un nouveau client")
        print("6. Fermez la fenêtre quand terminé")
        
        # Vérifier les propriétés du widget client
        if hasattr(editor, 'cliente_autocomplete'):
            client_widget = editor.cliente_autocomplete
            print(f"\n🔍 PROPRIÉTÉS DU WIDGET :")
            print(f"   • ReadOnly: {client_widget.isReadOnly()}")
            print(f"   • Enabled: {client_widget.isEnabled()}")
            print(f"   • Visible: {client_widget.isVisible()}")
            print(f"   • Has Focus: {client_widget.hasFocus()}")
            print(f"   • Focus Policy: {client_widget.focusPolicy()}")
            print(f"   • Placeholder: {client_widget.placeholderText()}")
            
            # Donner le focus au widget
            client_widget.setFocus()
            print(f"   • Focus donné au widget")
        
        # Lancer la boucle d'événements
        result = app.exec()
        
        print("\n✅ Test interactif terminé")
        return result == 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_client_input_interactive()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST INTERACTIF")
        print("="*60)
        
        if success:
            print("🎉 TEST INTERACTIF TERMINÉ !")
            print("\n✨ POINTS À VÉRIFIER :")
            print("   ✅ Le champ client était-il cliquable ?")
            print("   ✅ Pouviez-vous taper du texte ?")
            print("   ✅ Les suggestions apparaissaient-elles ?")
            print("   ✅ La sélection fonctionnait-elle ?")
            print("   ✅ Les nouveaux clients étaient-ils détectés ?")
            
            print("\n🔧 SI PROBLÈME DÉTECTÉ :")
            print("   • Le widget pourrait être masqué par un autre élément")
            print("   • Un gestionnaire d'événements pourrait intercepter la saisie")
            print("   • Le focus pourrait être capturé par un autre widget")
            
            return 0
        else:
            print("❌ TEST INTERACTIF ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 0  # Normal pour un test interactif
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
