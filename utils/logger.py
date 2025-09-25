"""
Sistema de logging para la aplicación Facturación Fácil
"""
import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

class AppLogger:
    """Clase para manejar el logging de la aplicación"""
    
    def __init__(self, app_name="facturacion_facil"):
        self.app_name = app_name
        self.log_dir = "logs"
        self.setup_logging()
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        # Crear directorio de logs si no existe
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configurar el logger principal
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicar handlers si ya existen
        if self.logger.handlers:
            return
        
        # Formato de logs
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para archivo principal (rotativo)
        main_log_file = os.path.join(self.log_dir, f"{self.app_name}.log")
        file_handler = RotatingFileHandler(
            main_log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Handler para errores (archivo separado)
        error_log_file = os.path.join(self.log_dir, f"{self.app_name}_errors.log")
        error_handler = RotatingFileHandler(
            error_log_file,
            maxBytes=2*1024*1024,  # 2MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        
        # Handler para consola (solo INFO y superior)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # Añadir handlers al logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
        
        # Log de inicio
        self.logger.info(f"=== Iniciando {self.app_name} ===")
        self.logger.info(f"Directorio de logs: {os.path.abspath(self.log_dir)}")
    
    def get_logger(self, module_name=None):
        """Obtiene un logger para un módulo específico"""
        if module_name:
            return logging.getLogger(f"{self.app_name}.{module_name}")
        return self.logger
    
    def log_startup_info(self):
        """Log información de inicio de la aplicación"""
        self.logger.info(f"Python version: {sys.version}")
        self.logger.info(f"Directorio de trabajo: {os.getcwd()}")
        self.logger.info(f"Argumentos: {sys.argv}")
    
    def log_exception(self, exception, context=""):
        """Log una excepción con contexto"""
        self.logger.error(f"Excepción en {context}: {str(exception)}", exc_info=True)
    
    def log_user_action(self, action, details=""):
        """Log una acción del usuario"""
        self.logger.info(f"Acción usuario: {action} - {details}")
    
    def log_database_operation(self, operation, table="", details=""):
        """Log una operación de base de datos"""
        self.logger.debug(f"DB {operation} en {table}: {details}")
    
    def log_file_operation(self, operation, file_path="", details=""):
        """Log una operación de archivo"""
        self.logger.debug(f"Archivo {operation}: {file_path} - {details}")
    
    def create_session_log(self):
        """Crea un log específico para la sesión actual"""
        session_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_log_file = os.path.join(self.log_dir, f"session_{session_time}.log")
        
        session_handler = logging.FileHandler(session_log_file, encoding='utf-8')
        session_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        session_handler.setFormatter(formatter)
        
        session_logger = logging.getLogger(f"{self.app_name}.session")
        session_logger.addHandler(session_handler)
        session_logger.setLevel(logging.DEBUG)
        
        session_logger.info(f"=== Nueva sesión iniciada: {session_time} ===")
        return session_logger

# Instancia global del logger
app_logger = AppLogger()

# Funciones de conveniencia
def get_logger(module_name=None):
    """Función de conveniencia para obtener un logger"""
    return app_logger.get_logger(module_name)

def log_info(message, module_name=None):
    """Log un mensaje de información"""
    logger = get_logger(module_name)
    logger.info(message)

def log_error(message, module_name=None, exception=None):
    """Log un mensaje de error"""
    logger = get_logger(module_name)
    if exception:
        logger.error(f"{message}: {str(exception)}", exc_info=True)
    else:
        logger.error(message)

def log_warning(message, module_name=None):
    """Log un mensaje de advertencia"""
    logger = get_logger(module_name)
    logger.warning(message)

def log_debug(message, module_name=None):
    """Log un mensaje de debug"""
    logger = get_logger(module_name)
    logger.debug(message)

def log_user_action(action, details=""):
    """Log una acción del usuario"""
    app_logger.log_user_action(action, details)

def log_database_operation(operation, table="", details=""):
    """Log una operación de base de datos"""
    app_logger.log_database_operation(operation, table, details)

def log_file_operation(operation, file_path="", details=""):
    """Log una operación de archivo"""
    app_logger.log_file_operation(operation, file_path, details)

def log_exception(exception, context=""):
    """Log una excepción con contexto"""
    app_logger.log_exception(exception, context)

# Configurar logging para módulos específicos
def setup_module_logger(module_name, level=logging.INFO):
    """Configura un logger específico para un módulo"""
    logger = logging.getLogger(f"facturacion_facil.{module_name}")
    logger.setLevel(level)
    return logger
