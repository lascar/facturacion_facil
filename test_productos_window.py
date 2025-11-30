#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test direct de la fenêtre des produits
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.productos_pyqt6 import ProductosPyQt6Window
from database.database import db

def main():
    print("=== Test de la fenêtre Productos ===")
    
    # Initialiser la base de données
    print("Initialisation de la base de données...")
    db.init_database()
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    # Créer et afficher la fenêtre
    print("Création de la fenêtre Productos...")
    window = ProductosPyQt6Window()
    window.show()
    
    print("Fenêtre affichée. Vérifiez les boutons...")
    
    # Lancer l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
