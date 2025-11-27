#!/usr/bin/env python3
"""
Script pour restaurer les fichiers depuis les sauvegardes PyQt6
"""

import os
import glob
import shutil

def find_backup_files():
    """Trouver tous les fichiers de sauvegarde"""
    backup_files = []
    
    # Chercher récursivement tous les fichiers .backup_pyqt6_*
    for root, dirs, files in os.walk('.'):
        # Ignorer les répertoires de cache
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
        
        for file in files:
            if '.backup_pyqt6_' in file:
                backup_path = os.path.join(root, file)
                original_path = backup_path.split('.backup_pyqt6_')[0]
                backup_files.append((backup_path, original_path))
    
    return backup_files

def restore_file(backup_path, original_path):
    """Restaurer un fichier depuis sa sauvegarde"""
    try:
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, original_path)
            print(f"✅ Restauré: {original_path}")
            return True
        else:
            print(f"❌ Sauvegarde introuvable: {backup_path}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la restauration de {original_path}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔄 RESTAURATION DEPUIS SAUVEGARDES PYQT6")
    print("="*50)
    
    # Trouver les fichiers de sauvegarde
    backup_files = find_backup_files()
    
    if not backup_files:
        print("❌ Aucune sauvegarde PyQt6 trouvée")
        return 1
    
    print(f"📁 {len(backup_files)} sauvegardes trouvées")
    
    # Demander confirmation
    response = input("\n⚠️ Voulez-vous restaurer tous les fichiers? (y/N): ")
    if response.lower() != 'y':
        print("❌ Restauration annulée")
        return 0
    
    # Restaurer les fichiers
    restored_count = 0
    for backup_path, original_path in backup_files:
        if restore_file(backup_path, original_path):
            restored_count += 1
    
    print("\n" + "="*50)
    print(f"🎉 RESTAURATION TERMINÉE")
    print(f"📊 {restored_count} fichiers restaurés")
    
    # Restaurer requirements.txt si nécessaire
    restore_requirements()
    
    print("\n💡 Les fichiers PyQt6 originaux ont été restaurés")
    print("Vous pouvez maintenant réinstaller PyQt6 si nécessaire")
    
    return 0

def restore_requirements():
    """Restaurer requirements.txt original"""
    backup_req = None
    for file in os.listdir('.'):
        if file.startswith('requirements.txt.backup_pyqt6_'):
            backup_req = file
            break
    
    if backup_req:
        try:
            shutil.copy2(backup_req, 'requirements.txt')
            print("✅ requirements.txt restauré")
        except Exception as e:
            print(f"⚠️ Erreur restauration requirements.txt: {e}")

if __name__ == "__main__":
    exit(main())
