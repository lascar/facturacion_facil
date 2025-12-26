"""
Decoradores para logging, error handling y performance monitoring
"""
import functools
import time
from typing import Callable, Any
from utils.logger import get_logger, log_exception

logger = get_logger("decorators")


def log_execution(func: Callable) -> Callable:
    """
    Decorador que registra la ejecución de una función
    
    Args:
        func: Función a decorar
        
    Returns:
        Función decorada con logging
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = f"{func.__module__}.{func.__qualname__}"
        logger.debug(f"→ Ejecutando: {func_name}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"✓ Completado: {func_name}")
            return result
        except Exception as e:
            logger.error(f"✗ Error en {func_name}: {str(e)}")
            raise
    
    return wrapper


def log_performance(threshold_seconds: float = 0.1) -> Callable:
    """
    Decorador que registra el tiempo de ejecución de una función
    
    Args:
        threshold_seconds: Umbral en segundos para considerar una función lenta
        
    Returns:
        Decorador configurado
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__qualname__}"
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                if execution_time > threshold_seconds:
                    logger.warning(
                        f"⚠ Función lenta ({execution_time:.3f}s): {func_name}"
                    )
                else:
                    logger.debug(
                        f"⏱ Tiempo de ejecución ({execution_time:.3f}s): {func_name}"
                    )
                
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"✗ Error después de {execution_time:.3f}s en {func_name}: {str(e)}"
                )
                raise
        
        return wrapper
    return decorator


def retry_on_error(max_attempts: int = 3, delay_seconds: float = 1.0) -> Callable:
    """
    Decorador que reintenta una función en caso de error
    
    Args:
        max_attempts: Número máximo de intentos
        delay_seconds: Tiempo de espera entre intentos
        
    Returns:
        Decorador configurado
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__qualname__}"
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.error(
                            f"✗ Fallo definitivo después de {max_attempts} intentos en {func_name}: {str(e)}"
                        )
                        raise
                    else:
                        logger.warning(
                            f"⚠ Intento {attempt}/{max_attempts} falló en {func_name}: {str(e)}. "
                            f"Reintentando en {delay_seconds}s..."
                        )
                        time.sleep(delay_seconds)
        
        return wrapper
    return decorator


def handle_exceptions(default_return: Any = None, log_traceback: bool = True) -> Callable:
    """
    Decorador que captura excepciones y retorna un valor por defecto
    
    Args:
        default_return: Valor a retornar en caso de excepción
        log_traceback: Si se debe registrar el traceback completo
        
    Returns:
        Decorador configurado
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = f"{func.__module__}.{func.__qualname__}"
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_traceback:
                    log_exception(e, func_name)
                else:
                    logger.error(f"✗ Error en {func_name}: {str(e)}")
                
                return default_return
        
        return wrapper
    return decorator


def validate_params(**validators) -> Callable:
    """
    Decorador que valida los parámetros de una función
    
    Args:
        **validators: Diccionario de validadores {param_name: validator_func}
        
    Returns:
        Decorador configurado
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Obtener los nombres de los parámetros
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Validar cada parámetro
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ValueError(
                            f"Validación fallida para parámetro '{param_name}' "
                            f"con valor {value} en {func.__qualname__}"
                        )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

