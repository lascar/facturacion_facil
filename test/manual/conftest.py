# -*- coding: utf-8 -*-
"""
Configuration pytest pour les tests manuels
"""

import pytest
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Importer les fixtures du conftest behaviour
from test.behaviour.conftest import (
    app_instance,
    isolated_test_database,
    isolated_test_config,
    test_database_path,
    test_config,
    screenshots_dir,
    mock_messagebox,
    mock_filedialog
)

# Réexporter les fixtures pour qu'elles soient disponibles dans test/manual/
__all__ = [
    'app_instance',
    'isolated_test_database',
    'isolated_test_config',
    'test_database_path',
    'test_config',
    'screenshots_dir',
    'mock_messagebox',
    'mock_filedialog'
]

