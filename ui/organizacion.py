import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk
from utils.translations import get_text
from database.models import Organizacion
from utils.logger import get_logger, log_user_action, log_exception
from utils.logo_manager import LogoManager
from common.ui_components import FormHelper
from utils.config import Config

class OrganizacionWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Configuración de Organización")
        self.window.geometry("800x700")
        self.window.transient(parent)

        # Asegurar que la ventana aparezca al frente
        self.window.lift()
        self.window.focus_force()
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))

        # Logger y configuración
        self.logger = get_logger("organizacion")
        self.config = Config()
        self.logo_manager = LogoManager()

        # Variables
        self.organizacion = None
        self.logo_image = None
        self.logo_path = ""
        self.directorio_imagenes = ""
        self.directorio_pdf = ""
        self.visor_pdf_path = ""

        # Crear interfaz
        self.create_widgets()
        self.load_organizacion_data()

        self.logger.info("Ventana de organización inicializada")

    def _show_message(self, msg_type, title, message):
        """Mostrar mensaje copiable con la ventana como parent para evitar que quede en segundo plano"""
        try:
            # Importar las funciones de diálogos copiables
            from common.custom_dialogs import (
                show_copyable_info, show_copyable_error,
                show_copyable_warning, show_copyable_confirm
            )

            # Asegurar que la ventana esté al frente
            self.window.lift()
            self.window.focus_force()
            self.window.attributes('-topmost', True)

            # Usar diálogos copiables en lugar de messagebox estándar
            if msg_type == "info":
                result = show_copyable_info(self.window, title, message)
            elif msg_type == "error":
                result = show_copyable_error(self.window, title, message)
            elif msg_type == "question":
                result = show_copyable_confirm(self.window, title, message)
            else:
                result = show_copyable_info(self.window, title, message)

            # Restaurar estado normal
            self.window.attributes('-topmost', False)
            return result

        except Exception as e:
            # En caso de error, restaurar estado y mostrar mensaje básico
            try:
                self.window.attributes('-topmost', False)
            except:
                pass
            # Fallback sin parent
            if msg_type == "info":
                return messagebox.showinfo(title, message)
            elif msg_type == "error":
                return messagebox.showerror(title, message)
            elif msg_type == "question":
                return messagebox.askyesno(title, message)
            else:
                return messagebox.showinfo(title, message)

    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Configuración de Organización",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 30))

        # Crear secciones
        self.create_datos_basicos_section(main_frame)
        self.create_logo_section(main_frame)
        self.create_configuracion_section(main_frame)
        self.create_buttons_section(main_frame)

    def create_datos_basicos_section(self, parent):
        """Crear sección de datos básicos"""
        # Frame para datos básicos
        datos_frame = ctk.CTkFrame(parent)
        datos_frame.pack(fill="x", pady=(0, 20))

        section_label = ctk.CTkLabel(
            datos_frame,
            text="📋 Datos Básicos de la Organización",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_label.pack(pady=(20, 15))

        # Grid para organizar los campos
        fields_frame = ctk.CTkFrame(datos_frame)
        fields_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Nombre de la organización
        ctk.CTkLabel(fields_frame, text="Nombre de la Organización *:").grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )
        self.nombre_entry = ctk.CTkEntry(fields_frame, width=300, placeholder_text="Ej: Mi Empresa S.L.")
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # CIF
        ctk.CTkLabel(fields_frame, text="CIF/NIF:").grid(
            row=1, column=0, sticky="w", padx=10, pady=10
        )
        self.cif_entry = ctk.CTkEntry(fields_frame, width=300, placeholder_text="Ej: B12345678")
        self.cif_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Dirección
        ctk.CTkLabel(fields_frame, text="Dirección:").grid(
            row=2, column=0, sticky="w", padx=10, pady=10
        )
        self.direccion_entry = ctk.CTkEntry(fields_frame, width=300, placeholder_text="Calle, número, ciudad, CP")
        self.direccion_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Teléfono
        ctk.CTkLabel(fields_frame, text="Teléfono:").grid(
            row=3, column=0, sticky="w", padx=10, pady=10
        )
        self.telefono_entry = ctk.CTkEntry(fields_frame, width=300, placeholder_text="Ej: +34 91 123 45 67")
        self.telefono_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Email
        ctk.CTkLabel(fields_frame, text="Email:").grid(
            row=4, column=0, sticky="w", padx=10, pady=10
        )
        self.email_entry = ctk.CTkEntry(fields_frame, width=300, placeholder_text="info@miempresa.com")
        self.email_entry.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Configurar expansión de columnas
        fields_frame.grid_columnconfigure(1, weight=1)

    def create_logo_section(self, parent):
        """Crear sección de gestión del logo"""
        # Frame para logo
        logo_frame = ctk.CTkFrame(parent)
        logo_frame.pack(fill="x", pady=(0, 20))

        section_label = ctk.CTkLabel(
            logo_frame,
            text="🖼️ Logo de la Organización",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_label.pack(pady=(20, 15))

        # Frame horizontal para logo y controles
        logo_content_frame = ctk.CTkFrame(logo_frame)
        logo_content_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Frame izquierdo para la imagen
        logo_display_frame = ctk.CTkFrame(logo_content_frame)
        logo_display_frame.pack(side="left", padx=(10, 20), pady=10)

        # Label para mostrar la imagen del logo
        self.logo_label = ctk.CTkLabel(
            logo_display_frame,
            text="Sin logo\nseleccionado",
            width=150,
            height=150,
            fg_color="gray90",
            corner_radius=10
        )
        self.logo_label.pack(padx=10, pady=10)

        # Frame derecho para controles
        logo_controls_frame = ctk.CTkFrame(logo_content_frame)
        logo_controls_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        # Botones de control del logo
        select_logo_btn = ctk.CTkButton(
            logo_controls_frame,
            text="📁 Seleccionar Logo",
            command=self.select_logo,
            width=200
        )
        select_logo_btn.pack(pady=10)

        remove_logo_btn = ctk.CTkButton(
            logo_controls_frame,
            text="🗑️ Quitar Logo",
            command=self.remove_logo,
            fg_color="#DC143C",
            hover_color="#B22222",
            width=200
        )
        remove_logo_btn.pack(pady=5)

        # Información sobre el logo
        info_label = ctk.CTkLabel(
            logo_controls_frame,
            text="Formatos soportados:\nPNG, JPG, JPEG, GIF, BMP\nTamaño recomendado: 200x200px",
            justify="left"
        )
        info_label.pack(pady=10)

        # Label para mostrar la ruta del logo
        self.logo_path_label = ctk.CTkLabel(
            logo_controls_frame,
            text="Ruta: Ninguna",
            wraplength=300,
            justify="left"
        )
        self.logo_path_label.pack(pady=5)

    def create_configuracion_section(self, parent):
        """Crear sección de configuración adicional"""
        # Frame para configuración
        config_frame = ctk.CTkFrame(parent)
        config_frame.pack(fill="x", pady=(0, 20))

        section_label = ctk.CTkLabel(
            config_frame,
            text="⚙️ Configuración Adicional",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        section_label.pack(pady=(20, 15))

        # Frame para campos de configuración
        config_fields_frame = ctk.CTkFrame(config_frame)
        config_fields_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Directorio por defecto para imágenes de productos
        ctk.CTkLabel(config_fields_frame, text="Directorio por defecto para imágenes de productos:").grid(
            row=0, column=0, sticky="w", padx=10, pady=10, columnspan=2
        )

        dir_frame = ctk.CTkFrame(config_fields_frame)
        dir_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.directorio_entry = ctk.CTkEntry(
            dir_frame,
            placeholder_text="Seleccione un directorio...",
            width=400
        )
        self.directorio_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        select_dir_btn = ctk.CTkButton(
            dir_frame,
            text="📁 Seleccionar",
            command=self.select_directorio,
            width=100
        )
        select_dir_btn.pack(side="right", padx=10, pady=10)

        # Directorio por defecto para descargas de PDF
        ctk.CTkLabel(config_fields_frame, text="Directorio por defecto para descargas de PDF:").grid(
            row=2, column=0, sticky="w", padx=10, pady=10, columnspan=2
        )

        pdf_dir_frame = ctk.CTkFrame(config_fields_frame)
        pdf_dir_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.directorio_pdf_entry = ctk.CTkEntry(
            pdf_dir_frame,
            placeholder_text="Seleccione un directorio para PDFs...",
            width=400
        )
        self.directorio_pdf_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        select_pdf_dir_btn = ctk.CTkButton(
            pdf_dir_frame,
            text="📁 Seleccionar",
            command=self.select_directorio_pdf,
            width=100
        )
        select_pdf_dir_btn.pack(side="right", padx=10, pady=10)

        # Visor PDF personalizado
        ctk.CTkLabel(config_fields_frame, text="Visor PDF personalizado (opcional):").grid(
            row=4, column=0, sticky="w", padx=10, pady=10, columnspan=2
        )

        pdf_viewer_frame = ctk.CTkFrame(config_fields_frame)
        pdf_viewer_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.visor_pdf_entry = ctk.CTkEntry(
            pdf_viewer_frame,
            placeholder_text="Ruta al ejecutable del visor PDF (dejar vacío para usar el predeterminado)...",
            width=400
        )
        self.visor_pdf_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        select_pdf_viewer_btn = ctk.CTkButton(
            pdf_viewer_frame,
            text="📁 Seleccionar",
            command=self.select_visor_pdf,
            width=100
        )
        select_pdf_viewer_btn.pack(side="right", padx=10, pady=10)

        # Número inicial de facturas
        ctk.CTkLabel(config_fields_frame, text="Número inicial para serie de facturas:").grid(
            row=6, column=0, sticky="w", padx=10, pady=10
        )
        self.numero_inicial_entry = ctk.CTkEntry(
            config_fields_frame,
            width=150,
            placeholder_text="1"
        )
        self.numero_inicial_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Información adicional
        info_frame = ctk.CTkFrame(config_fields_frame)
        info_frame.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        info_text = ctk.CTkLabel(
            info_frame,
            text="💡 Información:\n" +
                 "• El directorio de imágenes se usará como ubicación por defecto al agregar imágenes a productos\n" +
                 "• El directorio de PDF se usará para guardar y abrir automáticamente las facturas generadas\n" +
                 "• El visor PDF personalizado permite elegir qué programa usar para abrir PDFs (Adobe Reader, Foxit, etc.)\n" +
                 "• Si no se especifica visor personalizado, se usará el predeterminado del sistema\n" +
                 "• El número inicial de facturas se aplicará cuando se configure una nueva serie de numeración\n" +
                 "• Estos ajustes se pueden cambiar en cualquier momento",
            justify="left",
            wraplength=600
        )
        info_text.pack(padx=15, pady=15)

        # Configurar expansión de columnas
        config_fields_frame.grid_columnconfigure(1, weight=1)

    def create_buttons_section(self, parent):
        """Crear sección de botones"""
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", pady=20)

        # Frame interno para centrar botones
        buttons_inner_frame = ctk.CTkFrame(buttons_frame)
        buttons_inner_frame.pack(pady=20)

        # Botón Guardar
        save_btn = ctk.CTkButton(
            buttons_inner_frame,
            text="💾 Guardar Configuración",
            command=self.save_organizacion,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        save_btn.pack(side="left", padx=10)

        # Botón Cancelar
        cancel_btn = ctk.CTkButton(
            buttons_inner_frame,
            text="❌ Cancelar",
            command=self.cancel,
            fg_color="#6B6B6B",
            hover_color="#5A5A5A",
            width=150,
            height=40
        )
        cancel_btn.pack(side="left", padx=10)

        # Botón Restablecer
        reset_btn = ctk.CTkButton(
            buttons_inner_frame,
            text="🔄 Restablecer",
            command=self.reset_form,
            fg_color="#FF8C00",
            hover_color="#FF7F00",
            width=150,
            height=40
        )
        reset_btn.pack(side="left", padx=10)

    def load_organizacion_data(self):
        """Cargar datos existentes de la organización"""
        try:
            self.organizacion = Organizacion.get()

            # Cargar datos básicos
            FormHelper.set_entry_value(self.nombre_entry, self.organizacion.nombre)
            FormHelper.set_entry_value(self.cif_entry, self.organizacion.cif)
            FormHelper.set_entry_value(self.direccion_entry, self.organizacion.direccion)
            FormHelper.set_entry_value(self.telefono_entry, self.organizacion.telefono)
            FormHelper.set_entry_value(self.email_entry, self.organizacion.email)

            # Cargar configuración adicional
            FormHelper.set_entry_value(self.directorio_entry, self.organizacion.directorio_imagenes_defecto)
            FormHelper.set_entry_value(self.directorio_pdf_entry, self.organizacion.directorio_descargas_pdf)
            FormHelper.set_entry_value(self.visor_pdf_entry, self.organizacion.visor_pdf_personalizado)
            FormHelper.set_entry_value(self.numero_inicial_entry, str(self.organizacion.numero_factura_inicial))

            # Cargar logo si existe
            if self.organizacion.logo_path and os.path.exists(self.organizacion.logo_path):
                self.logo_path = self.organizacion.logo_path
                self.load_logo_image(self.logo_path)

            self.logger.info("Datos de organización cargados correctamente")

        except Exception as e:
            log_exception(e, "load_organizacion_data")
            self.logger.error(f"Error cargando datos de organización: {e}")

    def select_logo(self):
        """Seleccionar archivo de logo"""
        try:
            file_types = [
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("GIF", "*.gif"),
                ("BMP", "*.bmp"),
                ("Todos los archivos", "*.*")
            ]

            # Asegurar que la ventana esté al frente antes de abrir el diálogo
            self.window.lift()
            self.window.focus_force()
            self.window.attributes('-topmost', True)

            # Usar la ventana como parent para el diálogo
            filename = filedialog.askopenfilename(
                parent=self.window,
                title="Seleccionar Logo",
                filetypes=file_types,
                initialdir=self.config.get_default_image_directory()
            )

            # Restaurar el comportamiento normal de la ventana
            self.window.attributes('-topmost', False)

            if filename:
                # Copier le logo vers le répertoire permanent
                organization_name = self.nombre_entry.get() if hasattr(self, 'nombre_entry') else "organization"
                permanent_logo_path = self.logo_manager.save_logo(filename, organization_name)

                if permanent_logo_path:
                    # Supprimer l'ancien logo s'il existe
                    if self.logo_path and self.logo_path != permanent_logo_path:
                        self.logo_manager.remove_logo(self.logo_path)

                    self.logo_path = permanent_logo_path
                    self.load_logo_image(permanent_logo_path)
                    self.logger.info(f"Logo seleccionado y copiado: {filename} -> {permanent_logo_path}")
                    log_user_action("Logo seleccionado", permanent_logo_path)
                else:
                    self.logger.error(f"Error al copiar logo: {filename}")
                    self._show_message("error", "Error", "Error al guardar el logo. Verifique que el archivo sea una imagen válida.")

        except Exception as e:
            log_exception(e, "select_logo")
            # Asegurar que la ventana vuelva al estado normal en caso de error
            try:
                self.window.attributes('-topmost', False)
            except:
                pass
            self._show_message("error", "Error", f"Error al seleccionar logo: {str(e)}")

    def load_logo_image(self, image_path):
        """Cargar y mostrar imagen del logo con manejo robusto de errores TclError"""
        try:
            if not os.path.exists(image_path):
                self.logger.warning(f"Archivo de logo no existe: {image_path}")
                self.remove_logo()
                return

            # Actualizar la ruta del logo ANTES de cualquier operación
            self.logo_path = image_path

            # Limpiar completamente la imagen anterior
            self._clear_previous_logo_image()

            # Cargar y procesar imagen con manejo de errores
            pil_image = self._load_and_process_image(image_path)
            if pil_image is None:
                return

            # Crear CTkImage con configuración robusta
            success = self._create_and_display_ctk_image(pil_image, image_path)
            if not success:
                return

            self.logger.info(f"Logo cargado correctamente: {os.path.basename(image_path)}")

        except Exception as e:
            log_exception(e, "load_logo_image")
            self.logger.error(f"Error cargando imagen del logo: {e}")
            # Limpiar completamente en caso de error
            self.remove_logo()
            self._show_message("error", "Error", f"Error al cargar la imagen: {str(e)}")

    def _clear_previous_logo_image(self):
        """Limpiar completamente la imagen anterior"""
        try:
            # Limpiar referencia de imagen
            if hasattr(self, 'logo_image') and self.logo_image is not None:
                try:
                    del self.logo_image
                except:
                    pass
            self.logo_image = None

            # Limpiar el label de forma segura
            try:
                self.logo_label.configure(image="", text="Cargando...")
            except:
                try:
                    self.logo_label.configure(text="Cargando...")
                except:
                    pass

        except Exception as e:
            self.logger.debug(f"Error limpiando imagen anterior: {e}")

    def _load_and_process_image(self, image_path):
        """Cargar y procesar imagen PIL"""
        try:
            # Cargar imagen
            pil_image = Image.open(image_path)

            # Crear una copia para evitar problemas de referencia
            pil_image = pil_image.copy()

            # Convertir a RGB si es necesario (para evitar problemas con algunos formatos)
            if pil_image.mode not in ('RGB', 'RGBA'):
                pil_image = pil_image.convert('RGB')

            # Redimensionar manteniendo proporción
            pil_image.thumbnail((140, 140), Image.Resampling.LANCZOS)

            return pil_image

        except Exception as e:
            self.logger.error(f"Error procesando imagen: {e}")
            return None

    def _create_and_display_ctk_image(self, pil_image, image_path):
        """Crear CTkImage y mostrar en el label"""
        try:
            # Crear CTkImage con configuración muy robusta
            self.logo_image = ctk.CTkImage(
                light_image=pil_image,
                dark_image=pil_image,
                size=(140, 140)
            )

            # Intentar configurar el label con múltiples fallbacks
            success = self._configure_logo_label_safe()
            if not success:
                return False

            # Actualizar label de ruta
            try:
                self.logo_path_label.configure(text=f"Ruta: {os.path.basename(image_path)}")
            except Exception as e:
                self.logger.debug(f"Error actualizando label de ruta: {e}")

            return True

        except Exception as e:
            self.logger.error(f"Error creando CTkImage: {e}")
            return False

    def _configure_logo_label_safe(self):
        """Configurar el label del logo de forma segura con múltiples intentos"""
        attempts = [
            # Intento 1: Configuración normal
            lambda: self.logo_label.configure(image=self.logo_image, text=""),
            # Intento 2: Solo imagen
            lambda: self.logo_label.configure(image=self.logo_image),
            # Intento 3: Forzar actualización
            lambda: (self.logo_label.configure(image=""),
                    self.logo_label.configure(image=self.logo_image, text="")),
        ]

        for i, attempt in enumerate(attempts, 1):
            try:
                attempt()
                self.logger.debug(f"Logo configurado exitosamente en intento {i}")
                return True
            except Exception as e:
                self.logger.debug(f"Intento {i} falló: {e}")
                continue

        self.logger.error("Todos los intentos de configurar logo fallaron")
        return False

    def remove_logo(self):
        """Quitar logo seleccionado"""
        try:
            self.logo_path = ""

            # Limpiar imagen anterior si existe
            if hasattr(self, 'logo_image') and self.logo_image is not None:
                try:
                    del self.logo_image
                except:
                    pass
            self.logo_image = None

            # Restaurar el label a su estado inicial
            try:
                self.logo_label.configure(
                    image="",
                    text="Sin logo\nseleccionado"
                )
            except Exception as label_error:
                # Si hay error configurando el label, intentar solo el texto
                try:
                    self.logo_label.configure(text="Sin logo\nseleccionado")
                except:
                    pass  # Si aún hay error, ignorar
            self.logo_path_label.configure(text="Ruta: Ninguna")

            self.logger.info("Logo removido")
            log_user_action("Logo removido", "")

        except Exception as e:
            log_exception(e, "remove_logo")
            self.logger.error(f"Error removiendo logo: {e}")

    def select_directorio(self):
        """Seleccionar directorio por defecto para imágenes"""
        try:
            # Asegurar que la ventana esté al frente antes de abrir el diálogo
            self.window.lift()
            self.window.focus_force()
            self.window.attributes('-topmost', True)

            # Usar la ventana como parent para el diálogo
            directorio = filedialog.askdirectory(
                parent=self.window,
                title="Seleccionar Directorio por Defecto para Imágenes",
                initialdir=self.config.get_default_image_directory()
            )

            # Restaurar el comportamiento normal de la ventana
            self.window.attributes('-topmost', False)

            if directorio:
                self.directorio_imagenes = directorio
                FormHelper.set_entry_value(self.directorio_entry, directorio)
                self.logger.info(f"Directorio seleccionado: {directorio}")
                log_user_action("Directorio de imágenes seleccionado", directorio)

        except Exception as e:
            log_exception(e, "select_directorio")
            # Asegurar que la ventana vuelva al estado normal en caso de error
            try:
                self.window.attributes('-topmost', False)
            except:
                pass
            self._show_message("error", "Error", f"Error al seleccionar directorio: {str(e)}")

    def select_directorio_pdf(self):
        """Seleccionar directorio por defecto para descargas de PDF"""
        try:
            # Asegurar que la ventana esté al frente antes de abrir el diálogo
            self.window.lift()
            self.window.focus_force()
            self.window.attributes('-topmost', True)

            # Obtener directorio inicial (usar el actual si existe, sino el de descargas del usuario)
            initial_dir = self.directorio_pdf_entry.get().strip()
            if not initial_dir or not os.path.exists(initial_dir):
                initial_dir = os.path.expanduser("~/Downloads")

            # Usar la ventana como parent para el diálogo
            directorio = filedialog.askdirectory(
                parent=self.window,
                title="Seleccionar Directorio por Defecto para Descargas de PDF",
                initialdir=initial_dir
            )

            # Restaurar el comportamiento normal de la ventana
            self.window.attributes('-topmost', False)

            if directorio:
                self.directorio_pdf = directorio
                FormHelper.set_entry_value(self.directorio_pdf_entry, directorio)
                self.logger.info(f"Directorio PDF seleccionado: {directorio}")
                log_user_action("Directorio de PDF seleccionado", directorio)

        except Exception as e:
            log_exception(e, "select_directorio_pdf")
            # Asegurar que la ventana vuelva al estado normal en caso de error
            try:
                self.window.attributes('-topmost', False)
            except:
                pass
            self._show_message("error", "Error", f"Error al seleccionar directorio PDF: {str(e)}")

    def select_visor_pdf(self):
        """Seleccionar ejecutable del visor PDF personalizado"""
        try:
            # Asegurar que la ventana esté al frente antes de abrir el diálogo
            self.window.lift()
            self.window.focus_force()
            self.window.attributes('-topmost', True)

            # Obtener archivo inicial (usar el actual si existe)
            initial_file = self.visor_pdf_entry.get().strip()
            initial_dir = os.path.dirname(initial_file) if initial_file and os.path.exists(initial_file) else None

            # Definir tipos de archivo según el sistema operativo
            import platform
            system = platform.system()

            if system == "Windows":
                file_types = [
                    ("Ejecutables", "*.exe"),
                    ("Todos los archivos", "*.*")
                ]
                if not initial_dir:
                    initial_dir = "C:\\Program Files"
            elif system == "Darwin":  # macOS
                file_types = [
                    ("Aplicaciones", "*.app"),
                    ("Ejecutables", "*"),
                    ("Todos los archivos", "*.*")
                ]
                if not initial_dir:
                    initial_dir = "/Applications"
            else:  # Linux
                file_types = [
                    ("Ejecutables", "*"),
                    ("Todos los archivos", "*.*")
                ]
                if not initial_dir:
                    initial_dir = "/usr/bin"

            # Usar la ventana como parent para el diálogo
            archivo = filedialog.askopenfilename(
                parent=self.window,
                title="Seleccionar Visor PDF Personalizado",
                initialdir=initial_dir,
                filetypes=file_types
            )

            # Restaurar el comportamiento normal de la ventana
            self.window.attributes('-topmost', False)

            if archivo:
                self.visor_pdf_path = archivo
                FormHelper.set_entry_value(self.visor_pdf_entry, archivo)
                self.logger.info(f"Visor PDF seleccionado: {archivo}")
                log_user_action("Visor PDF seleccionado", archivo)

        except Exception as e:
            log_exception(e, "select_visor_pdf")
            # Asegurar que la ventana vuelva al estado normal en caso de error
            try:
                self.window.attributes('-topmost', False)
            except:
                pass
            self._show_message("error", "Error", f"Error al seleccionar visor PDF: {str(e)}")

    def validate_form(self):
        """Validar datos del formulario"""
        errors = []

        # Nombre es obligatorio
        if not self.nombre_entry.get().strip():
            errors.append("El nombre de la organización es obligatorio")

        # Validar CIF si se proporciona
        cif = self.cif_entry.get().strip()
        if cif and len(cif) < 8:
            errors.append("El CIF debe tener al menos 8 caracteres")

        # Validar email si se proporciona
        email = self.email_entry.get().strip()
        if email and "@" not in email:
            errors.append("El email no tiene un formato válido")

        # Validar número inicial
        try:
            numero_inicial = int(self.numero_inicial_entry.get() or "1")
            if numero_inicial < 1:
                errors.append("El número inicial debe ser mayor que 0")
        except ValueError:
            errors.append("El número inicial debe ser un número válido")

        return errors

    def save_organizacion(self):
        """Guardar datos de la organización"""
        try:
            # Validar formulario
            errors = self.validate_form()
            if errors:
                error_message = "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"• {error}" for error in errors)
                self._show_message("error", "Errores de Validación", error_message)
                return

            # Crear objeto organización con los datos del formulario
            organizacion = Organizacion(
                nombre=self.nombre_entry.get().strip(),
                cif=self.cif_entry.get().strip(),
                direccion=self.direccion_entry.get().strip(),
                telefono=self.telefono_entry.get().strip(),
                email=self.email_entry.get().strip(),
                logo_path=self.logo_path,
                directorio_imagenes_defecto=self.directorio_entry.get().strip(),
                numero_factura_inicial=int(self.numero_inicial_entry.get() or "1"),
                directorio_descargas_pdf=self.directorio_pdf_entry.get().strip(),
                visor_pdf_personalizado=self.visor_pdf_entry.get().strip()
            )

            # Guardar en base de datos
            organizacion.save()

            # Nettoyer les logos orphelins (garder seulement le logo actuel)
            if self.logo_path:
                self.logo_manager.cleanup_orphaned_logos(self.logo_path)

            # Actualizar configuración global si es necesario
            if organizacion.directorio_imagenes_defecto:
                self.config.set_default_image_directory(organizacion.directorio_imagenes_defecto)

            # Mostrar mensaje de éxito
            self._show_message(
                "info",
                "Éxito",
                "La configuración de la organización se ha guardado correctamente."
            )

            self.logger.info("Configuración de organización guardada correctamente")
            log_user_action("Organización guardada", f"Nombre: {organizacion.nombre}")

            # Cerrar ventana
            self.window.destroy()

        except Exception as e:
            log_exception(e, "save_organizacion")
            self._show_message("error", "Error", f"Error al guardar la configuración: {str(e)}")

    def reset_form(self):
        """Restablecer formulario a valores originales"""
        try:
            if self._show_message("question", "Confirmar", "¿Está seguro de que desea restablecer todos los campos?"):
                self.load_organizacion_data()
                self.logger.info("Formulario restablecido")
                log_user_action("Formulario restablecido", "")
        except Exception as e:
            log_exception(e, "reset_form")

    def cancel(self):
        """Cancelar y cerrar ventana"""
        try:
            if self.has_unsaved_changes():
                if self._show_message("question", "Confirmar", "Hay cambios sin guardar. ¿Está seguro de que desea salir?"):
                    self.window.destroy()
            else:
                self.window.destroy()
        except Exception as e:
            log_exception(e, "cancel")
            self.window.destroy()

    def has_unsaved_changes(self):
        """Verificar si hay cambios sin guardar"""
        try:
            if not self.organizacion:
                return True

            # Comparar valores actuales con los originales
            current_data = {
                'nombre': self.nombre_entry.get().strip(),
                'cif': self.cif_entry.get().strip(),
                'direccion': self.direccion_entry.get().strip(),
                'telefono': self.telefono_entry.get().strip(),
                'email': self.email_entry.get().strip(),
                'logo_path': self.logo_path,
                'directorio_imagenes_defecto': self.directorio_entry.get().strip(),
                'numero_factura_inicial': int(self.numero_inicial_entry.get() or "1")
            }

            original_data = {
                'nombre': self.organizacion.nombre,
                'cif': self.organizacion.cif,
                'direccion': self.organizacion.direccion,
                'telefono': self.organizacion.telefono,
                'email': self.organizacion.email,
                'logo_path': self.organizacion.logo_path,
                'directorio_imagenes_defecto': self.organizacion.directorio_imagenes_defecto,
                'numero_factura_inicial': self.organizacion.numero_factura_inicial
            }

            return current_data != original_data

        except Exception as e:
            log_exception(e, "has_unsaved_changes")
            return False
