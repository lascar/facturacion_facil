import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from utils.translations import get_text
from utils.logger import get_logger, log_user_action
from database.models import Cliente
from common.ui_components import BaseWindow, FormHelper
from common.validators import FormValidator
from common.treeview_sorter import add_sorting_to_treeview

class ClientesWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, "Gestión de Clientes", "1000x700")
        self.logger = get_logger(__name__)
        self.selected_cliente = None
        self.current_cliente = None
        
        self.create_widgets()
        self.load_clientes()
        
        log_user_action("Ventana de clientes abierta")
        self.logger.info("Ventana de clientes inicializada")
    
    def create_widgets(self):
        """Crea los widgets de la ventana"""
        # Configurar frame scrollable
        main_frame = self.setup_scrollable_frame(1000, 700)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Gestión de Clientes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)

        # Frame principal de contenido
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame superior - Lista de clientes
        top_frame = ctk.CTkFrame(content_frame)
        top_frame.pack(side="top", fill="x", pady=(0, 5))
        top_frame.configure(height=300)  # Hauteur fixe pour la liste

        self.create_clientes_list(top_frame)

        # Frame inferior - Formulario de cliente
        bottom_frame = ctk.CTkFrame(content_frame)
        bottom_frame.pack(side="bottom", fill="both", expand=True, pady=(5, 0))

        self.create_cliente_form(bottom_frame)

    def create_clientes_list(self, parent):
        """Crea la lista de clientes"""
        # Título y barra de búsqueda
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(header_frame, text="Lista de Clientes",
                   font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", pady=5)
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(header_frame)
        search_frame.pack(side="right", padx=10)
        
        ctk.CTkLabel(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(search_frame, width=200)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Lista de clientes con Treeview
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear Treeview para mostrar clientes
        columns = ("Nombre", "DNI/NIE", "Email", "Teléfono")
        self.clientes_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        
        # Configurar columnas
        self.clientes_tree.heading("Nombre", text="Nombre")
        self.clientes_tree.heading("DNI/NIE", text="DNI/NIE")
        self.clientes_tree.heading("Email", text="Email")
        self.clientes_tree.heading("Teléfono", text="Teléfono")
        
        self.clientes_tree.column("Nombre", width=250)
        self.clientes_tree.column("DNI/NIE", width=120)
        self.clientes_tree.column("Email", width=200)
        self.clientes_tree.column("Teléfono", width=120)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        self.clientes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Agregar ordenamiento
        add_sorting_to_treeview(self.clientes_tree)
        
        # Bind eventos
        self.clientes_tree.bind("<<TreeviewSelect>>", self.on_cliente_select)
        self.clientes_tree.bind("<Double-1>", self.on_cliente_double_click)

    def create_cliente_form(self, parent):
        """Crea el formulario de cliente"""
        # Título del formulario
        form_title = ctk.CTkLabel(parent, text="Datos del Cliente",
                                font=ctk.CTkFont(size=16, weight="bold"))
        form_title.pack(pady=(10, 5))
        
        # Frame del formulario
        form_frame = ctk.CTkFrame(parent)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campos del formulario en grid
        # Nombre (obligatorio)
        ctk.CTkLabel(form_frame, text="Nombre *:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.nombre_entry = ctk.CTkEntry(form_frame, width=300)
        self.nombre_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # DNI/NIE
        ctk.CTkLabel(form_frame, text="DNI/NIE:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.dni_nie_entry = ctk.CTkEntry(form_frame, width=200)
        self.dni_nie_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Email
        ctk.CTkLabel(form_frame, text="Email:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = ctk.CTkEntry(form_frame, width=300)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Teléfono
        ctk.CTkLabel(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.telefono_entry = ctk.CTkEntry(form_frame, width=200)
        self.telefono_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Dirección
        ctk.CTkLabel(form_frame, text="Dirección:").grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        self.direccion_text = ctk.CTkTextbox(form_frame, width=300, height=80)
        self.direccion_text.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        # Configurar expansión de columnas
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Botones de acción
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        self.nuevo_btn = ctk.CTkButton(buttons_frame, text="Nuevo Cliente", command=self.nuevo_cliente)
        self.nuevo_btn.pack(side="left", padx=5)
        
        self.guardar_btn = ctk.CTkButton(buttons_frame, text="Guardar", command=self.guardar_cliente)
        self.guardar_btn.pack(side="left", padx=5)
        
        self.eliminar_btn = ctk.CTkButton(buttons_frame, text="Eliminar", command=self.eliminar_cliente)
        self.eliminar_btn.pack(side="left", padx=5)
        
        self.limpiar_btn = ctk.CTkButton(buttons_frame, text="Limpiar", command=self.limpiar_formulario)
        self.limpiar_btn.pack(side="left", padx=5)

    def load_clientes(self):
        """Carga la lista de clientes"""
        try:
            # Limpiar la lista
            for item in self.clientes_tree.get_children():
                self.clientes_tree.delete(item)

            # Obtener clientes
            clientes = Cliente.get_all()

            # Agregar clientes a la lista
            for cliente in clientes:
                self.clientes_tree.insert("", "end", values=(
                    cliente.nombre,
                    cliente.dni_nie or "",
                    cliente.email or "",
                    cliente.telefono or ""
                ), tags=(cliente.id,))

            self.logger.debug(f"Cargados {len(clientes)} clientes")

        except Exception as e:
            self.logger.error(f"Error cargando clientes: {e}")
            messagebox.showerror("Error", f"Error cargando clientes: {e}")

    def on_search(self, event=None):
        """Maneja la búsqueda de clientes"""
        search_term = self.search_entry.get().strip()

        try:
            # Limpiar la lista
            for item in self.clientes_tree.get_children():
                self.clientes_tree.delete(item)

            if search_term:
                # Buscar clientes
                clientes = Cliente.search(search_term)
            else:
                # Mostrar todos los clientes
                clientes = Cliente.get_all()

            # Agregar clientes a la lista
            for cliente in clientes:
                self.clientes_tree.insert("", "end", values=(
                    cliente.nombre,
                    cliente.dni_nie or "",
                    cliente.email or "",
                    cliente.telefono or ""
                ), tags=(cliente.id,))

        except Exception as e:
            self.logger.error(f"Error en búsqueda: {e}")

    def on_cliente_select(self, event=None):
        """Maneja la selección de un cliente"""
        selection = self.clientes_tree.selection()
        if selection:
            item = self.clientes_tree.item(selection[0])
            cliente_id = item['tags'][0] if item['tags'] else None

            if cliente_id:
                self.selected_cliente = Cliente.get_by_id(cliente_id)
                self.load_cliente_data()

    def on_cliente_double_click(self, event=None):
        """Maneja el doble clic en un cliente"""
        self.on_cliente_select()

    def load_cliente_data(self):
        """Carga los datos del cliente seleccionado en el formulario"""
        if not self.selected_cliente:
            return

        try:
            cliente = self.selected_cliente
            self.current_cliente = cliente

            # Cargar datos en el formulario
            FormHelper.set_entry_value(self.nombre_entry, cliente.nombre)
            FormHelper.set_entry_value(self.dni_nie_entry, cliente.dni_nie or "")
            FormHelper.set_entry_value(self.email_entry, cliente.email or "")
            FormHelper.set_entry_value(self.telefono_entry, cliente.telefono or "")
            FormHelper.set_text_value(self.direccion_text, cliente.direccion or "")

            self.logger.debug(f"Datos del cliente {cliente.nombre} cargados")

        except Exception as e:
            self.logger.error(f"Error cargando datos del cliente: {e}")
            messagebox.showerror("Error", f"Error cargando datos del cliente: {e}")

    def nuevo_cliente(self):
        """Prepara el formulario para un nuevo cliente"""
        self.current_cliente = None
        self.selected_cliente = None
        self.limpiar_formulario()
        self.nombre_entry.focus()
        log_user_action("Nuevo cliente iniciado")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        try:
            FormHelper.clear_entry(self.nombre_entry)
            FormHelper.clear_entry(self.dni_nie_entry)
            FormHelper.clear_entry(self.email_entry)
            FormHelper.clear_entry(self.telefono_entry)
            FormHelper.clear_text_widget(self.direccion_text)

            self.logger.debug("Formulario de cliente limpiado")

        except Exception as e:
            self.logger.error(f"Error limpiando formulario: {e}")

    def validate_form(self):
        """Valida el formulario de cliente"""
        errors = []

        # Nombre es obligatorio
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            errors.append("El nombre es obligatorio")

        # Validar email si se proporciona
        email = self.email_entry.get().strip()
        if email:
            email_error = FormValidator.validate_email(email, "Email")
            if email_error:
                errors.append("El formato del email no es válido")

        return errors

    def guardar_cliente(self):
        """Guarda el cliente"""
        try:
            # Validar formulario
            errors = self.validate_form()
            if errors:
                messagebox.showerror("Errores de validación",
                                   "Por favor, corrija los siguientes errores:\n\n• " +
                                   "\n• ".join(errors))
                return

            # Crear o actualizar cliente
            if self.current_cliente:
                # Actualizar cliente existente
                cliente = self.current_cliente
            else:
                # Crear nuevo cliente
                cliente = Cliente()

            # Asignar valores
            cliente.nombre = self.nombre_entry.get().strip()
            cliente.dni_nie = self.dni_nie_entry.get().strip()
            cliente.email = self.email_entry.get().strip()
            cliente.telefono = self.telefono_entry.get().strip()
            cliente.direccion = self.direccion_text.get("1.0", "end-1c").strip()

            # Guardar
            cliente.save()

            # Recargar lista
            self.load_clientes()

            # Mensaje de éxito
            action = "actualizado" if self.current_cliente else "creado"
            messagebox.showinfo("Éxito", f"Cliente {action} correctamente")

            log_user_action(f"Cliente {action}: {cliente.nombre}")
            self.logger.info(f"Cliente {action}: {cliente.nombre}")

            # Limpiar formulario si es nuevo cliente
            if not self.current_cliente:
                self.limpiar_formulario()

        except Exception as e:
            self.logger.error(f"Error guardando cliente: {e}")
            messagebox.showerror("Error", f"Error guardando cliente: {e}")

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        if not self.current_cliente:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar")
            return

        try:
            # Confirmar eliminación
            respuesta = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Está seguro de que desea eliminar el cliente '{self.current_cliente.nombre}'?\n\n"
                "Esta acción no se puede deshacer."
            )

            if respuesta:
                # Eliminar cliente
                self.current_cliente.delete()

                # Recargar lista
                self.load_clientes()

                # Limpiar formulario
                self.limpiar_formulario()
                self.current_cliente = None
                self.selected_cliente = None

                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                log_user_action(f"Cliente eliminado: {self.current_cliente.nombre}")

        except Exception as e:
            self.logger.error(f"Error eliminando cliente: {e}")
            messagebox.showerror("Error", f"Error eliminando cliente: {e}")
