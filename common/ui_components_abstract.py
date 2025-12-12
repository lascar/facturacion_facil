# -*- coding: utf-8 -*-
"""
Componentes UI comunes refactorizados para usar la abstracción GUI
"""
from gui import get_gui_factory
from utils.translations import get_text
from config.config import app_config
from utils.logger import get_logger
import os
from PIL import Image

logger = get_logger("ui_components_abstract")

class AbstractFormHelper:
    """Helper para operaciones comunes en formularios usando abstracción GUI"""
    
    @staticmethod
    def clear_entry(entry_widget, default_value=""):
        """Limpia un campo de entrada y opcionalmente establece un valor por defecto"""
        try:
            if entry_widget is not None:
                native_widget = entry_widget.get_native_widget()
                
                # Detectar el tipo de widget nativo y usar la API apropiada
                if hasattr(native_widget, 'clear'):  # PyQt5
                    native_widget.clear()
                    if default_value:
                        native_widget.setText(str(default_value))
                elif hasattr(native_widget, 'delete'):  # Tkinter
                    native_widget.delete(0, 'end')
                    if default_value:
                        native_widget.insert(0, str(default_value))
        except (AttributeError, Exception):
            pass
    
    @staticmethod
    def clear_text_widget(text_widget):
        """Limpia un widget de texto"""
        try:
            if text_widget is not None:
                native_widget = text_widget.get_native_widget()
                
                if hasattr(native_widget, 'clear'):  # PyQt5
                    native_widget.clear()
                elif hasattr(native_widget, 'delete'):  # Tkinter
                    native_widget.delete("1.0", 'end')
        except (AttributeError, Exception):
            pass
    
    @staticmethod
    def get_entry_value(entry_widget, default=""):
        """Obtiene el valor de un campo de entrada de forma segura"""
        try:
            if entry_widget is not None:
                native_widget = entry_widget.get_native_widget()
                
                if hasattr(native_widget, 'text'):  # PyQt5
                    value = native_widget.text().strip()
                elif hasattr(native_widget, 'get'):  # Tkinter
                    value = native_widget.get().strip()
                else:
                    return default
                    
                return value if value else default
            return default
        except (AttributeError, Exception):
            return default
    
    @staticmethod
    def get_text_value(text_widget, default=""):
        """Obtiene el valor de un widget de texto de forma segura"""
        try:
            if text_widget is not None:
                native_widget = text_widget.get_native_widget()
                
                if hasattr(native_widget, 'toPlainText'):  # PyQt5
                    value = native_widget.toPlainText().strip()
                elif hasattr(native_widget, 'get'):  # Tkinter
                    value = native_widget.get("1.0", 'end').strip()
                else:
                    return default
                    
                return value if value else default
            return default
        except (AttributeError, Exception):
            return default
    
    @staticmethod
    def set_entry_value(entry_widget, value):
        """Establece el valor de un campo de entrada de forma segura"""
        try:
            if entry_widget is not None:
                native_widget = entry_widget.get_native_widget()
                
                if hasattr(native_widget, 'setText'):  # PyQt5
                    native_widget.setText(str(value))
                elif hasattr(native_widget, 'delete') and hasattr(native_widget, 'insert'):  # Tkinter
                    native_widget.delete(0, 'end')
                    native_widget.insert(0, str(value))
        except (AttributeError, Exception):
            pass
    
    @staticmethod
    def set_text_value(text_widget, value):
        """Establece el valor de un widget de texto de forma segura"""
        try:
            if text_widget is not None:
                native_widget = text_widget.get_native_widget()
                
                if hasattr(native_widget, 'setPlainText'):  # PyQt5
                    native_widget.setPlainText(str(value))
                elif hasattr(native_widget, 'delete') and hasattr(native_widget, 'insert'):  # Tkinter
                    native_widget.delete("1.0", 'end')
                    native_widget.insert("1.0", str(value))
        except (AttributeError, Exception):
            pass

class AbstractBaseWindow:
    """Clase base para ventanas usando abstracción GUI"""
    
    def __init__(self, parent, title, geometry="800x600"):
        self.gui_factory = get_gui_factory()
        self.parent = parent
        self.title = title
        self.geometry = geometry
        
        # Crear la ventana usando la factory
        if parent:
            self.window = self.gui_factory.create_toplevel(parent, title, geometry)
        else:
            self.window = self.gui_factory.create_window(title, geometry)
        
        # Logger
        self.logger = get_logger(self.__class__.__name__.lower())
        
        # Variables comunes
        self.imagen_path = ""
        self.main_frame = None
    
    def _show_message(self, message_type, title, message):
        """Helper para mostrar mensajes usando la abstracción GUI"""
        try:
            return self.gui_factory.show_message(message_type, title, message)
        except Exception as e:
            self.logger.error(f"Error al mostrar mensaje: {e}")
            return None
    
    def setup_scrollable_frame(self, width=None, height=None):
        """Configura un frame scrollable usando la abstracción GUI"""
        try:
            self.main_frame = self.gui_factory.create_scrollable_frame(self.window)
            if width and height:
                self.main_frame.configure(width=width, height=height)
            return self.main_frame
        except Exception as e:
            self.logger.error(f"Error al configurar frame scrollable: {e}")
            return None
    
    def bind_mousewheel_to_scrollable(self, widget):
        """Vincula el scroll de rueda del ratón (implementación básica)"""
        try:
            # Esta es una implementación básica - puede necesitar mejoras específicas por framework
            pass
        except Exception as e:
            self.logger.error(f"Error al vincular scroll: {e}")

    def configure_mousewheel_scrolling(self, scrollable_widget):
        """Configura el scroll de rueda del ratón para un widget scrollable"""
        try:
            # Método de compatibilidad para la interfaz legacy
            self.bind_mousewheel_to_scrollable(scrollable_widget)
            self.logger.debug("Scroll de rueda del ratón configurado")
        except Exception as e:
            self.logger.error(f"Error al configurar scroll: {e}")

class AbstractImageSelector:
    """Componente para selección y manejo de imágenes usando abstracción GUI"""

    def __init__(self, parent_window, logger=None):
        self.gui_factory = get_gui_factory()
        self.parent_window = parent_window
        self.logger = logger or get_logger("image_selector")
        self.imagen_path = ""
        self.imagen_display = None
        self.imagen_label = None
        self.quitar_imagen_btn = None

    def seleccionar_imagen(self):
        """Abre el diálogo para seleccionar una imagen usando la abstracción GUI"""
        try:
            initial_dir = app_config.get_default_image_directory()

            # Usar la abstracción GUI para el diálogo de archivos
            file_path = self.gui_factory.ask_file(
                title=get_text("seleccionar_imagen"),
                initialdir=initial_dir,
                filetypes=[
                    ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("GIF files", "*.gif"),
                    ("BMP files", "*.bmp"),
                    ("Todos los archivos", "*.*")
                ]
            )

            if file_path:
                filename = os.path.basename(file_path)
                assets_dir = app_config.get_assets_directory()

                if not os.path.exists(assets_dir):
                    os.makedirs(assets_dir)

                dest_path = os.path.join(assets_dir, filename)

                try:
                    import shutil
                    shutil.copy2(file_path, dest_path)
                    self.imagen_path = dest_path
                    if self.imagen_label:
                        self.imagen_label.configure(text=f"Imagen: {filename}")
                    self.update_image_display()
                    self.logger.info(f"Imagen seleccionada: {filename}")
                except Exception as e:
                    self.logger.error(f"Error al copiar imagen: {e}")
                    if hasattr(self.parent_window, '_show_message'):
                        self.parent_window._show_message("error", get_text("error"),
                                                       f"Error al copiar imagen: {str(e)}")

        except Exception as e:
            self.logger.error(f"Error al seleccionar imagen: {e}")

    def update_image_display(self):
        """Actualiza el display de la imagen"""
        if not self.imagen_display:
            return

        try:
            if self.imagen_path and os.path.exists(self.imagen_path):
                display_size = app_config.get_image_display_size()
                image = Image.open(self.imagen_path)
                image.thumbnail(display_size, Image.Resampling.LANCZOS)

                # Configurar la imagen en el widget de display
                # Nota: La implementación específica dependerá del framework
                native_display = self.imagen_display.get_native_widget()

                if hasattr(native_display, 'setPixmap'):  # PyQt5
                    from PyQt5.QtGui import QPixmap
                    # Convertir PIL Image a QPixmap
                    import io
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    pixmap = QPixmap()
                    pixmap.loadFromData(img_bytes.getvalue())
                    native_display.setPixmap(pixmap)
                else:  # Tkinter
                    from PIL import ImageTk
                    photo = ImageTk.PhotoImage(image)
                    native_display.configure(image=photo, text="")
                    native_display.image = photo  # Mantener referencia

                if self.quitar_imagen_btn:
                    self.quitar_imagen_btn.configure(state="normal")
            else:
                # Limpiar la imagen
                native_display = self.imagen_display.get_native_widget()
                if hasattr(native_display, 'clear'):  # PyQt5
                    native_display.clear()
                else:  # Tkinter
                    native_display.configure(image="", text="Sin imagen")
                    native_display.image = None

                if self.quitar_imagen_btn:
                    self.quitar_imagen_btn.configure(state="disabled")

        except Exception as e:
            self.logger.error(f"Error al actualizar display de imagen: {e}")

    def quitar_imagen(self):
        """Quita la imagen seleccionada"""
        self.imagen_path = ""
        if self.imagen_label:
            self.imagen_label.configure(text="Ninguna imagen seleccionada")
        self.update_image_display()

    def configurar_directorio_imagenes(self):
        """Configura el directorio por defecto de imágenes usando la abstracción GUI"""
        try:
            current_dir = app_config.get_default_image_directory()

            # Usar la abstracción GUI para el diálogo de directorio
            new_dir = self.gui_factory.ask_directory(
                title="Seleccionar directorio por defecto para imágenes",
                initialdir=current_dir
            )

            if new_dir:
                app_config.set_default_image_directory(new_dir)
                self.logger.info(f"Directorio de imágenes configurado: {new_dir}")
                if hasattr(self.parent_window, '_show_message'):
                    self.parent_window._show_message("info", "Configuración",
                                                   f"Directorio configurado: {new_dir}")
            else:
                if hasattr(self.parent_window, '_show_message'):
                    self.parent_window._show_message("error", "Error",
                                                   "No se pudo establecer el directorio")
        except Exception as e:
            self.logger.error(f"Error al configurar directorio: {e}")

# Alias para compatibilidad con el código existente
FormHelper = AbstractFormHelper
BaseWindow = AbstractBaseWindow
ImageSelector = AbstractImageSelector
