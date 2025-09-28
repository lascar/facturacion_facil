# -*- coding: utf-8 -*-
"""
Componentes UI comunes para productos y facturas
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.translations import get_text
from utils.config import app_config
from utils.logger import get_logger
import os
from PIL import Image, ImageTk

logger = get_logger("ui_components")

class BaseWindow:
    """Clase base para ventanas con funcionalidades comunes"""
    
    def __init__(self, parent, title, geometry="800x600"):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.transient(parent)
        
        # Configurar ventana al frente
        self.window.lift()
        self.window.focus_force()
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))
        
        # Logger
        self.logger = get_logger(self.__class__.__name__.lower())
        
        # Variables comunes
        self.imagen_path = ""
    
    def _show_message(self, message_type, title, message):
        """Helper para mostrar mensajes copiables con el parent correcto"""
        try:
            # Importar las funciones de diálogos copiables
            from common.custom_dialogs import (
                show_copyable_info, show_copyable_error,
                show_copyable_warning, show_copyable_confirm
            )

            # Asegurar que la ventana esté al frente
            if hasattr(self, 'window') and self.window.winfo_exists():
                self.window.lift()
                self.window.focus_force()

                # Usar diálogos copiables en lugar de messagebox estándar
                if message_type == "info":
                    return show_copyable_info(self.window, title, message)
                elif message_type == "error":
                    return show_copyable_error(self.window, title, message)
                elif message_type == "warning":
                    return show_copyable_warning(self.window, title, message)
                elif message_type == "yesno":
                    return show_copyable_confirm(self.window, title, message)
            else:
                # Fallback con messagebox estándar si la ventana no existe
                if message_type == "info":
                    messagebox.showinfo(title, message)
                elif message_type == "error":
                    messagebox.showerror(title, message)
                elif message_type == "warning":
                    messagebox.showwarning(title, message)
                elif message_type == "yesno":
                    return messagebox.askyesno(title, message)

        except Exception as e:
            self.logger.error(f"Error al mostrar mensaje copiable: {e}")
            # Fallback con messagebox estándar
            try:
                if message_type == "info":
                    messagebox.showinfo(title, message, parent=self.window if hasattr(self, 'window') else None)
                elif message_type == "error":
                    messagebox.showerror(title, message, parent=self.window if hasattr(self, 'window') else None)
                elif message_type == "warning":
                    messagebox.showwarning(title, message, parent=self.window if hasattr(self, 'window') else None)
                elif message_type == "yesno":
                    return messagebox.askyesno(title, message, parent=self.window if hasattr(self, 'window') else None)
            except Exception as fallback_error:
                self.logger.error(f"Error en fallback: {fallback_error}")
                # Último recurso: imprimir en consola
                print(f"{title}: {message}")
    
    def setup_scrollable_frame(self, width=1150, height=750):
        """Configura un frame scrollable con scroll de rueda del ratón"""
        # Frame principal scrollable
        self.main_frame = ctk.CTkScrollableFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_frame.configure(width=width, height=height)
        
        # Configurar scroll de rueda del ratón
        self.configure_mousewheel_scrolling()
        
        return self.main_frame
    
    def bind_mousewheel_to_scrollable(self, widget):
        """Vincula el scroll de la rueda del ratón a un widget scrollable"""
        def _on_mousewheel(event):
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                if event.delta:
                    delta = -1 * (event.delta / 120)
                else:
                    if event.num == 4:
                        delta = -1
                    elif event.num == 5:
                        delta = 1
                    else:
                        return
                
                try:
                    self.main_frame._parent_canvas.yview_scroll(int(delta), "units")
                except (AttributeError, tk.TclError):
                    pass

        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", _on_mousewheel)
        widget.bind("<Button-5>", _on_mousewheel)

    def configure_mousewheel_scrolling(self):
        """Configura el scroll de la rueda del ratón para toda la ventana"""
        try:
            self.bind_mousewheel_to_scrollable(self.window)
            
            if hasattr(self, 'main_frame'):
                self.bind_mousewheel_to_scrollable(self.main_frame)
            
            def bind_to_children(widget):
                try:
                    self.bind_mousewheel_to_scrollable(widget)
                    for child in widget.winfo_children():
                        bind_to_children(child)
                except (AttributeError, tk.TclError):
                    pass
            
            bind_to_children(self.window)
            
        except Exception as e:
            self.logger.error(f"Error al configurar scroll de rueda del ratón: {e}")

class ImageSelector:
    """Componente para selección y manejo de imágenes"""
    
    def __init__(self, parent_window, logger=None):
        self.parent_window = parent_window
        self.logger = logger or get_logger("image_selector")
        self.imagen_path = ""
        self.imagen_display = None
        self.imagen_label = None
    
    def create_image_widgets(self, parent_frame):
        """Crea los widgets para manejo de imágenes"""
        imagen_frame = ctk.CTkFrame(parent_frame)
        imagen_frame.pack(fill="x", padx=10, pady=5)

        # Título y botón de configuración
        img_header_frame = ctk.CTkFrame(imagen_frame)
        img_header_frame.pack(fill="x", padx=5, pady=(5, 0))

        ctk.CTkLabel(img_header_frame, text=get_text("imagen")).pack(side="left", padx=5)

        config_btn = ctk.CTkButton(img_header_frame, text="⚙️", width=30, height=25,
                                 command=self.configurar_directorio_imagenes)
        config_btn.pack(side="right", padx=5)

        # Frame para botones de imagen
        img_buttons_frame = ctk.CTkFrame(imagen_frame)
        img_buttons_frame.pack(fill="x", padx=5, pady=5)

        seleccionar_btn = ctk.CTkButton(img_buttons_frame, text=get_text("seleccionar_imagen"),
                                      command=self.seleccionar_imagen)
        seleccionar_btn.pack(side="left", padx=5)

        self.quitar_imagen_btn = ctk.CTkButton(img_buttons_frame, text=get_text("quitar_imagen"),
                                             command=self.quitar_imagen, state="disabled")
        self.quitar_imagen_btn.pack(side="left", padx=5)

        # Label para mostrar nombre de archivo
        self.imagen_label = ctk.CTkLabel(imagen_frame, text="Ninguna imagen seleccionada")
        self.imagen_label.pack(pady=5)

        # Display de imagen
        self.imagen_display = ctk.CTkLabel(imagen_frame, text="", width=150, height=150)
        self.imagen_display.pack(pady=5)

        return imagen_frame
    
    def seleccionar_imagen(self):
        """Abre el diálogo para seleccionar una imagen"""
        try:
            initial_dir = app_config.get_default_image_directory()
            supported_formats = app_config.get_supported_formats()
            filetypes_str = " ".join([f"*{fmt}" for fmt in supported_formats])

            # Asegurar que la ventana esté al frente
            self.parent_window.lift()
            self.parent_window.focus_force()

            file_path = filedialog.askopenfilename(
                title=get_text("seleccionar_imagen"),
                initialdir=initial_dir,
                parent=self.parent_window,
                filetypes=[
                    ("Imágenes", filetypes_str),
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
                photo = ImageTk.PhotoImage(image)
                
                self.imagen_display.configure(image=photo, text="")
                self.imagen_display.image = photo
                
                if self.quitar_imagen_btn:
                    self.quitar_imagen_btn.configure(state="normal")
            else:
                self.imagen_display.configure(image="", text="Sin imagen")
                self.imagen_display.image = None
                
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
        """Configura el directorio por defecto de imágenes"""
        try:
            current_dir = app_config.get_default_image_directory()
            
            self.parent_window.lift()
            self.parent_window.focus_force()
            
            new_dir = filedialog.askdirectory(
                title="Seleccionar directorio por defecto para imágenes",
                initialdir=current_dir,
                parent=self.parent_window
            )
            
            if new_dir:
                if app_config.set_default_image_directory(new_dir):
                    if hasattr(self.parent_window, '_show_message'):
                        self.parent_window._show_message("info", "Configuración",
                                                       f"Directorio actualizado:\n{new_dir}")
                else:
                    if hasattr(self.parent_window, '_show_message'):
                        self.parent_window._show_message("error", "Error",
                                                       "No se pudo establecer el directorio")
        except Exception as e:
            self.logger.error(f"Error al configurar directorio: {e}")

class FormHelper:
    """Helper para operaciones comunes en formularios"""
    
    @staticmethod
    def clear_entry(entry_widget, default_value=""):
        """Limpia un campo de entrada y opcionalmente establece un valor por defecto"""
        try:
            if entry_widget is not None:
                entry_widget.delete(0, tk.END)
                if default_value:
                    entry_widget.insert(0, default_value)
        except (tk.TclError, AttributeError):
            pass
    
    @staticmethod
    def clear_text_widget(text_widget):
        """Limpia un widget de texto"""
        try:
            if text_widget is not None:
                text_widget.delete("1.0", tk.END)
        except (tk.TclError, AttributeError):
            pass
    
    @staticmethod
    def get_entry_value(entry_widget, default=""):
        """Obtiene el valor de un campo de entrada de forma segura"""
        try:
            if entry_widget is not None:
                value = entry_widget.get().strip()
                return value if value else default
            return default
        except (tk.TclError, AttributeError):
            return default
    
    @staticmethod
    def get_text_value(text_widget, default=""):
        """Obtiene el valor de un widget de texto de forma segura"""
        try:
            if text_widget is not None:
                value = text_widget.get("1.0", tk.END).strip()
                return value if value else default
            return default
        except (tk.TclError, AttributeError):
            return default
    
    @staticmethod
    def set_entry_value(entry_widget, value):
        """Establece el valor de un campo de entrada de forma segura"""
        try:
            if entry_widget is not None:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(value))
        except (tk.TclError, AttributeError):
            pass
    
    @staticmethod
    def set_text_value(text_widget, value):
        """Establece el valor de un widget de texto de forma segura"""
        try:
            if text_widget is not None:
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", str(value))
        except (tk.TclError, AttributeError):
            pass
