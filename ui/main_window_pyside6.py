#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale PySide6 native
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QGridLayout, QPushButton, QLabel,
                            QMenuBar, QStatusBar, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

from ui.productos_pyside6 import ProductosPySide6Window
from ui.organizacion_pyside6 import OrganizacionPySide6Window
from ui.stock_pyside6 import StockPySide6Window
from ui.facturas_pyside6 import FacturasPySide6Window
from ui.clientes_pyside6 import ClientesPySide6Window

class MainWindowPySide6(QMainWindow):
    def __init__(self):
        super().__init__()

        # Créer l'application PySide6 si elle n'existe pas
        self.app = QApplication.instance() or QApplication([])
        
        self.setWindowTitle("Facturación Fácil - PySide6")
        self.setGeometry(100, 100, 1200, 800)
        
        # Variables pour les fenêtres
        self.productos_window = None
        self.organizacion_window = None
        self.stock_window = None
        self.facturas_window = None
        self.clientes_window = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Titre
        title_label = QLabel("Facturación Fácil")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Layout des boutons
        buttons_layout = QGridLayout()
        
        # Boutons principaux
        self.create_main_buttons(buttons_layout)
        
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()
        
        # Barre de statut
        self.statusBar().showMessage("Prêt - PySide6")
        
    def create_main_buttons(self, layout):
        """Créer les boutons principaux"""
        # Bouton Productos
        btn_productos = QPushButton("Productos")
        btn_productos.setMinimumSize(200, 80)
        btn_productos.clicked.connect(self.open_productos)
        layout.addWidget(btn_productos, 0, 0)
        
        # Bouton Organización
        btn_organizacion = QPushButton("Organización")
        btn_organizacion.setMinimumSize(200, 80)
        btn_organizacion.clicked.connect(self.open_organizacion)
        layout.addWidget(btn_organizacion, 0, 1)
        
        # Bouton Stock
        btn_stock = QPushButton("Stock")
        btn_stock.setMinimumSize(200, 80)
        btn_stock.clicked.connect(self.open_stock)
        layout.addWidget(btn_stock, 1, 0)
        
        # Bouton Facturas
        btn_facturas = QPushButton("Facturas")
        btn_facturas.setMinimumSize(200, 80)
        btn_facturas.clicked.connect(self.open_facturas)
        layout.addWidget(btn_facturas, 1, 1)
        
        # Bouton Clientes
        btn_clientes = QPushButton("Clientes")
        btn_clientes.setMinimumSize(200, 80)
        btn_clientes.clicked.connect(self.open_clientes)
        layout.addWidget(btn_clientes, 2, 0)
        
    def open_productos(self):
        """Ouvrir la fenêtre des produits"""
        try:
            if self.productos_window is None:
                self.productos_window = ProductosPySide6Window()
            self.productos_window.show()
            self.productos_window.raise_()
            self.productos_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur ouverture Productos: {str(e)}")
            
    def open_organizacion(self):
        """Ouvrir la fenêtre d'organisation"""
        try:
            if self.organizacion_window is None:
                self.organizacion_window = OrganizacionPySide6Window()
            self.organizacion_window.show()
            self.organizacion_window.raise_()
            self.organizacion_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur ouverture Organización: {str(e)}")
            
    def open_stock(self):
        """Ouvrir la fenêtre de stock"""
        try:
            if self.stock_window is None:
                self.stock_window = StockPySide6Window()
            self.stock_window.show()
            self.stock_window.raise_()
            self.stock_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur ouverture Stock: {str(e)}")
            
    def open_facturas(self):
        """Ouvrir la fenêtre des factures"""
        try:
            if self.facturas_window is None:
                self.facturas_window = FacturasPySide6Window()
            self.facturas_window.show()
            self.facturas_window.raise_()
            self.facturas_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur ouverture Facturas: {str(e)}")
            
    def open_clientes(self):
        """Ouvrir la fenêtre des clients"""
        try:
            if self.clientes_window is None:
                self.clientes_window = ClientesPySide6Window()
            self.clientes_window.show()
            self.clientes_window.raise_()
            self.clientes_window.activateWindow()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur ouverture Clientes: {str(e)}")
    
    def run(self):
        """Lancer l'application"""
        self.show()
        return self.app.exec()
        
    def closeEvent(self, event):
        """Gérer la fermeture de l'application"""
        reply = QMessageBox.question(
            self, 'Fermer', 
            'Êtes-vous sûr de vouloir fermer l\'application?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Fermer toutes les fenêtres ouvertes
            if self.productos_window:
                self.productos_window.close()
            if self.organizacion_window:
                self.organizacion_window.close()
            if self.stock_window:
                self.stock_window.close()
            if self.facturas_window:
                self.facturas_window.close()
            if self.clientes_window:
                self.clientes_window.close()
                
            event.accept()
        else:
            event.ignore()
