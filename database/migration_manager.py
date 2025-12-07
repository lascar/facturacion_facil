#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de migrations de base de données
Maintient la compatibilité avec les structures antérieures
"""

import sqlite3
import shutil
import os
from datetime import datetime
from utils.logger import get_logger

class MigrationManager:
    """Gestionnaire de migrations pour maintenir la compatibilité des données"""
    
    def __init__(self, db_path="facturacion.db"):
        self.db_path = db_path
        self.logger = get_logger(__name__)
        self.backup_dir = "backups"
        
        # Créer le répertoire de sauvegarde s'il n'existe pas
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, reason="migration"):
        """Crée une sauvegarde avant migration"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{reason}_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, backup_path)
                self.logger.info(f"Sauvegarde créée: {backup_path}")
                return backup_path
            else:
                self.logger.warning(f"Base de données {self.db_path} n'existe pas")
                return None
        except Exception as e:
            self.logger.error(f"Erreur création sauvegarde: {e}")
            return None
    
    def get_table_schema(self, table_name):
        """Récupère le schéma actuel d'une table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            conn.close()
            return columns
        except Exception as e:
            self.logger.error(f"Erreur récupération schéma {table_name}: {e}")
            return []
    
    def table_exists(self, table_name):
        """Vérifie si une table existe"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (table_name,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        except Exception as e:
            self.logger.error(f"Erreur vérification table {table_name}: {e}")
            return False
    
    def column_exists(self, table_name, column_name):
        """Vérifie si une colonne existe dans une table"""
        schema = self.get_table_schema(table_name)
        return any(col[1] == column_name for col in schema)
    
    def add_column_if_not_exists(self, table_name, column_name, column_type, default_value=None):
        """Ajoute une colonne si elle n'existe pas déjà"""
        if not self.column_exists(table_name, column_name):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Construire la requête ALTER TABLE
                alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
                if default_value is not None:
                    if isinstance(default_value, str):
                        alter_query += f" DEFAULT '{default_value}'"
                    else:
                        alter_query += f" DEFAULT {default_value}"
                
                cursor.execute(alter_query)
                conn.commit()
                conn.close()
                
                self.logger.info(f"Colonne {column_name} ajoutée à {table_name}")
                return True
                
            except Exception as e:
                self.logger.error(f"Erreur ajout colonne {column_name} à {table_name}: {e}")
                return False
        else:
            self.logger.info(f"Colonne {column_name} existe déjà dans {table_name}")
            return True
    
    def migrate_productos_table(self):
        """Migration spécifique pour la table productos"""
        self.logger.info("Début migration table productos")
        
        # Créer sauvegarde avant migration
        backup_path = self.create_backup("productos_migration")
        if not backup_path:
            self.logger.error("Impossible de créer une sauvegarde, migration annulée")
            return False
        
        try:
            # Vérifier si la table existe
            if not self.table_exists("productos"):
                self.logger.info("Table productos n'existe pas, création avec nouveau schéma")
                return self._create_productos_table_new_schema()
            
            # Récupérer le schéma actuel
            current_schema = self.get_table_schema("productos")
            self.logger.info(f"Schéma actuel productos: {[col[1] for col in current_schema]}")
            
            # Ajouter les colonnes manquantes une par une
            migrations_needed = [
                ("categoria", "TEXT", None),
                ("imagen_path", "TEXT", ""),
                ("stock_actual", "INTEGER", 0),
                ("stock_minimo", "INTEGER", 5),
                ("fecha_creacion", "TIMESTAMP", "CURRENT_TIMESTAMP"),
                ("fecha_actualizacion", "TIMESTAMP", "CURRENT_TIMESTAMP")
            ]
            
            success = True
            for column_name, column_type, default_value in migrations_needed:
                if not self.add_column_if_not_exists("productos", column_name, column_type, default_value):
                    success = False
            
            # Vérifier que la colonne referencia peut être NULL
            self._ensure_referencia_nullable()
            
            if success:
                self.logger.info("Migration productos terminée avec succès")
                return True
            else:
                self.logger.error("Erreurs durant la migration productos")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur migration productos: {e}")
            return False
    
    def _create_productos_table_new_schema(self):
        """Crée la table productos avec le nouveau schéma complet"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    referencia TEXT UNIQUE,
                    precio REAL NOT NULL,
                    categoria TEXT,
                    descripcion TEXT,
                    imagen_path TEXT,
                    iva_recomendado REAL DEFAULT 21.0,
                    stock_actual INTEGER DEFAULT 0,
                    stock_minimo INTEGER DEFAULT 5,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Créer l'index sur referencia
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_referencia ON productos (referencia)")
            
            conn.commit()
            conn.close()
            
            self.logger.info("Table productos créée avec nouveau schéma")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur création table productos: {e}")
            return False
    
    def _ensure_referencia_nullable(self):
        """S'assure que la colonne referencia peut être NULL"""
        try:
            # SQLite ne permet pas de modifier directement les contraintes
            # On vérifie juste que la colonne existe
            if self.column_exists("productos", "referencia"):
                self.logger.info("Colonne referencia existe et est utilisable")
                return True
            else:
                self.logger.warning("Colonne referencia n'existe pas")
                return False
        except Exception as e:
            self.logger.error(f"Erreur vérification referencia: {e}")
            return False
    
    def restore_from_backup(self, backup_path):
        """Restaure la base de données depuis une sauvegarde"""
        try:
            if os.path.exists(backup_path):
                # Créer une sauvegarde de l'état actuel avant restauration
                current_backup = self.create_backup("before_restore")
                
                # Restaurer
                shutil.copy2(backup_path, self.db_path)
                self.logger.info(f"Base de données restaurée depuis {backup_path}")
                
                # Appliquer les migrations nécessaires
                self.migrate_productos_table()
                
                return True
            else:
                self.logger.error(f"Sauvegarde {backup_path} n'existe pas")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur restauration: {e}")
            return False
    
    def run_all_migrations(self):
        """Exécute toutes les migrations nécessaires"""
        self.logger.info("Début des migrations")
        
        migrations = [
            ("productos", self.migrate_productos_table),
            # Ajouter d'autres migrations ici
        ]
        
        success = True
        for migration_name, migration_func in migrations:
            self.logger.info(f"Exécution migration: {migration_name}")
            if not migration_func():
                self.logger.error(f"Échec migration: {migration_name}")
                success = False
        
        if success:
            self.logger.info("Toutes les migrations terminées avec succès")
        else:
            self.logger.error("Certaines migrations ont échoué")
        
        return success
