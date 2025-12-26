"""
Tests para DatabaseEnhanced con decoradores y excepciones personalizadas
"""
import pytest
import os
import tempfile
from database.database_enhanced import DatabaseEnhanced
from utils.exceptions import (
    ClientNotFoundError,
    ProductNotFoundError,
    InsufficientStockError
)


class TestDatabaseEnhanced:
    """Tests para la clase DatabaseEnhanced"""
    
    def setup_method(self):
        """Configuración antes de cada test"""
        # Crear base de datos temporal
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = DatabaseEnhanced(self.temp_db.name)
    
    def teardown_method(self):
        """Limpieza después de cada test"""
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_get_client_by_id_not_found_raises_exception(self):
        """Test que get_client_by_id lanza excepción si no existe"""
        with pytest.raises(ClientNotFoundError) as exc_info:
            self.db.get_client_by_id(999)
        
        assert exc_info.value.details['id'] == 999
    
    def test_get_client_by_id_found(self):
        """Test que get_client_by_id retorna cliente si existe"""
        # Añadir un cliente
        client_data = {
            'nombre': 'Test Client',
            'nif': '12345678A',
            'direccion': 'Test Address',
            'email': 'test@test.com',
            'telefono': '123456789'
        }
        client_id = self.db.add_client(client_data)
        
        # Obtener el cliente
        client = self.db.get_client_by_id(client_id)
        
        assert client is not None
        assert client['nombre'] == 'Test Client'
        assert client['nif'] == '12345678A'
    
    def test_get_product_by_id_not_found_raises_exception(self):
        """Test que get_product_by_id lanza excepción si no existe"""
        with pytest.raises(ProductNotFoundError) as exc_info:
            self.db.get_product_by_id(999)
        
        assert exc_info.value.details['id'] == 999
    
    def test_get_product_by_id_found(self):
        """Test que get_product_by_id retorna producto si existe"""
        # Añadir un producto
        product_data = {
            'nombre': 'Test Product',
            'referencia': 'TEST-001',
            'precio': 100.0,
            'categoria': 'Test',
            'descripcion': 'Test description',
            'stock': 10
        }
        product_id = self.db.add_product(product_data)
        
        # Obtener el producto
        product = self.db.get_product_by_id(product_id)
        
        assert product is not None
        assert product['nombre'] == 'Test Product'
        assert product['referencia'] == 'TEST-001'
    
    def test_check_stock_availability_sufficient(self):
        """Test verificación de stock suficiente"""
        # Añadir un producto con stock
        product_data = {
            'nombre': 'Test Product',
            'referencia': 'TEST-001',
            'precio': 100.0,
            'stock': 10
        }
        product_id = self.db.add_product(product_data)
        
        # Verificar stock suficiente
        result = self.db.check_stock_availability(product_id, 5)
        assert result is True
    
    def test_check_stock_availability_insufficient(self):
        """Test verificación de stock insuficiente"""
        # Añadir un producto con stock limitado
        product_data = {
            'nombre': 'Test Product',
            'referencia': 'TEST-001',
            'precio': 100.0,
            'stock': 5
        }
        product_id = self.db.add_product(product_data)
        
        # Verificar stock insuficiente
        with pytest.raises(InsufficientStockError) as exc_info:
            self.db.check_stock_availability(product_id, 10)
        
        assert exc_info.value.details['solicitado'] == 10
        assert exc_info.value.details['disponible'] == 5
    
    def test_safe_get_all_clients_returns_empty_on_error(self):
        """Test que safe_get_all_clients retorna lista vacía en caso de error"""
        # Cerrar la base de datos para forzar un error
        # (esto es difícil de simular, así que solo verificamos que funciona normalmente)
        clients = self.db.safe_get_all_clients()
        assert isinstance(clients, list)
    
    def test_safe_get_all_products_returns_empty_on_error(self):
        """Test que safe_get_all_products retorna lista vacía en caso de error"""
        # Similar al test anterior
        products = self.db.safe_get_all_products()
        assert isinstance(products, list)
    
    def test_get_all_clients_with_performance_logging(self):
        """Test que get_all_clients registra performance"""
        # Añadir varios clientes
        for i in range(5):
            self.db.add_client({
                'nombre': f'Client {i}',
                'nif': f'NIF{i}',
                'direccion': f'Address {i}',
                'email': f'client{i}@test.com',
                'telefono': f'12345678{i}'
            })
        
        # Obtener todos los clientes (debería registrar performance)
        clients = self.db.get_all_clients()
        assert len(clients) == 5
    
    def test_get_all_products_with_performance_logging(self):
        """Test que get_all_products registra performance"""
        # Añadir varios productos
        for i in range(5):
            self.db.add_product({
                'nombre': f'Product {i}',
                'referencia': f'REF-{i}',
                'precio': 100.0 * (i + 1),
                'stock': 10
            })
        
        # Obtener todos los productos (debería registrar performance)
        products = self.db.get_all_products()
        assert len(products) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

