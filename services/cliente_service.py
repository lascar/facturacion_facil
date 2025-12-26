# -*- coding: utf-8 -*-
"""
Service métier pour la gestion des clients
Sépare la logique métier de la présentation UI
"""

from typing import Optional, List, Dict, Any
from services.base_service import BaseService
from utils.decorators import log_execution, log_performance
from utils.exceptions import (
    ClientValidationError, ClientNotFoundError,
    DatabaseError
)


class ClienteService(BaseService):
    """Service métier pour les clients"""
    
    @log_execution
    @log_performance(threshold_seconds=0.5)
    def get_all_clientes(self) -> List[Dict[str, Any]]:
        """
        Obtenir tous les clients
        
        Returns:
            Liste de dictionnaires de clients
            
        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            return self.db.get_all_clients()
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo clientes",
                details={'error': str(e)}
            )
    
    @log_execution
    def get_cliente_by_id(self, cliente_id: int) -> Dict[str, Any]:
        """
        Obtenir un client par son ID
        
        Args:
            cliente_id: ID du client
            
        Returns:
            Dictionnaire du client
            
        Raises:
            ClientNotFoundError: Si le client n'existe pas
            DatabaseError: En cas d'erreur de base de données
        """
        self.validate_id(cliente_id, 'cliente', ClientValidationError)
        
        try:
            cliente = self.db.get_client_by_id(cliente_id)
            if not cliente:
                raise ClientNotFoundError(cliente_id)
            return cliente
        except ClientNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo cliente {cliente_id}",
                details={'id': cliente_id, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def create_cliente(self, cliente_data: Dict[str, Any]) -> int:
        """
        Créer un nouveau client
        
        Args:
            cliente_data: Données du client
            
        Returns:
            ID du client créé
            
        Raises:
            ClientValidationError: Si les données sont invalides
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self._validate_cliente_data(cliente_data)
        
        try:
            cliente_id = self.db.add_client(cliente_data)
            self.logger.info(f"Cliente creado con ID: {cliente_id}")
            return cliente_id
        except Exception as e:
            raise DatabaseError(
                f"Error creando cliente",
                details={'data': cliente_data, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def update_cliente(self, cliente_data: Dict[str, Any]) -> bool:
        """
        Mettre à jour un client existant
        
        Args:
            cliente_data: Données du client (doit contenir 'id')
            
        Returns:
            True si la mise à jour a réussi
            
        Raises:
            ClientValidationError: Si les données sont invalides
            ClientNotFoundError: Si le client n'existe pas
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        if 'id' not in cliente_data:
            raise ClientValidationError(
                "ID de cliente requerido para actualización",
                details={'data': cliente_data}
            )
        
        self.validate_id(cliente_data['id'], 'cliente', ClientValidationError)
        self._validate_cliente_data(cliente_data)
        
        try:
            success = self.db.update_client(cliente_data)
            if not success:
                raise ClientNotFoundError(cliente_data['id'])
            self.logger.info(f"Cliente {cliente_data['id']} actualizado")
            return True
        except ClientNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error actualizando cliente {cliente_data.get('id')}",
                details={'data': cliente_data, 'error': str(e)}
            )
    
    @log_execution
    def delete_cliente(self, cliente_id: int) -> bool:
        """
        Supprimer un client

        Args:
            cliente_id: ID du client à supprimer

        Returns:
            True si la suppression a réussi

        Raises:
            ClientValidationError: Si l'ID est invalide
            DatabaseError: En cas d'erreur de base de données
        """
        self.validate_id(cliente_id, 'cliente', ClientValidationError)

        try:
            success = self.db.delete_client(cliente_id)
            self.logger.info(f"Cliente {cliente_id} eliminado")
            return success
        except Exception as e:
            raise DatabaseError(
                f"Error eliminando cliente {cliente_id}",
                details={'id': cliente_id, 'error': str(e)}
            )

    def _validate_cliente_data(self, data: Dict[str, Any]) -> None:
        """
        Valider les données d'un client

        Args:
            data: Données du client à valider

        Raises:
            ClientValidationError: Si les données sont invalides
        """
        # Champs requis
        required_fields = ['nombre']
        self.validate_required_fields(data, required_fields, ClientValidationError)

        # Validation de l'email (si fourni)
        if data.get('email'):
            email = data['email'].strip()
            if email and '@' not in email:
                raise ClientValidationError(
                    "Email inválido",
                    details={'email': email}
                )

