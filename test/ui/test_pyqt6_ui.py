#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests UI spécifiques à PyQt6
"""

import pytest
import sys
import os

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from gui import set_gui_framework, get_gui_factory

class TestPyQt6UI:
    """Tests UI pour PyQt6"""
    
    def setup_method(self):
        """Setup pour chaque test"""
        set_gui_framework('pyqt6')
        self.factory = get_gui_factory()
    
    def test_window_creation(self):
        """Test création de fenêtre PyQt6"""
        window = self.factory.create_window("Test PyQt6", "800x600")
        
        assert window is not None
        assert hasattr(window, 'get_native_widget')
        
        native_window = window.get_native_widget()
        assert native_window is not None
        assert native_window.windowTitle() == "Test PyQt6"
        assert native_window.width() == 800
        assert native_window.height() == 600
    
    def test_frame_creation(self):
        """Test création de frame PyQt6"""
        window = self.factory.create_window("Test", "400x300")
        frame = self.factory.create_frame(window)
        
        assert frame is not None
        assert hasattr(frame, 'pack')
        assert hasattr(frame, 'grid')
        
        # Test empaquetage
        frame.pack()
    
    def test_label_creation_and_config(self):
        """Test création et configuration de label PyQt6"""
        window = self.factory.create_window("Test", "400x300")
        frame = self.factory.create_frame(window)
        
        label = self.factory.create_label(frame, text="Test Label")
        assert label is not None
        
        native_label = label.get_native_widget()
        assert native_label.text() == "Test Label"
        
        # Test configuration
        label.configure(text="Updated Label")
        assert native_label.text() == "Updated Label"
        
        # Test avec font
        label.configure(font=("Arial", 14))
        font = native_label.font()
        assert font.family() == "Arial"
        assert font.pointSize() == 14
    
    def test_button_creation_and_command(self):
        """Test création de bouton PyQt6 avec commande"""
        window = self.factory.create_window("Test", "400x300")
        frame = self.factory.create_frame(window)
        
        clicked = False
        def on_click():
            nonlocal clicked
            clicked = True
        
        button = self.factory.create_button(frame, text="Test Button", command=on_click)
        assert button is not None
        
        native_button = button.get_native_widget()
        assert native_button.text() == "Test Button"
        
        # Simuler un clic
        native_button.click()
        assert clicked == True
    
    def test_entry_creation(self):
        """Test création d'entry PyQt6"""
        window = self.factory.create_window("Test", "400x300")
        frame = self.factory.create_frame(window)
        
        entry = self.factory.create_entry(frame)
        assert entry is not None
        
        native_entry = entry.get_native_widget()
        
        # Test saisie de texte
        native_entry.setText("Test Text")
        assert native_entry.text() == "Test Text"
        
        # Test effacement
        native_entry.clear()
        assert native_entry.text() == ""
    
    def test_treeview_creation(self):
        """Test création de TreeView PyQt6"""
        window = self.factory.create_window("Test", "400x300")
        frame = self.factory.create_frame(window)
        
        columns = ["Name", "Age", "City"]
        treeview = self.factory.create_treeview(frame, columns=columns)
        assert treeview is not None
        
        native_tree = treeview.get_native_widget()
        assert native_tree.columnCount() == len(columns)
        
        # Vérifier les en-têtes
        for i, col in enumerate(columns):
            header_text = native_tree.headerItem().text(i)
            assert header_text == col
    
    def test_combobox_creation(self):
        """Test création de Combobox PyQt6"""
        window = self.factory.create_window("Test", "400x300")
        frame = self.factory.create_frame(window)
        
        values = ["Option 1", "Option 2", "Option 3"]
        combo = self.factory.create_combobox(frame, values=values)
        assert combo is not None
        
        native_combo = combo.get_native_widget()
        assert native_combo.count() == len(values)
        
        # Vérifier les valeurs
        for i, value in enumerate(values):
            assert native_combo.itemText(i) == value
    
    def test_grid_layout(self):
        """Test du layout en grille PyQt6"""
        window = self.factory.create_window("Test", "400x300")
        frame = self.factory.create_frame(window)
        
        # Créer des boutons en grille
        buttons = []
        for i in range(2):
            for j in range(2):
                button = self.factory.create_button(frame, text=f"Button {i},{j}")
                button.grid(row=i, column=j)
                buttons.append(button)
        
        frame.pack()
        
        # Vérifier que tous les boutons ont été créés
        assert len(buttons) == 4
        for button in buttons:
            assert button is not None
    
    def test_scrollable_frame(self):
        """Test du frame scrollable PyQt6"""
        window = self.factory.create_window("Test", "400x300")
        
        scrollable = self.factory.create_scrollable_frame(window)
        assert scrollable is not None
        
        # Ajouter du contenu
        for i in range(10):
            label = self.factory.create_label(scrollable, text=f"Label {i}")
            label.pack()
        
        scrollable.pack()
    
    def test_message_dialogs(self):
        """Test des boîtes de dialogue PyQt6"""
        # Note: Ces tests vérifient seulement que les méthodes existent
        # et sont appelables, sans afficher les dialogues
        
        assert hasattr(self.factory, 'show_message')
        assert callable(self.factory.show_message)
        
        assert hasattr(self.factory, 'ask_file')
        assert callable(self.factory.ask_file)
        
        assert hasattr(self.factory, 'ask_directory')
        assert callable(self.factory.ask_directory)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
