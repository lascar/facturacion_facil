#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour exécuter les tests de comportement
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def run_behaviour_tests(test_file=None, headless=False, screenshots=False, slow=False, verbose=False):
    """Exécuter les tests de comportement avec les options spécifiées"""
    
    # Répertoire des tests de comportement
    behaviour_dir = Path(__file__).parent
    
    # Commande de base
    cmd = [sys.executable, "-m", "pytest"]
    
    # Ajouter le répertoire ou fichier de test
    if test_file:
        test_path = behaviour_dir / test_file
        if not test_path.exists():
            print(f"❌ Fichier de test non trouvé: {test_path}")
            return False
        cmd.append(str(test_path))
    else:
        cmd.append(str(behaviour_dir))
    
    # Options pytest
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Options personnalisées
    if headless:
        cmd.append("--headless")
    
    if screenshots:
        cmd.append("--screenshots")
    
    if slow:
        cmd.append("--slow")
    
    # Options supplémentaires
    cmd.extend([
        "--tb=short",  # Traceback court
        "-x",          # Arrêter au premier échec
        "--disable-warnings"  # Désactiver les warnings
    ])
    
    print(f"🚀 Exécution des tests de comportement...")
    print(f"📁 Répertoire: {behaviour_dir}")
    print(f"🔧 Commande: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        # Exécuter les tests
        result = subprocess.run(cmd, cwd=behaviour_dir.parent.parent, capture_output=False)
        
        if result.returncode == 0:
            print("=" * 60)
            print("✅ Tous les tests de comportement ont réussi!")
            return True
        else:
            print("=" * 60)
            print(f"❌ Tests échoués (code de retour: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des tests: {e}")
        return False

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Exécuter les tests de comportement Selenium")
    
    parser.add_argument(
        "test_file",
        nargs="?",
        help="Fichier de test spécifique à exécuter (ex: test_main_window_behaviour.py)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Exécuter en mode headless (sans interface graphique)"
    )
    
    parser.add_argument(
        "--screenshots",
        action="store_true",
        help="Prendre des captures d'écran en cas d'échec"
    )
    
    parser.add_argument(
        "--slow",
        action="store_true",
        help="Exécuter lentement pour le débogage"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mode verbeux"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lister les tests disponibles"
    )
    
    args = parser.parse_args()
    
    if args.list:
        # Lister les fichiers de test disponibles
        behaviour_dir = Path(__file__).parent
        test_files = list(behaviour_dir.glob("test_*.py"))
        
        print("📋 Tests de comportement disponibles:")
        print("=" * 40)
        for test_file in sorted(test_files):
            print(f"  • {test_file.name}")
        print("=" * 40)
        print(f"Total: {len(test_files)} fichiers de test")
        return
    
    # Exécuter les tests
    success = run_behaviour_tests(
        test_file=args.test_file,
        headless=args.headless,
        screenshots=args.screenshots,
        slow=args.slow,
        verbose=args.verbose
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
