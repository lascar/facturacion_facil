# -*- coding: utf-8 -*-
"""
Service métier pour la gestion de l'organisation
Sépare la logique métier de la présentation UI
"""

from typing import Optional, Dict, Any
from services.base_service import BaseService
from utils.decorators import log_execution, log_performance
from utils.exceptions import (
    OrganizationValidationError, OrganizationNotFoundError,
    DatabaseError
)


class OrganizacionService(BaseService):
    """Service métier pour l'organisation"""
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def get_organizacion(self) -> Optional[Dict[str, Any]]:
        """
        Obtenir les données de l'organisation
        
        Returns:
            Dictionnaire de l'organisation ou None si elle n'existe pas
            
        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            return self.db.get_organization_info()
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo organización",
                details={'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def create_organizacion(self, org_data: Dict[str, Any]) -> bool:
        """
        Créer l'organisation
        
        Args:
            org_data: Données de l'organisation
            
        Returns:
            True si la création a réussi
            
        Raises:
            OrganizationValidationError: Si les données sont invalides
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self._validate_organizacion_data(org_data)
        
        try:
            self.db.create_organization(org_data)
            self.logger.info("Organización creada")
            return True
        except Exception as e:
            raise DatabaseError(
                f"Error creando organización",
                details={'data': org_data, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.3)
    def update_organizacion(self, org_data: Dict[str, Any]) -> bool:
        """
        Mettre à jour l'organisation
        
        Args:
            org_data: Données de l'organisation (doit contenir 'id')
            
        Returns:
            True si la mise à jour a réussi
            
        Raises:
            OrganizationValidationError: Si les données sont invalides
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self._validate_organizacion_data(org_data)
        
        # Vérifier si l'organisation existe
        existing = self.get_organizacion()
        
        try:
            if existing and existing.get('id'):
                # Mise à jour
                org_data['id'] = existing['id']
                success = self.db.update_organization(org_data)
                if not success:
                    raise OrganizationNotFoundError(existing['id'])
                self.logger.info("Organización actualizada")
            else:
                # Création si elle n'existe pas
                self.db.create_organization(org_data)
                self.logger.info("Organización creada (no existía)")

            return True
        except OrganizationNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error actualizando organización",
                details={'data': org_data, 'error': str(e)}
            )
    
    def _validate_organizacion_data(self, data: Dict[str, Any]) -> None:
        """
        Valider les données de l'organisation
        
        Args:
            data: Données de l'organisation à valider
            
        Raises:
            OrganizationValidationError: Si les données sont invalides
        """
        # Champs requis
        required_fields = ['nombre']
        self.validate_required_fields(data, required_fields, OrganizationValidationError)
        
        # Validation du CIF (si fourni)
        if data.get('cif'):
            cif = data['cif'].strip()
            if cif and len(cif) < 9:
                raise OrganizationValidationError(
                    "CIF debe tener al menos 9 caracteres",
                    details={'cif': cif}
                )
        
        # Validation de l'email (si fourni)
        if data.get('email'):
            email = data['email'].strip()
            if email and '@' not in email:
                raise OrganizationValidationError(
                    "Email inválido",
                    details={'email': email}
                )
        
        # Validation du numéro de facture initial (si fourni)
        if 'numero_factura_inicial' in data and data['numero_factura_inicial'] is not None:
            numero_inicial = str(data['numero_factura_inicial']).strip()

            # Vérifier que ce n'est pas vide
            if len(numero_inicial) == 0:
                raise OrganizationValidationError(
                    "Número de factura inicial no puede estar vacío",
                    details={'numero': data['numero_factura_inicial']}
                )

            # Vérifier la longueur maximale
            if len(numero_inicial) > 50:
                raise OrganizationValidationError(
                    "Número de factura inicial es demasiado largo (máximo 50 caracteres)",
                    details={'numero': numero_inicial}
                )

            # Vérifier qu'il contient au moins un caractère alphanumérique
            if not any(c.isalnum() for c in numero_inicial):
                raise OrganizationValidationError(
                    "Número de factura inicial debe contener al menos un número o letra",
                    details={'numero': numero_inicial}
                )

