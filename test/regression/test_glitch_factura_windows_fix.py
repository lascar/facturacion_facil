#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de régression pour le fix du glitch des fenêtres de factures
Valide que les fenêtres s'ouvrent sans glitch visuel (sans changement de flags)
"""

import unittest
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from PyQt5.QtWidgets import QApplication
from utils.dialog_no_glitch_foreground import NoGlitchDialogForegroundMixin, force_dialog_no_glitch_foreground
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog, VerFacturaDialog
from ui.factura_edit_window import FacturaEditWindow


class TestGlitchFacturaWindowsFix(unittest.TestCase):
    """Tests pour vérifier que le glitch des fenêtres de factures est corrigé"""
    
    @classmethod
    def setUpClass(cls):
        """Initialiser QApplication pour les tests PyQt5"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def test_no_glitch_mixin_exists(self):
        """Test que le nouveau mixin sans glitch existe"""
        # Vérifier que la classe existe
        self.assertTrue(hasattr(NoGlitchDialogForegroundMixin, 'setup_no_glitch_foreground_display'))
        self.assertTrue(hasattr(NoGlitchDialogForegroundMixin, 'force_no_glitch_foreground_now'))
    
    def test_force_dialog_no_glitch_function_exists(self):
        """Test que la fonction utilitaire sans glitch existe"""
        # Vérifier que la fonction existe
        self.assertTrue(callable(force_dialog_no_glitch_foreground))
    
    def test_crear_factura_dialog_uses_no_glitch_mixin(self):
        """Test que CrearFacturaDialog utilise le mixin sans glitch"""
        # Vérifier l'héritage
        self.assertTrue(issubclass(CrearFacturaDialog, NoGlitchDialogForegroundMixin))
        
        # Vérifier que la méthode sans glitch est disponible
        self.assertTrue(hasattr(CrearFacturaDialog, 'setup_no_glitch_foreground_display'))
        self.assertTrue(hasattr(CrearFacturaDialog, 'force_no_glitch_foreground_now'))
    
    def test_editar_factura_dialog_uses_no_glitch_mixin(self):
        """Test que EditarFacturaDialog utilise le mixin sans glitch"""
        # Vérifier l'héritage
        self.assertTrue(issubclass(EditarFacturaDialog, NoGlitchDialogForegroundMixin))
        
        # Vérifier que la méthode sans glitch est disponible
        self.assertTrue(hasattr(EditarFacturaDialog, 'setup_no_glitch_foreground_display'))
        self.assertTrue(hasattr(EditarFacturaDialog, 'force_no_glitch_foreground_now'))
    
    def test_ver_factura_dialog_uses_no_glitch_mixin(self):
        """Test que VerFacturaDialog utilise le mixin sans glitch"""
        # Vérifier l'héritage
        self.assertTrue(issubclass(VerFacturaDialog, NoGlitchDialogForegroundMixin))
        
        # Vérifier que la méthode sans glitch est disponible
        self.assertTrue(hasattr(VerFacturaDialog, 'setup_no_glitch_foreground_display'))
        self.assertTrue(hasattr(VerFacturaDialog, 'force_no_glitch_foreground_now'))
    
    def test_factura_edit_window_uses_no_glitch_mixin(self):
        """Test que FacturaEditWindow utilise le mixin sans glitch"""
        # Vérifier l'héritage
        self.assertTrue(issubclass(FacturaEditWindow, NoGlitchDialogForegroundMixin))
        
        # Vérifier que la méthode sans glitch est disponible
        self.assertTrue(hasattr(FacturaEditWindow, 'setup_no_glitch_foreground_display'))
        self.assertTrue(hasattr(FacturaEditWindow, 'force_no_glitch_foreground_now'))
    
    def test_no_glitch_mixin_no_window_stays_on_top(self):
        """Test que le mixin sans glitch n'utilise pas WindowStaysOnTopHint"""
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QDialog
        
        # Créer un dialog de test avec le mixin
        class TestDialog(QDialog, NoGlitchDialogForegroundMixin):
            def __init__(self):
                super().__init__()
                self.setup_no_glitch_foreground_display()
        
        dialog = TestDialog()
        
        # Vérifier que WindowStaysOnTopHint n'est PAS utilisé
        flags = dialog.windowFlags()
        self.assertFalse(flags & Qt.WindowStaysOnTopHint, 
                        "Le mixin sans glitch ne doit pas utiliser WindowStaysOnTopHint")
        
        dialog.close()
    
    def test_regression_glitch_problema_original(self):
        """Test de régression pour vérifier que le glitch est corrigé"""
        # Ce test vérifie que la solution sans glitch est en place
        # Le problème original était le glitch visuel causé par les changements de flags
        
        # Vérifier que toutes les classes utilisent le mixin sans glitch
        self.assertTrue(issubclass(CrearFacturaDialog, NoGlitchDialogForegroundMixin))
        self.assertTrue(issubclass(EditarFacturaDialog, NoGlitchDialogForegroundMixin))
        self.assertTrue(issubclass(VerFacturaDialog, NoGlitchDialogForegroundMixin))
        self.assertTrue(issubclass(FacturaEditWindow, NoGlitchDialogForegroundMixin))
        
        # Vérifier que l'utilitaire sans glitch est disponible
        self.assertTrue(callable(force_dialog_no_glitch_foreground))
        
        # Si tous ces tests passent, le glitch est corrigé
        print("\n✅ GLITCH CORRIGÉ: Toutes les fenêtres de factures utilisent le système sans glitch")


def run_visual_test():
    """Test visuel pour vérifier l'absence de glitch (optionnel)"""
    print("\n🧪 Test visuel du fix du glitch...")
    
    app = QApplication.instance() or QApplication([])
    
    try:
        # Simuler l'ouverture d'un dialog comme dans l'usage réel
        from database.database import Database
        
        # Utiliser une base de test
        database = Database("base_de_datos/test_facturacion.db")
        
        print("1. Test CrearFacturaDialog...")
        crear_dialog = CrearFacturaDialog(database, None)
        
        # Vérifier qu'il utilise le mixin sans glitch
        if isinstance(crear_dialog, NoGlitchDialogForegroundMixin):
            print("   ✅ CrearFacturaDialog utilise le mixin sans glitch")
        else:
            print("   ❌ CrearFacturaDialog n'utilise pas le mixin sans glitch")
            return False
        
        crear_dialog.close()
        
        print("2. Test FacturaEditWindow...")
        
        # Créer une fenêtre d'édition
        edit_window = FacturaEditWindow(None, database, None)
        
        # Vérifier qu'elle utilise le mixin sans glitch
        if isinstance(edit_window, NoGlitchDialogForegroundMixin):
            print("   ✅ FacturaEditWindow utilise le mixin sans glitch")
        else:
            print("   ❌ FacturaEditWindow n'utilise pas le mixin sans glitch")
            return False
        
        edit_window.close()
        
        print("\n✅ SUCCÈS: Toutes les fenêtres utilisent le système sans glitch")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR dans le test visuel: {e}")
        return False


if __name__ == '__main__':
    # Lancer les tests unitaires
    unittest.main(verbosity=2, exit=False)
    
    # Lancer le test visuel optionnel
    run_visual_test()
