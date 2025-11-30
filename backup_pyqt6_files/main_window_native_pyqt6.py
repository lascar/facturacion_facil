#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale PyQt6 native (sans couche d'abstraction)
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from utils.translations import get_text
from ui.productos import ProductosWindow
from ui.organizacion import OrganizacionWindow
from ui.stock import StockWindow
from ui.facturas import FacturasWindow
from ui.clientes import ClientesWindow
from ui.search_window import SearchWindow

class MainWindowNativePyQt6(QMainWindow):
    """Fenêtre principale PyQt6 native"""
    
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.setWindowTitle(get_text("app_title"))
        self.setGeometry(100, 100, 800, 600)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Variables pour fenêtres secondaires
        self.productos_window = None
        self.organizacion_window = None
        self.stock_window = None
        self.facturas_window = None
        self.clientes_window = None
        self.search_window = None
        
        # Créer l'interface
        self.create_widgets()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def create_widgets(self):
        """Crée les widgets de l'interface"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal vertical
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Titre
        title_label = QLabel(get_text("app_title"))
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Grille de boutons
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setSpacing(15)
        
        # Définir les boutons
        buttons = [
            (get_text("productos"), self.open_productos, 0, 0),
            (get_text("organizacion"), self.open_organizacion, 0, 1),
            (get_text("stock"), self.open_stock, 1, 0),
            (get_text("facturas"), self.open_facturas, 1, 1),
            (get_text("clientes"), self.open_clientes, 2, 0),
            ("Buscar", self.open_search, 2, 1)
        ]
        
        # Créer et placer les boutons
        for text, command, row, col in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setMinimumSize(150, 50)
            button.clicked.connect(command)
            buttons_layout.addWidget(button, row, col)
        
        # Ajouter la grille au layout principal
        main_layout.addWidget(buttons_widget)
        
        # Espaceur pour centrer verticalement
        main_layout.addStretch()
    
    def open_productos(self):
        """Ouvre la fenêtre de productos"""
        print("Ouverture fenêtre Productos")
        if self.productos_window is None or not hasattr(self.productos_window, 'window'):
            try:
                self.productos_window = ProductosWindow(self)
            except Exception as e:
                print(f"Erreur ouverture Productos: {e}")
        else:
            try:
                self.productos_window.window.raise_()
                self.productos_window.window.activateWindow()
            except:
                pass
    
    def open_organizacion(self):
        """Ouvre la fenêtre de organización"""
        print("Ouverture fenêtre Organización")
        if self.organizacion_window is None or not hasattr(self.organizacion_window, 'window'):
            try:
                self.organizacion_window = OrganizacionWindow(self)
            except Exception as e:
                print(f"Erreur ouverture Organización: {e}")
        else:
            try:
                self.organizacion_window.window.raise_()
                self.organizacion_window.window.activateWindow()
            except:
                pass
    
    def open_stock(self):
        """Ouvre la fenêtre de stock"""
        print("Ouverture fenêtre Stock")
        if self.stock_window is None or not hasattr(self.stock_window, 'window'):
            try:
                self.stock_window = StockWindow(self)
            except Exception as e:
                print(f"Erreur ouverture Stock: {e}")
        else:
            try:
                self.stock_window.window.raise_()
                self.stock_window.window.activateWindow()
            except:
                pass
    
    def open_facturas(self):
        """Ouvre la fenêtre de facturas"""
        print("Ouverture fenêtre Facturas")
        if self.facturas_window is None or not hasattr(self.facturas_window, 'window'):
            try:
                self.facturas_window = FacturasWindow(self)
            except Exception as e:
                print(f"Erreur ouverture Facturas: {e}")
        else:
            try:
                self.facturas_window.window.raise_()
                self.facturas_window.window.activateWindow()
            except:
                pass
    
    def open_clientes(self):
        """Ouvre la fenêtre de clientes"""
        print("Ouverture fenêtre Clientes")
        if self.clientes_window is None or not hasattr(self.clientes_window, 'window'):
            try:
                self.clientes_window = ClientesWindow(self)
            except Exception as e:
                print(f"Erreur ouverture Clientes: {e}")
        else:
            try:
                self.clientes_window.window.raise_()
                self.clientes_window.window.activateWindow()
            except:
                pass
    
    def open_search(self):
        """Ouvre la fenêtre de búsqueda"""
        print("Ouverture fenêtre Búsqueda")
        if self.search_window is None or not hasattr(self.search_window, 'window'):
            try:
                self.search_window = SearchWindow(self)
            except Exception as e:
                print(f"Erreur ouverture Búsqueda: {e}")
        else:
            try:
                self.search_window.window.raise_()
                self.search_window.window.activateWindow()
            except:
                pass

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre
    window = MainWindowNativePyQt6()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
