#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version améliorée de la classe Database avec gestionnaires de contexte
Résout les problèmes de verrouillage (lock) de la base de données
"""

import sqlite3
import os
from datetime import datetime
from database.database_context_manager import DatabaseContextManager, with_connection, with_transaction
from database.migration_manager import MigrationManager
from utils.logger import get_logger, log_database_operation, log_exception

class DatabaseImproved(DatabaseContextManager):
    """Version améliorée de Database avec gestionnaires de contexte"""
    
    def __init__(self, db_path="facturacion.db"):
        super().__init__(db_path)
        self.logger = get_logger("database_improved")
        self.migration_manager = MigrationManager(db_path)
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec gestionnaire de contexte et migrations"""
        try:
            # Exécuter les migrations avant l'initialisation
            self.migration_manager.run_all_migrations()

            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Créer les tables si elles n'existent pas
                self._create_tables(cursor)
                self._create_indexes(cursor)
                conn.commit()

                self.logger.info("Base de données initialisée avec succès")

        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation: {e}")
            raise
    
    def _create_tables(self, cursor):
        """Crée les tables de base de données"""
        # Table productos
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
        
        # Table clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dni_nie TEXT,
                direccion TEXT,
                email TEXT,
                telefono TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table stock
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad_disponible INTEGER NOT NULL DEFAULT 0,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
            )
        """)
        
        # Table facturas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                fecha_factura DATE NOT NULL,
                cliente_id INTEGER,
                nombre_cliente TEXT NOT NULL,
                dni_nie_cliente TEXT,
                direccion_cliente TEXT,
                subtotal REAL NOT NULL,
                total_iva REAL NOT NULL,
                total_factura REAL NOT NULL,
                estado TEXT DEFAULT 'Borrador',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        """)
        
        # Table factura_items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS factura_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                referencia_producto TEXT NOT NULL,
                nombre_producto TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                iva REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (factura_id) REFERENCES facturas (id) ON DELETE CASCADE,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        """)
        
        # Table stock_movements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT,
                fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos (id) ON DELETE CASCADE
            )
        """)
        
        # Table organizacion
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_empresa TEXT NOT NULL,
                nif TEXT,
                direccion TEXT,
                telefono TEXT,
                email TEXT,
                logo_path TEXT,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def _create_indexes(self, cursor):
        """Crée les index pour optimiser les performances"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_productos_referencia ON productos (referencia)",
            "CREATE INDEX IF NOT EXISTS idx_stock_producto_id ON stock (producto_id)",
            "CREATE INDEX IF NOT EXISTS idx_facturas_numero ON facturas (numero_factura)",
            "CREATE INDEX IF NOT EXISTS idx_facturas_cliente ON facturas (cliente_id)",
            "CREATE INDEX IF NOT EXISTS idx_facturas_fecha ON facturas (fecha_factura)",
            "CREATE INDEX IF NOT EXISTS idx_factura_items_factura ON factura_items (factura_id)",
            "CREATE INDEX IF NOT EXISTS idx_factura_items_producto ON factura_items (producto_id)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_producto ON stock_movements (producto_id)",
            "CREATE INDEX IF NOT EXISTS idx_stock_movements_fecha ON stock_movements (fecha_movimiento)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
    
    # Méthodes pour les produits avec gestionnaires de contexte
    def add_product(self, product_data):
        """Ajoute un nouveau produit avec gestionnaire de contexte"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()

                # Obtenir le stock depuis les données (avec fallback)
                stock_actual = product_data.get('stock', product_data.get('stock_actual', 0))
                stock_minimo = product_data.get('stock_minimo', 5)

                cursor.execute("""
                    INSERT INTO productos (nombre, referencia, precio, categoria, descripcion,
                                         imagen_path, iva_recomendado, stock_actual, stock_minimo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    product_data['nombre'],
                    product_data.get('referencia'),
                    product_data.get('precio_venta', product_data.get('precio', 0)),
                    product_data.get('categoria'),
                    product_data.get('descripcion', ''),
                    product_data.get('imagen_path', ''),
                    product_data.get('iva_recomendado', 21.0),
                    stock_actual,
                    stock_minimo
                ))

                product_id = cursor.lastrowid

                # Créer l'entrée de stock initiale dans la table stock séparée
                cursor.execute("""
                    INSERT INTO stock (producto_id, cantidad_disponible)
                    VALUES (?, ?)
                """, (product_id, stock_actual))

                self.logger.info(f"Produit ajouté avec ID: {product_id}, catégorie: {product_data.get('categoria', 'N/A')}")
                return product_id
                
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise Exception(f"La référence '{product_data['referencia']}' existe déjà")
            raise
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout du produit: {e}")
            raise

    def get_products(self):
        """Récupère tous les produits avec gestionnaire de contexte"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria,
                           p.descripcion, p.imagen_path, p.iva_recomendado,
                           p.stock_actual, p.stock_minimo, s.cantidad_disponible
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    ORDER BY p.nombre
                """)
                return cursor.fetchall()

        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des produits: {e}")
            raise

    def get_all_products(self):
        """Obtient tous les produits formatés pour l'interface"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, referencia, precio, categoria, descripcion,
                           imagen_path, iva_recomendado, stock_actual, stock_minimo,
                           fecha_creacion, fecha_actualizacion
                    FROM productos
                    ORDER BY nombre
                """)

                products = []
                for row in cursor.fetchall():
                    products.append({
                        'id': row[0],
                        'nombre': row[1],
                        'referencia': row[2],
                        'precio_venta': row[3],
                        'precio_compra': row[3] * 0.7 if row[3] else 0,  # Simulado
                        'categoria': row[4],
                        'descripcion': row[5],
                        'imagen_path': row[6],
                        'iva_recomendado': row[7],
                        'stock_actual': row[8] or 0,
                        'stock_minimo': row[9] or 5,
                        'fecha_creacion': row[10],
                        'fecha_actualizacion': row[11]
                    })

                return products

        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des produits: {e}")
            return []

    def get_product_categories(self):
        """Obtient toutes les catégories de produits"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT categoria
                    FROM productos
                    WHERE categoria IS NOT NULL AND categoria != ''
                    ORDER BY categoria
                """)
                categories = [row[0] for row in cursor.fetchall()]
                return categories

        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des catégories: {e}")
            return []

    def update_product(self, product_data):
        """Met à jour un produit avec gestionnaire de contexte"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()

                # Obtenir le stock depuis les données (avec fallback)
                stock_actual = product_data.get('stock', product_data.get('stock_actual', 0))
                stock_minimo = product_data.get('stock_minimo', 5)

                cursor.execute("""
                    UPDATE productos
                    SET nombre = ?, referencia = ?, precio = ?, categoria = ?, descripcion = ?,
                        imagen_path = ?, iva_recomendado = ?, stock_actual = ?, stock_minimo = ?
                    WHERE id = ?
                """, (
                    product_data['nombre'],
                    product_data.get('referencia'),
                    product_data.get('precio_venta', product_data.get('precio', 0)),
                    product_data.get('categoria'),
                    product_data.get('descripcion', ''),
                    product_data.get('imagen_path', ''),
                    product_data.get('iva_recomendado', 21.0),
                    stock_actual,
                    stock_minimo,
                    product_data['id']
                ))

                # Mettre à jour aussi la table stock séparée
                cursor.execute("""
                    UPDATE stock
                    SET cantidad_disponible = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE producto_id = ?
                """, (stock_actual, product_data['id']))

                if cursor.rowcount > 0:
                    self.logger.info(f"Produit {product_data['id']} mis à jour, catégorie: {product_data.get('categoria', 'N/A')}")
                    return True
                else:
                    self.logger.warning(f"Produit {product_data['id']} non trouvé")
                    return False

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise Exception(f"La référence '{product_data['referencia']}' existe déjà")
            raise
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour du produit: {e}")
            raise

    def delete_product(self, product_id):
        """Supprime un produit avec gestionnaire de contexte"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()

                # Vérifier s'il y a des factures associées
                cursor.execute("SELECT COUNT(*) FROM factura_items WHERE producto_id = ?", (product_id,))
                invoice_count = cursor.fetchone()[0]

                if invoice_count > 0:
                    raise Exception(f"Impossible de supprimer le produit. Il est utilisé dans {invoice_count} facture(s).")

                # Supprimer le produit (le stock sera supprimé automatiquement par CASCADE)
                cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))

                if cursor.rowcount > 0:
                    self.logger.info(f"Produit {product_id} supprimé")
                    return True
                else:
                    self.logger.warning(f"Produit {product_id} non trouvé")
                    return False

        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du produit: {e}")
            raise

    # Méthodes pour les clients avec gestionnaires de contexte
    def add_client(self, client_data):
        """Ajoute un nouveau client avec gestionnaire de contexte"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO clientes (nombre, dni_nie, direccion, email, telefono)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    client_data['nombre'],
                    client_data.get('nif', ''),
                    client_data.get('direccion', ''),
                    client_data.get('email', ''),
                    client_data.get('telefono', '')
                ))

                client_id = cursor.lastrowid
                self.logger.info(f"Client ajouté avec ID: {client_id}")
                return client_id

        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout du client: {e}")
            raise

    def get_clients(self):
        """Récupère tous les clients avec gestionnaire de contexte"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, dni_nie, direccion, email, telefono
                    FROM clientes
                    ORDER BY nombre
                """)
                return cursor.fetchall()

        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des clients: {e}")
            raise
