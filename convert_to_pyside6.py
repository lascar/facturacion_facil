#!/usr/bin/env python3
"""
Script pour convertir automatiquement PyQt6 vers PySide6
"""

import os
import re
import shutil
from datetime import datetime

def backup_file(file_path):
    """Créer une sauvegarde du fichier"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_pyqt6_{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"📁 Sauvegarde: {backup_path}")
    return backup_path

def convert_pyqt6_to_pyside6(content):
    """Convertir le contenu PyQt6 vers PySide6"""
    
    # Remplacements d'imports
    replacements = [
        # Imports principaux
        (r'from PyQt6\.QtWidgets import', 'from PySide6.QtWidgets import'),
        (r'from PyQt6\.QtCore import', 'from PySide6.QtCore import'),
        (r'from PyQt6\.QtGui import', 'from PySide6.QtGui import'),
        (r'import PyQt6\.QtWidgets', 'import PySide6.QtWidgets'),
        (r'import PyQt6\.QtCore', 'import PySide6.QtCore'),
        (r'import PyQt6\.QtGui', 'import PySide6.QtGui'),
        (r'import PyQt6', 'import PySide6'),
        
        # Signaux PyQt6 -> PySide6
        (r'pyqtSignal', 'Signal'),
        
        # Variables et constantes
        (r'PYQT6_AVAILABLE', 'PYSIDE6_AVAILABLE'),
        (r'PyQt6GUIFactory', 'PySide6GUIFactory'),
        (r'PyQt6', 'PySide6'),
        
        # Commentaires et strings
        (r'"PyQt6', '"PySide6'),
        (r"'PyQt6", "'PySide6"),
        (r'# PyQt6', '# PySide6'),
        (r'PyQt6 native', 'PySide6 native'),
        (r'Version PyQt6', 'Version PySide6'),
        (r'Implémentation PyQt6', 'Implémentation PySide6'),
        
        # Framework names
        (r"'pyqt6'", "'pyside6'"),
        (r'"pyqt6"', '"pyside6"'),
        (r'framework.*pyqt6', 'framework pyside6'),
    ]
    
    # Appliquer les remplacements
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def convert_file(file_path):
    """Convertir un fichier PyQt6 vers PySide6"""
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier s'il contient PyQt6
        if 'PyQt6' not in content and 'pyqt6' not in content:
            return False
        
        print(f"🔄 Conversion: {file_path}")
        
        # Créer une sauvegarde
        backup_file(file_path)
        
        # Convertir le contenu
        new_content = convert_pyqt6_to_pyside6(content)
        
        # Écrire le nouveau contenu
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Converti: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la conversion de {file_path}: {e}")
        return False

def find_python_files():
    """Trouver tous les fichiers Python dans le projet"""
    python_files = []
    
    # Répertoires à scanner
    directories = ['.', 'ui', 'gui', 'test', 'tests', 'utils', 'database', 'common']
    
    for directory in directories:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                # Ignorer les répertoires de cache
                dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
                
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
    
    # Ajouter les fichiers à la racine
    for file in os.listdir('.'):
        if file.endswith('.py'):
            python_files.append(file)
    
    return python_files

def main():
    """Fonction principale"""
    print("🔄 CONVERSION PYQT6 → PYSIDE6")
    print("="*50)
    
    # Vérifier que PySide6 est installé
    try:
        import PySide6
        print("✅ PySide6 est disponible")
    except ImportError:
        print("❌ PySide6 n'est pas installé")
        print("Installez-le avec: pip install PySide6")
        return 1
    
    # Trouver tous les fichiers Python
    python_files = find_python_files()
    print(f"📁 {len(python_files)} fichiers Python trouvés")
    
    # Convertir les fichiers
    converted_count = 0
    for file_path in python_files:
        if convert_file(file_path):
            converted_count += 1
    
    print("\n" + "="*50)
    print(f"🎉 CONVERSION TERMINÉE")
    print(f"📊 {converted_count} fichiers convertis")
    print(f"📁 Sauvegardes créées avec extension .backup_pyqt6_*")
    
    # Mettre à jour requirements.txt
    update_requirements()
    
    print("\n💡 PROCHAINES ÉTAPES:")
    print("1. Tester l'application: python main.py")
    print("2. Si problème, restaurer: python restore_from_backup.py")
    print("3. Supprimer les sauvegardes si tout fonctionne")
    
    return 0

def update_requirements():
    """Mettre à jour requirements.txt"""
    try:
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                content = f.read()
            
            # Remplacer PyQt6 par PySide6
            new_content = content.replace('PyQt6', 'PySide6')
            
            with open('requirements.txt', 'w') as f:
                f.write(new_content)
            
            print("✅ requirements.txt mis à jour")
    except Exception as e:
        print(f"⚠️ Erreur mise à jour requirements.txt: {e}")

if __name__ == "__main__":
    exit(main())
