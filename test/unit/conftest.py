# -*- coding: utf-8 -*-
"""
Configuration pytest pour les tests unitaires
Fournit des fixtures isolées spécifiquement pour les tests unitaires
"""

import pytest
import os
import sys

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from test.utils.test_database_manager import test_db_manager


@pytest.fixture
def unit_db(request):
    """
    Base de données isolée pour tests unitaires

    Cette fixture crée une base de données complètement isolée pour chaque test unitaire.
    Elle garantit:
    - Une nouvelle base de données pour chaque test
    - Réinitialisation des séquences SQLite (IDs commencent à 1)
    - Nettoyage complet après chaque test (fichiers .db, -wal, -shm, -journal)
    """
    import tempfile
    import uuid
    import sqlite3
    import gc
    from database.database import Database

    # Obtenir le nom du test pour debugging
    test_name = request.node.name if hasattr(request, 'node') else 'unknown'

    # Créer un nom de fichier unique
    unique_id = str(uuid.uuid4())[:8]

    # Créer un fichier temporaire unique
    db_fd, db_path = tempfile.mkstemp(
        suffix='.db',
        prefix=f'unit_test_{test_name}_{unique_id}_'
    )
    os.close(db_fd)

    # Désactiver temporairement TEST_DATABASE_PATH pour forcer l'utilisation de notre DB
    old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
    os.environ.pop('TEST_DATABASE_PATH', None)

    # Créer l'instance de base de données
    test_db = Database(db_path)

    # Restaurer TEST_DATABASE_PATH
    if old_test_db_path:
        os.environ['TEST_DATABASE_PATH'] = old_test_db_path

    # Réinitialiser les séquences SQLite
    try:
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sqlite_sequence")
        conn.commit()
        conn.close()
    except:
        pass

    yield test_db

    # Nettoyage complet après chaque test
    try:
        # Fermer toutes les connexions
        if hasattr(test_db, 'close'):
            test_db.close()
    except:
        pass

    # Forcer la fermeture de toutes les connexions SQLite
    try:
        gc.collect()  # Forçer le garbage collector

        # Fermer toutes les connexions SQLite ouvertes
        for obj in gc.get_objects():
            if isinstance(obj, sqlite3.Connection):
                try:
                    obj.close()
                except:
                    pass
    except:
        pass

    try:
        # Supprimer tous les fichiers de base de données
        for ext in ['', '-wal', '-shm', '-journal']:
            path = db_path + ext
            if os.path.exists(path):
                try:
                    os.unlink(path)
                except:
                    pass
    except:
        pass


@pytest.fixture
def clean_unit_db(request):
    """
    Base de données isolée avec nettoyage agressif
    
    Utiliser cette fixture pour les tests qui nécessitent une isolation absolue.
    """
    import tempfile
    import uuid
    
    # Créer un nom de fichier unique
    unique_id = str(uuid.uuid4())[:8]
    test_name = request.node.name if hasattr(request, 'node') else 'unknown'
    
    # Créer dans un répertoire temporaire unique
    temp_dir = tempfile.mkdtemp(prefix=f'test_unit_{unique_id}_')
    db_path = os.path.join(temp_dir, f'{test_name}.db')
    
    # Créer l'instance de base de données
    from database.database import Database
    test_db = Database(db_path)
    
    # Réinitialiser les séquences
    try:
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sqlite_sequence")
        conn.commit()
        conn.close()
    except:
        pass
    
    yield test_db
    
    # Nettoyage agressif
    try:
        if hasattr(test_db, 'close'):
            test_db.close()
    except:
        pass
    
    try:
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    except:
        pass

