#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale migrée vers PyQt6 via la couche d'abstraction GUI
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui import set_gui_framework, get_gui_factory
from utils.translations import get_text
from ui.productos_pyqt6 import ProductosPyQt6Window
from ui.stock_pyqt6 import StockPyQt6Window
from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
from ui.clientes_pyqt6 import ClientesPyQt6Window

class MainWindowPyQt6:
    def __init__(self):
        # Définir le framework PyQt6
        set_gui_framework('pyqt6')
        
        # Créer l'application PyQt6
        from PyQt6.QtWidgets import QApplication
        self.app = QApplication.instance() or QApplication([])
        self.factory = get_gui_factory()

        # Créer la fenêtre principale
        self.root = self.factory.create_window("Facturación Fácil", "800x600")
        
        # Configurer la fenêtre
        native_window = self.root.get_native_widget()
        native_window.setWindowTitle(get_text("app_title"))
        native_window.resize(800, 600)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Créer l'interface
        self.create_widgets()
        
        # Variables pour ventanas secundarias
        self.productos_window = None
        self.organizacion_window = None
        self.stock_window = None
        self.facturas_window = None
        self.clientes_window = None
        self.search_window = None
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        from PyQt6.QtWidgets import QApplication
        
        window = self.root.get_native_widget()
        screen = QApplication.primaryScreen().geometry()
        
        # Calculer la position centrale
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        
        window.move(x, y)
    
    def create_widgets(self):
        """Crée les widgets de l'interface principale"""
        # Frame principal
        main_frame = self.factory.create_frame(self.root)
        main_frame.pack()
        
        # Titre
        title_label = self.factory.create_label(
            main_frame,
            text=get_text("app_title")
        )
        title_label.configure(font=("Arial", 24))
        title_label.pack()
        
        # Frame pour les boutons avec grid layout
        buttons_frame = self.factory.create_frame(main_frame)
        buttons_frame.pack()
        
        # Créer les boutons en grille
        self.create_button_grid(buttons_frame)
    
    def create_button_grid(self, parent):
        """Crée la grille de boutons"""
        buttons = [
            (get_text("productos"), self.open_productos, 0, 0),
            (get_text("organizacion"), self.open_organizacion, 0, 1),
            (get_text("stock"), self.open_stock, 1, 0),
            (get_text("facturas"), self.open_facturas, 1, 1),
            (get_text("clientes"), self.open_clientes, 2, 0),
            ("Buscar", self.open_search, 2, 1)
        ]
        
        for text, command, row, col in buttons:
            button = self.factory.create_button(
                parent,
                text=text,
                command=command
            )
            button.configure(font=("Arial", 14))
            button.grid(row=row, column=col)
    
    def open_productos(self):
        """Abre la ventana de productos"""
        if self.productos_window is None or not self.productos_window.isVisible():
            self.productos_window = ProductosPyQt6Window(self.root.get_native_widget())
            self.productos_window.show()
        else:
            # Traer la ventana al frente si ya existe
            self.productos_window.raise_()
            self.productos_window.activateWindow()

    def open_organizacion(self):
        """Abre la ventana de organización (no implementada)"""
        self.factory.show_message("info", "Organización", "Funcionalidad de organización no implementada en PyQt6")

    def open_stock(self):
        """Abre la ventana de stock"""
        if self.stock_window is None or not self.stock_window.isVisible():
            self.stock_window = StockPyQt6Window(self.root.get_native_widget())
            self.stock_window.show()
        else:
            self.stock_window.raise_()
            self.stock_window.activateWindow()

    def open_facturas(self):
        """Abre la ventana de facturas"""
        if self.facturas_window is None or not self.facturas_window.isVisible():
            self.facturas_window = FacturaEditorPyQt6Window(self.root.get_native_widget())
            self.facturas_window.show()
        else:
            self.facturas_window.raise_()
            self.facturas_window.activateWindow()

    def open_clientes(self):
        """Abre la ventana de clientes"""
        if self.clientes_window is None or not self.clientes_window.isVisible():
            self.clientes_window = ClientesPyQt6Window(self.root.get_native_widget())
            self.clientes_window.show()
        else:
            self.clientes_window.raise_()
            self.clientes_window.activateWindow()

    def open_search(self):
        """Abre la ventana de búsqueda (no implementada)"""
        self.factory.show_message("info", "Búsqueda", "Funcionalidad de búsqueda no implementada en PyQt6")
    
    def run(self):
        """Lance l'application"""
        # Afficher la fenêtre
        native_window = self.root.get_native_widget()
        native_window.show()

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
