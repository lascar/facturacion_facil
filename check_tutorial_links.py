#!/usr/bin/env python3
"""
Script pour vérifier tous les liens dans les fichiers HTML du tutorial
et identifier les fichiers manquants.
"""

import os
import re
from pathlib import Path

def extract_html_links(file_path):
    """Extrait tous les liens href vers des fichiers .html d'un fichier HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern pour trouver tous les liens href vers des fichiers .html
        pattern = r'href="([^"]*\.html)"'
        links = re.findall(pattern, content)
        return links
    except Exception as e:
        print(f"Erreur lors de la lecture de {file_path}: {e}")
        return []

def check_tutorial_links():
    """Vérifie tous les liens dans le dossier tutorial_html"""
    tutorial_dir = Path("doc/tutorial_html")
    
    if not tutorial_dir.exists():
        print(f"Le dossier {tutorial_dir} n'existe pas!")
        return
    
    # Obtenir tous les fichiers HTML existants
    existing_files = set()
    for file_path in tutorial_dir.glob("*.html"):
        existing_files.add(file_path.name)
    
    print("📁 Fichiers HTML existants:")
    for file in sorted(existing_files):
        print(f"  ✅ {file}")
    
    print("\n" + "="*60)
    
    # Analyser chaque fichier HTML
    broken_links = {}
    all_referenced_files = set()
    
    for html_file in tutorial_dir.glob("*.html"):
        print(f"\n🔍 Analyse de {html_file.name}:")
        
        links = extract_html_links(html_file)
        file_broken_links = []
        
        for link in links:
            all_referenced_files.add(link)
            if link not in existing_files:
                file_broken_links.append(link)
                print(f"  ❌ LIEN BRISÉ: {link}")
            else:
                print(f"  ✅ {link}")
        
        if file_broken_links:
            broken_links[html_file.name] = file_broken_links
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES LIENS BRISÉS:")
    
    if broken_links:
        for file, links in broken_links.items():
            print(f"\n❌ {file}:")
            for link in links:
                print(f"  → {link}")
    else:
        print("✅ Aucun lien brisé trouvé!")
    
    print("\n" + "="*60)
    print("📋 FICHIERS RÉFÉRENCÉS MAIS MANQUANTS:")
    
    missing_files = all_referenced_files - existing_files
    if missing_files:
        for file in sorted(missing_files):
            print(f"  ❌ {file}")
    else:
        print("✅ Tous les fichiers référencés existent!")
    
    return broken_links, missing_files

if __name__ == "__main__":
    print("🔍 Vérification des liens du tutorial HTML...")
    print("="*60)
    
    broken_links, missing_files = check_tutorial_links()
    
    print(f"\n📈 STATISTIQUES:")
    print(f"  • Fichiers avec liens brisés: {len(broken_links)}")
    print(f"  • Fichiers manquants au total: {len(missing_files)}")
