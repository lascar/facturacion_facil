# -*- coding: utf-8 -*-
"""
Configuration pytest pour les tests de comportement Selenium
"""

import pytest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.test_database import TestDatabase
from database.database import Database
from utils.logger import get_logger

logger = get_logger(__name__)

def has_display():
    """Vérifie si un serveur X est disponible"""
    import os
    return 'DISPLAY' in os.environ and os.environ['DISPLAY']

@pytest.fixture(scope="session")
def test_database_path():
    """Créer une base de données de test temporaire pour la session"""
    # Créer un répertoire temporaire pour les tests
    temp_dir = tempfile.mkdtemp(prefix="facturacion_test_behaviour_")
    db_path = os.path.join(temp_dir, "test_behaviour.db")
    
    logger.info(f"🧪 Création de la base de test behaviour: {db_path}")
    
    yield db_path
    
    # Nettoyage après les tests
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.info(f"🧹 Base de test behaviour nettoyée: {temp_dir}")
    except Exception as e:
        logger.warning(f"⚠️ Erreur lors du nettoyage: {e}")

@pytest.fixture(scope="function")
def isolated_test_database(test_database_path):
    """Créer une base de données de test isolée pour chaque test"""

    # Créer une instance de test database (elle crée son propre fichier temporaire)
    test_db = TestDatabase()

    logger.info(f"🔧 Base de test behaviour initialisée: {test_db.test_db_path}")

    yield test_db

    # Nettoyage après chaque test
    test_db.cleanup()
    logger.info("🧹 Données de test behaviour nettoyées")

@pytest.fixture(scope="function")
def app_instance(isolated_test_database, monkeypatch):
    """Créer une instance de l'application avec base de test"""

    # ACTIVER LE MODE TEST DÈS LE DÉBUT
    import os
    os.environ['PYTEST_RUNNING'] = '1'

    # PATCHER QMessageBox GLOBALEMENT
    from PyQt5.QtWidgets import QMessageBox
    original_question = QMessageBox.question
    original_critical = QMessageBox.critical
    original_warning = QMessageBox.warning
    original_information = QMessageBox.information

    def mock_question(*args, **kwargs):
        logger.debug("🔄 Dialog de confirmation intercepté dans conftest - Réponse automatique: Yes")
        return QMessageBox.Yes

    def mock_critical(*args, **kwargs):
        logger.debug(f"🔄 Dialog d'erreur intercepté - Fermeture automatique: {args[1] if len(args) > 1 else ''}")
        return QMessageBox.Ok

    def mock_warning(*args, **kwargs):
        logger.debug(f"🔄 Dialog d'avertissement intercepté - Fermeture automatique: {args[1] if len(args) > 1 else ''}")
        return QMessageBox.Ok

    def mock_information(*args, **kwargs):
        logger.debug(f"🔄 Dialog d'information intercepté - Fermeture automatique: {args[1] if len(args) > 1 else ''}")
        return QMessageBox.Ok

    QMessageBox.question = mock_question
    QMessageBox.critical = mock_critical
    QMessageBox.warning = mock_warning
    QMessageBox.information = mock_information

    # PATCHER QDialog.exec_() POUR ÉVITER LES BLOCAGES
    from PyQt5.QtWidgets import QDialog
    original_exec = QDialog.exec_

    def mock_exec(self):
        """Mock de exec_() qui affiche le dialogue sans bloquer"""
        logger.debug(f"🔄 QDialog.exec_() intercepté pour {self.__class__.__name__} - Affichage non-bloquant")
        # Afficher le dialogue en mode non-modal
        self.show()
        # Traiter les événements pour que le dialogue s'affiche
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        # Retourner Rejected par défaut (le test peut interagir avec le dialogue après)
        return QDialog.Rejected

    QDialog.exec_ = mock_exec

    # Remplacer l'instance globale de base de données par la base de test
    from database import database
    monkeypatch.setattr(database, 'db', isolated_test_database)

    # Importer et créer l'application après le monkeypatch
    from PyQt5.QtWidgets import QApplication
    from ui.main_window_pyqt5 import MainWindowPyQt5

    # Patcher aussi les modules UI qui importent db
    import ui.clientes_pyqt5
    import ui.productos_pyqt5
    import ui.client_autocomplete_widget
    import ui.product_autocomplete_widget
    import ui.data_cleanup_dialog
    monkeypatch.setattr(ui.clientes_pyqt5, 'db', isolated_test_database)
    monkeypatch.setattr(ui.productos_pyqt5, 'db', isolated_test_database)
    monkeypatch.setattr(ui.client_autocomplete_widget, 'db', isolated_test_database)
    monkeypatch.setattr(ui.product_autocomplete_widget, 'db', isolated_test_database)
    monkeypatch.setattr(ui.data_cleanup_dialog, 'db', isolated_test_database)

    # Créer l'application Qt si elle n'existe pas
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()

    # Créer la fenêtre principale
    main_window = MainWindowPyQt5()

    logger.info("🚀 Application de test behaviour créée")

    yield {
        'app': app,
        'main_window': main_window,
        'database': isolated_test_database
    }

    # Nettoyage SANS CONFIRMATION
    try:
        # Forcer la fermeture sans dialog
        logger.info("🔒 Fermeture forcée de l'application de test")

        # Fermer toutes les fenêtres enfants d'abord
        if hasattr(main_window, '_close_all_child_windows'):
            main_window._close_all_child_windows()

        # Fermer la fenêtre principale sans déclencher closeEvent
        main_window.hide()
        main_window.deleteLater()

        # Traiter les événements
        app.processEvents()

        logger.info("✅ Application de test behaviour fermée sans confirmation")
    except Exception as e:
        logger.warning(f"⚠️ Erreur lors de la fermeture: {e}")
    finally:
        # Restaurer QMessageBox originaux
        QMessageBox.question = original_question
        QMessageBox.critical = original_critical
        QMessageBox.warning = original_warning
        QMessageBox.information = original_information
        # Restaurer QDialog.exec_() original
        QDialog.exec_ = original_exec

def pytest_configure(config):
    """Configuration globale de pytest pour les tests behaviour"""
    import os

    # Activer le mode test globalement
    os.environ['PYTEST_RUNNING'] = '1'

    # Ajouter un marqueur pour les tests nécessitant un affichage graphique
    config.addinivalue_line(
        "markers", "gui: marque les tests nécessitant un affichage graphique (X server)"
    )

    # Patch global de QMessageBox pour TOUS les tests
    try:
        from PyQt5.QtWidgets import QMessageBox

        # Sauvegarder l'original
        if not hasattr(QMessageBox, '_original_question'):
            QMessageBox._original_question = QMessageBox.question
        if not hasattr(QMessageBox, '_original_critical'):
            QMessageBox._original_critical = QMessageBox.critical
        if not hasattr(QMessageBox, '_original_warning'):
            QMessageBox._original_warning = QMessageBox.warning
        if not hasattr(QMessageBox, '_original_information'):
            QMessageBox._original_information = QMessageBox.information

        def global_mock_question(*args, **kwargs):
            print("🔄 GLOBAL: Dialog de confirmation intercepté - Réponse automatique: Yes")
            return QMessageBox.Yes

        def global_mock_critical(*args, **kwargs):
            print("🔄 GLOBAL: Dialog d'erreur intercepté - Fermeture automatique")
            return QMessageBox.Ok

        def global_mock_warning(*args, **kwargs):
            print("🔄 GLOBAL: Dialog d'avertissement intercepté - Fermeture automatique")
            return QMessageBox.Ok

        def global_mock_information(*args, **kwargs):
            print("🔄 GLOBAL: Dialog d'information intercepté - Fermeture automatique")
            return QMessageBox.Ok

        QMessageBox.question = global_mock_question
        QMessageBox.critical = global_mock_critical
        QMessageBox.warning = global_mock_warning
        QMessageBox.information = global_mock_information
        print("✅ Patch global QMessageBox complet activé")

    except ImportError:
        print("⚠️ PyQt5 non disponible pour le patch global")

def pytest_unconfigure(config):
    """Nettoyage global après tous les tests"""
    import os

    # Restaurer QMessageBox original
    try:
        from PyQt5.QtWidgets import QMessageBox
        if hasattr(QMessageBox, '_original_question'):
            QMessageBox.question = QMessageBox._original_question
            delattr(QMessageBox, '_original_question')
        if hasattr(QMessageBox, '_original_critical'):
            QMessageBox.critical = QMessageBox._original_critical
            delattr(QMessageBox, '_original_critical')
        if hasattr(QMessageBox, '_original_warning'):
            QMessageBox.warning = QMessageBox._original_warning
            delattr(QMessageBox, '_original_warning')
        if hasattr(QMessageBox, '_original_information'):
            QMessageBox.information = QMessageBox._original_information
            delattr(QMessageBox, '_original_information')
        print("✅ Patch global QMessageBox complet restauré")
    except ImportError:
        pass

    # Nettoyer les variables d'environnement
    os.environ.pop('PYTEST_RUNNING', None)

def pytest_addoption(parser):
    """Ajouter des options de ligne de commande pour les tests behaviour"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Exécuter les tests en mode headless (sans interface graphique)"
    )
    parser.addoption(
        "--screenshots",
        action="store_true",
        default=False,
        help="Prendre des captures d'écran en cas d'échec"
    )
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="Exécuter les tests lentement pour le débogage"
    )

@pytest.fixture
def test_config(request):
    """Configuration des tests basée sur les options de ligne de commande"""
    return {
        'headless': request.config.getoption("--headless"),
        'screenshots': request.config.getoption("--screenshots"),
        'slow': request.config.getoption("--slow")
    }

@pytest.fixture(scope="session")
def screenshots_dir():
    """Répertoire pour sauvegarder les captures d'écran"""
    screenshots_path = os.path.join("test", "behaviour", "screenshots")
    os.makedirs(screenshots_path, exist_ok=True)
    return screenshots_path
