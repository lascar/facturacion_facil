# -*- coding: utf-8 -*-
"""
Base de données de test pour éviter d'utiliser la base de production
"""

import os
import shutil
import tempfile
from database.database import Database
from utils.logger import get_logger

class TestDatabase(Database):
    """Base de données de test qui utilise un fichier temporaire"""
    
    def __init__(self):
        self.logger = get_logger("test_database")
        
        # Créer un fichier temporaire pour la base de test
        self.temp_dir = tempfile.mkdtemp(prefix="facturacion_test_")
        self.test_db_path = os.path.join(self.temp_dir, "test_facturacion.db")
        
        # Copier la structure de la base de production (sans les données)
        self.setup_test_database()
        
        # Initialiser avec le chemin de test
        super().__init__(self.test_db_path)

        # Ajouter les données de test après l'initialisation
        self.add_test_data()

        self.logger.info(f"Base de données de test créée: {self.test_db_path}")
    
    def setup_test_database(self):
        """Créer la structure de la base de test"""
        try:
            # Créer une base vide avec la même structure
            # Ne pas appeler super().__init__ ici car on va le faire après
            pass

        except Exception as e:
            self.logger.error(f"Erreur création base de test: {e}")
            raise
    
    def add_test_data(self):
        """Ajouter des données de test"""
        try:
            # Clients de test
            test_clients = [
                {
                    'nombre': 'Client Test 1',
                    'nif': '12345678A',
                    'direccion': 'Calle Test 1',
                    'telefono': '111222333',
                    'email': 'test1@example.com'
                },
                {
                    'nombre': 'Client Test 2',
                    'nif': '87654321B',
                    'direccion': 'Calle Test 2',
                    'telefono': '444555666',
                    'email': 'test2@example.com'
                }
            ]
            
            for client_data in test_clients:
                self.add_client(client_data)
            
            # États de facture de test
            test_states = [
                {'nombre': 'Borrador', 'color': '#95a5a6'},
                {'nombre': 'Enviada', 'color': '#3498db'}
            ]
            
            for state in test_states:
                self.add_invoice_state(state)
            
            self.logger.info("Données de test ajoutées")
            
        except Exception as e:
            self.logger.error(f"Erreur ajout données de test: {e}")
    
    def cleanup(self):
        """Nettoyer la base de test"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.logger.info(f"Base de test nettoyée: {self.temp_dir}")
        except Exception as e:
            self.logger.error(f"Erreur nettoyage base de test: {e}")
    
    def __del__(self):
        """Nettoyage automatique"""
        self.cleanup()

# Instance globale pour les tests
test_db = None

def get_test_database():
    """Obtenir une instance de base de données de test"""
    global test_db
    if test_db is None:
        test_db = TestDatabase()
    return test_db

def cleanup_test_database():
    """Nettoyer la base de données de test"""
    global test_db
    if test_db is not None:
        test_db.cleanup()
        test_db = None
