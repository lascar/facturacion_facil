import pytest
import os
import sys
import tempfile
import sqlite3
import threading
from faker import Faker

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import Database
from database.models import Producto, Organizacion, Stock
from test.utils.test_database_manager import test_db_manager, isolated_test_db, isolated_test_environment

# Configurar Faker en español
fake = Faker('es_ES')

@pytest.fixture(scope="session")
def faker_instance():
    """Instancia de Faker configurada en español"""
    return fake

@pytest.fixture
def temp_db(request):
    """Base de datos temporal para tests - Version améliorée"""
    # Obtenir le nom du test pour debugging
    test_name = request.node.name if hasattr(request, 'node') else 'unknown'

    # Créer base de données isolée
    test_db, db_path = test_db_manager.create_test_database(test_name)

    yield test_db

    # Nettoyage automatique géré par le manager
    # (le manager nettoie automatiquement à la fin du thread)

@pytest.fixture
def sample_producto_data(faker_instance):
    """Datos de ejemplo para un producto"""
    return {
        'nombre': faker_instance.word().capitalize(),
        'referencia': faker_instance.ean13(),
        'precio': round(faker_instance.pyfloat(positive=True, max_value=1000, right_digits=2), 2),
        'categoria': faker_instance.random_element(['Electrónicos', 'Ropa', 'Hogar', 'Deportes']),
        'descripcion': faker_instance.text(max_nb_chars=200),
        'imagen_path': '',
        'iva_recomendado': faker_instance.random_element([0, 4, 10, 21])
    }

@pytest.fixture
def sample_producto(sample_producto_data):
    """Producto de ejemplo"""
    return Producto(**sample_producto_data)

@pytest.fixture
def sample_organizacion_data(faker_instance):
    """Datos de ejemplo para organización"""
    return {
        'nombre': faker_instance.company(),
        'direccion': faker_instance.address(),
        'telefono': faker_instance.phone_number(),
        'email': faker_instance.company_email(),
        'cif': faker_instance.random_element(['A12345678', 'B87654321', 'C11111111']),
        'logo_path': ''
    }

@pytest.fixture
def sample_organizacion(sample_organizacion_data):
    """Organización de ejemplo"""
    return Organizacion(**sample_organizacion_data)

@pytest.fixture
def productos_list(faker_instance):
    """Lista de productos de ejemplo"""
    productos = []
    for _ in range(5):
        producto_data = {
            'nombre': faker_instance.word().capitalize(),
            'referencia': faker_instance.ean13(),
            'precio': round(faker_instance.pyfloat(positive=True, max_value=500, right_digits=2), 2),
            'categoria': faker_instance.random_element(['Electrónicos', 'Ropa', 'Hogar']),
            'descripcion': faker_instance.text(max_nb_chars=100),
            'imagen_path': '',
            'iva_recomendado': 21.0
        }
        productos.append(Producto(**producto_data))
    return productos

@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch, temp_db, request):
    """Configurar entorno de test automáticamente"""
    # Obtenir le nom du test
    test_name = request.node.name if hasattr(request, 'node') else 'unknown'

    # Usar base de datos temporal
    monkeypatch.setattr('database.database.db', temp_db)
    monkeypatch.setattr('database.models.db', temp_db)

    # Crear directorio temporal para assets usando el manager
    test_assets_dir = test_db_manager.create_test_directory(f"{test_name}_assets")
    monkeypatch.setattr('os.makedirs', lambda path, exist_ok=True: None)

    yield

    # Le nettoyage est géré automatiquement par le manager

@pytest.fixture
def isolated_db(request):
    """Base de données complètement isolée pour tests spéciaux"""
    test_name = request.node.name if hasattr(request, 'node') else 'isolated'

    with isolated_test_db(test_name) as db:
        yield db

@pytest.fixture
def isolated_environment(request):
    """Environnement de test complètement isolé"""
    test_name = request.node.name if hasattr(request, 'node') else 'isolated'

    with isolated_test_environment(test_name) as env:
        yield env

@pytest.fixture
def clean_db(temp_db):
    """Base de données nettoyée avant chaque test"""
    # Remettre à zéro la base de données
    test_db_manager.reset_database(temp_db)
    yield temp_db

@pytest.fixture
def mock_messagebox(mocker):
    """Mock para PyQt5.QtWidgets.QMessageBox"""
    return mocker.patch('PyQt5.QtWidgets.QMessageBox')

# Hooks pytest pour nettoyage automatique
def pytest_runtest_teardown(item, nextitem):
    """Nettoyage après chaque test"""
    # Nettoyer les ressources du thread actuel
    test_db_manager.cleanup_test_resources()

def pytest_sessionfinish(session, exitstatus):
    """Nettoyage à la fin de tous les tests"""
    # Nettoyer toutes les ressources restantes
    test_db_manager.cleanup_all_test_resources()

    # Nettoyer la base de données de test par défaut
    if hasattr(session.config, '_pytest_default_db_path'):
        try:
            if os.path.exists(session.config._pytest_default_db_path):
                os.unlink(session.config._pytest_default_db_path)
        except Exception:
            pass

    # Nettoyer les variables d'environnement
    os.environ.pop('PYTEST_RUNNING', None)
    os.environ.pop('DISABLE_PDF_OPEN', None)
    os.environ.pop('TEST_DATABASE_PATH', None)

    # Afficher les statistiques finales
    stats = test_db_manager.get_test_stats()
    if stats['total_databases'] > 0 or stats['total_directories'] > 0:
        print(f"\n🧹 Nettoyage final: {stats['total_databases']} DBs, {stats['total_directories']} répertoires")

def pytest_ignore_collect(path, config):
    """Ignore les fichiers de démonstration qui créent des fenêtres GUI"""
    if "demo" in str(path):
        return True
    return False

def pytest_configure(config):
    """Configuration pytest"""
    # Définir les variables d'environnement pour désactiver l'ouverture des PDFs
    os.environ['PYTEST_RUNNING'] = '1'
    os.environ['DISABLE_PDF_OPEN'] = '1'

    # PROTECTION CRITIQUE: Empêcher l'accès à la base de données de production
    # Créer une base de données de test par défaut AVANT tout import
    import tempfile
    test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db', prefix='pytest_default_')
    os.close(test_db_fd)

    # Stocker le chemin pour nettoyage ultérieur
    config._pytest_default_db_path = test_db_path

    # Remplacer le chemin de la base de données de production par le chemin de test
    # AVANT que database.database soit importé
    os.environ['TEST_DATABASE_PATH'] = test_db_path

    # Ajouter des marqueurs personnalisés
    config.addinivalue_line(
        "markers", "isolated_db: marque les tests nécessitant une DB complètement isolée"
    )
    config.addinivalue_line(
        "markers", "clean_db: marque les tests nécessitant une DB nettoyée"
    )

@pytest.fixture
def mock_filedialog(mocker):
    """Mock para PyQt5.QtWidgets.QFileDialog"""
    return mocker.patch('PyQt5.QtWidgets.QFileDialog')
