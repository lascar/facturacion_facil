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
    
    def __init__(self, db_path="base_de_datos/facturacion.db"):
        self.db_path = db_path
        self.logger = get_logger(__name__)
        self.backup_dir = "base_de_datos/backups"
        
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
                ("talla", "TEXT", None),
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
                    talla TEXT,
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
    
    def remove_stock_columns_from_productos(self):
        """Migration pour supprimer les colonnes stock_actual et stock_minimo de productos"""
        self.logger.info("Début migration suppression colonnes stock de productos")

        # Créer sauvegarde avant migration
        backup_path = self.create_backup("remove_stock_columns")
        if not backup_path:
            self.logger.error("Impossible de créer une sauvegarde, migration annulée")
            return False

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Vérifier si les colonnes stock existent encore
            cursor.execute("PRAGMA table_info(productos)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            has_stock_actual = 'stock_actual' in column_names
            has_stock_minimo = 'stock_minimo' in column_names

            if not has_stock_actual and not has_stock_minimo:
                self.logger.info("Les colonnes stock ont déjà été supprimées")
                conn.close()
                return True

            self.logger.info(f"Colonnes à supprimer - stock_actual: {has_stock_actual}, stock_minimo: {has_stock_minimo}")

            # Étape 1: Migrer les données stock vers la table stock si nécessaire
            if has_stock_actual:
                self._migrate_stock_data_to_stock_table(cursor)

            # Étape 2: Créer une nouvelle table productos sans les colonnes stock
            cursor.execute("""
                CREATE TABLE productos_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    referencia TEXT UNIQUE,
                    precio REAL NOT NULL,
                    categoria TEXT,
                    descripcion TEXT,
                    imagen_path TEXT,
                    iva_recomendado REAL DEFAULT 21.0,
                    talla TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Étape 3: Copier les données (sans les colonnes stock)
            # D'abord, vérifier quelles colonnes existent réellement
            cursor.execute("PRAGMA table_info(productos)")
            existing_columns = [col[1] for col in cursor.fetchall()]

            # Construire la requête en fonction des colonnes existantes
            base_columns = ['id', 'nombre', 'referencia', 'precio', 'categoria',
                           'descripcion', 'imagen_path', 'iva_recomendado', 'talla']
            optional_columns = ['fecha_creacion', 'fecha_actualizacion']

            # Filtrer les colonnes qui existent réellement
            select_columns = []
            insert_columns = []

            for col in base_columns:
                if col in existing_columns:
                    select_columns.append(col)
                    insert_columns.append(col)

            for col in optional_columns:
                if col in existing_columns:
                    select_columns.append(col)
                    insert_columns.append(col)

            select_clause = ', '.join(select_columns)
            insert_clause = ', '.join(insert_columns)

            cursor.execute(f"""
                INSERT INTO productos_new ({insert_clause})
                SELECT {select_clause}
                FROM productos
            """)

            # Étape 4: Supprimer l'ancienne table et renommer la nouvelle
            cursor.execute("DROP TABLE productos")
            cursor.execute("ALTER TABLE productos_new RENAME TO productos")

            # Étape 5: Recréer les index
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_referencia ON productos (referencia)")

            conn.commit()
            conn.close()

            self.logger.info("Migration suppression colonnes stock terminée avec succès")
            return True

        except Exception as e:
            self.logger.error(f"Erreur migration suppression colonnes stock: {e}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False

    def _migrate_stock_data_to_stock_table(self, cursor):
        """Migre les données stock_actual vers la table stock si nécessaire"""
        try:
            # IMPORTANT: Vérifier d'abord si la colonne stock_actual existe encore
            cursor.execute("PRAGMA table_info(productos)")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]

            if 'stock_actual' not in column_names:
                self.logger.info("Colonne stock_actual n'existe plus, migration des données ignorée")
                return

            # Vérifier s'il y a des produits avec stock_actual mais sans entrée dans stock
            cursor.execute("""
                SELECT p.id, p.stock_actual
                FROM productos p
                LEFT JOIN stock s ON p.id = s.producto_id
                WHERE s.producto_id IS NULL AND p.stock_actual IS NOT NULL
            """)

            missing_stock_entries = cursor.fetchall()

            if missing_stock_entries:
                self.logger.info(f"Migration de {len(missing_stock_entries)} entrées stock manquantes")

                for producto_id, stock_actual in missing_stock_entries:
                    cursor.execute("""
                        INSERT INTO stock (producto_id, cantidad_disponible)
                        VALUES (?, ?)
                    """, (producto_id, stock_actual or 0))

            # Mettre à jour les entrées stock existantes avec stock_actual si différent
            cursor.execute("""
                UPDATE stock
                SET cantidad_disponible = (
                    SELECT p.stock_actual
                    FROM productos p
                    WHERE p.id = stock.producto_id
                ),
                fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE EXISTS (
                    SELECT 1 FROM productos p
                    WHERE p.id = stock.producto_id
                    AND p.stock_actual != stock.cantidad_disponible
                    AND p.stock_actual IS NOT NULL
                )
            """)

            self.logger.info("Données stock migrées vers la table stock")

        except Exception as e:
            self.logger.error(f"Erreur migration données stock: {e}")
            raise

    def migrate_productos_table_without_stock(self):
        """Migration productos sans ajouter les colonnes stock (elles sont dans la table stock)"""
        self.logger.info("Début migration table productos (sans colonnes stock)")

        # Créer sauvegarde avant migration
        backup_path = self.create_backup("productos_without_stock_migration")
        if not backup_path:
            self.logger.error("Impossible de créer une sauvegarde, migration annulée")
            return False

        try:
            # Vérifier si la table existe
            if not self.table_exists("productos"):
                self.logger.info("Table productos n'existe pas, création avec nouveau schéma (sans stock)")
                return self._create_productos_table_without_stock()

            # Récupérer le schéma actuel
            current_schema = self.get_table_schema("productos")
            self.logger.info(f"Schéma actuel productos: {[col[1] for col in current_schema]}")

            # Ajouter les colonnes manquantes une par une (SANS les colonnes stock)
            migrations_needed = [
                ("categoria", "TEXT", None),
                ("imagen_path", "TEXT", ""),
                ("talla", "TEXT", None),
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
                self.logger.info("Migration productos (sans stock) terminée avec succès")
                return True
            else:
                self.logger.error("Erreurs durant la migration productos (sans stock)")
                return False

        except Exception as e:
            self.logger.error(f"Erreur migration productos (sans stock): {e}")
            return False

    def _create_productos_table_without_stock(self):
        """Crée la table productos sans les colonnes stock"""
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
                    talla TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Créer l'index sur referencia
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_referencia ON productos (referencia)")

            conn.commit()
            conn.close()

            self.logger.info("Table productos créée avec nouveau schéma (sans stock)")
            return True

        except Exception as e:
            self.logger.error(f"Erreur création table productos (sans stock): {e}")
            return False

    def migrate_add_talla_column(self):
        """Migration pour ajouter la colonne talla à la table productos"""
        self.logger.info("Début migration ajout colonne talla")

        # Créer sauvegarde avant migration
        backup_path = self.create_backup("add_talla_column")
        if not backup_path:
            self.logger.error("Impossible de créer une sauvegarde, migration annulée")
            return False

        try:
            # Ajouter la colonne talla (TEXT, optionnelle, NULL par défaut)
            success = self.add_column_if_not_exists("productos", "talla", "TEXT", None)

            if success:
                self.logger.info("Migration ajout colonne talla terminée avec succès")
                return True
            else:
                self.logger.error("Erreur durant la migration ajout colonne talla")
                return False

        except Exception as e:
            self.logger.error(f"Erreur migration ajout colonne talla: {e}")
            return False

    def run_all_migrations(self):
        """Exécute toutes les migrations nécessaires"""
        self.logger.info("Début des migrations")

        # Vérifier si les colonnes stock existent encore
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(productos)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        has_stock_columns = 'stock_actual' in column_names or 'stock_minimo' in column_names
        conn.close()

        migrations = []

        # Si les colonnes stock existent, exécuter d'abord la migration de suppression
        if has_stock_columns:
            migrations.append(("remove_stock_columns", self.remove_stock_columns_from_productos))
        else:
            # Sinon, exécuter la migration productos normale (sans ajouter les colonnes stock)
            migrations.append(("productos_without_stock", self.migrate_productos_table_without_stock))

        # Ajouter la migration pour la colonne talla
        migrations.append(("add_talla_column", self.migrate_add_talla_column))

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
