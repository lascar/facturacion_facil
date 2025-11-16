# -*- coding: utf-8 -*-
"""
Ventana de búsqueda avanzada
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime, timedelta
from utils.translations import get_text
from utils.logger import get_logger
from database.models import Factura, Producto, Stock
from common.custom_dialogs import show_copyable_info, show_copyable_error

class SearchWindow:
    """Ventana de búsqueda avanzada"""
    
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Búsqueda Avanzada")
        self.window.geometry("1200x800")
        self.window.transient(parent)
        self.logger = get_logger("search_window")
        
        # Variables de búsqueda
        self.search_type = tk.StringVar(value="facturas")
        self.search_text = tk.StringVar()
        self.date_from = tk.StringVar()
        self.date_to = tk.StringVar()
        self.amount_from = tk.StringVar()
        self.amount_to = tk.StringVar()
        self.client_filter = tk.StringVar()
        self.status_filter = tk.StringVar(value="todos")
        
        # Resultados
        self.search_results = []
        
        # Configurar ventana
        self.setup_window_focus()
        self.create_widgets()
        self.load_initial_data()
    
    def setup_window_focus(self):
        """Configura el focus de la ventana"""
        try:
            self.window.lift()
            self.window.focus_force()
            self.window.attributes('-topmost', True)
            self.center_window()
            self.window.after(500, lambda: self.window.attributes('-topmost', False))
        except Exception as e:
            self.logger.error(f"Error configurando focus: {e}")
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        try:
            self.window.update_idletasks()
            width = self.window.winfo_width()
            height = self.window.winfo_height()
            x = (self.window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.window.winfo_screenheight() // 2) - (height // 2)
            self.window.geometry(f"{width}x{height}+{x}+{y}")
        except Exception as e:
            self.logger.error(f"Error centrando ventana: {e}")
    
    def create_widgets(self):
        """Crea la interfaz de usuario"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔍 Búsqueda Avanzada",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Frame de filtros
        self.create_filters_frame(main_frame)
        
        # Frame de resultados
        self.create_results_frame(main_frame)
        
        # Frame de acciones
        self.create_actions_frame(main_frame)
    
    def create_filters_frame(self, parent):
        """Crea el frame de filtros de búsqueda"""
        filters_frame = ctk.CTkFrame(parent)
        filters_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Título de filtros
        filters_title = ctk.CTkLabel(
            filters_frame,
            text="Filtros de Búsqueda",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filters_title.pack(pady=(15, 10))
        
        # Frame para organizar filtros en columnas
        filters_grid = ctk.CTkFrame(filters_frame)
        filters_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Columna 1: Tipo y texto
        col1_frame = ctk.CTkFrame(filters_grid)
        col1_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Tipo de búsqueda
        type_label = ctk.CTkLabel(col1_frame, text="Buscar en:")
        type_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        type_combo = ctk.CTkComboBox(
            col1_frame,
            variable=self.search_type,
            values=["facturas", "productos", "clientes", "todo"],
            command=self.on_search_type_changed
        )
        type_combo.pack(fill="x", padx=10, pady=(0, 10))
        
        # Texto de búsqueda
        text_label = ctk.CTkLabel(col1_frame, text="Texto a buscar:")
        text_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            col1_frame,
            textvariable=self.search_text,
            placeholder_text="Ingrese texto a buscar..."
        )
        self.search_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Columna 2: Fechas
        col2_frame = ctk.CTkFrame(filters_grid)
        col2_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Rango de fechas
        dates_label = ctk.CTkLabel(col2_frame, text="Rango de fechas:")
        dates_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Fecha desde
        from_label = ctk.CTkLabel(col2_frame, text="Desde:")
        from_label.pack(anchor="w", padx=10, pady=(0, 2))
        
        self.date_from_entry = ctk.CTkEntry(
            col2_frame,
            textvariable=self.date_from,
            placeholder_text="YYYY-MM-DD"
        )
        self.date_from_entry.pack(fill="x", padx=10, pady=(0, 5))
        
        # Fecha hasta
        to_label = ctk.CTkLabel(col2_frame, text="Hasta:")
        to_label.pack(anchor="w", padx=10, pady=(0, 2))
        
        self.date_to_entry = ctk.CTkEntry(
            col2_frame,
            textvariable=self.date_to,
            placeholder_text="YYYY-MM-DD"
        )
        self.date_to_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Columna 3: Montos y cliente
        col3_frame = ctk.CTkFrame(filters_grid)
        col3_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Rango de montos (solo para facturas)
        self.amounts_label = ctk.CTkLabel(col3_frame, text="Rango de montos (€):")
        self.amounts_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Monto desde
        self.amount_from_label = ctk.CTkLabel(col3_frame, text="Desde:")
        self.amount_from_label.pack(anchor="w", padx=10, pady=(0, 2))
        
        self.amount_from_entry = ctk.CTkEntry(
            col3_frame,
            textvariable=self.amount_from,
            placeholder_text="0.00"
        )
        self.amount_from_entry.pack(fill="x", padx=10, pady=(0, 5))
        
        # Monto hasta
        self.amount_to_label = ctk.CTkLabel(col3_frame, text="Hasta:")
        self.amount_to_label.pack(anchor="w", padx=10, pady=(0, 2))
        
        self.amount_to_entry = ctk.CTkEntry(
            col3_frame,
            textvariable=self.amount_to,
            placeholder_text="999999.99"
        )
        self.amount_to_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botones de acción rápida
        quick_actions_frame = ctk.CTkFrame(filters_frame)
        quick_actions_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        quick_label = ctk.CTkLabel(quick_actions_frame, text="Búsquedas rápidas:")
        quick_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        buttons_frame = ctk.CTkFrame(quick_actions_frame)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Botones de búsqueda rápida
        today_btn = ctk.CTkButton(
            buttons_frame,
            text="Hoy",
            command=self.search_today,
            width=80,
            height=30
        )
        today_btn.pack(side="left", padx=5)
        
        week_btn = ctk.CTkButton(
            buttons_frame,
            text="Esta semana",
            command=self.search_this_week,
            width=100,
            height=30
        )
        week_btn.pack(side="left", padx=5)
        
        month_btn = ctk.CTkButton(
            buttons_frame,
            text="Este mes",
            command=self.search_this_month,
            width=100,
            height=30
        )
        month_btn.pack(side="left", padx=5)
        
        stock_bajo_btn = ctk.CTkButton(
            buttons_frame,
            text="Stock bajo",
            command=self.search_low_stock,
            width=100,
            height=30,
            fg_color="orange",
            hover_color="darkorange"
        )
        stock_bajo_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Limpiar",
            command=self.clear_filters,
            width=80,
            height=30,
            fg_color="gray",
            hover_color="darkgray"
        )
        clear_btn.pack(side="right", padx=5)
        
        search_btn = ctk.CTkButton(
            buttons_frame,
            text="🔍 Buscar",
            command=self.perform_search,
            width=100,
            height=30,
            fg_color="green",
            hover_color="darkgreen"
        )
        search_btn.pack(side="right", padx=5)
    
    def create_results_frame(self, parent):
        """Crea el frame de resultados"""
        results_frame = ctk.CTkFrame(parent)
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Título de resultados
        self.results_title = ctk.CTkLabel(
            results_frame,
            text="Resultados de búsqueda",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.results_title.pack(pady=(15, 10))
        
        # Frame para la tabla de resultados
        table_frame = ctk.CTkFrame(results_frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Crear Treeview para mostrar resultados
        self.create_results_table(table_frame)
    
    def create_results_table(self, parent):
        """Crea la tabla de resultados usando Treeview"""
        # Frame para el Treeview y scrollbars
        tree_frame = tk.Frame(parent, bg=parent.cget("fg_color")[1])
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear Treeview
        self.results_tree = ttk.Treeview(tree_frame)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.results_tree.xview)
        
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Posicionar elementos
        self.results_tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Configurar columnas iniciales (se actualizarán según el tipo de búsqueda)
        self.update_results_columns("facturas")
        
        # Bind para doble clic
        self.results_tree.bind("<Double-1>", self.on_result_double_click)
    
    def create_actions_frame(self, parent):
        """Crea el frame de acciones"""
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Información de resultados
        self.results_info = ctk.CTkLabel(
            actions_frame,
            text="Listo para buscar",
            font=ctk.CTkFont(size=12)
        )
        self.results_info.pack(side="left", padx=20, pady=15)
        
        # Botones de acción
        export_btn = ctk.CTkButton(
            actions_frame,
            text="📊 Exportar",
            command=self.export_results,
            width=120,
            height=35
        )
        export_btn.pack(side="right", padx=(5, 20), pady=15)
        
        details_btn = ctk.CTkButton(
            actions_frame,
            text="👁️ Ver Detalles",
            command=self.show_details,
            width=120,
            height=35
        )
        details_btn.pack(side="right", padx=5, pady=15)

    def on_search_type_changed(self, value):
        """Maneja el cambio de tipo de búsqueda"""
        # Actualizar columnas de la tabla
        self.update_results_columns(value)

        # Mostrar/ocultar campos según el tipo
        if value == "productos":
            # Ocultar campos de monto para productos
            self.amounts_label.pack_forget()
            self.amount_from_label.pack_forget()
            self.amount_from_entry.pack_forget()
            self.amount_to_label.pack_forget()
            self.amount_to_entry.pack_forget()
        else:
            # Mostrar campos de monto para facturas
            self.amounts_label.pack(anchor="w", padx=10, pady=(10, 5))
            self.amount_from_label.pack(anchor="w", padx=10, pady=(0, 2))
            self.amount_from_entry.pack(fill="x", padx=10, pady=(0, 5))
            self.amount_to_label.pack(anchor="w", padx=10, pady=(0, 2))
            self.amount_to_entry.pack(fill="x", padx=10, pady=(0, 10))

    def update_results_columns(self, search_type):
        """Actualiza las columnas de la tabla según el tipo de búsqueda"""
        # Limpiar columnas existentes
        for col in self.results_tree["columns"]:
            self.results_tree.heading(col, text="")

        if search_type == "facturas":
            columns = ("numero", "fecha", "cliente", "total", "estado")
            headings = ("Número", "Fecha", "Cliente", "Total", "Estado")
            widths = (120, 100, 200, 100, 100)
        elif search_type == "productos":
            columns = ("referencia", "nombre", "precio", "categoria", "stock")
            headings = ("Referencia", "Nombre", "Precio", "Categoría", "Stock")
            widths = (120, 250, 100, 150, 80)
        elif search_type == "clientes":
            columns = ("nombre", "dni", "email", "telefono", "facturas")
            headings = ("Nombre", "DNI/NIE", "Email", "Teléfono", "Facturas")
            widths = (200, 120, 200, 120, 80)
        else:  # todo
            columns = ("tipo", "referencia", "nombre", "fecha", "valor")
            headings = ("Tipo", "Referencia", "Nombre/Cliente", "Fecha", "Valor")
            widths = (100, 120, 200, 100, 100)

        # Configurar columnas
        self.results_tree["columns"] = columns
        self.results_tree["show"] = "headings"

        for i, (col, heading, width) in enumerate(zip(columns, headings, widths)):
            self.results_tree.heading(col, text=heading)
            self.results_tree.column(col, width=width, minwidth=50)

    def load_initial_data(self):
        """Carga datos iniciales"""
        # Establecer fechas por defecto (último mes)
        today = datetime.now()
        last_month = today - timedelta(days=30)

        self.date_from.set(last_month.strftime("%Y-%m-%d"))
        self.date_to.set(today.strftime("%Y-%m-%d"))

        # Realizar búsqueda inicial
        self.perform_search()

    def search_today(self):
        """Búsqueda rápida: hoy"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_from.set(today)
        self.date_to.set(today)
        self.perform_search()

    def search_this_week(self):
        """Búsqueda rápida: esta semana"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())

        self.date_from.set(week_start.strftime("%Y-%m-%d"))
        self.date_to.set(today.strftime("%Y-%m-%d"))
        self.perform_search()

    def search_this_month(self):
        """Búsqueda rápida: este mes"""
        today = datetime.now()
        month_start = today.replace(day=1)

        self.date_from.set(month_start.strftime("%Y-%m-%d"))
        self.date_to.set(today.strftime("%Y-%m-%d"))
        self.perform_search()

    def search_low_stock(self):
        """Búsqueda rápida: productos con stock bajo"""
        self.search_type.set("productos")
        self.on_search_type_changed("productos")
        self.clear_filters()
        self.perform_search(low_stock_only=True)

    def clear_filters(self):
        """Limpia todos los filtros"""
        self.search_text.set("")
        self.date_from.set("")
        self.date_to.set("")
        self.amount_from.set("")
        self.amount_to.set("")
        self.client_filter.set("")
        self.status_filter.set("todos")

    def perform_search(self, low_stock_only=False):
        """Realiza la búsqueda según los filtros"""
        try:
            search_type = self.search_type.get()

            if search_type == "facturas":
                results = self.search_facturas()
            elif search_type == "productos":
                results = self.search_productos(low_stock_only)
            elif search_type == "clientes":
                results = self.search_clientes()
            else:  # todo
                results = self.search_all()

            self.display_results(results, search_type)

        except Exception as e:
            self.logger.error(f"Error en búsqueda: {e}")
            show_copyable_error(
                self.window,
                "Error de Búsqueda",
                f"Se produjo un error durante la búsqueda:\n\n{str(e)}\n\nVerifique los filtros e intente nuevamente."
            )

    def search_facturas(self):
        """Busca facturas según los filtros"""
        from database.database import db

        # Construir query base
        query = """
        SELECT numero_factura, fecha_factura, nombre_cliente, total_factura, 'Guardada' as estado
        FROM facturas
        WHERE 1=1
        """
        params = []

        # Filtro de texto
        search_text = self.search_text.get().strip()
        if search_text:
            query += " AND (numero_factura LIKE ? OR nombre_cliente LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%"])

        # Filtro de fechas
        date_from = self.date_from.get().strip()
        if date_from:
            query += " AND fecha_factura >= ?"
            params.append(date_from)

        date_to = self.date_to.get().strip()
        if date_to:
            query += " AND fecha_factura <= ?"
            params.append(date_to)

        # Filtro de montos
        amount_from = self.amount_from.get().strip()
        if amount_from:
            try:
                query += " AND total_factura >= ?"
                params.append(float(amount_from))
            except ValueError:
                pass

        amount_to = self.amount_to.get().strip()
        if amount_to:
            try:
                query += " AND total_factura <= ?"
                params.append(float(amount_to))
            except ValueError:
                pass

        query += " ORDER BY fecha_factura DESC, numero_factura DESC"

        return db.execute_query(query, params)

    def search_productos(self, low_stock_only=False):
        """Busca productos según los filtros"""
        from database.database import db

        # Query con JOIN para obtener stock
        query = """
        SELECT p.referencia, p.nombre, p.precio, p.categoria,
               COALESCE(s.cantidad_disponible, 0) as stock
        FROM productos p
        LEFT JOIN stock s ON p.id = s.producto_id
        WHERE 1=1
        """
        params = []

        # Filtro de stock bajo
        if low_stock_only:
            query += " AND COALESCE(s.cantidad_disponible, 0) <= 5"

        # Filtro de texto
        search_text = self.search_text.get().strip()
        if search_text:
            query += " AND (p.nombre LIKE ? OR p.referencia LIKE ? OR p.categoria LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"])

        query += " ORDER BY p.nombre"

        return db.execute_query(query, params)

    def search_clientes(self):
        """Busca clientes únicos de las facturas"""
        from database.database import db

        query = """
        SELECT nombre_cliente, dni_nie_cliente, email_cliente, telefono_cliente,
               COUNT(*) as num_facturas
        FROM facturas
        WHERE 1=1
        """
        params = []

        # Filtro de texto
        search_text = self.search_text.get().strip()
        if search_text:
            query += " AND (nombre_cliente LIKE ? OR dni_nie_cliente LIKE ? OR email_cliente LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"])

        query += " GROUP BY nombre_cliente, dni_nie_cliente, email_cliente, telefono_cliente"
        query += " ORDER BY nombre_cliente"

        return db.execute_query(query, params)

    def search_all(self):
        """Búsqueda global en todos los tipos"""
        results = []

        # Buscar en facturas
        facturas = self.search_facturas()
        for f in facturas:
            results.append(("Factura", f[0], f[2], f[1], f"{f[3]:.2f}€"))

        # Buscar en productos
        productos = self.search_productos()
        for p in productos:
            results.append(("Producto", p[0], p[1], "", f"{p[2]:.2f}€"))

        return results

    def display_results(self, results, search_type):
        """Muestra los resultados en la tabla"""
        # Limpiar resultados anteriores
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        # Guardar resultados
        self.search_results = results

        # Insertar nuevos resultados
        for result in results:
            self.results_tree.insert("", "end", values=result)

        # Actualizar información de resultados
        count = len(results)
        if count == 0:
            self.results_info.configure(text="No se encontraron resultados")
        elif count == 1:
            self.results_info.configure(text="1 resultado encontrado")
        else:
            self.results_info.configure(text=f"{count} resultados encontrados")

        # Actualizar título
        type_names = {
            "facturas": "Facturas",
            "productos": "Productos",
            "clientes": "Clientes",
            "todo": "Búsqueda Global"
        }
        type_name = type_names.get(search_type, "Resultados")
        self.results_title.configure(text=f"Resultados: {type_name}")

    def on_result_double_click(self, event):
        """Maneja el doble clic en un resultado"""
        selection = self.results_tree.selection()
        if not selection:
            return

        item = self.results_tree.item(selection[0])
        values = item['values']

        if not values:
            return

        search_type = self.search_type.get()

        if search_type == "facturas":
            self.show_factura_details(values)
        elif search_type == "productos":
            self.show_producto_details(values)
        elif search_type == "clientes":
            self.show_cliente_details(values)
        else:  # todo
            self.show_global_details(values)

    def show_factura_details(self, values):
        """Muestra detalles de una factura"""
        numero, fecha, cliente, total, estado = values

        details = f"""📄 Detalles de Factura

Información básica:
- Número de factura: {numero}
- Fecha: {fecha}
- Cliente: {cliente}
- Total: {total}€
- Estado: {estado}

Acciones disponibles:
- Doble clic para ver más detalles
- Exportar resultados para análisis
- Generar PDF de la factura

Esta información puede ser copiada para referencia."""

        show_copyable_info(self.window, f"Factura {numero}", details)

    def show_producto_details(self, values):
        """Muestra detalles de un producto"""
        referencia, nombre, precio, categoria, stock = values

        # Determinar estado del stock
        stock_num = int(stock) if str(stock).isdigit() else 0
        if stock_num == 0:
            stock_status = "🔴 Sin Stock"
        elif stock_num <= 5:
            stock_status = f"🟠 Stock Bajo ({stock_num})"
        elif stock_num <= 10:
            stock_status = f"🟡 Stock Medio ({stock_num})"
        else:
            stock_status = f"🟢 Stock OK ({stock_num})"

        details = f"""📦 Detalles de Producto

Información básica:
- Referencia: {referencia}
- Nombre: {nombre}
- Precio: {precio}€
- Categoría: {categoria}
- Stock disponible: {stock} unidades
- Estado: {stock_status}

Recomendaciones:
{self.get_stock_recommendations(stock_num)}

Esta información puede ser copiada para gestión de inventario."""

        show_copyable_info(self.window, f"Producto {referencia}", details)

    def show_cliente_details(self, values):
        """Muestra detalles de un cliente"""
        nombre, dni, email, telefono, num_facturas = values

        details = f"""👤 Detalles de Cliente

Información personal:
- Nombre: {nombre}
- DNI/NIE: {dni or 'No especificado'}
- Email: {email or 'No especificado'}
- Teléfono: {telefono or 'No especificado'}

Historial comercial:
- Número de facturas: {num_facturas}
- Estado: Cliente {'frecuente' if int(num_facturas) > 5 else 'ocasional'}

Esta información puede ser copiada para gestión de clientes."""

        show_copyable_info(self.window, f"Cliente {nombre}", details)

    def show_global_details(self, values):
        """Muestra detalles de búsqueda global"""
        tipo, referencia, nombre, fecha, valor = values

        details = f"""🔍 Resultado de Búsqueda Global

Información encontrada:
- Tipo: {tipo}
- Referencia/Número: {referencia}
- Nombre/Cliente: {nombre}
- Fecha: {fecha or 'N/A'}
- Valor: {valor}

Para más detalles, cambie el tipo de búsqueda específico.

Esta información puede ser copiada para análisis."""

        show_copyable_info(self.window, f"{tipo} {referencia}", details)

    def get_stock_recommendations(self, stock_num):
        """Obtiene recomendaciones según el nivel de stock"""
        if stock_num == 0:
            return "⚠️ URGENTE: Reaprovisionar inmediatamente\n⚠️ Producto sin disponibilidad para venta"
        elif stock_num <= 5:
            return "⚠️ Reaprovisionar pronto\n⚠️ Stock crítico, contactar proveedor"
        elif stock_num <= 10:
            return "📋 Considerar reposición\n📋 Stock en nivel medio"
        else:
            return "✅ Stock adecuado\n✅ No requiere acción inmediata"

    def show_details(self):
        """Muestra detalles del elemento seleccionado"""
        selection = self.results_tree.selection()
        if not selection:
            show_copyable_info(
                self.window,
                "Sin Selección",
                "Seleccione un elemento de la lista para ver sus detalles.\n\nPuede hacer doble clic en cualquier fila o usar este botón después de seleccionar."
            )
            return

        # Simular doble clic
        event = type('Event', (), {})()
        self.on_result_double_click(event)

    def export_results(self):
        """Exporta los resultados a un archivo"""
        if not self.search_results:
            show_copyable_info(
                self.window,
                "Sin Resultados",
                "No hay resultados para exportar.\n\nRealice una búsqueda primero y luego podrá exportar los resultados encontrados."
            )
            return

        try:
            # Crear contenido para exportar
            search_type = self.search_type.get()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Generar contenido CSV
            csv_content = self.generate_csv_content()

            # Guardar archivo
            filename = f"busqueda_{search_type}_{timestamp}.csv"
            filepath = os.path.join(os.getcwd(), filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(csv_content)

            # Mensaje de éxito
            success_msg = f"""✅ Resultados exportados exitosamente

Detalles de la exportación:
- Archivo: {filename}
- Ubicación: {filepath}
- Formato: CSV (compatible con Excel)
- Registros: {len(self.search_results)}
- Tipo de búsqueda: {search_type.title()}
- Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Contenido exportado:
- Todos los resultados de la búsqueda actual
- Encabezados de columna incluidos
- Formato compatible con Excel y otras aplicaciones
- Codificación UTF-8 para caracteres especiales

El archivo está listo para:
✅ Abrir en Excel o LibreOffice
✅ Importar en otras aplicaciones
✅ Compartir por email
✅ Archivar para referencia futura

Esta información puede ser copiada para documentación."""

            show_copyable_info(self.window, "Exportación Exitosa", success_msg)

        except Exception as e:
            error_msg = f"""❌ Error exportando resultados

Se produjo un error durante la exportación:

Detalles del error:
- Error: {str(e)}
- Tipo: {type(e).__name__}
- Función: export_results()
- Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Información del contexto:
- Resultados a exportar: {len(self.search_results)}
- Tipo de búsqueda: {search_type}

Posibles causas:
- Permisos de escritura insuficientes
- Espacio en disco insuficiente
- Caracteres especiales en los datos
- Archivo en uso por otra aplicación

Acciones recomendadas:
1. Verificar permisos de escritura en el directorio
2. Comprobar espacio disponible en disco
3. Cerrar Excel u otras aplicaciones que puedan usar el archivo
4. Intentar exportar nuevamente

Los resultados de búsqueda siguen disponibles en la aplicación.
Copie este mensaje para soporte técnico."""

            show_copyable_error(self.window, "Error de Exportación", error_msg)

    def generate_csv_content(self):
        """Genera el contenido CSV para exportar"""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # Escribir encabezados según el tipo de búsqueda
        search_type = self.search_type.get()

        if search_type == "facturas":
            writer.writerow(["Número", "Fecha", "Cliente", "Total", "Estado"])
        elif search_type == "productos":
            writer.writerow(["Referencia", "Nombre", "Precio", "Categoría", "Stock"])
        elif search_type == "clientes":
            writer.writerow(["Nombre", "DNI/NIE", "Email", "Teléfono", "Facturas"])
        else:  # todo
            writer.writerow(["Tipo", "Referencia", "Nombre/Cliente", "Fecha", "Valor"])

        # Escribir datos
        for result in self.search_results:
            writer.writerow(result)

        return output.getvalue()
