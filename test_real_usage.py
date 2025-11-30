#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'utilisation réelle - Ouvrir les deux fenêtres et tester la synchronisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from gui import set_gui_framework
from database.database import db
from ui.stock_pyqt5 import StockPyQt5Window
from ui.productos_pyqt5 import ProductosPyQt5Window
from utils.event_manager_pyqt5 import event_manager

class TestMainWindow(QMainWindow):
    """Fenêtre principale de test pour simuler l'utilisation réelle"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Synchronisation - Fenêtre Principale")
        self.setGeometry(100, 100, 300, 200)
        
        # Fenêtres
        self.stock_window = None
        self.productos_window = None
        
        # Interface
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Boutons pour ouvrir les fenêtres
        stock_btn = QPushButton("📊 Ouvrir Stock")
        stock_btn.clicked.connect(self.open_stock_window)
        layout.addWidget(stock_btn)
        
        productos_btn = QPushButton("📦 Ouvrir Productos")
        productos_btn.clicked.connect(self.open_productos_window)
        layout.addWidget(productos_btn)
        
        test_btn = QPushButton("🧪 Test Synchronisation")
        test_btn.clicked.connect(self.test_synchronization)
        layout.addWidget(test_btn)
        
        close_btn = QPushButton("❌ Fermer Tout")
        close_btn.clicked.connect(self.close_all)
        layout.addWidget(close_btn)
        
        print("🏠 Fenêtre principale créée")
        print("📋 Instructions:")
        print("   1. Cliquez 'Ouvrir Stock' et 'Ouvrir Productos'")
        print("   2. Dans Stock: Sélectionnez un produit et modifiez le stock")
        print("   3. Vérifiez que Productos se met à jour automatiquement")
        print("   4. Dans Productos: Modifiez un produit dans le formulaire")
        print("   5. Vérifiez que la liste se met à jour immédiatement")
    
    def open_stock_window(self):
        """Ouvrir la fenêtre Stock"""
        if self.stock_window is None:
            self.stock_window = StockPyQt5Window()
            print("📊 Fenêtre Stock ouverte")
        self.stock_window.show()
        self.stock_window.raise_()
    
    def open_productos_window(self):
        """Ouvrir la fenêtre Productos"""
        if self.productos_window is None:
            self.productos_window = ProductosPyQt5Window()
            print("📦 Fenêtre Productos ouverte")
        self.productos_window.show()
        self.productos_window.raise_()
    
    def test_synchronization(self):
        """Test automatique de synchronisation"""
        print("\n🧪 TEST AUTOMATIQUE DE SYNCHRONISATION")
        print("-" * 40)
        
        # Vérifier que les fenêtres sont ouvertes
        if not self.stock_window or not self.productos_window:
            print("❌ Ouvrez d'abord les deux fenêtres (Stock et Productos)")
            return
        
        # Obtenir un produit de test
        productos = db.get_all_products()
        if not productos:
            print("❌ Aucun produit trouvé. Créez des produits d'abord.")
            return
        
        test_product = productos[0]
        product_id = test_product['id']
        old_stock = test_product.get('stock_actual', 0)
        new_stock = old_stock + 10
        
        print(f"🎯 Test avec: {test_product.get('nombre', 'N/A')} (ID: {product_id})")
        print(f"📦 Stock: {old_stock} → {new_stock}")
        
        # Émettre le signal comme le ferait la fenêtre Stock
        print("📤 Émission du signal stock_adjusted...")
        event_manager.emit_stock_adjusted(product_id, old_stock, new_stock)
        
        # Traiter les événements
        QApplication.processEvents()
        
        # Vérifier si la fenêtre Productos a été mise à jour
        print("🔍 Vérification de la mise à jour dans Productos...")
        
        # Chercher le produit dans la table Productos
        found_updated = False
        for row in range(self.productos_window.products_table.rowCount()):
            item = self.productos_window.products_table.item(row, 0)  # Colonne ID
            if item and int(item.text()) == product_id:
                stock_item = self.productos_window.products_table.item(row, 4)  # Colonne Stock
                if stock_item:
                    current_stock = int(stock_item.text())
                    if current_stock == new_stock:
                        print(f"✅ SUCCÈS! Stock mis à jour dans Productos: {current_stock}")
                        found_updated = True
                    else:
                        print(f"❌ ÉCHEC! Stock non mis à jour: attendu {new_stock}, trouvé {current_stock}")
                break
        
        if not found_updated:
            print("❌ Produit non trouvé dans la table Productos")
        
        print("\n📝 Test terminé. Testez maintenant manuellement:")
        print("   • Modifiez un stock dans la fenêtre Stock")
        print("   • Vérifiez la mise à jour dans Productos")
        print("   • Modifiez un produit dans le formulaire Productos")
        print("   • Vérifiez la mise à jour dans la liste Productos")
    
    def close_all(self):
        """Fermer toutes les fenêtres"""
        if self.stock_window:
            self.stock_window.close()
            self.stock_window = None
        if self.productos_window:
            self.productos_window.close()
            self.productos_window = None
        self.close()

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DU TEST D'UTILISATION RÉELLE")
    print("=" * 50)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    # Créer la fenêtre principale de test
    main_window = TestMainWindow()
    main_window.show()
    
    # Démarrer l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
