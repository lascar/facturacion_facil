import sqlite3
import os
from datetime import datetime
from utils.logger import get_logger, log_database_operation, log_exception

class Database:
    def __init__(self, db_path="facturacion.db"):
        self.db_path = db_path
        self.logger = get_logger("database")
        self.init_database()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                referencia TEXT UNIQUE NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT,
                descripcion TEXT,
                imagen_path TEXT,
                iva_recomendado REAL DEFAULT 21.0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
                numero_factura_inicial INTEGER DEFAULT 1,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Agregar columnas nuevas si no existen (para compatibilidad con bases de datos existentes)
        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN directorio_imagenes_defecto TEXT')
        except sqlite3.OperationalError:
            pass  # La columna ya existe

        try:
            cursor.execute('ALTER TABLE organizacion ADD COLUMN numero_factura_inicial INTEGER DEFAULT 1')
        except sqlite3.OperationalError:
            pass  # La columna ya existe
        
        # Tabla stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                producto_id INTEGER PRIMARY KEY,
                cantidad_disponible INTEGER DEFAULT 0,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla facturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                fecha_factura DATE NOT NULL,
                nombre_cliente TEXT NOT NULL,
                dni_nie_cliente TEXT,
                direccion_cliente TEXT,
                email_cliente TEXT,
                telefono_cliente TEXT,
                subtotal REAL NOT NULL,
                total_iva REAL NOT NULL,
                total_factura REAL NOT NULL,
                modo_pago TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

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

# Instancia global de la base de datos
db = Database()
