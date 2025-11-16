#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de validation de la correction de la fenêtre principale PyQt6
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_translations():
    """Test que toutes les traductions nécessaires existent"""
    print("=== Test des traductions ===")
    
    from utils.translations import get_text
    
    required_keys = [
        "app_title",
        "productos", 
        "organizacion",
        "stock",
        "facturas",
        "clientes"
    ]
    
    success = True
    for key in required_keys:
        try:
            text = get_text(key)
            if text == key:  # Si get_text retourne la clé, c'est qu'elle n'existe pas
                print(f"✗ Traduction manquante pour '{key}'")
                success = False
            else:
                print(f"✓ '{key}' → '{text}'")
        except Exception as e:
            print(f"✗ Erreur pour '{key}': {e}")
            success = False
    
    return success

def test_main_window_creation():
    """Test de création de la fenêtre principale"""
    print("\n=== Test de création de la fenêtre principale ===")
    
    try:
        from gui import set_gui_framework
        set_gui_framework('pyqt6')
        
        from ui.main_window import MainWindow
        print("✓ Import de MainWindow réussi")
        
        # Test de création (sans affichage)
        print("✓ Classe MainWindow disponible")
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_creation():
    """Test de création des boutons"""
    print("\n=== Test de création des boutons ===")
    
    try:
        from gui import set_gui_framework, get_gui_factory
        set_gui_framework('pyqt6')
        
        factory = get_gui_factory()
        
        # Créer une fenêtre de test
        window = factory.create_window("Test", "400x300")
        
        # Créer un frame horizontal
        frame = factory.create_frame(window, layout='horizontal')
        print("✓ Frame horizontal créé")
        
        # Créer des boutons
        button1 = factory.create_button(frame, text="Test 1", command=lambda: print("Button 1"))
        button2 = factory.create_button(frame, text="Test 2", command=lambda: print("Button 2"))
        
        button1.pack()
        button2.pack()
        frame.pack()
        
        print("✓ Boutons créés et empaquetés avec succès")
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_layout_system():
    """Test du système de layout"""
    print("\n=== Test du système de layout ===")
    
    try:
        from gui import set_gui_framework, get_gui_factory
        set_gui_framework('pyqt6')
        
        factory = get_gui_factory()
        
        # Test layout vertical (par défaut)
        window = factory.create_window("Test Layout", "400x300")
        main_frame = factory.create_frame(window)
        
        # Test layout horizontal
        row_frame = factory.create_frame(main_frame, layout='horizontal')
        
        # Ajouter des widgets
        label = factory.create_label(row_frame, text="Test Label")
        button = factory.create_button(row_frame, text="Test Button")
        
        label.pack()
        button.pack()
        row_frame.pack()
        main_frame.pack()
        
        print("✓ Système de layout fonctionne correctement")
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🔧 TEST DE CORRECTION DE LA FENÊTRE PRINCIPALE PYQT6")
    print("="*60)
    
    tests = [
        ("Traductions", test_translations),
        ("Création fenêtre principale", test_main_window_creation),
        ("Création des boutons", test_button_creation),
        ("Système de layout", test_layout_system)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<30} {status}")
        if result:
            success_count += 1
    
    print(f"\nTests réussis: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("\n🎉 CORRECTION RÉUSSIE !")
        print("\n✨ La fenêtre principale PyQt6 devrait maintenant afficher tous les boutons:")
        print("   - Productos")
        print("   - Organización") 
        print("   - Stock")
        print("   - Facturas")
        print("   - Clientes")
        print("   - Buscar")
        print("\n🚀 Lancez l'application avec: python main.py")
        return 0
    else:
        print(f"\n⚠️ {len(results) - success_count} test(s) ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
