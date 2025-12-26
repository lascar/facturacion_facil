# -*- coding: utf-8 -*-
"""
Classe de base pour tous les services métier
Fournit des fonctionnalités communes : logging, gestion d'erreurs, accès DB
"""

from utils.decorators import log_execution, log_performance, retry_on_error, handle_exceptions
from utils.exceptions import DatabaseError, DatabaseConnectionError
from utils.logger import get_logger
from database.database import Database
from typing import Optional, Any, Dict, List


class BaseService:
    """
    Classe de base pour tous les services métier
    
    Fournit :
    - Accès à la base de données avec retry automatique
    - Logging standardisé
    - Gestion d'erreurs robuste
    - Méthodes utilitaires communes
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialiser le service
        
        Args:
            db_path: Chemin vers la base de données (optionnel)
        """
        self.db = Database(db_path) if db_path else Database()
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"{self.__class__.__name__} initialisé")
    
    @retry_on_error(max_attempts=3, delay_seconds=0.5)
    def get_connection(self):
        """
        Obtenir une connexion à la base de données avec retry automatique
        
        Returns:
            Connection SQLite
            
        Raises:
            DatabaseConnectionError: Si impossible de se connecter après 3 tentatives
        """
        try:
            return self.db.get_connection()
        except Exception as e:
            raise DatabaseConnectionError(
                f"Impossible de se connecter à la base de données",
                details={'error': str(e), 'service': self.__class__.__name__}
            )
    
    @handle_exceptions(default_return=None, log_traceback=True)
    def safe_execute(self, func, *args, **kwargs):
        """
        Exécuter une fonction de manière sécurisée
        
        Args:
            func: Fonction à exécuter
            *args: Arguments positionnels
            **kwargs: Arguments nommés
            
        Returns:
            Résultat de la fonction ou None en cas d'erreur
        """
        return func(*args, **kwargs)
    
    def validate_required_fields(self, data: Dict[str, Any], required_fields: List[str], error_class):
        """
        Valider que tous les champs requis sont présents
        
        Args:
            data: Dictionnaire de données à valider
            required_fields: Liste des champs requis
            error_class: Classe d'exception à lever en cas d'erreur
            
        Raises:
            error_class: Si un champ requis est manquant
        """
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            raise error_class(
                f"Campos requeridos faltantes: {', '.join(missing_fields)}",
                details={'missing_fields': missing_fields, 'data': data}
            )
    
    def validate_positive_number(self, value: Any, field_name: str, error_class):
        """
        Valider qu'une valeur est un nombre positif
        
        Args:
            value: Valeur à valider
            field_name: Nom du champ (pour le message d'erreur)
            error_class: Classe d'exception à lever
            
        Raises:
            error_class: Si la valeur n'est pas un nombre positif
        """
        try:
            num_value = float(value)
            if num_value < 0:
                raise error_class(
                    f"{field_name} debe ser un número positivo",
                    details={'field': field_name, 'value': value}
                )
        except (ValueError, TypeError):
            raise error_class(
                f"{field_name} debe ser un número válido",
                details={'field': field_name, 'value': value}
            )
    
    def validate_id(self, id_value: Any, entity_name: str, error_class):
        """
        Valider qu'un ID est valide (entier positif)
        
        Args:
            id_value: ID à valider
            entity_name: Nom de l'entité (pour le message d'erreur)
            error_class: Classe d'exception à lever
            
        Raises:
            error_class: Si l'ID n'est pas valide
        """
        try:
            int_id = int(id_value)
            if int_id <= 0:
                raise error_class(
                    f"ID de {entity_name} inválido: debe ser > 0",
                    details={'entity': entity_name, 'id': id_value}
                )
        except (ValueError, TypeError):
            raise error_class(
                f"ID de {entity_name} inválido: debe ser un número entero",
                details={'entity': entity_name, 'id': id_value}
            )
    
    @log_performance(threshold_seconds=1.0)
    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = True):
        """
        Exécuter une requête SQL avec logging de performance
        
        Args:
            query: Requête SQL
            params: Paramètres de la requête
            fetch_one: Si True, retourne une seule ligne
            fetch_all: Si True, retourne toutes les lignes
            
        Returns:
            Résultat de la requête ou None
            
        Raises:
            DatabaseError: En cas d'erreur SQL
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                result = None
            
            conn.close()
            return result
            
        except Exception as e:
            raise DatabaseError(
                f"Error ejecutando consulta SQL",
                details={'query': query, 'params': params, 'error': str(e)}
            )

