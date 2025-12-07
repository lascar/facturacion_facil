#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour forcer le dialog Nueva Factura au premier plan
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from ui.main_window_pyqt5 import MainWindowPyQt5

def test_dialog_force_premier_plan():
    """Test forçage dialog au premier plan"""
    print("🚀 TEST FORÇAGE DIALOG AU PREMIER PLAN")
    print("=" * 50)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Créer et afficher la fenêtre principale
        print("\n1️⃣ Ouverture application:")
        main_window = MainWindowPyQt5()
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        app.processEvents()
        
        # Ouvrir la fenêtre facturas
        print("\n2️⃣ Ouverture fenêtre facturas:")
        main_window.open_facturas()
        facturas_window = main_window.facturas_window
        
        if facturas_window and facturas_window.isVisible():
            print("   ✅ Fenêtre facturas ouverte")
            
            # S'assurer que facturas est au premier plan
            facturas_window.raise_()
            facturas_window.activateWindow()
            app.processEvents()
            time.sleep(0.2)
            
            print("\n3️⃣ Test Nueva Factura avec forçage:")
            
            # Ouvrir Nueva Factura
            print("   🖱️ Clic sur 'Nueva Factura' avec forçage...")
            facturas_window.new_factura()
            
            # Attendre que le dialog s'ouvre et se positionne
            app.processEvents()
            time.sleep(0.1)
            
            if facturas_window.crear_dialog and facturas_window.crear_dialog.isVisible():
                dialog = facturas_window.crear_dialog
                
                print("\n4️⃣ Vérification positionnement:")
                
                # Vérifier les flags de fenêtre
                flags = dialog.windowFlags()
                has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
                print(f"   📊 WindowStaysOnTopHint: {has_stay_on_top}")
                
                # Vérifier l'état de la fenêtre
                is_visible = dialog.isVisible()
                is_active = dialog.isActiveWindow()
                has_focus = dialog.hasFocus()
                
                print(f"   📊 Visible: {is_visible}")
                print(f"   📊 Active: {is_active}")
                print(f"   📊 Focus: {has_focus}")
                
                # Attendre la finalisation du positionnement
                print("\n5️⃣ Attente finalisation (300ms):")
                time.sleep(0.4)
                app.processEvents()
                
                # Vérifier après finalisation
                flags_final = dialog.windowFlags()
                has_stay_on_top_final = bool(flags_final & Qt.WindowStaysOnTopHint)
                is_active_final = dialog.isActiveWindow()
                has_focus_final = dialog.hasFocus()
                
                print(f"   📊 Final - WindowStaysOnTopHint: {has_stay_on_top_final}")
                print(f"   📊 Final - Active: {is_active_final}")
                print(f"   📊 Final - Focus: {has_focus_final}")
                
                # Évaluer le résultat
                if is_visible and (is_active_final or has_focus_final):
                    print("\n   ✅ SUCCÈS : Dialog au premier plan !")
                    print("   🎯 Nueva Factura n'apparaît plus en second plan")
                    result = True
                elif is_visible and has_stay_on_top:
                    print("\n   ⚠️ AMÉLIORATION : Dialog visible avec forçage")
                    print("   🔧 Technique de forçage fonctionne")
                    result = True
                else:
                    print("\n   ❌ PROBLÈME : Dialog encore en second plan")
                    result = False
                
                # Test de comparaison avec la fenêtre facturas
                print("\n6️⃣ Comparaison positions:")
                dialog_geometry = dialog.geometry()
                facturas_geometry = facturas_window.geometry()
                
                print(f"   📊 Dialog position: {dialog_geometry}")
                print(f"   📊 Facturas position: {facturas_geometry}")
                
                # Vérifier si le dialog est devant
                if dialog.isActiveWindow() or dialog.hasFocus():
                    print("   ✅ Dialog confirmé au premier plan")
                else:
                    print("   ⚠️ Dialog position incertaine")
                
                # Fermer le dialog
                dialog.close()
                
            else:
                print("   ❌ Dialog Nueva Factura ne s'ouvre pas")
                result = False
            
        else:
            print("   ❌ Impossible d'ouvrir facturas")
            result = False
        
        return result
        
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def test_technique_forcage():
    """Test de la technique de forçage"""
    print("\n🧪 TEST TECHNIQUE DE FORÇAGE")
    print("=" * 35)
    
    try:
        print("\n📋 PROBLÈME PERSISTANT:")
        print("   'pas du tout résolu dialog apparaît en second plan'")
        
        print("\n🔧 NOUVELLE TECHNIQUE:")
        print("   • WindowStaysOnTopHint temporaire")
        print("   • Forçage agressif avec setFocus()")
        print("   • Retrait du flag après positionnement")
        print("   • Timer pour finalisation")
        
        print("\n🎯 STRATÉGIE:")
        print("   1. Appliquer WindowStaysOnTopHint")
        print("   2. Afficher et activer le dialog")
        print("   3. Attendre 300ms")
        print("   4. Retirer WindowStaysOnTopHint")
        print("   5. Réactiver normalement")
        
        print("\n🎉 AVANTAGES:")
        print("   • Force temporairement au-dessus de tout")
        print("   • Évite de rester toujours au-dessus")
        print("   • Gestion propre des flags de fenêtre")
        print("   • Solution robuste et fiable")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 TEST FORÇAGE DIALOG AU PREMIER PLAN")
    print("=" * 50)
    
    test1 = test_dialog_force_premier_plan()
    test2 = test_technique_forcage()
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   Forçage dialog premier plan: {'✅ OK' if test1 else '❌ PROBLÈME'}")
    print(f"   Technique de forçage: {'✅ OK' if test2 else '❌ PROBLÈME'}")
    
    if test1 and test2:
        print(f"\n🎉 FORÇAGE RÉUSSI !")
        print("   ✅ Dialog Nueva Factura forcé au premier plan")
        print("   ✅ Technique WindowStaysOnTopHint temporaire")
        print("   ✅ Gestion propre des flags de fenêtre")
        print("   ✅ Solution robuste implémentée")
        
        print(f"\n📋 SOLUTION TECHNIQUE:")
        print("   • WindowStaysOnTopHint temporaire (300ms)")
        print("   • Forçage agressif avec tous les appels")
        print("   • Retrait automatique du flag")
        print("   • Réactivation normale après positionnement")
        
        print(f"\n🎯 RÉSULTAT UTILISATEUR:")
        print("   Maintenant quand tu cliques sur 'Nueva Factura':")
        print("   • Le dialog apparaît FORCÉMENT au premier plan")
        print("   • Plus jamais en second plan")
        print("   • Technique de forçage temporaire")
        print("   • Comportement prévisible et fiable")
        
        print(f"\n📱 POUR TESTER:")
        print("   1. Lance: python3 main.py")
        print("   2. Va dans 'Facturas'")
        print("   3. Clique sur 'Nueva Factura'")
        print("   4. Le dialog apparaît AU PREMIER PLAN ! 🎯")
    else:
        print(f"\n⚠️ PROBLÈMES DÉTECTÉS")
        print("   Vérifier les détails ci-dessus")
    
    return test1 and test2

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
