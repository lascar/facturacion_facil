# -*- coding: utf-8 -*-
"""
Base de données de test pour éviter d'utiliser la base de production
"""

import os
import shutil
import tempfile
from database.database import Database
from database.fixtures import TestFixtures
from utils.logger import get_logger

class TestDatabase(Database):
    """Base de données de test qui utilise un fichier temporaire"""
    
    def __init__(self, with_fixtures=True):
        self.logger = get_logger("test_database")

        # Créer un fichier temporaire pour la base de test
        self.temp_dir = tempfile.mkdtemp(prefix="facturacion_test_")
        self.test_db_path = os.path.join(self.temp_dir, "test_facturacion.db")

        # Initialiser avec le chemin de test (Database s'occupe de tout)
        super().__init__(self.test_db_path)

        # Gestionnaire de fixtures
        self.fixtures = TestFixtures(self.test_db_path)

        # Ajouter les fixtures ou les données de test basiques
        if with_fixtures:
            self.create_fixtures()
        else:
            # Ajouter seulement les données de base (ancienne méthode)
            self.add_test_data()

        self.logger.info(f"Base de données de test créée: {self.test_db_path}")
    

    
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
    
    def create_fixtures(self):
        """Créer les fixtures de test standardisées"""
        try:
            self.fixtures.create_fixtures()
            return self.fixtures.get_fixtures_summary()
        except Exception as e:
            self.logger.error(f"Erreur création fixtures: {e}")
            # Fallback vers les anciennes données de test
            self.add_test_data()
            return {'products_count': 0, 'clients_count': 0, 'invoices_count': 0}

    def reset_to_fixtures(self):
        """Remettre la base à l'état initial des fixtures"""
        try:
            self.fixtures.reset_to_fixtures()
            return self.fixtures.get_fixtures_summary()
        except Exception as e:
            self.logger.error(f"Erreur reset fixtures: {e}")
            raise

    def get_fixtures_summary(self):
        """Obtenir un résumé des fixtures"""
        return self.fixtures.get_fixtures_summary()

    # ==================== MÉTHODES MANQUANTES POUR COMPATIBILITÉ ====================

    def get_all_invoice_statuses(self):
        """Obtenir tous les états de factures (méthode de compatibilité)"""
        try:
            # Retourner des états par défaut pour les tests
            return [
                {
                    'id': 1,
                    'nombre': 'Borrador',
                    'descripcion': 'Factura en borrador',
                    'permite_modificacion': True,
                    'color': '#FFA500',
                    'orden': 1,
                    'activo': True
                },
                {
                    'id': 2,
                    'nombre': 'Enviada',
                    'descripcion': 'Factura enviada',
                    'permite_modificacion': False,
                    'color': '#0066CC',
                    'orden': 2,
                    'activo': True
                },
                {
                    'id': 3,
                    'nombre': 'Pagada',
                    'descripcion': 'Factura pagada',
                    'permite_modificacion': False,
                    'color': '#00AA00',
                    'orden': 3,
                    'activo': True
                }
            ]
        except Exception as e:
            self.logger.error(f"Error obteniendo estados de facturas: {e}")
            return []

    def get_invoice_status_by_name(self, status_name):
        """Obtenir un état de facture par nom (méthode de compatibilité)"""
        try:
            statuses = self.get_all_invoice_statuses()
            for status in statuses:
                if status['nombre'] == status_name:
                    return status
            return None
        except Exception as e:
            self.logger.error(f"Error obteniendo estado por nombre {status_name}: {e}")
            return None

    @property
    def db_path(self):
        """Propriété pour compatibilité avec les anciens tests"""
        return self.test_db_path

    @db_path.setter
    def db_path(self, value):
        """Setter pour compatibilité avec Database.__init__"""
        self.test_db_path = value

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

def get_test_database(with_fixtures=True):
    """Obtenir une instance de base de données de test"""
    global test_db
    if test_db is None:
        test_db = TestDatabase(with_fixtures=with_fixtures)
    return test_db

def cleanup_test_database():
    """Nettoyer la base de données de test"""
    global test_db
    if test_db is not None:
        test_db.cleanup()
        test_db = None
