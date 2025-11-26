#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de compatibilité Windows 11 pour Facturación Fácil
Vérifie que toutes les dépendances et fonctionnalités sont compatibles avec Windows 11
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def print_header(title):
    """Affiche un en-tête formaté"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def check_windows_version():
    """Vérifie la version de Windows"""
    print_header("VÉRIFICATION DE LA VERSION WINDOWS")
    
    system = platform.system()
    release = platform.release()
    version = platform.version()
    
    print(f"Système: {system}")
    print(f"Version: {release}")
    print(f"Build: {version}")
    
    if system != "Windows":
        print("❌ Ce test est conçu pour Windows uniquement")
        return False
    
    # Vérifier si c'est Windows 10 ou 11
    build_number = int(version.split('.')[-1]) if version else 0
    
    if build_number >= 22000:
        print("✅ Windows 11 détecté")
        return True
    elif build_number >= 10240:
        print("✅ Windows 10 détecté (compatible)")
        return True
    else:
        print("⚠️ Version Windows ancienne détectée")
        return False

def check_python_version():
    """Vérifie la version de Python"""
    print_header("VÉRIFICATION DE PYTHON")
    
    version = sys.version_info
    print(f"Version Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✅ Version Python compatible avec Windows 11")
        return True
    elif version.major == 3 and version.minor >= 8:
        print("⚠️ Version Python compatible mais non optimale pour Windows 11")
        return True
    else:
        print("❌ Version Python trop ancienne")
        return False

def check_dependencies():
    """Vérifie les dépendances principales"""
    print_header("VÉRIFICATION DES DÉPENDANCES")
    
    dependencies = [
        ('PyQt6', 'PyQt6'),
        ('customtkinter', 'customtkinter'),
        ('Pillow', 'PIL'),
        ('reportlab', 'reportlab'),
    ]
    
    all_ok = True
    
    for name, import_name in dependencies:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'Version inconnue')
            print(f"✅ {name}: {version}")
        except ImportError:
            print(f"❌ {name}: Non installé")
            all_ok = False
        except Exception as e:
            print(f"⚠️ {name}: Erreur - {e}")
            all_ok = False
    
    return all_ok

def check_pyqt6_functionality():
    """Teste les fonctionnalités PyQt6"""
    print_header("TEST PYQT6")
    
    try:
        from PyQt6.QtWidgets import QApplication, QWidget, QLabel
        from PyQt6.QtCore import Qt
        
        # Créer une application test (sans affichage)
        app = QApplication([])
        
        # Tester la création d'un widget
        widget = QWidget()
        label = QLabel("Test Windows 11", widget)
        
        print("✅ PyQt6 fonctionne correctement")
        
        # Nettoyer
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ Erreur PyQt6: {e}")
        return False

def check_file_structure():
    """Vérifie la structure des fichiers"""
    print_header("VÉRIFICATION DE LA STRUCTURE")
    
    required_files = [
        'main.py',
        'requirements.txt',
        'main.spec',
        'ui/',
        'database/',
        'utils/',
        'assets/',
    ]
    
    all_ok = True
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} manquant")
            all_ok = False
    
    return all_ok

def check_build_requirements():
    """Vérifie les outils de construction"""
    print_header("VÉRIFICATION DES OUTILS DE BUILD")
    
    try:
        import PyInstaller
        print(f"✅ PyInstaller: {PyInstaller.__version__}")
        build_ok = True
    except ImportError:
        print("❌ PyInstaller non installé")
        print("💡 Installer avec: pip install pyinstaller")
        build_ok = False
    
    return build_ok

def run_compatibility_test():
    """Exécute tous les tests de compatibilité"""
    print("🪟 TEST DE COMPATIBILITÉ WINDOWS 11 - FACTURACIÓN FÁCIL")
    print("="*60)
    
    tests = [
        ("Version Windows", check_windows_version),
        ("Version Python", check_python_version),
        ("Dépendances", check_dependencies),
        ("Fonctionnalité PyQt6", check_pyqt6_functionality),
        ("Structure des fichiers", check_file_structure),
        ("Outils de build", check_build_requirements),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé final
    print_header("RÉSUMÉ DES TESTS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHEC"
        print(f"{test_name}: {status}")
    
    print(f"\nRésultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 TOUS LES TESTS RÉUSSIS - Compatible Windows 11!")
        return True
    else:
        print("⚠️ Certains tests ont échoué - Vérifiez les erreurs ci-dessus")
        return False

if __name__ == "__main__":
    try:
        success = run_compatibility_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
