#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification pour détecter les tests qui utilisent les fichiers de production
🛡️ PROTECTION CRITIQUE: Empêcher l'utilisation de la base de production et config.json dans les tests
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Couleurs pour l'affichage
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

# Patterns dangereux à détecter
DANGEROUS_PATTERNS = [
    # Base de données
    (r'Database\(\s*\)', 'Database() sans paramètre - utilise la base de production par défaut'),
    (r'Database\(\s*["\']base_de_datos/facturacion\.db["\']', 'Database() avec chemin de production explicite'),
    (r'from database\.database import db(?!\s*#)', 'Import de l\'instance globale db sans protection'),
    (r'["\']base_de_datos/facturacion\.db["\']', 'Référence directe au chemin de la base de production'),

    # Configuration
    (r'["\']config/config\.json["\']', 'Accès direct à config/config.json de production'),
    (r'open\(["\']config\.json["\']', 'Ouverture directe de config.json'),
    (r'json\.load.*config\.json', 'Chargement direct de config.json'),
    (r'json\.dump.*config\.json', 'Écriture directe dans config.json'),
]

# Fichiers à ignorer (fichiers de configuration, documentation, etc.)
IGNORE_FILES = {
    'conftest.py',
    'test_database_manager.py',
    '__init__.py',
    'verify_no_production_db_usage.py',  # Ce script lui-même
}

# Répertoires à ignorer
IGNORE_DIRS = {
    '__pycache__',
    '.pytest_cache',
    'htmlcov',
}


def find_dangerous_patterns_in_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Recherche les patterns dangereux dans un fichier

    Returns:
        Liste de tuples (numéro_ligne, pattern_trouvé, description)
    """
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Ignorer les commentaires
                if line.strip().startswith('#'):
                    continue

                # Ignorer les lignes qui sont des strings (dans des regex, etc.)
                if line.strip().startswith(('r"', "r'", '"', "'")):
                    continue

                # Ignorer TestDatabase() qui est la classe de test (pas Database())
                if 'TestDatabase()' in line:
                    continue

                for pattern, description in DANGEROUS_PATTERNS:
                    if re.search(pattern, line):
                        issues.append((line_num, line.strip(), description))

    except Exception as e:
        print(f"{YELLOW}⚠️  Erreur lecture {file_path}: {e}{NC}")

    return issues


def scan_test_directory(test_dir: Path) -> dict:
    """
    Scanne tous les fichiers de test pour détecter les usages dangereux
    
    Returns:
        Dictionnaire {fichier: [(ligne, code, description), ...]}
    """
    results = {}
    
    for root, dirs, files in os.walk(test_dir):
        # Filtrer les répertoires à ignorer
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if not file.endswith('.py'):
                continue
            
            if file in IGNORE_FILES:
                continue
            
            file_path = Path(root) / file
            issues = find_dangerous_patterns_in_file(file_path)
            
            if issues:
                results[file_path] = issues
    
    return results


def print_report(results: dict) -> bool:
    """
    Affiche le rapport de vérification

    Returns:
        True si aucun problème trouvé, False sinon
    """
    print(f"\n{BLUE}🔍 === VÉRIFICATION USAGE FICHIERS DE PRODUCTION ==={NC}\n")

    if not results:
        print(f"{GREEN}✅ AUCUN PROBLÈME DÉTECTÉ{NC}")
        print(f"{GREEN}   Tous les tests utilisent correctement les fixtures de test{NC}\n")
        return True

    print(f"{RED}❌ PROBLÈMES DÉTECTÉS: {len(results)} fichier(s){NC}\n")

    for file_path, issues in results.items():
        print(f"{YELLOW}📄 {file_path}{NC}")

        for line_num, code, description in issues:
            print(f"   {RED}Ligne {line_num}:{NC} {description}")
            print(f"   {BLUE}Code:{NC} {code}")
            print()

    print(f"{RED}⚠️  ACTIONS REQUISES:{NC}")
    print(f"   1. Corriger les fichiers listés ci-dessus")
    print(f"   2. Utiliser les fixtures de test (temp_db, unit_db, integration_db)")
    print(f"   3. Remplacer Database() par self.db dans les tests")
    print(f"   4. NE PAS accéder directement à config/config.json")
    print(f"   5. Relancer ce script pour vérifier\n")

    return False


def main():
    """Point d'entrée principal"""
    # Trouver le répertoire racine du projet
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    test_dir = project_root / 'test'
    
    if not test_dir.exists():
        print(f"{RED}❌ Répertoire de tests non trouvé: {test_dir}{NC}")
        sys.exit(1)
    
    print(f"{BLUE}📁 Scan du répertoire: {test_dir}{NC}")
    
    # Scanner les fichiers de test
    results = scan_test_directory(test_dir)
    
    # Afficher le rapport
    success = print_report(results)
    
    # Code de sortie
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

