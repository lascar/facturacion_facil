#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de diagnostic de la synchronisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from gui import set_gui_framework
from database.database import db
from ui.stock_pyqt5 import StockPyQt5Window
from ui.productos_pyqt5 import ProductosPyQt5Window
from utils.event_manager_pyqt5 import event_manager

def test_sync_debug():
    """Test de diagnostic complet"""
    
    print("🔍 DIAGNOSTIC DE SYNCHRONISATION")
    print("=" * 50)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # 1. Vérifier les imports
        print("1️⃣ Vérification des imports...")
        print(f"   ✅ event_manager: {type(event_manager)}")
        print(f"   ✅ StockPyQt5Window: {StockPyQt5Window}")
        print(f"   ✅ ProductosPyQt5Window: {ProductosPyQt5Window}")
        
        # 2. Créer les fenêtres
        print("\n2️⃣ Création des fenêtres...")
        stock_window = StockPyQt5Window()
        productos_window = ProductosPyQt5Window()
        print("   ✅ Fenêtres créées")
        
        # 3. Vérifier les connexions
        print("\n3️⃣ Vérification des connexions...")
        
        # Vérifier que les méthodes existent
        has_connect = hasattr(productos_window, 'connect_event_signals')
        has_on_stock_adjusted = hasattr(productos_window, 'on_stock_adjusted')
        has_update_table = hasattr(productos_window, 'update_product_stock_in_table')
        
        print(f"   📡 connect_event_signals: {has_connect}")
        print(f"   📡 on_stock_adjusted: {has_on_stock_adjusted}")
        print(f"   📡 update_product_stock_in_table: {has_update_table}")
        
        # 4. Test d'émission de signal
        print("\n4️⃣ Test d'émission de signal...")
        
        # Capteur de signal pour vérifier la réception
        signals_received = []
        
        def debug_signal_receiver(product_id, old_stock, new_stock):
            signals_received.append({
                'product_id': product_id,
                'old_stock': old_stock,
                'new_stock': new_stock
            })
            print(f"   📡 Signal reçu par debug: Produit {product_id}, {old_stock} → {new_stock}")
        
        # Connecter notre capteur de debug
        event_manager.stock_adjusted.connect(debug_signal_receiver)
        
        # Émettre un signal de test
        print("   📤 Émission signal test...")
        event_manager.emit_stock_adjusted(999, 50, 75)
        
        # Traiter les événements
        app.processEvents()
        
        if signals_received:
            print(f"   ✅ Signal reçu: {signals_received[0]}")
        else:
            print("   ❌ Aucun signal reçu")
        
        # 5. Test avec données réelles
        print("\n5️⃣ Test avec données réelles...")
        
        productos = db.get_all_products()
        if productos:
            test_product = productos[0]
            product_id = test_product['id']
            old_stock = test_product.get('stock_actual', 0)
            new_stock = old_stock + 5
            
            print(f"   🎯 Produit test: {test_product.get('nombre', 'N/A')} (ID: {product_id})")
            print(f"   📦 Stock: {old_stock} → {new_stock}")
            
            # Charger les données dans la fenêtre productos
            productos_window.load_productos()
            
            # Vérifier que le produit est dans la table
            table_rows = productos_window.products_table.rowCount()
            print(f"   📊 Produits dans la table: {table_rows}")
            
            # Émettre le signal avec des données réelles
            print("   📤 Émission signal avec données réelles...")
            event_manager.emit_stock_adjusted(product_id, old_stock, new_stock)
            
            # Traiter les événements
            app.processEvents()
            
            # Vérifier si la table a été mise à jour
            for row in range(productos_window.products_table.rowCount()):
                item = productos_window.products_table.item(row, 0)  # Colonne ID
                if item and int(item.text()) == product_id:
                    stock_item = productos_window.products_table.item(row, 4)  # Colonne Stock
                    if stock_item:
                        current_stock = int(stock_item.text())
                        print(f"   📊 Stock dans table: {current_stock}")
                        if current_stock == new_stock:
                            print("   ✅ Table mise à jour correctement!")
                        else:
                            print(f"   ❌ Table non mise à jour: attendu {new_stock}, trouvé {current_stock}")
                    break
        else:
            print("   ⚠️  Aucun produit trouvé pour le test")
        
        print("\n🎯 DIAGNOSTIC TERMINÉ")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer
        try:
            stock_window.close()
            productos_window.close()
        except:
            pass
        app.quit()

if __name__ == "__main__":
    success = test_sync_debug()
    sys.exit(0 if success else 1)
