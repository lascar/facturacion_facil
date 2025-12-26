# -*- coding: utf-8 -*-
"""
Service métier pour la gestion des produits
Sépare la logique métier de la présentation UI
"""

from typing import Optional, List, Dict, Any
from services.base_service import BaseService
from utils.decorators import log_execution, log_performance
from utils.exceptions import (
    ProductValidationError, ProductNotFoundError,
    DatabaseError, InsufficientStockError
)


class ProductoService(BaseService):
    """Service métier pour les produits"""
    
    @log_execution
    @log_performance(threshold_seconds=0.5)
    def get_all_productos(self) -> List[Dict[str, Any]]:
        """
        Obtenir tous les produits
        
        Returns:
            Liste de dictionnaires de produits
            
        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            return self.db.get_all_products()
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo productos",
                details={'error': str(e)}
            )
    
    @log_execution
    def get_producto_by_id(self, producto_id: int) -> Dict[str, Any]:
        """
        Obtenir un produit par son ID
        
        Args:
            producto_id: ID du produit
            
        Returns:
            Dictionnaire du produit
            
        Raises:
            ProductNotFoundError: Si le produit n'existe pas
            DatabaseError: En cas d'erreur de base de données
        """
        self.validate_id(producto_id, 'producto', ProductValidationError)
        
        try:
            producto = self.db.get_product_by_id(producto_id)
            if not producto:
                raise ProductNotFoundError(producto_id)
            return producto
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo producto {producto_id}",
                details={'id': producto_id, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def create_producto(self, producto_data: Dict[str, Any]) -> int:
        """
        Créer un nouveau produit
        
        Args:
            producto_data: Données du produit
            
        Returns:
            ID du produit créé
            
        Raises:
            ProductValidationError: Si les données sont invalides
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self._validate_producto_data(producto_data)
        
        try:
            producto_id = self.db.add_product(producto_data)
            self.logger.info(f"Producto creado con ID: {producto_id}")
            return producto_id
        except Exception as e:
            raise DatabaseError(
                f"Error creando producto",
                details={'data': producto_data, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def update_producto(self, producto_data: Dict[str, Any]) -> bool:
        """
        Mettre à jour un produit existant
        
        Args:
            producto_data: Données du produit (doit contenir 'id')
            
        Returns:
            True si la mise à jour a réussi
            
        Raises:
            ProductValidationError: Si les données sont invalides
            ProductNotFoundError: Si le produit n'existe pas
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        if 'id' not in producto_data:
            raise ProductValidationError(
                "ID de producto requerido para actualización",
                details={'data': producto_data}
            )
        
        self.validate_id(producto_data['id'], 'producto', ProductValidationError)
        self._validate_producto_data(producto_data)

        # Ajouter les champs requis par la base de données avec des valeurs par défaut
        producto_data.setdefault('referencia', '')
        producto_data.setdefault('categoria', '')
        producto_data.setdefault('descripcion', '')
        producto_data.setdefault('iva_recomendado', 21.0)

        try:
            success = self.db.update_product(producto_data)
            if not success:
                raise ProductNotFoundError(producto_data['id'])
            self.logger.info(f"Producto {producto_data['id']} actualizado")
            return True
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error actualizando producto {producto_data.get('id')}",
                details={'data': producto_data, 'error': str(e)}
            )
    
    @log_execution
    def delete_producto(self, producto_id: int) -> bool:
        """
        Supprimer un produit

        Args:
            producto_id: ID du produit à supprimer

        Returns:
            True si la suppression a réussi

        Raises:
            ProductValidationError: Si l'ID est invalide
            DatabaseError: En cas d'erreur de base de données
        """
        self.validate_id(producto_id, 'producto', ProductValidationError)

        try:
            self.db.delete_product(producto_id)
            self.logger.info(f"Producto {producto_id} eliminado")
            return True
        except Exception as e:
            raise DatabaseError(
                f"Error eliminando producto {producto_id}",
                details={'id': producto_id, 'error': str(e)}
            )

    def _validate_producto_data(self, data: Dict[str, Any]) -> None:
        """
        Valider les données d'un produit

        Args:
            data: Données du produit à valider

        Raises:
            ProductValidationError: Si les données sont invalides
        """
        # Champs requis
        required_fields = ['nombre']
        self.validate_required_fields(data, required_fields, ProductValidationError)

        # Validation du prix
        if 'precio_venta' in data:
            self.validate_positive_number(
                data['precio_venta'],
                'precio_venta',
                ProductValidationError
            )

        # Validation de l'IVA
        if 'iva_recomendado' in data:
            try:
                iva = float(data['iva_recomendado'])
                if iva < 0 or iva > 100:
                    raise ProductValidationError(
                        "IVA debe estar entre 0 y 100",
                        details={'iva': iva}
                    )
            except (ValueError, TypeError):
                raise ProductValidationError(
                    "IVA debe ser un número válido",
                    details={'iva': data['iva_recomendado']}
                )

        # Validation du stock
        if 'stock' in data:
            try:
                stock = int(data['stock'])
                if stock < 0:
                    raise ProductValidationError(
                        "Stock no puede ser negativo",
                        details={'stock': stock}
                    )
            except (ValueError, TypeError):
                raise ProductValidationError(
                    "Stock debe ser un número entero válido",
                    details={'stock': data['stock']}
                )

