#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handler para el envío de facturas a Verifacti desde el detalle de factura.

Proporciona funciones para enviar facturas individuales y gestionar
el estado de envío (enviado, pendiente, error).
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtCore import Qt

from services.verifacti_service import (
    construir_payload_factura, enviar_factura_api,
    guardar_factura_local, guardar_log_error,
    cargar_configuracion, EstadoVerifacti,
    ENVIADAS_DIR, PENDIENTES_DIR, ERRORES_DIR,
    listar_facturas_pendientes, verificar_conectividad,
    consultar_estado_factura, inicializar_directorios
)
from database.models import Factura, Cliente

logger = logging.getLogger(__name__)


def obtener_datos_factura_completa(factura_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene todos los datos de una factura incluyendo cliente y líneas."""
    try:
        factura = Factura.get_by_id(factura_id)
        if not factura:
            return None
        
        # Obtener cliente
        cliente = None
        if factura.cliente_id:
            cliente = Cliente.get_by_id(factura.cliente_id)
        
        # Construir datos completos
        datos = {
            "id": factura.id,
            "numero": factura.numero_factura,
            "fecha": factura.fecha_factura,
            "total": factura.total_factura,
            "subtotal": factura.subtotal,
            "iva_total": factura.total_iva,
            "cliente": {
                "id": factura.cliente_id,
                "nombre": factura.nombre_cliente or (cliente.nombre if cliente else ""),
                "dni_nie": factura.dni_nie_cliente or (cliente.dni_nie if cliente else ""),
                "direccion": factura.direccion_cliente or "",
                "email": factura.email_cliente or "",
                "telefono": factura.telefono_cliente or ""
            },
            "lineas": []
        }
        
        # Añadir líneas
        for item in factura.items:
            producto = item.get_producto()
            linea = {
                "producto_id": item.producto_id,
                "descripcion": producto.nombre if producto else "Producto",
                "cantidad": item.cantidad,
                "precio": item.precio_unitario,
                "base": item.subtotal,
                "iva": item.iva_aplicado,
                "cuota_iva": item.iva_amount,
                "total": item.total
            }
            datos["lineas"].append(linea)
        
        return datos
        
    except Exception as e:
        logger.error(f"Error obteniendo datos de factura {factura_id}: {e}")
        return None


def enviar_factura_verifacti(
    factura_id: int,
    parent: Optional[Any] = None,
    mostrar_mensajes: bool = True
) -> tuple[bool, str]:
    """
    Envía una factura a Verifacti.
    
    Args:
        factura_id: ID de la factura a enviar
        parent: Widget padre para mensajes
        mostrar_mensajes: Si debe mostrar mensajes al usuario
        
    Returns:
        Tuple (éxito, mensaje)
    """
    # Verificar configuración
    config = cargar_configuracion()
    if not config.habilitado or not config.api_key:
        msg = "Verifacti no está configurado"
        if mostrar_mensajes:
            QMessageBox.warning(parent, "Configuración incompleta", msg)
        return False, msg
    
    # Asegurar que existen directorios
    try:
        inicializar_directorios()
    except Exception as e:
        logger.error(f"Error inicializando directorios: {e}")
    
    # Obtener datos de la factura
    datos_factura = obtener_datos_factura_completa(factura_id)
    if not datos_factura:
        msg = "No se pudieron obtener los datos de la factura"
        if mostrar_mensajes:
            QMessageBox.critical(parent, "Error", msg)
        return False, msg
    
    # Construir payload
    payload = construir_payload_factura(
        datos_factura,
        datos_factura["cliente"],
        datos_factura["lineas"],
        config
    )
    
    # Enviar a API
    respuesta = enviar_factura_api(payload, config.api_key)
    
    if respuesta.exito:
        # Éxito: guardar en enviadas
        try:
            guardar_factura_local(payload, respuesta, ENVIADAS_DIR)
            actualizar_estado_factura_db(factura_id, EstadoVerifacti.ENVIADO)
            
            msg = (
                f"Factura enviada correctamente a Verifacti.\n\n"
                f"UUID: {respuesta.uuid}\n"
                f"Estado: {respuesta.estado}"
            )
            if mostrar_mensajes:
                QMessageBox.information(parent, "Éxito", msg)
            return True, respuesta.uuid
            
        except Exception as e:
            logger.error(f"Error guardando factura enviada: {e}")
            # Aunque falló el guardado local, el envío fue exitoso
            return True, respuesta.uuid
    
    elif "Sin conexión" in respuesta.mensaje_error or "Timeout" in respuesta.mensaje_error:
        # Sin internet: guardar en pendientes
        try:
            guardar_factura_local(
                payload,
                respuesta,
                PENDIENTES_DIR
            )
            actualizar_estado_factura_db(factura_id, EstadoVerifacti.PENDIENTE)
            
            msg = (
                "No hay conexión a internet. La factura se ha guardado "
                "en 'verifacti/pendientes' para enviarla más tarde."
            )
            if mostrar_mensajes:
                QMessageBox.warning(parent, "Sin conexión", msg)
            return False, "pendiente"
            
        except Exception as e:
            logger.error(f"Error guardando factura pendiente: {e}")
            return False, str(e)
    
    else:
        # Error de API: guardar en errores
        try:
            guardar_factura_local(payload, respuesta, ERRORES_DIR)
            guardar_log_error(payload, respuesta.mensaje_error, ERRORES_DIR)
            actualizar_estado_factura_db(factura_id, EstadoVerifacti.ERROR)
            
            msg = (
                f"Error enviando factura a Verifacti:\n\n"
                f"{respuesta.mensaje_error}\n\n"
                f"La factura y el log de error se han guardado en 'verifacti/errores'."
            )
            if mostrar_mensajes:
                QMessageBox.critical(parent, "Error de envío", msg)
            return False, respuesta.mensaje_error
            
        except Exception as e:
            logger.error(f"Error guardando factura con error: {e}")
            return False, str(e)


def reenviar_facturas_pendientes(parent: Optional[Any] = None) -> tuple[int, int]:
    """
    Reenvía todas las facturas pendientes.
    
    Args:
        parent: Widget padre para mensajes
        
    Returns:
        Tuple (enviadas correctamente, fallidas)
    """
    config = cargar_configuracion()
    if not config.habilitado:
        QMessageBox.warning(
            parent,
            "No configurado",
            "Verifacti no está configurado."
        )
        return 0, 0
    
    # Verificar conectividad primero
    if not verificar_conectividad(config.api_key):
        QMessageBox.warning(
            parent,
            "Sin conexión",
            "No hay conexión con Verifacti. No se pueden enviar las facturas pendientes."
        )
        return 0, 0
    
    pendientes = listar_facturas_pendientes()
    if not pendientes:
        QMessageBox.information(
            parent,
            "Sin pendientes",
            "No hay facturas pendientes de envío."
        )
        return 0, 0
    
    exitos = 0
    fallidos = 0
    
    for archivo in pendientes:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            payload = data.get("factura", {})
            
            # Enviar
            respuesta = enviar_factura_api(payload, config.api_key)
            
            if respuesta.exito:
                # Mover a enviadas
                guardar_factura_local(payload, respuesta, ENVIADAS_DIR)
                archivo.unlink()  # Borrar de pendientes
                exitos += 1
            else:
                fallidos += 1
                
        except Exception as e:
            logger.error(f"Error reenviando factura {archivo}: {e}")
            fallidos += 1
    
    # Mostrar resumen
    QMessageBox.information(
        parent,
        "Resumen de envío",
        f"Facturas procesadas:\n"
        f"• Enviadas correctamente: {exitos}\n"
        f"• Fallidas: {fallidos}"
    )
    
    return exitos, fallidos


def actualizar_estado_factura_db(factura_id: int, estado: EstadoVerifacti) -> None:
    """
    Actualiza el estado Verifacti de una factura en la base de datos.
    
    Nota: Esta función requiere que exista el campo 'estado_verifacti' 
    en la tabla facturas. Si no existe, solo se loguea.
    """
    try:
        from database.database import db
        
        # Intentar actualizar
        query = """
            UPDATE facturas 
            SET estado_verifacti = ?, fecha_envio_verifacti = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        db.execute_query(query, (estado.value, factura_id))
        logger.info(f"Estado Verifacti actualizado para factura {factura_id}: {estado.value}")
        
    except Exception as e:
        # Probablemente no existe el campo, solo loguear
        logger.debug(f"No se pudo actualizar estado en BD (campo puede no existir): {e}")


def crear_boton_enviar_verifacti(parent: Any, factura_id: int) -> QPushButton:
    """
    Crea un botón para enviar una factura a Verifacti.
    
    Args:
        parent: Widget padre (diálogo de detalle)
        factura_id: ID de la factura
        
    Returns:
        Botón configurado
    """
    btn = QPushButton("📤 Enviar a Verifacti")
    btn.setToolTip("Enviar factura a Verifacti (AEAT)")
    
    def on_click():
        exito, msg = enviar_factura_verifacti(factura_id, parent)
        if exito:
            btn.setEnabled(False)
            btn.setText("✓ Enviado a Verifacti")
    
    btn.clicked.connect(on_click)
    return btn


def crear_boton_enviar_pendientes(parent: Any) -> QPushButton:
    """Crea un botón para enviar facturas pendientes."""
    btn = QPushButton("🔄 Enviar pendientes Verifacti")
    btn.setToolTip("Reenviar facturas pendientes a Verifacti")
    btn.clicked.connect(lambda: reenviar_facturas_pendientes(parent))
    return btn


def obtener_estado_factura(factura_id: int) -> EstadoVerifacti:
    """Obtiene el estado Verifacti de una factura."""
    try:
        from database.database import db
        query = "SELECT estado_verifacti FROM facturas WHERE id = ?"
        result = db.execute_query(query, (factura_id,))
        if result and result[0][0]:
            return EstadoVerifacti(result[0][0])
    except:
        pass
    return EstadoVerifacti.NO_ENVIADO
