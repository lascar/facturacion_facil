# -*- coding: utf-8 -*-
"""
Service de gestion du stock
Encapsule la logique métier liée au stock des produits
"""

from typing import List, Dict, Any, Optional
from utils.decorators import log_execution, log_performance
from utils.exceptions import (
    ProductValidationError,
    ProductNotFoundError,
    DatabaseError
)
from services.base_service import BaseService


class StockService(BaseService):
    """Service de gestion du stock des produits"""
    
    @log_execution
    @log_performance(threshold_seconds=0.5)
    def get_all_stock(self) -> List[Dict[str, Any]]:
        """
        Récupérer tous les produits avec leurs informations de stock
        
        Returns:
            Liste de dictionnaires représentant les produits avec stock
            
        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            productos = self.db.get_all_products()
            return productos
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo stock",
                details={'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def get_stock_by_product_id(self, producto_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupérer le stock d'un produit spécifique
        
        Args:
            producto_id: ID du produit
            
        Returns:
            Dictionnaire avec les informations du produit et son stock, ou None si non trouvé
            
        Raises:
            ProductValidationError: Si l'ID est invalide
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self.validate_id(producto_id, 'producto', ProductValidationError)
        
        try:
            producto = self.db.get_product_by_id(producto_id)
            return producto
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo stock del producto {producto_id}",
                details={'producto_id': producto_id, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def update_stock(self, producto_id: int, nuevo_stock: int) -> bool:
        """
        Mettre à jour le stock d'un produit
        
        Args:
            producto_id: ID du produit
            nuevo_stock: Nouveau stock (doit être >= 0)
            
        Returns:
            True si la mise à jour a réussi
            
        Raises:
            ProductValidationError: Si les données sont invalides
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self.validate_id(producto_id, 'producto', ProductValidationError)
        
        if nuevo_stock < 0:
            raise ProductValidationError(
                "El stock no puede ser negativo",
                details={'producto_id': producto_id, 'nuevo_stock': nuevo_stock}
            )
        
        try:
            success = self.db.update_product_stock(producto_id, nuevo_stock)
            return success
        except Exception as e:
            raise DatabaseError(
                f"Error actualizando stock del producto {producto_id}",
                details={'producto_id': producto_id, 'nuevo_stock': nuevo_stock, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def adjust_stock(self, producto_id: int, ajuste: int) -> bool:
        """
        Ajuster le stock d'un produit (+ ou -)
        
        Args:
            producto_id: ID du produit
            ajuste: Ajustement à appliquer (peut être négatif)
            
        Returns:
            True si l'ajustement a réussi
            
        Raises:
            ProductValidationError: Si les données sont invalides
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self.validate_id(producto_id, 'producto', ProductValidationError)
        
        try:
            success = self.db.adjust_product_stock(producto_id, ajuste)
            return success
        except Exception as e:
            raise DatabaseError(
                f"Error ajustando stock del producto {producto_id}",
                details={'producto_id': producto_id, 'ajuste': ajuste, 'error': str(e)}
            )
    
    # Note: update_stock_minimo() sera implémenté plus tard quand la table stock
    # aura une colonne stock_minimo

