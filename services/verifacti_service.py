#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servicio de integración con Verifacti API para cumplimiento Verifactu.

Módulo pythonic que proporciona funciones para enviar facturas a Verifacti,
gestionar estados y manejar reintentos.
"""

import json
import logging
import base64
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from enum import Enum

import requests

# Configuración de logging
logger = logging.getLogger(__name__)

# Constantes
API_BASE_URL = "https://api.verifacti.com"
VERIFACTI_DIR = Path("verifacti")
ENVIADAS_DIR = VERIFACTI_DIR / "enviadas"
PENDIENTES_DIR = VERIFACTI_DIR / "pendientes"
ERRORES_DIR = VERIFACTI_DIR / "errores"

DEFAULT_TIMEOUT = 30


class EstadoVerifacti(Enum):
    """Estados posibles de una factura en Verifacti."""
    PENDIENTE = "Pendiente"
    ENVIADO = "Enviado"
    ERROR = "Error"
    NO_ENVIADO = "No enviado"


@dataclass
class ConfigVerifacti:
    """Configuración de Verifacti almacenada en config.json."""
    nif: str = ""
    nombre_empresa: str = ""
    api_key: str = ""
    serie_factura: str = "A"
    habilitado: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nif": self.nif,
            "nombre_empresa": self.nombre_empresa,
            "api_key": self.api_key,
            "serie_factura": self.serie_factura,
            "habilitado": self.habilitado
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfigVerifacti":
        return cls(
            nif=data.get("nif", ""),
            nombre_empresa=data.get("nombre_empresa", ""),
            api_key=data.get("api_key", ""),
            serie_factura=data.get("serie_factura", "A"),
            habilitado=data.get("habilitado", False)
        )


@dataclass
class RespuestaVerifacti:
    """Respuesta de la API de Verifacti."""
    uuid: str
    estado: str
    url: str
    qr: str  # base64
    huella: str
    exito: bool = True
    mensaje_error: str = ""


def inicializar_directorios() -> None:
    """Crea la estructura de directorios de Verifacti si no existe."""
    try:
        VERIFACTI_DIR.mkdir(parents=True, exist_ok=True)
        ENVIADAS_DIR.mkdir(exist_ok=True)
        PENDIENTES_DIR.mkdir(exist_ok=True)
        ERRORES_DIR.mkdir(exist_ok=True)
        logger.info("Directorios Verifacti inicializados correctamente")
    except OSError as e:
        logger.error(f"Error creando directorios Verifacti: {e}")
        raise


def cargar_configuracion(config_path: Path = Path("config/config.json")) -> ConfigVerifacti:
    """Carga la configuración de Verifacti desde config.json."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        verifacti_data = config.get("verifacti", {})
        return ConfigVerifacti.from_dict(verifacti_data)
    except FileNotFoundError:
        logger.warning(f"Archivo de configuración no encontrado: {config_path}")
        return ConfigVerifacti()
    except json.JSONDecodeError as e:
        logger.error(f"Error decodificando JSON: {e}")
        return ConfigVerifacti()


def guardar_configuracion(
    config: ConfigVerifacti,
    config_path: Path = Path("config/config.json")
) -> bool:
    """Guarda la configuración de Verifacti en config.json."""
    try:
        with open(config_path, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            data["verifacti"] = config.to_dict()
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()
        logger.info("Configuración Verifacti guardada")
        return True
    except OSError as e:
        logger.error(f"Error guardando configuración: {e}")
        return False


def construir_payload_factura(
    factura: Dict[str, Any],
    cliente: Dict[str, Any],
    lineas: List[Dict[str, Any]],
    config: ConfigVerifacti
) -> Dict[str, Any]:
    """Construye el payload JSON para enviar una factura a Verifacti."""
    
    # Construir líneas de factura (agrupadas por IVA)
    lineas_payload = []
    for linea in lineas:
        linea_data = {
            "base_imponible": str(linea.get("base", 0)),
            "tipo_impositivo": str(linea.get("iva", 21)),
            "cuota_repercutida": str(linea.get("cuota_iva", 0))
        }
        lineas_payload.append(linea_data)
    
    # Determinar si es cliente extranjero (intracomunitario)
    nif_cliente = cliente.get("dni_nie", "")
    es_extranjero = False
    id_otro = None
    
    if nif_cliente and len(nif_cliente) > 2:
        prefijo = nif_cliente[:2].upper()
        if prefijo in ["FR", "DE", "IT", "PT", "BE", "NL", "AT"]:
            es_extranjero = True
            id_otro = {
                "codigo_pais": prefijo,
                "id_type": "02",
                "id": nif_cliente
            }
    
    payload = {
        "serie": config.serie_factura,
        "numero": str(factura.get("numero_factura", "")),
        "fecha_expedicion": formatear_fecha(factura.get("fecha_factura", "")),
        "tipo_factura": "F1",
        "descripcion": "Factura de venta",
        "lineas": lineas_payload,
        "importe_total": str(factura.get("total_factura", 0))
    }
    
    # Añadir cliente
    if es_extranjero and id_otro:
        payload["id_otro"] = id_otro
        payload["nombre"] = cliente.get("nombre", "Cliente extranjero")
        # Para operaciones intracomunitarias
        if lineas and lineas[0].get("iva", 0) == 0:
            payload["lineas"][0]["operacion_exenta"] = "E5"
    else:
        payload["nif"] = nif_cliente or "00000000T"
        payload["nombre"] = cliente.get("nombre", "Cliente")
    
    return payload


def formatear_fecha(fecha_str: str) -> str:
    """Formatea fecha de YYYY-MM-DD a DD-MM-YYYY."""
    if not fecha_str:
        return datetime.now().strftime("%d-%m-%Y")
    
    try:
        # Intentar parsear formato ISO
        if "-" in fecha_str and len(fecha_str.split("-")[0]) == 4:
            dt = datetime.strptime(fecha_str[:10], "%Y-%m-%d")
            return dt.strftime("%d-%m-%Y")
        return fecha_str
    except ValueError:
        return datetime.now().strftime("%d-%m-%Y")


def enviar_factura_api(
    payload: Dict[str, Any],
    api_key: str,
    timeout: int = DEFAULT_TIMEOUT
) -> RespuestaVerifacti:
    """Envía una factura a la API de Verifacti."""
    
    url = f"{API_BASE_URL}/verifactu/create"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
        
        return RespuestaVerifacti(
            uuid=data.get("uuid", ""),
            estado=data.get("estado", ""),
            url=data.get("url", ""),
            qr=data.get("qr", ""),
            huella=data.get("huella", ""),
            exito=True
        )
        
    except requests.exceptions.ConnectionError:
        logger.warning("Sin conexión a internet para enviar factura")
        return RespuestaVerifacti(
            uuid="", estado="", url="", qr="", huella="",
            exito=False, mensaje_error="Sin conexión a internet"
        )
    except requests.exceptions.Timeout:
        logger.warning("Timeout enviando factura a Verifacti")
        return RespuestaVerifacti(
            uuid="", estado="", url="", qr="", huella="",
            exito=False, mensaje_error="Timeout de conexión"
        )
    except requests.exceptions.HTTPError as e:
        error_msg = f"Error HTTP {e.response.status_code}"
        try:
            error_data = e.response.json()
            if "error" in error_data:
                error_msg = error_data["error"]
        except:
            pass
        logger.error(f"Error API Verifacti: {error_msg}")
        return RespuestaVerifacti(
            uuid="", estado="", url="", qr="", huella="",
            exito=False, mensaje_error=error_msg
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {e}")
        return RespuestaVerifacti(
            uuid="", estado="", url="", qr="", huella="",
            exito=False, mensaje_error=str(e)
        )


def guardar_factura_local(
    factura_data: Dict[str, Any],
    respuesta: RespuestaVerifacti,
    directorio: Path
) -> Path:
    """Guarda los datos de la factura en un archivo JSON local."""
    
    numero = factura_data.get("numero", "sin_numero")
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"factura_{numero}_{fecha}.json"
    filepath = directorio / filename
    
    data = {
        "factura": factura_data,
        "respuesta_verifacti": {
            "uuid": respuesta.uuid,
            "estado": respuesta.estado,
            "url": respuesta.url,
            "huella": respuesta.huella,
            "exito": respuesta.exito,
            "mensaje_error": respuesta.mensaje_error
        },
        "fecha_envio": datetime.now().isoformat()
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Factura guardada en: {filepath}")
        return filepath
    except OSError as e:
        logger.error(f"Error guardando factura local: {e}")
        raise


def guardar_log_error(
    factura_data: Dict[str, Any],
    error_msg: str,
    directorio: Path
) -> Path:
    """Guarda un log de error cuando falla el envío."""
    
    numero = factura_data.get("numero", "sin_numero")
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"factura_{numero}_{fecha}.log"
    filepath = directorio / filename
    
    log_data = {
        "factura": factura_data,
        "error": error_msg,
        "fecha_error": datetime.now().isoformat()
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Log de error guardado en: {filepath}")
        return filepath
    except OSError as e:
        logger.error(f"Error guardando log: {e}")
        raise


def obtener_qr_como_imagen(qr_base64: str) -> Optional[bytes]:
    """Decodifica el QR de base64 a bytes de imagen."""
    try:
        return base64.b64decode(qr_base64)
    except Exception as e:
        logger.error(f"Error decodificando QR: {e}")
        return None


def consultar_estado_factura(
    uuid: str,
    api_key: str
) -> Optional[Dict[str, Any]]:
    """Consulta el estado de una factura en Verifacti."""
    
    url = f"{API_BASE_URL}/verifactu/status"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(
            url,
            headers=headers,
            params={"uuid": uuid},
            timeout=DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error consultando estado: {e}")
        return None


def listar_facturas_pendientes() -> List[Path]:
    """Lista todas las facturas pendientes de envío."""
    try:
        return sorted(PENDIENTES_DIR.glob("factura_*.json"))
    except OSError:
        return []


def verificar_conectividad(api_key: str) -> bool:
    """Verifica si hay conexión con la API de Verifacti."""
    try:
        url = f"{API_BASE_URL}/verifactu/health"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False
