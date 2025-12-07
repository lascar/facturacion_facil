#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour forcer la libération des verrous de base de données
et appliquer les gestionnaires de contexte
"""

import os
import sqlite3
import time
import shutil
from datetime import datetime

def force_unlock_database(db_path="facturacion.db"):
    """Force la libération des verrous de la base de données"""
    print(f"🔓 Libération forcée des verrous pour {db_path}...")
    
    # Méthode 1: Fermer toutes les connexions potentielles
    try:
        # Créer une connexion avec timeout très court
        conn = sqlite3.connect(db_path, timeout=1.0)
        
        # Forcer la libération avec PRAGMA
        conn.execute("PRAGMA locking_mode = NORMAL")
        conn.execute("PRAGMA journal_mode = DELETE")  # Temporairement
        conn.execute("PRAGMA journal_mode = WAL")     # Puis remettre WAL
        
        conn.close()
        print("✅ Verrous libérés avec PRAGMA")
        return True
        
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("⚠️ Base de données toujours verrouillée, tentative de récupération...")
            return force_recovery(db_path)
        else:
            print(f"❌ Erreur inattendue: {e}")
            return False

def force_recovery(db_path="facturacion.db"):
    """Récupération forcée en cas de verrouillage persistant"""
    print("🚑 Récupération forcée de la base de données...")
    
    # Créer une sauvegarde d'urgence
    backup_path = f"{db_path}.emergency_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Copier le fichier même s'il est verrouillé
        shutil.copy2(db_path, backup_path)
        print(f"✅ Sauvegarde d'urgence créée: {backup_path}")
    except Exception as e:
        print(f"⚠️ Impossible de créer la sauvegarde: {e}")
    
    # Supprimer les fichiers de journal qui peuvent causer des verrous
    journal_files = [
        f"{db_path}-wal",
        f"{db_path}-shm",
        f"{db_path}-journal"
    ]
    
    for journal_file in journal_files:
        if os.path.exists(journal_file):
            try:
                os.remove(journal_file)
                print(f"✅ Fichier journal supprimé: {journal_file}")
            except Exception as e:
                print(f"⚠️ Impossible de supprimer {journal_file}: {e}")
    
    # Attendre un peu
    time.sleep(1)
    
    # Tenter de rouvrir la base de données
    try:
        conn = sqlite3.connect(db_path, timeout=5.0)
        conn.execute("PRAGMA integrity_check")
        result = conn.fetchone()
        
        if result and result[0] == "ok":
            print("✅ Intégrité de la base de données vérifiée")
            
            # Réappliquer les optimisations
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA foreign_keys = ON")
            
            conn.close()
            return True
        else:
            print(f"❌ Problème d'intégrité: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Échec de la récupération: {e}")
        return False

def apply_context_manager_optimizations(db_path="facturacion.db"):
    """Applique les optimisations des gestionnaires de contexte"""
    print("⚙️ Application des optimisations des gestionnaires de contexte...")
    
    try:
        # Utiliser notre nouveau gestionnaire de contexte
        from database.database_context_manager import DatabaseContextManager
        
        db_context = DatabaseContextManager(db_path)
        
        with db_context.get_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier l'état actuel
            cursor.execute("PRAGMA journal_mode")
            journal_mode = cursor.fetchone()[0]
            print(f"   Mode journal: {journal_mode}")
            
            cursor.execute("PRAGMA synchronous")
            sync_mode = cursor.fetchone()[0]
            print(f"   Mode synchrone: {sync_mode}")
            
            cursor.execute("PRAGMA foreign_keys")
            fk_status = cursor.fetchone()[0]
            print(f"   Clés étrangères: {'ON' if fk_status else 'OFF'}")
            
            # Appliquer les optimisations si nécessaire
            optimizations_applied = []
            
            if journal_mode != "wal":
                conn.execute("PRAGMA journal_mode = WAL")
                optimizations_applied.append("Mode WAL activé")
            
            if sync_mode != 1:  # NORMAL = 1
                conn.execute("PRAGMA synchronous = NORMAL")
                optimizations_applied.append("Synchronisation NORMAL")
            
            if not fk_status:
                conn.execute("PRAGMA foreign_keys = ON")
                optimizations_applied.append("Clés étrangères activées")
            
            # Autres optimisations
            conn.execute("PRAGMA cache_size = 10000")
            conn.execute("PRAGMA temp_store = MEMORY")
            conn.execute("PRAGMA busy_timeout = 30000")
            
            optimizations_applied.extend([
                "Cache augmenté à 10MB",
                "Stockage temporaire en mémoire",
                "Timeout de 30 secondes"
            ])
            
            # Analyser la base de données
            conn.execute("ANALYZE")
            optimizations_applied.append("Analyse de la base de données")
            
            conn.commit()
            
            for opt in optimizations_applied:
                print(f"   ✅ {opt}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors de l'application des optimisations: {e}")
        return False

def verify_fix(db_path="facturacion.db"):
    """Vérifie que les problèmes de verrouillage sont résolus"""
    print("🔍 Vérification de la résolution des problèmes...")
    
    try:
        from database.database_context_manager import DatabaseContextManager
        
        db_context = DatabaseContextManager(db_path)
        
        # Test 1: Connexion simple
        with db_context.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM productos")
            count = cursor.fetchone()[0]
            print(f"   ✅ Test connexion: {count} produits")
        
        # Test 2: Transaction
        with db_context.get_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM clientes")
            count = cursor.fetchone()[0]
            print(f"   ✅ Test transaction: {count} clients")
        
        # Test 3: Requête avec méthode execute_query
        result = db_context.execute_query("SELECT COUNT(*) FROM facturas")
        count = result[0][0] if result else 0
        print(f"   ✅ Test execute_query: {count} factures")
        
        print("✅ Tous les tests de vérification ont réussi")
        return True
        
    except Exception as e:
        print(f"❌ Échec de la vérification: {e}")
        return False

def main():
    """Fonction principale de correction"""
    print("🔧 CORRECTION DES PROBLÈMES DE VERROUILLAGE DE BASE DE DONNÉES")
    print("=" * 65)
    
    db_path = "facturacion.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    # Étape 1: Libérer les verrous
    if not force_unlock_database(db_path):
        print("❌ Impossible de libérer les verrous")
        return False
    
    # Étape 2: Appliquer les optimisations
    if not apply_context_manager_optimizations(db_path):
        print("❌ Impossible d'appliquer les optimisations")
        return False
    
    # Étape 3: Vérifier la correction
    if not verify_fix(db_path):
        print("❌ La correction n'a pas fonctionné")
        return False
    
    print("\n🎉 PROBLÈMES DE VERROUILLAGE RÉSOLUS !")
    print("   La base de données utilise maintenant les gestionnaires de contexte.")
    print("   Les connexions sont automatiquement fermées.")
    print("   Les performances sont optimisées.")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
