#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'implémentation PyQt6
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import set_gui_framework, create_gui_application, get_gui_factory
    from gui.abstract_gui import WidgetType
    
    def test_pyqt6_basic():
        """Test basique de l'implémentation PyQt6"""
        print("=== Test PyQt6 Basic ===")
        
        try:
            # Définir le framework PyQt6
            set_gui_framework('pyqt6')
            print("✓ Framework PyQt6 défini")
            
            # Créer la factory
            factory = get_gui_factory()
            print("✓ Factory PyQt6 créée")
            
            # Créer une fenêtre
            window = factory.create_window(title="Test PyQt6", geometry="600x400")
            print("✓ Fenêtre créée")
            
            # Créer un frame
            frame = factory.create_frame(window)
            print("✓ Frame créé")
            
            # Créer des widgets
            label = factory.create_label(frame, text="Bonjour PyQt6!")
            print("✓ Label créé")
            
            button = factory.create_button(frame, text="Cliquez-moi", command=lambda: print("Bouton cliqué!"))
            print("✓ Bouton créé")
            
            entry = factory.create_entry(frame)
            print("✓ Entry créé")
            
            # Empaqueter les widgets
            label.pack()
            button.pack()
            entry.pack()
            frame.pack()
            print("✓ Widgets empaquetés")
            
            print("✓ Test basique réussi!")
            return True
            
        except Exception as e:
            print(f"✗ Erreur dans le test basique: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_pyqt6_application():
        """Test de l'application PyQt6"""
        print("\n=== Test PyQt6 Application ===")
        
        try:
            # Définir le framework d'abord
            set_gui_framework('pyqt6')

            # Créer l'application
            app = create_gui_application()
            print("✓ Application PyQt6 créée")
            
            # Initialiser
            app.initialize()
            print("✓ Application initialisée")
            
            # Ajouter quelques widgets à la fenêtre principale
            factory = app.gui_factory
            main_window = app.main_window
            
            # Créer un frame principal
            main_frame = factory.create_frame(main_window)
            
            # Ajouter des widgets
            title_label = factory.create_label(main_frame, text="Test Application PyQt6")
            title_label.configure(font=("Arial", 16))
            
            test_button = factory.create_button(main_frame, text="Test Button", 
                                              command=lambda: print("Application test réussie!"))
            
            info_label = factory.create_label(main_frame, text="PyQt6 fonctionne correctement!")
            
            # Empaqueter
            title_label.pack()
            test_button.pack()
            info_label.pack()
            main_frame.pack()
            
            print("✓ Interface créée")
            print("✓ Test application réussi!")
            
            # Afficher la fenêtre (commenté pour les tests automatiques)
            # print("Affichage de la fenêtre...")
            # app.run()
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur dans le test application: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_pyqt6_widgets():
        """Test des différents widgets PyQt6"""
        print("\n=== Test PyQt6 Widgets ===")
        
        try:
            set_gui_framework('pyqt6')
            factory = get_gui_factory()
            
            # Créer une fenêtre de test
            window = factory.create_window(title="Test Widgets", geometry="500x600")
            main_frame = factory.create_frame(window)
            
            # Tester différents widgets
            widgets_created = []
            
            # Label
            label = factory.create_label(main_frame, text="Test Label")
            widgets_created.append("Label")
            
            # Button
            button = factory.create_button(main_frame, text="Test Button", command=lambda: print("Test button clicked"))
            widgets_created.append("Button")
            
            # Entry
            entry = factory.create_entry(main_frame)
            widgets_created.append("Entry")
            
            # Text
            text = factory.create_text(main_frame)
            widgets_created.append("Text")
            
            # Combobox
            combo = factory.create_combobox(main_frame, values=["Option 1", "Option 2", "Option 3"])
            widgets_created.append("Combobox")
            
            # TreeView
            tree = factory.create_treeview(main_frame, columns=["Col1", "Col2", "Col3"])
            widgets_created.append("TreeView")
            
            print(f"✓ Widgets créés: {', '.join(widgets_created)}")
            print("✓ Test widgets réussi!")
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur dans le test widgets: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def main():
        """Fonction principale de test"""
        print("Démarrage des tests PyQt6...")
        
        tests = [
            test_pyqt6_basic,
            test_pyqt6_application,
            test_pyqt6_widgets
        ]
        
        results = []
        for test in tests:
            results.append(test())
        
        print(f"\n=== Résultats ===")
        print(f"Tests réussis: {sum(results)}/{len(results)}")
        
        if all(results):
            print("✓ Tous les tests PyQt6 ont réussi!")
            print("\nVous pouvez maintenant utiliser PyQt6 dans votre application:")
            print("from gui import set_gui_framework")
            print("set_gui_framework('pyqt6')")
        else:
            print("✗ Certains tests ont échoué")
            return 1
        
        return 0

    if __name__ == "__main__":
        sys.exit(main())
        
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que PyQt6 est installé: pip install PyQt6")
    sys.exit(1)
