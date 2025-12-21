#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les tests de comportement et ajouter la fermeture automatique
"""

import os
import re
import glob

def fix_test_file(file_path):
    """Corriger un fichier de test pour ajouter la fermeture automatique"""
    
    print(f"🔧 Correction de {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Remplacer les appels directs à window.close() par la fermeture automatique
        patterns_to_fix = [
            # Pattern: stock_window.close()
            (r'(\s+)(\w+_window)\.close\(\)\s*\n(\s+)self\.wait_and_process_events\(\d+\)',
             r'\1# Fermeture automatique gérée par teardown_method()\n\1self.wait_and_process_events(500)'),
            
            # Pattern: window.close() suivi d'un wait
            (r'(\s+)(\w+)\.close\(\)\s*\n(\s+)self\.wait_and_process_events\(\d+\)',
             r'\1# Fermeture automatique gérée par teardown_method()\n\1self.wait_and_process_events(500)'),
            
            # Pattern: simple window.close()
            (r'(\s+)(\w+_window)\.close\(\)\s*$',
             r'\1# Fermeture automatique gérée par teardown_method()'),
        ]
        
        for pattern, replacement in patterns_to_fix:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        # 2. Ajouter un commentaire explicatif au début des méthodes de test
        test_method_pattern = r'(\s+def test_\w+\(self[^)]*\):\s*\n)(\s+"""[^"]*"""\s*\n)?'
        
        def add_auto_close_comment(match):
            method_def = match.group(1)
            docstring = match.group(2) if match.group(2) else ""
            
            comment = f'{method_def}{docstring}        # Note: Les fenêtres se ferment automatiquement via teardown_method()\n'
            return comment
        
        content = re.sub(test_method_pattern, add_auto_close_comment, content)
        
        # 3. Remplacer les longues attentes par des attentes plus courtes
        content = re.sub(r'self\.wait_and_process_events\((\d{4,})\)', 
                        r'self.wait_and_process_events(1000)', content)
        
        # 4. Ajouter un import pour QTimer si nécessaire
        if 'QTimer' not in content and 'from PyQt5.QtCore import' in content:
            content = re.sub(r'from PyQt5\.QtCore import ([^QTimer\n]*)',
                           r'from PyQt5.QtCore import \1, QTimer', content)

        # 5. Ajouter l'activation du mode test au début des classes de test
        if 'class Test' in content and 'PYTEST_RUNNING' not in content:
            setup_method_pattern = r'(\s+def setup_method\(self[^)]*\):\s*\n)'

            def add_test_mode(match):
                method_def = match.group(1)
                test_mode_code = f'''{method_def}        """Configuration avant chaque test"""
        # Activer le mode test pour éviter les boîtes de dialogue
        import os
        os.environ['PYTEST_RUNNING'] = '1'

'''
                return test_mode_code

            content = re.sub(setup_method_pattern, add_test_mode, content)
        
        # Sauvegarder seulement si des changements ont été faits
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Fichier corrigé")
            return True
        else:
            print(f"   ℹ️ Aucune correction nécessaire")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 CORRECTION DES TESTS DE COMPORTEMENT")
    print("=" * 50)
    
    # Trouver tous les fichiers de test de comportement
    test_files = []
    
    # Tests dans test/behaviour/
    behaviour_dir = "test/behaviour"
    if os.path.exists(behaviour_dir):
        test_files.extend(glob.glob(os.path.join(behaviour_dir, "test_*.py")))
    
    # Tests à la racine qui utilisent PyQt5
    root_test_files = glob.glob("test_*behaviour*.py")
    test_files.extend(root_test_files)
    
    if not test_files:
        print("❌ Aucun fichier de test trouvé")
        return
    
    print(f"📁 {len(test_files)} fichiers de test trouvés:")
    for file_path in test_files:
        print(f"   • {file_path}")
    
    print("\n🔧 Correction en cours...")
    
    fixed_count = 0
    for file_path in test_files:
        if fix_test_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ CORRECTION TERMINÉE")
    print(f"   📊 {fixed_count}/{len(test_files)} fichiers corrigés")
    
    print(f"\n📋 RÉSUMÉ DES CORRECTIONS:")
    print(f"   ✅ Suppression des appels manuels à window.close()")
    print(f"   ✅ Ajout de commentaires explicatifs")
    print(f"   ✅ Réduction des temps d'attente")
    print(f"   ✅ La fermeture automatique est gérée par teardown_method()")
    
    print(f"\n🚀 PROCHAINES ÉTAPES:")
    print(f"   1. Tester les corrections avec: pytest test/behaviour/ -v")
    print(f"   2. Vérifier qu'aucune fenêtre ne reste ouverte")
    print(f"   3. Les fenêtres se ferment automatiquement après chaque test")

if __name__ == '__main__':
    main()
