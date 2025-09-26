#!/usr/bin/env python3
"""
Script pour migrer tous les tests vers le nouveau système de base de données isolée
Remplace les anciennes fixtures temp_db locales par l'utilisation du système centralisé
"""

import os
import re
import glob
from pathlib import Path

def find_test_files():
    """Trouver tous les fichiers de test"""
    test_files = []
    
    # Chercher dans tous les répertoires de test
    patterns = [
        "test/**/*.py",
        "tests/**/*.py"
    ]
    
    for pattern in patterns:
        test_files.extend(glob.glob(pattern, recursive=True))
    
    # Filtrer les fichiers Python de test
    test_files = [f for f in test_files if f.endswith('.py') and ('test_' in f or f.endswith('_test.py'))]
    
    return test_files

def analyze_test_file(file_path):
    """Analyser un fichier de test pour détecter les problèmes"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Détecter les fixtures temp_db locales
        if re.search(r'@pytest\.fixture\s+def temp_db\(', content):
            issues.append("LOCAL_TEMP_DB_FIXTURE")
        
        # Détecter les créations manuelles de DB temporaires
        if re.search(r'tempfile\.mkstemp.*\.db', content):
            issues.append("MANUAL_TEMP_DB_CREATION")
        
        # Détecter les NamedTemporaryFile pour DB
        if re.search(r'NamedTemporaryFile.*\.db', content):
            issues.append("NAMED_TEMP_FILE_DB")
        
        # Détecter les Database() directes dans les tests
        if re.search(r'Database\(["\'].*\.db["\']', content):
            issues.append("DIRECT_DATABASE_CREATION")
        
        # Détecter les manipulations manuelles de db global
        if re.search(r'monkeypatch\.setattr.*database\.db', content):
            issues.append("MANUAL_DB_PATCHING")
        
        return issues
        
    except Exception as e:
        return [f"ERROR_READING_FILE: {e}"]

def suggest_migration(file_path, issues):
    """Suggérer des migrations pour un fichier"""
    suggestions = []
    
    if "LOCAL_TEMP_DB_FIXTURE" in issues:
        suggestions.append(
            "• Supprimer la fixture temp_db locale et utiliser celle du conftest.py global"
        )
    
    if "MANUAL_TEMP_DB_CREATION" in issues:
        suggestions.append(
            "• Remplacer tempfile.mkstemp par test_db_manager.create_test_database()"
        )
    
    if "NAMED_TEMP_FILE_DB" in issues:
        suggestions.append(
            "• Remplacer NamedTemporaryFile par isolated_test_db() context manager"
        )
    
    if "DIRECT_DATABASE_CREATION" in issues:
        suggestions.append(
            "• Utiliser la fixture temp_db au lieu de créer Database() directement"
        )
    
    if "MANUAL_DB_PATCHING" in issues:
        suggestions.append(
            "• Le patching de database.db est maintenant automatique via setup_test_environment"
        )
    
    return suggestions

def migrate_file(file_path):
    """Migrer un fichier vers le nouveau système"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Migration 1: Supprimer les fixtures temp_db locales
        content = re.sub(
            r'@pytest\.fixture\s+def temp_db\(.*?\):\s*""".*?""".*?yield.*?os\.unlink.*?\n',
            '# Utiliser la fixture temp_db globale du conftest.py\n',
            content,
            flags=re.DOTALL
        )
        
        # Migration 2: Remplacer les créations manuelles
        content = re.sub(
            r'tempfile\.mkstemp\(.*?suffix=["\']\.db["\'].*?\)',
            'test_db_manager.create_test_database()',
            content
        )
        
        # Migration 3: Ajouter les imports nécessaires si pas présents
        if 'test_db_manager' in content and 'from test.utils.test_database_manager import' not in content:
            # Ajouter l'import après les autres imports
            import_line = "from test.utils.test_database_manager import test_db_manager, isolated_test_db\n"
            
            # Trouver la fin des imports
            lines = content.split('\n')
            import_end = 0
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    import_end = i
            
            lines.insert(import_end + 1, import_line)
            content = '\n'.join(lines)
        
        # Sauvegarder seulement si des changements ont été faits
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Erreur migration {file_path}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔄 Migration des tests vers le système de base de données isolée")
    print("=" * 70)
    
    # Trouver tous les fichiers de test
    test_files = find_test_files()
    print(f"📁 Fichiers de test trouvés: {len(test_files)}")
    
    # Analyser chaque fichier
    files_with_issues = []
    total_issues = 0
    
    for file_path in test_files:
        issues = analyze_test_file(file_path)
        if issues and not any(issue.startswith("ERROR_") for issue in issues):
            files_with_issues.append((file_path, issues))
            total_issues += len(issues)
    
    print(f"⚠️ Fichiers nécessitant une migration: {len(files_with_issues)}")
    print(f"🔧 Total des problèmes détectés: {total_issues}")
    
    if not files_with_issues:
        print("✅ Tous les tests utilisent déjà le système de DB isolée !")
        return
    
    # Afficher les problèmes détectés
    print("\n📋 Analyse des problèmes:")
    for file_path, issues in files_with_issues:
        print(f"\n📄 {file_path}")
        for issue in issues:
            print(f"   ⚠️ {issue}")
        
        suggestions = suggest_migration(file_path, issues)
        if suggestions:
            print("   💡 Suggestions:")
            for suggestion in suggestions:
                print(f"      {suggestion}")
    
    # Demander confirmation pour la migration automatique
    print(f"\n🤖 Migration automatique disponible pour certains problèmes.")
    response = input("Voulez-vous procéder à la migration automatique ? (y/N): ")
    
    if response.lower() in ['y', 'yes', 'oui']:
        print("\n🔄 Migration en cours...")
        migrated_count = 0
        
        for file_path, issues in files_with_issues:
            if migrate_file(file_path):
                migrated_count += 1
                print(f"✅ Migré: {file_path}")
            else:
                print(f"⏭️ Aucun changement: {file_path}")
        
        print(f"\n🎉 Migration terminée: {migrated_count}/{len(files_with_issues)} fichiers migrés")
        
        if migrated_count > 0:
            print("\n💡 Recommandations post-migration:")
            print("   1. Exécuter les tests pour vérifier que tout fonctionne")
            print("   2. Réviser manuellement les fichiers migrés")
            print("   3. Supprimer les imports inutiles")
            print("   4. Ajouter des marqueurs pytest si nécessaire (@pytest.mark.isolated_db)")
    
    else:
        print("\n⏭️ Migration automatique annulée")
        print("💡 Vous pouvez migrer manuellement en suivant les suggestions ci-dessus")
    
    print(f"\n📚 Documentation du nouveau système:")
    print(f"   • Fixtures disponibles: temp_db, isolated_db, clean_db, isolated_environment")
    print(f"   • Context managers: isolated_test_db(), isolated_test_environment()")
    print(f"   • Marqueurs: @pytest.mark.isolated_db, @pytest.mark.clean_db")
    print(f"   • Nettoyage automatique après chaque test")

if __name__ == "__main__":
    main()
