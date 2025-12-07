#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que Nueva Factura ne se ferme plus automatiquement
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


def test_nueva_factura_no_auto_close():
    """Test que Nueva Factura ne se ferme pas automatiquement"""
    print("🧪 TEST: Nueva Factura ne se ferme pas automatiquement")
    print("=" * 50)
    
    # Setup
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    try:
        # Créer l'application
        main_window = MainWindowPyQt5()
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        app.processEvents()
        time.sleep(0.5)
        
        print("✅ Application principale créée")
        
        # Ouvrir facturas
        main_window.open_facturas()
        facturas_window = main_window.facturas_window
        
        assert facturas_window is not None, "Fenêtre facturas doit être créée"
        assert facturas_window.isVisible(), "Fenêtre facturas doit être visible"
        
        print("✅ Fenêtre Facturas ouverte")
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        app.processEvents()
        time.sleep(0.5)
        
        dialog = facturas_window.crear_dialog
        assert dialog is not None, "Dialog Nueva Factura doit être créé"
        assert dialog.isVisible(), "Dialog Nueva Factura doit être visible"
        
        print("✅ Dialog Nueva Factura ouvert")
        print(f"   Dialog visible: {dialog.isVisible()}")
        print(f"   Dialog actif: {dialog.isActiveWindow()}")
        
        # Test de stabilité pendant 5 secondes (au-delà du timer de nettoyage)
        print("\n⏱️ Test de stabilité pendant 5 secondes...")
        
        for i in range(10):  # 10 vérifications sur 5 secondes
            time.sleep(0.5)
            app.processEvents()
            
            is_visible = dialog.isVisible()
            print(f"   Seconde {(i+1)*0.5:.1f}: Dialog visible = {is_visible}")
            
            if not is_visible:
                print(f"❌ ÉCHEC: Dialog s'est fermé automatiquement à {(i+1)*0.5:.1f}s")
                return False
        
        print("\n✅ SUCCÈS: Dialog reste ouvert après 5 secondes")
        print("   Le problème de fermeture automatique est résolu !")
        
        # Test d'interaction utilisateur
        print("\n🖱️ Test d'interaction utilisateur...")
        
        # Simuler clic sur le dialog
        dialog.raise_()
        dialog.activateWindow()
        app.processEvents()
        time.sleep(0.2)
        
        assert dialog.isVisible(), "Dialog doit rester visible après interaction"
        print("✅ Dialog reste visible après interaction utilisateur")
        
        # Test de résistance au changement de focus
        print("\n🔄 Test de résistance au changement de focus...")
        
        facturas_window.raise_()
        facturas_window.activateWindow()
        app.processEvents()
        time.sleep(0.5)
        
        assert dialog.isVisible(), "Dialog doit rester visible après changement de focus"
        print("✅ Dialog résiste au changement de focus")
        
        # Nettoyage
        dialog.close()
        facturas_window.close()
        main_window.close()
        
        print(f"\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("   ✅ Dialog ne se ferme plus automatiquement")
        print("   ✅ Dialog reste stable pendant 5+ secondes")
        print("   ✅ Dialog répond aux interactions utilisateur")
        print("   ✅ Dialog résiste aux changements de focus")
        print("   ✅ Problème de fermeture automatique RÉSOLU")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False


def main():
    """Fonction principale"""
    success = test_nueva_factura_no_auto_close()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
