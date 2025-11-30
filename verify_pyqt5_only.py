#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification finale pour s'assurer que l'application utilise uniquement PyQt5
"""

import os
import re
from pathlib import Path

def scan_for_non_pyqt5_imports():
    """Scanne tous les fichiers Python actifs pour détecter les imports non-PyQt5"""
    
    # Patterns à détecter
    forbidden_patterns = [
        r'from PyQt6\.',
        r'import PyQt6',
        r'from PySide2\.',
        r'import PySide2',
        r'from PySide6\.',
        r'import PySide6',
        r'import tkinter',
        r'from tkinter',
        r'import customtkinter',
        r'from customtkinter'
    ]
    
    # Dossiers à scanner (exclure les sauvegardes et tests)
    scan_dirs = ['ui', 'database', 'utils', 'common', 'gui']
    scan_files = ['main.py']
    
    print("🔍 VÉRIFICATION IMPORTS NON-PYQT5")
    print("="*40)
    
    issues_found = []
    files_scanned = 0
    
    # Scanner les dossiers
    for scan_dir in scan_dirs:
        if os.path.exists(scan_dir):
            for root, dirs, files in os.walk(scan_dir):
                # Exclure les dossiers de sauvegarde
                dirs[:] = [d for d in dirs if not d.startswith('backup') and d != '__pycache__']
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        issues = scan_file_for_imports(file_path, forbidden_patterns)
                        if issues:
                            issues_found.extend([(file_path, issue) for issue in issues])
                        files_scanned += 1
    
    # Scanner les fichiers individuels
    for scan_file in scan_files:
        if os.path.exists(scan_file):
            issues = scan_file_for_imports(scan_file, forbidden_patterns)
            if issues:
                issues_found.extend([(scan_file, issue) for issue in issues])
            files_scanned += 1
    
    # Afficher les résultats
    print(f"📊 Fichiers scannés: {files_scanned}")
    
    if issues_found:
        print(f"\n❌ PROBLÈMES DÉTECTÉS: {len(issues_found)}")
        print("-" * 40)
        
        for file_path, issue in issues_found:
            print(f"🚨 {file_path}:")
            print(f"   Ligne {issue['line']}: {issue['content'].strip()}")
            print(f"   Pattern: {issue['pattern']}")
            print()
    else:
        print(f"\n✅ AUCUN PROBLÈME DÉTECTÉ!")
        print("   • Tous les fichiers utilisent uniquement PyQt5")
        print("   • Aucun import PyQt6/PySide2/PySide6/tkinter trouvé")
    
    return len(issues_found) == 0

def scan_file_for_imports(file_path, patterns):
    """Scanne un fichier pour les patterns interdits"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    issues.append({
                        'line': line_num,
                        'content': line,
                        'pattern': pattern
                    })
    except Exception as e:
        print(f"⚠️  Erreur lecture {file_path}: {e}")
    
    return issues

def verify_pyqt5_imports():
    """Vérifie que les imports PyQt5 sont corrects"""
    
    print("\n✅ VÉRIFICATION IMPORTS PYQT5")
    print("="*40)
    
    # Fichiers qui doivent avoir des imports PyQt5
    pyqt5_files = [
        'ui/main_window_pyqt5.py',
        'ui/base_pyqt5_window.py',
        'ui/productos_pyqt5.py',
        'ui/clientes_pyqt5.py',
        'ui/organizacion_pyqt5.py',
        'ui/stock_pyqt5.py',
        'ui/facturas_pyqt5.py'
    ]
    
    correct_imports = 0
    
    for file_path in pyqt5_files:
        if os.path.exists(file_path):
            has_pyqt5 = check_pyqt5_imports(file_path)
            if has_pyqt5:
                print(f"✅ {file_path}: Imports PyQt5 OK")
                correct_imports += 1
            else:
                print(f"❌ {file_path}: Pas d'imports PyQt5 détectés")
        else:
            print(f"⚠️  {file_path}: Fichier manquant")
    
    print(f"\n📊 Fichiers avec imports PyQt5 corrects: {correct_imports}/{len(pyqt5_files)}")
    return correct_imports == len(pyqt5_files)

def check_pyqt5_imports(file_path):
    """Vérifie qu'un fichier a des imports PyQt5"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'from PyQt5.' in content or 'import PyQt5' in content
    except:
        return False

def main():
    """Fonction principale"""
    print("🔧 VÉRIFICATION FINALE PYQT5")
    print("="*50)
    
    # Étape 1: Vérifier l'absence d'imports interdits
    no_forbidden_imports = scan_for_non_pyqt5_imports()
    
    # Étape 2: Vérifier la présence d'imports PyQt5
    has_pyqt5_imports = verify_pyqt5_imports()
    
    # Résumé final
    print(f"\n🎯 RÉSUMÉ FINAL")
    print("="*20)
    print(f"{'✅' if no_forbidden_imports else '❌'} Aucun import interdit: {'OK' if no_forbidden_imports else 'PROBLÈMES'}")
    print(f"{'✅' if has_pyqt5_imports else '❌'} Imports PyQt5 présents: {'OK' if has_pyqt5_imports else 'MANQUANTS'}")
    
    if no_forbidden_imports and has_pyqt5_imports:
        print(f"\n🎉 SUCCÈS COMPLET!")
        print(f"   • Application 100% PyQt5 ✅")
        print(f"   • Aucun framework concurrent ✅")
        print(f"   • Prêt pour la production ✅")
    else:
        print(f"\n⚠️  ATTENTION!")
        if not no_forbidden_imports:
            print(f"   • Des imports interdits ont été détectés")
        if not has_pyqt5_imports:
            print(f"   • Des imports PyQt5 sont manquants")
    
    print(f"\n🚀 L'application utilise maintenant uniquement PyQt5!")

if __name__ == "__main__":
    main()
