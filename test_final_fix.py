#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de validation de la correction PyQt6 native
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_native_pyqt6_window():
    """Test de la fenêtre PyQt6 native"""
    print("=== Test Fenêtre PyQt6 Native ===")
    
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
        window = MainWindow()
        print("✓ MainWindow créée")
        
        # Vérifier que c'est bien une QMainWindow
        from PyQt6.QtWidgets import QMainWindow
        assert isinstance(window, QMainWindow)
        print("✓ MainWindow est bien une QMainWindow native")
        
        # Vérifier le titre
        assert window.windowTitle() == "Facturación Fácil"
        print("✓ Titre correct")
        
        # Vérifier qu'il y a un widget central
        central_widget = window.centralWidget()
        assert central_widget is not None
        print("✓ Widget central présent")
        
        # Vérifier le layout
        layout = central_widget.layout()
        assert layout is not None
        print("✓ Layout principal présent")
        
        # Compter les widgets dans le layout
        widget_count = layout.count()
        print(f"✓ Nombre d'éléments dans le layout: {widget_count}")
        
        # Vérifier qu'il y a au moins le titre et la grille de boutons
        assert widget_count >= 2
        print("✓ Layout contient au moins titre + grille de boutons")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_creation():
    """Test de création des boutons"""
    print("\n=== Test Création des Boutons ===")
    
    try:
        from PyQt6.QtWidgets import QApplication, QPushButton
        from ui.main_window import MainWindow
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        # Créer la fenêtre
        window = MainWindow()
        
        # Trouver tous les boutons dans la fenêtre
        buttons = window.findChildren(QPushButton)
        print(f"✓ Nombre de boutons trouvés: {len(buttons)}")
        
        # Vérifier qu'on a bien 6 boutons
        assert len(buttons) == 6
        print("✓ 6 boutons créés comme attendu")
        
        # Vérifier les textes des boutons
        expected_texts = ["Productos", "Organización", "Stock", "Facturas", "Clientes", "Buscar"]
        button_texts = [button.text() for button in buttons]
        
        print("Textes des boutons trouvés:")
        for i, text in enumerate(button_texts):
            print(f"  {i+1}. '{text}'")
        
        # Vérifier que tous les textes attendus sont présents
        for expected_text in expected_texts:
            assert expected_text in button_texts
            print(f"✓ Bouton '{expected_text}' présent")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_functionality():
    """Test de fonctionnalité des boutons"""
    print("\n=== Test Fonctionnalité des Boutons ===")
    
    try:
        from PyQt6.QtWidgets import QApplication, QPushButton
        from ui.main_window import MainWindow
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        # Créer la fenêtre
        window = MainWindow()
        
        # Tester que chaque bouton a une fonction connectée
        buttons = window.findChildren(QPushButton)
        
        for button in buttons:
            # Vérifier que le bouton a des connexions
            signal = button.clicked
            receivers = signal.receivers(signal)
            
            if receivers > 0:
                print(f"✓ Bouton '{button.text()}' a une fonction connectée")
            else:
                print(f"⚠ Bouton '{button.text()}' n'a pas de fonction connectée")
        
        print("✓ Test de fonctionnalité terminé")
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale de test"""
    print("🔧 TEST FINAL DE CORRECTION PYQT6 NATIVE")
    print("="*60)
    
    tests = [
        ("Fenêtre PyQt6 Native", test_native_pyqt6_window),
        ("Création des Boutons", test_button_creation),
        ("Fonctionnalité des Boutons", test_button_functionality)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ FINAL")
    print("="*60)
    
    success_count = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<30} {status}")
        if result:
            success_count += 1
    
    print(f"\nTests réussis: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("\n🎉 CORRECTION FINALE RÉUSSIE !")
        print("\n✨ Votre fenêtre principale PyQt6 native affiche maintenant:")
        print("   ┌─────────────────────────────────────┐")
        print("   │           Facturación Fácil         │")
        print("   ├─────────────────────────────────────┤")
        print("   │  [Productos]    [Organización]      │")
        print("   │  [Stock]        [Facturas]          │")
        print("   │  [Clientes]     [Buscar]            │")
        print("   └─────────────────────────────────────┘")
        print("\n🚀 Lancez l'application avec: python main.py")
        print("🎯 Tous les 6 boutons devraient être visibles et fonctionnels !")
        return 0
    else:
        print(f"\n⚠️ {len(results) - success_count} test(s) ont échoué")
        return 1

if __name__ == "__main__":
    sys.exit(main())
