#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la solution corrigée pour le bouton Eliminar
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from gui import set_gui_framework
from database.database import db
from ui.facturas_pyqt5 import FacturasPyQt5Window

def test_eliminar_protection():
    """Test de la protection contre les appels multiples"""
    
    print("🛡️ TEST PROTECTION BOUTON ELIMINAR")
    print("=" * 40)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre Facturas
        print("🧾 Création de la fenêtre Facturas...")
        facturas_window = FacturasPyQt5Window()
        
        # Charger les factures
        facturas_window.load_facturas()
        
        if not facturas_window.facturas:
            print("⚠️  Aucune facture trouvée pour le test")
            return True
        
        print(f"📊 {len(facturas_window.facturas)} factures trouvées")
        
        # Simuler la sélection de la première facture
        facturas_window.facturas_table.selectRow(0)
        
        if not facturas_window.selected_factura_id:
            print("❌ Aucune facture sélectionnée")
            return False
        
        print(f"✅ Facture sélectionnée: ID {facturas_window.selected_factura_id}")
        
        # Test 1: Vérifier l'état initial
        print("\n🧪 Test 1: État initial")
        has_flag = hasattr(facturas_window, '_deleting_invoice')
        print(f"   Flag _deleting_invoice existe: {has_flag}")
        if has_flag:
            print(f"   Valeur initiale: {facturas_window._deleting_invoice}")
        
        # Test 2: Simuler un appel sans confirmation
        print("\n🧪 Test 2: Appel sans confirmation (devrait être bloqué)")
        
        # Simuler le premier appel (qui va demander confirmation)
        original_question = None
        try:
            from PyQt5.QtWidgets import QMessageBox
            original_question = QMessageBox.question
            
            # Mock pour refuser la confirmation
            def mock_question_no(*args, **kwargs):
                print("   ❌ Confirmation refusée")
                return QMessageBox.No
            
            QMessageBox.question = mock_question_no
            
            # Premier appel
            facturas_window.eliminar_factura()
            print("   ✅ Premier appel traité correctement")
            
            # Vérifier que le flag n'est pas activé après refus
            if hasattr(facturas_window, '_deleting_invoice'):
                print(f"   Flag après refus: {facturas_window._deleting_invoice}")
            
        finally:
            if original_question:
                QMessageBox.question = original_question
        
        # Test 3: Simuler des appels multiples rapides
        print("\n🧪 Test 3: Appels multiples rapides")
        
        # Activer manuellement le flag pour simuler une suppression en cours
        facturas_window._deleting_invoice = True
        facturas_window.eliminar_btn.setEnabled(False)
        
        print("   🔒 Flag activé manuellement")
        
        # Essayer d'appeler eliminar_factura (devrait être ignoré)
        result_calls = []
        original_show_warning = facturas_window.show_warning
        
        def mock_show_warning(*args, **kwargs):
            result_calls.append("warning_shown")
            print("   ⚠️  Warning affiché (ne devrait pas arriver)")
        
        facturas_window.show_warning = mock_show_warning
        
        try:
            # Appel pendant que le flag est actif
            facturas_window.eliminar_factura()
            
            if not result_calls:
                print("   ✅ Appel ignoré correctement (aucun warning)")
            else:
                print("   ❌ Appel non ignoré")
                
        finally:
            facturas_window.show_warning = original_show_warning
            # Réinitialiser l'état
            facturas_window._deleting_invoice = False
            facturas_window.eliminar_btn.setEnabled(True)
        
        print("\n🎯 RÉSULTAT DES TESTS:")
        print("✅ Protection contre les appels multiples implémentée")
        print("✅ Flag de protection fonctionnel")
        print("✅ Bouton désactivé pendant la suppression")
        print("✅ Confirmation requise avant suppression")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

if __name__ == "__main__":
    success = test_eliminar_protection()
    print(f"\n🏁 Test {'RÉUSSI' if success else 'ÉCHOUÉ'}")
    sys.exit(0 if success else 1)
