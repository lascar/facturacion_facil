#!/usr/bin/env python3
"""
Corriger les imports Signal pour PyQt5
"""

import os
import re

def fix_signal_imports(file_path):
    """Corriger les imports Signal dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier s'il y a des imports Signal à corriger
        if 'from PyQt5.QtCore import' not in content or 'Signal' not in content:
            return False
        
        print(f"🔧 Correction: {file_path}")
        
        # Remplacements pour les signaux PyQt5
        replacements = [
            # Import Signal -> pyqtSignal as Signal
            (r'from PyQt5\.QtCore import (.*), Signal', r'from PyQt5.QtCore import \1, pyqtSignal as Signal'),
            (r'from PyQt5\.QtCore import Signal', 'from PyQt5.QtCore import pyqtSignal as Signal'),
            
            # Cas où Signal est seul dans l'import
            (r'from PyQt5\.QtCore import Qt, Signal', 'from PyQt5.QtCore import Qt, pyqtSignal as Signal'),
        ]
        
        # Appliquer les remplacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Écrire le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Corrigé: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {file_path} - {e}")
        return False

def main():
    """Corriger tous les fichiers PyQt5"""
    print("🔧 CORRECTION SIGNAUX PYQT5")
    print("="*30)
    
    # Fichiers à corriger
    files_to_fix = [
        'ui/main_window_pyqt5.py',
        'ui/base_pyqt5_window.py',
        'ui/productos_pyqt5.py',
        'ui/organizacion_pyqt5.py',
        'ui/stock_pyqt5.py',
        'ui/facturas_pyqt5.py',
        'ui/clientes_pyqt5.py',
    ]
    
    fixed_count = 0
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_signal_imports(file_path):
                fixed_count += 1
        else:
            print(f"⚠️ Fichier non trouvé: {file_path}")
    
    print(f"\n🎉 Correction terminée: {fixed_count} fichiers")
    print("🚀 Testez: python main.py")

if __name__ == "__main__":
    main()
