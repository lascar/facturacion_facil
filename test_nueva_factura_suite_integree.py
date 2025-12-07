#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de tests intégrée pour Nueva Factura - Solution de forçage maximal
Tests intégrés sans dépendance pytest pour validation complète
"""

import sys
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window_pyqt5 import MainWindowPyQt5


class TestSuiteNuevaFactura:
    """Suite de tests intégrée pour Nueva Factura"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.test_results = {}
    
    def setup(self):
        """Setup pour les tests"""
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
    
    def cleanup(self):
        """Cleanup après les tests"""
        if self.main_window:
            try:
                if hasattr(self.main_window, 'facturas_window') and self.main_window.facturas_window:
                    if hasattr(self.main_window.facturas_window, 'crear_dialog') and self.main_window.facturas_window.crear_dialog:
                        self.main_window.facturas_window.crear_dialog.close()
                    self.main_window.facturas_window.close()
                self.main_window.close()
            except:
                pass
        self.main_window = None
    
    def assert_true(self, condition, message):
        """Assertion personnalisée"""
        if not condition:
            raise AssertionError(message)
    
    def test_nueva_factura_forcage_maximal(self):
        """Test du forçage maximal pour Nueva Factura"""
        print("   🧪 Test forçage maximal...")
        
        # Créer l'application
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.app.processEvents()
        
        # Ouvrir facturas
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        self.assert_true(facturas_window is not None, "Fenêtre facturas doit être créée")
        self.assert_true(facturas_window.isVisible(), "Fenêtre facturas doit être visible")
        
        # S'assurer que facturas est au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.5)
        
        # Ouvrir Nueva Factura avec forçage maximal
        facturas_window.new_factura()
        
        # Vérification immédiate
        self.app.processEvents()
        time.sleep(0.3)
        
        self.assert_true(facturas_window.crear_dialog is not None, "Dialog Nueva Factura doit être créé")
        self.assert_true(facturas_window.crear_dialog.isVisible(), "Dialog Nueva Factura doit être visible")
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier les flags de forçage maximal
        flags = dialog.windowFlags()
        has_stay_on_top = bool(flags & Qt.WindowStaysOnTopHint)
        has_bypass = bool(flags & Qt.X11BypassWindowManagerHint)
        has_frameless = bool(flags & Qt.FramelessWindowHint)
        has_tool = bool(flags & Qt.Tool)
        has_window = bool(flags & Qt.Window)
        
        # Au moins un flag de forçage doit être présent
        has_forcing_flags = has_stay_on_top or has_tool or has_bypass
        self.assert_true(has_forcing_flags, "Au moins un flag de forçage doit être appliqué")
        self.assert_true(has_window, "Flag Window doit être présent")
        
        # Vérifier que le dialog est actif
        is_active = dialog.isActiveWindow()
        self.assert_true(is_active, "Dialog doit être la fenêtre active")
        
        print("      ✅ Forçage maximal validé")
    
    def test_nueva_factura_resistance_focus(self):
        """Test de résistance au changement de focus"""
        print("   🧪 Test résistance focus...")
        
        # Setup
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        self.assert_true(dialog.isVisible(), "Dialog doit être visible initialement")
        
        # Essayer de forcer facturas au premier plan
        facturas_window.raise_()
        facturas_window.activateWindow()
        facturas_window.setFocus()
        self.app.processEvents()
        time.sleep(0.2)
        
        # Vérifier que le dialog reste accessible
        still_visible = dialog.isVisible()
        self.assert_true(still_visible, "Dialog doit rester visible après tentative de changement de focus")
        
        print("      ✅ Résistance focus validée")
    
    def test_nueva_factura_stabilite_long_terme(self):
        """Test de stabilité long terme du dialog"""
        print("   🧪 Test stabilité long terme...")
        
        # Setup
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        time.sleep(0.3)
        
        dialog = facturas_window.crear_dialog
        self.assert_true(dialog.isVisible(), "Dialog doit être visible initialement")
        
        # Attendre la période de maintien complète (2.5 secondes)
        time.sleep(2.5)
        self.app.processEvents()
        
        # Vérifier la stabilité après nettoyage
        final_visible = dialog.isVisible()
        self.assert_true(final_visible, "Dialog doit rester stable après la période de maintien")
        
        print("      ✅ Stabilité long terme validée")
    
    def test_nueva_factura_sans_parent(self):
        """Test que le dialog est créé sans parent"""
        print("   🧪 Test dialog sans parent...")
        
        # Setup
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        # Ouvrir Nueva Factura
        facturas_window.new_factura()
        self.app.processEvents()
        
        dialog = facturas_window.crear_dialog
        
        # Vérifier que le dialog n'a pas de parent
        parent = dialog.parent()
        self.assert_true(parent is None, "Dialog doit être créé sans parent pour éviter les conflits de hiérarchie")
        
        print("      ✅ Dialog sans parent validé")
    
    def test_scenario_utilisateur_complet(self):
        """Test du scénario utilisateur complet"""
        print("   🧪 Test scénario utilisateur complet...")
        
        # Simulation du workflow utilisateur complet
        self.main_window = MainWindowPyQt5()
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.5)
        
        # Utilisateur ouvre Facturas
        self.main_window.open_facturas()
        facturas_window = self.main_window.facturas_window
        
        self.assert_true(facturas_window.isVisible(), "Fenêtre Facturas doit être visible")
        
        # Utilisateur travaille dans facturas (simulation)
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(1.0)
        
        # MOMENT CRITIQUE: Utilisateur clique Nueva Factura
        facturas_window.new_factura()
        
        # Vérification immédiate (ce que voit l'utilisateur)
        self.app.processEvents()
        time.sleep(0.2)
        
        dialog = facturas_window.crear_dialog
        self.assert_true(dialog is not None, "Dialog doit être créé")
        self.assert_true(dialog.isVisible(), "Dialog doit être visible pour l'utilisateur")
        self.assert_true(dialog.isActiveWindow(), "Dialog doit être au premier plan")
        
        # Test de résistance utilisateur
        facturas_window.raise_()
        facturas_window.activateWindow()
        self.app.processEvents()
        time.sleep(0.3)
        
        # Dialog doit rester accessible
        self.assert_true(dialog.isVisible(), "Dialog doit rester accessible après tentative de retour à Facturas")
        
        print("      ✅ Scénario utilisateur complet validé")
    
    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("🚀 SUITE DE TESTS NUEVA FACTURA INTÉGRÉE")
        print("=" * 50)
        
        tests = [
            ("Forçage Maximal", self.test_nueva_factura_forcage_maximal),
            ("Résistance Focus", self.test_nueva_factura_resistance_focus),
            ("Stabilité Long Terme", self.test_nueva_factura_stabilite_long_terme),
            ("Dialog Sans Parent", self.test_nueva_factura_sans_parent),
            ("Scénario Utilisateur", self.test_scenario_utilisateur_complet)
        ]
        
        success_count = 0
        total_count = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Test: {test_name}")
            try:
                self.setup()
                test_func()
                self.test_results[test_name] = "SUCCÈS"
                success_count += 1
                print(f"   ✅ {test_name}: SUCCÈS")
            except Exception as e:
                self.test_results[test_name] = f"ÉCHEC: {e}"
                print(f"   ❌ {test_name}: ÉCHEC - {e}")
            finally:
                self.cleanup()
        
        # Résumé final
        print(f"\n🎯 RÉSUMÉ SUITE DE TESTS")
        print("=" * 30)
        print(f"   Tests réussis: {success_count}/{total_count}")
        print(f"   Taux de réussite: {(success_count/total_count)*100:.1f}%")
        
        if success_count == total_count:
            print(f"\n🎉 TOUS LES TESTS RÉUSSIS !")
            print("   ✅ Solution de forçage maximal validée")
            print("   ✅ Tests intégrés à la suite de tests")
            print("   ✅ Problème Nueva Factura définitivement résolu")
            
            print(f"\n📋 TESTS INTÉGRÉS:")
            print("   • Test de forçage maximal avec tous les flags")
            print("   • Test de résistance aux changements de focus")
            print("   • Test de stabilité long terme")
            print("   • Test de dialog sans parent")
            print("   • Test de scénario utilisateur complet")
            
            print(f"\n🎯 SOLUTION VALIDÉE:")
            print("   La solution de forçage maximal est maintenant")
            print("   intégrée et validée par une suite de tests complète.")
            
            return True
        else:
            print(f"\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
            for test_name, result in self.test_results.items():
                if "ÉCHEC" in result:
                    print(f"   ❌ {test_name}: {result}")
            return False


def main():
    """Fonction principale"""
    test_suite = TestSuiteNuevaFactura()
    success = test_suite.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
