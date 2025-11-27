#!/usr/bin/env python3
"""
Script pour convertir PySide6 vers PySide2 (plus stable sur Linux)
"""

import os
import re

def convert_file_to_pyside2(file_path):
    """Convertir un fichier PySide6 vers PySide2"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier s'il contient PySide6
        if 'PySide6' not in content:
            return False
        
        print(f"🔄 Conversion: {file_path}")
        
        # Remplacements PySide6 -> PySide2
        replacements = [
            (r'from PySide6\.QtWidgets import', 'from PySide2.QtWidgets import'),
            (r'from PySide6\.QtCore import', 'from PySide2.QtCore import'),
            (r'from PySide6\.QtGui import', 'from PySide2.QtGui import'),
            (r'import PySide6\.QtWidgets', 'import PySide2.QtWidgets'),
            (r'import PySide6\.QtCore', 'import PySide2.QtCore'),
            (r'import PySide6\.QtGui', 'import PySide2.QtGui'),
            (r'PySide6', 'PySide2'),
            (r'pyside6', 'pyside2'),
            
            # Ajustements spécifiques PySide2
            (r'Qt\.AlignmentFlag\.AlignCenter', 'Qt.AlignCenter'),
            (r'Qt\.Orientation\.Horizontal', 'Qt.Horizontal'),
            (r'Qt\.Orientation\.Vertical', 'Qt.Vertical'),
            (r'QFont\.Weight\.Bold', 'QFont.Bold'),
            (r'QMessageBox\.StandardButton\.', 'QMessageBox.'),
            (r'QTableWidget\.SelectionBehavior\.SelectRows', 'QTableWidget.SelectRows'),
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
    """Convertir tous les fichiers PySide6 vers PySide2"""
    print("🔄 CONVERSION PYSIDE6 → PYSIDE2")
    print("="*40)
    
    # Fichiers à convertir
    files_to_convert = [
        'main.py',
        'ui/main_window_pyside6.py',
        'ui/base_pyside6_window.py',
        'ui/productos_pyside6.py',
        'ui/organizacion_pyside6.py',
        'ui/stock_pyside6.py',
        'ui/facturas_pyside6.py',
        'ui/clientes_pyside6.py',
        'gui/__init__.py',
        'requirements.txt'
    ]
    
    converted_count = 0
    for file_path in files_to_convert:
        if os.path.exists(file_path):
            if convert_file_to_pyside2(file_path):
                converted_count += 1
        else:
            print(f"⚠️ Fichier non trouvé: {file_path}")
    
    # Renommer les fichiers
    rename_files = [
        ('ui/main_window_pyside6.py', 'ui/main_window_pyside2.py'),
        ('ui/base_pyside6_window.py', 'ui/base_pyside2_window.py'),
        ('ui/productos_pyside6.py', 'ui/productos_pyside2.py'),
        ('ui/organizacion_pyside6.py', 'ui/organizacion_pyside2.py'),
        ('ui/stock_pyside6.py', 'ui/stock_pyside2.py'),
        ('ui/facturas_pyside6.py', 'ui/facturas_pyside2.py'),
        ('ui/clientes_pyside6.py', 'ui/clientes_pyside2.py'),
    ]
    
    for old_name, new_name in rename_files:
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            print(f"📝 Renommé: {old_name} → {new_name}")
    
    print(f"\n🎉 Conversion terminée: {converted_count} fichiers")
    print("💡 Installez PySide2: pip install PySide2")
    print("🚀 Testez: python main.py")

if __name__ == "__main__":
    main()
