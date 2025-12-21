#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour réparer les erreurs de syntaxe causées par la désactivation des messages de debug
"""

import os
import re

def fix_syntax_errors_in_file(filepath):
    """Répare les erreurs de syntaxe dans un fichier"""
    if not os.path.exists(filepath):
        print(f"⚠️ Fichier non trouvé: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Patterns de réparation
        fixes = [
            # Try sans contenu suivi d'une fonction
            (r'try:\s*\n\s*# DEBUG désactivé\s*\n\s*# DEBUG désactivé\s*\n\s*def ', r'# DEBUG désactivé\n    # DEBUG désactivé\n    def '),
            
            # Try sans contenu suivi d'except
            (r'try:\s*\n\s*# DEBUG désactivé\s*\n\s*# DEBUG désactivé\s*\n\s*except', r'try:\n        pass\n    except'),
            
            # Except orphelin
            (r'^\s*except Exception as e:\s*\n(?=\s*def|\s*class|\s*$)', r'', re.MULTILINE),
            
            # Try sans contenu à la fin d'un bloc
            (r'try:\s*\n\s*# DEBUG désactivé\s*\n\s*# DEBUG désactivé\s*\n\s*$', r'# DEBUG désactivé\n    # DEBUG désactivé'),
        ]
        
        modified = False
        for pattern, replacement, *flags in fixes:
            flag = flags[0] if flags else 0
            new_content = re.sub(pattern, replacement, content, flags=flag)
            if new_content != content:
                content = new_content
                modified = True
        
        # Vérifications spécifiques pour custom_dialogs.py
        if 'custom_dialogs.py' in filepath:
            # Réparer les structures try/except cassées
            content = re.sub(
                r'try:\s*\n\s*# DEBUG désactivé\s*\n\s*# DEBUG désactivé\s*\n\s*def ',
                r'# DEBUG désactivé\n        # DEBUG désactivé\n        pass\n\n    def ',
                content
            )
            
            # Réparer les try sans except
            content = re.sub(
                r'try:\s*\n\s*# DEBUG désactivé\s*\n\s*# DEBUG désactivé\s*\n(?=\s*def|\s*class)',
                r'# DEBUG désactivé\n        # DEBUG désactivé\n',
                content
            )
        
        if modified or content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filepath}: Erreurs de syntaxe réparées")
            return True
        else:
            print(f"ℹ️ {filepath}: Aucune erreur à réparer")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec {filepath}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 RÉPARATION DES ERREURS DE SYNTAXE")
    print("="*60)
    
    # Fichiers à traiter
    files_to_fix = [
        "common/custom_dialogs.py",
        "ui/stock.py",
        "ui/productos.py",
        "ui/facturas.py",
        "ui/organizacion.py",
        "ui/clientes.py"
    ]
    
    fixed_count = 0
    
    for filepath in files_to_fix:
        if fix_syntax_errors_in_file(filepath):
            fixed_count += 1
    
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    print(f"Fichiers traités: {len(files_to_fix)}")
    print(f"Fichiers réparés: {fixed_count}")
    
    if fixed_count > 0:
        print("\n✅ Erreurs de syntaxe réparées avec succès !")
        print("🚀 Testez l'application maintenant:")
        print("   python main.py")
    else:
        print("\nℹ️ Aucune erreur de syntaxe à réparer")
    
    return 0

if __name__ == "__main__":
    exit(main())
