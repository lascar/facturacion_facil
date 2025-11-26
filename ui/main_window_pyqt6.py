#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale PyQt6 native
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QGridLayout, QPushButton, QLabel,
                            QMenuBar, QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from ui.productos_pyqt6 import ProductosPyQt6Window
from ui.organizacion_pyqt6 import OrganizacionPyQt6Window
from ui.stock_pyqt6 import StockPyQt6Window
from ui.facturas_pyqt6 import FacturasPyQt6Window
from ui.clientes_pyqt6 import ClientesPyQt6Window

class MainWindowPyQt6(QMainWindow):
    def __init__(self):
        super().__init__()

        # Créer l'application PyQt6 si elle n'existe pas
        self.app = QApplication.instance() or QApplication([])

        # Configurer la fenêtre principale
        self.setWindowTitle("Facturación Fácil")
        self.setGeometry(100, 100, 800, 600)
        self.center_window()

        # Variables pour les fenêtres secondaires
        self.productos_window = None
        self.organizacion_window = None
        self.stock_window = None
        self.facturas_window = None
        self.clientes_window = None

        # Créer l'interface
        self.create_widgets()
        self.create_menu()
        self.create_status_bar()

    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        screen = QApplication.primaryScreen().geometry()

        # Calculer la position centrale
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2

        self.move(x, y)

    def create_widgets(self):
        """Crée les widgets de l'interface principale"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Titre
        title_label = QLabel("Facturación Fácil")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Sous-titre
        subtitle_label = QLabel("Sistema de Gestión Comercial")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        main_layout.addWidget(subtitle_label)

        # Créer la grille de boutons
        self.create_button_grid(main_layout)
    
    def create_button_grid(self, main_layout):
        """Crée la grille de boutons"""
        # Container pour les boutons
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setSpacing(15)

        # Configuration des boutons
        buttons = [
            ("📦 Productos", self.open_productos, 0, 0, "Gestión de productos y catálogos"),
            ("👥 Clientes", self.open_clientes, 0, 1, "Gestión de clientes y contactos"),
            ("📋 Stock", self.open_stock, 1, 0, "Control de inventario y stock"),
            ("🧾 Facturas", self.open_facturas, 1, 1, "Creación y gestión de facturas"),
            ("🏢 Organización", self.open_organizacion, 2, 0, "Configuración de la empresa"),
        ]

        for text, command, row, col, tooltip in buttons:
            button = QPushButton(text)
            button.clicked.connect(command)
            button.setMinimumSize(200, 80)
            button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            button.setToolTip(tooltip)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
            """)
            buttons_layout.addWidget(button, row, col)

        main_layout.addWidget(buttons_widget)
        main_layout.addStretch()  # Espacio flexible al final

    def create_menu(self):
        """Crée la barre de menu"""
        menubar = self.menuBar()

        # Menu Archivo
        file_menu = menubar.addMenu('&Archivo')

        # Menu Gestión
        management_menu = menubar.addMenu('&Gestión')
        management_menu.addAction('&Productos', self.open_productos)
        management_menu.addAction('&Organización', self.open_organizacion)
        management_menu.addAction('&Clientes', self.open_clientes)
        management_menu.addAction('&Stock', self.open_stock)
        management_menu.addAction('&Facturas', self.open_facturas)

        # Menu Ayuda
        help_menu = menubar.addMenu('&Ayuda')
        help_menu.addAction('&Acerca de', self.show_about)

    def create_status_bar(self):
        """Crée la barre de statut"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Listo")

    def open_productos(self):
        """Abre la ventana de productos"""
        if self.productos_window is None or not self.productos_window.isVisible():
            self.productos_window = ProductosPyQt6Window(self)
            self.productos_window.show()
        else:
            # Traer la ventana al frente si ya existe
            self.productos_window.raise_()
            self.productos_window.activateWindow()

    def open_organizacion(self):
        """Abre la ventana de configuración de la organización"""
        if self.organizacion_window is None or not self.organizacion_window.isVisible():
            self.organizacion_window = OrganizacionPyQt6Window(self)
            self.organizacion_window.show()
        else:
            # Traer la ventana al frente si ya existe
            self.organizacion_window.raise_()
            self.organizacion_window.activateWindow()

    def open_stock(self):
        """Abre la ventana de stock"""
        if self.stock_window is None or not self.stock_window.isVisible():
            self.stock_window = StockPyQt6Window(self)
            self.stock_window.show()
        else:
            self.stock_window.raise_()
            self.stock_window.activateWindow()

    def open_facturas(self):
        """Abre la ventana de gestión de facturas"""
        if self.facturas_window is None or not self.facturas_window.isVisible():
            self.facturas_window = FacturasPyQt6Window(self)
            self.facturas_window.show()
        else:
            self.facturas_window.raise_()
            self.facturas_window.activateWindow()

    def open_clientes(self):
        """Abre la ventana de clientes"""
        if self.clientes_window is None or not self.clientes_window.isVisible():
            self.clientes_window = ClientesPyQt6Window(self)
            self.clientes_window.show()
        else:
            self.clientes_window.raise_()
            self.clientes_window.activateWindow()

    def show_about(self):
        """Muestra información sobre la aplicación"""
        QMessageBox.about(self, "Acerca de",
                         "Facturación Fácil v1.0\n\n"
                         "Sistema de gestión comercial\n"
                         "Desarrollado con PyQt6")

    def run(self):
        """Lance l'application"""
        # Afficher la fenêtre
        self.show()

        # Lancer la boucle d'événements
        return self.app.exec()

def main():
    """Fonction principale"""
    try:
        app = MainWindowPyQt6()
        return app.run()
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
