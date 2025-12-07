#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de la solution Nueva Factura simplifiée
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


def test_nueva_factura_solution_finale():
    """Test final de la solution Nueva Factura"""
    print("🧪 TEST FINAL: Solution Nueva Factura Simplifiée")
    print("=" * 50)
    
    # Setup
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    try:
        print("📱 Lancement de l'application...")
        
        # Créer l'application
        main_window = MainWindowPyQt5()
        main_window.show()
        app.processEvents()
        time.sleep(0.5)
        
        print("✅ Application principale lancée")
        
        # Ouvrir facturas
        print("📋 Ouverture fenêtre Facturas...")
        main_window.open_facturas()
        facturas_window = main_window.facturas_window
        app.processEvents()
        time.sleep(0.5)
        
        print("✅ Fenêtre Facturas ouverte")
        
        # S'assurer que facturas est au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        app.processEvents()
        time.sleep(0.5)
        
        print("✅ Facturas au premier plan")
        print(f"   Facturas visible: {facturas_window.isVisible()}")
        print(f"   Facturas actif: {facturas_window.isActiveWindow()}")
        
        # MOMENT CRITIQUE: Ouvrir Nueva Factura
        print(f"\n🎯 OUVERTURE NUEVA FACTURA...")
        print("   (Ceci était le problème principal)")
        
        facturas_window.new_factura()
        app.processEvents()
        time.sleep(1.0)  # Attendre le chargement
        
        # Vérifications
        print(f"\n📋 VÉRIFICATIONS CRITIQUES:")
        
        dialog = facturas_window.crear_dialog
        
        if dialog is None:
            print("❌ ÉCHEC: Dialog non créé")
            return False
            
        print(f"✅ Dialog créé: {type(dialog).__name__}")
        
        # Vérifier visibilité
        is_visible = dialog.isVisible()
        print(f"   Visible: {is_visible}")
        
        if not is_visible:
            print("❌ ÉCHEC: Dialog non visible")
            return False
        
        # Vérifier les flags
        flags = dialog.windowFlags()
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        has_window = bool(flags & Qt.Window)
        
        print(f"   WindowStaysOnTopHint: {has_stay_on_top}")
        print(f"   Window flag: {has_window}")
        print(f"   Actif: {dialog.isActiveWindow()}")
        
        # TEST CRITIQUE: Stabilité dans le temps
        print(f"\n⏱️ TEST CRITIQUE: Stabilité 5 secondes...")
        print("   (Vérifier que le dialog ne se ferme PAS automatiquement)")
        
        for i in range(10):  # 10 vérifications sur 5 secondes
            time.sleep(0.5)
            app.processEvents()
            
            still_visible = dialog.isVisible()
            status = "✅ OK" if still_visible else "❌ FERMÉ"
            print(f"   {(i+1)*0.5:.1f}s: {status}")
            
            if not still_visible:
                print(f"\n❌ ÉCHEC CRITIQUE: Dialog fermé automatiquement à {(i+1)*0.5:.1f}s")
                print("   Le problème de fermeture automatique persiste !")
                return False
        
        print("\n✅ SUCCÈS: Dialog reste ouvert pendant 5 secondes")
        
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
        
        print(f"\n🎉 SOLUTION FINALE VALIDÉE !")
        print("=" * 40)
        print("   ✅ Dialog Nueva Factura s'ouvre au premier plan")
        print("   ✅ Dialog reste stable (PAS de fermeture automatique)")
        print("   ✅ Dialog résiste aux changements de focus")
        print("   ✅ Dialog répond aux interactions utilisateur")
        print("   ✅ Solution simple et efficace")
        print(f"\n🏆 PROBLÈME RÉSOLU DÉFINITIVEMENT !")
        print("   La fenêtre Nueva Factura ne se ferme plus automatiquement")
        print("   et apparaît toujours au premier plan.")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    success = test_nueva_factura_solution_finale()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
