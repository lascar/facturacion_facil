# -*- coding: utf-8 -*-
"""
Servicio para manejar la numeración de facturas
"""

import re
from database.database import Database
from utils.config import app_config
from utils.logger import get_logger

logger = get_logger(__name__)

class FacturaNumberingService:
    """Servicio para generar y gestionar números de factura"""
    
    def __init__(self):
        self.db = Database()
        self.config = app_config
    
    def get_next_numero_factura(self):
        """
        Obtiene el siguiente número de factura sugerido
        Nuevo formato: número-año (ej: FAC-001-2025)
        """
        try:
            # Obtener el último número de factura de la base de datos
            ultimo_numero = self._get_ultimo_numero_factura()

            if ultimo_numero is not None:
                # Si hay facturas existentes, incrementar desde el último número
                siguiente_numero = ultimo_numero + 1
            else:
                # Si no hay facturas, usar el número inicial configurado
                siguiente_numero = self.config.get_factura_numero_inicial()

            # Formatear el número con prefijo y año al final
            numero_formateado = self._format_numero_factura(siguiente_numero)

            logger.info(f"Siguiente número de factura sugerido: {numero_formateado}")
            return numero_formateado

        except Exception as e:
            logger.error(f"Error obteniendo siguiente número de factura: {e}")
            # Fallback al formato básico
            from datetime import datetime
            year = datetime.now().year
            numero_inicial = self.config.get_factura_numero_inicial()
            prefijo = self.config.get_factura_prefijo()
            if prefijo:
                return f"{prefijo}-{numero_inicial:03d}-{year}"
            else:
                return f"{numero_inicial:03d}-{year}"
    
    def _get_ultimo_numero_factura(self):
        """
        Obtiene el último número de factura usado (solo la parte numérica)
        """
        try:
            # Obtener todas las facturas ordenadas por número de factura descendente
            query = "SELECT numero_factura FROM facturas ORDER BY id DESC LIMIT 50"
            facturas = self.db.execute_query(query)
            
            if not facturas:
                return None
            
            # Extraer números de todas las facturas y encontrar el máximo
            numeros = []
            for factura in facturas:
                numero_str = factura[0]  # numero_factura
                numero_numerico = self._extract_numero_from_string(numero_str)
                if numero_numerico is not None:
                    numeros.append(numero_numerico)
            
            if numeros:
                return max(numeros)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error obteniendo último número de factura: {e}")
            return None
    
    def _extract_numero_from_string(self, numero_str):
        """
        Extrae la parte numérica de un número de factura
        Nuevo formato: prefijo-número-año (ej: FAC-001-2025)
        """
        try:
            if not numero_str:
                return None

            import re
            from datetime import datetime
            current_year = datetime.now().year

            # Buscar patrón específico: algo-número-año
            match = re.search(r'-(\d+)-(\d{4})$', str(numero_str))
            if match:
                numero_secuencial = int(match.group(1))
                año = int(match.group(2))
                # Si el año coincide con el actual, devolver el número secuencial
                if año == current_year:
                    return numero_secuencial

            # Fallback: buscar todos los números y excluir años
            numeros = re.findall(r'\d+', str(numero_str))
            if numeros:
                numeros_int = [int(n) for n in numeros]
                # Excluir años (números de 4 dígitos >= 2000)
                numeros_no_año = [n for n in numeros_int if not (n >= 2000 and n <= 3000)]

                if numeros_no_año:
                    return max(numeros_no_año)

            return None

        except Exception as e:
            logger.debug(f"Error extrayendo número de '{numero_str}': {e}")
            return None
    
    def _format_numero_factura(self, numero):
        """
        Formatea un número de factura con prefijo, número y año al final
        Nuevo formato: prefijo-número-año (ej: FAC-001-2025)
        """
        try:
            from datetime import datetime

            prefijo = self.config.get_factura_prefijo()
            year = datetime.now().year

            # Formatear el número con ceros a la izquierda si es necesario
            numero_str = str(numero).zfill(3)  # Mínimo 3 dígitos para el nuevo formato

            # Construir el número completo con año al final
            if prefijo:
                numero_completo = f"{prefijo}-{numero_str}-{year}"
            else:
                numero_completo = f"{numero_str}-{year}"

            return numero_completo

        except Exception as e:
            logger.error(f"Error formateando número de factura: {e}")
            return f"{numero}-{datetime.now().year}"
    
    def validate_numero_factura(self, numero_factura):
        """
        Valida si un número de factura es válido y no está duplicado
        """
        try:
            if not numero_factura or not str(numero_factura).strip():
                return False, "El número de factura no puede estar vacío"
            
            numero_factura = str(numero_factura).strip()
            
            # Verificar si ya existe en la base de datos
            if self._numero_factura_exists(numero_factura):
                return False, f"El número de factura '{numero_factura}' ya existe"
            
            return True, "Número de factura válido"
            
        except Exception as e:
            logger.error(f"Error validando número de factura: {e}")
            return False, "Error validando número de factura"
    
    def _numero_factura_exists(self, numero_factura):
        """
        Verifica si un número de factura ya existe en la base de datos
        """
        try:
            query = "SELECT COUNT(*) FROM facturas WHERE numero_factura = ?"
            result = self.db.execute_query(query, (numero_factura,))
            return result[0][0] > 0 if result else False
            
        except Exception as e:
            logger.error(f"Error verificando existencia de número de factura: {e}")
            return False
    
    def update_next_numero_after_save(self, numero_factura_usado):
        """
        Actualiza la lógica interna después de guardar una factura
        Si el usuario usó un número personalizado, el siguiente se basará en ese
        """
        try:
            # Extraer la parte numérica del número usado
            numero_numerico = self._extract_numero_from_string(numero_factura_usado)
            
            if numero_numerico is not None:
                logger.info(f"Número de factura usado: {numero_factura_usado} (número: {numero_numerico})")
                # El siguiente número se calculará automáticamente basado en este
                # No necesitamos hacer nada especial aquí, ya que get_next_numero_factura()
                # siempre busca el último número usado
            
        except Exception as e:
            logger.error(f"Error actualizando numeración después de guardar: {e}")
    
    def get_configuracion_numeracion(self):
        """
        Obtiene la configuración actual de numeración
        """
        return {
            "numero_inicial": self.config.get_factura_numero_inicial(),
            "prefijo": self.config.get_factura_prefijo(),
            "sufijo": self.config.get_factura_sufijo(),
            "ultimo_numero_usado": self._get_ultimo_numero_factura()
        }
    
    def set_configuracion_numeracion(self, numero_inicial=None, prefijo=None, sufijo=None):
        """
        Establece la configuración de numeración
        """
        try:
            if numero_inicial is not None:
                self.config.set_factura_numero_inicial(numero_inicial)

            if prefijo is not None:
                self.config.set_factura_prefijo(prefijo)

            if sufijo is not None:
                self.config.set_factura_sufijo(sufijo)

            logger.info("Configuración de numeración actualizada")
            return True

        except Exception as e:
            logger.error(f"Error estableciendo configuración de numeración: {e}")
            return False

    def set_nueva_serie_numeracion(self, numero_inicial_personalizado):
        """
        Permite al usuario establecer un nuevo número inicial personalizado
        La próxima factura seguirá esta numeración
        """
        try:
            from datetime import datetime
            year = datetime.now().year

            # Validar que el número no esté ya en uso
            if self._numero_factura_exists(numero_inicial_personalizado):
                return False, "Este número de factura ya existe"

            # Extraer el patrón del número personalizado
            import re

            # Si el número ya tiene el año al final, usarlo tal como está
            if f"-{year}" in numero_inicial_personalizado:
                numero_base = numero_inicial_personalizado
            else:
                # Si no tiene año, agregarlo
                numero_base = f"{numero_inicial_personalizado}-{year}"

            # Guardar este número como referencia para la próxima numeración
            # Extraer prefijo si existe
            match = re.match(r'^([A-Za-z]*)-?(\d+)-(\d{4})$', numero_base)
            if match:
                prefijo_extraido = match.group(1) if match.group(1) else ""
                numero_extraido = int(match.group(2))

                # Actualizar configuración
                if prefijo_extraido:
                    self.config.set_factura_prefijo(prefijo_extraido)
                self.config.set_factura_numero_inicial(numero_extraido)

                logger.info(f"Nueva serie de numeración establecida: {numero_base}")
                return True, f"Nueva serie establecida. Próximo número: {self._format_numero_factura(numero_extraido + 1)}"

            return False, "Formato de número no válido"

        except Exception as e:
            logger.error(f"Error estableciendo nueva serie de numeración: {e}")
            return False, f"Error: {str(e)}"

# Instancia global del servicio
factura_numbering_service = FacturaNumberingService()
