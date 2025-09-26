from .database import db
from datetime import datetime

class Producto:
    def __init__(self, id=None, nombre="", referencia="", precio=0.0, 
                 categoria="", descripcion="", imagen_path="", iva_recomendado=21.0):
        self.id = id
        self.nombre = nombre
        self.referencia = referencia
        self.precio = precio
        self.categoria = categoria
        self.descripcion = descripcion
        self.imagen_path = imagen_path
        self.iva_recomendado = iva_recomendado
    
    def save(self):
        """Guarda el producto en la base de datos"""
        if self.id:
            # Actualizar producto existente
            query = '''UPDATE productos SET nombre=?, referencia=?, precio=?, 
                      categoria=?, descripcion=?, imagen_path=?, iva_recomendado=? 
                      WHERE id=?'''
            params = (self.nombre, self.referencia, self.precio, self.categoria,
                     self.descripcion, self.imagen_path, self.iva_recomendado, self.id)
            db.execute_query(query, params)
        else:
            # Crear nuevo producto
            query = '''INSERT INTO productos (nombre, referencia, precio, categoria, 
                      descripcion, imagen_path, iva_recomendado) 
                      VALUES (?, ?, ?, ?, ?, ?, ?)'''
            params = (self.nombre, self.referencia, self.precio, self.categoria,
                     self.descripcion, self.imagen_path, self.iva_recomendado)
            self.id = db.execute_query(query, params)
            
            # Crear entrada en stock
            Stock.create_for_product(self.id)
    
    def delete(self):
        """Elimina el producto de la base de datos"""
        if self.id:
            # Eliminar stock asociado
            db.execute_query("DELETE FROM stock WHERE producto_id=?", (self.id,))
            # Eliminar producto
            db.execute_query("DELETE FROM productos WHERE id=?", (self.id,))
    
    @staticmethod
    def get_all():
        """Obtiene todos los productos"""
        query = "SELECT * FROM productos ORDER BY nombre"
        results = db.execute_query(query)
        productos = []
        for row in results:
            producto = Producto(
                id=row[0], nombre=row[1], referencia=row[2], precio=row[3],
                categoria=row[4], descripcion=row[5], imagen_path=row[6],
                iva_recomendado=row[7]
            )
            productos.append(producto)
        return productos
    
    @staticmethod
    def get_by_id(producto_id):
        """Obtiene un producto por su ID"""
        query = "SELECT * FROM productos WHERE id=?"
        results = db.execute_query(query, (producto_id,))
        if results:
            row = results[0]
            return Producto(
                id=row[0], nombre=row[1], referencia=row[2], precio=row[3],
                categoria=row[4], descripcion=row[5], imagen_path=row[6],
                iva_recomendado=row[7]
            )
        return None

class Factura:
    def __init__(self, id=None, numero_factura="", fecha_factura="", nombre_cliente="",
                 dni_nie_cliente="", direccion_cliente="", email_cliente="", telefono_cliente="",
                 subtotal=0.0, total_iva=0.0, total_factura=0.0, modo_pago="", fecha_creacion=""):
        self.id = id
        self.numero_factura = numero_factura
        self.fecha_factura = fecha_factura
        self.nombre_cliente = nombre_cliente
        self.dni_nie_cliente = dni_nie_cliente
        self.direccion_cliente = direccion_cliente
        self.email_cliente = email_cliente
        self.telefono_cliente = telefono_cliente
        self.subtotal = subtotal
        self.total_iva = total_iva
        self.total_factura = total_factura
        self.modo_pago = modo_pago
        self.fecha_creacion = fecha_creacion
        self.items = []  # Lista de FacturaItem

    def save(self):
        """Guarda la factura en la base de datos"""
        if self.id:
            # Actualizar factura existente
            query = '''UPDATE facturas SET numero_factura=?, fecha_factura=?, nombre_cliente=?,
                      dni_nie_cliente=?, direccion_cliente=?, email_cliente=?, telefono_cliente=?,
                      subtotal=?, total_iva=?, total_factura=?, modo_pago=? WHERE id=?'''
            params = (self.numero_factura, self.fecha_factura, self.nombre_cliente,
                     self.dni_nie_cliente, self.direccion_cliente, self.email_cliente,
                     self.telefono_cliente, self.subtotal, self.total_iva, self.total_factura,
                     self.modo_pago, self.id)
            db.execute_query(query, params)
        else:
            # Crear nueva factura
            query = '''INSERT INTO facturas (numero_factura, fecha_factura, nombre_cliente,
                      dni_nie_cliente, direccion_cliente, email_cliente, telefono_cliente,
                      subtotal, total_iva, total_factura, modo_pago)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            params = (self.numero_factura, self.fecha_factura, self.nombre_cliente,
                     self.dni_nie_cliente, self.direccion_cliente, self.email_cliente,
                     self.telefono_cliente, self.subtotal, self.total_iva, self.total_factura,
                     self.modo_pago)
            self.id = db.execute_query(query, params)

        # Guardar items de la factura
        if self.items:
            # Eliminar items existentes
            db.execute_query("DELETE FROM factura_items WHERE factura_id=?", (self.id,))

            # Insertar nuevos items
            for item in self.items:
                item.factura_id = self.id
                item.save()

    def delete(self):
        """Elimina la factura y sus items"""
        if self.id:
            # Eliminar items primero
            db.execute_query("DELETE FROM factura_items WHERE factura_id=?", (self.id,))
            # Eliminar factura
            db.execute_query("DELETE FROM facturas WHERE id=?", (self.id,))

    def add_item(self, producto_id, cantidad, precio_unitario, iva_aplicado, descuento=0):
        """Añade un item a la factura"""
        item = FacturaItem(
            factura_id=self.id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            iva_aplicado=iva_aplicado,
            descuento=descuento
        )
        self.items.append(item)
        return item

    def calculate_totals(self):
        """Calcula los totales de la factura basándose en los items"""
        self.subtotal = 0.0
        self.total_iva = 0.0

        for item in self.items:
            item.calculate_totals()
            self.subtotal += item.subtotal
            self.total_iva += item.iva_amount

        self.total_factura = self.subtotal + self.total_iva

    @staticmethod
    def get_all():
        """Obtiene todas las facturas"""
        query = "SELECT * FROM facturas ORDER BY fecha_factura DESC, numero_factura DESC"
        results = db.execute_query(query)
        facturas = []
        for row in results:
            factura = Factura(
                id=row[0], numero_factura=row[1], fecha_factura=row[2], nombre_cliente=row[3],
                dni_nie_cliente=row[4], direccion_cliente=row[5], email_cliente=row[6],
                telefono_cliente=row[7], subtotal=row[8], total_iva=row[9], total_factura=row[10],
                modo_pago=row[11], fecha_creacion=row[12]
            )
            # Cargar items de la factura
            factura.items = FacturaItem.get_by_factura_id(factura.id)
            facturas.append(factura)
        return facturas

    @staticmethod
    def get_by_id(factura_id):
        """Obtiene una factura por su ID"""
        query = "SELECT * FROM facturas WHERE id=?"
        results = db.execute_query(query, (factura_id,))
        if results:
            row = results[0]
            factura = Factura(
                id=row[0], numero_factura=row[1], fecha_factura=row[2], nombre_cliente=row[3],
                dni_nie_cliente=row[4], direccion_cliente=row[5], email_cliente=row[6],
                telefono_cliente=row[7], subtotal=row[8], total_iva=row[9], total_factura=row[10],
                modo_pago=row[11], fecha_creacion=row[12]
            )
            # Cargar items de la factura
            factura.items = FacturaItem.get_by_factura_id(factura.id)
            return factura
        return None

    @staticmethod
    def get_next_numero():
        """Obtiene el siguiente número de factura"""
        return db.get_next_factura_number()

class FacturaItem:
    def __init__(self, id=None, factura_id=None, producto_id=None, cantidad=1,
                 precio_unitario=0.0, iva_aplicado=21.0, descuento=0.0):
        self.id = id
        self.factura_id = factura_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.iva_aplicado = iva_aplicado
        self.descuento = descuento
        # Campos calculados
        self.subtotal = 0.0
        self.descuento_amount = 0.0
        self.iva_amount = 0.0
        self.total = 0.0
        self.producto = None  # Se carga cuando es necesario

    def save(self):
        """Guarda el item de factura en la base de datos"""
        self.calculate_totals()

        if self.id:
            # Actualizar item existente
            query = '''UPDATE factura_items SET factura_id=?, producto_id=?, cantidad=?,
                      precio_unitario=?, iva_aplicado=?, descuento=?, subtotal=?,
                      descuento_amount=?, iva_amount=?, total=? WHERE id=?'''
            params = (self.factura_id, self.producto_id, self.cantidad, self.precio_unitario,
                     self.iva_aplicado, self.descuento, self.subtotal, self.descuento_amount,
                     self.iva_amount, self.total, self.id)
            db.execute_query(query, params)
        else:
            # Crear nuevo item
            query = '''INSERT INTO factura_items (factura_id, producto_id, cantidad,
                      precio_unitario, iva_aplicado, descuento, subtotal, descuento_amount,
                      iva_amount, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            params = (self.factura_id, self.producto_id, self.cantidad, self.precio_unitario,
                     self.iva_aplicado, self.descuento, self.subtotal, self.descuento_amount,
                     self.iva_amount, self.total)
            self.id = db.execute_query(query, params)

    def calculate_totals(self):
        """Calcula los totales del item"""
        from common.validators import CalculationHelper

        result = CalculationHelper.calculate_line_total(
            self.precio_unitario, self.cantidad, self.iva_aplicado, self.descuento
        )

        self.subtotal = result['subtotal']
        self.descuento_amount = result['descuento_amount']
        self.iva_amount = result['iva_amount']
        self.total = result['total']

    def get_producto(self):
        """Obtiene el producto asociado al item"""
        if not self.producto and self.producto_id:
            self.producto = Producto.get_by_id(self.producto_id)
        return self.producto

    @staticmethod
    def get_by_factura_id(factura_id):
        """Obtiene todos los items de una factura"""
        query = "SELECT * FROM factura_items WHERE factura_id=? ORDER BY id"
        results = db.execute_query(query, (factura_id,))
        items = []
        for row in results:
            item = FacturaItem(
                id=row[0], factura_id=row[1], producto_id=row[2], cantidad=row[3],
                precio_unitario=row[4], iva_aplicado=row[5], descuento=row[6],
            )
            # Cargar valores calculados
            item.subtotal = row[7]
            item.descuento_amount = row[8]
            item.iva_amount = row[9]
            item.total = row[10]
            items.append(item)
        return items

class Organizacion:
    def __init__(self, nombre="", direccion="", telefono="", email="", cif="",
                 logo_path="", directorio_imagenes_defecto="", numero_factura_inicial=1,
                 directorio_descargas_pdf="", visor_pdf_personalizado=""):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.cif = cif
        self.logo_path = logo_path
        self.directorio_imagenes_defecto = directorio_imagenes_defecto
        self.numero_factura_inicial = numero_factura_inicial
        self.directorio_descargas_pdf = directorio_descargas_pdf
        self.visor_pdf_personalizado = visor_pdf_personalizado
    
    def save(self):
        """Guarda los datos de la organización"""
        # Verificar si ya existe una organización
        existing = Organizacion.get()
        if existing and existing.nombre:  # Si existe et n'est pas vide
            query = '''UPDATE organizacion SET nombre=?, direccion=?, telefono=?,
                      email=?, cif=?, logo_path=?, directorio_imagenes_defecto=?,
                      numero_factura_inicial=?, directorio_descargas_pdf=?, visor_pdf_personalizado=?, fecha_actualizacion=CURRENT_TIMESTAMP
                      WHERE id=1'''
        else:
            query = '''INSERT INTO organizacion (id, nombre, direccion, telefono,
                      email, cif, logo_path, directorio_imagenes_defecto, numero_factura_inicial, directorio_descargas_pdf, visor_pdf_personalizado)
                      VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        params = (self.nombre, self.direccion, self.telefono, self.email, self.cif,
                 self.logo_path, self.directorio_imagenes_defecto, self.numero_factura_inicial, self.directorio_descargas_pdf, self.visor_pdf_personalizado)
        db.execute_query(query, params)
    
    @staticmethod
    def get():
        """Obtiene los datos de la organización"""
        query = "SELECT * FROM organizacion WHERE id=1"
        results = db.execute_query(query)
        if results:
            row = results[0]
            # Orden de columnas: id, nombre, direccion, telefono, email, cif, logo_path, fecha_actualizacion, directorio_imagenes_defecto, numero_factura_inicial, directorio_descargas_pdf, visor_pdf_personalizado
            # Manejar compatibilidad con bases de datos existentes
            directorio_imagenes = row[8] if len(row) > 8 and row[8] is not None else ""
            numero_inicial = row[9] if len(row) > 9 and row[9] is not None else 1
            directorio_pdf = row[10] if len(row) > 10 and row[10] is not None else ""
            visor_pdf = row[11] if len(row) > 11 and row[11] is not None else ""

            return Organizacion(
                nombre=row[1], direccion=row[2], telefono=row[3],
                email=row[4], cif=row[5], logo_path=row[6],
                directorio_imagenes_defecto=directorio_imagenes,
                numero_factura_inicial=numero_inicial,
                directorio_descargas_pdf=directorio_pdf,
                visor_pdf_personalizado=visor_pdf
            )
        return Organizacion()

class Stock:
    def __init__(self, producto_id, cantidad_disponible=0):
        self.producto_id = producto_id
        self.cantidad_disponible = cantidad_disponible
    
    def save(self):
        """Actualiza el stock del producto"""
        query = '''UPDATE stock SET cantidad_disponible=?, fecha_actualizacion=CURRENT_TIMESTAMP 
                  WHERE producto_id=?'''
        db.execute_query(query, (self.cantidad_disponible, self.producto_id))
    
    @staticmethod
    def create_for_product(producto_id):
        """Crea una entrada de stock para un nuevo producto"""
        query = "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, 0)"
        db.execute_query(query, (producto_id,))
    
    @staticmethod
    def get_all():
        """Obtiene todo el stock con información de productos"""
        query = '''SELECT s.producto_id, s.cantidad_disponible, p.nombre, p.referencia 
                  FROM stock s 
                  JOIN productos p ON s.producto_id = p.id 
                  ORDER BY p.nombre'''
        return db.execute_query(query)
    
    @staticmethod
    def get_by_product(producto_id):
        """Obtiene el stock de un producto específico"""
        query = "SELECT cantidad_disponible FROM stock WHERE producto_id=?"
        results = db.execute_query(query, (producto_id,))
        return results[0][0] if results else 0
    
    @staticmethod
    def update_stock(producto_id, cantidad_vendida):
        """Actualiza el stock después de una venta"""
        current_stock = Stock.get_by_product(producto_id)
        new_stock = max(0, current_stock - cantidad_vendida)
        query = '''UPDATE stock SET cantidad_disponible=?, fecha_actualizacion=CURRENT_TIMESTAMP
                  WHERE producto_id=?'''
        db.execute_query(query, (new_stock, producto_id))

        # Registrar movimiento en historial
        StockMovement.create(producto_id, -cantidad_vendida, "VENTA", f"Venta de {cantidad_vendida} unidades")

    @staticmethod
    def get_low_stock(threshold=5):
        """Obtiene productos con stock bajo"""
        query = '''SELECT s.producto_id, s.cantidad_disponible, p.nombre, p.referencia
                  FROM stock s
                  JOIN productos p ON s.producto_id = p.id
                  WHERE s.cantidad_disponible <= ?
                  ORDER BY s.cantidad_disponible ASC, p.nombre'''
        return db.execute_query(query, (threshold,))

class StockMovement:
    """Clase para registrar movimientos de stock"""
    def __init__(self, id=None, producto_id=None, cantidad=0, tipo="MANUAL",
                 descripcion="", fecha_movimiento=None):
        self.id = id
        self.producto_id = producto_id
        self.cantidad = cantidad  # Positivo para entrada, negativo para salida
        self.tipo = tipo  # MANUAL, VENTA, AJUSTE, INICIAL
        self.descripcion = descripcion
        self.fecha_movimiento = fecha_movimiento

    def save(self):
        """Guarda el movimiento de stock"""
        query = '''INSERT INTO stock_movements (producto_id, cantidad, tipo, descripcion)
                  VALUES (?, ?, ?, ?)'''
        params = (self.producto_id, self.cantidad, self.tipo, self.descripcion)
        self.id = db.execute_query(query, params)

    @staticmethod
    def create(producto_id, cantidad, tipo, descripcion):
        """Crea un nuevo movimiento de stock"""
        movement = StockMovement(
            producto_id=producto_id,
            cantidad=cantidad,
            tipo=tipo,
            descripcion=descripcion
        )
        movement.save()
        return movement

    @staticmethod
    def get_by_product(producto_id, limit=10):
        """Obtiene los últimos movimientos de un producto"""
        query = '''SELECT id, producto_id, cantidad, tipo, descripcion, fecha_movimiento
                  FROM stock_movements
                  WHERE producto_id=?
                  ORDER BY fecha_movimiento DESC
                  LIMIT ?'''
        results = db.execute_query(query, (producto_id, limit))
        movements = []
        for row in results:
            movement = StockMovement(
                id=row[0], producto_id=row[1], cantidad=row[2],
                tipo=row[3], descripcion=row[4], fecha_movimiento=row[5]
            )
            movements.append(movement)
        return movements
