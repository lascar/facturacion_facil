import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from utils.translations import get_text
from utils.logger import get_logger, log_user_action, log_database_operation, log_exception
from database.models import Factura, FacturaItem, Producto, Organizacion, Stock
from common.ui_components import BaseWindow, FormHelper
from common.validators import FormValidator, CalculationHelper
from ui.facturas_methods import FacturasMethodsMixin
from ui.producto_factura_dialog import ProductoFacturaDialog
from ui.configuracion_facturas import ConfiguracionFacturasDialog
from datetime import datetime
import os

class FacturasWindow(BaseWindow, FacturasMethodsMixin):
    def __init__(self, parent, nueva_factura=False):
        super().__init__(parent, get_text("facturas"), "1200x800")

        # Variables específicas de facturas
        self.facturas = []
        self.selected_factura = None
        self.current_factura = None
        self.factura_items = []
        self.productos_disponibles = []

        # Crear interfaz
        self.create_widgets()

        # Cargar datos
        self.load_facturas()
        self.load_productos_disponibles()

        if nueva_factura:
            self.nueva_factura()

        self.logger.info("Ventana de facturas inicializada correctamente")

    def create_widgets(self):
        """Crea los widgets de la ventana"""
        # Configurar frame scrollable
        main_frame = self.setup_scrollable_frame(1400, 900)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text=get_text("facturas"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))

        # Frame contenedor horizontal
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame izquierdo - Lista de facturas
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.create_facturas_list(left_frame)

        # Frame derecho - Formulario de factura
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.create_factura_form(right_frame)

    def create_facturas_list(self, parent):
        """Crea la lista de facturas"""
        # Título y botones
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        list_label = ctk.CTkLabel(header_frame, text="Lista de Facturas",
                                font=ctk.CTkFont(size=16, weight="bold"))
        list_label.pack(side="left", padx=5)

        nueva_btn = ctk.CTkButton(header_frame, text=get_text("nueva_factura"),
                                command=self.nueva_factura, width=120)
        nueva_btn.pack(side="right", padx=5)

        # Lista de facturas con Treeview
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear Treeview para mostrar facturas
        columns = ("Número", "Fecha", "Cliente", "Total")
        self.facturas_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        # Configurar columnas
        self.facturas_tree.heading("Número", text="Número")
        self.facturas_tree.heading("Fecha", text="Fecha")
        self.facturas_tree.heading("Cliente", text="Cliente")
        self.facturas_tree.heading("Total", text="Total")

        self.facturas_tree.column("Número", width=100)
        self.facturas_tree.column("Fecha", width=100)
        self.facturas_tree.column("Cliente", width=150)
        self.facturas_tree.column("Total", width=100)

        # Scrollbar para la lista
        scrollbar_facturas = ttk.Scrollbar(list_frame, orient="vertical",
                                         command=self.facturas_tree.yview)
        self.facturas_tree.configure(yscrollcommand=scrollbar_facturas.set)

        self.facturas_tree.pack(side="left", fill="both", expand=True)
        scrollbar_facturas.pack(side="right", fill="y")

        # Bind para selección
        self.facturas_tree.bind("<<TreeviewSelect>>", self.on_factura_select)

        # Botones de acción
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=10, pady=5)

        # Nota: El botón "Editar Factura" se ha eliminado porque la edición
        # se activa automáticamente al seleccionar una factura

        eliminar_btn = ctk.CTkButton(buttons_frame, text="Eliminar Factura",
                                   fg_color="#DC143C", hover_color="#B22222",
                                   command=self.eliminar_factura)
        eliminar_btn.pack(side="left", padx=5)

        pdf_btn = ctk.CTkButton(buttons_frame, text=get_text("exportar_pdf"),
                              command=self.exportar_pdf)
        pdf_btn.pack(side="right", padx=5)

    def create_factura_form(self, parent):
        """Crea el formulario de factura"""
        # Título del formulario (guardar referencia para actualizaciones)
        self.form_title_label = ctk.CTkLabel(parent, text="Datos de la Factura",
                                           font=ctk.CTkFont(size=16, weight="bold"))
        self.form_title_label.pack(pady=(10, 20))

        # Frame scrollable para el formulario
        form_frame = ctk.CTkScrollableFrame(parent)
        form_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Datos básicos de la factura
        self.create_factura_header(form_frame)

        # Datos del cliente
        self.create_cliente_section(form_frame)

        # Productos de la factura
        self.create_productos_section(form_frame)

        # Totales
        self.create_totales_section(form_frame)

        # Botones de acción
        self.create_action_buttons(form_frame)

    def create_factura_header(self, parent):
        """Crea la sección de datos básicos de la factura"""
        header_frame = ctk.CTkFrame(parent)
        header_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(header_frame, text="Datos Básicos",
                   font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))

        # Frame para campos en dos columnas
        fields_frame = ctk.CTkFrame(header_frame)
        fields_frame.pack(fill="x", padx=10, pady=5)

        # Columna izquierda
        left_col = ctk.CTkFrame(fields_frame)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Número de factura
        ctk.CTkLabel(left_col, text=get_text("numero_factura") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.numero_entry = ctk.CTkEntry(left_col, placeholder_text="Número automático")
        self.numero_entry.pack(fill="x", padx=10, pady=5)

        # Columna derecha
        right_col = ctk.CTkFrame(fields_frame)
        right_col.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Fecha de factura
        ctk.CTkLabel(right_col, text=get_text("fecha_factura") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.fecha_entry = ctk.CTkEntry(right_col, placeholder_text="YYYY-MM-DD")
        self.fecha_entry.pack(fill="x", padx=10, pady=5)

        # Establecer fecha actual por defecto
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Modo de pago
        ctk.CTkLabel(header_frame, text=get_text("modo_pago")).pack(anchor="w", padx=10, pady=(10, 0))
        self.modo_pago_var = ctk.StringVar(value="efectivo")
        modo_pago_frame = ctk.CTkFrame(header_frame)
        modo_pago_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkRadioButton(modo_pago_frame, text=get_text("efectivo"),
                         variable=self.modo_pago_var, value="efectivo").pack(side="left", padx=10)
        ctk.CTkRadioButton(modo_pago_frame, text=get_text("tarjeta"),
                         variable=self.modo_pago_var, value="tarjeta").pack(side="left", padx=10)
        ctk.CTkRadioButton(modo_pago_frame, text=get_text("transferencia"),
                         variable=self.modo_pago_var, value="transferencia").pack(side="left", padx=10)

    def create_cliente_section(self, parent):
        """Crea la sección de datos del cliente"""
        cliente_frame = ctk.CTkFrame(parent)
        cliente_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(cliente_frame, text=get_text("datos_cliente"),
                   font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))

        # Frame para campos en dos columnas
        fields_frame = ctk.CTkFrame(cliente_frame)
        fields_frame.pack(fill="x", padx=10, pady=5)

        # Columna izquierda
        left_col = ctk.CTkFrame(fields_frame)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Nombre del cliente
        ctk.CTkLabel(left_col, text=get_text("nombre_cliente") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.nombre_cliente_entry = ctk.CTkEntry(left_col, placeholder_text="Nombre completo del cliente")
        self.nombre_cliente_entry.pack(fill="x", padx=10, pady=5)

        # DNI/NIE
        ctk.CTkLabel(left_col, text=get_text("dni_nie")).pack(anchor="w", padx=10, pady=(10, 0))
        self.dni_nie_entry = ctk.CTkEntry(left_col, placeholder_text="12345678A o X1234567A")
        self.dni_nie_entry.pack(fill="x", padx=10, pady=5)

        # Email
        ctk.CTkLabel(left_col, text=get_text("email_cliente")).pack(anchor="w", padx=10, pady=(10, 0))
        self.email_cliente_entry = ctk.CTkEntry(left_col, placeholder_text="cliente@email.com")
        self.email_cliente_entry.pack(fill="x", padx=10, pady=5)

        # Columna derecha
        right_col = ctk.CTkFrame(fields_frame)
        right_col.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # Dirección
        ctk.CTkLabel(right_col, text=get_text("direccion_cliente")).pack(anchor="w", padx=10, pady=(10, 0))
        self.direccion_cliente_text = ctk.CTkTextbox(right_col, height=60)
        self.direccion_cliente_text.pack(fill="x", padx=10, pady=5)

        # Teléfono
        ctk.CTkLabel(right_col, text=get_text("telefono_cliente")).pack(anchor="w", padx=10, pady=(10, 0))
        self.telefono_cliente_entry = ctk.CTkEntry(right_col, placeholder_text="+34 123 456 789")
        self.telefono_cliente_entry.pack(fill="x", padx=10, pady=5)

    def create_productos_section(self, parent):
        """Crea la sección de productos de la factura"""
        productos_frame = ctk.CTkFrame(parent)
        productos_frame.pack(fill="x", padx=10, pady=10)

        # Título y botón agregar
        header_frame = ctk.CTkFrame(productos_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(header_frame, text=get_text("productos_factura"),
                   font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)

        agregar_btn = ctk.CTkButton(header_frame, text=get_text("agregar_producto"),
                                  command=self.agregar_producto, width=120)
        agregar_btn.pack(side="right", padx=5)

        # Lista de productos en la factura
        list_frame = ctk.CTkFrame(productos_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview para productos
        columns = ("Producto", "Cantidad", "Precio Unit.", "IVA %", "Descuento %", "Total")
        self.productos_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        for col in columns:
            self.productos_tree.heading(col, text=col)

        self.productos_tree.column("Producto", width=200)
        self.productos_tree.column("Cantidad", width=80)
        self.productos_tree.column("Precio Unit.", width=100)
        self.productos_tree.column("IVA %", width=80)
        self.productos_tree.column("Descuento %", width=100)
        self.productos_tree.column("Total", width=100)

        # Scrollbar para productos
        scrollbar_productos = ttk.Scrollbar(list_frame, orient="vertical",
                                          command=self.productos_tree.yview)
        self.productos_tree.configure(yscrollcommand=scrollbar_productos.set)

        self.productos_tree.pack(side="left", fill="both", expand=True)
        scrollbar_productos.pack(side="right", fill="y")

        # Botones para productos
        prod_buttons_frame = ctk.CTkFrame(productos_frame)
        prod_buttons_frame.pack(fill="x", padx=10, pady=5)

        editar_prod_btn = ctk.CTkButton(prod_buttons_frame, text="Editar Item",
                                      command=self.editar_producto_factura)
        editar_prod_btn.pack(side="left", padx=5)

        eliminar_prod_btn = ctk.CTkButton(prod_buttons_frame, text="Eliminar Item",
                                        fg_color="#DC143C", hover_color="#B22222",
                                        command=self.eliminar_producto_factura)
        eliminar_prod_btn.pack(side="left", padx=5)

    def create_totales_section(self, parent):
        """Crea la sección de totales"""
        totales_frame = ctk.CTkFrame(parent)
        totales_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(totales_frame, text="Totales",
                   font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))

        # Frame para totales en columnas
        totales_grid = ctk.CTkFrame(totales_frame)
        totales_grid.pack(fill="x", padx=10, pady=5)

        # Subtotal
        ctk.CTkLabel(totales_grid, text=get_text("subtotal") + ":").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.subtotal_label = ctk.CTkLabel(totales_grid, text="0.00 €", font=ctk.CTkFont(weight="bold"))
        self.subtotal_label.grid(row=0, column=1, sticky="e", padx=10, pady=5)

        # Total IVA
        ctk.CTkLabel(totales_grid, text=get_text("total_iva") + ":").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.total_iva_label = ctk.CTkLabel(totales_grid, text="0.00 €", font=ctk.CTkFont(weight="bold"))
        self.total_iva_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        # Total factura
        ctk.CTkLabel(totales_grid, text=get_text("total_factura") + ":",
                   font=ctk.CTkFont(size=16, weight="bold")).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.total_factura_label = ctk.CTkLabel(totales_grid, text="0.00 €",
                                              font=ctk.CTkFont(size=16, weight="bold"))
        self.total_factura_label.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        # Configurar grid
        totales_grid.grid_columnconfigure(1, weight=1)

    def create_action_buttons(self, parent):
        """Crea los botones de acción"""
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=10, pady=20)

        # Botón guardar
        self.guardar_btn = ctk.CTkButton(buttons_frame, text=get_text("guardar"),
                                       command=self.guardar_factura, width=120, height=35,
                                       fg_color="#2E8B57", hover_color="#228B22")
        self.guardar_btn.pack(side="left", padx=10)

        # Botón limpiar
        limpiar_btn = ctk.CTkButton(buttons_frame, text=get_text("limpiar"),
                                  command=self.limpiar_formulario, width=120)
        limpiar_btn.pack(side="left", padx=10)

        # Botón generar PDF
        pdf_btn = ctk.CTkButton(buttons_frame, text=get_text("exportar_pdf"),
                              command=self.generar_pdf, width=120)
        pdf_btn.pack(side="right", padx=10)

        # Botón configuración de numeración
        config_btn = ctk.CTkButton(buttons_frame, text="Configurar Numeración",
                                 command=self.configurar_numeracion, width=150,
                                 fg_color="#1f538d", hover_color="#14375e")
        config_btn.pack(side="right", padx=10)

    def load_facturas(self):
        """Carga la lista de facturas"""
        try:
            self.facturas = Factura.get_all()

            # Limpiar la lista
            for item in self.facturas_tree.get_children():
                self.facturas_tree.delete(item)

            # Agregar facturas a la lista
            for factura in self.facturas:
                self.facturas_tree.insert("", "end", values=(
                    factura.numero_factura,
                    factura.fecha_factura,
                    factura.nombre_cliente,
                    CalculationHelper.format_currency(factura.total_factura)
                ))

            self.logger.info(f"Cargadas {len(self.facturas)} facturas")

        except Exception as e:
            log_exception(e, "load_facturas")
            self._show_message("error", get_text("error"), f"Error al cargar facturas: {str(e)}")

    def load_productos_disponibles(self):
        """Carga la lista de productos disponibles con información de stock"""
        try:
            self.productos_disponibles = Producto.get_all()

            # Agregar información de stock a cada producto para referencia
            for producto in self.productos_disponibles:
                producto._stock_actual = Stock.get_by_product(producto.id)

            self.logger.info(f"Cargados {len(self.productos_disponibles)} productos disponibles con información de stock")
        except Exception as e:
            log_exception(e, "load_productos_disponibles")
            self.productos_disponibles = []

    def on_factura_select(self, event):
        """Maneja la selección de una factura en la lista y la carga automáticamente para edición"""
        try:
            selection = self.facturas_tree.selection()
            if selection:
                item = selection[0]
                index = self.facturas_tree.index(item)
                self.selected_factura = self.facturas[index]

                # Cargar factura en el formulario para edición automática
                self.load_factura_to_form()

                # Actualizar título del formulario para indicar modo edición
                self.form_title_label.configure(
                    text=f"Editando Factura: {self.selected_factura.numero_factura}",
                    text_color="#2E8B57"  # Verde para indicar edición activa
                )

                self.logger.info(f"Factura seleccionada y cargada para edición: {self.selected_factura.numero_factura}")
                log_user_action("Factura en edición automática", f"Número: {self.selected_factura.numero_factura}")
            else:
                # Si no hay selección, volver al título normal
                self.form_title_label.configure(
                    text="Datos de la Factura",
                    text_color=None  # Color por defecto
                )
        except Exception as e:
            log_exception(e, "on_factura_select")

    def nueva_factura(self):
        """Prepara el formulario para una nueva factura"""
        try:
            self.selected_factura = None
            self.current_factura = Factura()
            self.factura_items = []

            self.limpiar_formulario()

            # Inicializar número de factura usando el servicio de numeración
            self.initialize_numero_factura()

            # Actualizar título del formulario para nueva factura
            self.form_title_label.configure(
                text="Nueva Factura",
                text_color="#1f538d"  # Azul para nueva factura
            )

            # Limpiar selección en la lista
            self.facturas_tree.selection_remove(self.facturas_tree.selection())

            self.logger.info("Nueva factura iniciada")
            log_user_action("Nueva factura", "Formulario preparado")

        except Exception as e:
            log_exception(e, "nueva_factura")
            self._show_message("error", get_text("error"), f"Error al crear nueva factura: {str(e)}")

    def configurar_numeracion(self):
        """Abre el diálogo de configuración de numeración de facturas"""
        try:
            dialog = ConfiguracionFacturasDialog(self.window)
            result = dialog.show()

            if result:
                # Si se guardó la configuración, actualizar el número de factura actual
                self.initialize_numero_factura()
                log_user_action("Configuración de numeración", "Configuración actualizada")

        except Exception as e:
            log_exception(e, "configurar_numeracion")
            self._show_message("error", get_text("error"), f"Error en configuración: {str(e)}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        try:
            # Limpiar campos básicos
            FormHelper.clear_entry(self.numero_entry)
            FormHelper.set_entry_value(self.fecha_entry, datetime.now().strftime("%Y-%m-%d"))
            self.modo_pago_var.set("efectivo")

            # Limpiar datos del cliente
            FormHelper.clear_entry(self.nombre_cliente_entry)
            FormHelper.clear_entry(self.dni_nie_entry)
            FormHelper.clear_entry(self.email_cliente_entry)
            FormHelper.clear_text_widget(self.direccion_cliente_text)
            FormHelper.clear_entry(self.telefono_cliente_entry)

            # Limpiar productos
            for item in self.productos_tree.get_children():
                self.productos_tree.delete(item)

            self.factura_items = []

            # Actualizar totales
            self.update_totales()

            self.logger.debug("Formulario de factura limpiado")

        except Exception as e:
            log_exception(e, "limpiar_formulario")

    def load_factura_to_form(self):
        """Carga los datos de la factura seleccionada en el formulario"""
        if not self.selected_factura:
            return

        try:
            factura = self.selected_factura
            self.current_factura = factura

            # Cargar datos básicos
            FormHelper.set_entry_value(self.numero_entry, factura.numero_factura)
            FormHelper.set_entry_value(self.fecha_entry, factura.fecha_factura)
            self.modo_pago_var.set(factura.modo_pago or "efectivo")

            # Cargar datos del cliente
            FormHelper.set_entry_value(self.nombre_cliente_entry, factura.nombre_cliente)
            FormHelper.set_entry_value(self.dni_nie_entry, factura.dni_nie_cliente or "")
            FormHelper.set_entry_value(self.email_cliente_entry, factura.email_cliente or "")
            FormHelper.set_text_value(self.direccion_cliente_text, factura.direccion_cliente or "")
            FormHelper.set_entry_value(self.telefono_cliente_entry, factura.telefono_cliente or "")

            # Cargar productos
            self.factura_items = factura.items.copy()
            self.update_productos_tree()

            # Actualizar totales
            self.update_totales()

            self.logger.info(f"Factura cargada en formulario: {factura.numero_factura}")

        except Exception as e:
            log_exception(e, "load_factura_to_form")
            self._show_message("error", get_text("error"), f"Error al cargar factura: {str(e)}")
