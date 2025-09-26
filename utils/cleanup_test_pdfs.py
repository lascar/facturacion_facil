#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour nettoyer les PDFs générés par les tests
"""

import os
import glob
import tempfile
from datetime import datetime, timedelta


def cleanup_test_pdfs():
    """Nettoyer les PDFs générés par les tests"""
    print("🧹 Nettoyage des PDFs de test...")
    
    cleaned_count = 0
    total_size = 0
    
    # Répertoires à nettoyer
    directories_to_clean = [
        "pdfs",  # Répertoire par défaut
        "/tmp",  # Répertoires temporaires
        tempfile.gettempdir(),  # Répertoire temporaire système
    ]
    
    # Patterns de fichiers PDF de test
    test_pdf_patterns = [
        "**/Factura_*.pdf",
        "**/test_*.pdf", 
        "**/tmp*.pdf",
        "**/TEST-*.pdf",
        "**/VISOR-*.pdf",
        "**/Demo_*.pdf",
        "**/factura_*.pdf"
    ]
    
    for directory in directories_to_clean:
        if not os.path.exists(directory):
            continue
            
        print(f"\n📁 Nettoyage du répertoire: {directory}")
        
        for pattern in test_pdf_patterns:
            # Chercher les fichiers correspondant au pattern
            search_path = os.path.join(directory, pattern)
            pdf_files = glob.glob(search_path, recursive=True)
            
            for pdf_file in pdf_files:
                try:
                    # Vérifier que c'est bien un fichier PDF de test
                    if is_test_pdf(pdf_file):
                        file_size = os.path.getsize(pdf_file)
                        os.remove(pdf_file)
                        
                        cleaned_count += 1
                        total_size += file_size
                        
                        print(f"   🗑️  Supprimé: {os.path.basename(pdf_file)} ({file_size} bytes)")
                        
                except Exception as e:
                    print(f"   ❌ Erreur supprimant {pdf_file}: {e}")
    
    # Nettoyer les répertoires temporaires vides
    cleanup_empty_temp_dirs()
    
    print(f"\n📊 Résumé du nettoyage:")
    print(f"   🗑️  Fichiers supprimés: {cleaned_count}")
    print(f"   💾 Espace libéré: {total_size / 1024:.1f} KB")
    
    if cleaned_count == 0:
        print("   ✅ Aucun PDF de test trouvé - système déjà propre")
    else:
        print("   ✅ Nettoyage terminé avec succès")
    
    return cleaned_count


def is_test_pdf(pdf_path):
    """Vérifier si un PDF est un fichier de test"""
    filename = os.path.basename(pdf_path).lower()
    
    # Patterns de noms de fichiers de test
    test_indicators = [
        'test',
        'tmp',
        'demo',
        'visor-',
        'factura_test',
        'factura_demo'
    ]
    
    # Vérifier les patterns
    for indicator in test_indicators:
        if indicator in filename:
            return True
    
    # Vérifier si c'est un fichier récent (moins de 24h) dans un répertoire temporaire
    if '/tmp/' in pdf_path or tempfile.gettempdir() in pdf_path:
        try:
            file_time = datetime.fromtimestamp(os.path.getmtime(pdf_path))
            if datetime.now() - file_time < timedelta(hours=24):
                return True
        except:
            pass
    
    # Vérifier la taille (les PDFs de test sont généralement petits)
    try:
        file_size = os.path.getsize(pdf_path)
        if file_size < 10000:  # Moins de 10KB, probablement un test
            return True
    except:
        pass
    
    return False


def cleanup_empty_temp_dirs():
    """Nettoyer les répertoires temporaires vides"""
    print(f"\n📁 Nettoyage des répertoires temporaires vides...")
    
    temp_base = tempfile.gettempdir()
    cleaned_dirs = 0
    
    try:
        for item in os.listdir(temp_base):
            item_path = os.path.join(temp_base, item)
            
            # Vérifier si c'est un répertoire temporaire de test
            if (os.path.isdir(item_path) and 
                (item.startswith('tmp') or 'test' in item.lower())):
                
                try:
                    # Vérifier si le répertoire est vide
                    if not os.listdir(item_path):
                        os.rmdir(item_path)
                        cleaned_dirs += 1
                        print(f"   🗑️  Répertoire vide supprimé: {item}")
                except Exception as e:
                    # Ignorer les erreurs (répertoire peut être utilisé)
                    pass
    
    except Exception as e:
        print(f"   ⚠️  Erreur accédant aux répertoires temporaires: {e}")
    
    if cleaned_dirs > 0:
        print(f"   ✅ {cleaned_dirs} répertoires vides supprimés")
    else:
        print(f"   ✅ Aucun répertoire vide trouvé")


def cleanup_specific_test_files():
    """Nettoyer des fichiers de test spécifiques connus"""
    print(f"\n🎯 Nettoyage de fichiers de test spécifiques...")
    
    specific_files = [
        "pdfs/Factura_TEST-001.pdf",
        "pdfs/Factura_DEMO-001.pdf", 
        "pdfs/Factura_VISOR-*.pdf",
        "/tmp/test_factura.pdf",
        "/tmp/fake.pdf",
        "/tmp/fake2.pdf"
    ]
    
    cleaned = 0
    
    for file_pattern in specific_files:
        if '*' in file_pattern:
            # Pattern avec wildcard
            files = glob.glob(file_pattern)
            for file_path in files:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        cleaned += 1
                        print(f"   🗑️  Supprimé: {file_path}")
                    except Exception as e:
                        print(f"   ❌ Erreur: {e}")
        else:
            # Fichier spécifique
            if os.path.exists(file_pattern):
                try:
                    os.remove(file_pattern)
                    cleaned += 1
                    print(f"   🗑️  Supprimé: {file_pattern}")
                except Exception as e:
                    print(f"   ❌ Erreur: {e}")
    
    if cleaned == 0:
        print(f"   ✅ Aucun fichier spécifique trouvé")
    else:
        print(f"   ✅ {cleaned} fichiers spécifiques supprimés")


def main():
    """Fonction principale"""
    print("🧹 NETTOYAGE DES PDFS DE TEST")
    print("=" * 40)
    
    # Nettoyage général
    total_cleaned = cleanup_test_pdfs()
    
    # Nettoyage spécifique
    cleanup_specific_test_files()
    
    print(f"\n🎉 Nettoyage terminé!")
    
    if total_cleaned > 0:
        print(f"💡 Conseil: Les tests ne génèrent plus de PDFs ouverts grâce aux variables d'environnement")
        print(f"   PYTEST_RUNNING=1 et DISABLE_PDF_OPEN=1")
    
    return total_cleaned


if __name__ == "__main__":
    main()
