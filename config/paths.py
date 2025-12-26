#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralización de rutas del proyecto usando pathlib
Refactorización Pythonic - Paso 6 de Arjan Codes
"""

from pathlib import Path
from typing import Final

# ============================================================================
# RUTAS BASE
# ============================================================================

# Directorio raíz del proyecto
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.resolve()

# ============================================================================
# DIRECTORIOS PRINCIPALES
# ============================================================================

# Base de datos
DATABASE_DIR: Final[Path] = PROJECT_ROOT / "base_de_datos"
DATABASE_PATH: Final[Path] = DATABASE_DIR / "facturacion.db"

# Configuración
CONFIG_DIR: Final[Path] = PROJECT_ROOT / "config"
CONFIG_FILE: Final[Path] = CONFIG_DIR / "config.json"

# Facturas y PDFs
FACTURAS_DIR: Final[Path] = PROJECT_ROOT / "facturas"
FACTURAS_PDF_DIR: Final[Path] = PROJECT_ROOT / "facturas_pdf"

# Logos e imágenes
LOGO_DIR: Final[Path] = PROJECT_ROOT / "logo"
ASSETS_DIR: Final[Path] = PROJECT_ROOT / "assets"
ASSETS_IMAGES_DIR: Final[Path] = ASSETS_DIR / "images"

# Logs
LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"
LOGS_FILE: Final[Path] = LOGS_DIR / "facturacion_facil.log"
LOGS_ERROR_FILE: Final[Path] = LOGS_DIR / "facturacion_facil_errors.log"

# Tests
TEST_DIR: Final[Path] = PROJECT_ROOT / "test"
TEST_DATABASE_DIR: Final[Path] = TEST_DIR / "test_databases"

# Data
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
STOCK_MOTIVOS_FILE: Final[Path] = DATA_DIR / "stock_motivos.json"

# ============================================================================
# FUNCIONES UTILITARIAS
# ============================================================================

def ensure_directories_exist() -> None:
    """
    Crea todos los directorios necesarios si no existen
    """
    directories = [
        DATABASE_DIR,
        CONFIG_DIR,
        FACTURAS_DIR,
        FACTURAS_PDF_DIR,
        LOGO_DIR,
        ASSETS_DIR,
        ASSETS_IMAGES_DIR,
        LOGS_DIR,
        TEST_DIR,
        TEST_DATABASE_DIR,
        DATA_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def get_test_database_path(test_name: str = "test") -> Path:
    """
    Retorna el path para una base de datos de test
    
    Args:
        test_name: Nombre del test (se añadirá automáticamente el prefijo)
    
    Returns:
        Path: Ruta completa a la base de datos de test
    """
    TEST_DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    return TEST_DATABASE_DIR / f"test_{test_name}.db"


def get_backup_database_path(timestamp: str = None) -> Path:
    """
    Retorna el path para un backup de la base de datos
    
    Args:
        timestamp: Timestamp opcional para el nombre del backup
    
    Returns:
        Path: Ruta completa al archivo de backup
    """
    from datetime import datetime
    
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return DATABASE_DIR / f"facturacion_backup_{timestamp}.db"


def is_test_database(db_path: Path | str) -> bool:
    """
    Verifica si una ruta corresponde a una base de datos de test
    
    Args:
        db_path: Ruta a verificar
    
    Returns:
        bool: True si es una base de datos de test
    """
    path_str = str(db_path).lower()
    return any(keyword in path_str for keyword in ["test", "temp", "tmp"])


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

# Crear directorios al importar el módulo
ensure_directories_exist()

