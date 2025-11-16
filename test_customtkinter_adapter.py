#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test spécifique de l'adaptateur avec CustomTkinter
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_customtkinter_toplevel():
    """Test de création d'un CTkToplevel avec l'adaptateur"""
    print("🧪 TEST CUSTOMTKINTER TOPLEVEL AVEC ADAPTATEUR")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow
        from ui.pyqt6_window_adapter import create_adapter_for_pyqt6_parent
        
        # Configurer PyQt6
        from gui import set_gui_framework
        set_gui_framework('pyqt6')
        
        # Créer une application PyQt6 pour le test
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✓ QApplication créée")
        
        # Créer une fenêtre PyQt6 de test
        main_window = QMainWindow()
        main_window.setWindowTitle("Test Parent Window")
        main_window.resize(800, 600)
        
        print("✓ Fenêtre PyQt6 parent créée")
        
        # Créer l'adaptateur
        adapter = create_adapter_for_pyqt6_parent(main_window)
        print("✓ Adaptateur créé")
        
        # Vérifier les attributs nécessaires
        required_attrs = [
            '_last_child_ids', 'children', '_name', '_w', 'master',
            '_tclCommands', 'tk'
        ]
        
        for attr in required_attrs:
            if hasattr(adapter, attr):
                print(f"✓ Attribut '{attr}' présent")
            else:
                print(f"❌ Attribut '{attr}' manquant")
                return False
        
        # Test de création CustomTkinter
        print("\n--- Test de création CTkToplevel ---")
        
        try:
            import customtkinter as ctk
            
            # Tenter de créer un CTkToplevel avec l'adaptateur
            toplevel = ctk.CTkToplevel(adapter)
            print("✓ CTkToplevel créé avec succès !")
            
            # Configurer la fenêtre
            toplevel.title("Test Toplevel")
            toplevel.geometry("400x300")
            print("✓ Configuration de la fenêtre réussie")
            
            # Tester l'ajout de widgets
            label = ctk.CTkLabel(toplevel, text="Test Label")
            label.pack(pady=20)
            print("✓ Widget ajouté avec succès")
            
            # Fermer la fenêtre de test
            toplevel.destroy()
            print("✓ Fenêtre fermée proprement")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création CTkToplevel: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_productos_window_creation():
    """Test de création de la fenêtre Productos avec l'adaptateur"""
    print("\n🏭 TEST CRÉATION FENÊTRE PRODUCTOS")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow
        from ui.pyqt6_window_adapter import create_adapter_for_pyqt6_parent
        
        # Configurer PyQt6
        from gui import set_gui_framework
        set_gui_framework('pyqt6')
        
        # Créer une application PyQt6 pour le test
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✓ QApplication créée")
        
        # Créer une fenêtre PyQt6 de test
        main_window = QMainWindow()
        main_window.setWindowTitle("Test Main Window")
        main_window.resize(800, 600)
        
        print("✓ Fenêtre principale créée")
        
        # Créer l'adaptateur
        adapter = create_adapter_for_pyqt6_parent(main_window)
        print("✓ Adaptateur créé")
        
        # Tenter de créer la fenêtre Productos
        print("\n--- Création de ProductosWindow ---")
        
        try:
            from ui.productos import ProductosWindow
            
            # Créer la fenêtre Productos
            productos_window = ProductosWindow(adapter)
            print("✓ ProductosWindow créée avec succès !")
            
            # Vérifier que la fenêtre a été créée
            if hasattr(productos_window, 'window'):
                print("✓ Attribut 'window' présent")
                
                # Tester quelques méthodes
                productos_window.window.title("Test Productos")
                print("✓ Titre modifié avec succès")
                
                # Fermer la fenêtre
                productos_window.window.destroy()
                print("✓ Fenêtre fermée proprement")
                
                return True
            else:
                print("❌ Attribut 'window' manquant")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la création ProductosWindow: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TESTS CUSTOMTKINTER AVEC ADAPTATEUR PYQT6")
    print("="*60)
    
    tests = [
        ("CustomTkinter Toplevel", test_customtkinter_toplevel),
        ("Fenêtre Productos", test_productos_window_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS CUSTOMTKINTER")
    print("="*60)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<30} {status}")
        if result:
            success_count += 1
    
    print(f"\nTests réussis: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("\n🎉 TOUS LES TESTS CUSTOMTKINTER ONT RÉUSSI !")
        print("\n✨ L'adaptateur fonctionne parfaitement avec CustomTkinter !")
        print("\n🚀 Les fenêtres secondaires peuvent maintenant s'ouvrir:")
        print("   • ProductosWindow ✓")
        print("   • Toutes les autres fenêtres devraient fonctionner")
        return 0
    else:
        print(f"\n⚠️ {len(results) - success_count} test(s) ont échoué")
        print("\n💡 L'adaptateur nécessite des améliorations supplémentaires")
        return 1

if __name__ == "__main__":
    sys.exit(main())
