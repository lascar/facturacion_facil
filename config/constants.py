#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constantes centralizadas del proyecto
Refactorización Pythonic - Paso 6 de Arjan Codes
"""

from typing import Final

# ============================================================================
# CONSTANTES DE BASE DE DATOS
# ============================================================================

# Configuración de conexión
DB_TIMEOUT: Final[float] = 30.0  # Timeout en segundos
DB_CACHE_SIZE: Final[int] = 10000
DB_JOURNAL_MODE: Final[str] = "WAL"
DB_SYNCHRONOUS: Final[str] = "NORMAL"
DB_TEMP_STORE: Final[str] = "MEMORY"

# ============================================================================
# CONSTANTES DE FACTURACIÓN
# ============================================================================

# IVA por defecto
DEFAULT_IVA: Final[float] = 21.0

# Número de factura inicial
DEFAULT_FACTURA_INICIAL: Final[str] = "1"

# Modos de pago
MODOS_PAGO: Final[tuple[str, ...]] = (
    "Efectivo",
    "Tarjeta",
    "Transferencia",
    "Bizum",
    "PayPal",
)

# Estados de factura
ESTADOS_FACTURA: Final[tuple[str, ...]] = (
    "Borrador",
    "Emitida",
    "Pagada",
    "Cancelada",
)

# ============================================================================
# CONSTANTES DE STOCK
# ============================================================================

# Stock mínimo por defecto
DEFAULT_STOCK_MINIMO: Final[int] = 5

# Stock inicial
DEFAULT_STOCK_INICIAL: Final[int] = 0

# Tipos de movimiento de stock
TIPO_MOVIMIENTO_ENTRADA: Final[str] = "entrada"
TIPO_MOVIMIENTO_SALIDA: Final[str] = "salida"
TIPO_MOVIMIENTO_AJUSTE: Final[str] = "ajuste"

# ============================================================================
# CONSTANTES DE INTERFAZ
# ============================================================================

# Tamaños de ventana
MAIN_WINDOW_WIDTH: Final[int] = 1200
MAIN_WINDOW_HEIGHT: Final[int] = 800

DIALOG_WIDTH: Final[int] = 800
DIALOG_HEIGHT: Final[int] = 600

# Colores (HEX)
COLOR_PRIMARY: Final[str] = "#2c3e50"
COLOR_SECONDARY: Final[str] = "#34495e"
COLOR_SUCCESS: Final[str] = "#27ae60"
COLOR_WARNING: Final[str] = "#f39c12"
COLOR_DANGER: Final[str] = "#e74c3c"
COLOR_INFO: Final[str] = "#3498db"
COLOR_LIGHT: Final[str] = "#ecf0f1"

# ============================================================================
# CONSTANTES DE PDF
# ============================================================================

# Orientación del logo
LOGO_ORIENTATION_LANDSCAPE: Final[str] = "landscape"
LOGO_ORIENTATION_PORTRAIT: Final[str] = "portrait"

# Tamaño de página
PDF_PAGE_SIZE: Final[str] = "A4"

# Márgenes (en cm)
PDF_MARGIN_CM: Final[float] = 2.0

# ============================================================================
# CONSTANTES DE LOGGING
# ============================================================================

# Niveles de log
LOG_LEVEL_DEBUG: Final[str] = "DEBUG"
LOG_LEVEL_INFO: Final[str] = "INFO"
LOG_LEVEL_WARNING: Final[str] = "WARNING"
LOG_LEVEL_ERROR: Final[str] = "ERROR"
LOG_LEVEL_CRITICAL: Final[str] = "CRITICAL"

# Formato de log
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

# Rotación de logs
LOG_MAX_BYTES: Final[int] = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT: Final[int] = 5

# ============================================================================
# CONSTANTES DE VALIDACIÓN
# ============================================================================

# Longitudes máximas
MAX_LENGTH_NOMBRE: Final[int] = 200
MAX_LENGTH_REFERENCIA: Final[int] = 50
MAX_LENGTH_DNI_NIE: Final[int] = 20
MAX_LENGTH_EMAIL: Final[int] = 100
MAX_LENGTH_TELEFONO: Final[int] = 20
MAX_LENGTH_CIF: Final[int] = 20

# Valores numéricos
MIN_PRECIO: Final[float] = 0.0
MAX_PRECIO: Final[float] = 999999.99
MIN_CANTIDAD: Final[int] = 1
MAX_CANTIDAD: Final[int] = 999999

# ============================================================================
# CONSTANTES DE FORMATO
# ============================================================================

# Formato de fecha
DATE_FORMAT: Final[str] = "%Y-%m-%d"
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT: Final[str] = "%d/%m/%Y"
DISPLAY_DATETIME_FORMAT: Final[str] = "%d/%m/%Y %H:%M:%S"

# Formato de moneda
CURRENCY_SYMBOL: Final[str] = "€"
CURRENCY_DECIMAL_PLACES: Final[int] = 2

# ============================================================================
# CONSTANTES DE TESTING
# ============================================================================

# Prefijos para identificar tests
TEST_PREFIX: Final[str] = "test_"
TEST_DATABASE_PREFIX: Final[str] = "test_"
TEST_TEMP_PREFIX: Final[str] = "temp_"

# Timeout para tests
TEST_TIMEOUT_SECONDS: Final[int] = 30

