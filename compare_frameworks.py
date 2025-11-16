#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de comparaison entre les différents frameworks GUI
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework, create_gui_application, get_gui_factory

def test_framework_performance(framework_name):
    """Test les performances d'un framework"""
    print(f"\n=== Test {framework_name.upper()} ===")
    
    try:
        start_time = time.time()
        
        # Définir le framework
        set_gui_framework(framework_name)
        setup_time = time.time()
        
        # Créer la factory
        factory = get_gui_factory()
        factory_time = time.time()
        
        # Créer une fenêtre
        window = factory.create_window(title=f"Test {framework_name}", geometry="600x400")
        window_time = time.time()
        
        # Créer plusieurs widgets
        main_frame = factory.create_frame(window)
        
        widgets = []
        for i in range(10):
            label = factory.create_label(main_frame, text=f"Label {i+1}")
            button = factory.create_button(main_frame, text=f"Button {i+1}", 
                                         command=lambda x=i: print(f"Button {x+1} clicked"))
            entry = factory.create_entry(main_frame)
            
            widgets.extend([label, button, entry])
            
            # Empaqueter
            label.pack()
            button.pack()
            entry.pack()
        
        main_frame.pack()
        widgets_time = time.time()
        
        # Calculer les temps
        times = {
            'Setup': setup_time - start_time,
            'Factory': factory_time - setup_time,
            'Window': window_time - factory_time,
            'Widgets': widgets_time - window_time,
            'Total': widgets_time - start_time
        }
        
        print(f"✓ {framework_name} initialisé avec succès")
        print(f"  - Setup: {times['Setup']:.3f}s")
        print(f"  - Factory: {times['Factory']:.3f}s")
        print(f"  - Window: {times['Window']:.3f}s")
        print(f"  - Widgets (30): {times['Widgets']:.3f}s")
        print(f"  - Total: {times['Total']:.3f}s")
        
        return True, times
        
    except Exception as e:
        print(f"✗ Erreur avec {framework_name}: {e}")
        return False, None

def compare_frameworks():
    """Compare les différents frameworks"""
    print("=== Comparaison des Frameworks GUI ===")
    
    frameworks = ['tkinter', 'customtkinter', 'pyqt6']
    results = {}
    
    for framework in frameworks:
        success, times = test_framework_performance(framework)
        if success:
            results[framework] = times
    
    # Afficher le résumé
    print("\n=== RÉSUMÉ COMPARATIF ===")
    
    if results:
        print(f"{'Framework':<15} {'Setup':<8} {'Factory':<8} {'Window':<8} {'Widgets':<8} {'Total':<8}")
        print("-" * 65)
        
        for framework, times in results.items():
            print(f"{framework:<15} {times['Setup']:<8.3f} {times['Factory']:<8.3f} "
                  f"{times['Window']:<8.3f} {times['Widgets']:<8.3f} {times['Total']:<8.3f}")
        
        # Trouver le plus rapide
        fastest = min(results.items(), key=lambda x: x[1]['Total'])
        print(f"\n🏆 Framework le plus rapide: {fastest[0].upper()} ({fastest[1]['Total']:.3f}s)")
        
        # Recommandations
        print("\n=== RECOMMANDATIONS ===")
        
        if 'pyqt6' in results:
            print("✓ PyQt6: Recommandé pour les applications professionnelles")
            print("  - Interface native Windows")
            print("  - Performances excellentes")
            print("  - Widgets riches et modernes")
        
        if 'customtkinter' in results:
            print("✓ CustomTkinter: Bon pour les prototypes rapides")
            print("  - Interface moderne")
            print("  - Facile à utiliser")
            print("  - Moins performant sur Windows")
        
        if 'tkinter' in results:
            print("✓ Tkinter: Basique mais fiable")
            print("  - Inclus avec Python")
            print("  - Interface basique")
            print("  - Performances correctes")
    
    else:
        print("Aucun framework n'a pu être testé avec succès")

def show_migration_guide():
    """Affiche le guide de migration"""
    print("\n=== GUIDE DE MIGRATION ===")
    print("""
Pour migrer votre application vers PyQt6:

1. Installer PyQt6:
   pip install PyQt6

2. Changer le framework dans votre code:
   from gui import set_gui_framework
   set_gui_framework('pyqt6')  # au lieu de 'customtkinter'

3. Votre code existant fonctionnera automatiquement grâce à la couche d'abstraction!

4. Avantages de PyQt6:
   ✓ Interface native Windows
   ✓ Performances supérieures
   ✓ Widgets plus riches
   ✓ Meilleure compatibilité
   ✓ Styling avancé

5. Test de migration:
   python main_pyqt6_demo.py
""")

def main():
    """Fonction principale"""
    print("Script de comparaison des frameworks GUI")
    print("Cela va tester les performances de chaque framework disponible.")
    
    try:
        compare_frameworks()
        show_migration_guide()
        
        print("\n=== PROCHAINES ÉTAPES ===")
        print("1. Testez PyQt6: python test_pyqt6.py")
        print("2. Démonstration: python main_pyqt6_demo.py")
        print("3. Migrez progressivement vos fenêtres")
        
        return 0
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
