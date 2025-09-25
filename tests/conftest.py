import pytest
import os
import sys
import tempfile
import sqlite3
from faker import Faker

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import Database
from database.models import Producto, Organizacion, Stock

# Configurar Faker en español
fake = Faker('es_ES')

@pytest.fixture(scope="session")
def faker_instance():
    """Instancia de Faker configurada en español"""
    return fake

@pytest.fixture
def temp_db():
    """Base de datos temporal para tests"""
    # Crear archivo temporal
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    # Crear instancia de base de datos temporal
    test_db = Database(db_path)
    
    yield test_db
    
    # Limpiar después del test
    if os.path.exists(db_path):
        os.unlink(db_path)

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
def setup_test_environment(monkeypatch, temp_db):
    """Configurar entorno de test automáticamente"""
    # Usar base de datos temporal
    monkeypatch.setattr('database.database.db', temp_db)
    monkeypatch.setattr('database.models.db', temp_db)
    
    # Crear directorio temporal para assets
    test_assets_dir = tempfile.mkdtemp()
    monkeypatch.setattr('os.makedirs', lambda path, exist_ok=True: None)
    
    yield
    
    # Limpiar directorio temporal
    import shutil
    if os.path.exists(test_assets_dir):
        shutil.rmtree(test_assets_dir, ignore_errors=True)

@pytest.fixture
def mock_messagebox(mocker):
    """Mock para tkinter.messagebox"""
    return mocker.patch('tkinter.messagebox')

@pytest.fixture
def mock_filedialog(mocker):
    """Mock para tkinter.filedialog"""
    return mocker.patch('tkinter.filedialog')
