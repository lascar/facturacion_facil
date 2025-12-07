#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de sauvegarde automatique pour la base de données
Crée des sauvegardes avant les opérations critiques
"""

import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

class AutoBackupSystem:
    def __init__(self, db_path="facturacion.db", backup_dir="backups"):
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self, operation_name="manual"):
        """Crée une sauvegarde avec un nom descriptif"""
        try:
            if not os.path.exists(self.db_path):
                print(f"⚠️  Base de données {self.db_path} non trouvée")
                return None
            
            # Générer nom de backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{operation_name}_{timestamp}.db"
            backup_path = self.backup_dir / backup_name
            
            # Créer la sauvegarde
            shutil.copy2(self.db_path, backup_path)
            
            # Vérifier l'intégrité
            if self._verify_backup(backup_path):
                print(f"✅ Backup créé: {backup_path}")
                return str(backup_path)
            else:
                print(f"❌ Backup corrompu: {backup_path}")
                os.remove(backup_path)
                return None
                
        except Exception as e:
            print(f"❌ Erreur créant backup: {e}")
            return None
    
    def _verify_backup(self, backup_path):
        """Vérifie l'intégrité d'une sauvegarde"""
        try:
            conn = sqlite3.connect(backup_path)
            cursor = conn.cursor()
            
            # Test simple d'intégrité
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            
            conn.close()
            return result[0] == "ok"
            
        except Exception:
            return False
    
    def list_backups(self):
        """Liste toutes les sauvegardes disponibles"""
        try:
            backups = []
            for backup_file in self.backup_dir.glob("backup_*.db"):
                stat = backup_file.stat()
                backups.append({
                    'name': backup_file.name,
                    'path': str(backup_file),
                    'size': stat.st_size,
                    'date': datetime.fromtimestamp(stat.st_mtime)
                })
            
            # Trier par date (plus récent en premier)
            backups.sort(key=lambda x: x['date'], reverse=True)
            return backups
            
        except Exception as e:
            print(f"❌ Erreur listant backups: {e}")
            return []
    
    def restore_backup(self, backup_path):
        """Restaure une sauvegarde"""
        try:
            if not os.path.exists(backup_path):
                print(f"❌ Backup non trouvé: {backup_path}")
                return False
            
            # Vérifier l'intégrité avant restauration
            if not self._verify_backup(backup_path):
                print(f"❌ Backup corrompu: {backup_path}")
                return False
            
            # Créer backup de la base actuelle
            current_backup = self.create_backup("before_restore")
            if not current_backup:
                print("⚠️  Impossible de sauvegarder la base actuelle")
            
            # Restaurer
            shutil.copy2(backup_path, self.db_path)
            print(f"✅ Base restaurée depuis: {backup_path}")
            
            if current_backup:
                print(f"💾 Base précédente sauvegardée: {current_backup}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur restaurant backup: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count=10):
        """Nettoie les anciennes sauvegardes (garde les N plus récentes)"""
        try:
            backups = self.list_backups()
            
            if len(backups) <= keep_count:
                print(f"ℹ️  {len(backups)} backups trouvés (< {keep_count}), aucun nettoyage nécessaire")
                return 0
            
            # Supprimer les plus anciens
            to_delete = backups[keep_count:]
            deleted_count = 0
            
            for backup in to_delete:
                try:
                    os.remove(backup['path'])
                    deleted_count += 1
                    print(f"🗑️  Backup supprimé: {backup['name']}")
                except Exception as e:
                    print(f"⚠️  Erreur supprimant {backup['name']}: {e}")
            
            print(f"✅ {deleted_count} anciens backups supprimés")
            return deleted_count
            
        except Exception as e:
            print(f"❌ Erreur nettoyant backups: {e}")
            return 0
    
    def get_backup_stats(self):
        """Obtient des statistiques sur les sauvegardes"""
        try:
            backups = self.list_backups()
            
            if not backups:
                return {
                    'count': 0,
                    'total_size': 0,
                    'total_size_mb': 0,
                    'latest': None,
                    'oldest': None
                }
            
            total_size = sum(b['size'] for b in backups)
            
            return {
                'count': len(backups),
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'latest': backups[0]['date'],
                'oldest': backups[-1]['date']
            }
            
        except Exception as e:
            print(f"❌ Erreur calculant stats: {e}")
            return None

def main():
    """Fonction principale pour tests"""
    backup_system = AutoBackupSystem()
    
    print("🔧 SYSTÈME DE SAUVEGARDE AUTOMATIQUE")
    print("=" * 50)
    
    # Statistiques
    stats = backup_system.get_backup_stats()
    if stats:
        print(f"\n📊 Statistiques des sauvegardes:")
        print(f"   • Nombre: {stats['count']}")
        print(f"   • Taille totale: {stats['total_size_mb']} MB")
        if stats['latest']:
            print(f"   • Plus récent: {stats['latest']}")
        if stats['oldest']:
            print(f"   • Plus ancien: {stats['oldest']}")
    
    # Créer une sauvegarde de test
    print(f"\n🔄 Test de création de sauvegarde...")
    backup_path = backup_system.create_backup("test")
    
    if backup_path:
        print(f"✅ Test réussi!")
    else:
        print(f"❌ Test échoué!")
    
    # Nettoyer les anciens backups
    print(f"\n🧹 Nettoyage des anciens backups...")
    deleted = backup_system.cleanup_old_backups(5)
    
    print(f"\n🎉 Test terminé!")

if __name__ == "__main__":
    main()
