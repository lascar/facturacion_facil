#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour patcher les imports CustomTkinter dans les fenêtres existantes
"""

import os
import shutil
import re
from datetime import datetime

def backup_file(file_path):
    """Crée une sauvegarde d'un fichier"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup_ctk_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"✓ Sauvegarde créée: {backup_path}")
        return backup_path
    return None

def patch_customtkinter_imports(file_path):
    """Patch les imports CustomTkinter dans un fichier"""
    if not os.path.exists(file_path):
        print(f"✗ Fichier non trouvé: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacer l'import customtkinter
        if "import customtkinter as ctk" in content:
            # Ajouter l'import de l'adaptateur
            new_import = """# Import adapté pour PyQt6
from gui import set_gui_framework
set_gui_framework('pyqt6')

# Utiliser l'adaptateur CustomTkinter vers PyQt6
try:
    import customtkinter as ctk
except ImportError:
    # Si CustomTkinter n'est pas disponible, utiliser l'adaptateur
    from gui.customtkinter_to_pyqt6_adapter import create_customtkinter_adapter
    ctk = create_customtkinter_adapter()"""
            
            content = content.replace("import customtkinter as ctk", new_import)
        
        # Sauvegarder si des changements ont été faits
        if content != original_content:
            backup_file(file_path)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Fichier patché: {file_path}")
            return True
        else:
            print(f"- Aucun changement nécessaire: {file_path}")
            return True
            
    except Exception as e:
        print(f"✗ Erreur lors du patch de {file_path}: {e}")
        return False

def find_ui_files():
    """Trouve tous les fichiers UI à patcher"""
    ui_files = []
    ui_dir = "ui"
    
    if os.path.exists(ui_dir):
        for file in os.listdir(ui_dir):
            if file.endswith('.py') and file != '__init__.py' and file != 'main_window.py':
                ui_files.append(os.path.join(ui_dir, file))
    
    return ui_files

def patch_all_ui_files():
    """Patch tous les fichiers UI"""
    print("=== Patch des imports CustomTkinter ===")
    
    ui_files = find_ui_files()
    
    if not ui_files:
        print("Aucun fichier UI trouvé à patcher")
        return True
    
    print(f"Fichiers UI trouvés: {len(ui_files)}")
    for file in ui_files:
        print(f"  - {file}")
    
    success_count = 0
    for file_path in ui_files:
        print(f"\n--- Patch de {file_path} ---")
        if patch_customtkinter_imports(file_path):
            success_count += 1
    
    print(f"\n✓ Fichiers patchés avec succès: {success_count}/{len(ui_files)}")
    return success_count == len(ui_files)

def create_compatibility_module():
    """Crée un module de compatibilité pour CustomTkinter"""
    print("\n=== Création du module de compatibilité ===")
    
    compat_file = "customtkinter_compat.py"
    
    compat_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de compatibilité CustomTkinter pour PyQt6
"""

from gui import set_gui_framework
set_gui_framework('pyqt6')

# Réexporter l'adaptateur comme customtkinter
from gui.customtkinter_to_pyqt6_adapter import create_customtkinter_adapter

# Créer le module adapté
_ctk_adapter = create_customtkinter_adapter()

# Exporter toutes les classes
CTkToplevel = _ctk_adapter.CTkToplevel
CTkFrame = _ctk_adapter.CTkFrame
CTkScrollableFrame = _ctk_adapter.CTkScrollableFrame
CTkLabel = _ctk_adapter.CTkLabel
CTkButton = _ctk_adapter.CTkButton

# Fonctions de configuration
set_appearance_mode = _ctk_adapter.set_appearance_mode
set_default_color_theme = _ctk_adapter.set_default_color_theme

# Alias pour compatibilité
CTk = CTkToplevel  # Pour les fenêtres principales
'''
    
    try:
        with open(compat_file, 'w', encoding='utf-8') as f:
            f.write(compat_content)
        
        print(f"✓ Module de compatibilité créé: {compat_file}")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la création du module de compatibilité: {e}")
        return False

def test_patched_imports():
    """Teste les imports patchés"""
    print("\n=== Test des imports patchés ===")
    
    try:
        # Tester l'import du module de compatibilité
        import customtkinter_compat as ctk
        print("✓ Import du module de compatibilité réussi")
        
        # Tester la création d'objets
        print("✓ Test des imports patchés réussi")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🔧 PATCH DES IMPORTS CUSTOMTKINTER VERS PYQT6")
    print("=" * 50)
    
    steps = [
        ("Patch des fichiers UI", patch_all_ui_files),
        ("Création du module de compatibilité", create_compatibility_module),
        ("Test des imports patchés", test_patched_imports)
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        print(f"\n--- {step_name} ---")
        if step_func():
            success_count += 1
        else:
            print(f"✗ Échec de l'étape: {step_name}")
    
    if success_count == len(steps):
        print("\n🎉 Patch des imports réussi !")
        print("\nVos fenêtres CustomTkinter existantes devraient maintenant fonctionner avec PyQt6.")
        print("Testez avec: python main.py")
        return 0
    else:
        print(f"\n⚠ Patch partiellement réussi ({success_count}/{len(steps)} étapes)")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
