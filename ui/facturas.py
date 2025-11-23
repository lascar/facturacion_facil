
# -*- coding: utf-8 -*-
"""
Interface PyQt6 pure
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QTextEdit, QPushButton, QTreeWidget, 
                            QTreeWidgetItem, QMessageBox, QFrame)
from PyQt6.QtCore import Qt


from utils.translations import get_text
from utils.logger import get_logger, log_user_action, log_database_operation, log_exception
from database.models import Factura, FacturaItem, Producto, Organizacion, Stock, Cliente
from database.optimized_models import OptimizedFactura, OptimizedProducto
from common.ui_components import BaseWindow, FormHelper
from common.validators import FormValidator, CalculationHelper
from common.treeview_sorter import add_sorting_to_treeview
from ui.facturas_methods import FacturasMethodsMixin
from ui.producto_factura_dialog_simple import ProductoFacturaDialog
from ui.configuracion_facturas_simple import ConfiguracionFacturasDialog
from datetime import datetime
import os

class FacturasWindow(BaseWindow, FacturasMethodsMixin):
    def __init__(self, parent, nueva_factura=False):
        super().__init__(parent, get_text("facturas"), "1000x900")

        # Variables específicas de facturas
        self.facturas = []
        self.selected_factura = None
        self.current_factura = None
        self.factura_items = []
        self.selected_cliente = None
        self.clientes_window = None
        self.productos_disponibles = []

        # Crear interfaz
        self.create_widgets()

        # Cargar datos
        self.load_facturas()
        self.load_productos_disponibles()
        self.load_clientes_combobox()

        if nueva_factura:
            self.nueva_factura()

        self.logger.info("Ventana de facturas inicializada correctamente")

    def create_widgets(self):
        """Crea los widgets de la ventana"""
        # Configurar frame scrollable con nueva geometría más compacta
        main_frame = self.setup_scrollable_frame(1000, 900)

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

        # Frame superior - Lista de facturas (hauteur fixe)
        top_frame = ctk.CTkFrame(content_frame)
        top_frame.pack(side="top", fill="x", pady=(0, 5))
        top_frame.configure(height=300)  # Hauteur fixe pour la liste

        self.create_facturas_list(top_frame)

        # Frame inferior - Formulario de factura (prend l'espace restant)
        bottom_frame = ctk.CTkFrame(content_frame)
        bottom_frame.pack(side="bottom", fill="both", expand=True, pady=(5, 0))

        self.create_factura_form(bottom_frame)

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

        # Crear Treeview para mostrar facturas (hauteur réduite pour layout vertical)
        columns = ("Número", "Fecha", "Cliente", "Total")
        self.facturas_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)

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

        # Configurar ordenación por columnas
        self.facturas_tree_sorter = add_sorting_to_treeview(self.facturas_tree)

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

        # Selección de cliente existente
        ctk.CTkLabel(left_col, text="Cliente existente").pack(anchor="w", padx=10, pady=(10, 0))

        # Frame para dropdown y botón
        cliente_select_frame = ctk.CTkFrame(left_col)
        cliente_select_frame.pack(fill="x", padx=10, pady=5)

        self.cliente_combobox = ctk.CTkComboBox(
            cliente_select_frame,
            values=["-- Seleccionar cliente --"],
            command=self.on_cliente_selected,
            width=200
        )
        self.cliente_combobox.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Botón para gestionar clientes
        self.gestionar_clientes_btn = ctk.CTkButton(
            cliente_select_frame,
            text="👥",
            width=30,
            command=self.open_clientes_window
        )
        self.gestionar_clientes_btn.pack(side="right")

        # Nombre del cliente (editable)
        ctk.CTkLabel(left_col, text=get_text("nombre_cliente") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.nombre_cliente_entry = ctk.CTkEntry(left_col, placeholder_text="Nombre completo del cliente")
        self.nombre_cliente_entry.pack(fill="x", padx=10, pady=5)
        self.nombre_cliente_entry.bind("<KeyRelease>", self.on_nombre_cliente_changed)

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

        # Treeview para productos con columna de imagen
        # Widget personnalisé pour productos avec images
        from ui.producto_list_widget import ProductoListWidget

        self.productos_tree = ProductoListWidget(
            list_frame,
            height=300,
            corner_radius=10
        )
        self.productos_tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Configurer le callback de sélection
        self.productos_tree.set_selection_callback(self.on_producto_selected)

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
                                       command=self.debug_guardar_factura, width=120, height=35,
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
        """Carga la lista de facturas (OPTIMIZADO)"""
        try:
            # 🚀 OPTIMIZACIÓN: Usar requête optimisée pour éviter le problème N+1
            try:
                # Pour l'affichage de la liste, utiliser le résumé optimisé
                facturas_summary = OptimizedFactura.get_summary_optimized()

                # Limpiar la lista
                for item in self.facturas_tree.get_children():
                    self.facturas_tree.delete(item)

                # Agregar facturas a la lista (depuis le résumé)
                for factura_data in facturas_summary:
                    self.facturas_tree.insert("", "end", values=(
                        factura_data['numero_factura'],
                        factura_data['fecha_factura'],
                        factura_data['nombre_cliente'],
                        CalculationHelper.format_currency(factura_data['total_factura'])
                    ))

                # Garder une référence pour la compatibilité
                self.facturas = []
                self.facturas_summary = facturas_summary

                self.logger.info(f"Cargadas {len(facturas_summary)} facturas (OPTIMIZADO - résumé)")

            except Exception as opt_error:
                self.logger.warning(f"Error en método optimizado, usando fallback: {opt_error}")
                # Fallback vers la méthode originale
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

                self.logger.info(f"Cargadas {len(self.facturas)} facturas (método original)")

        except Exception as e:
            log_exception(e, "load_facturas")
            self._show_message("error", get_text("error"), f"Error al cargar facturas: {str(e)}")

    def load_productos_disponibles(self):
        """Carga la lista de productos disponibles con información de stock (OPTIMIZADO)"""
        try:
            # 🚀 OPTIMIZACIÓN: Usar requête optimisée qui évite le problème N+1
            try:
                self.productos_disponibles = OptimizedProducto.get_all_with_stock_optimized()
                self.logger.info(f"Cargados {len(self.productos_disponibles)} productos disponibles con información de stock (OPTIMIZADO)")
            except Exception as opt_error:
                self.logger.warning(f"Error en método optimizado, usando fallback: {opt_error}")
                # Fallback vers la méthode originale
                self.productos_disponibles = Producto.get_all()

                # Agregar información de stock a cada producto para referencia
                for producto in self.productos_disponibles:
                    producto._stock_actual = Stock.get_by_product(producto.id)

                self.logger.info(f"Cargados {len(self.productos_disponibles)} productos disponibles con información de stock (método original)")

        except Exception as e:
            log_exception(e, "load_productos_disponibles")
            self.productos_disponibles = []

    def debug_guardar_factura(self):
        """Método de debugging para guardar factura con logging detallado"""
        try:
            self.logger.info("🔧 DEBUG: Botón guardar presionado")
            self.logger.info(f"🔧 DEBUG: Método guardar_factura disponible: {hasattr(self, 'guardar_factura')}")
            self.logger.info(f"🔧 DEBUG: Tipo de guardar_factura: {type(getattr(self, 'guardar_factura', None))}")

            # Verificar que tenemos los atributos necesarios
            self.logger.info(f"🔧 DEBUG: current_factura: {self.current_factura}")
            self.logger.info(f"🔧 DEBUG: factura_items: {len(self.factura_items) if hasattr(self, 'factura_items') else 'NO EXISTE'}")

            # Llamar al método original
            if hasattr(self, 'guardar_factura'):
                self.logger.info("🔧 DEBUG: Llamando a guardar_factura...")
                try:
                    self.guardar_factura()
                    self.logger.info("🔧 DEBUG: guardar_factura completado SIN ERRORES")
                except Exception as e:
                    self.logger.error(f"🔧 DEBUG: EXCEPCIÓN en guardar_factura: {e}")
                    import traceback
                    self.logger.error(f"🔧 DEBUG: Traceback completo: {traceback.format_exc()}")
                    # Re-lanzar para que sea visible
                    raise
            else:
                self.logger.error("🔧 DEBUG: ¡Método guardar_factura NO disponible!")
                self._show_message("error", "Error de Desarrollo",
                                 "Método guardar_factura no está disponible. Problema de herencia.")

        except Exception as e:
            self.logger.error(f"🔧 DEBUG: Error en debug_guardar_factura: {e}")
            import traceback
            self.logger.error(f"🔧 DEBUG: Traceback: {traceback.format_exc()}")
            self._show_message("error", "Error de Debug", f"Error en debug_guardar_factura: {str(e)}")

    def on_factura_select(self, event):
        """Maneja la selección de una factura en la lista y la carga automáticamente para edición"""
        try:
            selection = self.facturas_tree.selection()
            if selection:
                item = selection[0]
                # Obtener el número de factura desde la primera columna del TreeView
                item_values = self.facturas_tree.item(item, 'values')
                if item_values and len(item_values) > 0:
                    numero_factura = item_values[0]  # Primera columna es el número de factura

                    # Buscar la factura por número en la base de datos
                    self.logger.info(f"🔍 DEBUG: Buscando factura con número: {numero_factura}")
                    self.selected_factura = Factura.get_by_numero(numero_factura)
                    self.logger.info(f"🔍 DEBUG: Factura encontrada: {self.selected_factura is not None}")

                    if self.selected_factura:
                        self.logger.info(f"🔍 DEBUG: Factura ID: {self.selected_factura.id}, Items: {len(self.selected_factura.items)}")

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
                        self.logger.error(f"No se encontró la factura con número: {numero_factura}")
                        self._show_message("error", "Error", f"No se encontró la factura {numero_factura}")
                else:
                    self.logger.error("No se pudo obtener el número de factura de la selección")
            else:
                # Si no hay selección, volver al título normal
                self.selected_factura = None
                self.form_title_label.configure(
                    text="Datos de la Factura",
                    text_color=None  # Color por defecto
                )
        except Exception as e:
            log_exception(e, "on_factura_select")
            self.logger.error(f"Error en selección de factura: {e}")
            self._show_message("error", "Error", f"Error al seleccionar factura: {str(e)}")

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
            self.productos_tree.clear_items()

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

    def load_clientes_combobox(self):
        """Carga la lista de clientes en el combobox"""
        try:
            clientes = Cliente.get_all()
            cliente_names = ["-- Seleccionar cliente --"] + [cliente.nombre for cliente in clientes]
            self.cliente_combobox.configure(values=cliente_names)
            self.cliente_combobox.set("-- Seleccionar cliente --")

            self.logger.debug(f"Cargados {len(clientes)} clientes en combobox")

        except Exception as e:
            self.logger.error(f"Error cargando clientes: {e}")

    def on_cliente_selected(self, selected_name):
        """Maneja la selección de un cliente del combobox"""
        if selected_name == "-- Seleccionar cliente --":
            self.selected_cliente = None
            return

        try:
            # Buscar el cliente por nombre
            cliente = Cliente.get_by_nombre(selected_name)
            if cliente:
                self.selected_cliente = cliente

                # Cargar datos del cliente en el formulario
                FormHelper.set_entry_value(self.nombre_cliente_entry, cliente.nombre)
                FormHelper.set_entry_value(self.dni_nie_entry, cliente.dni_nie or "")
                FormHelper.set_entry_value(self.email_cliente_entry, cliente.email or "")
                FormHelper.set_text_value(self.direccion_cliente_text, cliente.direccion or "")
                FormHelper.set_entry_value(self.telefono_cliente_entry, cliente.telefono or "")

                self.logger.debug(f"Cliente seleccionado: {cliente.nombre}")

        except Exception as e:
            self.logger.error(f"Error seleccionando cliente: {e}")

    def on_nombre_cliente_changed(self, event=None):
        """Maneja cambios en el nombre del cliente"""
        # Si el usuario está escribiendo, deseleccionar el cliente del combobox
        current_name = self.nombre_cliente_entry.get().strip()
        if self.selected_cliente and current_name != self.selected_cliente.nombre:
            self.selected_cliente = None
            self.cliente_combobox.set("-- Seleccionar cliente --")

    def open_clientes_window(self):
        """Abre la ventana de gestión de clientes"""
        try:
            from ui.clientes import ClientesWindow

            if self.clientes_window is None or not self.clientes_window.window.winfo_exists():
                self.clientes_window = ClientesWindow(self.window)
                # Callback para recargar clientes cuando se cierre la ventana
                self.clientes_window.window.protocol("WM_DELETE_WINDOW", self.on_clientes_window_closed)
            else:
                self.clientes_window.window.lift()
                self.clientes_window.window.focus_force()

        except Exception as e:
            self.logger.error(f"Error abriendo ventana de clientes: {e}")
            self._show_message("error", "Error", f"Error abriendo ventana de clientes: {e}")

    def on_clientes_window_closed(self):
        """Callback cuando se cierra la ventana de clientes"""
        try:
            if self.clientes_window:
                self.clientes_window.window.destroy()
                self.clientes_window = None

            # Recargar la lista de clientes
            self.load_clientes_combobox()

        except Exception as e:
            self.logger.error(f"Error cerrando ventana de clientes: {e}")

    def auto_add_cliente_if_new(self):
        """Añade automáticamente un cliente si es nuevo"""
        try:
            nombre = self.nombre_cliente_entry.get().strip()

            # Si no hay nombre, no hacer nada
            if not nombre:
                return None

            # Si ya hay un cliente seleccionado, usar ese
            if self.selected_cliente and self.selected_cliente.nombre == nombre:
                return self.selected_cliente.id

            # Buscar si el cliente ya existe
            cliente_existente = Cliente.get_by_nombre(nombre)
            if cliente_existente:
                return cliente_existente.id

            # Crear nuevo cliente con los datos del formulario
            nuevo_cliente = Cliente(
                nombre=nombre,
                dni_nie=self.dni_nie_entry.get().strip(),
                email=self.email_cliente_entry.get().strip(),
                telefono=self.telefono_cliente_entry.get().strip(),
                direccion=self.direccion_cliente_text.get("1.0", "end-1c").strip()
            )

            cliente_id = nuevo_cliente.save()

            # Recargar la lista de clientes
            self.load_clientes_combobox()

            # Seleccionar el nuevo cliente en el combobox
            self.cliente_combobox.set(nombre)
            self.selected_cliente = nuevo_cliente

            self.logger.info(f"Nuevo cliente creado automáticamente: {nombre}")
            log_user_action(f"Cliente creado automáticamente: {nombre}")

            return cliente_id

        except Exception as e:
            self.logger.error(f"Error creando cliente automáticamente: {e}")
            return None
