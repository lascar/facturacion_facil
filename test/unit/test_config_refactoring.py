#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour la refactorisation Pythonic
Validation des nouveaux modules config/paths.py et config/constants.py
"""

import pytest
from pathlib import Path
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.paths import (
    PROJECT_ROOT,
    DATABASE_DIR,
    DATABASE_PATH,
    CONFIG_DIR,
    CONFIG_FILE,
    FACTURAS_DIR,
    FACTURAS_PDF_DIR,
    LOGO_DIR,
    LOGS_DIR,
    ensure_directories_exist,
    get_test_database_path,
    get_backup_database_path,
    is_test_database,
)

from config.constants import (
    DB_TIMEOUT,
    DEFAULT_IVA,
    DEFAULT_STOCK_MINIMO,
    MODOS_PAGO,
    ESTADOS_FACTURA,
    COLOR_PRIMARY,
    DATE_FORMAT,
)


class TestConfigPaths:
    """Tests pour config/paths.py"""
    
    def test_project_root_exists(self):
        """Vérifie que PROJECT_ROOT existe et est un Path"""
        assert isinstance(PROJECT_ROOT, Path)
        assert PROJECT_ROOT.exists()
        assert PROJECT_ROOT.is_dir()
    
    def test_database_paths_are_paths(self):
        """Vérifie que les chemins de base de données sont des Path objects"""
        assert isinstance(DATABASE_DIR, Path)
        assert isinstance(DATABASE_PATH, Path)
        assert str(DATABASE_PATH).endswith("facturacion.db")
    
    def test_config_paths_are_paths(self):
        """Vérifie que les chemins de config sont des Path objects"""
        assert isinstance(CONFIG_DIR, Path)
        assert isinstance(CONFIG_FILE, Path)
        assert str(CONFIG_FILE).endswith("config.json")
    
    def test_facturas_paths_are_paths(self):
        """Vérifie que les chemins de facturas sont des Path objects"""
        assert isinstance(FACTURAS_DIR, Path)
        assert isinstance(FACTURAS_PDF_DIR, Path)
    
    def test_logo_paths_are_paths(self):
        """Vérifie que les chemins de logos sont des Path objects"""
        assert isinstance(LOGO_DIR, Path)
    
    def test_logs_paths_are_paths(self):
        """Vérifie que les chemins de logs sont des Path objects"""
        assert isinstance(LOGS_DIR, Path)
    
    def test_ensure_directories_exist(self):
        """Vérifie que ensure_directories_exist crée les répertoires"""
        ensure_directories_exist()
        
        # Vérifier que les répertoires principaux existent
        assert DATABASE_DIR.exists()
        assert CONFIG_DIR.exists()
        assert LOGS_DIR.exists()
    
    def test_get_test_database_path(self):
        """Vérifie que get_test_database_path retourne un Path valide"""
        test_path = get_test_database_path("example")
        
        assert isinstance(test_path, Path)
        assert "test_example.db" in str(test_path)
        assert is_test_database(test_path)
    
    def test_get_backup_database_path(self):
        """Vérifie que get_backup_database_path retourne un Path valide"""
        backup_path = get_backup_database_path("20241225_120000")
        
        assert isinstance(backup_path, Path)
        assert "facturacion_backup_20241225_120000.db" in str(backup_path)
    
    def test_is_test_database_detection(self):
        """Vérifie la détection des bases de données de test"""
        # Cas positifs
        assert is_test_database("/path/to/test_database.db")
        assert is_test_database("/path/to/temp_database.db")
        assert is_test_database("/tmp/database.db")
        assert is_test_database(Path("/test/database.db"))
        
        # Cas négatifs
        assert not is_test_database("/path/to/facturacion.db")
        assert not is_test_database("/production/database.db")


class TestConfigConstants:
    """Tests pour config/constants.py"""
    
    def test_database_constants_types(self):
        """Vérifie les types des constantes de base de données"""
        assert isinstance(DB_TIMEOUT, float)
        assert DB_TIMEOUT > 0
    
    def test_facturacion_constants(self):
        """Vérifie les constantes de facturation"""
        assert isinstance(DEFAULT_IVA, float)
        assert DEFAULT_IVA == 21.0
        
        assert isinstance(MODOS_PAGO, tuple)
        assert len(MODOS_PAGO) > 0
        assert "Efectivo" in MODOS_PAGO
        
        assert isinstance(ESTADOS_FACTURA, tuple)
        assert len(ESTADOS_FACTURA) > 0
        assert "Emitida" in ESTADOS_FACTURA
    
    def test_stock_constants(self):
        """Vérifie les constantes de stock"""
        assert isinstance(DEFAULT_STOCK_MINIMO, int)
        assert DEFAULT_STOCK_MINIMO >= 0
    
    def test_color_constants(self):
        """Vérifie les constantes de couleur"""
        assert isinstance(COLOR_PRIMARY, str)
        assert COLOR_PRIMARY.startswith("#")
        assert len(COLOR_PRIMARY) == 7  # Format #RRGGBB
    
    def test_date_format_constants(self):
        """Vérifie les constantes de format de date"""
        assert isinstance(DATE_FORMAT, str)
        assert "%" in DATE_FORMAT  # Format strftime


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

