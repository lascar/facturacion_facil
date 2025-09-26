"""
Utilitaires pour la gestion des images dans l'application
"""
import os
from PIL import Image, ImageTk
import tkinter as tk
from utils.logger import get_logger

class ImageUtils:
    """Classe utilitaire pour la gestion des images"""
    
    def __init__(self):
        self.logger = get_logger("image_utils")
        self._image_cache = {}  # Cache pour les images redimensionnées
    
    @staticmethod
    def create_mini_image(image_path, size=(32, 32)):
        """
        Crée une mini image redimensionnée pour affichage dans les listes

        Args:
            image_path (str): Chemin vers l'image source
            size (tuple): Taille désirée (largeur, hauteur)

        Returns:
            ImageTk.PhotoImage: Image redimensionnée prête pour tkinter
            None: Si erreur ou image inexistante
        """
        logger = get_logger("image_utils")

        try:
            if not image_path or not os.path.exists(image_path):
                logger.debug(f"Image non trouvée: {image_path}")
                return None

            # Vérifier qu'il y a une fenêtre tkinter disponible
            try:
                import tkinter as tk
                root = tk._default_root
                if root is None:
                    # Créer une fenêtre racine temporaire si nécessaire
                    temp_root = tk.Tk()
                    temp_root.withdraw()  # Cacher la fenêtre
            except:
                logger.debug("Pas de fenêtre tkinter disponible")
                return None

            # Ouvrir et redimensionner l'image
            with Image.open(image_path) as img:
                # Convertir en RGB si nécessaire (pour éviter les problèmes avec certains formats)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Créer un fond blanc pour les images avec transparence
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Redimensionner en gardant les proportions
                img.thumbnail(size, Image.Resampling.LANCZOS)

                # Créer une nouvelle image avec la taille exacte demandée (centrer l'image)
                final_img = Image.new('RGB', size, (255, 255, 255))

                # Calculer la position pour centrer l'image
                x = (size[0] - img.width) // 2
                y = (size[1] - img.height) // 2

                final_img.paste(img, (x, y))

                # Convertir pour tkinter
                photo = ImageTk.PhotoImage(final_img)

                logger.debug(f"Mini image créée: {os.path.basename(image_path)} -> {size}")
                return photo

        except Exception as e:
            logger.warning(f"Erreur lors de la création de mini image pour {image_path}: {e}")
            return None
    
    @staticmethod
    def create_placeholder_image(size=(32, 32), text="📷"):
        """
        Crée une image placeholder pour les produits sans image

        Args:
            size (tuple): Taille de l'image
            text (str): Texte à afficher

        Returns:
            ImageTk.PhotoImage: Image placeholder
        """
        try:
            # Vérifier qu'il y a une fenêtre tkinter disponible
            try:
                import tkinter as tk
                root = tk._default_root
                if root is None:
                    # Créer une fenêtre racine temporaire si nécessaire
                    temp_root = tk.Tk()
                    temp_root.withdraw()  # Cacher la fenêtre
            except:
                logger = get_logger("image_utils")
                logger.debug("Pas de fenêtre tkinter disponible pour placeholder")
                return None

            # Créer une image avec fond gris clair
            img = Image.new('RGB', size, (240, 240, 240))

            # Pour l'instant, on retourne juste l'image unie
            # On pourrait ajouter du texte avec PIL.ImageDraw si nécessaire
            photo = ImageTk.PhotoImage(img)
            return photo

        except Exception as e:
            logger = get_logger("image_utils")
            logger.warning(f"Erreur lors de la création d'image placeholder: {e}")
            return None
    
    def get_cached_mini_image(self, image_path, size=(32, 32)):
        """
        Récupère une mini image du cache ou la crée si nécessaire
        
        Args:
            image_path (str): Chemin vers l'image
            size (tuple): Taille désirée
            
        Returns:
            ImageTk.PhotoImage: Image redimensionnée
        """
        cache_key = f"{image_path}_{size[0]}x{size[1]}"
        
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        
        mini_image = self.create_mini_image(image_path, size)
        if mini_image:
            self._image_cache[cache_key] = mini_image
        
        return mini_image
    
    def clear_cache(self):
        """Vide le cache des images"""
        self._image_cache.clear()
        self.logger.debug("Cache d'images vidé")
    
    @staticmethod
    def get_mini_image_size():
        """Retourne la taille standard pour les mini images dans les listes"""
        return (32, 32)  # Taille optimale pour les TreeView
    
    @staticmethod
    def is_image_file(file_path):
        """
        Vérifie si un fichier est une image supportée
        
        Args:
            file_path (str): Chemin vers le fichier
            
        Returns:
            bool: True si c'est une image supportée
        """
        if not file_path:
            return False
        
        supported_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in supported_extensions

# Instance globale pour utilisation dans l'application
image_utils = ImageUtils()
