#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manuel de l'interface pour vérifier la synchronisation des stocks
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.append('.')

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel
from PyQt5.QtCore import QTimer

from ui.stock_pyqt5 import StockPyQt5Window
from ui.productos_pyqt5 import ProductosPyQt5Window
from database.database_improved import DatabaseImproved
from utils.event_manager_pyqt5 import event_manager

class TestSyncWindow(QMainWindow):
    """Fenêtre de test pour la synchronisation"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Synchronisation Stocks")
        self.setGeometry(100, 100, 400, 300)
        
        # Variables
        self.stock_window = None
        self.productos_window = None
        
        # Interface
        self.setup_ui()
        
        # Préparer les données de test
        self.prepare_test_data()
    
    def setup_ui(self):
        """Configurer l'interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("🧪 Test Synchronisation Stocks Après Migration")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "1. Cliquez sur 'Ouvrir Stock' et 'Ouvrir Productos'\n"
            "2. Placez les fenêtres côte à côte\n"
            "3. Dans Stock: sélectionnez un produit et changez le stock\n"
            "4. Cliquez 'Ajustar Stock'\n"
            "5. Vérifiez que Productos se met à jour automatiquement"
        )
        instructions.setStyleSheet("margin: 10px; padding: 10px; background: #f0f0f0;")
        layout.addWidget(instructions)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.stock_btn = QPushButton("📊 Ouvrir Stock")
        self.stock_btn.clicked.connect(self.open_stock_window)
        buttons_layout.addWidget(self.stock_btn)
        
        self.productos_btn = QPushButton("📦 Ouvrir Productos")
        self.productos_btn.clicked.connect(self.open_productos_window)
        buttons_layout.addWidget(self.productos_btn)
        
        layout.addLayout(buttons_layout)
        
        # Bouton de test automatique
        self.auto_test_btn = QPushButton("🤖 Test Automatique")
        self.auto_test_btn.clicked.connect(self.run_automatic_test)
        layout.addWidget(self.auto_test_btn)
        
        # Status
        self.status_label = QLabel("Prêt pour les tests")
        self.status_label.setStyleSheet("margin: 10px; padding: 5px; background: #e8f5e8;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def prepare_test_data(self):
        """Préparer des données de test"""
        try:
            db_improved = DatabaseImproved()
            
            # Vérifier s'il y a déjà des produits
            products = db_improved.get_all_products()
            if len(products) == 0:
                # Créer des produits de test
                test_products = [
                    {
                        'nombre': 'Producto Test Sync 1',
                        'referencia': 'SYNC001',
                        'precio': 25.50,
                        'categoria': 'Test',
                        'stock_actual': 100
                    },
                    {
                        'nombre': 'Producto Test Sync 2',
                        'referencia': 'SYNC002',
                        'precio': 15.75,
                        'categoria': 'Test',
                        'stock_actual': 50
                    }
                ]
                
                for product in test_products:
                    db_improved.add_product(product)
                
                self.status_label.setText("✅ Données de test créées")
            else:
                self.status_label.setText(f"✅ {len(products)} produits disponibles pour les tests")
                
        except Exception as e:
            self.status_label.setText(f"❌ Erreur préparation données: {e}")
    
    def open_stock_window(self):
        """Ouvrir la fenêtre Stock"""
        try:
            if self.stock_window is None:
                self.stock_window = StockPyQt5Window()
            
            self.stock_window.show()
            self.stock_window.raise_()
            self.stock_window.activateWindow()
            
            self.status_label.setText("📊 Fenêtre Stock ouverte")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur ouverture Stock: {e}")
    
    def open_productos_window(self):
        """Ouvrir la fenêtre Productos"""
        try:
            if self.productos_window is None:
                self.productos_window = ProductosPyQt5Window()
            
            self.productos_window.show()
            self.productos_window.raise_()
            self.productos_window.activateWindow()
            
            self.status_label.setText("📦 Fenêtre Productos ouverte")
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur ouverture Productos: {e}")
    
    def run_automatic_test(self):
        """Exécuter un test automatique de synchronisation"""
        try:
            self.status_label.setText("🤖 Test automatique en cours...")
            
            # Ouvrir les fenêtres si nécessaire
            if self.stock_window is None:
                self.open_stock_window()
            if self.productos_window is None:
                self.open_productos_window()
            
            # Attendre un peu que les fenêtres se chargent
            QTimer.singleShot(1000, self.perform_sync_test)
            
        except Exception as e:
            self.status_label.setText(f"❌ Erreur test automatique: {e}")
    
    def perform_sync_test(self):
        """Effectuer le test de synchronisation"""
        try:
            # Simuler un changement de stock
            if self.stock_window and len(self.stock_window.productos) > 0:
                product = self.stock_window.productos[0]
                product_id = product.get('id')
                old_stock = product.get('stock_actual', 0)
                new_stock = old_stock + 10
                
                # Émettre le signal de changement
                event_manager.emit_stock_adjusted(product_id, old_stock, new_stock)
                
                self.status_label.setText(f"🔄 Signal émis: Produit {product_id}, {old_stock} → {new_stock}")
                
                # Vérifier après un délai
                QTimer.singleShot(500, lambda: self.check_sync_result(product_id, new_stock))
            else:
                self.status_label.setText("❌ Aucun produit disponible pour le test")
                
        except Exception as e:
            self.status_label.setText(f"❌ Erreur durant test: {e}")
    
    def check_sync_result(self, product_id, expected_stock):
        """Vérifier le résultat de la synchronisation"""
        try:
            if self.productos_window:
                # Vérifier si le stock a été mis à jour dans la fenêtre Productos
                # (Cette vérification dépend de l'implémentation de la fenêtre)
                self.status_label.setText("✅ Test automatique terminé - Vérifiez visuellement la synchronisation")
            else:
                self.status_label.setText("❌ Fenêtre Productos non ouverte")
                
        except Exception as e:
            self.status_label.setText(f"❌ Erreur vérification: {e}")
    
    def closeEvent(self, event):
        """Fermer toutes les fenêtres"""
        if self.stock_window:
            self.stock_window.close()
        if self.productos_window:
            self.productos_window.close()
        event.accept()

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Créer la fenêtre de test
    test_window = TestSyncWindow()
    test_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
