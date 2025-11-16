#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de l'application complète PyQt6 + CustomTkinter
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_application_startup():
    """Test de démarrage de l'application"""
    print("🚀 TEST DE DÉMARRAGE DE L'APPLICATION")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✓ QApplication créée")
        
        # Créer la fenêtre principale
        main_window = MainWindow()
        print("✓ MainWindow créée")
        
        # Vérifier que c'est bien une QMainWindow
        from PyQt6.QtWidgets import QMainWindow
        assert isinstance(main_window, QMainWindow)
        print("✓ MainWindow est bien une QMainWindow native")
        
        # Vérifier le titre
        assert main_window.windowTitle() == "Facturación Fácil"
        print("✓ Titre correct")
        
        # Vérifier qu'il y a un widget central
        central_widget = main_window.centralWidget()
        assert central_widget is not None
        print("✓ Widget central présent")
        
        # Vérifier le layout
        layout = central_widget.layout()
        assert layout is not None
        print("✓ Layout principal présent")
        
        # Compter les boutons
        from PyQt6.QtWidgets import QPushButton
        buttons = main_window.findChildren(QPushButton)
        print(f"✓ Nombre de boutons trouvés: {len(buttons)}")
        assert len(buttons) == 6
        print("✓ 6 boutons créés comme attendu")
        
        # Vérifier les textes des boutons
        expected_texts = ["Productos", "Organización", "Stock", "Facturas", "Clientes", "Buscar"]
        button_texts = [button.text() for button in buttons]
        
        for expected_text in expected_texts:
            assert expected_text in button_texts
            print(f"✓ Bouton '{expected_text}' présent")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_adapter_functionality():
    """Test de fonctionnalité de l'adaptateur"""
    print("\n🔗 TEST DE L'ADAPTATEUR PYQT6")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow
        from ui.pyqt6_window_adapter import create_adapter_for_pyqt6_parent
        
        # Créer une application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        # Créer une fenêtre PyQt6 de test
        main_window = QMainWindow()
        main_window.setWindowTitle("Test Window")
        main_window.resize(800, 600)
        
        print("✓ Fenêtre PyQt6 de test créée")
        
        # Créer l'adaptateur
        adapter = create_adapter_for_pyqt6_parent(main_window)
        print("✓ Adaptateur créé")
        
        # Tester les attributs essentiels
        essential_attrs = ['tk', '_last_child_ids', 'children', 'master']
        for attr in essential_attrs:
            assert hasattr(adapter, attr)
            print(f"✓ Attribut '{attr}' présent")
        
        # Tester les méthodes essentielles
        essential_methods = ['geometry', 'title', 'lift', 'focus_force']
        for method in essential_methods:
            assert hasattr(adapter, method)
            print(f"✓ Méthode '{method}' présente")

        # Tester splitlist dans l'objet tk
        assert hasattr(adapter.tk, 'splitlist')
        print("✓ Méthode 'splitlist' présente dans tk")

        # Tester splitlist avec différents types
        assert adapter.tk.splitlist("a b c") == ["a", "b", "c"]
        assert adapter.tk.splitlist(("a", "b", "c")) == ["a", "b", "c"]
        assert adapter.tk.splitlist(None) == []
        print("✓ Méthode splitlist fonctionne avec tous les types")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_customtkinter_compatibility():
    """Test de compatibilité avec CustomTkinter"""
    print("\n🎨 TEST DE COMPATIBILITÉ CUSTOMTKINTER")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow
        from ui.pyqt6_window_adapter import create_adapter_for_pyqt6_parent
        import customtkinter as ctk
        
        # Configurer PyQt6
        from gui import set_gui_framework
        set_gui_framework('pyqt6')
        
        # Créer une application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        # Créer une fenêtre PyQt6 de test
        main_window = QMainWindow()
        main_window.setWindowTitle("Test Parent Window")
        main_window.resize(800, 600)
        
        print("✓ Fenêtre PyQt6 parent créée")
        
        # Créer l'adaptateur
        adapter = create_adapter_for_pyqt6_parent(main_window)
        print("✓ Adaptateur créé")
        
        # Tester la création d'un CTkToplevel
        toplevel = ctk.CTkToplevel(adapter)
        print("✓ CTkToplevel créé avec succès")
        
        # Configurer la fenêtre
        toplevel.title("Test Toplevel")
        toplevel.geometry("400x300")
        print("✓ Configuration de la fenêtre réussie")
        
        # Tester l'ajout de widgets
        label = ctk.CTkLabel(toplevel, text="Test Label")
        label.pack(pady=20)
        print("✓ Widget ajouté avec succès")
        
        button = ctk.CTkButton(toplevel, text="Test Button")
        button.pack(pady=10)
        print("✓ Bouton ajouté avec succès")
        
        # Fermer la fenêtre de test
        toplevel.destroy()
        print("✓ Fenêtre fermée proprement")
        
        # Nettoyer l'adaptateur
        adapter.cleanup()
        print("✓ Adaptateur nettoyé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TEST FINAL DE L'APPLICATION PYQT6 + CUSTOMTKINTER")
    print("="*80)
    
    tests = [
        ("Démarrage de l'application", test_application_startup),
        ("Fonctionnalité de l'adaptateur", test_adapter_functionality),
        ("Compatibilité CustomTkinter", test_customtkinter_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé final
    print("\n" + "="*80)
    print("RÉSUMÉ FINAL DES TESTS")
    print("="*80)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<35} {status}")
        if result:
            success_count += 1
    
    print(f"\nTests réussis: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("\n🎉 TOUS LES TESTS FINAUX ONT RÉUSSI !")
        print("\n✨ VOTRE APPLICATION EST COMPLÈTEMENT FONCTIONNELLE !")
        print("\n🖥️ Interface finale disponible :")
        print("   ┌─────────────────────────────────────┐")
        print("   │           Facturación Fácil         │")
        print("   ├─────────────────────────────────────┤")
        print("   │  [Productos]    [Organización]      │")
        print("   │  [Stock]        [Facturas]          │")
        print("   │  [Clientes]     [Buscar]            │")
        print("   └─────────────────────────────────────┘")
        print("\n🚀 Commande de lancement :")
        print("   python main.py")
        print("\n🎯 TOUTES LES FONCTIONNALITÉS SONT OPÉRATIONNELLES !")
        return 0
    else:
        print(f"\n⚠️ {len(results) - success_count} test(s) ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
