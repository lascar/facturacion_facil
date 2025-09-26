"""
Gestionnaire d'images générique pour l'application
Fournit des fonctionnalités communes pour la gestion d'images
"""

from utils.file_manager import ImageFileManager
from utils.logger import get_logger
from PIL import Image, ImageTk
import os

class ImageManager:
    """Gestionnaire d'images générique avec cache et optimisation"""
    
    def __init__(self, subdirectory="images", cache_size=100):
        """
        Initialiser le gestionnaire d'images
        
        Args:
            subdirectory (str): Sous-répertoire pour stocker les images
            cache_size (int): Taille maximale du cache d'images
        """
        self.logger = get_logger(f"image_manager_{subdirectory}")
        self.file_manager = ImageFileManager(subdirectory=subdirectory)
        self.cache_size = cache_size
        self._image_cache = {}
        self._cache_order = []
    
    @property
    def storage_directory(self):
        """Répertoire de stockage des images"""
        return self.file_manager.storage_directory
    
    def save_image(self, source_path, name_prefix="image"):
        """
        Sauvegarder une image dans le répertoire permanent
        
        Args:
            source_path (str): Chemin vers l'image source
            name_prefix (str): Préfixe pour le nom de fichier
            
        Returns:
            str: Chemin vers l'image sauvegardée, ou None si erreur
        """
        return self.file_manager.save_file(source_path, name_prefix)
    
    def remove_image(self, image_path):
        """
        Supprimer une image
        
        Args:
            image_path (str): Chemin vers l'image à supprimer
            
        Returns:
            bool: True si suppression réussie
        """
        # Supprimer du cache si présente
        self._remove_from_cache(image_path)
        return self.file_manager.remove_file(image_path)
    
    def update_image(self, old_image_path, new_source_path, name_prefix="image"):
        """
        Mettre à jour une image
        
        Args:
            old_image_path (str): Chemin vers l'ancienne image
            new_source_path (str): Chemin vers la nouvelle image source
            name_prefix (str): Préfixe pour le nom de fichier
            
        Returns:
            str: Chemin vers la nouvelle image, ou None si erreur
        """
        # Supprimer l'ancienne image du cache
        self._remove_from_cache(old_image_path)
        return self.file_manager.update_file(old_image_path, new_source_path, name_prefix)
    
    def get_image_info(self, image_path):
        """
        Obtenir des informations sur une image
        
        Args:
            image_path (str): Chemin vers l'image
            
        Returns:
            dict: Informations sur l'image
        """
        return self.file_manager.get_image_info(image_path)
    
    def list_images(self):
        """
        Lister toutes les images
        
        Returns:
            list: Liste des chemins vers les images
        """
        return self.file_manager.list_images()
    
    def cleanup_orphaned_images(self, current_images=None, keep_count=10):
        """
        Nettoyer les images orphelines
        
        Args:
            current_images (list): Liste des images actuellement utilisées
            keep_count (int): Nombre d'images récentes à conserver
            
        Returns:
            int: Nombre d'images supprimées
        """
        try:
            all_images = self.list_images()
            cleaned = 0
            
            # Créer un set des images à conserver
            images_to_keep = set()
            if current_images:
                images_to_keep.update(current_images)
            
            # Trier par date de modification (plus récentes en premier)
            all_images.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            
            # Ajouter les images les plus récentes
            for i, image_path in enumerate(all_images):
                if len(images_to_keep) < keep_count:
                    images_to_keep.add(image_path)
                else:
                    break
            
            # Supprimer les autres images
            for image_path in all_images:
                if image_path not in images_to_keep:
                    if self.remove_image(image_path):
                        cleaned += 1
            
            if cleaned > 0:
                self.logger.info(f"Nettoyage: {cleaned} images orphelines supprimées")
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Erreur nettoyage images: {e}")
            return 0
    
    def create_thumbnail(self, image_path, size=(64, 64)):
        """
        Créer une miniature d'une image
        
        Args:
            image_path (str): Chemin vers l'image source
            size (tuple): Taille de la miniature (largeur, hauteur)
            
        Returns:
            PIL.Image: Image miniature, ou None si erreur
        """
        try:
            if not self.file_manager.file_exists(image_path):
                return None
            
            with Image.open(image_path) as img:
                # Créer une copie pour éviter de modifier l'original
                thumbnail = img.copy()
                thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
                return thumbnail
                
        except Exception as e:
            self.logger.error(f"Erreur création miniature: {e}")
            return None
    
    def get_cached_image(self, image_path, size=None):
        """
        Obtenir une image depuis le cache ou la charger
        
        Args:
            image_path (str): Chemin vers l'image
            size (tuple): Taille souhaitée (optionnel)
            
        Returns:
            PIL.Image: Image chargée, ou None si erreur
        """
        try:
            if not self.file_manager.file_exists(image_path):
                return None
            
            # Créer clé de cache
            cache_key = f"{image_path}_{size}" if size else image_path
            
            # Vérifier le cache
            if cache_key in self._image_cache:
                # Mettre à jour l'ordre d'utilisation
                self._cache_order.remove(cache_key)
                self._cache_order.append(cache_key)
                return self._image_cache[cache_key]
            
            # Charger l'image
            with Image.open(image_path) as img:
                # Créer une copie pour éviter les problèmes de fermeture
                loaded_image = img.copy()
                
                # Redimensionner si nécessaire
                if size:
                    loaded_image.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Ajouter au cache
                self._add_to_cache(cache_key, loaded_image)
                
                return loaded_image
                
        except Exception as e:
            self.logger.error(f"Erreur chargement image: {e}")
            return None
    
    def get_cached_tkinter_image(self, image_path, size=None):
        """
        Obtenir une image Tkinter depuis le cache
        
        Args:
            image_path (str): Chemin vers l'image
            size (tuple): Taille souhaitée (optionnel)
            
        Returns:
            ImageTk.PhotoImage: Image Tkinter, ou None si erreur
        """
        try:
            pil_image = self.get_cached_image(image_path, size)
            if pil_image:
                return ImageTk.PhotoImage(pil_image)
            return None
            
        except Exception as e:
            self.logger.error(f"Erreur création image Tkinter: {e}")
            return None
    
    def create_placeholder_image(self, size=(64, 64), color='lightgray', text=None):
        """
        Créer une image placeholder
        
        Args:
            size (tuple): Taille de l'image
            color (str): Couleur de fond
            text (str): Texte à afficher (optionnel)
            
        Returns:
            PIL.Image: Image placeholder
        """
        try:
            img = Image.new('RGB', size, color=color)
            
            if text:
                from PIL import ImageDraw, ImageFont
                draw = ImageDraw.Draw(img)
                
                # Essayer d'utiliser une police par défaut
                try:
                    font = ImageFont.load_default()
                except:
                    font = None
                
                # Calculer position du texte (centré)
                if font:
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                else:
                    text_width = len(text) * 6  # Estimation
                    text_height = 11
                
                x = (size[0] - text_width) // 2
                y = (size[1] - text_height) // 2
                
                draw.text((x, y), text, fill='black', font=font)
            
            return img
            
        except Exception as e:
            self.logger.error(f"Erreur création placeholder: {e}")
            # Retourner une image simple en cas d'erreur
            return Image.new('RGB', size, color='lightgray')
    
    def _add_to_cache(self, cache_key, image):
        """Ajouter une image au cache"""
        try:
            # Supprimer les anciennes entrées si le cache est plein
            while len(self._image_cache) >= self.cache_size:
                oldest_key = self._cache_order.pop(0)
                del self._image_cache[oldest_key]
            
            # Ajouter la nouvelle image
            self._image_cache[cache_key] = image
            self._cache_order.append(cache_key)
            
        except Exception as e:
            self.logger.error(f"Erreur ajout cache: {e}")
    
    def _remove_from_cache(self, image_path):
        """Supprimer une image du cache"""
        try:
            keys_to_remove = [key for key in self._image_cache.keys() if key.startswith(image_path)]
            for key in keys_to_remove:
                del self._image_cache[key]
                if key in self._cache_order:
                    self._cache_order.remove(key)
                    
        except Exception as e:
            self.logger.error(f"Erreur suppression cache: {e}")
    
    def clear_cache(self):
        """Vider le cache d'images"""
        self._image_cache.clear()
        self._cache_order.clear()
        self.logger.info("Cache d'images vidé")
    
    def get_cache_stats(self):
        """Obtenir des statistiques sur le cache"""
        return {
            'size': len(self._image_cache),
            'max_size': self.cache_size,
            'usage': f"{len(self._image_cache)}/{self.cache_size}"
        }
