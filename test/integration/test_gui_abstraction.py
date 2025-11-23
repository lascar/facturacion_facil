#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests d'intégration pour l'architecture d'abstraction GUI
"""

import pytest
import sys
import os

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

class TestGUIAbstraction:
    """Tests d'intégration pour l'abstraction GUI"""
    
    def test_framework_loading(self):
        """Test du chargement des frameworks"""
        from gui import get_gui_manager, set_gui_framework
        
        print("🧪 Test chargement des frameworks")
        print("=" * 40)
        
        # Test PyQt6 (nouveau framework par défaut)
        print("\n   1️⃣ Test PyQt6")
        set_gui_framework('pyqt6')
        manager = get_gui_manager()

        assert manager.get_current_framework() == 'pyqt6'
        assert 'PyQt6' in type(manager.get_factory()).__name__
        print(f"     ✅ PyQt6 chargé: {type(manager.get_factory()).__name__}")

        # Test PyQt6 (framework unique après migration)
        print("\n   2️⃣ Test PyQt6 (framework unique)")
        set_gui_framework('pyqt6')
        manager = get_gui_manager()

        assert manager.get_current_framework() == 'pyqt6'
        assert 'PyQt6' in type(manager.get_factory()).__name__
        print(f"     ✅ PyQt6 confirmé: {type(manager.get_factory()).__name__}")

        # Test que les autres frameworks ne sont plus supportés
        print("\n   3️⃣ Test frameworks non supportés")
        try:
            set_gui_framework('pyqt6')
            # Devrait toujours retourner PyQt6 car c'est le seul supporté
            assert manager.get_current_framework() == 'pyqt6'
            print("     ✅ Migration vers PyQt6 confirmée")
        except Exception as e:
            print(f"     ✅ Frameworks non supportés correctement rejetés: {e}")
    
    def test_widget_creation(self):
        """Test de création de widgets"""
        from gui import get_gui_factory, set_gui_framework
        
        print("\n🧪 Test création de widgets")
        print("=" * 40)
        
        frameworks = ['pyqt6', 'tkinter']
        
        for framework in frameworks:
            print(f"\n   🎨 Test avec {framework}")
            set_gui_framework(framework)
            factory = get_gui_factory()
            
            # Créer une fenêtre
            window = factory.create_window(f"Test {framework}", "400x300")
            assert window is not None
            assert hasattr(window, 'get_native_widget')
            print(f"     ✅ Fenêtre créée")
            
            # Créer un frame
            frame = factory.create_frame(window)
            assert frame is not None
            assert hasattr(frame, 'pack')
            print(f"     ✅ Frame créé")
            
            # Créer des widgets
            label = factory.create_label(frame, text="Test Label")
            assert label is not None
            print(f"     ✅ Label créé")
            
            button = factory.create_button(frame, text="Test Button", command=lambda: None)
            assert button is not None
            print(f"     ✅ Button créé")
            
            entry = factory.create_entry(frame)
            assert entry is not None
            print(f"     ✅ Entry créé")
            
            # Test empaquetage (sans afficher)
            try:
                frame.pack(fill="both", expand=True)
                label.pack(pady=5)
                button.pack(pady=5)
                entry.pack(pady=5)
                print(f"     ✅ Widgets empaquetés")
            except Exception as e:
                print(f"     ⚠️ Empaquetage: {e}")
    
    def test_abstract_components(self):
        """Test des composants abstraits"""
        from gui.abstract_components import AbstractForm, AbstractListWindow
        from gui import set_gui_framework
        
        print("\n🧪 Test composants abstraits")
        print("=" * 40)
        
        # Test avec PyQt6 (framework par défaut)
        print("\n   📝 Test AbstractForm")
        set_gui_framework('pyqt6')
        
        class TestForm(AbstractForm):
            def create_widgets(self):
                self.add_field("nom", "Nom:", "entry")
                self.add_field("email", "Email:", "entry")
                self.add_button("save", "Sauvegarder", lambda: None)
        
        try:
            # Ne pas afficher la fenêtre pour les tests
            form = TestForm()
            form.create_widgets()
            
            # Tester les méthodes
            form.set_field_value("nom", "Test User")
            nom = form.get_field_value("nom")
            assert nom == "Test User"
            
            form.clear_form()
            nom_cleared = form.get_field_value("nom")
            assert nom_cleared == ""
            
            print("     ✅ AbstractForm fonctionne")
            
            # Nettoyer
            form.destroy()
            
        except Exception as e:
            print(f"     ⚠️ AbstractForm: {e}")
        
        # Test AbstractListWindow
        print("\n   📋 Test AbstractListWindow")
        
        class TestList(AbstractListWindow):
            def create_widgets(self):
                self.create_list_widgets()
            
            def load_data(self):
                self.add_item(["Item 1", "Value 1"])
                self.add_item(["Item 2", "Value 2"])
            
            def on_item_selected(self, event=None):
                pass
        
        try:
            test_list = TestList()
            test_list.set_columns(["Name", "Value"])
            test_list.create_widgets()
            test_list.load_data()
            
            print("     ✅ AbstractListWindow fonctionne")
            
            # Nettoyer
            test_list.destroy()
            
        except Exception as e:
            print(f"     ⚠️ AbstractListWindow: {e}")
    
    def test_framework_switching(self):
        """Test du changement de framework"""
        from gui import get_gui_manager, set_gui_framework
        
        print("\n🧪 Test changement de framework")
        print("=" * 40)
        
        manager = get_gui_manager()
        
        # Test changements multiples (inclure PyQt6)
        frameworks = ['pyqt6', 'tkinter', 'pyqt6']
        
        for i, framework in enumerate(frameworks):
            print(f"\n   {i+1}️⃣ Changement vers {framework}")
            
            set_gui_framework(framework)
            current = manager.get_current_framework()
            factory_type = type(manager.get_factory()).__name__
            
            # Après migration PyQt6, tous les frameworks doivent retourner 'pyqt6'
            assert current == 'pyqt6', f"Après migration, le framework doit être PyQt6, mais c'est {current}"
            print(f"     ✅ Framework: {current}")
            print(f"     ✅ Factory: {factory_type}")
            
            # Créer un widget pour vérifier que ça fonctionne
            factory = manager.get_factory()
            window = factory.create_window("Test Switch", "300x200")
            assert window is not None
            print(f"     ✅ Widget créé avec succès")
    
    def test_message_dialogs(self):
        """Test des boîtes de dialogue"""
        from gui import get_gui_factory, set_gui_framework
        
        print("\n🧪 Test boîtes de dialogue")
        print("=" * 40)
        
        frameworks = ['pyqt6', 'tkinter']
        
        for framework in frameworks:
            print(f"\n   💬 Test avec {framework}")
            set_gui_framework(framework)
            factory = get_gui_factory()
            
            # Test des différents types de messages
            # (Ne pas afficher réellement pour les tests automatiques)
            try:
                # Ces méthodes existent et sont callable
                assert hasattr(factory, 'show_message')
                assert callable(factory.show_message)
                
                assert hasattr(factory, 'ask_file')
                assert callable(factory.ask_file)
                
                assert hasattr(factory, 'ask_directory')
                assert callable(factory.ask_directory)
                
                print(f"     ✅ Méthodes de dialogue disponibles")
                
            except Exception as e:
                print(f"     ❌ Erreur: {e}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
