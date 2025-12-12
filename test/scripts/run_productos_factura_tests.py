#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour exécuter les tests de produits dans les facturas
"""

import sys
import os
import subprocess

# Essayer d'importer pytest, mais continuer sans si pas disponible
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    print("⚠️  pytest non disponible, utilisation de tests simples")

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def run_unit_tests():
    """Exécuter les tests unitaires de produits"""
    print("🧪 Exécution des tests unitaires de produits...")
    
    test_file = os.path.join(os.path.dirname(__file__), '..', 'unit', 'test_productos_factura.py')
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            test_file,
            '-v',
            '--tb=short',
            '--color=yes'
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests unitaires: {e}")
        return False

def run_integration_tests():
    """Exécuter les tests d'intégration de produits"""
    print("🔗 Exécution des tests d'intégration de produits...")
    
    test_file = os.path.join(os.path.dirname(__file__), '..', 'integration', 'test_productos_factura_integration.py')
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            test_file,
            '-v',
            '--tb=short',
            '--color=yes',
            '-m', 'not slow'  # Exclure les tests lents par défaut
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests d'intégration: {e}")
        return False

def run_all_productos_tests():
    """Exécuter tous les tests de produits"""
    print("🚀 Exécution de tous les tests de produits...")
    
    test_pattern = os.path.join(os.path.dirname(__file__), '..', '**', '*productos_factura*.py')
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            test_pattern,
            '-v',
            '--tb=short',
            '--color=yes',
            '-m', 'not slow'
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de tous les tests: {e}")
        return False

def run_specific_test(test_name):
    """Exécuter un test spécifique"""
    print(f"🎯 Exécution du test spécifique: {test_name}")
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            '-k', test_name,
            '-v',
            '--tb=short',
            '--color=yes'
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..', '..'))
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution du test {test_name}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧪 SCRIPT DE TESTS PRODUCTOS FACTURA")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "unit":
            success = run_unit_tests()
        elif command == "integration":
            success = run_integration_tests()
        elif command == "all":
            success = run_all_productos_tests()
        elif command.startswith("test_"):
            success = run_specific_test(command)
        else:
            print(f"❌ Commande inconnue: {command}")
            print("Commandes disponibles: unit, integration, all, test_<nom_du_test>")
            return 1
    else:
        # Par défaut, exécuter les tests unitaires
        print("Aucune commande spécifiée, exécution des tests unitaires...")
        success = run_unit_tests()
    
    print("=" * 50)
    if success:
        print("✅ TOUS LES TESTS ONT RÉUSSI")
        return 0
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
