"""
Versión mejorada de Database con decoradores y excepciones personalizadas
Este archivo demuestra cómo usar los nuevos decoradores y excepciones
"""
import sqlite3
from typing import Optional, List, Dict, Any
from database.database import Database
from utils.decorators import log_performance, retry_on_error, handle_exceptions
from utils.exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
    ClientNotFoundError,
    ProductNotFoundError,
    InsufficientStockError
)
from utils.logger import get_logger


class DatabaseEnhanced(Database):
    """
    Versión mejorada de Database con mejor manejo de errores y logging
    """
    
    def __init__(self, db_path="base_de_datos/facturacion.db"):
        self.logger = get_logger("database_enhanced")
        super().__init__(db_path)
    
    @retry_on_error(max_attempts=3, delay_seconds=0.5)
    def get_connection(self):
        """Obtiene una conexión a la base de datos con retry automático"""
        try:
            return super().get_connection()
        except Exception as e:
            raise DatabaseConnectionError(
                f"No se pudo conectar a la base de datos después de varios intentos",
                {'db_path': self.db_path, 'error': str(e)}
            )
    
    @log_performance(threshold_seconds=0.1)
    def get_client_by_id(self, client_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un cliente por su ID con logging de performance
        
        Args:
            client_id: ID del cliente
            
        Returns:
            Diccionario con datos del cliente o None si no existe
            
        Raises:
            ClientNotFoundError: Si el cliente no existe
        """
        client = super().get_client_by_id(client_id)
        
        if client is None:
            raise ClientNotFoundError(client_id)
        
        return client
    
    @log_performance(threshold_seconds=0.1)
    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene un producto por su ID con logging de performance
        
        Args:
            product_id: ID del producto
            
        Returns:
            Diccionario con datos del producto o None si no existe
            
        Raises:
            ProductNotFoundError: Si el producto no existe
        """
        product = super().get_product_by_id(product_id)
        
        if product is None:
            raise ProductNotFoundError(product_id)
        
        return product
    
    @log_performance(threshold_seconds=0.2)
    def get_all_clients(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los clientes con logging de performance
        
        Returns:
            Lista de diccionarios con datos de clientes
        """
        return super().get_all_clients()
    
    @log_performance(threshold_seconds=0.2)
    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los productos con logging de performance
        
        Returns:
            Lista de diccionarios con datos de productos
        """
        return super().get_all_products()
    
    def get_product_stock(self, product_id: int) -> int:
        """
        Obtiene el stock actual de un producto desde la tabla stock

        Args:
            product_id: ID del producto

        Returns:
            Cantidad de stock disponible
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id=?", (product_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            self.logger.error(f"Error obteniendo stock del producto {product_id}: {e}")
            return 0

    def check_stock_availability(self, product_id: int, quantity: int) -> bool:
        """
        Verifica si hay stock suficiente para un producto

        Args:
            product_id: ID del producto
            quantity: Cantidad solicitada

        Returns:
            True si hay stock suficiente

        Raises:
            ProductNotFoundError: Si el producto no existe
            InsufficientStockError: Si no hay stock suficiente
        """
        product = self.get_product_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(product_id)

        # Obtener stock desde la tabla stock
        available_stock = self.get_product_stock(product_id)

        if available_stock < quantity:
            raise InsufficientStockError(
                product_name=product.get('nombre', 'Desconocido'),
                requested=quantity,
                available=available_stock
            )

        return True
    
    @handle_exceptions(default_return=[], log_traceback=True)
    def safe_get_all_clients(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los clientes de forma segura (no lanza excepciones)
        
        Returns:
            Lista de clientes o lista vacía en caso de error
        """
        return self.get_all_clients()
    
    @handle_exceptions(default_return=[], log_traceback=True)
    def safe_get_all_products(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los productos de forma segura (no lanza excepciones)
        
        Returns:
            Lista de productos o lista vacía en caso de error
        """
        return self.get_all_products()

