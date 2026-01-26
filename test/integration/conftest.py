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
def integration_db(monkeypatch):
    """
    Base de données isolée pour tests d'intégration avec monkeypatch
    
    Cette fixture:
    - Crée une base de données temporaire unique
    - Utilise monkeypatch pour remplacer l'instance globale db dans les modèles
    - Garantit un nettoyage complet après chaque test
    """
    import uuid
    from database.database import Database
    
    # Créer un fichier temporaire unique
    unique_id = str(uuid.uuid4())[:8]
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db', prefix=f'integration_test_{unique_id}_')
    temp_file.close()
    db_path = temp_file.name
    
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
    
    # Supprimer les fichiers
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

