import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from database.migration_manager import MigrationManager
from utils.logger import get_logger, log_database_operation, log_exception

class Database:
    def __init__(self, db_path="base_de_datos/facturacion.db"):
        self.db_path = db_path
        self.logger = get_logger("database")
        self.migration_manager = MigrationManager(db_path)
        self.init_database()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)  # Timeout de 30 segundos
            conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
            # Configurar WAL mode para mejor concurrencia
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.execute("PRAGMA cache_size=10000")
            conn.execute("PRAGMA temp_store=MEMORY")
            return conn
        except Exception as e:
            self.logger.error(f"Error conectando a la base de datos: {e}")
            raise
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        # Étape 1 : Exécuter les migrations AVANT l'initialisation
        self.migration_manager.run_all_migrations()

        # Étape 2 : Créer/mettre à jour les tables
        conn = self.get_connection()
        cursor = conn.cursor()

        # Tabla productos
        cursor.execute('''
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
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Ajouter la colonne talla si elle n'existe pas (pour compatibilité avec bases existantes)
        try:
            cursor.execute('ALTER TABLE productos ADD COLUMN talla TEXT')
        except sqlite3.OperationalError:
            pass  # La colonne existe déjà
        
        # Tabla organización
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS organizacion (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                email TEXT,
                cif TEXT,
                logo_path TEXT,
                directorio_imagenes_defecto TEXT,
                numero_factura_inicial TEXT DEFAULT '1',
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Agregar columnas nuevas si no existen (para compatibilidad con bases de datos existentes)
        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN directorio_imagenes_defecto TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN numero_factura_inicial TEXT DEFAULT \'1\'')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN directorio_descargas_pdf TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN visor_pdf_personalizado TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN logo_orientation TEXT DEFAULT \'landscape\'')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN directorio_logos_storage TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN directorio_informes TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN directorio_descargas_pdf TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN visor_pdf_personalizado TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN logo_orientation TEXT DEFAULT \'landscape\'')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN directorio_logos_storage TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        # Migración: Añadir columnas de stock a productos
        # ⚠️ DÉSACTIVÉ: Les colonnes stock_actual et stock_minimo ont été supprimées
        # On utilise maintenant uniquement la table stock dédiée
        # Ne pas réactiver ces lignes car elles causent des conflits avec le système de migration
        # try:
        #     cursor.execute('ALTER TABLE productos ADD COLUMN stock_actual INTEGER DEFAULT 0')
        # except sqlite3.OperationalError:
        #     pass  # La columna ya existe
        #
        # try:
        #     cursor.execute('ALTER TABLE productos ADD COLUMN stock_minimo INTEGER DEFAULT 5')
        # except sqlite3.OperationalError:
        #     pass  # La columna ya existe

        # Migración: Hacer la referencia opcional (no obligatoria)
        try:
            # Verificar la estructura actual de la tabla productos
            cursor.execute("PRAGMA table_info(productos)")
            columns = cursor.fetchall()
            referencia_column = next((col for col in columns if col[1] == 'referencia'), None)

            print(f"DEBUG: Columna referencia encontrada: {referencia_column}")

            # Verificar si referencia tiene NOT NULL (columna 3 = notnull, 1 = tiene NOT NULL)
            if referencia_column and referencia_column[3] == 1:
                print("DEBUG: Migración de referencia opcional necesaria...")

                try:
                    # Nettoyer d'abord si la table temp existe déjà
                    cursor.execute("DROP TABLE IF EXISTS productos_temp")

                    # Créer une nouvelle table avec referencia optionnelle (structure fixe)
                    cursor.execute('''
                        CREATE TABLE productos_temp (
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
                    ''')
                    print("DEBUG: Table productos_temp créée avec referencia optionnelle")

                    # Copier les données existantes (en remplaçant les références vides par NULL)
                    cursor.execute('''
                        INSERT INTO productos_temp (id, nombre, referencia, precio, categoria, descripcion, imagen_path, iva_recomendado, stock_actual, stock_minimo, fecha_creacion)
                        SELECT id, nombre,
                               CASE WHEN referencia = '' OR referencia IS NULL THEN NULL ELSE referencia END as referencia,
                               precio, categoria, descripcion, imagen_path, iva_recomendado,
                               stock_actual, stock_minimo, fecha_creacion
                        FROM productos
                    ''')
                    print("DEBUG: Données copiées vers productos_temp")

                    # Supprimer l'ancienne table et renommer
                    cursor.execute('DROP TABLE productos')
                    cursor.execute('ALTER TABLE productos_temp RENAME TO productos')
                    print("DEBUG: Table productos remplacée")

                    # Vérifier que la migration a réussi
                    cursor.execute("PRAGMA table_info(productos)")
                    new_columns = cursor.fetchall()
                    new_ref_column = next((col for col in new_columns if col[1] == 'referencia'), None)

                    if new_ref_column and new_ref_column[3] == 0:  # notnull = 0 (optionnel)
                        print("DEBUG: Migration referencia opcional terminée avec succès ✅")
                    else:
                        print(f"DEBUG: Migration échouée, referencia toujours NOT NULL: {new_ref_column}")

                    # Commit pour sauvegarder la migration
                    conn.commit()
                    print("DEBUG: Migration commitée avec succès")

                except Exception as migration_error:
                    print(f"DEBUG: Erreur pendant la migration: {migration_error}")
                    conn.rollback()
                    # Nettoyer en cas d'erreur
                    try:
                        cursor.execute("DROP TABLE IF EXISTS productos_temp")
                    except:
                        pass
                    raise migration_error
            else:
                print("DEBUG: Referencia déjà optionnelle, migration non nécessaire")

        except Exception as e:
            print(f"DEBUG: Erreur migration referencia: {e}")
            import traceback
            traceback.print_exc()
            pass  # Continuer même en cas d'erreur

        # Migración: Cambiar numero_factura_inicial de INTEGER a TEXT para soportar formatos como "2025-FACT-1"
        try:
            # Verificar si la columna es INTEGER
            cursor.execute("PRAGMA table_info(organizacion)")
            columns = cursor.fetchall()
            numero_inicial_column = next((col for col in columns if col[1] == 'numero_factura_inicial'), None)

            if numero_inicial_column and 'INTEGER' in numero_inicial_column[2]:
                # Crear tabla temporal con el nuevo esquema
                cursor.execute('''
                    CREATE TABLE organizacion_temp (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        direccion TEXT,
                        telefono TEXT,
                        email TEXT,
                        cif TEXT,
                        logo_path TEXT,
                        directorio_imagenes_defecto TEXT,
                        numero_factura_inicial TEXT DEFAULT '1',
                        directorio_descargas_pdf TEXT,
                        visor_pdf_personalizado TEXT,
                        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Copiar datos existentes (convertir INTEGER a TEXT)
                cursor.execute('''
                    INSERT INTO organizacion_temp
                    SELECT id, nombre, direccion, telefono, email, cif, logo_path,
                           directorio_imagenes_defecto, CAST(numero_factura_inicial AS TEXT),
                           directorio_descargas_pdf, visor_pdf_personalizado, fecha_actualizacion
                    FROM organizacion
                ''')

                # Eliminar tabla antigua y renombrar la nueva
                cursor.execute('DROP TABLE organizacion')
                cursor.execute('ALTER TABLE organizacion_temp RENAME TO organizacion')

                print("✅ Migración completada: numero_factura_inicial ahora soporta texto")

        except Exception as e:
            print(f"⚠️ Error en migración de numero_factura_inicial: {e}")
            # Continuar sin error para no romper la aplicación
        
        # Tabla stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                producto_id INTEGER PRIMARY KEY,
                cantidad_disponible INTEGER DEFAULT 0,
                stock_minimo INTEGER DEFAULT 0,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')

        # Ajouter la colonne stock_minimo si elle n'existe pas
        try:
            cursor.execute('ALTER TABLE stock ADD COLUMN stock_minimo INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        # Tabla movimientos de stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT,
                fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dni_nie TEXT,
                direccion TEXT,
                email TEXT,
                telefono TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabla facturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                fecha_factura DATE NOT NULL,
                cliente_id INTEGER,
                nombre_cliente TEXT NOT NULL,
                dni_nie_cliente TEXT,
                direccion_cliente TEXT,
                email_cliente TEXT,
                telefono_cliente TEXT,
                subtotal REAL NOT NULL,
                total_iva REAL NOT NULL,
                total_factura REAL NOT NULL,
                modo_pago TEXT,
                estado TEXT DEFAULT 'Borrador',
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

        # Tabla de estados de facturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS factura_estados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT,
                permite_modificacion BOOLEAN DEFAULT 1,
                color TEXT DEFAULT '#007bff',
                orden INTEGER DEFAULT 0,
                activo BOOLEAN DEFAULT 1,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Agregar columna cliente_id a facturas existentes si no existe
        try:
            cursor.execute('ALTER TABLE facturas ADD COLUMN cliente_id INTEGER')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        # Agregar columna estado a facturas existentes si no existe
        try:
            cursor.execute("ALTER TABLE facturas ADD COLUMN estado TEXT DEFAULT 'Borrador'")
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        # Inicializar estados por defecto si no existen
        self._init_default_invoice_statuses(cursor)

        # Tabla items de factura
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS factura_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                iva_aplicado REAL NOT NULL,
                descuento REAL DEFAULT 0,
                subtotal REAL NOT NULL,
                descuento_amount REAL DEFAULT 0,
                iva_amount REAL NOT NULL,
                total REAL NOT NULL,
                FOREIGN KEY (factura_id) REFERENCES facturas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def _init_default_invoice_statuses(self, cursor):
        """Inicializa los estados por defecto de las facturas"""
        try:
            # Verificar si ya existen estados
            cursor.execute("SELECT COUNT(*) FROM factura_estados")
            count = cursor.fetchone()[0]

            if count == 0:
                # Insertar estados por defecto
                default_statuses = [
                    ('Borrador', 'Factura en proceso de creación', 1, '#6c757d', 1),
                    ('Pendiente', 'Factura enviada, pendiente de pago', 0, '#ffc107', 2),
                    ('Pagada', 'Factura pagada completamente', 0, '#28a745', 3),
                    ('Vencida', 'Factura vencida sin pagar', 0, '#dc3545', 4),
                    ('Cancelada', 'Factura cancelada', 0, '#6f42c1', 5),
                    ('Anulada', 'Factura anulada', 0, '#fd7e14', 6)
                ]

                for nombre, descripcion, permite_mod, color, orden in default_statuses:
                    cursor.execute('''
                        INSERT INTO factura_estados (nombre, descripcion, permite_modificacion, color, orden)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (nombre, descripcion, permite_mod, color, orden))

                self.logger.info("Estados de factura por defecto inicializados")

        except Exception as e:
            self.logger.error(f"Error inicializando estados de factura: {e}")

    def execute_query(self, query, params=None):
        """Ejecuta una consulta y devuelve los resultados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if query.strip().upper().startswith(('SELECT', 'PRAGMA')):
            results = cursor.fetchall()
            conn.close()
            return results
        else:
            conn.commit()
            lastrowid = cursor.lastrowid
            conn.close()
            return lastrowid
    
    def get_next_factura_number(self):
        """Genera el siguiente número de factura con año al final"""
        year = datetime.now().year

        # Obtener el último número de factura del año actual
        query = """
        SELECT numero_factura FROM facturas
        WHERE numero_factura LIKE ?
        ORDER BY id DESC LIMIT 1
        """
        result = self.execute_query(query, (f"%-{year}",))

        if result:
            # Extraer el número secuencial del último número
            ultimo_numero = result[0][0]
            try:
                # Buscar el patrón número-año al final
                if f"-{year}" in ultimo_numero:
                    parte_antes_año = ultimo_numero.replace(f"-{year}", "")
                    # Extraer el último número de la parte antes del año
                    import re
                    numeros = re.findall(r'\d+', parte_antes_año)
                    if numeros:
                        ultimo_seq = int(numeros[-1])
                        siguiente_seq = ultimo_seq + 1
                        # Mantener el mismo formato pero incrementar el número
                        nuevo_numero = re.sub(r'\d+(?!.*\d)', str(siguiente_seq), parte_antes_año)
                        return f"{nuevo_numero}-{year}"
            except:
                pass

        # Si no hay facturas previas o hay error, empezar con 1
        return f"1-{year}"

    def get_product_categories(self):
        """Obtiene todas las categorías de productos dinámicamente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT categoria FROM productos WHERE categoria IS NOT NULL AND categoria != '' ORDER BY categoria")
            categories = [row[0] for row in cursor.fetchall()]
            conn.close()
            return categories  # Retourner liste vide si aucune catégorie
        except Exception as e:
            self.logger.error(f"Error obteniendo categorías: {e}")
            return []  # Retourner liste vide en cas d'erreur

    def get_all_products(self):
        """Obtiene todos los productos con información de stock desde tabla stock"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Utiliser uniquement la table stock comme source de vérité
            cursor.execute("""
                SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria, p.descripcion,
                       p.iva_recomendado, p.talla, p.fecha_creacion,
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
                    'precio_compra': row[3] * 0.7,  # Simulado
                    'categoria': row[4],
                    'descripcion': row[5],
                    'iva_recomendado': row[6],
                    'talla': row[7],
                    'fecha_creacion': row[8],
                    'stock_actual': row[9],  # Depuis stock table uniquement
                    'stock_minimo': 5  # Valeur par défaut
                })

            conn.close()
            return products

        except Exception as e:
            self.logger.error(f"Error obteniendo productos: {e}")
            return []

    def update_product_stock(self, product_id, new_stock):
        """Actualiza el stock de un producto en la tabla stock"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Actualizar o insertar en la tabla stock
            cursor.execute("""
                INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(producto_id) DO UPDATE SET
                    cantidad_disponible = excluded.cantidad_disponible,
                    fecha_actualizacion = CURRENT_TIMESTAMP
            """, (product_id, new_stock))

            conn.commit()
            conn.close()
            self.logger.info(f"Stock actualizado para producto {product_id}: {new_stock}")
            return True

        except Exception as e:
            self.logger.error(f"Error actualizando stock del producto {product_id}: {e}")
            raise e

    def adjust_product_stock(self, product_id, adjustment):
        """Ajusta el stock de un producto (+ o -) en la tabla stock"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Obtener el stock actual desde la tabla stock
            cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (product_id,))
            result = cursor.fetchone()

            if not result:
                # Si no existe entrada en stock, crearla con el ajuste
                new_stock = max(0, adjustment)
                cursor.execute("""
                    INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (product_id, new_stock))
                current_stock = 0
            else:
                current_stock = result[0] or 0
                new_stock = max(0, current_stock + adjustment)  # No permitir stock negativo

                # Actualizar el stock
                cursor.execute("""
                    UPDATE stock
                    SET cantidad_disponible = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE producto_id = ?
                """, (new_stock, product_id))

            conn.commit()
            conn.close()

            self.logger.info(f"Stock ajustado para producto {product_id}: {current_stock} → {new_stock} ({adjustment:+d})")
            return new_stock

        except Exception as e:
            self.logger.error(f"Error ajustando stock del producto {product_id}: {e}")
            raise e

    def get_products_with_low_stock(self):
        """Obtiene productos con stock bajo (menor al mínimo)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Utiliser la tabla stock, stock_minimo par défaut = 5
            cursor.execute("""
                SELECT p.id, p.nombre, p.referencia,
                       COALESCE(s.cantidad_disponible, 0) as stock_actual,
                       5 as stock_minimo
                FROM productos p
                LEFT JOIN stock s ON p.id = s.producto_id
                WHERE COALESCE(s.cantidad_disponible, 0) < 5
                ORDER BY COALESCE(s.cantidad_disponible, 0) ASC
            """)

            products = []
            for row in cursor.fetchall():
                product = {
                    'id': row[0],
                    'nombre': row[1],
                    'referencia': row[2],
                    'stock_actual': row[3],
                    'stock_minimo': row[4]
                }
                products.append(product)

            conn.close()
            return products

        except Exception as e:
            self.logger.error(f"Error obteniendo productos con stock bajo: {e}")
            return []

    def process_invoice_stock_movement(self, invoice_data, operation='subtract'):
        """Procesa el movimiento de stock para una factura

        Args:
            invoice_data: Datos de la factura con líneas
            operation: 'subtract' para venta (por defecto), 'add' para devolución
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            movements_processed = []

            for linea in invoice_data.get('lineas', []):
                producto_id = linea.get('producto_id')
                cantidad = linea.get('cantidad', 0)

                if not producto_id or cantidad <= 0:
                    continue

                # Obtener el stock actual desde la tabla stock
                cursor.execute("""
                    SELECT COALESCE(s.cantidad_disponible, 0), p.nombre
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    WHERE p.id = ?
                """, (producto_id,))
                result = cursor.fetchone()

                if not result:
                    self.logger.warning(f"Producto {producto_id} no encontrado para movimiento de stock")
                    continue

                stock_actual, nombre_producto = result

                # Calcular el nuevo stock
                if operation == 'subtract':
                    nuevo_stock = max(0, stock_actual - cantidad)  # No permitir stock negativo
                    movimiento = -cantidad
                elif operation == 'add':
                    nuevo_stock = stock_actual + cantidad
                    movimiento = cantidad
                else:
                    raise ValueError(f"Operación no válida: {operation}")

                # Actualizar el stock en la tabla stock
                cursor.execute("""
                    INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(producto_id) DO UPDATE SET
                        cantidad_disponible = excluded.cantidad_disponible,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                """, (producto_id, nuevo_stock))

                # Registrar el movimiento
                movements_processed.append({
                    'producto_id': producto_id,
                    'nombre_producto': nombre_producto,
                    'stock_anterior': stock_actual,
                    'movimiento': movimiento,
                    'stock_nuevo': nuevo_stock
                })

                self.logger.info(f"Stock actualizado - {nombre_producto}: {stock_actual} → {nuevo_stock} ({movimiento:+d})")

            conn.commit()
            conn.close()

            return movements_processed

        except Exception as e:
            self.logger.error(f"Error procesando movimiento de stock: {e}")
            raise e

    def _process_invoice_stock_movement_with_connection(self, cursor, invoice_data, operation='subtract'):
        """Procesa el movimiento de stock usando una conexión existente"""
        try:
            movements_processed = []

            for linea in invoice_data.get('lineas', []):
                producto_id = linea.get('producto_id')
                cantidad = linea.get('cantidad', 0)

                if not producto_id or cantidad <= 0:
                    continue

                # Obtener el stock actual desde la tabla stock
                cursor.execute("""
                    SELECT COALESCE(s.cantidad_disponible, 0), p.nombre
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    WHERE p.id = ?
                """, (producto_id,))
                result = cursor.fetchone()

                if not result:
                    self.logger.warning(f"Producto {producto_id} no encontrado para movimiento de stock")
                    continue

                stock_actual, nombre_producto = result

                # Calcular el nuevo stock
                if operation == 'subtract':
                    nuevo_stock = max(0, stock_actual - cantidad)  # No permitir stock negativo
                    movimiento = -cantidad
                elif operation == 'add':
                    nuevo_stock = stock_actual + cantidad
                    movimiento = cantidad
                else:
                    raise ValueError(f"Operación no válida: {operation}")

                # Actualizar el stock en la tabla stock
                cursor.execute("""
                    INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(producto_id) DO UPDATE SET
                        cantidad_disponible = excluded.cantidad_disponible,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                """, (producto_id, nuevo_stock))

                # Registrar el movimiento
                movements_processed.append({
                    'producto_id': producto_id,
                    'nombre_producto': nombre_producto,
                    'stock_anterior': stock_actual,
                    'movimiento': movimiento,
                    'stock_nuevo': nuevo_stock
                })

                self.logger.info(f"Stock actualizado - {nombre_producto}: {stock_actual} → {nuevo_stock} ({movimiento:+d})")

            return movements_processed

        except Exception as e:
            self.logger.error(f"Error procesando movimiento de stock con conexión: {e}")
            raise e

    def reverse_invoice_stock_movement(self, invoice_id):
        """Revierte el movimiento de stock de una factura (para modificaciones)"""
        try:
            # Obtener la factura original
            original_invoice = self.get_invoice_by_id(invoice_id)
            if not original_invoice:
                return []

            # Revertir el movimiento (añadir de vuelta al stock)
            return self.process_invoice_stock_movement(original_invoice, operation='add')

        except Exception as e:
            self.logger.error(f"Error revirtiendo movimiento de stock para factura {invoice_id}: {e}")
            raise e

    def get_product_by_id(self, product_id):
        """Obtiene un producto por su ID"""
        try:
            conn = self.get_connection()
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
            conn.close()

            if row:
                return {
                    'id': row[0],
                    'nombre': row[1],
                    'referencia': row[2],
                    'precio_venta': row[3],
                    'precio_compra': row[3] * 0.7,  # Simulado
                    'categoria': row[4],
                    'descripcion': row[5],
                    'iva_recomendado': row[6],
                    'talla': row[7],
                    'fecha_creacion': row[8],
                    'stock_actual': row[9]
                }
            return None

        except Exception as e:
            self.logger.error(f"Error obteniendo producto {product_id}: {e}")
            return None

    def add_product(self, product_data):
        """Añade un nuevo producto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Obtenir le stock depuis les données (avec fallback)
            stock_actual = product_data.get('stock', product_data.get('stock_actual', 0))

            # Obtenir la talla si elle existe
            talla = product_data.get('talla', None)

            cursor.execute("""
                INSERT INTO productos (nombre, referencia, precio, categoria, descripcion, iva_recomendado, talla)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product_data['nombre'],
                product_data.get('referencia', None),
                product_data.get('precio', product_data.get('precio_venta', 0.0)),
                product_data.get('categoria', ''),
                product_data.get('descripcion', ''),
                product_data.get('iva_recomendado', 21.0),
                talla
            ))

            product_id = cursor.lastrowid

            # Créer l'entrée dans la table stock
            cursor.execute("""
                INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (product_id, stock_actual))

            conn.commit()
            conn.close()

            self.logger.info(f"Producto añadido con ID: {product_id}, stock: {stock_actual}")
            return product_id

        except Exception as e:
            self.logger.error(f"Error añadiendo producto: {e}")
            raise e

    def update_product(self, product_data):
        """Actualiza un producto existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Obtenir le stock depuis les données (avec fallback)
            stock_actual = product_data.get('stock', product_data.get('stock_actual', 0))

            # Obtenir la talla si elle existe
            talla = product_data.get('talla', None)

            cursor.execute("""
                UPDATE productos
                SET nombre = ?, referencia = ?, precio = ?, categoria = ?, descripcion = ?, iva_recomendado = ?, talla = ?
                WHERE id = ?
            """, (
                product_data['nombre'],
                product_data['referencia'],
                product_data['precio_venta'],
                product_data['categoria'],
                product_data['descripcion'],
                product_data.get('iva_recomendado', 21.0),
                talla,
                product_data['id']
            ))

            # Mettre à jour le stock dans la table stock
            cursor.execute("""
                INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(producto_id) DO UPDATE SET
                    cantidad_disponible = excluded.cantidad_disponible,
                    fecha_actualizacion = CURRENT_TIMESTAMP
            """, (product_data['id'], stock_actual))

            conn.commit()
            conn.close()

            self.logger.info(f"Producto {product_data['id']} actualizado, stock: {stock_actual}")
            return True

        except Exception as e:
            self.logger.error(f"Error actualizando producto: {e}")
            raise e

    def delete_product(self, product_id):
        """Elimina un producto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))

            conn.commit()
            conn.close()

            self.logger.info(f"Producto {product_id} eliminado")

        except Exception as e:
            self.logger.error(f"Error eliminando producto: {e}")
            raise e

    # ==================== MÉTODOS PARA CLIENTES ====================

    def get_all_clients(self):
        """Obtiene todos los clientes"""
        try:
            conn = self.get_connection()
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

            conn.close()
            return clients

        except Exception as e:
            self.logger.error(f"Error obteniendo clientes: {e}")
            return []

    def add_client(self, client_data):
        """Añade un nuevo cliente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, dni_nie, direccion, email, telefono)
                VALUES (?, ?, ?, ?, ?)
            """, (
                client_data['nombre'],
                client_data.get('nif', ''),  # Mapear nif a dni_nie
                client_data.get('direccion', ''),
                client_data.get('email', ''),
                client_data.get('telefono', '')
            ))

            client_id = cursor.lastrowid
            conn.commit()
            conn.close()

            self.logger.info(f"Cliente añadido con ID: {client_id}")
            return client_id

        except Exception as e:
            self.logger.error(f"Error añadiendo cliente: {e}")
            raise e

    def update_client(self, client_data):
        """Actualiza un cliente existente"""
        try:
            conn = self.get_connection()
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
                conn.commit()
                conn.close()
                self.logger.info(f"Cliente {client_data['id']} actualizado")
                return True
            else:
                conn.close()
                self.logger.warning(f"Cliente {client_data['id']} no encontrado para actualizar")
                return False

        except Exception as e:
            self.logger.error(f"Error actualizando cliente: {e}")
            raise e

    def get_client_by_name(self, nombre):
        """Busca un cliente por nombre, priorizando el que tiene más datos"""
        try:
            conn = self.get_connection()
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
            conn.close()

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
            self.logger.error(f"Error buscando cliente: {e}")
            return None

    def get_client_by_id(self, client_id):
        """Obtiene un cliente por su ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, dni_nie, direccion, email, telefono, fecha_creacion
                FROM clientes
                WHERE id = ?
            """, (client_id,))

            row = cursor.fetchone()
            conn.close()

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

    def delete_client(self, client_id):
        """Elimina un cliente por ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Verificar si el cliente tiene facturas asociadas
            cursor.execute("SELECT COUNT(*) FROM facturas WHERE cliente_id = ?", (client_id,))
            invoice_count = cursor.fetchone()[0]

            if invoice_count > 0:
                conn.close()
                raise Exception(f"No se puede eliminar el cliente. Tiene {invoice_count} factura(s) asociada(s).")

            # Eliminar el cliente
            cursor.execute("DELETE FROM clientes WHERE id = ?", (client_id,))

            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                self.logger.info(f"Cliente {client_id} eliminado")
                return True
            else:
                conn.close()
                self.logger.warning(f"Cliente {client_id} no encontrado")
                return False

        except Exception as e:
            self.logger.error(f"Error eliminando cliente {client_id}: {e}")
            raise e

    def delete_multiple_clients(self, client_ids):
        """Elimina múltiples clientes por IDs"""
        try:
            conn = self.get_connection()
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

                conn.close()
                raise Exception(f"No se pueden eliminar algunos clientes con facturas asociadas:\n" +
                              "\n".join(error_details))

            # Eliminar los clientes
            cursor.execute(f"DELETE FROM clientes WHERE id IN ({placeholders})", client_ids)

            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            self.logger.info(f"{deleted_count} clientes eliminados")
            return deleted_count

        except Exception as e:
            self.logger.error(f"Error eliminando clientes múltiples: {e}")
            raise e

    # ==================== MÉTODOS PARA FACTURAS ====================

    def add_invoice(self, invoice_data):
        """Añade una nueva factura completa"""
        try:
            conn = self.get_connection()
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
                cursor.execute("""
                    INSERT INTO factura_items (factura_id, producto_id, cantidad, precio_unitario,
                                             iva_aplicado, descuento, subtotal, descuento_amount,
                                             iva_amount, total)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    factura_id,
                    linea.get('producto_id'),
                    linea.get('cantidad', 1),
                    linea.get('precio_unitario', 0.0),
                    linea.get('iva_aplicado', 21.0),
                    linea.get('descuento', 0.0),
                    linea.get('subtotal', 0.0),
                    linea.get('descuento_amount', 0.0),
                    linea.get('iva_amount', 0.0),
                    linea.get('total', 0.0)
                ))

            # Procesar movimiento de stock (restar del inventario) usando la misma conexión
            print(f"DEBUG DB: Procesando stock para factura con {len(invoice_data.get('lineas', []))} líneas")
            stock_movements = self._process_invoice_stock_movement_with_connection(cursor, invoice_data, operation='subtract')
            print(f"DEBUG DB: Stock movements procesados: {len(stock_movements) if stock_movements else 0}")

            conn.commit()
            conn.close()

            self.logger.info(f"Factura añadida con ID: {factura_id}")
            if stock_movements:
                self.logger.info(f"Movimientos de stock procesados: {len(stock_movements)} productos")
                for movement in stock_movements:
                    print(f"DEBUG: {movement['nombre_producto']}: {movement['stock_anterior']} → {movement['stock_nuevo']}")
                for movement in stock_movements:
                    self.logger.info(f"  • {movement['nombre_producto']}: {movement['stock_anterior']} → {movement['stock_nuevo']}")

            return factura_id

        except Exception as e:
            self.logger.error(f"Error añadiendo factura: {e}")
            raise e

    def update_invoice(self, invoice_data):
        """Actualiza una factura existente"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Datos de la factura
            invoice_id = invoice_data['id']
            numero_factura = invoice_data['numero']
            fecha_factura = invoice_data['fecha']
            cliente_data = invoice_data['cliente']
            subtotal = invoice_data['subtotal']
            iva_total = invoice_data['iva_total']
            total = invoice_data['total']

            # Actualizar la factura
            cursor.execute("""
                UPDATE facturas SET
                    numero_factura = ?,
                    fecha_factura = ?,
                    cliente_id = ?,
                    nombre_cliente = ?,
                    dni_nie_cliente = ?,
                    direccion_cliente = ?,
                    subtotal = ?,
                    total_iva = ?,
                    total_factura = ?,
                    estado = ?
                WHERE id = ?
            """, (
                numero_factura,
                fecha_factura,
                cliente_data.get('id'),
                cliente_data.get('nombre', ''),
                cliente_data.get('nif', ''),
                cliente_data.get('direccion', ''),
                subtotal,
                iva_total,
                total,
                invoice_data.get('estado', 'Borrador'),
                invoice_id
            ))

            if cursor.rowcount > 0:
                # Revertir el movimiento de stock de la factura original
                try:
                    # Obtener las líneas originales de la factura
                    cursor.execute("""
                        SELECT fi.producto_id, fi.cantidad
                        FROM factura_items fi
                        WHERE fi.factura_id = ?
                    """, (invoice_id,))

                    original_lines = []
                    for row in cursor.fetchall():
                        original_lines.append({
                            'producto_id': row[0],
                            'cantidad': row[1]
                        })

                    if original_lines:
                        original_invoice_data = {'lineas': original_lines}
                        reversed_movements = self._process_invoice_stock_movement_with_connection(cursor, original_invoice_data, operation='add')
                        if reversed_movements:
                            self.logger.info(f"Stock revertido para {len(reversed_movements)} productos")
                except Exception as e:
                    self.logger.warning(f"Error revirtiendo stock: {e}")

                # Actualizar las líneas de factura
                # Primero, eliminar las líneas existentes
                cursor.execute("DELETE FROM factura_items WHERE factura_id = ?", (invoice_id,))

                # Luego, insertar las nuevas líneas
                lineas = invoice_data.get('lineas', [])
                for linea in lineas:
                    cursor.execute("""
                        INSERT INTO factura_items (factura_id, producto_id, cantidad, precio_unitario,
                                                 iva_aplicado, descuento, subtotal, descuento_amount,
                                                 iva_amount, total)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        invoice_id,
                        linea.get('producto_id'),
                        linea.get('cantidad', 1),
                        linea.get('precio_unitario', 0.0),
                        linea.get('iva_aplicado', 21.0),
                        linea.get('descuento', 0.0),
                        linea.get('subtotal', 0.0),
                        linea.get('descuento_amount', 0.0),
                        linea.get('iva_amount', 0.0),
                        linea.get('total', 0.0)
                    ))

                # Procesar el nuevo movimiento de stock
                try:
                    new_movements = self._process_invoice_stock_movement_with_connection(cursor, invoice_data, operation='subtract')
                    if new_movements:
                        self.logger.info(f"Nuevo stock procesado para {len(new_movements)} productos")
                except Exception as e:
                    self.logger.warning(f"Error procesando nuevo stock: {e}")

                conn.commit()
                conn.close()
                self.logger.info(f"Factura {invoice_id} actualizada con {len(lineas)} líneas")
                return True
            else:
                conn.close()
                self.logger.warning(f"Factura {invoice_id} no encontrada para actualizar")
                return False

        except Exception as e:
            self.logger.error(f"Error actualizando factura {invoice_data.get('id', 'N/A')}: {e}")
            raise e

    def get_all_invoices(self):
        """Obtiene todas las facturas"""
        try:
            conn = self.get_connection()
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
                    'estado': row[7] if row[7] else 'Borrador'  # Estado desde la base de datos
                }
                invoices.append(invoice)

            conn.close()
            return invoices

        except Exception as e:
            self.logger.error(f"Error obteniendo facturas: {e}")
            return []

    def get_invoice_by_id(self, invoice_id):
        """Obtiene una factura completa por ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Obtener datos de la factura
            cursor.execute("""
                SELECT id, numero_factura, fecha_factura, cliente_id,
                       nombre_cliente, dni_nie_cliente, direccion_cliente,
                       subtotal, total_iva, total_factura, estado
                FROM facturas
                WHERE id = ?
            """, (invoice_id,))

            factura_row = cursor.fetchone()
            conn.close()

            if not factura_row:
                return None

            # Construir el objeto factura
            invoice_data = {
                'id': factura_row[0],
                'numero': factura_row[1],
                'fecha': factura_row[2],
                'vencimiento': factura_row[2],  # Usar la misma fecha par défaut
                'cliente': {
                    'id': factura_row[3],
                    'nombre': factura_row[4],
                    'nif': factura_row[5] or '',
                    'direccion': factura_row[6] or ''
                },
                'subtotal': factura_row[7],
                'iva_total': factura_row[8],
                'total': factura_row[9],
                'estado': factura_row[10] if factura_row[10] else 'Borrador',  # Estado desde la base de datos
                'lineas': []  # Pour l'instant, pas de lignes détaillées
            }

            # Cargar las líneas de la factura
            invoice_data['lineas'] = self.get_invoice_items(factura_row[0])

            return invoice_data

        except Exception as e:
            self.logger.error(f"Error obteniendo factura {invoice_id}: {e}")
            return None

    def get_invoice_by_number(self, numero_factura):
        """Obtiene una factura por su número"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, numero_factura, fecha_factura, cliente_id,
                       nombre_cliente, dni_nie_cliente, direccion_cliente,
                       subtotal, total_iva, total_factura
                FROM facturas
                WHERE numero_factura = ?
            """, (numero_factura,))

            factura_row = cursor.fetchone()
            conn.close()

            if not factura_row:
                return None

            # Construir le même objet que get_invoice_by_id
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
                'estado': 'Pendiente',
                'lineas': []
            }

            # Cargar las líneas de la factura
            invoice_data['lineas'] = self.get_invoice_items(factura_row[0])

            return invoice_data

        except Exception as e:
            self.logger.error(f"Error obteniendo factura por número {numero_factura}: {e}")
            return None

    def get_invoice_items(self, invoice_id):
        """Obtiene las líneas de una factura"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT fi.id, fi.producto_id, fi.cantidad, fi.precio_unitario,
                       fi.iva_aplicado, fi.descuento, fi.subtotal, fi.iva_amount, fi.total,
                       p.nombre as producto_nombre, p.referencia as producto_referencia
                FROM factura_items fi
                LEFT JOIN productos p ON fi.producto_id = p.id
                WHERE fi.factura_id = ?
                ORDER BY fi.id
            """, (invoice_id,))

            items = []
            for row in cursor.fetchall():
                item = {
                    'id': row[0],
                    'producto_id': row[1],
                    'cantidad': row[2],
                    'precio_unitario': row[3],
                    'iva_aplicado': row[4],
                    'descuento': row[5] or 0.0,
                    'subtotal': row[6],
                    'iva_amount': row[7],
                    'total': row[8],
                    'producto_nombre': row[9] or 'Producto eliminado',
                    'producto_referencia': row[10] or 'N/A'
                }
                items.append(item)

            conn.close()
            return items

        except Exception as e:
            self.logger.error(f"Error obteniendo líneas de factura {invoice_id}: {e}")
            return []

    def delete_invoice(self, invoice_id):
        """Elimina una factura por ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Eliminar la factura
            cursor.execute("DELETE FROM facturas WHERE id = ?", (invoice_id,))

            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                self.logger.info(f"Factura {invoice_id} eliminada")
                return True
            else:
                conn.close()
                self.logger.warning(f"Factura {invoice_id} no encontrada")
                return False

        except Exception as e:
            self.logger.error(f"Error eliminando factura {invoice_id}: {e}")
            raise e

    def delete_multiple_invoices(self, invoice_ids):
        """Elimina múltiples facturas por IDs"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Crear placeholders para la consulta
            placeholders = ','.join(['?' for _ in invoice_ids])

            # Eliminar las facturas
            cursor.execute(f"DELETE FROM facturas WHERE id IN ({placeholders})", invoice_ids)

            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            self.logger.info(f"{deleted_count} facturas eliminadas")
            return deleted_count

        except Exception as e:
            self.logger.error(f"Error eliminando facturas múltiples: {e}")
            raise e

    def get_invoice_id_by_number(self, numero_factura):
        """Obtiene el ID de una factura por su número"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM facturas WHERE numero_factura = ?", (numero_factura,))

            row = cursor.fetchone()
            conn.close()

            return row[0] if row else None

        except Exception as e:
            self.logger.error(f"Error obteniendo ID de factura {numero_factura}: {e}")
            return None

    def get_last_invoice_number(self):
        """Obtiene el último número de factura"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT numero_factura FROM facturas
                ORDER BY id DESC LIMIT 1
            """)

            row = cursor.fetchone()
            conn.close()

            return row[0] if row else None

        except Exception as e:
            self.logger.error(f"Error obteniendo último número de factura: {e}")
            return None

    # ==================== MÉTODOS PARA ESTADOS DE FACTURAS ====================

    def get_all_invoice_statuses(self):
        """Obtiene todos los estados de facturas"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, descripcion, permite_modificacion, color, orden, activo
                FROM factura_estados
                WHERE activo = 1
                ORDER BY orden
            """)

            statuses = []
            for row in cursor.fetchall():
                status = {
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2],
                    'permite_modificacion': bool(row[3]),
                    'color': row[4],
                    'orden': row[5],
                    'activo': bool(row[6])
                }
                statuses.append(status)

            conn.close()
            return statuses

        except Exception as e:
            self.logger.error(f"Error obteniendo estados de facturas: {e}")
            return []

    def save_invoice_status(self, status_data):
        """Guarda o actualiza un estado de factura"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            if status_data.get('id'):
                # Actualizar estado existente
                cursor.execute("""
                    UPDATE factura_estados SET
                        nombre = ?,
                        descripcion = ?,
                        permite_modificacion = ?,
                        color = ?,
                        orden = ?
                    WHERE id = ?
                """, (
                    status_data['nombre'],
                    status_data['descripcion'],
                    status_data['permite_modificacion'],
                    status_data['color'],
                    status_data['orden'],
                    status_data['id']
                ))
            else:
                # Crear nuevo estado
                cursor.execute("""
                    INSERT INTO factura_estados (nombre, descripcion, permite_modificacion, color, orden)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    status_data['nombre'],
                    status_data['descripcion'],
                    status_data['permite_modificacion'],
                    status_data['color'],
                    status_data['orden']
                ))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            self.logger.error(f"Error guardando estado de factura: {e}")
            return False

    def delete_invoice_status(self, status_id):
        """Elimina un estado de factura (marca como inactivo)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Marcar como inactivo en lugar de eliminar
            cursor.execute("UPDATE factura_estados SET activo = 0 WHERE id = ?", (status_id,))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            self.logger.error(f"Error eliminando estado de factura: {e}")
            return False

    def get_invoice_status_by_name(self, status_name):
        """Obtiene un estado de factura por nombre"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, descripcion, permite_modificacion, color, orden, activo
                FROM factura_estados
                WHERE nombre = ? AND activo = 1
            """, (status_name,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2],
                    'permite_modificacion': bool(row[3]),
                    'color': row[4],
                    'orden': row[5],
                    'activo': bool(row[6])
                }
            return None

        except Exception as e:
            self.logger.error(f"Error obteniendo estado por nombre {status_name}: {e}")
            return None

    def add_invoice_state(self, state_data):
        """Añade un nuevo estado de factura"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Valores por defecto
            nombre = state_data.get('nombre', '')
            descripcion = state_data.get('descripcion', '')
            permite_modificacion = state_data.get('permite_modificacion', True)
            color = state_data.get('color', '#007bff')
            orden = state_data.get('orden', 0)

            # Verificar si ya existe un estado con ese nombre
            cursor.execute("SELECT id FROM factura_estados WHERE nombre = ?", (nombre,))
            existing = cursor.fetchone()
            if existing:
                conn.close()
                self.logger.warning(f"Estado de factura ya existe: {nombre}")
                return existing[0]

            # Si no se especifica orden, usar el siguiente disponible
            if orden == 0:
                cursor.execute("SELECT MAX(orden) FROM factura_estados")
                max_orden = cursor.fetchone()[0]
                orden = (max_orden or 0) + 1

            cursor.execute("""
                INSERT INTO factura_estados (nombre, descripcion, permite_modificacion, color, orden)
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, descripcion, permite_modificacion, color, orden))

            state_id = cursor.lastrowid
            conn.commit()
            conn.close()

            self.logger.info(f"Estado de factura añadido: {nombre} (ID: {state_id})")
            return state_id

        except Exception as e:
            self.logger.error(f"Error añadiendo estado de factura: {e}")
            return None

    # ==================== MÉTODOS PARA ORGANIZACIÓN ====================

    def get_organization_info(self):
        """Obtiene la información de la organización"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, direccion, telefono, email, cif, logo_path,
                       directorio_imagenes_defecto, numero_factura_inicial,
                       directorio_descargas_pdf, visor_pdf_personalizado, logo_orientation,
                       directorio_logos_storage
                FROM organizacion
                WHERE id = 1
            """)

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    'id': row[0],
                    'nombre': row[1] or '',
                    'direccion': row[2] or '',
                    'telefono': row[3] or '',
                    'email': row[4] or '',
                    'cif': row[5] or '',
                    'logo_path': row[6] or '',
                    'directorio_imagenes_defecto': row[7] or '',
                    'numero_factura_inicial': row[8] or '1',
                    'directorio_descargas_pdf': row[9] or '',
                    'visor_pdf_personalizado': row[10] or '',
                    'logo_orientation': row[11] if len(row) > 11 else 'landscape',
                    'directorio_logos_storage': row[12] if len(row) > 12 else ''
                }
            return None

        except Exception as e:
            self.logger.error(f"Error obteniendo información de organización: {e}")
            return None

    def create_organization(self, org_data):
        """Crea la información de la organización"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO organizacion
                (id, nombre, direccion, telefono, email, cif, logo_path,
                 directorio_imagenes_defecto, numero_factura_inicial,
                 directorio_descargas_pdf, visor_pdf_personalizado, logo_orientation,
                 directorio_logos_storage)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                org_data.get('nombre', ''),
                org_data.get('direccion', ''),
                org_data.get('telefono', ''),
                org_data.get('email', ''),
                org_data.get('cif', ''),
                org_data.get('logo_path', ''),
                org_data.get('directorio_imagenes_defecto', ''),
                org_data.get('numero_factura_inicial', '1'),
                org_data.get('directorio_descargas_pdf', ''),
                org_data.get('visor_pdf_personalizado', ''),
                org_data.get('logo_orientation', 'landscape'),
                org_data.get('directorio_logos_storage', '')
            ))

            conn.commit()
            conn.close()
            self.logger.info("Información de organización creada")

        except Exception as e:
            self.logger.error(f"Error creando organización: {e}")
            raise e

    def create_organization(self, org_data):
        """Crea una nueva organización"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO organizacion (
                    nombre, direccion, telefono, email, cif, logo_path,
                    directorio_imagenes_defecto, numero_factura_inicial,
                    directorio_descargas_pdf, visor_pdf_personalizado,
                    logo_orientation, directorio_logos_storage
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                org_data.get('nombre', ''),
                org_data.get('direccion', ''),
                org_data.get('telefono', ''),
                org_data.get('email', ''),
                org_data.get('cif', ''),
                org_data.get('logo_path', ''),
                org_data.get('directorio_imagenes_defecto', ''),
                org_data.get('numero_factura_inicial', '1'),
                org_data.get('directorio_descargas_pdf', ''),
                org_data.get('visor_pdf_personalizado', ''),
                org_data.get('logo_orientation', 'landscape'),
                org_data.get('directorio_logos_storage', '')
            ))

            org_id = cursor.lastrowid
            conn.commit()
            conn.close()

            self.logger.info(f"Organización creada con ID: {org_id}")
            return org_id

        except Exception as e:
            self.logger.error(f"Error creando organización: {e}")
            return None

    def update_organization(self, org_data):
        """Actualiza la información de la organización"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE organizacion
                SET nombre = ?, direccion = ?, telefono = ?, email = ?, cif = ?,
                    logo_path = ?, directorio_imagenes_defecto = ?, numero_factura_inicial = ?,
                    directorio_descargas_pdf = ?, visor_pdf_personalizado = ?, logo_orientation = ?,
                    directorio_logos_storage = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                org_data.get('nombre', ''),
                org_data.get('direccion', ''),
                org_data.get('telefono', ''),
                org_data.get('email', ''),
                org_data.get('cif', ''),
                org_data.get('logo_path', ''),
                org_data.get('directorio_imagenes_defecto', ''),
                org_data.get('numero_factura_inicial', '1'),
                org_data.get('directorio_descargas_pdf', ''),
                org_data.get('visor_pdf_personalizado', ''),
                org_data.get('logo_orientation', 'landscape'),
                org_data.get('directorio_logos_storage', ''),
                org_data.get('id', 1)
            ))

            conn.commit()
            conn.close()
            self.logger.info(f"Información de organización actualizada")
            return True

        except Exception as e:
            self.logger.error(f"Error actualizando organización: {e}")
            raise e

# Instancia global de la base de datos
db = Database()
