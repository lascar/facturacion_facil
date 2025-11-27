#!/usr/bin/env python3
"""
Script pour convertir PySide2 vers PyQt5
"""

import os
import re

def convert_file_to_pyqt5(file_path):
    """Convertir un fichier PySide2 vers PyQt5"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier s'il contient PySide2
        if 'PySide2' not in content and 'pyside2' not in content:
            return False
        
        print(f"🔄 Conversion: {file_path}")
        
        # Remplacements PySide2 -> PyQt5
        replacements = [
            # Imports
            (r'from PySide2\.QtWidgets import', 'from PyQt5.QtWidgets import'),
            (r'from PySide2\.QtCore import', 'from PyQt5.QtCore import'),
            (r'from PySide2\.QtGui import', 'from PyQt5.QtGui import'),
            (r'import PySide2\.QtWidgets', 'import PyQt5.QtWidgets'),
            (r'import PySide2\.QtCore', 'import PyQt5.QtCore'),
            (r'import PySide2\.QtGui', 'import PyQt5.QtGui'),
            
            # Noms de modules
            (r'PySide2', 'PyQt5'),
            (r'pyside2', 'pyqt5'),
            
            # Signaux PySide2 -> PyQt5
            (r'from PySide2\.QtCore import Signal', 'from PyQt5.QtCore import pyqtSignal as Signal'),
            (r'Signal\(', 'pyqtSignal('),
            
            # Constantes Qt (déjà compatibles entre PySide2 et PyQt5)
            # Pas de changements nécessaires pour les constantes Qt
        ]
        
        # Appliquer les remplacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Écrire le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Converti: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {file_path} - {e}")
        return False

def main():
    """Convertir tous les fichiers PySide2 vers PyQt5"""
    print("🔄 CONVERSION PYSIDE2 → PYQT5")
    print("="*40)
    
    # Fichiers à convertir
    files_to_convert = [
        'main.py',
        'ui/main_window_pyside2.py',
        'ui/base_pyside2_window.py',
        'ui/productos_pyside2.py',
        'ui/organizacion_pyside2.py',
        'ui/stock_pyside2.py',
        'ui/facturas_pyside2.py',
        'ui/clientes_pyside2.py',
        'gui/__init__.py',
        'requirements.txt'
    ]
    
    converted_count = 0
    for file_path in files_to_convert:
        if os.path.exists(file_path):
            if convert_file_to_pyqt5(file_path):
                converted_count += 1
        else:
            print(f"⚠️ Fichier non trouvé: {file_path}")
    
    # Renommer les fichiers
    rename_files = [
        ('ui/main_window_pyside2.py', 'ui/main_window_pyqt5.py'),
        ('ui/base_pyside2_window.py', 'ui/base_pyqt5_window.py'),
        ('ui/productos_pyside2.py', 'ui/productos_pyqt5.py'),
        ('ui/organizacion_pyside2.py', 'ui/organizacion_pyqt5.py'),
        ('ui/stock_pyside2.py', 'ui/stock_pyqt5.py'),
        ('ui/facturas_pyside2.py', 'ui/facturas_pyqt5.py'),
        ('ui/clientes_pyside2.py', 'ui/clientes_pyqt5.py'),
    ]
    
    for old_name, new_name in rename_files:
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            print(f"📝 Renommé: {old_name} → {new_name}")
    
    # Mettre à jour les imports dans main.py
    if os.path.exists('main.py'):
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('main_window_pyside2', 'main_window_pyqt5')
        content = content.replace('MainWindowPySide2', 'MainWindowPyQt5')
        
        with open('main.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("📝 Mis à jour main.py")
    
    print(f"\n🎉 Conversion terminée: {converted_count} fichiers")
    print("💡 Installez PyQt5: pip install PyQt5")
    print("🚀 Testez: python main.py")

if __name__ == "__main__":
    main()
