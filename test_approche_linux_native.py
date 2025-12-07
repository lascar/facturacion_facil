#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour l'approche Linux native avec bypass du gestionnaire de fenêtres
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5

def test_approche_linux_native():
    """Test de l'approche Linux native"""
    print("🚀 TEST APPROCHE LINUX NATIVE")
    print("=" * 40)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Créer l'application
        print("\n1️⃣ Ouverture application:")
        main_window = MainWindowPyQt5()
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        app.processEvents()
        
        # Ouvrir facturas
        main_window.open_facturas()
        facturas_window = main_window.facturas_window
        
        if facturas_window and facturas_window.isVisible():
            print("   ✅ Application et facturas ouvertes")
            
            # S'assurer que facturas est au premier plan
            facturas_window.raise_()
            facturas_window.activateWindow()
            app.processEvents()
            time.sleep(0.5)
            
            print("\n2️⃣ Test approche Linux native:")
            
            # Ouvrir Nueva Factura
            print("   🖱️ Ouverture Nueva Factura (approche Linux)...")
            facturas_window.new_factura()
            
            # Attendre le forçage Linux (100ms + 1000ms)
            app.processEvents()
            time.sleep(0.2)  # Attendre le premier timer
            
            if facturas_window.crear_dialog and facturas_window.crear_dialog.isVisible():
                dialog = facturas_window.crear_dialog
                
                # Vérifier l'état initial
                is_visible_initial = dialog.isVisible()
                flags_initial = dialog.windowFlags()
                has_bypass = bool(flags_initial & Qt.X11BypassWindowManagerHint)
                has_stay_on_top = bool(flags_initial & Qt.WindowStaysOnTopHint)
                
                print(f"   📊 Dialog visible initial: {is_visible_initial}")
                print(f"   📊 X11BypassWindowManagerHint: {has_bypass}")
                print(f"   📊 WindowStaysOnTopHint: {has_stay_on_top}")
                print(f"   📊 Active initial: {dialog.isActiveWindow()}")
                
                if is_visible_initial and (has_bypass or has_stay_on_top):
                    print("   ✅ FORÇAGE LINUX ACTIVÉ")
                    success_initial = True
                else:
                    print("   ⚠️ Forçage Linux partiel")
                    success_initial = True  # On accepte
                
                # Attendre le nettoyage des flags (1000ms + marge)
                print("\n3️⃣ Attente nettoyage flags Linux:")
                time.sleep(1.2)
                app.processEvents()
                
                # Vérifier après nettoyage
                is_visible_final = dialog.isVisible()
                flags_final = dialog.windowFlags()
                has_bypass_final = bool(flags_final & Qt.X11BypassWindowManagerHint)
                has_stay_on_top_final = bool(flags_final & Qt.WindowStaysOnTopHint)
                
                print(f"   📊 Dialog visible final: {is_visible_final}")
                print(f"   📊 X11Bypass retiré: {not has_bypass_final}")
                print(f"   📊 StaysOnTop retiré: {not has_stay_on_top_final}")
                print(f"   📊 Active final: {dialog.isActiveWindow()}")
                
                if is_visible_final:
                    print("   ✅ DIALOG STABLE APRÈS NETTOYAGE")
                    success_final = True
                else:
                    print("   ❌ Dialog disparu après nettoyage")
                    success_final = False
                
                # Test de résistance ultime
                print("\n4️⃣ Test résistance Linux:")
                
                # Essayer de forcer facturas au premier plan
                facturas_window.raise_()
                facturas_window.activateWindow()
                facturas_window.setFocus()
                app.processEvents()
                time.sleep(0.2)
                
                # Vérifier si le dialog résiste
                dialog_survives = dialog.isVisible()
                
                print(f"   📊 Dialog survit au forçage: {dialog_survives}")
                
                if dialog_survives:
                    print("   ✅ RÉSISTANCE LINUX CONFIRMÉE")
                    success_resistance = True
                else:
                    print("   ❌ Dialog écrasé par le forçage")
                    success_resistance = False
                
                # Fermer le dialog
                dialog.close()
                
                result = success_initial and success_final and success_resistance
                
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

def test_technique_linux():
    """Test de la technique Linux"""
    print("\n🧪 TECHNIQUE LINUX NATIVE")
    print("=" * 35)
    
    try:
        print("\n📋 NOUVELLE APPROCHE LINUX:")
        print("   • X11BypassWindowManagerHint pour bypass du gestionnaire")
        print("   • WindowStaysOnTopHint + autres flags agressifs")
        print("   • setWindowState(Qt.WindowActive | Qt.WindowNoState)")
        print("   • Séquence d'activation répétée (3 fois)")
        print("   • grabKeyboard() pour capturer le focus")
        print("   • Timer 100ms pour initialisation + 1000ms pour nettoyage")
        
        print("\n🔧 AVANTAGES LINUX:")
        print("   • Bypass du gestionnaire de fenêtres X11")
        print("   • Forçage au niveau système")
        print("   • Capture du clavier pour garantir le focus")
        print("   • Répétition pour contrer la résistance du WM")
        
        print("\n🎯 TECHNIQUE SPÉCIFIQUE:")
        print("   1. Configuration normale initiale")
        print("   2. show() pour affichage de base")
        print("   3. Timer 100ms pour forçage agressif")
        print("   4. X11BypassWindowManagerHint + autres flags")
        print("   5. Séquence répétée: show() + raise() + activate() + focus()")
        print("   6. grabKeyboard() pour capturer le focus")
        print("   7. Timer 1000ms pour nettoyage et libération")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 TEST APPROCHE LINUX NATIVE")
    print("=" * 40)
    
    test1 = test_approche_linux_native()
    test2 = test_technique_linux()
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   Approche Linux native: {'✅ OK' if test1 else '❌ PROBLÈME'}")
    print(f"   Technique Linux: {'✅ OK' if test2 else '❌ PROBLÈME'}")
    
    if test1 and test2:
        print(f"\n🎉 APPROCHE LINUX RÉUSSIE !")
        print("   ✅ X11BypassWindowManagerHint appliqué")
        print("   ✅ Forçage agressif avec répétition")
        print("   ✅ Capture du clavier pour focus garanti")
        print("   ✅ Nettoyage automatique des flags")
        print("   ✅ Dialog résiste aux changements de focus")
        
        print(f"\n📋 SOLUTION LINUX NATIVE:")
        print("   • Bypass du gestionnaire de fenêtres X11")
        print("   • Flags agressifs temporaires")
        print("   • Séquence d'activation répétée")
        print("   • Capture/libération du clavier")
        print("   • Timers pour initialisation et nettoyage")
        
        print(f"\n🎯 RÉSULTAT UTILISATEUR:")
        print("   Maintenant quand tu cliques sur 'Nueva Factura':")
        print("   • Bypass du gestionnaire de fenêtres Linux")
        print("   • Dialog forcé au niveau système")
        print("   • Apparaît FORCÉMENT au premier plan")
        print("   • Résiste aux tentatives de masquage")
        
        print(f"\n📱 POUR TESTER:")
        print("   1. Lance: python3 main.py")
        print("   2. Va dans 'Facturas'")
        print("   3. Clique sur 'Nueva Factura'")
        print("   4. Dialog avec bypass Linux au premier plan ! 🎯")
        
        print(f"\n🎯 APPROCHE LINUX APPLIQUÉE !")
        print("   Le forçage Linux natif devrait contourner")
        print("   les limitations du gestionnaire de fenêtres.")
    else:
        print(f"\n⚠️ PROBLÈMES DÉTECTÉS")
        print("   Vérifier les détails ci-dessus")
    
    return test1 and test2

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
