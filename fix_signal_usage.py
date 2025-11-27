#!/usr/bin/env python3
"""
Corriger l'usage de pyqtSignal vers Signal dans tous les fichiers
"""

import os
import re

def fix_signal_usage(file_path):
    """Corriger l'usage de pyqtSignal dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier s'il y a des usages pyqtSignal à corriger
        if 'pyqtSignal(' not in content:
            return False
        
        print(f"🔧 Correction usage: {file_path}")
        
        # Remplacer pyqtSignal( par Signal(
        content = content.replace('pyqtSignal(', 'Signal(')
        
        # Écrire le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Corrigé usage: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {file_path} - {e}")
        return False

def main():
    """Corriger l'usage Signal dans tous les fichiers PyQt5"""
    print("🔧 CORRECTION USAGE SIGNAL PYQT5")
    print("="*35)
    
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
            if fix_signal_usage(file_path):
                fixed_count += 1
        else:
            print(f"⚠️ Fichier non trouvé: {file_path}")
    
    print(f"\n🎉 Correction usage terminée: {fixed_count} fichiers")
    print("🚀 Testez: python main.py")

if __name__ == "__main__":
    main()
