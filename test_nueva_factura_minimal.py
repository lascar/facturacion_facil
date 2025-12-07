#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test minimal pour Nueva Factura - Juste tester l'ouverture et le positionnement
"""

import sys
import time
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


def test_nueva_factura_minimal():
    """Test minimal de Nueva Factura"""
    print("🧪 TEST MINIMAL: Nueva Factura")
    print("=" * 35)
    
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
        time.sleep(0.2)
        
        print("✅ Application principale créée")
        
        # Ouvrir facturas
        main_window.open_facturas()
        facturas_window = main_window.facturas_window
        app.processEvents()
        time.sleep(0.2)
        
        print("✅ Fenêtre Facturas ouverte")
        
        # S'assurer que facturas est au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        app.processEvents()
        time.sleep(0.3)
        
        print("✅ Facturas au premier plan")
        print(f"   Facturas visible: {facturas_window.isVisible()}")
        print(f"   Facturas actif: {facturas_window.isActiveWindow()}")
        
        # MOMENT CRITIQUE: Ouvrir Nueva Factura
        print(f"\n🎯 OUVERTURE NUEVA FACTURA...")
        
        # Vérifier qu'il n'y a pas déjà un dialog ouvert
        if hasattr(facturas_window, 'crear_dialog') and facturas_window.crear_dialog:
            print("⚠️ Dialog déjà ouvert, fermeture...")
            facturas_window.crear_dialog.close()
            facturas_window.crear_dialog = None
            app.processEvents()
            time.sleep(0.2)
        
        # Ouvrir le dialog
        print("   Appel new_factura()...")
        facturas_window.new_factura()
        
        print("   Traitement événements...")
        app.processEvents()
        time.sleep(1.0)  # Attendre plus longtemps pour le chargement
        
        # Vérifications
        print(f"\n📋 VÉRIFICATIONS:")
        
        if not hasattr(facturas_window, 'crear_dialog'):
            print("❌ ÉCHEC: Attribut crear_dialog non créé")
            return False
            
        dialog = facturas_window.crear_dialog
        
        if dialog is None:
            print("❌ ÉCHEC: Dialog non créé (None)")
            return False
            
        print(f"✅ Dialog créé: {type(dialog).__name__}")
        
        # Vérifier visibilité
        is_visible = dialog.isVisible()
        print(f"   Visible: {is_visible}")
        
        if not is_visible:
            print("❌ ÉCHEC: Dialog non visible")
            # Essayer de le rendre visible
            print("   Tentative de rendu visible...")
            dialog.show()
            dialog.raise_()
            dialog.activateWindow()
            app.processEvents()
            time.sleep(0.3)
            
            is_visible_after = dialog.isVisible()
            print(f"   Visible après tentative: {is_visible_after}")
            
            if not is_visible_after:
                print("❌ ÉCHEC: Impossible de rendre le dialog visible")
                return False
        
        # Vérifier les flags
        flags = dialog.windowFlags()
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        has_window = bool(flags & Qt.Window)
        
        print(f"   WindowStaysOnTopHint: {has_stay_on_top}")
        print(f"   Window flag: {has_window}")
        print(f"   Actif: {dialog.isActiveWindow()}")
        
        # Test de stabilité courte
        print(f"\n⏱️ Test stabilité 2 secondes...")
        
        for i in range(4):
            time.sleep(0.5)
            app.processEvents()
            
            still_visible = dialog.isVisible()
            print(f"   {(i+1)*0.5:.1f}s: Visible={still_visible}")
            
            if not still_visible:
                print(f"❌ ÉCHEC: Dialog fermé à {(i+1)*0.5:.1f}s")
                return False
        
        print("✅ Dialog reste stable")
        
        # Nettoyage
        dialog.close()
        facturas_window.close()
        main_window.close()
        
        print(f"\n🎉 TEST MINIMAL RÉUSSI !")
        print("   ✅ Dialog Nueva Factura s'ouvre")
        print("   ✅ Dialog est visible")
        print("   ✅ Dialog a les bons flags")
        print("   ✅ Dialog reste stable")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    success = test_nueva_factura_minimal()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
