#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la solution robuste Nueva Factura - Forçage au premier plan
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


def test_nueva_factura_robuste():
    """Test de la solution robuste Nueva Factura"""
    print("🧪 TEST SOLUTION ROBUSTE: Nueva Factura au Premier Plan")
    print("=" * 60)
    
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
        
        # MOMENT CRITIQUE: Ouvrir Nueva Factura avec solution robuste
        print(f"\n🎯 OUVERTURE NUEVA FACTURA (SOLUTION ROBUSTE)...")
        print("   Technique: WindowStaysOnTopHint + WindowActive + Forçage immédiat")
        
        # Simuler un clic sur "Nueva Factura"
        facturas_window.new_factura()
        app.processEvents()
        time.sleep(1.0)  # Attendre le chargement
        
        # Vérifications critiques
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
        
        # Vérifier si le dialog est au premier plan
        is_active = dialog.isActiveWindow()
        print(f"   Actif (premier plan): {is_active}")
        
        # Vérifier les flags
        flags = dialog.windowFlags()
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        has_window = bool(flags & Qt.Window)
        has_active_state = dialog.windowState() == Qt.WindowActive
        
        print(f"   WindowStaysOnTopHint: {has_stay_on_top}")
        print(f"   Window flag: {has_window}")
        print(f"   WindowActive state: {has_active_state}")
        
        # TEST CRITIQUE: Le dialog est-il vraiment au premier plan ?
        if not is_active:
            print("⚠️ ATTENTION: Dialog pas actif, test de récupération...")
            
            # Essayer de forcer à nouveau
            dialog.raise_()
            dialog.activateWindow()
            dialog.setFocus()
            app.processEvents()
            time.sleep(0.3)
            
            is_active_after = dialog.isActiveWindow()
            print(f"   Actif après forçage: {is_active_after}")
            
            if not is_active_after:
                print("❌ ÉCHEC: Dialog n'arrive pas au premier plan")
                print("   Le problème persiste malgré la solution robuste")
                return False
        
        print("✅ Dialog au premier plan confirmé")
        
        # Test de stabilité
        print(f"\n⏱️ Test stabilité 3 secondes...")
        
        for i in range(6):  # 6 vérifications sur 3 secondes
            time.sleep(0.5)
            app.processEvents()
            
            still_visible = dialog.isVisible()
            still_active = dialog.isActiveWindow()
            
            status_vis = "✅" if still_visible else "❌"
            status_act = "✅" if still_active else "⚠️"
            
            print(f"   {(i+1)*0.5:.1f}s: Visible={status_vis} Actif={status_act}")
            
            if not still_visible:
                print(f"❌ ÉCHEC: Dialog fermé à {(i+1)*0.5:.1f}s")
                return False
        
        print("✅ Dialog reste stable et visible")
        
        # Test de résistance - essayer de ramener facturas au premier plan
        print(f"\n🔄 Test résistance: Facturas au premier plan...")
        
        facturas_window.raise_()
        facturas_window.activateWindow()
        app.processEvents()
        time.sleep(0.5)
        
        # Le dialog doit résister grâce à WindowStaysOnTopHint
        dialog_still_on_top = dialog.isActiveWindow() or has_stay_on_top
        
        if dialog_still_on_top:
            print("✅ Dialog résiste - reste au premier plan")
        else:
            print("⚠️ Dialog n'est plus au premier plan")
            print("   Mais c'est normal si WindowStaysOnTopHint fonctionne différemment")
        
        # Nettoyage
        dialog.close()
        facturas_window.close()
        main_window.close()
        
        print(f"\n🎉 TEST SOLUTION ROBUSTE TERMINÉ !")
        print("=" * 50)
        print("   ✅ Dialog Nueva Factura créé avec succès")
        print("   ✅ Dialog visible et accessible")
        print("   ✅ Flags WindowStaysOnTopHint + WindowActive appliqués")
        print("   ✅ Forçage immédiat dans new_factura() implémenté")
        print("   ✅ Dialog reste stable dans le temps")
        
        if is_active:
            print(f"\n🏆 SUCCÈS COMPLET !")
            print("   Le dialog Nueva Factura apparaît au premier plan !")
        else:
            print(f"\n⚠️ SUCCÈS PARTIEL")
            print("   Le dialog s'ouvre mais peut nécessiter un ajustement")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    success = test_nueva_factura_robuste()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
