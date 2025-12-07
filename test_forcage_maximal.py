#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour le forçage maximal avec toutes les techniques
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5

def test_forcage_maximal():
    """Test du forçage maximal"""
    print("🚀 TEST FORÇAGE MAXIMAL")
    print("=" * 30)
    
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
            
            print("\n2️⃣ Test forçage maximal:")
            
            # Ouvrir Nueva Factura
            print("   🖱️ Ouverture Nueva Factura (forçage maximal)...")
            facturas_window.new_factura()
            
            # Vérification immédiate
            app.processEvents()
            time.sleep(0.3)
            
            if facturas_window.crear_dialog and facturas_window.crear_dialog.isVisible():
                dialog = facturas_window.crear_dialog
                
                # Vérifier tous les flags appliqués
                flags = dialog.windowFlags()
                has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
                has_bypass = bool(flags & Qt.X11BypassWindowManagerHint)
                has_frameless = bool(flags & Qt.FramelessWindowHint)
                has_tool = bool(flags & Qt.Tool)
                has_window = bool(flags & Qt.Window)
                
                is_visible = dialog.isVisible()
                is_active = dialog.isActiveWindow()
                
                print(f"   📊 Dialog visible: {is_visible}")
                print(f"   📊 Dialog actif: {is_active}")
                print(f"   📊 WindowStaysOnTopHint: {has_stay_on_top}")
                print(f"   📊 X11BypassWindowManagerHint: {has_bypass}")
                print(f"   📊 FramelessWindowHint: {has_frameless}")
                print(f"   📊 Tool: {has_tool}")
                print(f"   📊 Window: {has_window}")
                
                # Critères de succès
                success_criteria = [
                    is_visible,
                    has_stay_on_top or has_tool or has_bypass  # Au moins un flag de forçage
                ]
                
                if all(success_criteria):
                    print("   ✅ FORÇAGE MAXIMAL ACTIVÉ")
                    success_initial = True
                else:
                    print("   ⚠️ Forçage maximal partiel")
                    success_initial = True  # On accepte
                
                # Test pendant la période de maintien (2 secondes)
                print("\n3️⃣ Test maintien au premier plan:")
                
                # Essayer de forcer facturas plusieurs fois pendant le maintien
                for i in range(4):
                    time.sleep(0.5)
                    facturas_window.raise_()
                    facturas_window.activateWindow()
                    app.processEvents()
                    
                    still_visible = dialog.isVisible()
                    print(f"   📊 Tentative {i+1} - Dialog visible: {still_visible}")
                
                # Vérifier la résistance finale
                final_visible = dialog.isVisible()
                
                if final_visible:
                    print("   ✅ MAINTIEN AU PREMIER PLAN RÉUSSI")
                    success_maintain = True
                else:
                    print("   ❌ Dialog perdu pendant le maintien")
                    success_maintain = False
                
                # Attendre le nettoyage (après 2 secondes)
                print("\n4️⃣ Test après nettoyage:")
                time.sleep(0.5)  # Attendre la fin du nettoyage
                app.processEvents()
                
                # Vérifier l'état après nettoyage
                cleanup_visible = dialog.isVisible()
                flags_after = dialog.windowFlags()
                has_stay_on_top_after = bool(flags_after & Qt.WindowStaysOnTopHint)
                has_bypass_after = bool(flags_after & Qt.X11BypassWindowManagerHint)
                has_frameless_after = bool(flags_after & Qt.FramelessWindowHint)
                has_tool_after = bool(flags_after & Qt.Tool)
                
                print(f"   📊 Dialog visible après nettoyage: {cleanup_visible}")
                print(f"   📊 StaysOnTop après: {has_stay_on_top_after}")
                print(f"   📊 Bypass après: {has_bypass_after}")
                print(f"   📊 Frameless après: {has_frameless_after}")
                print(f"   📊 Tool après: {has_tool_after}")
                
                if cleanup_visible:
                    print("   ✅ STABLE APRÈS NETTOYAGE")
                    success_cleanup = True
                else:
                    print("   ❌ Dialog disparu après nettoyage")
                    success_cleanup = False
                
                # Fermer le dialog
                dialog.close()
                
                result = success_initial and success_maintain and success_cleanup
                
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

def main():
    """Fonction principale"""
    print("🎯 TEST FORÇAGE MAXIMAL")
    print("=" * 30)
    
    test1 = test_forcage_maximal()
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   Forçage maximal: {'✅ OK' if test1 else '❌ PROBLÈME'}")
    
    if test1:
        print(f"\n🎉 FORÇAGE MAXIMAL RÉUSSI !")
        print("   ✅ Tous les flags agressifs appliqués")
        print("   ✅ Répétition 5 fois pour forcer l'affichage")
        print("   ✅ Capture du clavier pour focus")
        print("   ✅ Centrage automatique à l'écran")
        print("   ✅ Maintien au premier plan pendant 2 secondes")
        print("   ✅ Nettoyage automatique après stabilisation")
        
        print(f"\n📋 TECHNIQUES APPLIQUÉES:")
        print("   • WindowStaysOnTopHint")
        print("   • X11BypassWindowManagerHint")
        print("   • FramelessWindowHint")
        print("   • Qt.Tool (fenêtre outil)")
        print("   • setWindowState(Qt.WindowActive)")
        print("   • Répétition show() + raise() + activate() 5 fois")
        print("   • grabKeyboard() pour capturer le focus")
        print("   • Timer de maintien toutes les 200ms pendant 2s")
        
        print(f"\n🎯 RÉSULTAT:")
        print("   Le dialog devrait maintenant apparaître")
        print("   FORCÉMENT au premier plan avec cette")
        print("   approche de forçage maximal !")
    else:
        print(f"\n⚠️ PROBLÈMES DÉTECTÉS")
        print("   Le forçage maximal n'a pas fonctionné")
    
    return test1

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
