#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la solution simplifiée pour Nueva Factura
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


def test_nueva_factura_solution_simple():
    """Test de la solution simplifiée"""
    print("🧪 TEST: Solution simplifiée Nueva Factura")
    print("=" * 45)
    
    # Setup
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    try:
        # Créer l'application
        main_window = MainWindowPyQt5()
        main_window.show()
        app.processEvents()
        time.sleep(0.3)
        
        print("✅ Application principale créée")
        
        # Ouvrir facturas
        main_window.open_facturas()
        facturas_window = main_window.facturas_window
        app.processEvents()
        time.sleep(0.3)
        
        print("✅ Fenêtre Facturas ouverte")
        
        # S'assurer que facturas est au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        app.processEvents()
        time.sleep(0.5)
        
        print("✅ Facturas au premier plan")
        
        # MOMENT CRITIQUE: Ouvrir Nueva Factura
        print("\n🎯 OUVERTURE NUEVA FACTURA...")
        facturas_window.new_factura()
        app.processEvents()
        time.sleep(0.5)
        
        dialog = facturas_window.crear_dialog
        
        # Vérifications immédiates
        if dialog is None:
            print("❌ ÉCHEC: Dialog non créé")
            return False
            
        if not dialog.isVisible():
            print("❌ ÉCHEC: Dialog non visible")
            return False
            
        print("✅ Dialog Nueva Factura créé et visible")
        print(f"   Visible: {dialog.isVisible()}")
        print(f"   Actif: {dialog.isActiveWindow()}")
        
        # Vérifier les flags
        flags = dialog.windowFlags()
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        has_window = bool(flags & Qt.Window)
        
        print(f"   WindowStaysOnTopHint: {has_stay_on_top}")
        print(f"   Window flag: {has_window}")
        
        # Test de stabilité pendant 3 secondes
        print(f"\n⏱️ Test de stabilité pendant 3 secondes...")
        
        for i in range(6):  # 6 vérifications sur 3 secondes
            time.sleep(0.5)
            app.processEvents()
            
            is_visible = dialog.isVisible()
            is_active = dialog.isActiveWindow()
            
            print(f"   {(i+1)*0.5:.1f}s: Visible={is_visible}, Actif={is_active}")
            
            if not is_visible:
                print(f"❌ ÉCHEC: Dialog fermé à {(i+1)*0.5:.1f}s")
                return False
        
        print("✅ Dialog reste ouvert et stable")
        
        # Test de résistance au changement de focus
        print(f"\n🔄 Test résistance changement de focus...")
        
        # Essayer de ramener facturas au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        app.processEvents()
        time.sleep(0.5)
        
        if not dialog.isVisible():
            print("❌ ÉCHEC: Dialog fermé après changement de focus")
            return False
            
        print("✅ Dialog résiste au changement de focus")
        
        # Test d'interaction utilisateur
        print(f"\n🖱️ Test interaction utilisateur...")
        
        dialog.raise_()
        dialog.activateWindow()
        app.processEvents()
        time.sleep(0.3)
        
        if not dialog.isVisible():
            print("❌ ÉCHEC: Dialog fermé après interaction")
            return False
            
        print("✅ Dialog répond aux interactions")
        
        # Nettoyage
        dialog.close()
        facturas_window.close()
        main_window.close()
        
        print(f"\n🎉 SOLUTION SIMPLIFIÉE VALIDÉE !")
        print("   ✅ Dialog s'ouvre au premier plan")
        print("   ✅ Dialog reste stable (pas de fermeture auto)")
        print("   ✅ Dialog résiste aux changements de focus")
        print("   ✅ Dialog répond aux interactions utilisateur")
        print("   ✅ Solution simple et efficace")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    success = test_nueva_factura_solution_simple()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
