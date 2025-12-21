#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour désactiver les messages de debug verbeux
"""

import os
import re

def disable_debug_in_file(filepath):
    """Désactive les messages de debug dans un fichier"""
    if not os.path.exists(filepath):
        print(f"⚠️ Fichier non trouvé: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les lignes de debug avant
        debug_lines_before = len(re.findall(r'print\(f?"?🔍 DEBUG:', content))
        
        # Remplacer les print de debug par des commentaires
        patterns = [
            (r'print\(f?"?🔍 DEBUG:.*?\)"?\)', r'# DEBUG désactivé'),
            (r'print\(f?"?✅ DEBUG:.*?\)"?\)', r'# DEBUG désactivé'),
            (r'print\(f?"?❌ DEBUG:.*?\)"?\)', r'# DEBUG désactivé'),
        ]
        
        modified = False
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            if new_content != content:
                content = new_content
                modified = True
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            debug_lines_after = len(re.findall(r'print\(f?"?🔍 DEBUG:', content))
            print(f"✅ {filepath}: {debug_lines_before - debug_lines_after} lignes de debug désactivées")
            return True
        else:
            print(f"ℹ️ {filepath}: Aucun debug à désactiver")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec {filepath}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔇 DÉSACTIVATION DES MESSAGES DE DEBUG VERBEUX")
    print("="*60)
    
    # Fichiers à traiter
    files_to_process = [
        "common/custom_dialogs.py",
        "ui/productos.py",
        "ui/stock.py",
        "ui/facturas.py",
        "ui/organizacion.py",
        "ui/clientes.py"
    ]
    
    modified_count = 0
    
    for filepath in files_to_process:
        if disable_debug_in_file(filepath):
            modified_count += 1
    
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    print(f"Fichiers traités: {len(files_to_process)}")
    print(f"Fichiers modifiés: {modified_count}")
    
    if modified_count > 0:
        print("\n✅ Messages de debug désactivés avec succès !")
        print("🚀 Relancez l'application pour voir la différence:")
        print("   python main.py")
    else:
        print("\nℹ️ Aucun message de debug à désactiver")
    
    return 0

if __name__ == "__main__":
    exit(main())
