#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale migrée vers PyQt6 via la couche d'abstraction GUI
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui import set_gui_framework, create_gui_application, get_gui_factory
from utils.translations import get_text
from ui.productos import ProductosWindow
from ui.organizacion import OrganizacionWindow
from ui.stock import StockWindow
from ui.facturas import FacturasWindow
from ui.clientes import ClientesWindow
from ui.search_window import SearchWindow

class MainWindowPyQt6:
    def __init__(self):
        # Définir le framework PyQt6
        set_gui_framework('pyqt6')
        
        # Créer l'application et la factory
        self.app = create_gui_application()
        self.factory = self.app.gui_factory
        
        # Initialiser l'application
        self.app.initialize()
        self.root = self.app.main_window
        
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
        if self.productos_window is None or not hasattr(self.productos_window, 'window'):
            self.productos_window = ProductosWindow(self.root.get_native_widget())
        else:
            # Traer la ventana al frente si ya existe
            self.productos_window.window.lift()
            self.productos_window.window.focus_force()
    
    def open_organizacion(self):
        """Abre la ventana de organización"""
        if self.organizacion_window is None or not hasattr(self.organizacion_window, 'window'):
            self.organizacion_window = OrganizacionWindow(self.root.get_native_widget())
        else:
            self.organizacion_window.window.lift()
            self.organizacion_window.window.focus_force()
    
    def open_stock(self):
        """Abre la ventana de stock"""
        if self.stock_window is None or not hasattr(self.stock_window, 'window'):
            self.stock_window = StockWindow(self.root.get_native_widget())
        else:
            self.stock_window.window.lift()
            self.stock_window.window.focus_force()
    
    def open_facturas(self):
        """Abre la ventana de facturas"""
        if self.facturas_window is None or not hasattr(self.facturas_window, 'window'):
            self.facturas_window = FacturasWindow(self.root.get_native_widget())
        else:
            self.facturas_window.window.lift()
            self.facturas_window.window.focus_force()
    
    def open_clientes(self):
        """Abre la ventana de clientes"""
        if self.clientes_window is None or not hasattr(self.clientes_window, 'window'):
            self.clientes_window = ClientesWindow(self.root.get_native_widget())
        else:
            self.clientes_window.window.lift()
            self.clientes_window.window.focus_force()
    
    def open_search(self):
        """Abre la ventana de búsqueda"""
        if self.search_window is None or not hasattr(self.search_window, 'window'):
            self.search_window = SearchWindow(self.root.get_native_widget())
        else:
            self.search_window.window.lift()
            self.search_window.window.focus_force()
    
    def run(self):
        """Lance l'application"""
        return self.app.run()

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
