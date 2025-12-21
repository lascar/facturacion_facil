# -*- coding: utf-8 -*-
"""
Tests de comportement simples pour valider la configuration
"""

import pytest
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.test_database import TestDatabase
from utils.logger import get_logger

class TestSimpleBehaviour:
    """Tests de comportement simples pour valider la configuration"""
    
    def test_test_database_creation(self):
        """Test de création d'une base de données de test"""
        logger = get_logger(self.__class__.__name__)
        logger.info("🧪 Test: Création base de données de test")
        
        # Créer une base de test
        test_db = TestDatabase()
        
        # Vérifier que la base est créée
        assert test_db is not None, "Base de données de test non créée"
        assert hasattr(test_db, 'test_db_path'), "Chemin de base de test manquant"
        assert os.path.exists(test_db.test_db_path), "Fichier de base de test non créé"
        
        logger.info(f"✅ Base de test créée: {test_db.test_db_path}")
        
        # Vérifier que des clients de test existent
        clients = test_db.get_all_clients()
        assert len(clients) > 0, "Aucun client de test trouvé"
        logger.info(f"✅ {len(clients)} clients de test trouvés")
        
        # Nettoyage
        test_db.cleanup()
        logger.info("✅ Test création base de données réussi")
    
    def test_pyqt5_import(self):
        """Test d'importation des modules PyQt5"""
        logger = get_logger(self.__class__.__name__)
        logger.info("🧪 Test: Importation modules PyQt5")
        
        try:
            from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
            from PyQt5.QtCore import Qt, pyqtSignal
            from PyQt5.QtGui import QFont
            logger.info("✅ Modules PyQt5 importés avec succès")
        except ImportError as e:
            pytest.fail(f"Erreur importation PyQt5: {e}")
    
    def test_main_window_import(self):
        """Test d'importation de la fenêtre principale"""
        logger = get_logger(self.__class__.__name__)
        logger.info("🧪 Test: Importation fenêtre principale")
        
        try:
            from ui.main_window_pyqt5 import MainWindowPyQt5
            logger.info("✅ MainWindowPyQt5 importée avec succès")
        except ImportError as e:
            pytest.fail(f"Erreur importation MainWindowPyQt5: {e}")
    
    def test_automation_utils(self):
        """Test des utilitaires d'automatisation"""
        logger = get_logger(self.__class__.__name__)
        logger.info("🧪 Test: Utilitaires d'automatisation")
        
        try:
            from test.behaviour.utils.pyqt5_automation import PyQt5Automation
            from test.behaviour.utils.test_data_factory import TestDataFactory
            
            # Tester la factory de données
            client_data = TestDataFactory.create_test_client(1)
            assert 'nombre' in client_data, "Données client invalides"
            assert 'nif' in client_data, "NIF manquant dans les données client"
            
            product_data = TestDataFactory.create_test_product(1)
            assert 'nombre' in product_data, "Données produit invalides"
            assert 'precio_venta' in product_data, "Prix manquant dans les données produit"
            
            logger.info("✅ Utilitaires d'automatisation fonctionnels")
            
        except ImportError as e:
            pytest.fail(f"Erreur importation utilitaires: {e}")
    
    def test_behaviour_test_structure(self):
        """Test de la structure des tests de comportement"""
        logger = get_logger(self.__class__.__name__)
        logger.info("🧪 Test: Structure tests de comportement")
        
        # Vérifier que les fichiers de test existent
        behaviour_dir = os.path.dirname(__file__)
        
        expected_files = [
            'test_main_window_behaviour.py',
            'test_clientes_behaviour.py', 
            'test_facturas_behaviour.py',
            'base_behaviour_test.py',
            'conftest.py'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(behaviour_dir, filename)
            assert os.path.exists(filepath), f"Fichier manquant: {filename}"
            logger.info(f"✅ Fichier présent: {filename}")
        
        # Vérifier le répertoire utils
        utils_dir = os.path.join(behaviour_dir, 'utils')
        assert os.path.exists(utils_dir), "Répertoire utils manquant"
        
        utils_files = [
            'pyqt5_automation.py',
            'test_data_factory.py'
        ]
        
        for filename in utils_files:
            filepath = os.path.join(utils_dir, filename)
            assert os.path.exists(filepath), f"Fichier utils manquant: {filename}"
            logger.info(f"✅ Fichier utils présent: {filename}")
        
        logger.info("✅ Structure tests de comportement validée")
    
    def test_screenshots_directory(self):
        """Test du répertoire de captures d'écran"""
        logger = get_logger(self.__class__.__name__)
        logger.info("🧪 Test: Répertoire captures d'écran")
        
        behaviour_dir = os.path.dirname(__file__)
        screenshots_dir = os.path.join(behaviour_dir, 'screenshots')
        
        assert os.path.exists(screenshots_dir), "Répertoire screenshots manquant"
        assert os.path.isdir(screenshots_dir), "screenshots n'est pas un répertoire"
        
        logger.info(f"✅ Répertoire screenshots présent: {screenshots_dir}")
    
    def test_pytest_configuration(self):
        """Test de la configuration pytest"""
        logger = get_logger(self.__class__.__name__)
        logger.info("🧪 Test: Configuration pytest")

        # Chercher pytest.ini à la racine du projet
        behaviour_dir = os.path.dirname(__file__)
        root_dir = os.path.join(behaviour_dir, '..', '..')
        pytest_ini = os.path.join(root_dir, 'pytest.ini')

        assert os.path.exists(pytest_ini), "Fichier pytest.ini manquant à la racine"

        # Lire le contenu
        with open(pytest_ini, 'r') as f:
            content = f.read()

        assert '[pytest]' in content, "Configuration pytest invalide"
        assert 'markers' in content, "Marqueurs pytest manquants"
        assert 'behaviour' in content, "Marqueur behaviour manquant"

        logger.info("✅ Configuration pytest validée")
