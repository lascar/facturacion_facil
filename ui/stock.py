import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from utils.translations import get_text
from database.models import Stock, Producto, StockMovement
from common.ui_components import BaseWindow
from common.custom_dialogs import (
    show_copyable_info, show_copyable_success,
    show_copyable_warning, show_copyable_error,
    show_copyable_confirm
)
from utils.logger import get_logger

class StockWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(get_text("gestion_stock"))
        self.window.geometry("1000x700")
        self.window.transient(parent)
        self.logger = get_logger("stock_window")

        # Configurar ventana para que aparezca al frente
        self.setup_window_focus()

        # Variables
        self.stock_data = []
        self.filtered_data = []
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_stock)

        self.create_widgets()
        self.load_stock_data()

        # Asegurar que la ventana esté al frente después de cargar datos
        self.window.after(100, self.ensure_window_focus)

    def setup_window_focus(self):
        """Configura la ventana para que aparezca correctamente al frente"""
        try:
            # Configuraciones básicas de ventana
            self.window.lift()
            self.window.focus_force()
            self.window.attributes('-topmost', True)

            # Centrar la ventana en la pantalla
            self.center_window()

            # Programar para quitar topmost después de un momento
            self.window.after(500, lambda: self.window.attributes('-topmost', False))

        except Exception as e:
            self.logger.error(f"Error configurando foco de ventana: {e}")

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

    def ensure_window_focus(self):
        """Asegura que la ventana mantenga el foco"""
        try:
            if self.window.winfo_exists():
                self.window.lift()
                self.window.focus_force()
                self.window.tkraise()
        except Exception as e:
            self.logger.error(f"Error asegurando foco: {e}")

    def setup_modal_window_focus(self, modal_window):
        """Configura una ventana modal para que aparezca correctamente al frente"""
        try:
            # Configuraciones para ventana modal
            modal_window.lift()
            modal_window.focus_force()
            modal_window.attributes('-topmost', True)
            modal_window.grab_set()  # Hacer modal

            # Centrar la ventana modal
            self.center_modal_window(modal_window)

            # Programar para quitar topmost después de un momento pero mantener modal
            modal_window.after(500, lambda: modal_window.attributes('-topmost', False))

        except Exception as e:
            self.logger.error(f"Error configurando ventana modal: {e}")

    def center_modal_window(self, modal_window):
        """Centra una ventana modal respecto a su padre"""
        try:
            modal_window.update_idletasks()

            # Obtener dimensiones de la ventana modal
            modal_width = modal_window.winfo_width()
            modal_height = modal_window.winfo_height()

            # Obtener posición y dimensiones de la ventana padre
            parent_x = self.window.winfo_x()
            parent_y = self.window.winfo_y()
            parent_width = self.window.winfo_width()
            parent_height = self.window.winfo_height()

            # Calcular posición centrada
            x = parent_x + (parent_width // 2) - (modal_width // 2)
            y = parent_y + (parent_height // 2) - (modal_height // 2)

            # Asegurar que la ventana esté dentro de la pantalla
            screen_width = modal_window.winfo_screenwidth()
            screen_height = modal_window.winfo_screenheight()

            x = max(0, min(x, screen_width - modal_width))
            y = max(0, min(y, screen_height - modal_height))

            modal_window.geometry(f"{modal_width}x{modal_height}+{x}+{y}")

        except Exception as e:
            self.logger.error(f"Error centrando ventana modal: {e}")

    def show_success_message(self, title, message):
        """Muestra un mensaje de éxito con texto copiable"""
        try:
            self.ensure_window_focus()
            return show_copyable_success(self.window, title, message)
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de éxito: {e}")
            # Fallback con messagebox estándar
            messagebox.showinfo(title, message, parent=self.window)
            return True

    def show_error_message(self, title, message):
        """Muestra un mensaje de error con texto copiable"""
        try:
            self.ensure_window_focus()
            return show_copyable_error(self.window, title, message)
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de error: {e}")
            # Fallback con messagebox estándar
            messagebox.showerror(title, message, parent=self.window)
            return True

    def show_warning_message(self, title, message):
        """Muestra un mensaje de advertencia con texto copiable"""
        try:
            self.ensure_window_focus()
            return show_copyable_warning(self.window, title, message)
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje de advertencia: {e}")
            # Fallback con messagebox estándar
            messagebox.showwarning(title, message, parent=self.window)
            return True

    def show_info_message(self, title, message):
        """Muestra un mensaje informativo con texto copiable"""
        try:
            self.ensure_window_focus()
            return show_copyable_info(self.window, title, message)
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje informativo: {e}")
            # Fallback con messagebox estándar
            messagebox.showinfo(title, message, parent=self.window)
            return True

    def create_widgets(self):
        """Crea la interfaz de usuario"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text=get_text("gestion_stock"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        # Frame de controles superiores
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Búsqueda
        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=20)

        search_label = ctk.CTkLabel(search_frame, text="Buscar:")
        search_label.pack(side="left", padx=(10, 5))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Buscar por nombre o referencia..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botones de acción
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(side="right", padx=(10, 20), pady=20)

        refresh_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Actualizar",
            command=self.load_stock_data,
            width=120
        )
        refresh_btn.pack(side="left", padx=5)

        low_stock_btn = ctk.CTkButton(
            buttons_frame,
            text="⚠️ Stock Bajo",
            command=self.show_low_stock,
            width=120,
            fg_color="orange",
            hover_color="darkorange"
        )
        low_stock_btn.pack(side="left", padx=5)

        # Frame para la tabla de stock
        self.create_stock_table(main_frame)

    def create_stock_table(self, parent):
        """Crea la tabla de stock"""
        # Frame contenedor con scroll
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Encabezados
        headers_frame = ctk.CTkFrame(table_frame)
        headers_frame.pack(fill="x", padx=10, pady=(10, 0))

        headers = [
            ("Producto", 0.25),
            ("Referencia", 0.15),
            ("Stock Actual", 0.12),
            ("Estado", 0.12),
            ("Última Actualización", 0.16),
            ("Acciones", 0.20)
        ]

        for header, width in headers:
            label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(weight="bold")
            )
            label.pack(side="left", fill="x", expand=True if width > 0.2 else False,
                      padx=5, pady=5)

        # Frame scrollable para los datos
        self.scrollable_frame = ctk.CTkScrollableFrame(table_frame)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def load_stock_data(self):
        """Carga los datos de stock desde la base de datos"""
        try:
            # Obtener datos de stock con información de productos
            query_results = Stock.get_all()
            self.stock_data = []

            for row in query_results:
                producto_id, cantidad, nombre, referencia = row

                # Obtener fecha de última actualización
                from database.database import db
                fecha_query = "SELECT fecha_actualizacion FROM stock WHERE producto_id=?"
                fecha_result = db.execute_query(fecha_query, (producto_id,))
                fecha_actualizacion = fecha_result[0][0] if fecha_result else "N/A"

                self.stock_data.append({
                    'producto_id': producto_id,
                    'nombre': nombre,
                    'referencia': referencia,
                    'cantidad': cantidad,
                    'fecha_actualizacion': fecha_actualizacion
                })

            self.filtered_data = self.stock_data.copy()
            self.update_stock_display()
            self.logger.info(f"Cargados {len(self.stock_data)} productos en stock")

        except Exception as e:
            self.logger.error(f"Error cargando datos de stock: {e}")
            self.show_error_message("Error", f"Error cargando datos de stock: {e}")

    def update_stock_display(self):
        """Actualiza la visualización de la tabla de stock"""
        # Limpiar frame scrollable
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.filtered_data:
            no_data_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay productos en stock",
                font=ctk.CTkFont(size=16)
            )
            no_data_label.pack(pady=50)
            return

        # Crear filas de datos
        for i, item in enumerate(self.filtered_data):
            self.create_stock_row(item, i)

    def create_stock_row(self, item, row_index):
        """Crea una fila de la tabla de stock"""
        # Frame para la fila
        row_frame = ctk.CTkFrame(self.scrollable_frame)
        row_frame.pack(fill="x", padx=5, pady=2)

        # Determinar color según el stock
        cantidad = item['cantidad']
        if cantidad == 0:
            stock_color = "red"
            estado_text = "Sin Stock"
        elif cantidad <= 5:
            stock_color = "orange"
            estado_text = "Stock Bajo"
        elif cantidad <= 10:
            stock_color = "yellow"
            estado_text = "Stock Medio"
        else:
            stock_color = "green"
            estado_text = "Stock OK"

        # Nombre del producto
        nombre_label = ctk.CTkLabel(
            row_frame,
            text=item['nombre'][:30] + "..." if len(item['nombre']) > 30 else item['nombre'],
            anchor="w"
        )
        nombre_label.pack(side="left", fill="x", expand=True, padx=(10, 5))

        # Referencia
        ref_label = ctk.CTkLabel(
            row_frame,
            text=item['referencia'],
            anchor="w",
            width=120
        )
        ref_label.pack(side="left", padx=5)

        # Cantidad actual
        cantidad_label = ctk.CTkLabel(
            row_frame,
            text=str(cantidad),
            anchor="center",
            width=80,
            text_color=stock_color
        )
        cantidad_label.pack(side="left", padx=5)

        # Estado
        estado_label = ctk.CTkLabel(
            row_frame,
            text=estado_text,
            anchor="center",
            width=100,
            text_color=stock_color
        )
        estado_label.pack(side="left", padx=5)

        # Fecha actualización
        fecha_text = item['fecha_actualizacion']
        if fecha_text and fecha_text != "N/A":
            try:
                from datetime import datetime
                fecha_dt = datetime.fromisoformat(fecha_text.replace('Z', '+00:00'))
                fecha_text = fecha_dt.strftime("%d/%m/%Y %H:%M")
            except:
                pass

        fecha_label = ctk.CTkLabel(
            row_frame,
            text=fecha_text[:16] if fecha_text else "N/A",
            anchor="center",
            width=130
        )
        fecha_label.pack(side="left", padx=5)

        # Botones de acción
        actions_frame = ctk.CTkFrame(row_frame)
        actions_frame.pack(side="right", padx=(5, 10))

        # Botón modificar stock
        modify_btn = ctk.CTkButton(
            actions_frame,
            text="✏️",
            width=30,
            height=25,
            command=lambda: self.modify_stock(item)
        )
        modify_btn.pack(side="left", padx=2)

        # Botón agregar stock
        add_btn = ctk.CTkButton(
            actions_frame,
            text="➕",
            width=30,
            height=25,
            fg_color="green",
            hover_color="darkgreen",
            command=lambda: self.add_stock(item)
        )
        add_btn.pack(side="left", padx=2)

        # Botón quitar stock
        remove_btn = ctk.CTkButton(
            actions_frame,
            text="➖",
            width=30,
            height=25,
            fg_color="red",
            hover_color="darkred",
            command=lambda: self.remove_stock(item)
        )
        remove_btn.pack(side="left", padx=2)

        # Botón historial
        history_btn = ctk.CTkButton(
            actions_frame,
            text="📋",
            width=30,
            height=25,
            fg_color="gray",
            hover_color="darkgray",
            command=lambda: self.show_stock_history(item)
        )
        history_btn.pack(side="left", padx=2)

    def filter_stock(self, *args):
        """Filtra los datos de stock según el texto de búsqueda"""
        search_text = self.search_var.get().lower()

        if not search_text:
            self.filtered_data = self.stock_data.copy()
        else:
            self.filtered_data = [
                item for item in self.stock_data
                if search_text in item['nombre'].lower() or
                   search_text in item['referencia'].lower()
            ]

        self.update_stock_display()

    def show_low_stock(self):
        """Muestra solo productos con stock bajo (<=5)"""
        self.filtered_data = [
            item for item in self.stock_data
            if item['cantidad'] <= 5
        ]
        self.update_stock_display()

        if not self.filtered_data:
            self.show_info_message("Stock Bajo", "No hay productos con stock bajo.")

    def modify_stock(self, item):
        """Permite modificar directamente la cantidad de stock"""
        try:
            # Asegurar que la ventana esté al frente antes del diálogo
            self.ensure_window_focus()

            current_stock = item['cantidad']
            new_stock = simpledialog.askinteger(
                "Modificar Stock",
                f"Stock actual de '{item['nombre']}': {current_stock}\n\nIngrese la nueva cantidad:",
                initialvalue=current_stock,
                minvalue=0,
                parent=self.window
            )

            if new_stock is not None and new_stock != current_stock:
                # Actualizar en base de datos
                stock_obj = Stock(item['producto_id'], new_stock)
                stock_obj.save()

                # Registrar movimiento
                diferencia = new_stock - current_stock
                tipo_movimiento = "AJUSTE_POSITIVO" if diferencia > 0 else "AJUSTE_NEGATIVO"
                descripcion = f"Ajuste manual: {current_stock} -> {new_stock}"
                StockMovement.create(item['producto_id'], diferencia, tipo_movimiento, descripcion)

                # Actualizar en memoria
                item['cantidad'] = new_stock

                # Refrescar display
                self.update_stock_display()

                self.logger.info(f"Stock modificado para producto {item['producto_id']}: {current_stock} -> {new_stock}")
                self.show_success_message("Éxito", f"Stock actualizado correctamente.\nAnterior: {current_stock}\nNuevo: {new_stock}")

        except Exception as e:
            self.logger.error(f"Error modificando stock: {e}")
            self.show_error_message("Error", f"Error modificando stock: {e}")

    def add_stock(self, item):
        """Permite agregar stock a un producto"""
        try:
            # Asegurar que la ventana esté al frente antes del diálogo
            self.ensure_window_focus()

            cantidad_agregar = simpledialog.askinteger(
                "Agregar Stock",
                f"Producto: {item['nombre']}\nStock actual: {item['cantidad']}\n\n¿Cuántas unidades desea agregar?",
                minvalue=1,
                parent=self.window
            )

            if cantidad_agregar:
                new_stock = item['cantidad'] + cantidad_agregar

                # Actualizar en base de datos
                stock_obj = Stock(item['producto_id'], new_stock)
                stock_obj.save()

                # Registrar movimiento
                descripcion = f"Entrada manual de {cantidad_agregar} unidades"
                StockMovement.create(item['producto_id'], cantidad_agregar, "ENTRADA", descripcion)

                # Actualizar en memoria
                old_stock = item['cantidad']
                item['cantidad'] = new_stock

                # Refrescar display
                self.update_stock_display()

                self.logger.info(f"Stock agregado para producto {item['producto_id']}: +{cantidad_agregar} (total: {new_stock})")
                self.show_success_message("Éxito", f"Stock agregado correctamente.\nAnterior: {old_stock}\nAgregado: +{cantidad_agregar}\nNuevo total: {new_stock}")

        except Exception as e:
            self.logger.error(f"Error agregando stock: {e}")
            self.show_error_message("Error", f"Error agregando stock: {e}")

    def remove_stock(self, item):
        """Permite quitar stock de un producto"""
        try:
            current_stock = item['cantidad']
            if current_stock == 0:
                self.show_warning_message("Advertencia", "No hay stock disponible para quitar.")
                return

            # Asegurar que la ventana esté al frente antes del diálogo
            self.ensure_window_focus()

            cantidad_quitar = simpledialog.askinteger(
                "Quitar Stock",
                f"Producto: {item['nombre']}\nStock actual: {current_stock}\n\n¿Cuántas unidades desea quitar?",
                minvalue=1,
                maxvalue=current_stock,
                parent=self.window
            )

            if cantidad_quitar:
                new_stock = current_stock - cantidad_quitar

                # Actualizar en base de datos
                stock_obj = Stock(item['producto_id'], new_stock)
                stock_obj.save()

                # Registrar movimiento
                descripcion = f"Salida manual de {cantidad_quitar} unidades"
                StockMovement.create(item['producto_id'], -cantidad_quitar, "SALIDA", descripcion)

                # Actualizar en memoria
                item['cantidad'] = new_stock

                # Refrescar display
                self.update_stock_display()

                self.logger.info(f"Stock removido para producto {item['producto_id']}: -{cantidad_quitar} (total: {new_stock})")
                self.show_success_message("Éxito", f"Stock removido correctamente.\nAnterior: {current_stock}\nRemovido: -{cantidad_quitar}\nNuevo total: {new_stock}")

                # Advertir si el stock queda bajo
                if new_stock <= 5:
                    self.show_warning_message("Stock Bajo", f"¡Atención! El stock de '{item['nombre']}' está bajo ({new_stock} unidades).")

        except Exception as e:
            self.logger.error(f"Error removiendo stock: {e}")
            self.show_error_message("Error", f"Error removiendo stock: {e}")

    def show_stock_history(self, item):
        """Muestra el historial de movimientos de stock de un producto"""
        try:
            # Crear ventana de historial
            history_window = ctk.CTkToplevel(self.window)
            history_window.title(f"Historial de Stock - {item['nombre']}")
            history_window.geometry("800x500")
            history_window.transient(self.window)

            # Configurar ventana para que aparezca al frente
            self.setup_modal_window_focus(history_window)

            # Título
            title_label = ctk.CTkLabel(
                history_window,
                text=f"Historial de Stock - {item['nombre']}",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            title_label.pack(pady=20)

            # Info del producto
            info_frame = ctk.CTkFrame(history_window)
            info_frame.pack(fill="x", padx=20, pady=(0, 20))

            info_text = f"Referencia: {item['referencia']} | Stock Actual: {item['cantidad']} unidades"
            info_label = ctk.CTkLabel(info_frame, text=info_text)
            info_label.pack(pady=10)

            # Frame para la tabla de historial
            table_frame = ctk.CTkFrame(history_window)
            table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

            # Encabezados
            headers_frame = ctk.CTkFrame(table_frame)
            headers_frame.pack(fill="x", padx=10, pady=(10, 0))

            headers = ["Fecha", "Tipo", "Cantidad", "Descripción"]
            for header in headers:
                label = ctk.CTkLabel(
                    headers_frame,
                    text=header,
                    font=ctk.CTkFont(weight="bold")
                )
                label.pack(side="left", fill="x", expand=True, padx=5, pady=5)

            # Frame scrollable para los movimientos
            scrollable_frame = ctk.CTkScrollableFrame(table_frame)
            scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Obtener movimientos
            movements = StockMovement.get_by_product(item['producto_id'], limit=50)

            if not movements:
                no_data_label = ctk.CTkLabel(
                    scrollable_frame,
                    text="No hay movimientos registrados para este producto",
                    font=ctk.CTkFont(size=14)
                )
                no_data_label.pack(pady=50)
            else:
                # Crear filas de movimientos
                for movement in movements:
                    self.create_movement_row(scrollable_frame, movement)

            # Botón cerrar
            close_btn = ctk.CTkButton(
                history_window,
                text="Cerrar",
                command=history_window.destroy,
                width=100
            )
            close_btn.pack(pady=20)

        except Exception as e:
            self.logger.error(f"Error mostrando historial: {e}")
            self.show_error_message("Error", f"Error mostrando historial: {e}")

    def create_movement_row(self, parent, movement):
        """Crea una fila para un movimiento de stock"""
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", padx=5, pady=2)

        # Formatear fecha
        fecha_text = movement.fecha_movimiento
        if fecha_text:
            try:
                from datetime import datetime
                fecha_dt = datetime.fromisoformat(fecha_text.replace('Z', '+00:00'))
                fecha_text = fecha_dt.strftime("%d/%m/%Y %H:%M")
            except:
                pass

        # Fecha
        fecha_label = ctk.CTkLabel(
            row_frame,
            text=fecha_text[:16] if fecha_text else "N/A",
            anchor="w"
        )
        fecha_label.pack(side="left", fill="x", expand=True, padx=5)

        # Tipo con color
        tipo_colors = {
            "ENTRADA": "green",
            "SALIDA": "red",
            "VENTA": "orange",
            "AJUSTE_POSITIVO": "blue",
            "AJUSTE_NEGATIVO": "purple",
            "INICIAL": "gray"
        }

        tipo_color = tipo_colors.get(movement.tipo, "white")
        tipo_label = ctk.CTkLabel(
            row_frame,
            text=movement.tipo,
            anchor="center",
            text_color=tipo_color
        )
        tipo_label.pack(side="left", fill="x", expand=True, padx=5)

        # Cantidad con signo y color
        cantidad_text = f"+{movement.cantidad}" if movement.cantidad > 0 else str(movement.cantidad)
        cantidad_color = "green" if movement.cantidad > 0 else "red"

        cantidad_label = ctk.CTkLabel(
            row_frame,
            text=cantidad_text,
            anchor="center",
            text_color=cantidad_color
        )
        cantidad_label.pack(side="left", fill="x", expand=True, padx=5)

        # Descripción
        descripcion_text = movement.descripcion[:40] + "..." if len(movement.descripcion) > 40 else movement.descripcion
        descripcion_label = ctk.CTkLabel(
            row_frame,
            text=descripcion_text,
            anchor="w"
        )
        descripcion_label.pack(side="left", fill="x", expand=True, padx=5)
