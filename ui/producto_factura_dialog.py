# -*- coding: utf-8 -*-
"""
Diálogo para agregar/editar productos en facturas
"""
import customtkinter as ctk
import tkinter as tk
from utils.translations import get_text
from utils.logger import get_logger
from common.validators import FormValidator, CalculationHelper
from common.ui_components import FormHelper
from database.models import Stock

class ProductoFacturaDialog:
    """Diálogo para seleccionar y configurar un producto para la factura"""
    
    def __init__(self, parent, productos_disponibles, producto_seleccionado=None,
                 cantidad_inicial=1, precio_inicial=None, iva_inicial=None, descuento_inicial=0):
        self.parent = parent
        self.productos_disponibles = productos_disponibles
        self.producto_seleccionado = producto_seleccionado
        self.result = None
        self.logger = get_logger("producto_factura_dialog")
        
        # Crear ventana de diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Agregar/Editar Producto")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)

        # Variables
        self.cantidad_inicial = cantidad_inicial
        self.precio_inicial = precio_inicial
        self.iva_inicial = iva_inicial
        self.descuento_inicial = descuento_inicial

        self.create_widgets()

        # Si hay producto seleccionado, cargarlo
        if self.producto_seleccionado:
            self.load_producto_data()

        # Hacer modal después de crear todos los widgets
        self.dialog.update_idletasks()  # Asegurar que la ventana esté completamente creada
        self.dialog.grab_set()  # Modal
        self.dialog.lift()
        self.dialog.focus_force()

        # Configurar scroll DESPUÉS de grab_set para que tenga prioridad
        self.configure_mousewheel_scrolling_aggressive()
    
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        # Frame principal scrollable
        main_frame = ctk.CTkScrollableFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Guardar referencia al frame scrollable para el scroll
        self.main_scrollable_frame = main_frame
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Configurar Producto para Factura",
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # Selección de producto
        self.create_producto_selection(main_frame)
        
        # Configuración del producto
        self.create_producto_config(main_frame)
        
        # Preview de totales
        self.create_totales_preview(main_frame)

        # Botones
        self.create_buttons(main_frame)

        # Inicialización automática del primer producto si es necesario
        self.initialize_first_product_if_needed()

    def initialize_first_product_if_needed(self):
        """Inicializa automáticamente el primer producto si no hay ninguno seleccionado"""
        if hasattr(self, '_needs_auto_init') and self._needs_auto_init:
            productos_names = [f"{p.nombre} ({p.referencia}) - {CalculationHelper.format_currency(p.precio)}"
                              for p in self.productos_disponibles]
            if productos_names:
                self.producto_combo.set(productos_names[0])
                # Llamar manualmente a la función de selección para inicializar
                self.on_producto_selected(productos_names[0])

    def create_producto_selection(self, parent):
        """Crea la sección de selección de producto"""
        selection_frame = ctk.CTkFrame(parent)
        selection_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(selection_frame, text="Seleccionar Producto:",
                   font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # ComboBox para productos con información de stock
        productos_names = []
        for p in self.productos_disponibles:
            stock_actual = Stock.get_by_product(p.id)
            stock_info = f"Stock: {stock_actual}"
            if stock_actual == 0:
                stock_info = "🔴 Sin Stock"
            elif stock_actual <= 5:
                stock_info = f"🟠 Stock Bajo: {stock_actual}"
            elif stock_actual <= 10:
                stock_info = f"🟡 Stock: {stock_actual}"
            else:
                stock_info = f"🟢 Stock: {stock_actual}"

            producto_text = f"{p.nombre} ({p.referencia}) - {CalculationHelper.format_currency(p.precio)} - {stock_info}"
            productos_names.append(producto_text)
        
        self.producto_combo = ctk.CTkComboBox(selection_frame, values=productos_names,
                                            command=self.on_producto_selected, width=400)
        self.producto_combo.pack(padx=10, pady=5)

        # Información del producto seleccionado (crear antes de la inicialización)
        self.info_frame = ctk.CTkFrame(selection_frame)
        self.info_frame.pack(fill="x", padx=10, pady=5)

        self.info_label = ctk.CTkLabel(self.info_frame, text="Seleccione un producto para ver detalles",
                                     wraplength=400)
        self.info_label.pack(pady=10)

        # Botón para actualizar stock
        refresh_btn = ctk.CTkButton(
            selection_frame,
            text="🔄 Actualizar Stock",
            command=self.refresh_stock_info,
            width=150,
            height=25
        )
        refresh_btn.pack(pady=5)

        # Marcar que necesitamos inicializar el primer producto después
        self._needs_auto_init = not self.producto_seleccionado and productos_names
    
    def create_producto_config(self, parent):
        """Crea la sección de configuración del producto"""
        config_frame = ctk.CTkFrame(parent)
        config_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(config_frame, text="Configuración:",
                   font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # Frame para campos en dos columnas
        fields_frame = ctk.CTkFrame(config_frame)
        fields_frame.pack(fill="x", padx=10, pady=5)
        
        # Columna izquierda
        left_col = ctk.CTkFrame(fields_frame)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Cantidad
        ctk.CTkLabel(left_col, text=get_text("cantidad") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.cantidad_entry = ctk.CTkEntry(left_col, placeholder_text="1")
        self.cantidad_entry.pack(fill="x", padx=10, pady=5)
        self.cantidad_entry.bind("<KeyRelease>", self.update_preview)
        
        # Precio unitario
        ctk.CTkLabel(left_col, text=get_text("precio_unitario") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.precio_entry = ctk.CTkEntry(left_col, placeholder_text="0.00")
        self.precio_entry.pack(fill="x", padx=10, pady=5)
        self.precio_entry.bind("<KeyRelease>", self.update_preview)
        
        # Columna derecha
        right_col = ctk.CTkFrame(fields_frame)
        right_col.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # IVA aplicado
        ctk.CTkLabel(right_col, text=get_text("iva_aplicado") + "*").pack(anchor="w", padx=10, pady=(10, 0))
        self.iva_entry = ctk.CTkEntry(right_col, placeholder_text="21.0")
        self.iva_entry.pack(fill="x", padx=10, pady=5)
        self.iva_entry.bind("<KeyRelease>", self.update_preview)
        
        # Descuento
        ctk.CTkLabel(right_col, text="Descuento (%)").pack(anchor="w", padx=10, pady=(10, 0))
        self.descuento_entry = ctk.CTkEntry(right_col, placeholder_text="0.0")
        self.descuento_entry.pack(fill="x", padx=10, pady=5)
        self.descuento_entry.bind("<KeyRelease>", self.update_preview)
        
        # Establecer valores iniciales
        FormHelper.set_entry_value(self.cantidad_entry, str(self.cantidad_inicial))
        FormHelper.set_entry_value(self.descuento_entry, str(self.descuento_inicial))
    
    def create_totales_preview(self, parent):
        """Crea la sección de preview de totales"""
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(preview_frame, text="Preview de Totales:",
                   font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        
        # Grid para totales
        totales_grid = ctk.CTkFrame(preview_frame)
        totales_grid.pack(fill="x", padx=10, pady=5)
        
        # Subtotal
        ctk.CTkLabel(totales_grid, text="Subtotal:").grid(row=0, column=0, sticky="w", padx=10, pady=2)
        self.subtotal_preview = ctk.CTkLabel(totales_grid, text="0.00 €")
        self.subtotal_preview.grid(row=0, column=1, sticky="e", padx=10, pady=2)
        
        # Descuento
        ctk.CTkLabel(totales_grid, text="Descuento:").grid(row=1, column=0, sticky="w", padx=10, pady=2)
        self.descuento_preview = ctk.CTkLabel(totales_grid, text="0.00 €")
        self.descuento_preview.grid(row=1, column=1, sticky="e", padx=10, pady=2)
        
        # IVA
        ctk.CTkLabel(totales_grid, text="IVA:").grid(row=2, column=0, sticky="w", padx=10, pady=2)
        self.iva_preview = ctk.CTkLabel(totales_grid, text="0.00 €")
        self.iva_preview.grid(row=2, column=1, sticky="e", padx=10, pady=2)
        
        # Total
        ctk.CTkLabel(totales_grid, text="Total:", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.total_preview = ctk.CTkLabel(totales_grid, text="0.00 €", font=ctk.CTkFont(weight="bold"))
        self.total_preview.grid(row=3, column=1, sticky="e", padx=10, pady=5)
        
        # Configurar grid
        totales_grid.grid_columnconfigure(1, weight=1)
    
    def create_buttons(self, parent):
        """Crea los botones del diálogo"""
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=10, pady=20)
        
        # Botón cancelar
        cancel_btn = ctk.CTkButton(buttons_frame, text=get_text("cancelar"),
                                 command=self.cancel, width=120)
        cancel_btn.pack(side="left", padx=10)
        
        # Botón aceptar
        accept_btn = ctk.CTkButton(buttons_frame, text=get_text("aceptar"),
                                 command=self.accept, width=120,
                                 fg_color="#2E8B57", hover_color="#228B22")
        accept_btn.pack(side="right", padx=10)
    
    def on_producto_selected(self, selection):
        """Maneja la selección de un producto"""
        try:
            if not selection:
                return

            # Encontrar el producto seleccionado usando el parámetro selection
            # El formato es: "Nombre (Referencia) - Precio"
            nombre_producto = selection.split(" (")[0]
            producto = next((p for p in self.productos_disponibles if p.nombre == nombre_producto), None)

            if not producto:
                # Fallback: usar el valor actual del combo
                combo_value = self.producto_combo.get()
                if combo_value:
                    nombre_producto = combo_value.split(" (")[0]
                    producto = next((p for p in self.productos_disponibles if p.nombre == nombre_producto), None)

            if not producto:
                self.logger.warning(f"No se pudo encontrar el producto: {selection}")
                return

            self.producto_seleccionado = producto

            # Obtener información de stock
            stock_actual = Stock.get_by_product(producto.id)

            # Actualizar información incluyendo stock
            info_text = (f"Nombre: {producto.nombre}\n"
                        f"Referencia: {producto.referencia}\n"
                        f"Precio: {CalculationHelper.format_currency(producto.precio)}\n"
                        f"Categoría: {producto.categoria}\n"
                        f"IVA Recomendado: {CalculationHelper.format_percentage(producto.iva_recomendado)}\n"
                        f"Stock Disponible: {stock_actual} unidades")

            # Agregar advertencia si stock es bajo o cero
            if stock_actual == 0:
                info_text += "\n⚠️ PRODUCTO SIN STOCK"
            elif stock_actual <= 5:
                info_text += f"\n⚠️ STOCK BAJO ({stock_actual} unidades)"

            if producto.descripcion:
                info_text += f"\nDescripción: {producto.descripcion[:100]}..."
            
            self.info_label.configure(text=info_text)
            
            # Establecer valores por defecto
            if self.precio_inicial is None:
                FormHelper.set_entry_value(self.precio_entry, str(producto.precio))
            
            if self.iva_inicial is None:
                FormHelper.set_entry_value(self.iva_entry, str(producto.iva_recomendado))
            
            self.update_preview()
            
        except Exception as e:
            self.logger.error(f"Error al seleccionar producto: {e}")
    
    def load_producto_data(self):
        """Carga los datos del producto seleccionado"""
        if not self.producto_seleccionado:
            return
        
        # Seleccionar en el combo
        producto_text = f"{self.producto_seleccionado.nombre} ({self.producto_seleccionado.referencia}) - {CalculationHelper.format_currency(self.producto_seleccionado.precio)}"
        self.producto_combo.set(producto_text)
        
        # Cargar valores
        FormHelper.set_entry_value(self.precio_entry, str(self.precio_inicial or self.producto_seleccionado.precio))
        FormHelper.set_entry_value(self.iva_entry, str(self.iva_inicial or self.producto_seleccionado.iva_recomendado))
        
        # Actualizar info y preview
        self.on_producto_selected(producto_text)
    
    def update_preview(self, event=None):
        """Actualiza el preview de totales"""
        try:
            cantidad = int(FormHelper.get_entry_value(self.cantidad_entry, "1"))
            precio = float(FormHelper.get_entry_value(self.precio_entry, "0"))
            iva = float(FormHelper.get_entry_value(self.iva_entry, "0"))
            descuento = float(FormHelper.get_entry_value(self.descuento_entry, "0"))
            
            result = CalculationHelper.calculate_line_total(precio, cantidad, iva, descuento)
            
            self.subtotal_preview.configure(text=CalculationHelper.format_currency(result['subtotal']))
            self.descuento_preview.configure(text=CalculationHelper.format_currency(result['descuento_amount']))
            self.iva_preview.configure(text=CalculationHelper.format_currency(result['iva_amount']))
            self.total_preview.configure(text=CalculationHelper.format_currency(result['total']))
            
        except (ValueError, TypeError):
            # Si hay errores en los valores, mostrar ceros
            for label in [self.subtotal_preview, self.descuento_preview, self.iva_preview, self.total_preview]:
                label.configure(text="0.00 €")
    
    def validate_form(self):
        """Valida el formulario incluyendo verificación de stock"""
        errors = []

        if not self.producto_seleccionado:
            errors.append("Debe seleccionar un producto")
            return errors

        # Validar cantidad
        cantidad_str = FormHelper.get_entry_value(self.cantidad_entry)
        error = FormValidator.validate_cantidad(cantidad_str)
        if error:
            errors.append(error)
        else:
            # Validar stock disponible
            try:
                cantidad_solicitada = int(cantidad_str)
                stock_actual = Stock.get_by_product(self.producto_seleccionado.id)

                if cantidad_solicitada > stock_actual:
                    if stock_actual == 0:
                        errors.append(f"El producto '{self.producto_seleccionado.nombre}' no tiene stock disponible")
                    else:
                        errors.append(f"Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad_solicitada}")

            except ValueError:
                pass  # El error de cantidad ya se capturó arriba

        # Validar precio
        precio_str = FormHelper.get_entry_value(self.precio_entry)
        error = FormValidator.validate_precio(precio_str)
        if error:
            errors.append(error)

        # Validar IVA
        iva_str = FormHelper.get_entry_value(self.iva_entry)
        error = FormValidator.validate_iva(iva_str)
        if error:
            errors.append(error)

        # Validar descuento
        descuento_str = FormHelper.get_entry_value(self.descuento_entry, "0")
        if descuento_str:
            try:
                descuento = float(descuento_str)
                if descuento < 0 or descuento > 100:
                    errors.append("El descuento debe estar entre 0 y 100%")
            except ValueError:
                errors.append("El descuento debe ser un número válido")

        return errors
    
    def accept(self):
        """Acepta el diálogo"""
        errors = self.validate_form()
        if errors:
            tk.messagebox.showerror("Error de Validación", "\n".join(errors), parent=self.dialog)
            return
        
        try:
            cantidad = int(FormHelper.get_entry_value(self.cantidad_entry))
            precio = float(FormHelper.get_entry_value(self.precio_entry))
            iva = float(FormHelper.get_entry_value(self.iva_entry))
            descuento = float(FormHelper.get_entry_value(self.descuento_entry, "0"))
            
            self.result = (self.producto_seleccionado.id, cantidad, precio, iva, descuento)
            self._cleanup_bindings()
            self.dialog.destroy()
            
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al procesar datos: {str(e)}", parent=self.dialog)
    
    def cancel(self):
        """Cancela el diálogo"""
        self.result = None
        self._cleanup_bindings()
        self.dialog.destroy()

    def _cleanup_bindings(self):
        """Limpia los bindings globales al cerrar el diálogo"""
        try:
            if hasattr(self, 'dialog') and self.dialog.winfo_exists():
                # Restaurar el manejador original si existía
                if hasattr(self, '_original_mousewheel_handler') and self._original_mousewheel_handler:
                    try:
                        self.dialog.tk.call('bind', 'all', '<MouseWheel>', self._original_mousewheel_handler)
                    except Exception:
                        pass
                else:
                    # Si no había manejador original, limpiar completamente
                    try:
                        self.dialog.tk.call('bind', 'all', '<MouseWheel>', '')
                        self.dialog.tk.call('bind', 'all', '<Button-4>', '')
                        self.dialog.tk.call('bind', 'all', '<Button-5>', '')
                    except Exception:
                        pass

                # Limpiar bindings normales
                try:
                    self.dialog.unbind_all("<MouseWheel>")
                    self.dialog.unbind_all("<Button-4>")
                    self.dialog.unbind_all("<Button-5>")
                except Exception:
                    pass

                self.logger.info("Interceptor de scroll basado en foco removido")

        except (AttributeError, tk.TclError):
            pass

    def bind_mousewheel_to_scrollable(self, widget):
        """Vincula el scroll de la rueda del ratón a un widget scrollable"""
        def _on_mousewheel(event):
            # Interceptar TODOS los eventos de scroll y dirigirlos al frame scrollable
            try:
                if (hasattr(self, 'main_scrollable_frame') and
                    self.main_scrollable_frame is not None and
                    self.main_scrollable_frame.winfo_exists()):

                    # Calcular delta del scroll
                    if hasattr(event, 'delta') and event.delta:
                        delta = -1 * (event.delta / 120)
                    elif hasattr(event, 'num'):
                        if event.num == 4:
                            delta = -1
                        elif event.num == 5:
                            delta = 1
                        else:
                            return "break"  # Importante: break para evitar propagación
                    else:
                        return "break"

                    # Aplicar scroll al frame scrollable principal
                    self.main_scrollable_frame._parent_canvas.yview_scroll(int(delta), "units")
                    return "break"  # Evitar que el evento se propague a la ventana padre

            except (AttributeError, tk.TclError):
                pass

            return "break"  # Siempre evitar propagación

        # Binding más agresivo con return "break"
        widget.bind("<MouseWheel>", _on_mousewheel, "+")
        widget.bind("<Button-4>", _on_mousewheel, "+")
        widget.bind("<Button-5>", _on_mousewheel, "+")

        # También bind a eventos de focus para asegurar captura
        try:
            widget.bind("<FocusIn>", lambda e: self._ensure_scroll_binding(widget), "+")
        except (AttributeError, tk.TclError):
            pass

    def _ensure_scroll_binding(self, widget):
        """Asegura que el binding de scroll esté activo para un widget"""
        try:
            # Re-bind cuando un widget obtiene foco
            self.bind_mousewheel_to_scrollable(widget)
        except (AttributeError, tk.TclError):
            pass

    def configure_mousewheel_scrolling_aggressive(self):
        """Configuración agresiva que intercepta scroll y lo redirige según el foco"""
        try:
            # Interceptar TODOS los eventos de scroll a nivel global
            self._original_mousewheel_handler = None

            # Guardar el manejador original si existe
            try:
                self._original_mousewheel_handler = self.dialog.tk.call('bind', 'all', '<MouseWheel>')
            except:
                pass

            # Instalar nuestro interceptor global
            self.dialog.tk.call('bind', 'all', '<MouseWheel>',
                               self.dialog.register(self._focus_aware_scroll_handler))
            self.dialog.tk.call('bind', 'all', '<Button-4>',
                               self.dialog.register(self._focus_aware_scroll_handler))
            self.dialog.tk.call('bind', 'all', '<Button-5>',
                               self.dialog.register(self._focus_aware_scroll_handler))

            self.logger.info("Interceptor de scroll basado en foco instalado")

        except Exception as e:
            self.logger.error(f"Error en configuración agresiva de scroll: {e}")

    def _focus_aware_scroll_handler(self):
        """Manejador que redirige scroll según el widget que tiene foco"""
        def handler(event):
            try:
                # Obtener el widget que tiene foco actualmente
                focused_widget = self.dialog.focus_get()

                if focused_widget is not None:
                    # Verificar si el widget con foco pertenece a nuestro diálogo
                    if self._widget_belongs_to_dialog(focused_widget):
                        # El foco está en nuestro diálogo, aplicar scroll aquí
                        self._apply_scroll_to_dialog(event)
                        return "break"  # Evitar que llegue a la ventana padre
                    else:
                        # El foco está en otra ventana, dejar que maneje el scroll
                        if self._original_mousewheel_handler:
                            # Llamar al manejador original
                            return self._original_mousewheel_handler
                else:
                    # Sin foco específico, verificar posición del cursor
                    if self._is_cursor_over_dialog():
                        self._apply_scroll_to_dialog(event)
                        return "break"

            except Exception as e:
                self.logger.debug(f"Error en manejador de scroll basado en foco: {e}")
                pass

        return handler

    def _widget_belongs_to_dialog(self, widget):
        """Verifica si un widget pertenece a nuestro diálogo"""
        try:
            if widget is None:
                return False

            # Recorrer la jerarquía de widgets hacia arriba
            current = widget
            while current is not None:
                if current == self.dialog:
                    return True
                try:
                    current = current.master
                except AttributeError:
                    break

            return False

        except Exception:
            return False

    def _is_cursor_over_dialog(self):
        """Verifica si el cursor está sobre el diálogo"""
        try:
            if not hasattr(self, 'dialog') or not self.dialog.winfo_exists():
                return False

            # Obtener posición del cursor
            cursor_x = self.dialog.winfo_pointerx()
            cursor_y = self.dialog.winfo_pointery()

            # Obtener coordenadas del diálogo
            dialog_x = self.dialog.winfo_rootx()
            dialog_y = self.dialog.winfo_rooty()
            dialog_width = self.dialog.winfo_width()
            dialog_height = self.dialog.winfo_height()

            # Verificar si el cursor está dentro
            return (dialog_x <= cursor_x <= dialog_x + dialog_width and
                    dialog_y <= cursor_y <= dialog_y + dialog_height)
        except Exception:
            return False

    def _apply_scroll_to_dialog(self, event):
        """Aplica el scroll al frame scrollable del diálogo"""
        try:
            if (hasattr(self, 'main_scrollable_frame') and
                self.main_scrollable_frame is not None and
                self.main_scrollable_frame.winfo_exists()):

                # Calcular delta del scroll
                if hasattr(event, 'delta') and event.delta:
                    delta = -1 * (event.delta / 120)
                elif hasattr(event, 'num'):
                    if event.num == 4:
                        delta = -1
                    elif event.num == 5:
                        delta = 1
                    else:
                        return
                else:
                    return

                # Aplicar scroll
                self.main_scrollable_frame._parent_canvas.yview_scroll(int(delta), "units")

        except Exception:
            pass

    def _setup_scroll_polling(self):
        """Configura polling para capturar eventos de scroll perdidos"""
        try:
            self._last_cursor_pos = (0, 0)
            self._check_scroll_events()
        except Exception:
            pass

    def _check_scroll_events(self):
        """Verifica eventos de scroll periódicamente"""
        try:
            if hasattr(self, 'dialog') and self.dialog.winfo_exists():
                # Verificar si el cursor está sobre el diálogo
                if self._is_cursor_over_dialog():
                    # Configurar binding temporal más agresivo
                    self.dialog.focus_set()

                # Programar siguiente verificación
                self.dialog.after(100, self._check_scroll_events)
        except Exception:
            pass

    def configure_mousewheel_scrolling(self):
        """Configura el scroll de la rueda del ratón para el diálogo"""
        try:
            # Binding global al diálogo principal con máxima prioridad
            self.dialog.bind_all("<MouseWheel>", self._global_mousewheel_handler, "+")
            self.dialog.bind_all("<Button-4>", self._global_mousewheel_handler, "+")
            self.dialog.bind_all("<Button-5>", self._global_mousewheel_handler, "+")

            # También binding normal para compatibilidad
            self.bind_mousewheel_to_scrollable(self.dialog)

            def bind_to_children(widget):
                try:
                    self.bind_mousewheel_to_scrollable(widget)
                    for child in widget.winfo_children():
                        bind_to_children(child)
                except (AttributeError, tk.TclError):
                    pass

            bind_to_children(self.dialog)

        except Exception as e:
            self.logger.error(f"Error al configurar scroll de rueda del ratón en diálogo: {e}")

    def _global_mousewheel_handler(self, event):
        """Manejador global de eventos de rueda del ratón"""
        try:
            # Solo procesar si el evento está dentro de nuestro diálogo
            if (hasattr(self, 'dialog') and self.dialog.winfo_exists() and
                self._is_event_in_dialog(event)):

                if (hasattr(self, 'main_scrollable_frame') and
                    self.main_scrollable_frame is not None and
                    self.main_scrollable_frame.winfo_exists()):

                    # Calcular delta del scroll
                    if hasattr(event, 'delta') and event.delta:
                        delta = -1 * (event.delta / 120)
                    elif hasattr(event, 'num'):
                        if event.num == 4:
                            delta = -1
                        elif event.num == 5:
                            delta = 1
                        else:
                            return
                    else:
                        return

                    # Aplicar scroll al frame scrollable principal
                    self.main_scrollable_frame._parent_canvas.yview_scroll(int(delta), "units")
                    return "break"  # Evitar propagación

        except (AttributeError, tk.TclError):
            pass

    def _is_event_in_dialog(self, event):
        """Verifica si un evento ocurrió dentro del diálogo"""
        try:
            if not hasattr(self, 'dialog') or not self.dialog.winfo_exists():
                return False

            # Obtener coordenadas del diálogo
            dialog_x = self.dialog.winfo_rootx()
            dialog_y = self.dialog.winfo_rooty()
            dialog_width = self.dialog.winfo_width()
            dialog_height = self.dialog.winfo_height()

            # Obtener coordenadas del evento
            event_x = event.x_root
            event_y = event.y_root

            # Verificar si el evento está dentro del diálogo
            return (dialog_x <= event_x <= dialog_x + dialog_width and
                    dialog_y <= event_y <= dialog_y + dialog_height)

        except (AttributeError, tk.TclError):
            return False
    
    def show(self):
        """Muestra el diálogo y retorna el resultado"""
        self.dialog.wait_window()
        return self.result

    def refresh_stock_info(self):
        """Actualiza la información de stock en el combo de productos"""
        try:
            # Guardar selección actual
            current_selection = self.producto_combo.get()

            # Regenerar lista de productos con stock actualizado
            productos_names = []
            for p in self.productos_disponibles:
                stock_actual = Stock.get_by_product(p.id)
                stock_info = f"Stock: {stock_actual}"
                if stock_actual == 0:
                    stock_info = "🔴 Sin Stock"
                elif stock_actual <= 5:
                    stock_info = f"🟠 Stock Bajo: {stock_actual}"
                elif stock_actual <= 10:
                    stock_info = f"🟡 Stock: {stock_actual}"
                else:
                    stock_info = f"🟢 Stock: {stock_actual}"

                producto_text = f"{p.nombre} ({p.referencia}) - {CalculationHelper.format_currency(p.precio)} - {stock_info}"
                productos_names.append(producto_text)

            # Actualizar combo
            self.producto_combo.configure(values=productos_names)

            # Restaurar selección si es posible
            if current_selection:
                try:
                    # Buscar la selección actual en la nueva lista
                    nombre_producto = current_selection.split(" (")[0]
                    nueva_seleccion = next((p for p in productos_names if p.startswith(nombre_producto)), None)
                    if nueva_seleccion:
                        self.producto_combo.set(nueva_seleccion)
                        self.on_producto_selected(nueva_seleccion)
                except:
                    pass

            self.logger.info("Información de stock actualizada en diálogo de productos")

        except Exception as e:
            self.logger.error(f"Error actualizando información de stock: {e}")
