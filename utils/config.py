"""
Configuración de la aplicación
"""
import os
import json
from pathlib import Path

class Config:
    """Clase para manejar la configuración de la aplicación"""
    
    def __init__(self):
        self.config_file = "config.json"
        self.default_config = {
            "default_image_directory": str(Path.home() / "Pictures"),
            "assets_directory": "assets/images",
            "max_image_size": 1024 * 1024,  # 1MB
            "supported_image_formats": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
            "image_display_size": (150, 150),
            # Configuración de numeración de facturas
            "factura_numero_inicial": 1,
            "factura_auto_increment": True,
            "factura_prefijo": "",
            "factura_sufijo": "",
            "factura_formato": "{prefijo}{numero}{sufijo}"
        }
        self.config = self.load_config()
    
    def load_config(self):
        """Carga la configuración desde el archivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Fusionar con la configuración por défaut pour les nouvelles clés
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            except (json.JSONDecodeError, IOError):
                return self.default_config.copy()
        else:
            return self.default_config.copy()
    
    def save_config(self):
        """Sauvegarde la configuración en el archivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # Ignorer les erreurs de sauvegarde
    
    def get(self, key, default=None):
        """Obtient une valeur de configuration"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Définit une valeur de configuration"""
        self.config[key] = value
        self.save_config()
    
    def get_default_image_directory(self):
        """Obtient le répertoire par défaut pour les images"""
        directory = self.get("default_image_directory")
        if os.path.exists(directory):
            return directory
        else:
            # Fallback vers le répertoire home si le répertoire configuré n'existe pas
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

    # Métodos para configuración de facturas
    def get_factura_numero_inicial(self):
        """Obtiene el número inicial para facturas"""
        return self.get("factura_numero_inicial", 1)

    def set_factura_numero_inicial(self, numero):
        """Establece el número inicial para facturas"""
        if isinstance(numero, int) and numero > 0:
            self.set("factura_numero_inicial", numero)
            return True
        return False

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

    # Métodos para configuración de facturas
    def get_factura_numero_inicial(self):
        """Obtiene el número inicial para facturas"""
        return self.get("factura_numero_inicial", 1)

    def set_factura_numero_inicial(self, numero):
        """Establece el número inicial para facturas"""
        if isinstance(numero, int) and numero > 0:
            self.set("factura_numero_inicial", numero)
            return True
        return False

    def get_factura_auto_increment(self):
        """Obtiene si el auto-incremento está habilitado"""
        return self.get("factura_auto_increment", True)

    def set_factura_auto_increment(self, enabled):
        """Establece si el auto-incremento está habilitado"""
        self.set("factura_auto_increment", bool(enabled))

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

# Instance globale de configuration
app_config = Config()
