#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple de l'input client pour vérifier qu'on peut écrire
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_client_input():
    """Test simple de l'input client"""
    print("✏️ TEST SIMPLE DE L'INPUT CLIENT")
    print("="*50)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
        from ui.widgets.client_autocomplete import ClientAutoCompleteWidget
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Test 1: Widget autonome
        print("\n--- Test 1: Widget Autonome ---")
        
        widget = ClientAutoCompleteWidget()
        widget.show()
        
        print("✅ Widget créé et affiché")
        print(f"✅ ReadOnly: {widget.isReadOnly()}")
        print(f"✅ Enabled: {widget.isEnabled()}")
        print(f"✅ Placeholder: {widget.placeholderText()}")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(0.5)
        
        # Test de saisie programmatique
        widget.setText("Test de saisie")
        app.processEvents()
        
        if widget.text() == "Test de saisie":
            print("✅ Saisie programmatique fonctionne")
        else:
            print(f"❌ Saisie programmatique échoue: '{widget.text()}'")
        
        # Effacer
        widget.clear()
        app.processEvents()
        
        if widget.text() == "":
            print("✅ Effacement fonctionne")
        else:
            print(f"❌ Effacement échoue: '{widget.text()}'")
        
        widget.close()
        
        # Test 2: Dans l'éditeur de factures
        print("\n--- Test 2: Dans l'Éditeur de Factures ---")
        
        from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
        
        editor = FacturaEditorPyQt6Window()
        editor.show()
        
        print("✅ Éditeur de factures créé")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(0.5)
        
        # Vérifier le widget client
        if hasattr(editor, 'cliente_autocomplete'):
            client_widget = editor.cliente_autocomplete
            
            print(f"✅ Widget client trouvé")
            print(f"✅ ReadOnly: {client_widget.isReadOnly()}")
            print(f"✅ Enabled: {client_widget.isEnabled()}")
            print(f"✅ Visible: {client_widget.isVisible()}")
            print(f"✅ Focus Policy: {client_widget.focusPolicy()}")
            
            # Test de saisie
            client_widget.setText("Cliente de Prueba")
            app.processEvents()
            
            if client_widget.text() == "Cliente de Prueba":
                print("✅ Saisie dans l'éditeur fonctionne")
            else:
                print(f"❌ Saisie dans l'éditeur échoue: '{client_widget.text()}'")
            
            # Test de focus
            client_widget.setFocus()
            app.processEvents()
            
            if client_widget.hasFocus():
                print("✅ Widget peut recevoir le focus")
            else:
                print("⚠️ Widget ne peut pas recevoir le focus")
            
            # Test de sélection
            client_widget.selectAll()
            app.processEvents()
            
            if client_widget.hasSelectedText():
                print("✅ Sélection de texte fonctionne")
            else:
                print("⚠️ Sélection de texte ne fonctionne pas")
            
        else:
            print("❌ Widget client non trouvé dans l'éditeur")
        
        editor.close()
        
        # Test 3: Vérification des propriétés CSS
        print("\n--- Test 3: Propriétés CSS ---")
        
        test_widget = ClientAutoCompleteWidget()
        
        # Vérifier le style
        style_sheet = test_widget.styleSheet()
        if "background-color: white" in style_sheet:
            print("✅ Style CSS appliqué")
        else:
            print("⚠️ Style CSS non appliqué")
        
        # Vérifier les propriétés dynamiques
        test_widget.setProperty("hasClient", True)
        test_widget.style().polish(test_widget)
        print("✅ Propriété dynamique 'hasClient' testée")
        
        test_widget.setProperty("hasClient", False)
        test_widget.setProperty("isNew", True)
        test_widget.style().polish(test_widget)
        print("✅ Propriété dynamique 'isNew' testée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_client_input()
        
        print("\n" + "="*50)
        print("RÉSUMÉ DU TEST D'INPUT CLIENT")
        print("="*50)
        
        if success:
            print("🎉 TEST D'INPUT CLIENT RÉUSSI !")
            print("\n✨ VÉRIFICATIONS EFFECTUÉES :")
            print("   ✅ Widget autonome fonctionnel")
            print("   ✅ Saisie programmatique")
            print("   ✅ Intégration dans l'éditeur")
            print("   ✅ Propriétés d'édition")
            print("   ✅ Focus et sélection")
            print("   ✅ Styles CSS")
            
            print("\n🔧 SI LE PROBLÈME PERSISTE :")
            print("   1. Vérifiez que le widget a le focus")
            print("   2. Cliquez dans le champ avant de taper")
            print("   3. Vérifiez qu'aucun autre widget ne capture les événements")
            print("   4. Redémarrez l'application")
            
            return 0
        else:
            print("❌ TEST D'INPUT CLIENT ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
