# -*- coding: utf-8 -*-
"""
Configuration pytest pour les tests d'intégration
"""

import pytest
import os
import tempfile
import gc
import sqlite3

# Importer isolated_test_config depuis test/behaviour/conftest.py
from test.behaviour.conftest import isolated_test_config


@pytest.fixture
def integration_db(monkeypatch, tmp_path):
    """
    Base de données isolée pour tests d'intégration avec monkeypatch
    
    Cette fixture:
    - Crée une base de données temporaire unique
    - Utilise monkeypatch pour remplacer l'instance globale db dans les modèles
    - Isole config.json pour les tests d'Organizacion
    - Garantit un nettoyage complet après chaque test
    """
    import uuid
    from database.database import Database
    import json
    
    # Créer un fichier temporaire unique pour la DB
    unique_id = str(uuid.uuid4())[:8]
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db', prefix=f'integration_test_{unique_id}_')
    temp_file.close()
    db_path = temp_file.name
    
    # Créer un fichier config.json temporaire
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = str(config_dir / "config.json")
    
    # Écrire un config.json vide
    with open(config_file, 'w') as f:
        json.dump({'organizacion_defaults': {}}, f)
    
    # Patcher CONFIG_FILE
    old_config_file = os.environ.get('CONFIG_FILE')
    monkeypatch.setenv('CONFIG_FILE', config_file)
    
    # Invalider le cache de config
    from config.config import invalidate_config_cache, _config_cache
    _config_cache.clear()
    invalidate_config_cache(config_file)
    
    # Désactiver temporairement TEST_DATABASE_PATH
    old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
    os.environ.pop('TEST_DATABASE_PATH', None)
    
    # Créer l'instance de base de données
    test_db = Database(db_path)
    
    # Monkeypatch l'instance globale dans database.models
    try:
        import database.models
        monkeypatch.setattr(database.models, 'db', test_db)
    except:
        pass
    
    # Restaurer TEST_DATABASE_PATH
    if old_test_db_path:
        os.environ['TEST_DATABASE_PATH'] = old_test_db_path
    
    yield test_db
    
    # Nettoyage complet
    try:
        if hasattr(test_db, 'close'):
            test_db.close()
    except:
        pass
    
    # Forcer le garbage collector
    gc.collect()
    
    # Fermer toutes les connexions SQLite
    for obj in gc.get_objects():
        if isinstance(obj, sqlite3.Connection):
            try:
                obj.close()
            except:
                pass
    
    # Supprimer les fichiers DB
    try:
        for ext in ['', '-wal', '-shm', '-journal']:
            path = db_path + ext
            if os.path.exists(path):
                try:
                    os.unlink(path)
                except:
                    pass
    except:
        pass
    
    # Restaurer CONFIG_FILE si nécessaire
    if old_config_file:
        os.environ['CONFIG_FILE'] = old_config_file
    else:
        os.environ.pop('CONFIG_FILE', None)
    
    # Invalider le cache à nouveau
    _config_cache.clear()

