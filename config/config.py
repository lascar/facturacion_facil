"""
Configuración de la aplicación - Cache avec functools.lru_cache
Toute la configuration organisation est dans config.json, rien dans la DB.
"""
import os
import json
from pathlib import Path
from functools import lru_cache

# Cache global pour la configuration
_config_cache = {}


def get_config(config_file=None):
    """
    Obtient la configuration avec cache.
    Le cache est invalidé automatiquement lors de la sauvegarde.
    """
    config_path = config_file or os.environ.get('CONFIG_FILE', 'config/config.json')
    
    # Clé de cache basée sur le chemin du fichier
    cache_key = config_path
    
    if cache_key not in _config_cache:
        _config_cache[cache_key] = _load_config_from_file(config_path)
    
    return _config_cache[cache_key]


def invalidate_config_cache(config_file=None):
    """
    Invalide le cache de configuration.
    Doit être appelé après chaque sauvegarde de l'organisation.
    """
    config_path = config_file or os.environ.get('CONFIG_FILE', 'config/config.json')
    cache_key = config_path
    
    if cache_key in _config_cache:
        del _config_cache[cache_key]
        return True
    return False


def _load_config_from_file(config_path):
    """Charge la configuration depuis le fichier JSON"""
    default_config = {
        "default_image_directory": str(Path.home() / "Pictures"),
        "assets_directory": "assets/images",
        "max_image_size": 1024 * 1024,
        "supported_image_formats": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
        "image_display_size": (150, 150),
        "factura_numero_inicial": 1,
        "factura_auto_increment": True,
        "factura_prefijo": "",
        "factura_sufijo": "",
        "factura_formato": "{prefijo}{numero}{sufijo}",
        "organizacion_defaults": {}
    }
    
    # S'assurer que le répertoire existe
    config_dir = os.path.dirname(config_path)
    if config_dir and not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir, exist_ok=True)
        except OSError:
            pass
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            # Fusionner avec la configuration par défaut
            merged_config = default_config.copy()
            merged_config.update(config)
            return merged_config
        except (json.JSONDecodeError, IOError):
            return default_config.copy()
    else:
        # Créer le fichier avec la config par défaut
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
        return default_config.copy()


def save_config(config_data, config_file=None):
    """
    Sauvegarde la configuration dans le fichier JSON.
    Invalide automatiquement le cache.
    """
    config_path = config_file or os.environ.get('CONFIG_FILE', 'config/config.json')
    
    # S'assurer que le répertoire existe
    config_dir = os.path.dirname(config_path)
    if config_dir and not os.path.exists(config_dir):
        try:
            os.makedirs(config_dir, exist_ok=True)
        except OSError:
            pass
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        # Invalider le cache après sauvegarde
        invalidate_config_cache(config_path)
        return True
    except IOError as e:
        print(f"Erreur sauvegarde config: {e}")
        return False


class Config:
    """Clase para manejar la configuración de la aplicación (compatible legacy)"""

    def __init__(self, config_file=None):
        self.config_file = config_file or os.environ.get('CONFIG_FILE', 'config/config.json')
        self.config = get_config(self.config_file)

    def reload(self):
        """Recharge la configuration depuis le fichier (invalide le cache)"""
        invalidate_config_cache(self.config_file)
        self.config = get_config(self.config_file)
        return self.config

    def get(self, key, default=None):
        """Obtient une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration et sauvegarde"""
        self.config[key] = value
        return save_config(self.config, self.config_file)
    
    def get_organizacion_defaults(self):
        """Obtient les valeurs par défaut de l'organisation"""
        return self.config.get('organizacion_defaults', {})
    
    def set_organizacion_defaults(self, data):
        """Définit les valeurs par défaut de l'organisation et sauvegarde"""
        self.config['organizacion_defaults'] = data
        return save_config(self.config, self.config_file)

    # Méthodes pour la configuration des factures
    def get_factura_numero_inicial(self):
        """Obtiene el número inicial para facturas desde config.json"""
        org_defaults = self.get_organizacion_defaults()
        numero = org_defaults.get('numero_factura_inicial', 1)
        
        if isinstance(numero, str):
            if numero.isdigit():
                return int(numero)
            return numero  # Format personnalisé comme "2026/02"
        return numero

    def set_factura_numero_inicial(self, numero):
        """Establece el número inicial para facturas"""
        org_defaults = self.get_organizacion_defaults()
        org_defaults['numero_factura_inicial'] = str(numero)
        return self.set_organizacion_defaults(org_defaults)

    def get_factura_prefijo(self):
        """Obtiene el prefijo para números de factura"""
        return self.get("factura_prefijo", "")

    def set_factura_prefijo(self, prefijo):
        """Establece el prefijo para números de factura"""
        self.set("factura_prefijo", str(prefijo))

    def get_factura_sufijo(self):
        """Obtiene el sufijo para números de factura"""
        return self.get("factura_sufijo", "")

    def set_factura_sufijo(self, sufijo):
        """Establece el sufijo para números de factura"""
        self.set("factura_sufijo", str(sufijo))

    def get_factura_formato(self):
        """Obtiene el formato para números de factura"""
        return self.get("factura_formato", "{prefijo}{numero}{sufijo}")

    def set_factura_formato(self, formato):
        """Establece el formato para números de factura"""
        self.set("factura_formato", str(formato))

    def get_factura_auto_increment(self):
        """Obtiene si el auto-incremento está habilitado"""
        return self.get("factura_auto_increment", True)

    def set_factura_auto_increment(self, enabled):
        """Establece si el auto-incremento está habilitado"""
        self.set("factura_auto_increment", bool(enabled))

    # Méthodes legacy pour compatibilité
    def get_default_image_directory(self):
        """Obtient le répertoire par défaut pour les images"""
        directory = self.get("default_image_directory")
        if os.path.exists(directory):
            return directory
        return str(Path.home())
    
    def set_default_image_directory(self, directory):
        """Définit le répertoire par défaut pour les images"""
        if os.path.exists(directory):
            self.set("default_image_directory", directory)
            return True
        return False
    
    def get_assets_directory(self):
        """Obtient le répertoire des assets"""
        return self.get("assets_directory", "assets/images")
    
    def get_image_display_size(self):
        """Obtient la taille d'affichage des images"""
        return tuple(self.get("image_display_size", (150, 150)))
    
    def get_supported_formats(self):
        """Obtient les formats d'image supportés"""
        return self.get("supported_image_formats", [".png", ".jpg", ".jpeg", ".gif", ".bmp"])


# Instance globale de configuration (legacy compatibility)
app_config = Config()
