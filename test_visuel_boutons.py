#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test visuel des boutons +/- pour vérification manuelle
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_visuel_boutons():
    """Test visuel des boutons +/-"""
    print("👁️ TEST VISUEL DES BOUTONS +/-")
    print("="*40)
    print("Ce test ouvre la fenêtre de stock pour vérification visuelle.")
    print("Vérifiez que les boutons affichent bien '+' et '-'")
    print("Appuyez sur Ctrl+C pour fermer quand vous avez vérifié.")
    print()
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.stock_pyqt6 import StockPyQt6Window
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Créer la fenêtre de stock
        print("🔄 Ouverture de la fenêtre de stock...")
        
        stock_window = StockPyQt6Window()
        stock_window.show()
        
        print("✅ Fenêtre de stock ouverte")
        print()
        print("👁️ VÉRIFICATION VISUELLE :")
        print("   1. Regardez les boutons dans la colonne 'Acciones'")
        print("   2. Vérifiez que le bouton rouge affiche '-'")
        print("   3. Vérifiez que le bouton vert affiche '+'")
        print("   4. Testez les clics pour voir s'ils fonctionnent")
        print("   5. Appuyez sur Ctrl+C quand c'est bon")
        print()
        
        # Traiter les événements et attendre
        try:
            while True:
                app.processEvents()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n✅ Test visuel terminé par l'utilisateur")
        
        # Fermer la fenêtre
        stock_window.close()
        print("✅ Fenêtre fermée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_visuel_boutons()
        
        print("\n" + "="*40)
        print("RÉSUMÉ DU TEST VISUEL")
        print("="*40)
        
        if success:
            print("🎉 TEST VISUEL TERMINÉ !")
            print("\n✨ POINTS À VÉRIFIER :")
            print("   ✅ Boutons visibles dans la colonne 'Acciones'")
            print("   ✅ Bouton rouge avec symbole '-'")
            print("   ✅ Bouton vert avec symbole '+'")
            print("   ✅ Taille appropriée (30x30px)")
            print("   ✅ Bordures arrondies")
            print("   ✅ Clics fonctionnels")
            
            print("\n🎯 SI LES SYMBOLES NE SONT PAS VISIBLES :")
            print("   • Problème de police ou d'encodage")
            print("   • Essayer une police différente")
            print("   • Vérifier les paramètres système")
            
            print("\n🚀 UTILISATION NORMALE :")
            print("   python main.py → Stock")
            print("   Cliquez sur les boutons +/- pour tester")
            
            return 0
        else:
            print("❌ TEST VISUEL ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu")
        return 0
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
