#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug visuel de la fenêtre principale PyQt6
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework, get_gui_factory
from utils.translations import get_text

def create_simple_test_window():
    """Crée une fenêtre de test simple avec tous les boutons"""
    print("=== Création fenêtre de test simple ===")
    
    # Définir PyQt6
    set_gui_framework('pyqt6')
    factory = get_gui_factory()
    
    # Créer la fenêtre
    window = factory.create_window("Test Debug - Facturación Fácil", "600x500")
    
    # Obtenir le widget natif pour debug
    native_window = window.get_native_widget()
    print(f"Fenêtre native: {type(native_window)}")
    
    # Créer le contenu avec layout vertical simple
    main_frame = factory.create_frame(window)
    print(f"Frame principal créé: {type(main_frame.get_native_widget())}")
    
    # Titre
    title = factory.create_label(main_frame, text="DEBUG - Tous les boutons")
    title.configure(font=("Arial", 16))
    title.pack()
    print("✓ Titre ajouté")
    
    # Créer tous les boutons un par un avec pack simple
    buttons_info = [
        ("Productos", lambda: print("Productos clicked")),
        ("Organización", lambda: print("Organización clicked")),
        ("Stock", lambda: print("Stock clicked")),
        ("Facturas", lambda: print("Facturas clicked")),
        ("Clientes", lambda: print("Clientes clicked")),
        ("Buscar", lambda: print("Buscar clicked"))
    ]
    
    print(f"\nCréation de {len(buttons_info)} boutons...")
    
    for i, (text, command) in enumerate(buttons_info):
        print(f"Création bouton {i+1}: {text}")
        
        button = factory.create_button(main_frame, text=text, command=command)
        button.configure(font=("Arial", 12))
        button.pack()
        
        # Debug du widget natif
        native_button = button.get_native_widget()
        print(f"  - Widget natif: {type(native_button)}")
        print(f"  - Texte: {native_button.text()}")
        print(f"  - Visible: {native_button.isVisible()}")
        print(f"  - Taille: {native_button.size().width()}x{native_button.size().height()}")
    
    # Empaqueter le frame principal
    main_frame.pack()
    print("✓ Frame principal empaqueté")
    
    # Afficher la fenêtre
    native_window.show()
    print("✓ Fenêtre affichée")
    
    return window, factory._app

def create_grid_test_window():
    """Crée une fenêtre de test avec layout en grille"""
    print("\n=== Création fenêtre de test grille ===")
    
    set_gui_framework('pyqt6')
    factory = get_gui_factory()
    
    # Créer la fenêtre
    window = factory.create_window("Test Grille - Facturación Fácil", "600x400")
    
    # Frame principal
    main_frame = factory.create_frame(window)
    
    # Titre
    title = factory.create_label(main_frame, text="TEST GRILLE - Layout par rangées")
    title.configure(font=("Arial", 16))
    title.pack()
    
    # Créer les rangées comme dans la version corrigée
    buttons_data = [
        [("Productos", lambda: print("Productos")), ("Organización", lambda: print("Organización"))],
        [("Stock", lambda: print("Stock")), ("Facturas", lambda: print("Facturas"))],
        [("Clientes", lambda: print("Clientes")), ("Buscar", lambda: print("Buscar"))]
    ]
    
    print(f"Création de {len(buttons_data)} rangées...")
    
    for row_idx, row_buttons in enumerate(buttons_data):
        print(f"Rangée {row_idx + 1}:")
        
        # Créer frame horizontal pour cette rangée
        row_frame = factory.create_frame(main_frame, layout='horizontal')
        
        for text, command in row_buttons:
            print(f"  - Bouton: {text}")
            button = factory.create_button(row_frame, text=text, command=command)
            button.configure(font=("Arial", 12))
            button.pack()
        
        row_frame.pack()
        print(f"  ✓ Rangée {row_idx + 1} empaquetée")
    
    main_frame.pack()
    
    # Afficher
    window.get_native_widget().show()
    print("✓ Fenêtre grille affichée")
    
    return window, factory._app

def main():
    """Fonction principale de debug"""
    print("🔍 DEBUG VISUEL DE LA FENÊTRE PRINCIPALE PYQT6")
    print("="*60)
    
    try:
        # Test 1: Fenêtre simple avec tous les boutons en vertical
        print("TEST 1: Layout vertical simple")
        window1, app = create_simple_test_window()
        
        print("\n" + "="*60)
        print("TEST 2: Layout par rangées (comme dans l'app)")
        window2, _ = create_grid_test_window()
        
        print("\n" + "="*60)
        print("🖥️  DEUX FENÊTRES DE TEST OUVERTES:")
        print("1. Fenêtre simple (layout vertical)")
        print("2. Fenêtre grille (layout par rangées)")
        print("\n💡 Vérifiez visuellement quels boutons sont visibles")
        print("🔄 Fermez les fenêtres pour terminer le test")
        
        # Lancer la boucle d'événements
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
