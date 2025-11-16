#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration de migration de la fenêtre principale vers PyQt6
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework, create_gui_application, get_gui_factory
from utils.translations import get_text

class MainWindowPyQt6:
    """Version PyQt6 de la fenêtre principale"""
    
    def __init__(self):
        # Définir le framework PyQt6
        set_gui_framework('pyqt6')

        # Créer l'application
        self.app = create_gui_application()
        self.factory = self.app.gui_factory
        
        # Initialiser l'application
        self.app.initialize()
        self.root = self.app.main_window
        
        # Configurer la fenêtre
        self.root.get_native_widget().setWindowTitle(get_text("app_title"))
        self.root.get_native_widget().resize(800, 600)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Créer l'interface
        self.create_widgets()
        
        # Variables pour fenêtres secondaires
        self.productos_window = None
        self.organizacion_window = None
        self.stock_window = None
        self.facturas_window = None
        self.clientes_window = None
        self.search_window = None
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        window = self.root.get_native_widget()
        
        # Obtenir les dimensions de l'écran
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        
        # Calculer la position centrale
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        
        # Déplacer la fenêtre
        window.move(x, y)
    
    def create_widgets(self):
        """Crée les widgets de la fenêtre principale"""
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
        
        # Frame pour les boutons
        buttons_frame = self.factory.create_frame(main_frame)
        buttons_frame.pack()
        
        # Créer les boutons principaux
        self.create_main_buttons(buttons_frame)
    
    def create_main_buttons(self, parent):
        """Crée les boutons principaux"""
        buttons = [
            (get_text("productos"), self.open_productos),
            (get_text("organizacion"), self.open_organizacion),
            (get_text("stock"), self.open_stock),
            (get_text("facturas"), self.open_facturas),
            (get_text("clientes"), self.open_clientes),
            ("Buscar", self.open_search)
        ]
        
        for text, command in buttons:
            button = self.factory.create_button(
                parent,
                text=text,
                command=command
            )
            button.configure(font=("Arial", 14))
            button.pack()
    
    def open_productos(self):
        """Abre la ventana de productos"""
        print("Abriendo ventana de productos (PyQt6)")
        self.factory.show_message("info", "Productos", "Funcionalidad de productos (demo PyQt6)")
    
    def open_organizacion(self):
        """Abre la ventana de organización"""
        print("Abriendo ventana de organización (PyQt6)")
        self.factory.show_message("info", "Organización", "Funcionalidad de organización (demo PyQt6)")
    
    def open_stock(self):
        """Abre la ventana de stock"""
        print("Abriendo ventana de stock (PyQt6)")
        self.factory.show_message("info", "Stock", "Funcionalidad de stock (demo PyQt6)")
    
    def open_facturas(self):
        """Abre la ventana de facturas"""
        print("Abriendo ventana de facturas (PyQt6)")
        self.factory.show_message("info", "Facturas", "Funcionalidad de facturas (demo PyQt6)")
    
    def open_clientes(self):
        """Abre la ventana de clientes"""
        print("Abriendo ventana de clientes (PyQt6)")
        self.factory.show_message("info", "Clientes", "Funcionalidad de clientes (demo PyQt6)")
    
    def open_search(self):
        """Abre la ventana de búsqueda"""
        print("Abriendo ventana de búsqueda (PyQt6)")
        self.factory.show_message("info", "Búsqueda", "Funcionalidad de búsqueda (demo PyQt6)")
    
    def run(self):
        """Lance l'application"""
        print("Lancement de l'application PyQt6...")
        print("Fermer la fenêtre pour terminer.")
        return self.app.run()

def main():
    """Fonction principale"""
    try:
        print("=== Démonstration Migration PyQt6 ===")
        print("Création de la fenêtre principale avec PyQt6...")
        
        # Créer et lancer l'application
        app = MainWindowPyQt6()
        return app.run()
        
    except ImportError as e:
        print(f"Erreur: PyQt6 n'est pas installé - {e}")
        print("Installez PyQt6 avec: pip install PyQt6")
        return 1
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
