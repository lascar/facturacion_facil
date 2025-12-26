"""
Tests para las excepciones personalizadas
"""
import pytest
from utils.exceptions import (
    FacturacionError,
    DatabaseError,
    DatabaseConnectionError,
    ValidationError,
    ClientValidationError,
    InsufficientStockError,
    DuplicateInvoiceNumberError,
    ClientNotFoundError,
    ProductNotFoundError,
    MissingConfigurationError
)


class TestFacturacionError:
    """Tests para la excepción base"""
    
    def test_basic_error(self):
        """Test excepción básica sin detalles"""
        error = FacturacionError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {}
    
    def test_error_with_details(self):
        """Test excepción con detalles"""
        error = FacturacionError("Test error", {'key': 'value', 'num': 42})
        assert "Test error" in str(error)
        assert "key=value" in str(error)
        assert "num=42" in str(error)


class TestDatabaseErrors:
    """Tests para errores de base de datos"""
    
    def test_database_error(self):
        """Test error genérico de base de datos"""
        error = DatabaseError("DB error")
        assert isinstance(error, FacturacionError)
        assert str(error) == "DB error"
    
    def test_database_connection_error(self):
        """Test error de conexión"""
        error = DatabaseConnectionError("Connection failed")
        assert isinstance(error, DatabaseError)
        assert str(error) == "Connection failed"


class TestValidationErrors:
    """Tests para errores de validación"""
    
    def test_validation_error(self):
        """Test error genérico de validación"""
        error = ValidationError("Invalid data")
        assert isinstance(error, FacturacionError)
        assert str(error) == "Invalid data"
    
    def test_client_validation_error(self):
        """Test error de validación de cliente"""
        error = ClientValidationError("Invalid client")
        assert isinstance(error, ValidationError)
        assert str(error) == "Invalid client"


class TestBusinessLogicErrors:
    """Tests para errores de lógica de negocio"""
    
    def test_insufficient_stock_error(self):
        """Test error de stock insuficiente"""
        error = InsufficientStockError("Producto A", requested=10, available=5)
        
        assert "Producto A" in str(error)
        assert error.details['producto'] == "Producto A"
        assert error.details['solicitado'] == 10
        assert error.details['disponible'] == 5
    
    def test_duplicate_invoice_number_error(self):
        """Test error de número de factura duplicado"""
        error = DuplicateInvoiceNumberError("FAC-001")
        
        assert "FAC-001" in str(error)
        assert error.details['numero_factura'] == "FAC-001"


class TestDataNotFoundErrors:
    """Tests para errores de datos no encontrados"""
    
    def test_client_not_found_error(self):
        """Test error de cliente no encontrado"""
        error = ClientNotFoundError(123)
        
        assert "Cliente" in str(error)
        assert error.details['tipo'] == "Cliente"
        assert error.details['id'] == 123
    
    def test_product_not_found_error(self):
        """Test error de producto no encontrado"""
        error = ProductNotFoundError(456)
        
        assert "Producto" in str(error)
        assert error.details['tipo'] == "Producto"
        assert error.details['id'] == 456


class TestConfigurationErrors:
    """Tests para errores de configuración"""
    
    def test_missing_configuration_error(self):
        """Test error de configuración faltante"""
        error = MissingConfigurationError("database_path")
        
        assert "database_path" in str(error)
        assert error.details['clave'] == "database_path"


class TestErrorHierarchy:
    """Tests para la jerarquía de excepciones"""
    
    def test_all_errors_inherit_from_base(self):
        """Test que todas las excepciones heredan de FacturacionError"""
        errors = [
            DatabaseError("test"),
            ValidationError("test"),
            ClientValidationError("test"),
            InsufficientStockError("prod", 1, 0),
            ClientNotFoundError(1)
        ]
        
        for error in errors:
            assert isinstance(error, FacturacionError)
    
    def test_specific_errors_inherit_correctly(self):
        """Test que las excepciones específicas heredan correctamente"""
        assert isinstance(DatabaseConnectionError("test"), DatabaseError)
        assert isinstance(ClientValidationError("test"), ValidationError)
        assert isinstance(InsufficientStockError("p", 1, 0), FacturacionError)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

