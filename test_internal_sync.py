#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la synchronisation interne dans la fenêtre Productos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from gui import set_gui_framework
from database.database import db
from ui.productos_pyqt5 import ProductosPyQt5Window

def test_internal_sync():
    """Test de la synchronisation interne formulaire ↔ liste"""
    
    print("🔄 TEST SYNCHRONISATION INTERNE PRODUCTOS")
    print("=" * 50)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre Productos
        print("📦 Création de la fenêtre Productos...")
        productos_window = ProductosPyQt5Window()
        productos_window.show()
        
        # Traiter les événements pour s'assurer que tout est initialisé
        app.processEvents()
        
        # Vérifier qu'il y a des produits
        if productos_window.products_table.rowCount() == 0:
            print("❌ Aucun produit dans la table. Créez des produits d'abord.")
            return False
        
        print(f"📊 Produits dans la table: {productos_window.products_table.rowCount()}")
        
        # Sélectionner le premier produit
        productos_window.products_table.selectRow(0)
        productos_window.on_product_selected()
        
        # Traiter les événements
        app.processEvents()
        
        # Vérifier que le formulaire est rempli
        if not productos_window.selected_producto_id:
            print("❌ Aucun produit sélectionné")
            return False
        
        print(f"✅ Produit sélectionné: {productos_window.selected_producto_id}")
        print(f"📝 Nom dans formulaire: '{productos_window.nombre_edit.text()}'")
        
        # Obtenir les valeurs originales
        original_name = productos_window.nombre_edit.text()
        original_price = productos_window.precio_edit.value()
        
        # Test 1: Modifier le nom
        print("\n🧪 Test 1: Modification du nom...")
        new_name = f"{original_name}_MODIFIÉ"
        productos_window.nombre_edit.setText(new_name)
        
        # Traiter les événements pour déclencher la synchronisation
        app.processEvents()
        
        # Vérifier que la table a été mise à jour
        selected_row = productos_window.products_table.currentRow()
        if selected_row >= 0:
            name_item = productos_window.products_table.item(selected_row, 1)  # Colonne Nom
            if name_item and name_item.text() == new_name:
                print(f"✅ Nom mis à jour dans la table: '{name_item.text()}'")
            else:
                current_name = name_item.text() if name_item else "None"
                print(f"❌ Nom non mis à jour dans la table: attendu '{new_name}', trouvé '{current_name}'")
        
        # Test 2: Modifier le prix
        print("\n🧪 Test 2: Modification du prix...")
        new_price = original_price + 5.50
        productos_window.precio_edit.setValue(new_price)
        
        # Traiter les événements
        app.processEvents()
        
        # Vérifier que la table a été mise à jour
        if selected_row >= 0:
            price_item = productos_window.products_table.item(selected_row, 3)  # Colonne Prix
            if price_item:
                current_price = float(price_item.text())
                if abs(current_price - new_price) < 0.01:  # Comparaison avec tolérance
                    print(f"✅ Prix mis à jour dans la table: {current_price}")
                else:
                    print(f"❌ Prix non mis à jour dans la table: attendu {new_price}, trouvé {current_price}")
            else:
                print("❌ Aucun item prix trouvé dans la table")
        
        # Test 3: Vérifier les connexions des signaux
        print("\n🧪 Test 3: Vérification des connexions...")
        
        # Vérifier que les méthodes de connexion existent
        has_setup_form = hasattr(productos_window, 'setup_form_connections')
        has_on_form_changed = hasattr(productos_window, 'on_form_data_changed')
        has_update_table = hasattr(productos_window, 'update_table_row_from_form')
        
        print(f"📡 setup_form_connections: {has_setup_form}")
        print(f"📡 on_form_data_changed: {has_on_form_changed}")
        print(f"📡 update_table_row_from_form: {has_update_table}")
        
        # Vérifier si les signaux sont bloqués
        signals_blocked = productos_window.nombre_edit.signalsBlocked()
        print(f"🚫 Signaux bloqués: {signals_blocked}")
        
        print("\n🎯 TEST TERMINÉ")
        print("📝 Résumé:")
        print("   • Si les modifications apparaissent dans la table → Synchronisation OK")
        print("   • Si les modifications n'apparaissent pas → Problème de synchronisation")
        
        # Garder la fenêtre ouverte pour inspection manuelle
        print("\n👀 Fenêtre ouverte pour inspection manuelle...")
        print("   • Modifiez des valeurs dans le formulaire")
        print("   • Vérifiez si la table se met à jour automatiquement")
        print("   • Fermez la fenêtre pour terminer")
        
        # Démarrer la boucle d'événements
        return app.exec_() == 0
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_internal_sync()
    sys.exit(0 if success else 1)
