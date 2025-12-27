#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour corriger les warnings PytestReturnNotNoneWarning
Remplace 'return True' par 'assert True' dans les fonctions de test
"""

import os
import re
from pathlib import Path

def fix_test_file(filepath):
    """Corriger un fichier de test"""
    print(f"📝 Traitement de {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes = 0

    # Pattern pour trouver les fonctions de test qui retournent True/False
    lines = content.split('\n')
    new_lines = []
    in_test_function = False
    current_indent = 0

    for i, line in enumerate(lines):
        # Détecter le début d'une fonction de test
        if re.match(r'\s*def test_', line):
            in_test_function = True
            current_indent = len(re.match(r'(\s*)', line).group(1))
            new_lines.append(line)
            continue

        # Détecter la fin d'une fonction (nouvelle fonction ou classe)
        if in_test_function and line.strip() and not line.startswith(' ' * (current_indent + 1)):
            if re.match(r'\s*(def |class )', line):
                in_test_function = False

        # Si on est dans une fonction de test et qu'on trouve "return True/False"
        if in_test_function and re.search(r'\s+return (True|False)\s*$', line):
            indent = re.match(r'(\s*)', line).group(1)
            value = re.search(r'return (True|False)', line).group(1)

            # Remplacer par assert
            if value == "True":
                new_line = f"{indent}assert True"
            else:
                # Pour False, ajouter un message d'erreur si possible
                new_line = f"{indent}assert False, \"Test failed\""

            new_lines.append(new_line)
            changes += 1
            print(f"  ✅ Ligne {i+1}: '{line.strip()}' → '{new_line.strip()}'")
        else:
            new_lines.append(line)

    if changes > 0:
        new_content = '\n'.join(new_lines)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ {changes} changement(s) effectué(s)")
        return changes
    else:
        print(f"  ℹ️  Aucun changement nécessaire")
        return 0

def main():
    """Fonction principale"""
    print("🔧 Correction des warnings PytestReturnNotNoneWarning\n")
    
    # Liste des fichiers à corriger
    test_files = [
        "test/integration/test_pdf_download_feature.py",
        "test/integration/test_safe_organizacion_defaults_integration.py",
        "test/integration/test_visor_pdf_personalizado.py",
        "test/test_logo_resilience.py",
        "test/unit/test_file_manager.py",
        "test/unit/test_stock_migration.py",
        "test/unit/test_validacion_facturas_opcional.py",
        "test/unit/test_validate_form.py",
    ]
    
    total_changes = 0
    files_modified = 0
    
    for filepath in test_files:
        if os.path.exists(filepath):
            changes = fix_test_file(filepath)
            if changes > 0:
                files_modified += 1
                total_changes += changes
        else:
            print(f"⚠️  Fichier non trouvé: {filepath}")
        print()
    
    print(f"\n✅ Terminé!")
    print(f"   Fichiers modifiés: {files_modified}")
    print(f"   Total de changements: {total_changes}")

if __name__ == "__main__":
    main()

