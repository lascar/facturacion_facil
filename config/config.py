"""
Configuración de la aplicación
"""
import os
import json
from pathlib import Path

class Config:
    """Clase para manejar la configuración de la aplicación"""
    
    def __init__(self):
        self.config_file = "config/config.json"
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
        # S'assurer que le répertoire config existe
        self._ensure_config_directory()
        self.config = self.load_config()

    def _ensure_config_directory(self):
        """S'assure que le répertoire config existe"""
        config_dir = os.path.dirname(self.config_file)
        if config_dir and not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir, exist_ok=True)
            except OSError:
                pass  # Ignorer les erreurs de création de répertoire

    def load_config(self):
        """Carga la configuración desde el archivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Fusionar avec la configuración par défaut pour les nouvelles clés
                merged_config = self.default_config.copy()
                merged_config.update(config)
                return merged_config
            except (json.JSONDecodeError, IOError):
                # Si le fichier existe mais est corrompu, le recréer
                self._create_default_config_file()
                return self.default_config.copy()
        else:
            # Si le fichier n'existe pas, le créer
            self._create_default_config_file()
            return self.default_config.copy()

    def _create_default_config_file(self):
        """Crée un fichier config.json vide avec la structure par défaut"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                # Créer un fichier vide pour préserver les configurations existantes
                # Les valeurs par défaut sont gérées en mémoire
                json.dump({}, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # Ignorer les erreurs de création
    
    def save_config(self):
        """Sauvegarde la configuración en el archivo"""
        try:
            # S'assurer que le répertoire existe avant de sauvegarder
            self._ensure_config_directory()
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
        """Obtiene el número inicial para facturas desde la tabla organizacion"""
        try:
            # Leer desde la tabla organizacion en lugar del archivo config.json
            import sqlite3
            conn = sqlite3.connect("base_de_datos/facturacion.db")
            cursor = conn.cursor()
            cursor.execute("SELECT numero_factura_inicial FROM organizacion WHERE id = 1")
            result = cursor.fetchone()
            conn.close()

            if result and result[0]:
                numero_inicial = result[0]
                # Si es un string que parece un número, convertir a int
                if isinstance(numero_inicial, str) and numero_inicial.isdigit():
                    return int(numero_inicial)
                # Si es un string con formato personalizado, devolverlo tal como está
                return numero_inicial
            else:
                # Fallback al valor por defecto
                return self.get("factura_numero_inicial", 1)

        except Exception as e:
            # En caso de error, usar el valor del archivo config
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
