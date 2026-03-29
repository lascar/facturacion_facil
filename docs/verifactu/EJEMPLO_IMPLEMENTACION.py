#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo de implementación del servicio Verifactu
Este código es una propuesta conceptual para discusión.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import hashlib
import json
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EstadoVerifactu(Enum):
    """Estados posibles de un registro Verifactu"""
    PENDIENTE = "PENDIENTE"
    ENVIADO = "ENVIADO"
    ACEPTADO = "ACEPTADO"
    RECHAZADO = "RECHAZADO"
    ERROR = "ERROR"


class ModoVerifactu(Enum):
    """Modalidades de operación Verifactu"""
    VERIFACTU = "VERIFACTU"  # Envío automático a AEAT
    NO_VERIFACTU = "NO_VERIFACTU"  # Sistema homologado sin envío automático


@dataclass
class RegistroVerifactu:
    """Modelo de datos para registro Verifactu"""
    factura_id: int
    numero_factura: str
    fecha_factura: str
    nif_emisor: str
    nif_receptor: str
    importe_total: float
    hash_registro: str
    estado: EstadoVerifactu = EstadoVerifactu.PENDIENTE
    id_envio_aeat: Optional[str] = None
    fecha_envio: Optional[datetime] = None
    respuesta_aeat: Optional[Dict[str, Any]] = None
    codigo_qr: Optional[str] = None
    firma_electronica: Optional[str] = None
    timestamp_creacion: datetime = field(default_factory=datetime.now)


@dataclass
class ConfigVerifactu:
    """Configuración del sistema Verifactu"""
    modo_operacion: ModoVerifactu = ModoVerifactu.NO_VERIFACTU
    entorno: str = "PRUEBAS"  # PRUEBAS o PRODUCCION
    certificado_path: Optional[Path] = None
    certificado_password: Optional[str] = None
    nif_emisor: str = ""
    nombre_emisor: str = ""
    url_api_aeat: str = "https://prewww2.aeat.es/wlpl/SSII-FACT/ws/"
    
    def __post_init__(self):
        if self.entorno == "PRODUCCION":
            self.url_api_aeat = "https://www2.agenciatributaria.gob.es/wlpl/SSII-FACT/ws/"


class IntegrityService:
    """
    Servicio para garantizar integridad e inalterabilidad de facturas.
    Implementa la modalidad NO_VERIFACTU.
    """
    
    def __init__(self, db_path: Path = Path("base_de_datos/facturacion.db")):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
    
    def calcular_hash_factura(self, factura_data: Dict[str, Any]) -> str:
        """
        Calcula el hash SHA-256 de una factura.
        
        Args:
            factura_data: Diccionario con los datos de la factura
            
        Returns:
            Hash SHA-256 en formato hexadecimal
        """
        # Normalizar datos (ordenar claves para consistencia)
        datos_normalizados = json.dumps(factura_data, sort_keys=True, ensure_ascii=False)
        
        # Calcular hash
        hash_obj = hashlib.sha256(datos_normalizados.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        
        self.logger.info(f"Hash calculado para factura: {hash_hex[:16]}...")
        return hash_hex
    
    def verificar_integridad(self, factura_id: int) -> bool:
        """
        Verifica que una factura no ha sido alterada.
        
        Args:
            factura_id: ID de la factura a verificar
            
        Returns:
            True si la integridad es válida, False en caso contrario
        """
        # Aquí iría la lógica para:
        # 1. Recuperar la factura de la base de datos
        # 2. Recalcular el hash
        # 3. Comparar con el hash almacenado
        
        self.logger.info(f"Verificando integridad de factura {factura_id}")
        # Implementación pendiente...
        return True
    
    def exportar_registros_json(self, fecha_inicio: datetime, fecha_fin: datetime) -> str:
        """
        Exporta registros en formato JSON para AEAT.
        
        Args:
            fecha_inicio: Fecha inicial del rango
            fecha_fin: Fecha final del rango
            
        Returns:
            Ruta del archivo exportado
        """
        # Aquí iría la lógica para exportar registros
        
        filename = f"registros_verifactu_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.json"
        output_path = Path("exports") / filename
        
        self.logger.info(f"Exportando registros a: {output_path}")
        # Implementación pendiente...
        
        return str(output_path)


class VerifactuService:
    """
    Servicio principal para la integración con Verifactu AEAT.
    Implementa la modalidad VERIFACTU (envío automático).
    """
    
    def __init__(self, config: ConfigVerifactu):
        self.config = config
        self.integrity_service = IntegrityService()
        self.logger = logging.getLogger(__name__)
    
    def registrar_factura(self, factura_data: Dict[str, Any]) -> RegistroVerifactu:
        """
        Registra una factura en el sistema Verifactu.
        
        Args:
            factura_data: Datos completos de la factura
            
        Returns:
            RegistroVerifactu creado
        """
        # Calcular hash de integridad
        hash_registro = self.integrity_service.calcular_hash_factura(factura_data)
        
        # Crear registro
        registro = RegistroVerifactu(
            factura_id=factura_data['id'],
            numero_factura=factura_data['numero_factura'],
            fecha_factura=factura_data['fecha_factura'],
            nif_emisor=self.config.nif_emisor,
            nif_receptor=factura_data.get('dni_nie_cliente', ''),
            importe_total=factura_data.get('total_factura', 0.0),
            hash_registro=hash_registro,
            estado=EstadoVerifactu.PENDIENTE
        )
        
        self.logger.info(f"Factura {registro.numero_factura} registrada en Verifactu (hash: {hash_registro[:16]}...)")
        
        # Si es modo VERIFACTU, enviar inmediatamente
        if self.config.modo_operacion == ModoVerifactu.VERIFACTU:
            self._enviar_a_aeat(registro)
        
        return registro
    
    def _enviar_a_aeat(self, registro: RegistroVerifactu) -> bool:
        """
        Envía un registro a la AEAT (simulado).
        
        En implementación real, esto usaría:
        - zeep para SOAP
        - requests para REST
        - Certificado digital para autenticación
        """
        self.logger.info(f"Enviando factura {registro.numero_factura} a AEAT...")
        
        # Simular envío (en producción, llamar API real)
        try:
            # Aquí iría la llamada real a la API de AEAT
            # response = requests.post(
            #     self.config.url_api_aeat,
            #     data=self._construir_xml_envio(registro),
            #     cert=self.config.certificado_path
            # )
            
            # Simular respuesta exitosa
            registro.estado = EstadoVerifactu.ACEPTADO
            registro.id_envio_aeat = f"AEAT_{datetime.now().strftime('%Y%m%d%H%M%S')}_{registro.factura_id}"
            registro.fecha_envio = datetime.now()
            registro.respuesta_aeat = {"codigo": "0", "descripcion": "Aceptada"}
            
            # Generar código QR
            registro.codigo_qr = self._generar_codigo_qr(registro)
            
            self.logger.info(f"Factura {registro.numero_factura} enviada correctamente (ID: {registro.id_envio_aeat})")
            return True
            
        except Exception as e:
            registro.estado = EstadoVerifactu.ERROR
            self.logger.error(f"Error enviando factura: {e}")
            return False
    
    def _generar_codigo_qr(self, registro: RegistroVerifactu) -> str:
        """
        Genera el código QR verificable para una factura.
        
        El código QR debe contener:
        - URL de verificación AEAT
        - ID del registro
        - Hash de integridad
        """
        import qrcode
        import base64
        from io import BytesIO
        
        # Construir datos del QR
        qr_data = {
            "verifactu": "1.0",
            "id_registro": registro.id_envio_aeat,
            "nif_emisor": registro.nif_emisor,
            "numero_factura": registro.numero_factura,
            "fecha": registro.fecha_factura,
            "importe": registro.importe_total,
            "hash": registro.hash_registro[:16]  # Primeros 16 caracteres
        }
        
        # Generar QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        # Convertir a base64 para almacenar/insertar en PDF
        buffer = BytesIO()
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(buffer, format='PNG')
        
        return base64.b64encode(buffer.getvalue()).decode()
    
    def consultar_estado(self, id_envio: str) -> Optional[EstadoVerifactu]:
        """
        Consulta el estado de un envío en la AEAT.
        
        Args:
            id_envio: ID del envío a consultar
            
        Returns:
            Estado actual del envío
        """
        self.logger.info(f"Consultando estado de envío: {id_envio}")
        # Implementación pendiente...
        return EstadoVerifactu.ACEPTADO
    
    def obtener_url_verificacion(self, registro: RegistroVerifactu) -> str:
        """
        Genera la URL de verificación pública de una factura.
        """
        base_url = "https://www.agenciatributaria.gob.es/verifactu/verificar"
        return f"{base_url}?id={registro.id_envio_aeat}&hash={registro.hash_registro[:16]}"


def ejemplo_uso():
    """Ejemplo de uso del servicio Verifactu"""
    
    # Configuración
    config = ConfigVerifactu(
        modo_operacion=ModoVerifactu.NO_VERIFACTU,  # Empezar sin envío automático
        entorno="PRUEBAS",
        nif_emisor="B12345678",
        nombre_emisor="Mi Empresa SL"
    )
    
    # Crear servicio
    verifactu = VerifactuService(config)
    
    # Datos de ejemplo de una factura
    factura_ejemplo = {
        'id': 1,
        'numero_factura': 'FAC-2024-0001',
        'fecha_factura': '2024-01-15',
        'dni_nie_cliente': '12345678A',
        'nombre_cliente': 'Cliente Ejemplo',
        'total_factura': 121.00,
        'lineas': [
            {'producto': 'Producto A', 'cantidad': 2, 'precio': 50.00, 'iva': 21},
        ]
    }
    
    # Registrar factura
    registro = verifactu.registrar_factura(factura_ejemplo)
    
    print(f"\n=== Registro Verifactu Creado ===")
    print(f"Factura: {registro.numero_factura}")
    print(f"Hash: {registro.hash_registro}")
    print(f"Estado: {registro.estado.value}")
    print(f"URL Verificación: {verifactu.obtener_url_verificacion(registro)}")


if __name__ == "__main__":
    ejemplo_uso()
