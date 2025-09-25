import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.translations import get_text
from utils.config import app_config
from utils.logger import get_logger, log_user_action, log_file_operation, log_exception, log_database_operation
from database.models import Producto
import os
import shutil
from PIL import Image, ImageTk

class ProductosWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(get_text("gestion_productos"))
        self.window.geometry("900x700")  # Tamaño inicial más pequeño para demostrar scrolling
        self.window.transient(parent)

        # Asegurar que la ventana aparezca al frente
        self.window.lift()
        self.window.focus_force()
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))

        # Logger para este módulo
        self.logger = get_logger("productos")
        self.logger.info("Inicializando ventana de gestión de productos")

        # Variables
        self.productos = []
        self.selected_producto = None
        self.imagen_path = ""

        # Crear interfaz
        self.create_widgets()

        # Configurar comportamiento de scrolling
        self.configure_scrollable_behavior()

        # Configurar scroll con rueda del ratón
        self.configure_mousewheel_scrolling()

        self.load_productos()

        self.logger.info("Ventana de productos inicializada correctamente con scrolling habilitado")

    def configure_scrollable_behavior(self):
        """Configura el comportamiento del scrolling"""
        try:
            # Permitir que la ventana sea redimensionable
            self.window.resizable(True, True)

            # Configurar tamaño mínimo de la ventana
            self.window.minsize(800, 600)

            # Configurar tamaño máximo razonable
            self.window.maxsize(1600, 1200)

            self.logger.debug("Comportamiento de scrolling configurado")

        except Exception as e:
            self.logger.error(f"Error al configurar scrolling: {e}")

    def bind_mousewheel_to_scrollable(self, widget):
        """Vincula el scroll de la rueda del ratón a un widget scrollable"""
        def _on_mousewheel(event):
            # Solo hacer scroll si el widget scrollable existe y está visible
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                # Determinar la dirección del scroll
                if event.delta:
                    # Windows y MacOS
                    delta = -1 * (event.delta / 120)
                else:
                    # Linux
                    if event.num == 4:
                        delta = -1
                    elif event.num == 5:
                        delta = 1
                    else:
                        return

                # Hacer scroll en el frame principal
                try:
                    self.main_frame._parent_canvas.yview_scroll(int(delta), "units")
                except (AttributeError, tk.TclError):
                    # Si no hay canvas o hay error, intentar con el método alternativo
                    pass

        # Vincular eventos de rueda del ratón
        widget.bind("<MouseWheel>", _on_mousewheel)  # Windows y MacOS
        widget.bind("<Button-4>", _on_mousewheel)    # Linux scroll up
        widget.bind("<Button-5>", _on_mousewheel)    # Linux scroll down

    def configure_mousewheel_scrolling(self):
        """Configura el scroll de la rueda del ratón para toda la ventana"""
        try:
            # Vincular el scroll a la ventana principal
            self.bind_mousewheel_to_scrollable(self.window)

            # Vincular el scroll al frame principal si existe
            if hasattr(self, 'main_frame'):
                self.bind_mousewheel_to_scrollable(self.main_frame)

            # Función recursiva para vincular a todos los widgets hijos
            def bind_to_children(widget):
                try:
                    self.bind_mousewheel_to_scrollable(widget)
                    for child in widget.winfo_children():
                        bind_to_children(child)
                except (AttributeError, tk.TclError):
                    pass

            # Aplicar a todos los widgets de la ventana
            bind_to_children(self.window)

            self.logger.debug("Scroll de rueda del ratón configurado para todos los widgets")

        except Exception as e:
            self.logger.error(f"Error al configurar scroll de rueda del ratón: {e}")

    def _show_message(self, message_type, title, message):
        """Helper para mostrar mensajes con el parent correcto"""
        try:
            # Asegurar que la ventana esté al frente
            if hasattr(self, 'window') and self.window.winfo_exists():
                self.window.lift()
                self.window.focus_force()

                # Usar la ventana como parent para que el popup aparezca encima
                if message_type == "info":
                    messagebox.showinfo(title, message, parent=self.window)
                elif message_type == "error":
                    messagebox.showerror(title, message, parent=self.window)
                elif message_type == "warning":
                    messagebox.showwarning(title, message, parent=self.window)
                elif message_type == "yesno":
                    return messagebox.askyesno(title, message, parent=self.window)
            else:
                # Fallback si la ventana no existe
                if message_type == "info":
                    messagebox.showinfo(title, message)
                elif message_type == "error":
                    messagebox.showerror(title, message)
                elif message_type == "warning":
                    messagebox.showwarning(title, message)
                elif message_type == "yesno":
                    return messagebox.askyesno(title, message)
        except Exception as e:
            self.logger.error(f"Error al mostrar mensaje: {e}")
            # Fallback básico
            print(f"{title}: {message}")

    def create_widgets(self):
        """Crea los widgets de la ventana"""
        # Frame principal scrollable para permitir desplazamiento cuando el contenido es grande
        self.main_frame = ctk.CTkScrollableFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configurar el scrollable frame para que tenga un tamaño mínimo apropiado
        self.main_frame.configure(width=1150, height=750)  # Tamaño mínimo para el contenido

        self.logger.debug("Frame principal scrollable creado con tamaño mínimo configurado")
        
        # Título
        title_label = ctk.CTkLabel(
            self.main_frame,
            text=get_text("gestion_productos"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))

        # Frame contenedor horizontal
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame izquierdo - Lista de productos
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Lista de productos
        list_label = ctk.CTkLabel(left_frame, text="Lista de Productos", font=ctk.CTkFont(size=16, weight="bold"))
        list_label.pack(pady=(10, 5))
        
        # Frame para la lista con scrollbar
        list_frame = ctk.CTkFrame(left_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.productos_listbox = tk.Listbox(list_frame, font=("Arial", 10))
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.productos_listbox.yview)
        self.productos_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.productos_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.productos_listbox.bind("<<ListboxSelect>>", self.on_producto_select)
        
        # Botones de lista
        buttons_frame = ctk.CTkFrame(left_frame)
        buttons_frame.pack(fill="x", padx=10, pady=5)

        eliminar_btn = ctk.CTkButton(buttons_frame, text=get_text("eliminar_producto"),
                                   fg_color="#DC143C", hover_color="#B22222", command=self.eliminar_producto)
        eliminar_btn.pack(fill="x", padx=5)
        
        # Frame derecho - Formulario
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Formulario
        form_label = ctk.CTkLabel(right_frame, text="Datos del Producto", font=ctk.CTkFont(size=16, weight="bold"))
        form_label.pack(pady=(10, 20))
        
        # Crear campos del formulario
        self.create_form_fields(right_frame)
    
    def create_form_fields(self, parent):
        """Crea los campos del formulario"""
        # Frame para el formulario
        form_frame = ctk.CTkFrame(parent)
        form_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Nombre
        ctk.CTkLabel(form_frame, text=get_text("nombre") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre del producto")
        self.nombre_entry.pack(fill="x", padx=10, pady=5)
        
        # Referencia
        ctk.CTkLabel(form_frame, text=get_text("referencia") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.referencia_entry = ctk.CTkEntry(form_frame, placeholder_text="Código de referencia")
        self.referencia_entry.pack(fill="x", padx=10, pady=5)
        
        # Frame para precio y categoría
        precio_cat_frame = ctk.CTkFrame(form_frame)
        precio_cat_frame.pack(fill="x", padx=10, pady=5)
        
        # Precio
        precio_frame = ctk.CTkFrame(precio_cat_frame)
        precio_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(precio_frame, text=get_text("precio") + "*").pack(anchor="w", padx=5, pady=(5, 0))
        self.precio_entry = ctk.CTkEntry(precio_frame, placeholder_text="0.00")
        self.precio_entry.pack(fill="x", padx=5, pady=5)
        
        # Categoría
        cat_frame = ctk.CTkFrame(precio_cat_frame)
        cat_frame.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(cat_frame, text=get_text("categoria")).pack(anchor="w", padx=5, pady=(5, 0))
        self.categoria_entry = ctk.CTkEntry(cat_frame, placeholder_text="Categoría")
        self.categoria_entry.pack(fill="x", padx=5, pady=5)
        
        # IVA
        ctk.CTkLabel(form_frame, text=get_text("iva_recomendado")).pack(anchor="w", padx=10, pady=(10, 0))
        self.iva_entry = ctk.CTkEntry(form_frame, placeholder_text="21.0")
        self.iva_entry.pack(fill="x", padx=10, pady=5)
        
        # Descripción
        ctk.CTkLabel(form_frame, text=get_text("descripcion")).pack(anchor="w", padx=10, pady=(10, 0))
        self.descripcion_text = ctk.CTkTextbox(form_frame, height=80)
        self.descripcion_text.pack(fill="x", padx=10, pady=5)
        
        # Imagen
        imagen_frame = ctk.CTkFrame(form_frame)
        imagen_frame.pack(fill="x", padx=10, pady=5)

        # Título y botón de configuración
        img_header_frame = ctk.CTkFrame(imagen_frame)
        img_header_frame.pack(fill="x", padx=5, pady=(5, 0))

        ctk.CTkLabel(img_header_frame, text=get_text("imagen")).pack(side="left", padx=5)

        config_btn = ctk.CTkButton(img_header_frame, text="⚙️", width=30, height=25,
                                 command=self.configurar_directorio_imagenes)
        config_btn.pack(side="right", padx=5)

        # Display de imagen
        self.imagen_display_frame = ctk.CTkFrame(imagen_frame)
        self.imagen_display_frame.pack(fill="x", padx=5, pady=5)

        self.imagen_display = ctk.CTkLabel(self.imagen_display_frame, text="", width=150, height=150)
        self.imagen_display.pack(side="left", padx=5, pady=5)

        # Info y botones de imagen
        img_info_frame = ctk.CTkFrame(self.imagen_display_frame)
        img_info_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.imagen_label = ctk.CTkLabel(img_info_frame, text="Ninguna imagen seleccionada",
                                       wraplength=200, justify="left")
        self.imagen_label.pack(anchor="w", padx=5, pady=5)

        img_btn_frame = ctk.CTkFrame(img_info_frame)
        img_btn_frame.pack(fill="x", padx=5, pady=5)

        imagen_btn = ctk.CTkButton(img_btn_frame, text=get_text("seleccionar_imagen"),
                                 command=self.seleccionar_imagen)
        imagen_btn.pack(side="top", fill="x", pady=2)

        self.quitar_imagen_btn = ctk.CTkButton(img_btn_frame, text="Quitar imagen",
                                             fg_color="#DC143C", hover_color="#B22222",
                                             command=self.quitar_imagen)
        self.quitar_imagen_btn.pack(side="top", fill="x", pady=2)
        
        # Botones del formulario
        buttons_form_frame = ctk.CTkFrame(form_frame)
        buttons_form_frame.pack(fill="x", padx=10, pady=20)
        self.logger.debug("Frame de botones del formulario creado y packed")

        # Primera fila de botones
        top_buttons_frame = ctk.CTkFrame(buttons_form_frame)
        top_buttons_frame.pack(fill="x", pady=(0, 5))

        nuevo_btn = ctk.CTkButton(top_buttons_frame, text=get_text("nuevo_producto"),
                                fg_color="#1f538d", hover_color="#14375e", command=self.nuevo_producto)
        nuevo_btn.pack(fill="x", padx=5)

        # Segunda fila de botones
        bottom_buttons_frame = ctk.CTkFrame(buttons_form_frame)
        bottom_buttons_frame.pack(fill="x", pady=5)
        self.logger.info(f"Frame inferior de botones creado: {bottom_buttons_frame}")

        guardar_btn = ctk.CTkButton(
            bottom_buttons_frame,
            text=get_text("guardar"),
            fg_color="#2E8B57",
            hover_color="#228B22",
            command=self.guardar_producto,
            width=120,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        guardar_btn.pack(side="left", padx=5, pady=5)
        self.logger.info(f"Botón 'Guardar' creado: {guardar_btn} en frame {bottom_buttons_frame}")

        cancelar_btn = ctk.CTkButton(
            bottom_buttons_frame,
            text=get_text("cancelar"),
            fg_color="#808080",
            hover_color="#696969",
            command=self.limpiar_formulario,
            width=120,
            height=35,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        cancelar_btn.pack(side="right", padx=5, pady=5)
        self.logger.info(f"Botón 'Cancelar' creado: {cancelar_btn} en frame {bottom_buttons_frame}")
    
    def load_productos(self):
        """Carga la lista de productos"""
        try:
            self.logger.debug("Cargando lista de productos desde la base de datos")

            # Verificar que la ventana y widgets existen antes de usarlos
            if not hasattr(self, 'window') or not self.window.winfo_exists():
                self.logger.warning("Ventana no existe, cancelando carga de productos")
                return

            if not hasattr(self, 'productos_listbox'):
                self.logger.warning("productos_listbox no existe, cancelando carga")
                return

            self.productos = Producto.get_all()
            log_database_operation("SELECT", "productos", f"Cargados {len(self.productos)} productos")

            # Verificar que el listbox aún existe antes de manipularlo
            try:
                self.productos_listbox.delete(0, tk.END)
            except tk.TclError as tcl_error:
                self.logger.warning(f"Error al acceder al listbox: {tcl_error}")
                return

            for producto in self.productos:
                display_text = f"{producto.nombre} - {producto.referencia} - €{producto.precio:.2f}"
                try:
                    self.productos_listbox.insert(tk.END, display_text)
                except tk.TclError as tcl_error:
                    self.logger.warning(f"Error al insertar en listbox: {tcl_error}")
                    break

            self.logger.info(f"Lista de productos actualizada: {len(self.productos)} productos")
        except Exception as e:
            log_exception(e, "load_productos")
            self.logger.error(f"Error al cargar productos: {str(e)}")
            # Mostrar error con parent correcto
            self._show_message("error", get_text("error"), f"Error al cargar productos: {str(e)}")
    
    def on_producto_select(self, event):
        """Maneja la selección de un producto en la lista"""
        try:
            selection = self.productos_listbox.curselection()
            if selection:
                index = selection[0]
                self.selected_producto = self.productos[index]
                self.logger.info(f"Producto seleccionado: {self.selected_producto.nombre} (ID: {getattr(self.selected_producto, 'id', 'N/A')})")
                self.logger.debug(f"Imagen del producto: {getattr(self.selected_producto, 'imagen_path', 'N/A')}")
                self.load_producto_to_form()
            else:
                self.logger.debug("No hay selección en la lista")
        except Exception as e:
            log_exception(e, "on_producto_select")
            self.logger.error(f"Error al seleccionar producto: {str(e)}")
    
    def load_producto_to_form(self):
        """Carga los datos del producto seleccionado en el formulario"""
        if self.selected_producto:
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, self.selected_producto.nombre)
            
            self.referencia_entry.delete(0, tk.END)
            self.referencia_entry.insert(0, self.selected_producto.referencia)
            
            self.precio_entry.delete(0, tk.END)
            self.precio_entry.insert(0, str(self.selected_producto.precio))
            
            self.categoria_entry.delete(0, tk.END)
            self.categoria_entry.insert(0, self.selected_producto.categoria)
            
            self.iva_entry.delete(0, tk.END)
            self.iva_entry.insert(0, str(self.selected_producto.iva_recomendado))
            
            self.descripcion_text.delete("1.0", tk.END)
            self.descripcion_text.insert("1.0", self.selected_producto.descripcion)
            
            # Cargar imagen del producto
            self.imagen_path = self.selected_producto.imagen_path or ""
            if self.imagen_path:
                filename = os.path.basename(self.imagen_path)
                self.imagen_label.configure(text=f"Imagen: {filename}")
                self.logger.debug(f"Cargando imagen del producto: {self.imagen_path}")
            else:
                self.imagen_label.configure(text="Ninguna imagen seleccionada")
                self.logger.debug("Producto sin imagen")

            # Actualizar el display de la imagen
            self.update_image_display()

    def nuevo_producto(self):
        """Prepara el formulario para un nuevo producto"""
        self.selected_producto = None
        self.limpiar_formulario()

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        try:
            # Verificar que la ventana existe antes de manipular widgets
            if not hasattr(self, 'window') or not self.window.winfo_exists():
                self.logger.warning("Ventana no existe, cancelando limpieza de formulario")
                return

            # Limpiar campos de entrada con verificación
            form_entries = [
                ('nombre_entry', ''),
                ('referencia_entry', ''),
                ('precio_entry', ''),
                ('categoria_entry', ''),
                ('iva_entry', '21.0')
            ]

            for entry_name, default_value in form_entries:
                if hasattr(self, entry_name):
                    entry_widget = getattr(self, entry_name)
                    try:
                        entry_widget.delete(0, tk.END)
                        if default_value:
                            entry_widget.insert(0, default_value)
                    except tk.TclError as e:
                        self.logger.warning(f"Error al limpiar {entry_name}: {e}")

            # Limpiar descripción
            if hasattr(self, 'descripcion_text'):
                try:
                    self.descripcion_text.delete("1.0", tk.END)
                except tk.TclError as e:
                    self.logger.warning(f"Error al limpiar descripcion_text: {e}")

            # Limpiar imagen
            self.imagen_path = ""
            if hasattr(self, 'imagen_label'):
                try:
                    self.imagen_label.configure(text="Ninguna imagen seleccionada")
                except tk.TclError as e:
                    self.logger.warning(f"Error al configurar imagen_label: {e}")

            # Actualizar display de imagen
            self.update_image_display()

            # Limpiar selección
            self.selected_producto = None

        except Exception as e:
            log_exception(e, "limpiar_formulario")
            self.logger.error(f"Error al limpiar formulario: {str(e)}")

    def seleccionar_imagen(self):
        """Abre el diálogo para seleccionar una imagen"""
        self.logger.info("Usuario hizo clic en 'Seleccionar Imagen'")
        log_user_action("Clic en seleccionar imagen", "Abriendo diálogo de selección")

        try:
            # Usar el répertoire par défaut configuré
            initial_dir = app_config.get_default_image_directory()
            self.logger.debug(f"Directorio inicial para selección: {initial_dir}")

            # Construir los tipos de archivos soportados correctamente
            supported_formats = app_config.get_supported_formats()
            filetypes_str = " ".join([f"*{fmt}" for fmt in supported_formats])
            self.logger.debug(f"Formatos soportados: {supported_formats}")

            # Asegurar que la ventana esté al frente antes del diálogo
            self.window.lift()
            self.window.focus_force()

            self.logger.info("Abriendo diálogo de selección de archivos")
            file_path = filedialog.askopenfilename(
                title=get_text("seleccionar_imagen"),
                initialdir=initial_dir,
                parent=self.window,  # ✅ AÑADIDO: Especificar parent para que aparezca encima
                filetypes=[
                    ("Imágenes", filetypes_str),
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("GIF files", "*.gif"),
                    ("BMP files", "*.bmp"),
                    ("Todos los archivos", "*.*")
                ]
            )
            self.logger.debug(f"Resultado del diálogo: {file_path if file_path else 'Cancelado'}")

            if file_path:
                # Crear directorio de imágenes si no existe
                images_dir = app_config.get_assets_directory()
                os.makedirs(images_dir, exist_ok=True)

                # Copiar imagen al directorio de la aplicación
                filename = os.path.basename(file_path)
                dest_path = os.path.join(images_dir, filename)

                try:
                    shutil.copy2(file_path, dest_path)
                    self.imagen_path = dest_path
                    self.imagen_label.configure(text=f"Imagen: {filename}")
                    self.update_image_display()

                    log_file_operation("COPY", file_path, f"Copiado a {dest_path}")
                    log_user_action("Imagen seleccionada", f"Archivo: {filename}")
                    self.logger.info(f"Imagen seleccionada y copiada: {filename}")
                except Exception as e:
                    error_msg = f"Error al copiar imagen: {str(e)}"
                    log_exception(e, "seleccionar_imagen - copy")
                    self._show_message("error", get_text("error"), error_msg)
            else:
                self.logger.debug("Usuario canceló la selección de imagen")

        except Exception as e:
            error_msg = f"Error al abrir el diálogo de selección: {str(e)}"
            self.logger.error(error_msg)
            log_exception(e, "seleccionar_imagen")
            self._show_message("error", get_text("error"), error_msg)

    def update_image_display(self):
        """Actualiza el display de la imagen"""
        # Verificar que la ventana y widgets existen antes de usarlos
        if not hasattr(self, 'window') or not self.window.winfo_exists():
            self.logger.debug("Ventana no existe, cancelando actualización de imagen")
            return

        if not hasattr(self, 'imagen_display') or not hasattr(self, 'quitar_imagen_btn'):
            self.logger.debug("Widgets de imagen no están inicializados aún")
            return

        try:
            self.logger.debug(f"Actualizando display de imagen. Path: '{self.imagen_path}'")

            if self.imagen_path and os.path.exists(self.imagen_path):
                self.logger.debug(f"Archivo de imagen existe: {self.imagen_path}")

                # Cargar y redimensionar la imagen
                display_size = app_config.get_image_display_size()
                self.logger.debug(f"Tamaño de display: {display_size}")

                image = Image.open(self.imagen_path)
                original_size = image.size
                image.thumbnail(display_size, Image.Resampling.LANCZOS)
                new_size = image.size

                self.logger.debug(f"Imagen redimensionada de {original_size} a {new_size}")

                # Convertir para tkinter
                photo = ImageTk.PhotoImage(image)

                # Actualizar el display
                self.imagen_display.configure(image=photo, text="")
                self.imagen_display.image = photo  # Mantener una referencia

                # Mostrar el botón para quitar
                self.quitar_imagen_btn.pack(side="top", fill="x", pady=2)

                self.logger.info(f"Imagen cargada y mostrada: {os.path.basename(self.imagen_path)}")
            else:
                if self.imagen_path:
                    self.logger.warning(f"Archivo de imagen no existe: {self.imagen_path}")
                else:
                    self.logger.debug("No hay imagen para mostrar")

                # Mostrar placeholder
                self.imagen_display.configure(image="", text="Sin imagen\n📷")
                self.imagen_display.image = None

                # Ocultar el botón para quitar
                self.quitar_imagen_btn.pack_forget()

        except Exception as e:
            print(f"Error al actualizar display de imagen: {e}")
            if hasattr(self, 'imagen_display'):
                self.imagen_display.configure(image="", text="Error\n❌")
                self.imagen_display.image = None

    def quitar_imagen(self):
        """Quita la imagen seleccionada"""
        self.imagen_path = ""
        if hasattr(self, 'imagen_label'):
            self.imagen_label.configure(text="Ninguna imagen seleccionada")
        self.update_image_display()

    def configurar_directorio_imagenes(self):
        """Abre el diálogo para configurar el directorio por défaut de imágenes"""
        try:
            current_dir = app_config.get_default_image_directory()

            # Asegurar que la ventana esté al frente antes del diálogo
            self.window.lift()
            self.window.focus_force()

            new_dir = filedialog.askdirectory(
                title="Seleccionar directorio por defecto para imágenes",
                initialdir=current_dir,
                parent=self.window  # ✅ AÑADIDO: Especificar parent para que aparezca encima
            )

            if new_dir:
                if app_config.set_default_image_directory(new_dir):
                    self._show_message("info", "Configuración",
                                     f"Directorio por defecto actualizado:\n{new_dir}")
                else:
                    self._show_message("error", "Error",
                                     "No se pudo establecer el directorio seleccionado")

        except Exception as e:
            error_msg = f"Error al configurar directorio: {str(e)}"
            self._show_message("error", get_text("error"), error_msg)

    def validate_form(self):
        """Valida los datos del formulario"""
        errors = []

        self.logger.debug("Iniciando validación del formulario")

        # Validar nombre
        if not self.nombre_entry.get().strip():
            error_msg = f"{get_text('nombre') or 'Nombre'}: {get_text('campo_requerido') or 'Este campo es requerido'}"
            errors.append(error_msg)
            self.logger.debug("Error: Nombre vacío")

        # Validar referencia
        if not self.referencia_entry.get().strip():
            error_msg = f"{get_text('referencia') or 'Referencia'}: {get_text('campo_requerido') or 'Este campo es requerido'}"
            errors.append(error_msg)
            self.logger.debug("Error: Referencia vacía")

        # Validar precio
        try:
            precio = float(self.precio_entry.get())
            if precio < 0:
                errors.append(get_text("precio_invalido") or "El precio debe ser un número válido")
                self.logger.debug(f"Error: Precio negativo: {precio}")
        except ValueError:
            errors.append(get_text("precio_invalido") or "El precio debe ser un número válido")
            self.logger.debug(f"Error: Precio inválido: {self.precio_entry.get()}")

        # Validar IVA
        try:
            iva = float(self.iva_entry.get())
            if iva < 0 or iva > 100:
                errors.append(get_text("iva_invalido") or "El IVA debe ser un número válido entre 0 y 100")
                self.logger.debug(f"Error: IVA fuera de rango: {iva}")
        except ValueError:
            errors.append(get_text("iva_invalido") or "El IVA debe ser un número válido entre 0 y 100")
            self.logger.debug(f"Error: IVA inválido: {self.iva_entry.get()}")

        self.logger.debug(f"Validación completada. Errores encontrados: {len(errors)}")
        return errors

    def guardar_producto(self):
        """Guarda el producto en la base de datos"""
        try:
            self.logger.info("Usuario hizo clic en 'Guardar'")
            log_user_action("Clic en guardar producto", "Iniciando validación y guardado")

            # Verificar que la ventana existe antes de proceder
            if not hasattr(self, 'window') or not self.window.winfo_exists():
                self.logger.warning("Ventana no existe, cancelando guardado")
                return

            errors = self.validate_form()
            self.logger.debug(f"Resultado de validate_form: {errors} (tipo: {type(errors)})")

            if errors:
                self.logger.warning(f"Errores de validación en formulario: {errors}")
                # Asegurar que errors es una lista
                if not isinstance(errors, list):
                    errors = [str(errors)]
                self._show_message("error", get_text("error"), "\n".join(errors))
                return

            # Crear o actualizar producto
            is_update = bool(self.selected_producto)
            if self.selected_producto:
                producto = self.selected_producto
                self.logger.info(f"Actualizando producto existente: {producto.referencia}")
            else:
                producto = Producto()
                self.logger.info("Creando nuevo producto")

            producto.nombre = self.nombre_entry.get().strip()
            producto.referencia = self.referencia_entry.get().strip()
            producto.precio = float(self.precio_entry.get())
            producto.categoria = self.categoria_entry.get().strip()
            producto.iva_recomendado = float(self.iva_entry.get())
            producto.descripcion = self.descripcion_text.get("1.0", tk.END).strip()
            producto.imagen_path = self.imagen_path

            producto.save()

            operation = "UPDATE" if is_update else "INSERT"
            log_database_operation(operation, "productos", f"Producto {producto.referencia}")
            log_user_action(f"Producto {'actualizado' if is_update else 'creado'}",
                          f"Referencia: {producto.referencia}, Nombre: {producto.nombre}")

            self._show_message("info", get_text("confirmar"), get_text("producto_guardado"))
            self.load_productos()
            self.limpiar_formulario()

        except Exception as e:
            log_exception(e, "guardar_producto")
            self._show_message("error", get_text("error"), f"Error al guardar producto: {str(e)}")

    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        if not self.selected_producto:
            self._show_message("warning", get_text("error"), "Seleccione un producto para eliminar")
            return

        if self._show_message("yesno", get_text("confirmar"), get_text("confirmar_eliminacion")):
            try:
                self.selected_producto.delete()
                self._show_message("info", get_text("confirmar"), get_text("producto_eliminado"))
                self.load_productos()
                self.limpiar_formulario()
            except Exception as e:
                self._show_message("error", get_text("error"), f"Error al eliminar producto: {str(e)}")
