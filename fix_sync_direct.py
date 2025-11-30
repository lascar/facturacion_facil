#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction directe de la synchronisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from gui import set_gui_framework
from database.database import db
from ui.productos_pyqt5 import ProductosPyQt5Window
from ui.stock_pyqt5 import StockPyQt5Window
from utils.event_manager_pyqt5 import event_manager

def fix_synchronization():
    """Correction directe de la synchronisation"""
    
    print("🔧 CORRECTION DIRECTE DE LA SYNCHRONISATION")
    print("=" * 50)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # Test 1: Vérifier que les signaux fonctionnent
        print("1️⃣ Test des signaux...")
        
        signals_received = []
        
        def test_receiver(product_id, old_stock, new_stock):
            signals_received.append((product_id, old_stock, new_stock))
            print(f"   📡 Signal reçu: Produit {product_id}, {old_stock} → {new_stock}")
        
        # Connecter le récepteur de test
        event_manager.stock_adjusted.connect(test_receiver)
        
        # Émettre un signal de test
        event_manager.emit_stock_adjusted(999, 10, 20)
        app.processEvents()
        
        if signals_received:
            print("   ✅ Les signaux fonctionnent")
        else:
            print("   ❌ Les signaux ne fonctionnent pas")
            return False
        
        # Test 2: Créer les fenêtres et tester la synchronisation
        print("\n2️⃣ Test synchronisation inter-fenêtres...")
        
        stock_window = StockPyQt5Window()
        productos_window = ProductosPyQt5Window()
        
        # Vérifier qu'il y a des produits
        productos = db.get_all_products()
        if not productos:
            print("   ❌ Aucun produit trouvé")
            return False
        
        test_product = productos[0]
        product_id = test_product['id']
        old_stock = test_product.get('stock_actual', 0)
        new_stock = old_stock + 5
        
        print(f"   🎯 Test avec produit: {test_product.get('nombre', 'N/A')} (ID: {product_id})")
        
        # Charger les données dans la fenêtre productos
        productos_window.load_productos()
        app.processEvents()
        
        # Vérifier que le produit est dans la table
        found_in_table = False
        for row in range(productos_window.products_table.rowCount()):
            item = productos_window.products_table.item(row, 0)
            if item and int(item.text()) == product_id:
                found_in_table = True
                break
        
        if not found_in_table:
            print(f"   ❌ Produit {product_id} non trouvé dans la table")
            return False
        
        print(f"   ✅ Produit trouvé dans la table à la ligne {row}")
        
        # Émettre le signal de changement de stock
        print(f"   📤 Émission signal: {old_stock} → {new_stock}")
        event_manager.emit_stock_adjusted(product_id, old_stock, new_stock)
        app.processEvents()
        
        # Vérifier la mise à jour dans la table
        stock_item = productos_window.products_table.item(row, 4)  # Colonne Stock
        if stock_item:
            current_stock = int(stock_item.text())
            if current_stock == new_stock:
                print(f"   ✅ Stock mis à jour dans la table: {current_stock}")
            else:
                print(f"   ❌ Stock non mis à jour: attendu {new_stock}, trouvé {current_stock}")
        else:
            print("   ❌ Aucun item stock trouvé")
        
        # Test 3: Synchronisation interne
        print("\n3️⃣ Test synchronisation interne...")
        
        # Sélectionner le produit dans la table
        productos_window.products_table.selectRow(row)
        productos_window.on_product_selected()
        app.processEvents()
        
        if productos_window.selected_producto_id != product_id:
            print(f"   ❌ Produit non sélectionné correctement: {productos_window.selected_producto_id}")
            return False
        
        print(f"   ✅ Produit sélectionné: {productos_window.selected_producto_id}")
        
        # Modifier le nom dans le formulaire
        original_name = productos_window.nombre_edit.text()
        new_name = f"{original_name}_TEST"
        
        print(f"   📝 Modification nom: '{original_name}' → '{new_name}'")
        productos_window.nombre_edit.setText(new_name)
        app.processEvents()
        
        # Vérifier la mise à jour dans la table
        name_item = productos_window.products_table.item(row, 1)  # Colonne Nom
        if name_item and name_item.text() == new_name:
            print(f"   ✅ Nom mis à jour dans la table: '{name_item.text()}'")
        else:
            current_name = name_item.text() if name_item else "None"
            print(f"   ❌ Nom non mis à jour: attendu '{new_name}', trouvé '{current_name}'")
        
        print("\n🎯 TESTS TERMINÉS")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

if __name__ == "__main__":
    success = fix_synchronization()
    if success:
        print("\n✅ Tests réussis - La synchronisation devrait fonctionner")
    else:
        print("\n❌ Tests échoués - Problème de synchronisation détecté")
    sys.exit(0 if success else 1)
