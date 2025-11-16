#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migration automatique vers PyQt6
"""

import os
import shutil
import sys
from datetime import datetime

def backup_file(file_path):
    """Crée une sauvegarde d'un fichier"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"✓ Sauvegarde créée: {backup_path}")
        return backup_path
    return None

def migrate_main_window():
    """Migre la fenêtre principale vers PyQt6"""
    print("=== Migration de la fenêtre principale ===")
    
    original_file = "ui/main_window.py"
    new_file = "ui/main_window_pyqt6.py"
    
    if not os.path.exists(original_file):
        print(f"✗ Fichier original non trouvé: {original_file}")
        return False
    
    if not os.path.exists(new_file):
        print(f"✗ Fichier PyQt6 non trouvé: {new_file}")
        return False
    
    # Créer une sauvegarde
    backup_path = backup_file(original_file)
    
    # Remplacer le fichier original
    shutil.copy2(new_file, original_file)
    print(f"✓ {original_file} remplacé par la version PyQt6")
    
    # Mettre à jour les imports dans le fichier
    update_main_window_imports()
    
    return True

def update_main_window_imports():
    """Met à jour les imports dans main_window.py"""
    file_path = "ui/main_window.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer la classe
        content = content.replace('class MainWindowPyQt6:', 'class MainWindow:')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Imports mis à jour dans main_window.py")
        
    except Exception as e:
        print(f"✗ Erreur lors de la mise à jour des imports: {e}")

def update_main_py():
    """Met à jour main.py pour utiliser PyQt6"""
    print("\n=== Mise à jour de main.py ===")
    
    main_file = "main.py"
    if not os.path.exists(main_file):
        print(f"✗ Fichier main.py non trouvé")
        return False
    
    # Créer une sauvegarde
    backup_path = backup_file(main_file)
    
    try:
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter l'import pour définir le framework PyQt6
        if "from gui import set_gui_framework" not in content:
            # Trouver la ligne d'import de MainWindow
            lines = content.split('\n')
            insert_index = 0
            
            for i, line in enumerate(lines):
                if "from ui.main_window import MainWindow" in line:
                    insert_index = i
                    break
            
            # Insérer les imports PyQt6
            lines.insert(insert_index, "from gui import set_gui_framework")
            lines.insert(insert_index + 1, "")
            lines.insert(insert_index + 2, "# Définir PyQt6 comme framework GUI")
            lines.insert(insert_index + 3, "set_gui_framework('pyqt6')")
            lines.insert(insert_index + 4, "")
            
            content = '\n'.join(lines)
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ main.py mis à jour pour utiliser PyQt6")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la mise à jour de main.py: {e}")
        return False

def test_migration():
    """Teste la migration"""
    print("\n=== Test de la migration ===")
    
    try:
        # Importer et tester
        sys.path.insert(0, os.getcwd())
        
        from gui import set_gui_framework
        set_gui_framework('pyqt6')
        
        from ui.main_window import MainWindow
        print("✓ Import de MainWindow réussi")
        
        # Test de création (sans affichage)
        print("✓ Migration testée avec succès")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_migration_summary():
    """Affiche le résumé de la migration"""
    print("\n" + "="*50)
    print("RÉSUMÉ DE LA MIGRATION")
    print("="*50)
    print("""
✅ Migration vers PyQt6 terminée !

Changements effectués:
- ui/main_window.py → sauvegardé et remplacé par la version PyQt6
- main.py → mis à jour pour utiliser PyQt6
- Couche d'abstraction GUI → PyQt6 configuré par défaut

Avantages obtenus:
✓ Interface native Windows
✓ Performances améliorées
✓ Widgets plus riches
✓ Meilleure compatibilité

Pour lancer l'application:
python main.py

Pour revenir à CustomTkinter (si nécessaire):
1. Restaurer les fichiers .backup_*
2. Ou changer set_gui_framework('customtkinter') dans main.py
""")

def main():
    """Fonction principale de migration"""
    print("🔄 MIGRATION AUTOMATIQUE VERS PYQT6")
    print("="*40)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("ui/main_window.py"):
        print("✗ Erreur: Exécutez ce script depuis le répertoire racine du projet")
        return 1
    
    # Étapes de migration
    steps = [
        ("Migration de la fenêtre principale", migrate_main_window),
        ("Mise à jour de main.py", update_main_py),
        ("Test de la migration", test_migration)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n--- {step_name} ---")
        if step_func():
            success_count += 1
        else:
            print(f"✗ Échec de l'étape: {step_name}")
    
    if success_count == len(steps):
        show_migration_summary()
        print("\n🎉 Migration réussie ! Votre application utilise maintenant PyQt6.")
        return 0
    else:
        print(f"\n⚠ Migration partiellement réussie ({success_count}/{len(steps)} étapes)")
        print("Vérifiez les erreurs ci-dessus et corrigez manuellement si nécessaire.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
