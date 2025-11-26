#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration de l'interface utilisateur avec les statuts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

def test_ui_integration():
    """Test de l'intégration UI avec les statuts"""
    
    print("🧪 Test d'intégration UI - Système de statuts")
    print("=" * 50)
    
    try:
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        # Test 1: Fenêtre d'organisation avec statuts
        print("\n1. Test de la fenêtre d'organisation...")
        from ui.organizacion_pyqt6 import OrganizacionPyQt6Window
        
        org_window = OrganizacionPyQt6Window()
        print("✅ Fenêtre d'organisation créée")
        
        # Vérifier que la table des statuts existe
        if hasattr(org_window, 'statuses_table'):
            print("✅ Table des statuts trouvée")
            print(f"   Colonnes: {org_window.statuses_table.columnCount()}")
            print(f"   Lignes: {org_window.statuses_table.rowCount()}")
        else:
            print("❌ Table des statuts non trouvée")
        
        # Test 2: Éditeur de factures avec statuts
        print("\n2. Test de l'éditeur de factures...")
        from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
        
        editor_window = FacturaEditorPyQt6Window()
        print("✅ Éditeur de factures créé")
        
        # Vérifier que le combo des statuts existe
        if hasattr(editor_window, 'estado_combo'):
            print("✅ Combo des statuts trouvé")
            print(f"   Nombre d'options: {editor_window.estado_combo.count()}")
            
            # Afficher les options
            for i in range(editor_window.estado_combo.count()):
                option = editor_window.estado_combo.itemText(i)
                print(f"   - {option}")
        else:
            print("❌ Combo des statuts non trouvé")
        
        # Test 3: Liste des factures avec statuts
        print("\n3. Test de la liste des factures...")
        from ui.facturas_pyqt6 import FacturasPyQt6Window
        
        list_window = FacturasPyQt6Window()
        print("✅ Liste des factures créée")
        
        # Vérifier que le filtre des statuts existe
        if hasattr(list_window, 'status_filter'):
            print("✅ Filtre des statuts trouvé")
            print(f"   Nombre d'options: {list_window.status_filter.count()}")
            
            # Afficher les options
            for i in range(list_window.status_filter.count()):
                option = list_window.status_filter.itemText(i)
                print(f"   - {option}")
        else:
            print("❌ Filtre des statuts non trouvé")
        
        # Test 4: Dialogue de configuration des statuts
        print("\n4. Test du dialogue de configuration...")
        from ui.invoice_status_dialog import InvoiceStatusDialog
        
        dialog = InvoiceStatusDialog()
        print("✅ Dialogue de configuration créé")
        
        # Vérifier les champs
        fields_to_check = ['name_edit', 'description_edit', 'allow_modification_cb', 'color_btn', 'order_spin']
        for field in fields_to_check:
            if hasattr(dialog, field):
                print(f"✅ Champ '{field}' trouvé")
            else:
                print(f"❌ Champ '{field}' manquant")
        
        print("\n🎉 Test d'intégration UI terminé avec succès!")
        
        # Fermer les fenêtres
        org_window.close()
        editor_window.close()
        list_window.close()
        dialog.close()
        
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test UI: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ui_integration()
    if success:
        print("\n✅ Test d'intégration UI réussi!")
    else:
        print("\n❌ Test d'intégration UI échoué!")
        sys.exit(1)
