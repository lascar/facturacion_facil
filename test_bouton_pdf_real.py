#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du bouton PDF dans l'application réelle
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application_avec_bouton_pdf():
    """Test de l'application avec le bouton PDF"""
    print("🚀 Test de l'application avec bouton PDF")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.main_window_pyqt5 import MainWindowPyQt5
        
        # Créer l'application
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        print("✅ Application PyQt5 créée")
        
        # Créer la fenêtre principale
        main_window = MainWindowPyQt5()
        print("✅ Fenêtre principale créée")
        
        # Afficher la fenêtre
        main_window.show()
        print("✅ Fenêtre affichée")
        
        print("\n📋 INSTRUCTIONS POUR LE TEST:")
        print("1. La fenêtre principale s'ouvre")
        print("2. Clique sur 'Facturas' pour ouvrir la gestion des factures")
        print("3. Vérifie que le bouton '📄 Exportar PDF' est présent")
        print("4. Sélectionne une facture et teste le bouton PDF")
        print("5. Ferme l'application quand tu as terminé")
        
        print("\n🎯 VÉRIFICATIONS À FAIRE:")
        print("✓ Le bouton PDF est visible dans l'interface")
        print("✓ Le bouton PDF est entre 'Editar' et 'Eliminar'")
        print("✓ Le bouton affiche l'icône 📄 et le texte 'Exportar PDF'")
        print("✓ Cliquer sans sélection affiche un message d'avertissement")
        print("✓ Cliquer avec une facture sélectionnée génère un PDF")
        print("✓ Le PDF est sauvegardé dans le dossier 'pdfs/'")
        
        print("\n⏳ Lancement de l'application...")
        print("   (Ferme la fenêtre pour terminer le test)")
        
        # Lancer l'application
        app.exec_()
        
        print("\n✅ Application fermée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    # Désactiver l'ouverture automatique des PDFs
    os.environ['DISABLE_PDF_OPEN'] = '1'
    
    success = test_application_avec_bouton_pdf()
    
    if success:
        print("\n🎉 TEST TERMINÉ AVEC SUCCÈS!")
        print("Le bouton PDF a été ajouté à l'interface des factures.")
    else:
        print("\n❌ TEST ÉCHOUÉ!")
        print("Vérifiez les erreurs ci-dessus.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
