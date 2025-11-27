#!/usr/bin/env python3
"""
Script de diagnostic pour les problèmes PyQt6 sur Windows
"""

import sys
import os
import platform
import subprocess

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_info(message):
    print(f"💡 {message}")

def check_system_info():
    print_header("INFORMATIONS SYSTÈME")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Machine: {platform.machine()}")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")

def check_virtual_env():
    print_header("ENVIRONNEMENT VIRTUEL")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_success("Environnement virtuel actif")
        print(f"Virtual env: {sys.prefix}")
    else:
        print_warning("Pas d'environnement virtuel détecté")

def check_qt_installation():
    print_header("VÉRIFICATION PYQT6")
    
    # Test d'importation PyQt6
    try:
        import PyQt6
        print_success(f"PyQt6 installé: {PyQt6.__file__}")
        
        try:
            from PyQt6 import QtCore
            print_success(f"QtCore importé: version Qt {QtCore.QT_VERSION_STR}")
        except Exception as e:
            print_error(f"Échec import QtCore: {e}")
            return False
            
        try:
            from PyQt6 import QtWidgets
            print_success("QtWidgets importé")
        except Exception as e:
            print_error(f"Échec import QtWidgets: {e}")
            
    except ImportError as e:
        print_error(f"PyQt6 non installé: {e}")
        return False
    
    return True

def check_pyside6_alternative():
    print_header("VÉRIFICATION PYSIDE6 (ALTERNATIVE)")
    
    try:
        import PySide6
        print_success(f"PySide6 disponible: {PySide6.__file__}")
        
        try:
            from PySide6 import QtCore
            print_success(f"PySide6 QtCore: version Qt {QtCore.QT_VERSION_STR}")
            return True
        except Exception as e:
            print_error(f"Échec import PySide6 QtCore: {e}")
            
    except ImportError:
        print_info("PySide6 non installé (alternative possible)")
    
    return False

def check_visual_cpp():
    print_header("VÉRIFICATION VISUAL C++ REDISTRIBUTABLE")
    
    # Vérifier les DLL Visual C++
    system32 = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32')
    
    required_dlls = [
        'msvcp140.dll',
        'vcruntime140.dll',
        'vcruntime140_1.dll'
    ]
    
    missing_dlls = []
    for dll in required_dlls:
        dll_path = os.path.join(system32, dll)
        if os.path.exists(dll_path):
            print_success(f"Trouvé: {dll}")
        else:
            print_error(f"Manquant: {dll}")
            missing_dlls.append(dll)
    
    if missing_dlls:
        print_warning("DLL Visual C++ manquantes")
        print_info("Téléchargez: https://aka.ms/vs/17/release/vc_redist.x64.exe")
        return False
    
    return True

def suggest_solutions():
    print_header("SOLUTIONS RECOMMANDÉES")
    
    print("1. 🔧 Réinstaller PyQt6:")
    print("   pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip")
    print("   pip install PyQt6==6.6.1")
    print()
    
    print("2. 📦 Installer Visual C++ Redistributable:")
    print("   https://aka.ms/vs/17/release/vc_redist.x64.exe")
    print()
    
    print("3. 🔄 Alternative PySide6:")
    print("   pip uninstall PyQt6")
    print("   pip install PySide6")
    print()
    
    print("4. 🐍 Recréer l'environnement virtuel:")
    print("   rmdir /s venv")
    print("   python -m venv venv")
    print("   venv\\Scripts\\activate.bat")
    print("   pip install -r requirements.txt")

def main():
    print_header("DIAGNOSTIC PYQT6 WINDOWS")
    
    check_system_info()
    check_virtual_env()
    
    qt_works = check_qt_installation()
    pyside_works = check_pyside6_alternative()
    vcpp_ok = check_visual_cpp()
    
    print_header("RÉSUMÉ")
    
    if qt_works:
        print_success("PyQt6 fonctionne correctement")
    elif pyside_works:
        print_warning("PyQt6 ne fonctionne pas, mais PySide6 est disponible")
    else:
        print_error("Ni PyQt6 ni PySide6 ne fonctionnent")
        
    if not vcpp_ok:
        print_error("Problème avec Visual C++ Redistributable")
    
    if not qt_works:
        suggest_solutions()

if __name__ == "__main__":
    main()
