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
    
    def __init__(self, db_path="base_de_datos/facturacion.db"):
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
        # Table productos (sans les colonnes stock qui sont maintenant dans la table stock)
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

                cursor.execute("""
                    INSERT INTO productos (nombre, referencia, precio, categoria, descripcion,
                                         imagen_path, iva_recomendado, talla)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    product_data['nombre'],
                    product_data.get('referencia'),
                    product_data.get('precio_venta', product_data.get('precio', 0)),
                    product_data.get('categoria'),
                    product_data.get('descripcion', ''),
                    product_data.get('imagen_path', ''),
                    product_data.get('iva_recomendado', 21.0),
                    product_data.get('talla')
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
        """Obtient tous les produits formatés pour l'interface avec stock depuis la table stock"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria, p.descripcion,
                           p.imagen_path, p.iva_recomendado, p.talla, p.fecha_creacion, p.fecha_actualizacion,
                           COALESCE(s.cantidad_disponible, 0) as stock_actual
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    ORDER BY p.nombre
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
                        'talla': row[8],
                        'fecha_creacion': row[9],
                        'fecha_actualizacion': row[10],
                        'stock_actual': row[11] or 0,
                        'stock_minimo': 5  # Valeur par défaut, plus tard on pourrait l'ajouter à la table stock
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

                cursor.execute("""
                    UPDATE productos
                    SET nombre = ?, referencia = ?, precio = ?, categoria = ?, descripcion = ?,
                        imagen_path = ?, iva_recomendado = ?, talla = ?
                    WHERE id = ?
                """, (
                    product_data['nombre'],
                    product_data.get('referencia'),
                    product_data.get('precio_venta', product_data.get('precio', 0)),
                    product_data.get('categoria'),
                    product_data.get('descripcion', ''),
                    product_data.get('imagen_path', ''),
                    product_data.get('iva_recomendado', 21.0),
                    product_data.get('talla'),
                    product_data['id']
                ))

                # Mettre à jour la table stock séparée
                cursor.execute("""
                    UPDATE stock
                    SET cantidad_disponible = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE producto_id = ?
                """, (stock_actual, product_data['id']))

                # Si aucune ligne n'a été mise à jour dans stock, créer l'entrée
                if cursor.rowcount == 0:
                    cursor.execute("""
                        INSERT INTO stock (producto_id, cantidad_disponible)
                        VALUES (?, ?)
                    """, (product_data['id'], stock_actual))

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

    def get_all_clients(self):
        """Obtiene todos los clientes (alias de get_clients con formato compatible)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, dni_nie, direccion, email, telefono, fecha_creacion
                    FROM clientes
                    ORDER BY nombre
                """)

                clients = []
                for row in cursor.fetchall():
                    client = {
                        'id': row[0],
                        'nombre': row[1],
                        'nif': row[2] or '',  # Mapear dni_nie a nif para compatibilidad
                        'direccion': row[3] or '',
                        'email': row[4] or '',
                        'telefono': row[5] or '',
                        'fecha_creacion': row[6]
                    }
                    clients.append(client)

                return clients

        except Exception as e:
            self.logger.error(f"Error obteniendo clientes: {e}")
            return []

    def get_client_by_id(self, client_id):
        """Obtiene un cliente por su ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, dni_nie, direccion, email, telefono, fecha_creacion
                    FROM clientes
                    WHERE id = ?
                """, (client_id,))

                row = cursor.fetchone()

                if row:
                    return {
                        'id': row[0],
                        'nombre': row[1],
                        'nif': row[2] or '',  # Mapear dni_nie a nif
                        'direccion': row[3] or '',
                        'email': row[4] or '',
                        'telefono': row[5] or '',
                        'fecha_creacion': row[6]
                    }
                return None

        except Exception as e:
            self.logger.error(f"Error obteniendo cliente {client_id}: {e}")
            return None

    def get_product_by_id(self, product_id):
        """Obtiene un producto por su ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria, p.descripcion,
                           p.iva_recomendado, p.talla, p.fecha_creacion,
                           COALESCE(s.cantidad_disponible, 0) as stock_actual
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    WHERE p.id = ?
                """, (product_id,))

                row = cursor.fetchone()

                if row:
                    return {
                        'id': row[0],
                        'nombre': row[1],
                        'referencia': row[2],
                        'precio_venta': row[3],
                        'precio_compra': row[3] * 0.7 if row[3] else 0,  # Simulado
                        'categoria': row[4],
                        'descripcion': row[5],
                        'iva_recomendado': row[6],
                        'talla': row[7],
                        'fecha_creacion': row[8],
                        'stock_actual': row[9] or 0
                    }
                return None

        except Exception as e:
            self.logger.error(f"Error obteniendo producto {product_id}: {e}")
            return None

    def add_invoice(self, invoice_data):
        """Añade una nueva factura completa"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()

                # Insertar la factura principal
                cursor.execute("""
                    INSERT INTO facturas (numero_factura, fecha_factura, cliente_id,
                                        nombre_cliente, dni_nie_cliente, direccion_cliente,
                                        subtotal, total_iva, total_factura, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_data['numero'],
                    invoice_data['fecha'],
                    invoice_data['cliente'].get('id'),
                    invoice_data['cliente']['nombre'],
                    invoice_data['cliente'].get('nif', ''),
                    invoice_data['cliente'].get('direccion', ''),
                    invoice_data['subtotal'],
                    invoice_data['iva_total'],
                    invoice_data['total'],
                    invoice_data.get('estado', 'Borrador')
                ))

                factura_id = cursor.lastrowid

                # Sauvegarder les lignes de facture
                lineas = invoice_data.get('lineas', [])
                for linea in lineas:
                    # Obtenir les informations du produit
                    producto = self.get_product_by_id(linea.get('producto_id'))
                    if not producto:
                        raise Exception(f"Producto {linea.get('producto_id')} no encontrado")

                    # Calculer le subtotal
                    cantidad = linea.get('cantidad', 1)
                    precio_unitario = linea.get('precio_unitario', 0.0)
                    subtotal = cantidad * precio_unitario

                    cursor.execute("""
                        INSERT INTO factura_items (factura_id, producto_id, referencia_producto,
                                                 nombre_producto, cantidad, precio_unitario,
                                                 iva, subtotal)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        factura_id,
                        linea.get('producto_id'),
                        producto.get('referencia', ''),
                        producto.get('nombre', ''),
                        cantidad,
                        precio_unitario,
                        linea.get('iva_aplicado', 21.0),
                        subtotal
                    ))

                self.logger.info(f"Factura añadida con ID: {factura_id}")
                return factura_id

        except Exception as e:
            self.logger.error(f"Error añadiendo factura: {e}")
            raise

    def update_client(self, client_data):
        """Actualiza un cliente existente"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE clientes
                    SET nombre = ?, dni_nie = ?, direccion = ?, email = ?, telefono = ?
                    WHERE id = ?
                """, (
                    client_data['nombre'],
                    client_data.get('nif', ''),  # Mapear nif a dni_nie
                    client_data.get('direccion', ''),
                    client_data.get('email', ''),
                    client_data.get('telefono', ''),
                    client_data['id']
                ))

                if cursor.rowcount > 0:
                    self.logger.info(f"Cliente {client_data['id']} actualizado")
                    return True
                else:
                    self.logger.warning(f"Cliente {client_data['id']} no encontrado para actualizar")
                    return False

        except Exception as e:
            self.logger.error(f"Error actualizando cliente: {e}")
            raise

    def get_invoice_by_number(self, numero_factura):
        """Obtiene una factura por su número"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id, numero_factura, fecha_factura, cliente_id,
                           nombre_cliente, dni_nie_cliente, direccion_cliente,
                           subtotal, total_iva, total_factura, estado
                    FROM facturas
                    WHERE numero_factura = ?
                """, (numero_factura,))

                factura_row = cursor.fetchone()

                if not factura_row:
                    return None

                # Construir el objeto factura
                invoice_data = {
                    'id': factura_row[0],
                    'numero': factura_row[1],
                    'fecha': factura_row[2],
                    'vencimiento': factura_row[2],
                    'cliente': {
                        'id': factura_row[3],
                        'nombre': factura_row[4],
                        'nif': factura_row[5] or '',
                        'direccion': factura_row[6] or ''
                    },
                    'subtotal': factura_row[7],
                    'iva_total': factura_row[8],
                    'total': factura_row[9],
                    'estado': factura_row[10] if factura_row[10] else 'Borrador',
                    'lineas': []
                }

                # Cargar las líneas de la factura
                cursor.execute("""
                    SELECT fi.id, fi.producto_id, fi.cantidad, fi.precio_unitario,
                           fi.iva, fi.subtotal,
                           fi.nombre_producto, fi.referencia_producto
                    FROM factura_items fi
                    WHERE fi.factura_id = ?
                """, (factura_row[0],))

                items = []
                for row in cursor.fetchall():
                    # Calculer les montants dérivés
                    cantidad = row[2]
                    precio_unitario = row[3]
                    iva_aplicado = row[4]
                    subtotal = row[5]
                    iva_amount = subtotal * (iva_aplicado / 100.0)
                    total = subtotal + iva_amount

                    item = {
                        'id': row[0],
                        'producto_id': row[1],
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario,
                        'iva_aplicado': iva_aplicado,
                        'descuento': 0.0,
                        'subtotal': subtotal,
                        'iva_amount': iva_amount,
                        'total': total,
                        'producto_nombre': row[6] or 'Producto eliminado',
                        'producto_referencia': row[7] or 'N/A'
                    }
                    items.append(item)

                invoice_data['lineas'] = items
                return invoice_data

        except Exception as e:
            self.logger.error(f"Error obteniendo factura por número {numero_factura}: {e}")
            return None

    def get_last_invoice_number(self):
        """Obtiene el último número de factura"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT numero_factura FROM facturas
                    ORDER BY id DESC LIMIT 1
                """)

                row = cursor.fetchone()
                return row[0] if row else None

        except Exception as e:
            self.logger.error(f"Error obteniendo último número de factura: {e}")
            return None

    def get_all_invoices(self):
        """Obtiene todas las facturas"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, numero_factura, fecha_factura, cliente_id, nombre_cliente,
                           total_factura, fecha_creacion, estado
                    FROM facturas
                    ORDER BY fecha_creacion DESC
                """)

                invoices = []
                for row in cursor.fetchall():
                    invoice = {
                        'id': row[0],
                        'numero': row[1],
                        'fecha': row[2],
                        'vencimiento': row[2],  # Usar la misma fecha por defecto
                        'cliente_id': row[3],
                        'cliente_nombre': row[4],
                        'total': row[5],
                        'fecha_creacion': row[6],
                        'estado': row[7] if row[7] else 'Borrador'
                    }
                    invoices.append(invoice)

                return invoices

        except Exception as e:
            self.logger.error(f"Error obteniendo facturas: {e}")
            return []

    def get_invoice_items(self, invoice_id):
        """Obtiene las líneas de una factura"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT fi.id, fi.producto_id, fi.cantidad, fi.precio_unitario,
                           fi.iva, fi.subtotal,
                           fi.nombre_producto, fi.referencia_producto
                    FROM factura_items fi
                    WHERE fi.factura_id = ?
                    ORDER BY fi.id
                """, (invoice_id,))

                items = []
                for row in cursor.fetchall():
                    # Calculer les montants dérivés
                    cantidad = row[2]
                    precio_unitario = row[3]
                    iva_aplicado = row[4]
                    subtotal = row[5]
                    iva_amount = subtotal * (iva_aplicado / 100.0)
                    total = subtotal + iva_amount

                    item = {
                        'id': row[0],
                        'producto_id': row[1],
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario,
                        'iva_aplicado': iva_aplicado,
                        'descuento': 0.0,
                        'subtotal': subtotal,
                        'iva_amount': iva_amount,
                        'total': total,
                        'producto_nombre': row[6] or 'Producto eliminado',
                        'producto_referencia': row[7] or 'N/A'
                    }
                    items.append(item)

                return items

        except Exception as e:
            self.logger.error(f"Error obteniendo items de factura {invoice_id}: {e}")
            return []

    def get_client_by_name(self, nombre):
        """Busca un cliente por nombre, priorizando el que tiene más datos"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, dni_nie, direccion, email, telefono, fecha_creacion
                    FROM clientes
                    WHERE LOWER(nombre) = LOWER(?)
                    ORDER BY
                        CASE WHEN dni_nie IS NOT NULL AND dni_nie != '' THEN 1 ELSE 0 END +
                        CASE WHEN direccion IS NOT NULL AND direccion != '' THEN 1 ELSE 0 END +
                        CASE WHEN email IS NOT NULL AND email != '' THEN 1 ELSE 0 END +
                        CASE WHEN telefono IS NOT NULL AND telefono != '' THEN 1 ELSE 0 END DESC,
                        id DESC
                    LIMIT 1
                """, (nombre,))

                row = cursor.fetchone()

                if row:
                    return {
                        'id': row[0],
                        'nombre': row[1],
                        'nif': row[2] or '',
                        'direccion': row[3] or '',
                        'email': row[4] or '',
                        'telefono': row[5] or '',
                        'fecha_creacion': row[6]
                    }
                return None

        except Exception as e:
            self.logger.error(f"Error buscando cliente por nombre {nombre}: {e}")
            return None

    def delete_client(self, client_id):
        """Elimina un cliente por ID"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()

                # Verificar si el cliente tiene facturas asociadas
                cursor.execute("SELECT COUNT(*) FROM facturas WHERE cliente_id = ?", (client_id,))
                invoice_count = cursor.fetchone()[0]

                if invoice_count > 0:
                    raise Exception(f"No se puede eliminar el cliente. Tiene {invoice_count} factura(s) asociada(s).")

                # Eliminar el cliente
                cursor.execute("DELETE FROM clientes WHERE id = ?", (client_id,))

                if cursor.rowcount > 0:
                    self.logger.info(f"Cliente {client_id} eliminado")
                    return True
                else:
                    self.logger.warning(f"Cliente {client_id} no encontrado")
                    return False

        except Exception as e:
            self.logger.error(f"Error eliminando cliente {client_id}: {e}")
            raise

    def delete_multiple_clients(self, client_ids):
        """Elimina múltiples clientes por IDs"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()

                # Verificar si algún cliente tiene facturas asociadas
                placeholders = ','.join(['?' for _ in client_ids])
                cursor.execute(f"""
                    SELECT cliente_id, COUNT(*) as invoice_count
                    FROM facturas
                    WHERE cliente_id IN ({placeholders})
                    GROUP BY cliente_id
                """, client_ids)

                clients_with_invoices = cursor.fetchall()

                if clients_with_invoices:
                    # Construir mensaje de error
                    error_details = []
                    for client_id, count in clients_with_invoices:
                        error_details.append(f"Cliente ID {client_id}: {count} factura(s)")

                    raise Exception(f"No se pueden eliminar algunos clientes con facturas asociadas:\n" +
                                  "\n".join(error_details))

                # Eliminar los clientes
                cursor.execute(f"DELETE FROM clientes WHERE id IN ({placeholders})", client_ids)

                deleted_count = cursor.rowcount
                self.logger.info(f"{deleted_count} clientes eliminados")
                return deleted_count

        except Exception as e:
            self.logger.error(f"Error eliminando clientes múltiples: {e}")
            raise

    # Méthodes pour l'organisation
    def get_organization_info(self):
        """Obtiene la información de la organización"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre_empresa, nif, direccion, telefono, email, logo_path
                    FROM organizacion
                    WHERE id = 1
                """)

                row = cursor.fetchone()

                if row:
                    return {
                        'id': row[0],
                        'nombre': row[1] or '',
                        'direccion': row[3] or '',
                        'telefono': row[4] or '',
                        'email': row[5] or '',
                        'cif': row[2] or '',
                        'logo_path': row[6] or '',
                        'directorio_imagenes_defecto': '',
                        'numero_factura_inicial': '1',
                        'directorio_descargas_pdf': '',
                        'visor_pdf_personalizado': '',
                        'logo_orientation': 'landscape',
                        'directorio_logos_storage': ''
                    }
                return None

        except Exception as e:
            self.logger.error(f"Error obteniendo información de organización: {e}")
            return None

    def create_organization(self, org_data):
        """Crea la información de la organización"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO organizacion
                    (id, nombre_empresa, nif, direccion, telefono, email, logo_path)
                    VALUES (1, ?, ?, ?, ?, ?, ?)
                """, (
                    org_data.get('nombre', ''),
                    org_data.get('cif', ''),
                    org_data.get('direccion', ''),
                    org_data.get('telefono', ''),
                    org_data.get('email', ''),
                    org_data.get('logo_path', '')
                ))

                self.logger.info("Información de organización creada")

        except Exception as e:
            self.logger.error(f"Error creando organización: {e}")
            raise

    def update_organization(self, org_data):
        """Actualiza la información de la organización"""
        try:
            with self.get_transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE organizacion
                    SET nombre_empresa = ?, nif = ?, direccion = ?, telefono = ?,
                        email = ?, logo_path = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    org_data.get('nombre', ''),
                    org_data.get('cif', ''),
                    org_data.get('direccion', ''),
                    org_data.get('telefono', ''),
                    org_data.get('email', ''),
                    org_data.get('logo_path', ''),
                    org_data.get('id', 1)
                ))

                self.logger.info("Información de organización actualizada")

        except Exception as e:
            self.logger.error(f"Error actualizando organización: {e}")
            raise
