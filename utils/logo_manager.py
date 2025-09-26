"""
Gestionnaire de logos pour l'organisation
Gère la copie et la persistance des logos dans un répertoire permanent
"""

from utils.file_manager import ImageFileManager
from utils.logger import get_logger

class LogoManager:
    """Gestionnaire pour les logos de l'organisation - Version simplifiée"""

    def __init__(self):
        self.logger = get_logger("logo_manager")
        self.file_manager = ImageFileManager(subdirectory="logos")
    
    @property
    def logo_directory(self):
        """Répertoire pour stocker les logos de façon permanente"""
        return self.file_manager.storage_directory
    
    def save_logo(self, source_path, organization_name="organization"):
        """
        Copie un logo vers le répertoire permanent de l'application

        Args:
            source_path (str): Chemin vers le fichier logo source
            organization_name (str): Nom de l'organisation (pour nommage)

        Returns:
            str: Chemin vers le logo copié, ou None si erreur
        """
        name_prefix = f"{self.file_manager.clean_filename(organization_name)}_logo"
        return self.file_manager.save_file(source_path, name_prefix)

    def remove_logo(self, logo_path):
        """
        Supprimer un logo du répertoire permanent

        Args:
            logo_path (str): Chemin vers le logo à supprimer

        Returns:
            bool: True si suppression réussie
        """
        return self.file_manager.remove_file(logo_path)
    
    def update_logo(self, old_logo_path, new_source_path, organization_name="organization"):
        """
        Mettre à jour un logo (supprimer l'ancien, copier le nouveau)

        Args:
            old_logo_path (str): Chemin vers l'ancien logo
            new_source_path (str): Chemin vers le nouveau logo source
            organization_name (str): Nom de l'organisation

        Returns:
            str: Chemin vers le nouveau logo, ou None si erreur
        """
        name_prefix = f"{self.file_manager.clean_filename(organization_name)}_logo"
        return self.file_manager.update_file(old_logo_path, new_source_path, name_prefix)
    
    def get_logo_info(self, logo_path):
        """
        Obtenir des informations sur un logo

        Args:
            logo_path (str): Chemin vers le logo

        Returns:
            dict: Informations sur le logo
        """
        return self.file_manager.get_image_info(logo_path)
    
    def list_logos(self):
        """
        Lister tous les logos dans le répertoire

        Returns:
            list: Liste des chemins vers les logos
        """
        return self.file_manager.list_images()
    
    def cleanup_orphaned_logos(self, current_logo_path=None):
        """
        Nettoyer les logos orphelins (non utilisés)

        Args:
            current_logo_path (str): Chemin du logo actuellement utilisé

        Returns:
            int: Nombre de logos supprimés
        """
        return self.file_manager.cleanup_orphaned_files(current_logo_path, keep_count=1)
