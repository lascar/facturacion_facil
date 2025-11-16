#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests d'intégration spécifiques à PyQt6
"""

import pytest
import sys
import os

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

class TestPyQt6Integration:
    """Tests d'intégration pour PyQt6"""
    
    def test_pyqt6_framework_loading(self):
        """Test du chargement spécifique de PyQt6"""
        from gui import set_gui_framework, get_gui_factory, get_gui_manager
        
        print("🧪 Test chargement PyQt6")
        print("=" * 40)
        
        # Définir PyQt6
        set_gui_framework('pyqt6')
        
        # Vérifier le manager
        manager = get_gui_manager()
        assert manager.get_current_framework() == 'pyqt6'
        print("✅ Framework PyQt6 défini")
        
        # Vérifier la factory
        factory = get_gui_factory()
        assert 'PyQt6' in type(factory).__name__
        print(f"✅ Factory PyQt6: {type(factory).__name__}")
        
        # Vérifier que PyQt6 est disponible
        try:
            import PyQt6
            print("✅ PyQt6 module disponible")
        except ImportError:
            pytest.skip("PyQt6 non installé")
    
    def test_pyqt6_widgets_creation(self):
        """Test de création de widgets PyQt6"""
        from gui import set_gui_framework, get_gui_factory
        
        print("\n🧪 Test création widgets PyQt6")
        print("=" * 40)
        
        set_gui_framework('pyqt6')
        factory = get_gui_factory()
        
        # Créer une fenêtre
        window = factory.create_window("Test PyQt6", "600x400")
        assert window is not None
        assert hasattr(window, 'get_native_widget')
        print("✅ Fenêtre PyQt6 créée")
        
        # Vérifier que c'est bien un widget PyQt6
        native_widget = window.get_native_widget()
        assert 'PyQt6' in str(type(native_widget))
        print(f"✅ Widget natif PyQt6: {type(native_widget).__name__}")
        
        # Créer des widgets enfants
        main_frame = factory.create_frame(window)
        assert main_frame is not None
        print("✅ Frame PyQt6 créé")
        
        # Label avec style
        label = factory.create_label(main_frame, text="Test PyQt6 Label")
        assert label is not None
        print("✅ Label PyQt6 créé")
        
        # Bouton avec commande
        button_clicked = False
        def on_button_click():
            nonlocal button_clicked
            button_clicked = True
        
        button = factory.create_button(main_frame, text="Test Button", command=on_button_click)
        assert button is not None
        print("✅ Button PyQt6 créé")
        
        # Entry
        entry = factory.create_entry(main_frame)
        assert entry is not None
        print("✅ Entry PyQt6 créé")
        
        # TreeView avec colonnes
        treeview = factory.create_treeview(main_frame, columns=["Col1", "Col2", "Col3"])
        assert treeview is not None
        print("✅ TreeView PyQt6 créé")
        
        # Combobox avec valeurs
        combo = factory.create_combobox(main_frame, values=["Option 1", "Option 2", "Option 3"])
        assert combo is not None
        print("✅ Combobox PyQt6 créé")
    
    def test_pyqt6_layout_system(self):
        """Test du système de layout PyQt6"""
        from gui import set_gui_framework, get_gui_factory
        
        print("\n🧪 Test layouts PyQt6")
        print("=" * 40)
        
        set_gui_framework('pyqt6')
        factory = get_gui_factory()
        
        # Créer une fenêtre
        window = factory.create_window("Test Layout", "500x400")
        main_frame = factory.create_frame(window)
        
        # Test pack layout
        label1 = factory.create_label(main_frame, text="Label Pack")
        label1.pack()
        print("✅ Pack layout testé")
        
        # Test grid layout
        button_frame = factory.create_frame(main_frame)
        
        button1 = factory.create_button(button_frame, text="Button 1")
        button2 = factory.create_button(button_frame, text="Button 2")
        button3 = factory.create_button(button_frame, text="Button 3")
        button4 = factory.create_button(button_frame, text="Button 4")
        
        # Placer en grille
        button1.grid(row=0, column=0)
        button2.grid(row=0, column=1)
        button3.grid(row=1, column=0)
        button4.grid(row=1, column=1)
        
        button_frame.pack()
        main_frame.pack()
        
        print("✅ Grid layout testé")
    
    def test_pyqt6_dialogs(self):
        """Test des dialogues PyQt6"""
        from gui import set_gui_framework, get_gui_factory
        
        print("\n🧪 Test dialogues PyQt6")
        print("=" * 40)
        
        set_gui_framework('pyqt6')
        factory = get_gui_factory()
        
        # Vérifier que les méthodes de dialogue existent
        assert hasattr(factory, 'show_message')
        assert callable(factory.show_message)
        print("✅ show_message disponible")
        
        assert hasattr(factory, 'ask_file')
        assert callable(factory.ask_file)
        print("✅ ask_file disponible")
        
        assert hasattr(factory, 'ask_directory')
        assert callable(factory.ask_directory)
        print("✅ ask_directory disponible")
        
        # Note: On ne teste pas l'affichage réel pour éviter les interactions utilisateur
    
    def test_pyqt6_performance(self):
        """Test des performances PyQt6"""
        import time
        from gui import set_gui_framework, get_gui_factory
        
        print("\n🧪 Test performances PyQt6")
        print("=" * 40)
        
        set_gui_framework('pyqt6')
        factory = get_gui_factory()
        
        # Mesurer le temps de création de widgets
        start_time = time.time()
        
        window = factory.create_window("Performance Test", "400x300")
        main_frame = factory.create_frame(window)
        
        # Créer plusieurs widgets
        widgets = []
        for i in range(50):
            label = factory.create_label(main_frame, text=f"Label {i}")
            button = factory.create_button(main_frame, text=f"Button {i}")
            entry = factory.create_entry(main_frame)
            
            widgets.extend([label, button, entry])
            
            # Empaqueter
            label.pack()
            button.pack()
            entry.pack()
        
        main_frame.pack()
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        print(f"✅ Création de {len(widgets)} widgets en {creation_time:.3f}s")
        
        # Vérifier que c'est raisonnablement rapide (moins de 2 secondes)
        assert creation_time < 2.0, f"Création trop lente: {creation_time:.3f}s"
        
        widgets_per_second = len(widgets) / creation_time
        print(f"✅ Performance: {widgets_per_second:.1f} widgets/seconde")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
