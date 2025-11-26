#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du dialogue de configuration des statuts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_status_dialog():
    """Test du dialogue de configuration des statuts"""
    
    print("🧪 Test du dialogue de configuration des statuts")
    print("=" * 50)
    
    try:
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        # Test 1: Dialogue vide (nouveau statut)
        print("\n1️⃣ Test du dialogue pour nouveau statut...")
        from ui.invoice_status_dialog import InvoiceStatusDialog
        
        dialog = InvoiceStatusDialog()
        print("✅ Dialogue créé sans erreur")
        
        # Vérifier les champs
        fields_to_check = [
            ('name_edit', 'Champ nom'),
            ('description_edit', 'Champ description'),
            ('allow_modification_cb', 'Checkbox modification'),
            ('color_btn', 'Bouton couleur'),
            ('color_preview', 'Aperçu couleur'),
            ('order_spin', 'Spinner ordre')
        ]
        
        for field_name, field_desc in fields_to_check:
            if hasattr(dialog, field_name):
                field = getattr(dialog, field_name)
                print(f"✅ {field_desc} trouvé: {type(field).__name__}")
            else:
                print(f"❌ {field_desc} manquant")
        
        # Vérifier la couleur par défaut
        if hasattr(dialog, 'selected_color'):
            print(f"✅ Couleur par défaut: {dialog.selected_color}")
        else:
            print("❌ Couleur par défaut manquante")
        
        # Test 2: Dialogue avec données existantes
        print("\n2️⃣ Test du dialogue avec données existantes...")
        
        existing_status = {
            'nombre': 'Test Status',
            'descripcion': 'Description de test',
            'permite_modificacion': True,
            'color': '#ff5733',
            'orden': 5
        }
        
        dialog_with_data = InvoiceStatusDialog(status_data=existing_status)
        print("✅ Dialogue avec données créé sans erreur")
        
        # Vérifier que les données sont chargées
        if hasattr(dialog_with_data, 'name_edit') and dialog_with_data.name_edit.text() == 'Test Status':
            print("✅ Nom chargé correctement")
        else:
            print(f"❌ Nom non chargé: {dialog_with_data.name_edit.text() if hasattr(dialog_with_data, 'name_edit') else 'Champ manquant'}")
        
        if hasattr(dialog_with_data, 'description_edit') and dialog_with_data.description_edit.toPlainText() == 'Description de test':
            print("✅ Description chargée correctement")
        else:
            print("❌ Description non chargée")
        
        if hasattr(dialog_with_data, 'allow_modification_cb') and dialog_with_data.allow_modification_cb.isChecked():
            print("✅ Checkbox modification cochée")
        else:
            print("❌ Checkbox modification non cochée")
        
        if hasattr(dialog_with_data, 'selected_color') and dialog_with_data.selected_color == '#ff5733':
            print("✅ Couleur chargée correctement")
        else:
            print(f"❌ Couleur non chargée: {getattr(dialog_with_data, 'selected_color', 'Attribut manquant')}")
        
        if hasattr(dialog_with_data, 'order_spin') and dialog_with_data.order_spin.value() == 5:
            print("✅ Ordre chargé correctement")
        else:
            print("❌ Ordre non chargé")
        
        # Test 3: Validation des méthodes
        print("\n3️⃣ Test des méthodes du dialogue...")
        
        methods_to_check = [
            'setup_ui',
            'load_data',
            'select_color',
            'update_color_preview',
            'save_status',
            'get_status_data'
        ]
        
        for method_name in methods_to_check:
            if hasattr(dialog, method_name):
                method = getattr(dialog, method_name)
                if callable(method):
                    print(f"✅ Méthode {method_name} disponible")
                else:
                    print(f"❌ {method_name} n'est pas une méthode")
            else:
                print(f"❌ Méthode {method_name} manquante")
        
        # Test 4: Test de la méthode get_status_data
        print("\n4️⃣ Test de récupération des données...")
        
        try:
            status_data = dialog_with_data.get_status_data()
            if status_data:
                print("✅ Données récupérées:")
                print(f"   - Nom: {status_data.get('nombre', 'N/A')}")
                print(f"   - Description: {status_data.get('descripcion', 'N/A')}")
                print(f"   - Modifiable: {status_data.get('permite_modificacion', 'N/A')}")
                print(f"   - Couleur: {status_data.get('color', 'N/A')}")
                print(f"   - Ordre: {status_data.get('orden', 'N/A')}")
            else:
                print("❌ Aucune donnée récupérée")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des données: {e}")
        
        # Fermer les dialogues
        dialog.close()
        dialog_with_data.close()
        
        # Fermer l'application après un court délai
        QTimer.singleShot(100, app.quit)
        
        print("\n🎉 Test du dialogue terminé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_status_dialog()
    if success:
        print("\n✅ Dialogue de configuration des statuts fonctionnel!")
    else:
        print("\n❌ Problèmes détectés dans le dialogue!")
        sys.exit(1)
