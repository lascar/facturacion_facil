# -*- coding: utf-8 -*-
"""
Validadores comunes para productos y facturas
"""
from utils.translations import get_text
from utils.logger import get_logger
import re

logger = get_logger("validators")

class ValidationError(Exception):
    """Excepción personalizada para errores de validación"""
    pass

class FormValidator:
    """Clase para validar formularios comunes"""
    
    @staticmethod
    def validate_required_field(value, field_name):
        """Valida que un campo requerido no esté vacío"""
        if not value or not value.strip():
            return f"{field_name}: {get_text('campo_requerido')}"
        return None
    
    @staticmethod
    def validate_precio(precio_str, field_name="Precio"):
        """Valida que el precio sea un número válido y positivo"""
        try:
            precio = float(precio_str)
            if precio < 0:
                return f"{field_name}: {get_text('precio_invalido')}"
            return None
        except (ValueError, TypeError):
            return f"{field_name}: {get_text('precio_invalido')}"
    
    @staticmethod
    def validate_cantidad(cantidad_str, field_name="Cantidad"):
        """Valida que la cantidad sea un número entero válido y positivo"""
        try:
            cantidad = int(cantidad_str)
            if cantidad < 0:
                return f"{field_name}: {get_text('cantidad_invalida')}"
            return None
        except (ValueError, TypeError):
            return f"{field_name}: {get_text('cantidad_invalida')}"
    
    @staticmethod
    def validate_iva(iva_str, field_name="IVA"):
        """Valida que el IVA sea un número válido entre 0 y 100"""
        try:
            iva = float(iva_str)
            if iva < 0 or iva > 100:
                return f"{field_name}: {get_text('iva_invalido')}"
            return None
        except (ValueError, TypeError):
            return f"{field_name}: {get_text('iva_invalido')}"
    
    @staticmethod
    def validate_email(email, field_name="Email"):
        """Valida formato de email (opcional pero con formato correcto si se proporciona)"""
        if not email or not email.strip():
            return None  # Email es opcional

        email = email.strip()

        # Validar longitud mínima y máxima
        if len(email) < 5 or len(email) > 254:
            return f"{field_name}: Longitud de email inválida (5-254 caracteres)"

        # Patrón mejorado para email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return f"{field_name}: Formato de email inválido (ejemplo: usuario@dominio.com)"

        # Validar que no tenga puntos consecutivos
        if '..' in email:
            return f"{field_name}: Email no puede tener puntos consecutivos"

        return None
    
    @staticmethod
    def validate_phone(phone, field_name="Teléfono"):
        """Valida formato de teléfono (opcional pero con formato correcto si se proporciona)"""
        if not phone or not phone.strip():
            return None  # Teléfono es opcional

        phone = phone.strip()

        # Validar longitud mínima y máxima
        if len(phone) < 6 or len(phone) > 20:
            return f"{field_name}: Longitud de teléfono inválida (6-20 caracteres)"

        # Permitir números, espacios, guiones, paréntesis y signo + (solo al inicio)
        phone_pattern = r'^(\+)?[\d\s\-\(\)]+$'
        if not re.match(phone_pattern, phone):
            return f"{field_name}: Formato de teléfono inválido (solo números, espacios, +, -, (), permitidos)"

        # Validar que el + solo aparezca al inicio
        if phone.count('+') > 1 or ('+' in phone and not phone.startswith('+')):
            return f"{field_name}: El signo + solo puede aparecer al inicio"

        # Validar que tenga al menos 6 dígitos
        digits_only = re.sub(r'[^\d]', '', phone)
        if len(digits_only) < 6:
            return f"{field_name}: Debe contener al menos 6 dígitos"

        return None
    
    @staticmethod
    def validate_dni_nie(dni_nie, field_name="DNI/NIE/NIF"):
        """Valida formato básico de DNI/NIE/NIF español (opcional pero con formato correcto si se proporciona)"""
        if not dni_nie or not dni_nie.strip():
            return None  # DNI/NIE/NIF es opcional

        dni_nie = dni_nie.strip().upper()

        # Validar longitud
        if len(dni_nie) != 9:
            return f"{field_name}: Debe tener exactamente 9 caracteres"

        # Patrón para DNI/NIF (8 dígitos + letra) o NIE (letra + 7 dígitos + letra)
        dni_pattern = r'^\d{8}[A-Z]$'
        nie_pattern = r'^[XYZ]\d{7}[A-Z]$'

        if not (re.match(dni_pattern, dni_nie) or re.match(nie_pattern, dni_nie)):
            return f"{field_name}: Formato inválido (ejemplos: 12345678A, X1234567A)"

        # Nota: No validamos la letra de control del DNI para mayor flexibilidad
        # en un sistema de facturación que puede recibir documentos de diferentes países

        return None

class CalculationHelper:
    """Clase para cálculos comunes de precios e IVA"""
    
    @staticmethod
    def calculate_iva_amount(precio_base, iva_percentage):
        """Calcula el importe del IVA"""
        try:
            precio = float(precio_base)
            iva = float(iva_percentage)
            return round(precio * (iva / 100), 2)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def calculate_precio_con_iva(precio_base, iva_percentage):
        """Calcula el precio con IVA incluido"""
        try:
            precio = float(precio_base)
            iva = float(iva_percentage)
            return round(precio * (1 + iva / 100), 2)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def calculate_line_total(precio_unitario, cantidad, iva_percentage=0, descuento_percentage=0):
        """Calcula el total de una línea de factura"""
        try:
            precio = float(precio_unitario)
            cant = int(cantidad)
            iva = float(iva_percentage)
            descuento = float(descuento_percentage)
            
            # Subtotal sin descuento ni IVA
            subtotal = precio * cant
            
            # Aplicar descuento
            if descuento > 0:
                subtotal = subtotal * (1 - descuento / 100)
            
            # Aplicar IVA
            total_con_iva = subtotal * (1 + iva / 100)
            
            return {
                'subtotal': round(subtotal, 2),
                'descuento_amount': round(precio * cant * (descuento / 100), 2),
                'iva_amount': round(subtotal * (iva / 100), 2),
                'total': round(total_con_iva, 2)
            }
        except (ValueError, TypeError):
            return {
                'subtotal': 0.0,
                'descuento_amount': 0.0,
                'iva_amount': 0.0,
                'total': 0.0
            }
    
    @staticmethod
    def format_currency(amount, currency_symbol="€"):
        """Formatea un importe como moneda"""
        try:
            return f"{float(amount):.2f} {currency_symbol}"
        except (ValueError, TypeError):
            return f"0.00 {currency_symbol}"
    
    @staticmethod
    def format_percentage(percentage):
        """Formatea un porcentaje"""
        try:
            return f"{float(percentage):.1f}%"
        except (ValueError, TypeError):
            return "0.0%"
