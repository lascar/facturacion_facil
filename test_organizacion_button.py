#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que le bouton Organización est présent et fonctionne
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework
set_gui_framework('pyqt6')

from PyQt6.QtWidgets import QApplication
from ui.main_window_pyqt6 import MainWindowPyQt6
from database.database import db

def test_organizacion_button():
    """Test que le bouton Organización est présent et fonctionne"""
    
    # Initialiser la base de données
    db.init_database()
    
    # Créer l'application Qt
    app = QApplication.instance() or QApplication([])
    
    # Créer la fenêtre principale
    main_window = MainWindowPyQt6()
    
    # Vérifier que la fenêtre a la méthode open_organizacion
    assert hasattr(main_window, 'open_organizacion'), "La méthode open_organizacion n'existe pas"
    
    # Vérifier que la variable organizacion_window existe
    assert hasattr(main_window, 'organizacion_window'), "La variable organizacion_window n'existe pas"
    
    # Afficher la fenêtre
    main_window.show()
    
    # Chercher le bouton Organización dans les widgets
    central_widget = main_window.centralWidget()
    buttons_found = []
    
    def find_buttons(widget):
        """Trouve tous les boutons dans le widget et ses enfants"""
        from PyQt6.QtWidgets import QPushButton
        if isinstance(widget, QPushButton):
            buttons_found.append(widget.text())
        
        for child in widget.findChildren(QPushButton):
            buttons_found.append(child.text())
    
    find_buttons(central_widget)
    
    print("Boutons trouvés:", buttons_found)
    
    # Vérifier que le bouton Organización est présent
    organizacion_found = any("Organización" in btn for btn in buttons_found)
    assert organizacion_found, f"Bouton Organización non trouvé. Boutons disponibles: {buttons_found}"
    
    print("✅ Test réussi : Le bouton Organización est présent !")
    
    # Tester l'ouverture de la fenêtre d'organisation
    try:
        main_window.open_organizacion()
        print("✅ Test réussi : La méthode open_organizacion fonctionne !")
        
        # Vérifier que la fenêtre d'organisation a été créée
        assert main_window.organizacion_window is not None, "La fenêtre d'organisation n'a pas été créée"
        print("✅ Test réussi : La fenêtre d'organisation a été créée !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ouverture de la fenêtre d'organisation: {e}")
        raise
    
    # Fermer l'application
    app.quit()
    
    return True

if __name__ == "__main__":
    try:
        test_organizacion_button()
        print("\n🎉 Tous les tests sont passés avec succès !")
        print("Le bouton pour l'entreprise/organisation est maintenant présent et fonctionnel.")
    except Exception as e:
        print(f"\n❌ Test échoué: {e}")
        sys.exit(1)
