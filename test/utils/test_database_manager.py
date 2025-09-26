"""
Gestionnaire de base de données pour les tests
Assure l'isolation complète et le nettoyage automatique
"""

import os
import tempfile
import shutil
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from utils.logger import get_logger

class DatabaseManager:
    """Gestionnaire centralisé pour les bases de données de test"""
    
    def __init__(self):
        self.logger = get_logger("test_database_manager")
        self._test_databases = {}
        self._test_directories = {}
        self._lock = threading.Lock()
        
    def create_test_database(self, test_name=None):
        """
        Créer une base de données de test isolée
        
        Args:
            test_name (str): Nom du test (optionnel, pour debugging)
            
        Returns:
            tuple: (Database instance, db_path)
        """
        from database.database import Database
        
        with self._lock:
            # Créer un fichier temporaire unique
            db_fd, db_path = tempfile.mkstemp(
                suffix='.db',
                prefix=f'test_{test_name}_' if test_name else 'test_'
            )
            os.close(db_fd)
            
            # Créer l'instance de base de données
            test_db = Database(db_path)
            
            # Enregistrer pour nettoyage
            thread_id = threading.get_ident()
            if thread_id not in self._test_databases:
                self._test_databases[thread_id] = []
            self._test_databases[thread_id].append(db_path)
            
            self.logger.debug(f"Base de données de test créée: {os.path.basename(db_path)}")
            return test_db, db_path
    
    def create_test_directory(self, test_name=None):
        """
        Créer un répertoire temporaire pour les tests
        
        Args:
            test_name (str): Nom du test (optionnel)
            
        Returns:
            str: Chemin vers le répertoire temporaire
        """
        with self._lock:
            # Créer un répertoire temporaire
            temp_dir = tempfile.mkdtemp(
                prefix=f'test_{test_name}_' if test_name else 'test_'
            )
            
            # Enregistrer pour nettoyage
            thread_id = threading.get_ident()
            if thread_id not in self._test_directories:
                self._test_directories[thread_id] = []
            self._test_directories[thread_id].append(temp_dir)
            
            self.logger.debug(f"Répertoire de test créé: {os.path.basename(temp_dir)}")
            return temp_dir
    
    def cleanup_test_resources(self, thread_id=None):
        """
        Nettoyer toutes les ressources de test pour un thread
        
        Args:
            thread_id (int): ID du thread (par défaut: thread actuel)
        """
        if thread_id is None:
            thread_id = threading.get_ident()
        
        with self._lock:
            # Nettoyer les bases de données
            if thread_id in self._test_databases:
                for db_path in self._test_databases[thread_id]:
                    try:
                        if os.path.exists(db_path):
                            os.unlink(db_path)
                            self.logger.debug(f"Base de données supprimée: {os.path.basename(db_path)}")
                    except Exception as e:
                        self.logger.warning(f"Erreur suppression DB {db_path}: {e}")
                del self._test_databases[thread_id]
            
            # Nettoyer les répertoires
            if thread_id in self._test_directories:
                for temp_dir in self._test_directories[thread_id]:
                    try:
                        if os.path.exists(temp_dir):
                            shutil.rmtree(temp_dir, ignore_errors=True)
                            self.logger.debug(f"Répertoire supprimé: {os.path.basename(temp_dir)}")
                    except Exception as e:
                        self.logger.warning(f"Erreur suppression répertoire {temp_dir}: {e}")
                del self._test_directories[thread_id]
    
    def cleanup_all_test_resources(self):
        """Nettoyer toutes les ressources de test de tous les threads"""
        with self._lock:
            # Nettoyer toutes les bases de données
            for thread_id in list(self._test_databases.keys()):
                # Nettoyer les bases de données pour ce thread
                if thread_id in self._test_databases:
                    for db_path in self._test_databases[thread_id]:
                        try:
                            if os.path.exists(db_path):
                                os.unlink(db_path)
                                self.logger.debug(f"Base de données supprimée: {os.path.basename(db_path)}")
                        except Exception as e:
                            self.logger.warning(f"Erreur suppression DB {db_path}: {e}")
                    del self._test_databases[thread_id]

                # Nettoyer les répertoires pour ce thread
                if thread_id in self._test_directories:
                    for temp_dir in self._test_directories[thread_id]:
                        try:
                            if os.path.exists(temp_dir):
                                shutil.rmtree(temp_dir, ignore_errors=True)
                                self.logger.debug(f"Répertoire supprimé: {os.path.basename(temp_dir)}")
                        except Exception as e:
                            self.logger.warning(f"Erreur suppression répertoire {temp_dir}: {e}")
                    del self._test_directories[thread_id]

            self.logger.info("Toutes les ressources de test nettoyées")
    
    @contextmanager
    def isolated_database(self, test_name=None):
        """
        Context manager pour une base de données isolée
        
        Args:
            test_name (str): Nom du test
            
        Yields:
            Database: Instance de base de données isolée
        """
        test_db, db_path = self.create_test_database(test_name)
        
        try:
            yield test_db
        finally:
            # Nettoyage automatique
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
                    self.logger.debug(f"Base de données nettoyée: {os.path.basename(db_path)}")
            except Exception as e:
                self.logger.warning(f"Erreur nettoyage DB {db_path}: {e}")
    
    @contextmanager
    def isolated_environment(self, test_name=None):
        """
        Context manager pour un environnement de test complet
        
        Args:
            test_name (str): Nom du test
            
        Yields:
            dict: Environnement de test avec 'db' et 'temp_dir'
        """
        test_db, db_path = self.create_test_database(test_name)
        temp_dir = self.create_test_directory(test_name)
        
        try:
            yield {
                'db': test_db,
                'db_path': db_path,
                'temp_dir': temp_dir
            }
        finally:
            # Nettoyage automatique
            try:
                if os.path.exists(db_path):
                    os.unlink(db_path)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
                self.logger.debug(f"Environnement nettoyé: {test_name}")
            except Exception as e:
                self.logger.warning(f"Erreur nettoyage environnement {test_name}: {e}")
    
    def reset_database(self, test_db):
        """
        Remettre à zéro une base de données de test
        
        Args:
            test_db (Database): Instance de base de données à remettre à zéro
        """
        try:
            conn = test_db.get_connection()
            cursor = conn.cursor()
            
            # Obtenir toutes les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Supprimer toutes les données (mais garder la structure)
            for table in tables:
                if table != 'sqlite_sequence':  # Table système SQLite
                    cursor.execute(f"DELETE FROM {table}")
            
            # Remettre à zéro les auto-increment
            cursor.execute("DELETE FROM sqlite_sequence")
            
            conn.commit()
            conn.close()
            
            self.logger.debug("Base de données remise à zéro")
            
        except Exception as e:
            self.logger.error(f"Erreur remise à zéro DB: {e}")
            raise
    
    def get_test_stats(self):
        """Obtenir des statistiques sur les ressources de test"""
        with self._lock:
            total_dbs = sum(len(dbs) for dbs in self._test_databases.values())
            total_dirs = sum(len(dirs) for dirs in self._test_directories.values())
            
            return {
                'active_threads': len(self._test_databases),
                'total_databases': total_dbs,
                'total_directories': total_dirs,
                'databases_by_thread': {tid: len(dbs) for tid, dbs in self._test_databases.items()},
                'directories_by_thread': {tid: len(dirs) for tid, dirs in self._test_directories.items()}
            }

# Instance globale du gestionnaire
test_db_manager = DatabaseManager()

def setup_test_database(test_name=None):
    """
    Fonction utilitaire pour configurer une base de données de test
    
    Args:
        test_name (str): Nom du test
        
    Returns:
        Database: Instance de base de données de test
    """
    return test_db_manager.create_test_database(test_name)[0]

def cleanup_test_databases():
    """Fonction utilitaire pour nettoyer toutes les bases de données de test"""
    test_db_manager.cleanup_all_test_resources()

@contextmanager
def isolated_test_db(test_name=None):
    """
    Context manager simple pour une base de données de test isolée
    
    Args:
        test_name (str): Nom du test
        
    Yields:
        Database: Instance de base de données isolée
    """
    with test_db_manager.isolated_database(test_name) as db:
        yield db

@contextmanager
def isolated_test_environment(test_name=None):
    """
    Context manager simple pour un environnement de test complet
    
    Args:
        test_name (str): Nom du test
        
    Yields:
        dict: Environnement de test
    """
    with test_db_manager.isolated_environment(test_name) as env:
        yield env
