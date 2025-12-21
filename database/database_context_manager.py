#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de contexte pour les connexions de base de données
Résout les problèmes de verrouillage (lock) en garantissant la fermeture des connexions
"""

import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime
from utils.logger import get_logger, log_database_operation, log_exception

class DatabaseContextManager:
    """Gestionnaire de base de données avec support des gestionnaires de contexte"""
    
    def __init__(self, db_path="facturacion.db"):
        self.db_path = db_path
        self.logger = get_logger("database_context")
        
    def get_connection_config(self):
        """Configuration optimisée pour SQLite"""
        return {
            'timeout': 30.0,  # Timeout de 30 secondes pour éviter les deadlocks
            'check_same_thread': False,  # Permet l'utilisation multi-thread
            'isolation_level': None  # Autocommit désactivé pour contrôle manuel
        }
    
    @contextmanager
    def get_connection(self):
        """Gestionnaire de contexte pour les connexions de base de données"""
        conn = None
        try:
            # S'assurer que le répertoire parent existe
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                self.logger.debug(f"Répertoire créé: {db_dir}")

            # Créer la connexion avec configuration optimisée
            conn = sqlite3.connect(self.db_path, **self.get_connection_config())
            
            # Optimisations SQLite pour éviter les locks
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA cache_size = 10000")
            conn.execute("PRAGMA temp_store = MEMORY")
            conn.execute("PRAGMA busy_timeout = 30000")  # 30 secondes de timeout
            
            self.logger.debug("Connexion de base de données ouverte")
            yield conn
            
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Erreur de base de données: {e}")
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Erreur inattendue: {e}")
            raise
        finally:
            if conn:
                conn.close()
                self.logger.debug("Connexion de base de données fermée")
    
    @contextmanager
    def get_transaction(self):
        """Gestionnaire de contexte pour les transactions"""
        with self.get_connection() as conn:
            try:
                conn.execute("BEGIN IMMEDIATE")  # Transaction immédiate pour éviter les deadlocks
                self.logger.debug("Transaction commencée")
                yield conn
                conn.commit()
                self.logger.debug("Transaction commitée")
            except Exception as e:
                conn.rollback()
                self.logger.error(f"Transaction annulée: {e}")
                raise
    
    def execute_query(self, query, params=None):
        """Exécute une requête avec gestionnaire de contexte"""
        start_time = datetime.now()
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Log de la requête
                log_database_operation(query[:100] + "..." if len(query) > 100 else query)
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Déterminer le type d'opération
                if query.strip().upper().startswith(('SELECT', 'PRAGMA')):
                    results = cursor.fetchall()
                    
                    # Log de performance
                    execution_time = (datetime.now() - start_time).total_seconds()
                    if execution_time > 0.1:  # Requêtes lentes
                        self.logger.warning(f"Requête lente ({execution_time:.3f}s): {query[:50]}...")
                    
                    return results
                else:
                    conn.commit()
                    lastrowid = cursor.lastrowid
                    return lastrowid
                    
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            self.logger.error(f"Requête: {query}")
            self.logger.error(f"Paramètres: {params}")
            raise
        except Exception as e:
            log_exception(e, "execute_query")
            raise
    
    def execute_many(self, query, params_list):
        """Exécute plusieurs requêtes en une seule transaction"""
        if not params_list:
            return
            
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, params_list)
                self.logger.info(f"Exécution en lot: {len(params_list)} opérations")
                return cursor.rowcount
                
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de l'exécution en lot: {e}")
            raise
    
    def execute_script(self, script):
        """Exécute un script SQL complet"""
        try:
            with self.get_connection() as conn:
                conn.executescript(script)
                conn.commit()
                self.logger.info("Script SQL exécuté avec succès")
                
        except sqlite3.Error as e:
            self.logger.error(f"Erreur lors de l'exécution du script: {e}")
            raise

# Instance globale avec gestionnaire de contexte
db_context = DatabaseContextManager()

# Fonctions utilitaires pour faciliter la migration
def with_connection(func):
    """Décorateur pour les fonctions nécessitant une connexion"""
    def wrapper(*args, **kwargs):
        with db_context.get_connection() as conn:
            return func(conn, *args, **kwargs)
    return wrapper

def with_transaction(func):
    """Décorateur pour les fonctions nécessitant une transaction"""
    def wrapper(*args, **kwargs):
        with db_context.get_transaction() as conn:
            return func(conn, *args, **kwargs)
    return wrapper
