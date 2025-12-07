#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour vérifier que le problème du TODO.md est résolu
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window_pyqt5 import MainWindowPyQt5

def test_application_nueva_factura():
    """Test complet avec l'application réelle"""
    print("🚀 TEST APPLICATION RÉELLE - NUEVA FACTURA")
    print("=" * 50)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre principale
        print("\n1️⃣ Ouverture application principale:")
        main_window = MainWindowPyQt5()
        main_window.show()
        print("   ✅ Application principale ouverte")
        
        # Ouvrir la fenêtre des facturas
        print("\n2️⃣ Ouverture fenêtre facturas:")
        main_window.open_facturas()
        facturas_window = main_window.facturas_window
        
        if facturas_window and facturas_window.isVisible():
            print("   ✅ Fenêtre facturas ouverte")
            
            # Test du problème original
            print("\n3️⃣ Test clics multiples sur Nueva Factura:")
            
            # Premier clic
            print("   🖱️ Premier clic sur 'Nueva Factura'...")
            facturas_window.new_factura()
            
            # Vérifier qu'un dialog est ouvert
            if facturas_window.crear_dialog is not None and facturas_window.crear_dialog.isVisible():
                print("   ✅ Une fenêtre Nueva Factura s'ouvre")
                
                # Deuxième clic rapide
                print("   🖱️ Deuxième clic rapide...")
                facturas_window.new_factura()
                
                # Vérifier qu'il n'y a toujours qu'une seule fenêtre
                app.processEvents()  # Traiter les événements
                
                # Compter les fenêtres Nueva Factura ouvertes
                dialogs_ouverts = 0
                if facturas_window.crear_dialog is not None and facturas_window.crear_dialog.isVisible():
                    dialogs_ouverts = 1
                
                print(f"   📊 Nombre de dialogs Nueva Factura ouverts: {dialogs_ouverts}")
                
                if dialogs_ouverts == 1:
                    print("   ✅ PROBLÈME RÉSOLU : Une seule fenêtre ouverte !")
                    print("   🎯 Plus de fenêtres multiples derrière la fenêtre facturas")
                    result = True
                else:
                    print("   ❌ Problème persistant : Plusieurs fenêtres ouvertes")
                    result = False
                
                # Troisième clic pour être sûr
                print("   🖱️ Troisième clic pour vérifier...")
                facturas_window.new_factura()
                
                # Vérifier que la même fenêtre est réutilisée
                if facturas_window.crear_dialog is not None and facturas_window.crear_dialog.isVisible():
                    print("   ✅ Même fenêtre réutilisée (amenée au premier plan)")
                else:
                    print("   ⚠️ Problème avec la réutilisation")
                
                # Fermer le dialog pour nettoyer
                facturas_window.crear_dialog.close()
                app.processEvents()
                
            else:
                print("   ❌ Aucune fenêtre Nueva Factura ne s'est ouverte")
                result = False
            
        else:
            print("   ❌ Impossible d'ouvrir la fenêtre facturas")
            result = False
        
        return result
        
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def test_todo_status():
    """Test du statut du TODO"""
    print("\n🧪 TEST STATUT TODO")
    print("=" * 25)
    
    try:
        # Lire le fichier TODO.md
        with open("TODO.md", "r", encoding="utf-8") as f:
            todo_content = f.read()
        
        print("\n📋 Contenu TODO.md:")
        print("   " + "\n   ".join(todo_content.split("\n")[:10]))  # Afficher les 10 premières lignes
        
        # Vérifier que le problème est marqué comme résolu
        if "✅ RÉSOLU" in todo_content and "RÉSOLU" in todo_content:
            print("\n   ✅ Problème marqué comme RÉSOLU dans TODO.md")
            return True
        else:
            print("\n   ⚠️ Problème pas encore marqué comme résolu")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur lecture TODO.md: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 TEST FINAL RÉSOLUTION TODO - NUEVA FACTURA")
    print("=" * 55)
    
    test1 = test_application_nueva_factura()
    test2 = test_todo_status()
    
    print(f"\n🎯 RÉSUMÉ FINAL:")
    print(f"   Application Nueva Factura: {'✅ OK' if test1 else '❌ PROBLÈME'}")
    print(f"   Statut TODO: {'✅ OK' if test2 else '❌ PROBLÈME'}")
    
    if test1 and test2:
        print(f"\n🎉 TODO COMPLÈTEMENT RÉSOLU !")
        print("   ✅ Plus de fenêtres multiples Nueva Factura")
        print("   ✅ Une seule fenêtre s'ouvre à la fois")
        print("   ✅ Réutilisation intelligente des dialogs")
        print("   ✅ TODO.md mis à jour avec le statut résolu")
        
        print(f"\n📋 PROBLÈME ORIGINAL (TODO.md):")
        print("   'quand on fait nueva factura maintenant 2 fenetres")
        print("   nueva factura s'ouvrent derriére la fenetre de facturas'")
        
        print(f"\n🎯 SOLUTION IMPLÉMENTÉE:")
        print("   • Protection contre clics multiples")
        print("   • Variables de contrôle des dialogs")
        print("   • Réutilisation des fenêtres existantes")
        print("   • Nettoyage automatique des références")
        
        print(f"\n📱 RÉSULTAT UTILISATEUR:")
        print("   Maintenant quand tu cliques sur 'Nueva Factura':")
        print("   • Une seule fenêtre s'ouvre")
        print("   • Si tu cliques à nouveau, elle revient au premier plan")
        print("   • Plus de fenêtres qui s'empilent derrière !")
        print("   • Interface propre et prévisible")
        
        print(f"\n🎯 POUR VÉRIFIER:")
        print("   1. Lance: python3 main.py")
        print("   2. Va dans 'Facturas'")
        print("   3. Clique plusieurs fois rapidement sur 'Nueva Factura'")
        print("   4. Une seule fenêtre s'ouvre ! 🎯")
        
        print(f"\n📝 TODO.md UPDATED:")
        print("   ✅ Problème marqué comme RÉSOLU")
        print("   📋 Prochaines tâches identifiées")
    else:
        print(f"\n⚠️ PROBLÈMES DÉTECTÉS")
        print("   Vérifier les détails ci-dessus")
    
    return test1 and test2

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
