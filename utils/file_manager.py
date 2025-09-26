"""
Gestionnaire de fichiers générique pour l'application
Fournit des fonctionnalités communes de gestion de fichiers
"""

import os
import shutil
import uuid
import re
from pathlib import Path
from PIL import Image
from utils.logger import get_logger

class FileManager:
    """Gestionnaire de fichiers générique avec fonctionnalités communes"""
    
    def __init__(self, base_directory="data", subdirectory="files"):
        """
        Initialiser le gestionnaire de fichiers
        
        Args:
            base_directory (str): Répertoire de base (ex: "data")
            subdirectory (str): Sous-répertoire (ex: "logos", "images", "documents")
        """
        self.logger = get_logger(f"file_manager_{subdirectory}")
        self.base_directory = base_directory
        self.subdirectory = subdirectory
        self._ensure_directory()
    
    @property
    def storage_directory(self):
        """Répertoire de stockage complet"""
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        storage_dir = os.path.join(app_dir, self.base_directory, self.subdirectory)
        return storage_dir
    
    def _ensure_directory(self):
        """Assurer que le répertoire de stockage existe"""
        try:
            os.makedirs(self.storage_directory, exist_ok=True)
            self.logger.debug(f"Répertoire: {self.storage_directory}")
        except Exception as e:
            self.logger.error(f"Erreur création répertoire: {e}")
    
    def save_file(self, source_path, name_prefix="file", file_extension=None):
        """
        Copier un fichier vers le répertoire de stockage
        
        Args:
            source_path (str): Chemin vers le fichier source
            name_prefix (str): Préfixe pour le nom de fichier
            file_extension (str): Extension forcée (optionnel)
            
        Returns:
            str: Chemin vers le fichier copié, ou None si erreur
        """
        try:
            if not self.file_exists(source_path):
                self.logger.warning(f"Fichier source inexistant: {source_path}")
                return None
            
            # Déterminer l'extension
            if file_extension:
                extension = file_extension if file_extension.startswith('.') else f'.{file_extension}'
            else:
                extension = os.path.splitext(source_path)[1].lower()
                if not extension:
                    extension = '.dat'  # Extension par défaut
            
            # Générer nom de fichier unique
            clean_prefix = self.clean_filename(name_prefix)
            unique_id = uuid.uuid4().hex[:8]
            filename = f"{clean_prefix}_{unique_id}{extension}"
            destination_path = os.path.join(self.storage_directory, filename)
            
            # Copier le fichier
            shutil.copy2(source_path, destination_path)
            
            # Vérifier que la copie a réussi
            if self.file_exists(destination_path):
                self.logger.info(f"Fichier copié: {os.path.basename(source_path)} -> {filename}")
                return destination_path
            else:
                self.logger.error(f"Échec copie vers: {destination_path}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde fichier: {e}")
            return None
    
    def remove_file(self, file_path):
        """
        Supprimer un fichier du répertoire de stockage
        
        Args:
            file_path (str): Chemin vers le fichier à supprimer
            
        Returns:
            bool: True si suppression réussie
        """
        try:
            if not file_path:
                return True  # Rien à supprimer
            
            # Vérifier que le fichier est dans notre répertoire
            if not file_path.startswith(self.storage_directory):
                self.logger.warning(f"Fichier hors répertoire géré: {file_path}")
                return True  # Ne pas supprimer fichiers externes
            
            if self.file_exists(file_path):
                os.remove(file_path)
                self.logger.info(f"Fichier supprimé: {os.path.basename(file_path)}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur suppression fichier: {e}")
            return False
    
    def update_file(self, old_file_path, new_source_path, name_prefix="file"):
        """
        Mettre à jour un fichier (supprimer l'ancien, copier le nouveau)
        
        Args:
            old_file_path (str): Chemin vers l'ancien fichier
            new_source_path (str): Chemin vers le nouveau fichier source
            name_prefix (str): Préfixe pour le nom de fichier
            
        Returns:
            str: Chemin vers le nouveau fichier, ou None si erreur
        """
        try:
            # Sauvegarder le nouveau fichier
            new_file_path = self.save_file(new_source_path, name_prefix)
            
            if new_file_path:
                # Supprimer l'ancien fichier seulement si le nouveau est sauvegardé
                self.remove_file(old_file_path)
                return new_file_path
            else:
                self.logger.error("Échec sauvegarde nouveau fichier")
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur mise à jour fichier: {e}")
            return None
    
    def list_files(self, pattern=None):
        """
        Lister tous les fichiers dans le répertoire
        
        Args:
            pattern (str): Pattern de filtrage (optionnel)
            
        Returns:
            list: Liste des chemins vers les fichiers
        """
        try:
            if not os.path.exists(self.storage_directory):
                return []
            
            files = []
            for filename in os.listdir(self.storage_directory):
                file_path = os.path.join(self.storage_directory, filename)
                if os.path.isfile(file_path):
                    if pattern is None or pattern.lower() in filename.lower():
                        files.append(file_path)
            
            return sorted(files)
            
        except Exception as e:
            self.logger.error(f"Erreur listage fichiers: {e}")
            return []
    
    def cleanup_orphaned_files(self, current_file_path=None, keep_count=1):
        """
        Nettoyer les fichiers orphelins
        
        Args:
            current_file_path (str): Fichier actuellement utilisé
            keep_count (int): Nombre de fichiers à conserver
            
        Returns:
            int: Nombre de fichiers supprimés
        """
        try:
            all_files = self.list_files()
            cleaned = 0
            
            # Trier par date de modification (plus récents en premier)
            all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            # Garder le fichier actuel et les plus récents
            files_to_keep = set()
            if current_file_path:
                files_to_keep.add(current_file_path)
            
            # Ajouter les fichiers les plus récents
            for i, file_path in enumerate(all_files):
                if len(files_to_keep) < keep_count:
                    files_to_keep.add(file_path)
                else:
                    break
            
            # Supprimer les autres fichiers
            for file_path in all_files:
                if file_path not in files_to_keep:
                    if self.remove_file(file_path):
                        cleaned += 1
            
            if cleaned > 0:
                self.logger.info(f"Nettoyage: {cleaned} fichiers orphelins supprimés")
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Erreur nettoyage fichiers: {e}")
            return 0
    
    def get_file_info(self, file_path):
        """
        Obtenir des informations sur un fichier
        
        Args:
            file_path (str): Chemin vers le fichier
            
        Returns:
            dict: Informations sur le fichier
        """
        info = {
            'exists': False,
            'size': None,
            'extension': None,
            'basename': None,
            'modified': None
        }
        
        try:
            if not file_path or not self.file_exists(file_path):
                return info
            
            info['exists'] = True
            info['size'] = os.path.getsize(file_path)
            info['extension'] = os.path.splitext(file_path)[1].lower()
            info['basename'] = os.path.basename(file_path)
            info['modified'] = os.path.getmtime(file_path)
            
        except Exception as e:
            self.logger.debug(f"Erreur info fichier: {e}")
        
        return info
    
    @staticmethod
    def file_exists(file_path):
        """Vérifier qu'un fichier existe"""
        return file_path and os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def clean_filename(name):
        """Nettoyer un nom pour l'utiliser dans un nom de fichier"""
        if not name:
            return "file"
        
        # Remplacer caractères non autorisés par underscore
        clean = re.sub(r'[^\w\-_.]', '_', str(name))
        # Limiter la longueur
        clean = clean[:20]
        # Éviter nom vide
        if not clean:
            clean = "file"
        return clean

class ImageFileManager(FileManager):
    """Gestionnaire spécialisé pour les fichiers images"""
    
    def __init__(self, subdirectory="images"):
        super().__init__(subdirectory=subdirectory)
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    
    def save_file(self, source_path, name_prefix="image", file_extension=None):
        """Sauvegarder une image avec validation"""
        try:
            # Valider que c'est bien une image
            if not self.is_valid_image(source_path):
                self.logger.warning(f"Fichier non valide comme image: {source_path}")
                return None
            
            return super().save_file(source_path, name_prefix, file_extension)
            
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde image: {e}")
            return None
    
    def is_valid_image(self, file_path):
        """Vérifier qu'un fichier est une image valide"""
        try:
            if not self.file_exists(file_path):
                return False
            
            # Vérifier l'extension
            extension = os.path.splitext(file_path)[1].lower()
            if extension not in self.supported_formats:
                return False
            
            # Vérifier l'intégrité avec PIL
            with Image.open(file_path) as img:
                img.verify()
            return True
            
        except Exception:
            return False
    
    def get_image_info(self, image_path):
        """Obtenir des informations détaillées sur une image"""
        info = self.get_file_info(image_path)
        
        if info['exists']:
            try:
                with Image.open(image_path) as img:
                    info['format'] = img.format
                    info['dimensions'] = img.size
                    info['size_str'] = f"{img.size[0]}x{img.size[1]}"
                    info['mode'] = img.mode
                    
            except Exception as e:
                self.logger.debug(f"Erreur info image: {e}")
        
        return info
    
    def list_images(self):
        """Lister toutes les images valides"""
        all_files = self.list_files()
        images = []
        
        for file_path in all_files:
            if self.is_valid_image(file_path):
                images.append(file_path)
        
        return images
