# -*- coding: utf-8 -*-

TEXTS = {
    # Ventana principal
    "app_title": "Facturación Fácil",
    "productos": "Productos",
    "organizacion": "Organización",
    "stock": "Stock",
    "facturas": "Facturas",
    "nueva_factura": "Nueva Factura",
    "salir": "Salir",
    
    # Productos
    "gestion_productos": "Gestión de Productos",
    "nuevo_producto": "Nuevo Producto",
    "editar_producto": "Editar Producto",
    "eliminar_producto": "Eliminar Producto",
    "nombre": "Nombre",
    "referencia": "Referencia",
    "precio": "Precio",
    "cantidad": "Cantidad",
    "categoria": "Categoría",
    "descripcion": "Descripción",
    "imagen": "Imagen",
    "iva_recomendado": "IVA Recomendado (%)",
    "guardar": "Guardar",
    "cancelar": "Cancelar",
    "seleccionar_imagen": "Seleccionar Imagen",
    "quitar_imagen": "Quitar Imagen",
    "configurar_directorio": "Configurar Directorio",
    
    # Organización
    "datos_organizacion": "Datos de la Organización",
    "nombre_empresa": "Nombre de la Empresa",
    "direccion": "Dirección",
    "telefono": "Teléfono",
    "email": "Email",
    "cif": "CIF",
    "logo": "Logo",
    "seleccionar_logo": "Seleccionar Logo",
    
    # Stock
    "gestion_stock": "Gestión de Stock",
    "cantidad_disponible": "Cantidad Disponible",
    "actualizar_stock": "Actualizar Stock",
    "nueva_cantidad": "Nueva Cantidad",
    
    # Facturas
    "crear_factura": "Crear Factura",
    "datos_cliente": "Datos del Cliente",
    "nombre_cliente": "Nombre del Cliente",
    "dni_nie": "DNI/NIE",
    "direccion_cliente": "Dirección del Cliente",
    "email_cliente": "Email del Cliente",
    "telefono_cliente": "Teléfono del Cliente",
    "fecha_factura": "Fecha de Factura",
    "numero_factura": "Número de Factura",
    "productos_factura": "Productos de la Factura",
    "agregar_producto": "Agregar Producto",
    "precio_unitario": "Precio Unitario",
    "precio_total": "Precio Total",
    "iva_aplicado": "IVA Aplicado (%)",
    "subtotal": "Subtotal",
    "total_iva": "Total IVA",
    "total_factura": "Total Factura",
    "modo_pago": "Modo de Pago",
    "generar_factura": "Generar Factura",
    "efectivo": "Efectivo",
    "tarjeta": "Tarjeta",
    "transferencia": "Transferencia",
    "editar": "Editar",
    "eliminar": "Eliminar",
    "nuevo": "Nuevo",
    "exito": "Éxito",
    "advertencia": "Advertencia",
    "confirmacion": "Confirmación",
    "configuracion_guardada": "Configuración guardada correctamente",
    
    # Mensajes
    "producto_guardado": "Producto guardado correctamente",
    "producto_eliminado": "Producto eliminado correctamente",
    "organizacion_guardada": "Datos de organización guardados",
    "stock_actualizado": "Stock actualizado correctamente",
    "factura_generada": "Factura generada correctamente",
    "error": "Error",
    "confirmar": "Confirmar",
    "confirmar_eliminacion": "¿Está seguro de que desea eliminar este producto?",
    "campo_requerido": "Este campo es requerido",
    "precio_invalido": "El precio debe ser un número válido",
    "cantidad_invalida": "La cantidad debe ser un número entero válido",
    "iva_invalido": "El IVA debe ser un número válido entre 0 y 100",
    
    # Botones
    "si": "Sí",
    "no": "No",
    "aceptar": "Aceptar",
    "buscar": "Buscar",
    "limpiar": "Limpiar",
    "imprimir": "Imprimir",
    "exportar_pdf": "Exportar PDF"
}

def get_text(key):
    """Obtiene el texto traducido para una clave dada"""
    return TEXTS.get(key, key)
