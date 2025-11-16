#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la structure GUI sans dépendances externes
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test des imports de base"""
    print("=== Test des imports ===")
    
    try:
        from gui import SUPPORTED_FRAMEWORKS, DEFAULT_FRAMEWORK
        print(f"✓ Frameworks supportés: {SUPPORTED_FRAMEWORKS}")
        print(f"✓ Framework par défaut: {DEFAULT_FRAMEWORK}")
        
        from gui.gui_manager import GUIManager
        print("✓ GUIManager importé")
        
        from gui.abstract_gui import AbstractWidget, AbstractGUIFactory
        print("✓ Classes abstraites importées")
        
        return True
    except Exception as e:
        print(f"✗ Erreur d'import: {e}")
        return False

def test_framework_detection():
    """Test de détection des frameworks"""
    print("\n=== Test de détection des frameworks ===")
    
    try:
        from gui.gui_manager import GUIManager
        manager = GUIManager()
        
        available = manager.AVAILABLE_FRAMEWORKS
        print(f"✓ Frameworks configurés: {list(available.keys())}")
        
        # Test de chaque framework
        for framework_name in available.keys():
            try:
                framework_info = available[framework_name]
                module_name = framework_info['module']
                print(f"  - {framework_name}: module {module_name}")
                
                # Essayer d'importer le module
                try:
                    __import__(module_name)
                    print(f"    ✓ Module {module_name} disponible")
                except ImportError as e:
                    print(f"    ⚠ Module {module_name} non disponible: {e}")
                    
            except Exception as e:
                print(f"    ✗ Erreur avec {framework_name}: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Erreur de détection: {e}")
        return False

def test_customtkinter_fallback():
    """Test avec CustomTkinter (fallback)"""
    print("\n=== Test CustomTkinter (fallback) ===")
    
    try:
        from gui import set_gui_framework, get_gui_factory
        
        # Tester CustomTkinter
        set_gui_framework('customtkinter')
        factory = get_gui_factory()
        print("✓ CustomTkinter factory créée")
        
        # Test basique sans affichage
        print("✓ CustomTkinter disponible comme fallback")
        return True
        
    except Exception as e:
        print(f"✗ Erreur CustomTkinter: {e}")
        return False

def test_pyqt6_availability():
    """Test de disponibilité de PyQt6"""
    print("\n=== Test disponibilité PyQt6 ===")
    
    try:
        import PyQt6
        print("✓ PyQt6 est installé")
        
        from PyQt6.QtWidgets import QApplication
        print("✓ PyQt6.QtWidgets disponible")
        
        # Test de notre implémentation
        from gui.pyqt6_impl import PyQt6GUIFactory
        print("✓ PyQt6GUIFactory importée")
        
        return True
        
    except ImportError as e:
        print(f"⚠ PyQt6 non disponible: {e}")
        print("  Pour installer PyQt6:")
        print("  - Ubuntu/Debian: sudo apt install python3-pyqt6")
        print("  - Ou avec pip: pip install PyQt6")
        return False
    except Exception as e:
        print(f"✗ Erreur PyQt6: {e}")
        return False

def show_installation_guide():
    """Affiche le guide d'installation"""
    print("\n=== Guide d'installation PyQt6 ===")
    print("""
Méthodes d'installation de PyQt6:

1. Avec pip (recommandé):
   pip install PyQt6

2. Avec apt (Ubuntu/Debian):
   sudo apt update
   sudo apt install python3-pyqt6

3. Avec conda:
   conda install pyqt

4. Vérification de l'installation:
   python3 -c "import PyQt6; print('PyQt6 installé avec succès')"
""")

def main():
    """Fonction principale de test"""
    print("=== Test de la structure GUI ===")
    
    tests = [
        ("Imports de base", test_imports),
        ("Détection des frameworks", test_framework_detection),
        ("CustomTkinter fallback", test_customtkinter_fallback),
        ("Disponibilité PyQt6", test_pyqt6_availability)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "="*50)
    print("RÉSUMÉ DES TESTS")
    print("="*50)
    
    for test_name, result in results:
        status = "✓ RÉUSSI" if result else "✗ ÉCHOUÉ"
        print(f"{test_name:<30} {status}")
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests réussis: {successful}/{total}")
    
    if not results[-1][1]:  # Si PyQt6 n'est pas disponible
        show_installation_guide()
        print("\nAprès installation de PyQt6, exécutez:")
        print("python test_pyqt6.py")
    else:
        print("\n✓ Tout est prêt! Vous pouvez maintenant exécuter:")
        print("python test_pyqt6.py")
        print("python main_pyqt6_demo.py")
    
    return 0 if successful == total else 1

if __name__ == "__main__":
    sys.exit(main())
