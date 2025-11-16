#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fenêtre principale PyQt6 native (solution au problème de layout)
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from utils.translations import get_text
# Nouvelles fenêtres PyQt6 natives
from ui.productos_pyqt6 import ProductosPyQt6Window
from ui.stock_pyqt6 import StockPyQt6Window
from ui.facturas_pyqt6 import FacturasPyQt6Window
from ui.clientes_pyqt6 import ClientesPyQt6Window
from ui.organizacion_pyqt6 import OrganizacionPyQt6Window
from ui.search_pyqt6 import SearchPyQt6Window

# Anciennes fenêtres CustomTkinter (pour compatibilité temporaire)
# from ui.productos import ProductosWindow
# from ui.organizacion import OrganizacionWindow
# from ui.stock import StockWindow
# from ui.facturas import FacturasWindow
# from ui.clientes import ClientesWindow
# from ui.search_window import SearchWindow
# from ui.pyqt6_window_adapter import create_adapter_for_pyqt6_parent

class MainWindow(QMainWindow):
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

    def force_window_visible(self, window, window_name):
        """Force une fenêtre CustomTkinter à être visible"""
        try:
            if hasattr(window, 'window'):
                # Séquence complète pour forcer l'affichage
                window.window.deiconify()  # S'assurer qu'elle n'est pas minimisée
                window.window.state('normal')  # État normal
                window.window.lift()       # Amener au premier plan
                window.window.focus_force() # Forcer le focus
                window.window.grab_set()   # Capturer les événements

                # Forcer temporairement au-dessus de tout
                window.window.attributes('-topmost', True)
                window.window.update()     # Forcer la mise à jour

                # Retirer le topmost après un délai
                window.window.after(200, lambda: self._remove_topmost(window.window))

                # Centrer la fenêtre si possible
                try:
                    window.window.geometry("800x600+100+100")
                except:
                    pass

                print(f"✅ Fenêtre {window_name} affichée et mise au premier plan")
                return True
        except Exception as e:
            print(f"Erreur affichage {window_name}: {e}")
            return False
        return False

    def _remove_topmost(self, window):
        """Retire l'attribut topmost d'une fenêtre"""
        try:
            window.attributes('-topmost', False)
        except:
            pass

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
        """Ouvre la fenêtre de productos PyQt6"""
        print("Ouverture fenêtre Productos PyQt6")
        if self.productos_window is None:
            try:
                # Créer la fenêtre PyQt6 native
                self.productos_window = ProductosPyQt6Window(self)
                self.productos_window.show()
                print("✅ Fenêtre Productos PyQt6 ouverte")

            except Exception as e:
                print(f"Erreur ouverture Productos PyQt6: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Réactiver la fenêtre existante
            self.productos_window.show()
            self.productos_window.raise_()
            self.productos_window.activateWindow()
            print("✅ Fenêtre Productos PyQt6 réactivée")

    def open_organizacion(self):
        """Ouvre la fenêtre de organización PyQt6"""
        print("Ouverture fenêtre Organización PyQt6")
        if self.organizacion_window is None:
            try:
                # Créer la fenêtre PyQt6 native
                self.organizacion_window = OrganizacionPyQt6Window(self)
                self.organizacion_window.show()
                print("✅ Fenêtre Organización PyQt6 ouverte")

            except Exception as e:
                print(f"Erreur ouverture Organización PyQt6: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Réactiver la fenêtre existante
            self.organizacion_window.show()
            self.organizacion_window.raise_()
            self.organizacion_window.activateWindow()
            print("✅ Fenêtre Organización PyQt6 réactivée")

    def open_stock(self):
        """Ouvre la fenêtre de stock PyQt6"""
        print("Ouverture fenêtre Stock PyQt6")
        if self.stock_window is None:
            try:
                # Créer la fenêtre PyQt6 native
                self.stock_window = StockPyQt6Window(self)
                self.stock_window.show()
                print("✅ Fenêtre Stock PyQt6 ouverte")

            except Exception as e:
                print(f"Erreur ouverture Stock PyQt6: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Réactiver la fenêtre existante
            self.stock_window.show()
            self.stock_window.raise_()
            self.stock_window.activateWindow()
            print("✅ Fenêtre Stock PyQt6 réactivée")

    def open_facturas(self):
        """Ouvre la fenêtre de facturas PyQt6"""
        print("Ouverture fenêtre Facturas PyQt6")
        if self.facturas_window is None:
            try:
                # Créer la fenêtre PyQt6 native
                self.facturas_window = FacturasPyQt6Window(self)
                self.facturas_window.show()
                print("✅ Fenêtre Facturas PyQt6 ouverte")

            except Exception as e:
                print(f"Erreur ouverture Facturas PyQt6: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Réactiver la fenêtre existante
            self.facturas_window.show()
            self.facturas_window.raise_()
            self.facturas_window.activateWindow()
            print("✅ Fenêtre Facturas PyQt6 réactivée")

    def open_clientes(self):
        """Ouvre la fenêtre de clientes PyQt6"""
        print("Ouverture fenêtre Clientes PyQt6")
        if self.clientes_window is None:
            try:
                # Créer la fenêtre PyQt6 native
                self.clientes_window = ClientesPyQt6Window(self)
                self.clientes_window.show()
                print("✅ Fenêtre Clientes PyQt6 ouverte")

            except Exception as e:
                print(f"Erreur ouverture Clientes PyQt6: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Réactiver la fenêtre existante
            self.clientes_window.show()
            self.clientes_window.raise_()
            self.clientes_window.activateWindow()
            print("✅ Fenêtre Clientes PyQt6 réactivée")

    def open_search(self):
        """Ouvre la fenêtre de búsqueda PyQt6"""
        print("Ouverture fenêtre Búsqueda PyQt6")
        if self.search_window is None:
            try:
                # Créer la fenêtre PyQt6 native
                self.search_window = SearchPyQt6Window(self)
                self.search_window.show()
                print("✅ Fenêtre Búsqueda PyQt6 ouverte")

            except Exception as e:
                print(f"Erreur ouverture Búsqueda PyQt6: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Réactiver la fenêtre existante
            self.search_window.show()
            self.search_window.raise_()
            self.search_window.activateWindow()
            print("✅ Fenêtre Búsqueda PyQt6 réactivée")

    def show(self):
        """Affiche la fenêtre"""
        super().show()

    def run(self):
        """Lance l'application (pour compatibilité)"""
        self.show()
        return QApplication.instance().exec()

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
