"""
Tests para los decoradores de logging y error handling
"""
import pytest
import time
from utils.decorators import (
    log_execution,
    log_performance,
    retry_on_error,
    handle_exceptions,
    validate_params
)


class TestLogExecution:
    """Tests para el decorador log_execution"""
    
    def test_log_execution_success(self):
        """Test que el decorador registra ejecución exitosa"""
        @log_execution
        def sample_function():
            return "success"
        
        result = sample_function()
        assert result == "success"
    
    def test_log_execution_with_exception(self):
        """Test que el decorador registra excepciones"""
        @log_execution
        def failing_function():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            failing_function()


class TestLogPerformance:
    """Tests para el decorador log_performance"""
    
    def test_log_performance_fast_function(self):
        """Test función rápida no genera warning"""
        @log_performance(threshold_seconds=0.1)
        def fast_function():
            return "fast"
        
        result = fast_function()
        assert result == "fast"
    
    def test_log_performance_slow_function(self):
        """Test función lenta genera warning"""
        @log_performance(threshold_seconds=0.01)
        def slow_function():
            time.sleep(0.02)
            return "slow"
        
        result = slow_function()
        assert result == "slow"


class TestRetryOnError:
    """Tests para el decorador retry_on_error"""
    
    def test_retry_success_on_first_attempt(self):
        """Test función exitosa en primer intento"""
        @retry_on_error(max_attempts=3, delay_seconds=0.01)
        def successful_function():
            return "success"
        
        result = successful_function()
        assert result == "success"
    
    def test_retry_success_after_failures(self):
        """Test función exitosa después de fallos"""
        attempt_count = {'count': 0}
        
        @retry_on_error(max_attempts=3, delay_seconds=0.01)
        def eventually_successful():
            attempt_count['count'] += 1
            if attempt_count['count'] < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = eventually_successful()
        assert result == "success"
        assert attempt_count['count'] == 3
    
    def test_retry_fails_after_max_attempts(self):
        """Test función falla después de máximo de intentos"""
        @retry_on_error(max_attempts=2, delay_seconds=0.01)
        def always_failing():
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError, match="Always fails"):
            always_failing()


class TestHandleExceptions:
    """Tests para el decorador handle_exceptions"""
    
    def test_handle_exceptions_returns_default(self):
        """Test retorna valor por defecto en caso de excepción"""
        @handle_exceptions(default_return="default", log_traceback=False)
        def failing_function():
            raise ValueError("Error")
        
        result = failing_function()
        assert result == "default"
    
    def test_handle_exceptions_success(self):
        """Test retorna valor normal si no hay excepción"""
        @handle_exceptions(default_return="default")
        def successful_function():
            return "success"
        
        result = successful_function()
        assert result == "success"


class TestValidateParams:
    """Tests para el decorador validate_params"""
    
    def test_validate_params_success(self):
        """Test validación exitosa de parámetros"""
        @validate_params(
            x=lambda v: v > 0,
            y=lambda v: isinstance(v, str)
        )
        def sample_function(x, y):
            return f"{x}-{y}"
        
        result = sample_function(5, "test")
        assert result == "5-test"
    
    def test_validate_params_failure(self):
        """Test validación fallida de parámetros"""
        @validate_params(
            x=lambda v: v > 0
        )
        def sample_function(x):
            return x
        
        with pytest.raises(ValueError, match="Validación fallida"):
            sample_function(-1)
    
    def test_validate_params_with_defaults(self):
        """Test validación con valores por defecto"""
        @validate_params(
            x=lambda v: v > 0
        )
        def sample_function(x=10):
            return x
        
        result = sample_function()
        assert result == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

