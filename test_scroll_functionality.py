#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du fonctionnement du scroll avec la molette de souris dans les fenêtres PyQt5
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import des fenêtres à tester
from ui.productos_pyqt5 import ProductosPyQt5Window
from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
from ui.facturas_pyqt5 import FacturasPyQt5Window
from ui.clientes_pyqt5 import ClientesPyQt5Window
from ui.stock_pyqt5 import StockPyQt5Window

class ScrollTestMainWindow(QMainWindow):
    """Fenêtre principale pour tester le scroll"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test du Scroll - Facturación Fácil")
        self.setGeometry(100, 100, 400, 300)
        
        # Variables pour les fenêtres
        self.productos_window = None
        self.organizacion_window = None
        self.facturas_window = None
        self.clientes_window = None
        self.stock_window = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("Test du Scroll avec la Molette de Souris")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Cliquez sur les boutons pour ouvrir les fenêtres.\n"
            "Testez le scroll avec la molette de souris dans chaque fenêtre.\n"
            "Les fenêtres avec beaucoup de contenu devraient être scrollables."
        )
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)
        
        # Boutons pour ouvrir les fenêtres
        self.create_test_buttons(layout)
        
    def create_test_buttons(self, layout):
        """Créer les boutons de test"""
        buttons_info = [
            ("🛍️ Productos (avec scroll)", self.open_productos),
            ("🏢 Organización (avec scroll)", self.open_organizacion),
            ("📄 Facturas (avec scroll)", self.open_facturas),
            ("👥 Clientes", self.open_clientes),
            ("📦 Stock", self.open_stock),
        ]
        
        for text, callback in buttons_info:
            button = QPushButton(text)
            button.clicked.connect(callback)
            button.setMinimumHeight(40)
            layout.addWidget(button)
            
    def open_productos(self):
        """Ouvrir la fenêtre des produits"""
        try:
            if self.productos_window is None:
                self.productos_window = ProductosPyQt5Window(self)
            self.productos_window.show()
            self.productos_window.raise_()
            self.productos_window.activateWindow()
            print("✅ Fenêtre Productos ouverte - Testez le scroll avec la molette !")
        except Exception as e:
            print(f"❌ Erreur ouverture Productos: {e}")
            
    def open_organizacion(self):
        """Ouvrir la fenêtre d'organisation"""
        try:
            if self.organizacion_window is None:
                self.organizacion_window = OrganizacionPyQt5Window(self)
            self.organizacion_window.show()
            self.organizacion_window.raise_()
            self.organizacion_window.activateWindow()
            print("✅ Fenêtre Organización ouverte - Testez le scroll avec la molette !")
        except Exception as e:
            print(f"❌ Erreur ouverture Organización: {e}")
            
    def open_facturas(self):
        """Ouvrir la fenêtre des factures"""
        try:
            if self.facturas_window is None:
                self.facturas_window = FacturasPyQt5Window(self)
            self.facturas_window.show()
            self.facturas_window.raise_()
            self.facturas_window.activateWindow()
            print("✅ Fenêtre Facturas ouverte - Testez le scroll avec la molette !")
        except Exception as e:
            print(f"❌ Erreur ouverture Facturas: {e}")
            
    def open_clientes(self):
        """Ouvrir la fenêtre des clients"""
        try:
            if self.clientes_window is None:
                self.clientes_window = ClientesPyQt5Window(self)
            self.clientes_window.show()
            self.clientes_window.raise_()
            self.clientes_window.activateWindow()
            print("✅ Fenêtre Clientes ouverte")
        except Exception as e:
            print(f"❌ Erreur ouverture Clientes: {e}")
            
    def open_stock(self):
        """Ouvrir la fenêtre du stock"""
        try:
            if self.stock_window is None:
                self.stock_window = StockPyQt5Window(self)
            self.stock_window.show()
            self.stock_window.raise_()
            self.stock_window.activateWindow()
            print("✅ Fenêtre Stock ouverte")
        except Exception as e:
            print(f"❌ Erreur ouverture Stock: {e}")

def main():
    """Fonction principale"""
    print("🧪 TEST DU SCROLL AVEC LA MOLETTE DE SOURIS")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre de test
    test_window = ScrollTestMainWindow()
    test_window.show()
    
    print("\n📋 INSTRUCTIONS DE TEST:")
    print("1. Cliquez sur les boutons pour ouvrir les fenêtres")
    print("2. Dans chaque fenêtre, utilisez la molette de souris pour scroller")
    print("3. Les fenêtres marquées 'avec scroll' devraient être scrollables")
    print("4. Vérifiez que le scroll est fluide et réactif")
    print("\n🎯 Fenêtres avec scroll activé:")
    print("   • Productos")
    print("   • Organización") 
    print("   • Facturas")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
