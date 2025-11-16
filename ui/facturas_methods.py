# -*- coding: utf-8 -*-
"""
Métodos adicionales para la gestión de facturas
"""
# Import adapté pour PyQt6
from gui import set_gui_framework
set_gui_framework('pyqt6')

# Utiliser l'adaptateur CustomTkinter vers PyQt6
try:
    import customtkinter as ctk
except ImportError:
    # Si CustomTkinter n'est pas disponible, utiliser l'adaptateur
    from gui.customtkinter_to_pyqt6_adapter import create_customtkinter_adapter
    ctk = create_customtkinter_adapter()
import tkinter as tk
from tkinter import messagebox, simpledialog
from common.custom_dialogs import (
    show_copyable_confirm, show_copyable_error,
    show_copyable_info, show_copyable_warning,
    show_copyable_success, show_stock_confirmation_dialog
)
from utils.pdf_generator import PDFGenerator
from utils.translations import get_text
from utils.logger import log_user_action, log_database_operation, log_exception
from utils.factura_numbering import factura_numbering_service
from utils.image_utils import ImageUtils
from database.models import Producto, Stock, Factura
from common.validators import FormValidator, CalculationHelper
from common.ui_components import FormHelper
from common.custom_dialogs import show_copyable_confirm, show_copyable_error
from ui.producto_factura_dialog import ProductoFacturaDialog

class FacturasMethodsMixin:
    """Mixin con métodos adicionales para la gestión de facturas"""

    def initialize_numero_factura(self):
        """Inicializa el número de factura con el siguiente número sugerido"""
        try:
            siguiente_numero = factura_numbering_service.get_next_numero_factura()
            FormHelper.set_entry_value(self.numero_entry, siguiente_numero)
            log_user_action("Número de factura inicializado", f"Número: {siguiente_numero}")
        except Exception as e:
            log_exception(e, "initialize_numero_factura")
    
    def validate_factura_form(self):
        """Valida los datos del formulario de factura"""
        errors = []
        
        # Validar número de factura
        numero = FormHelper.get_entry_value(self.numero_entry)
        error = FormValidator.validate_required_field(numero, get_text("numero_factura"))
        if error:
            errors.append(error)
        else:
            # Validar que el número no esté duplicado
            is_valid, validation_message = factura_numbering_service.validate_numero_factura(numero)
            if not is_valid:
                errors.append(validation_message)
        
        # Validar fecha
        fecha = FormHelper.get_entry_value(self.fecha_entry)
        error = FormValidator.validate_required_field(fecha, get_text("fecha_factura"))
        if error:
            errors.append(error)
        
        # Validar nombre del cliente
        nombre_cliente = FormHelper.get_entry_value(self.nombre_cliente_entry)
        error = FormValidator.validate_required_field(nombre_cliente, get_text("nombre_cliente"))
        if error:
            errors.append(error)
        
        # Validar DNI/NIE (opcional)
        dni_nie = FormHelper.get_entry_value(self.dni_nie_entry)
        if dni_nie:
            error = FormValidator.validate_dni_nie(dni_nie)
            if error:
                errors.append(error)
        
        # Validar email (opcional)
        email = FormHelper.get_entry_value(self.email_cliente_entry)
        if email:
            error = FormValidator.validate_email(email)
            if error:
                errors.append(error)
        
        # Validar teléfono (opcional)
        telefono = FormHelper.get_entry_value(self.telefono_cliente_entry)
        if telefono:
            error = FormValidator.validate_phone(telefono)
            if error:
                errors.append(error)
        
        # Validar que hay al menos un producto
        if not self.factura_items:
            errors.append("Debe agregar al menos un producto a la factura")
        else:
            # Validar stock disponible para cada producto
            stock_errors = self.validate_stock_availability()
            errors.extend(stock_errors)

        return errors

    def validate_stock_availability(self):
        """Valida que hay stock suficiente para todos los productos de la factura"""
        errors = []

        try:
            for item in self.factura_items:
                # Obtener producto y stock actual
                producto = item.get_producto()
                if not producto:
                    continue

                stock_actual = Stock.get_by_product(item.producto_id)

                if item.cantidad > stock_actual:
                    if stock_actual == 0:
                        errors.append(f"❌ '{producto.nombre}': Sin stock disponible")
                    else:
                        errors.append(f"❌ '{producto.nombre}': Stock insuficiente (Disponible: {stock_actual}, Necesario: {item.cantidad})")
                elif stock_actual <= 5 and stock_actual > 0:
                    # Advertencia para stock bajo (no error, solo información)
                    self.logger.warning(f"Stock bajo para producto {producto.nombre}: {stock_actual} unidades")

        except Exception as e:
            self.logger.error(f"Error validando stock: {e}")
            errors.append("Error al verificar disponibilidad de stock")

        return errors

    def show_stock_confirmation_dialog_direct(self, title, message):
        """Muestra diálogo de confirmación de stock con botones CONFIRMAR/CANCELAR"""
        try:
            # Crear diálogo personalizado directamente
            dialog = ctk.CTkToplevel()
            dialog.title(title)
            dialog.geometry("600x400")

            # Hacer que esté siempre encima
            dialog.attributes('-topmost', True)
            dialog.lift()
            dialog.focus_force()

            # Variable para el resultado
            result = None

            # Frame principal
            main_frame = ctk.CTkFrame(dialog)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Título con icono
            title_frame = ctk.CTkFrame(main_frame)
            title_frame.pack(fill="x", pady=(0, 15))

            title_label = ctk.CTkLabel(
                title_frame,
                text=f"📦 {title}",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            title_label.pack(pady=10)

            # Área de texto
            text_widget = ctk.CTkTextbox(
                main_frame,
                height=200,
                font=ctk.CTkFont(size=11, family="Consolas")
            )
            text_widget.pack(fill="both", expand=True, pady=(0, 15))
            text_widget.insert("1.0", message)
            text_widget.configure(state="disabled")

            # Frame de botones
            buttons_frame = ctk.CTkFrame(main_frame)
            buttons_frame.pack(fill="x")

            def confirmar_clicked():
                nonlocal result
                result = True
                dialog.destroy()

            def cancelar_clicked():
                nonlocal result
                result = False
                dialog.destroy()

            def copiar_clicked():
                try:
                    dialog.clipboard_clear()
                    dialog.clipboard_append(message)
                    dialog.update()
                except:
                    pass

            # Botón Copiar (izquierda)
            copiar_btn = ctk.CTkButton(
                buttons_frame,
                text="📋 Copiar",
                command=copiar_clicked,
                width=100,
                height=35,
                fg_color="gray",
                hover_color="darkgray"
            )
            copiar_btn.pack(side="left", padx=15, pady=15)

            # Botón CANCELAR (derecha)
            cancelar_btn = ctk.CTkButton(
                buttons_frame,
                text="❌ CANCELAR",
                command=cancelar_clicked,
                width=140,
                height=40,
                fg_color="#DC143C",
                hover_color="#B22222",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            cancelar_btn.pack(side="right", padx=(5, 15), pady=15)

            # Botón CONFIRMAR (derecha)
            confirmar_btn = ctk.CTkButton(
                buttons_frame,
                text="✅ CONFIRMAR",
                command=confirmar_clicked,
                width=140,
                height=40,
                fg_color="#2E8B57",
                hover_color="#228B22",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            confirmar_btn.pack(side="right", padx=5, pady=15)

            # Focus en CONFIRMAR
            confirmar_btn.focus()

            # Bind teclas
            dialog.bind("<Return>", lambda e: confirmar_clicked())
            dialog.bind("<Escape>", lambda e: cancelar_clicked())

            # Centrar el diálogo
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (400 // 2)
            dialog.geometry(f"600x400+{x}+{y}")

            # Esperar resultado
            dialog.wait_window()

            return result

        except Exception as e:
            self.logger.error(f"Error creando diálogo directo: {e}")
            return None

    def show_simple_confirmation_dialog(self, message):
        """Diálogo de confirmación simple usando tkinter estándar"""
        try:
            import tkinter as tk
            from tkinter import messagebox

            # Crear ventana temporal para el messagebox
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal
            root.attributes('-topmost', True)

            # Mostrar diálogo con botones personalizados
            result = show_copyable_confirm(
                root,
                "Confirmar Procesamiento de Factura",
                f"{message}\n\n¿Desea continuar y procesar la factura?\n\n"
                f"• SÍ = Confirmar y procesar\n"
                f"• NO = Cancelar operación"
            )

            root.destroy()

            self.logger.info(f"🔧 DEBUG: Resultado diálogo simple: {result}")
            return result

        except Exception as e:
            self.logger.error(f"Error con diálogo simple: {e}")
            # Último recurso: preguntar por consola
            print(f"\n📦 CONFIRMACIÓN DE STOCK:")
            print(message)
            print(f"\n¿Desea continuar y procesar la factura? (s/n): ", end="")
            try:
                response = input().lower().strip()
                return response in ['s', 'si', 'sí', 'y', 'yes']
            except:
                return False

    def show_stock_impact_summary(self):
        """Muestra un resumen del impacto en stock antes de guardar la factura"""
        try:
            if not self.factura_items:
                return True

            # Crear mensaje de resumen
            summary_lines = ["📦 IMPACTO EN STOCK:\n"]

            for item in self.factura_items:
                producto = item.get_producto()
                if not producto:
                    continue

                stock_actual = Stock.get_by_product(item.producto_id)
                stock_despues = max(0, stock_actual - item.cantidad)

                # Determinar estado del stock después
                if stock_despues == 0:
                    estado = "🔴 SIN STOCK"
                elif stock_despues <= 5:
                    estado = f"🟠 STOCK BAJO ({stock_despues})"
                elif stock_despues <= 10:
                    estado = f"🟡 STOCK MEDIO ({stock_despues})"
                else:
                    estado = f"🟢 STOCK OK ({stock_despues})"

                summary_lines.append(
                    f"• {producto.nombre}:\n"
                    f"  Stock actual: {stock_actual} → Después: {stock_despues} unidades\n"
                    f"  Estado: {estado}\n"
                )

            summary_lines.append("\n" + "="*50)
            summary_lines.append("🔄 ACCIÓN A REALIZAR:")
            summary_lines.append("• Se guardará la factura")
            summary_lines.append("• Se actualizará automáticamente el stock")
            summary_lines.append("• Se registrarán los movimientos de stock")
            summary_lines.append("\n¿Desea continuar y procesar la factura?")
            summary_message = "\n".join(summary_lines)

            # Mostrar diálogo específico de confirmación de stock
            self.logger.info("🔧 DEBUG: Usando diálogo directo con botones CONFIRMAR/CANCELAR...")
            try:
                result = self.show_stock_confirmation_dialog_direct("Confirmar Procesamiento de Factura", summary_message)
                self.logger.info(f"🔧 DEBUG: Resultado del diálogo directo: {result}")

                # Si el resultado es None, significa que hubo un error
                if result is None:
                    self.logger.warning("🔧 DEBUG: Diálogo directo retornó None, usando fallback...")
                    return self.show_simple_confirmation_dialog(summary_message)

                return result
            except Exception as e:
                self.logger.error(f"🔧 DEBUG: Error con diálogo directo: {e}")
                import traceback
                self.logger.error(f"🔧 DEBUG: Traceback: {traceback.format_exc()}")

                # Fallback con diálogo simple
                self.logger.info("🔧 DEBUG: Usando fallback diálogo simple...")
                return self.show_simple_confirmation_dialog(summary_message)

        except Exception as e:
            self.logger.error(f"Error mostrando resumen de stock: {e}")
            return True  # En caso de error, permitir continuar
    
    def agregar_producto(self):
        """Abre el diálogo para agregar un producto a la factura"""
        try:
            if not self.productos_disponibles:
                self._show_message("warning", "Advertencia", 
                                 "No hay productos disponibles. Agregue productos primero.")
                return
            
            dialog = ProductoFacturaDialog(self.window, self.productos_disponibles)
            result = dialog.show()
            
            if result:
                producto_id, cantidad, precio_unitario, iva_aplicado, descuento = result
                
                # Verificar stock disponible
                stock_disponible = Stock.get_by_product(producto_id)
                if stock_disponible < cantidad:
                    if not show_copyable_confirm(self.window, "Stock Insuficiente",
                                               f"⚠️ Stock insuficiente detectado:\n\n"
                                               f"📦 Stock disponible: {stock_disponible}\n"
                                               f"📋 Cantidad solicitada: {cantidad}\n"
                                               f"❌ Faltante: {cantidad - stock_disponible}\n\n"
                                               "¿Desea continuar de todos modos?\n\n"
                                               "💡 Nota: Esto puede generar stock negativo."):
                        return
                
                # Crear item de factura
                from database.models import FacturaItem
                item = FacturaItem(
                    producto_id=producto_id,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    iva_aplicado=iva_aplicado,
                    descuento=descuento
                )
                item.calculate_totals()
                
                self.factura_items.append(item)
                self.update_productos_tree()
                self.update_totales()
                
                log_user_action("Producto agregado a factura", 
                              f"Producto ID: {producto_id}, Cantidad: {cantidad}")
                
        except Exception as e:
            log_exception(e, "agregar_producto")
            self._show_message("error", get_text("error"), f"Error al agregar producto: {str(e)}")
    
    def editar_producto_factura(self):
        """Edita un producto de la factura"""
        try:
            selected_index = self.productos_tree.get_selected_index()
            if selected_index is None:
                self._show_message("warning", "Advertencia", "Seleccione un producto para editar")
                return

            item = self.factura_items[selected_index]
            
            # Buscar el producto
            producto = next((p for p in self.productos_disponibles if p.id == item.producto_id), None)
            if not producto:
                self._show_message("error", "Error", "Producto no encontrado")
                return
            
            dialog = ProductoFacturaDialog(self.window, self.productos_disponibles, 
                                         producto_seleccionado=producto,
                                         cantidad_inicial=item.cantidad,
                                         precio_inicial=item.precio_unitario,
                                         iva_inicial=item.iva_aplicado,
                                         descuento_inicial=item.descuento)
            result = dialog.show()
            
            if result:
                producto_id, cantidad, precio_unitario, iva_aplicado, descuento = result
                
                # Actualizar item
                item.producto_id = producto_id
                item.cantidad = cantidad
                item.precio_unitario = precio_unitario
                item.iva_aplicado = iva_aplicado
                item.descuento = descuento
                item.calculate_totals()
                
                self.update_productos_tree()
                self.update_totales()
                
                log_user_action("Producto editado en factura", f"Producto ID: {producto_id}")
                
        except Exception as e:
            log_exception(e, "editar_producto_factura")
            self._show_message("error", get_text("error"), f"Error al editar producto: {str(e)}")
    
    def eliminar_producto_factura(self):
        """Elimina un producto de la factura"""
        try:
            selected_index = self.productos_tree.get_selected_index()
            if selected_index is None:
                self._show_message("warning", "Advertencia", "Seleccione un producto para eliminar")
                return

            if self._show_message("yesno", "Confirmar", "¿Eliminar este producto de la factura?"):
                removed_item = self.factura_items.pop(selected_index)

                self.update_productos_tree()
                self.update_totales()

                log_user_action("Producto eliminado de factura",
                              f"Producto ID: {removed_item.producto_id}")

        except Exception as e:
            log_exception(e, "eliminar_producto_factura")
            self._show_message("error", get_text("error"), f"Error al eliminar producto: {str(e)}")
    
    def update_productos_tree(self):
        """Actualiza la lista de productos en la factura con mini imágenes"""
        try:
            # Utiliser le nouveau widget personnalisé
            self.productos_tree.update_items(self.factura_items)

        except Exception as e:
            log_exception(e, "update_productos_tree")

    def on_producto_selected(self, index):
        """Callback appelé quand un produit est sélectionné dans la liste"""
        try:
            if 0 <= index < len(self.factura_items):
                self.selected_item_index = index
                log_user_action("Producto seleccionado en factura", f"Index: {index}")
        except Exception as e:
            log_exception(e, "on_producto_selected")
    
    def update_totales(self):
        """Actualiza los totales de la factura"""
        try:
            subtotal = sum(item.subtotal for item in self.factura_items)
            total_iva = sum(item.iva_amount for item in self.factura_items)
            total_factura = subtotal + total_iva
            
            self.subtotal_label.configure(text=CalculationHelper.format_currency(subtotal))
            self.total_iva_label.configure(text=CalculationHelper.format_currency(total_iva))
            self.total_factura_label.configure(text=CalculationHelper.format_currency(total_factura))
            
        except Exception as e:
            log_exception(e, "update_totales")
    
    def guardar_factura(self):
        """Guarda la factura en la base de datos"""
        try:
            # Validar formulario
            errors = self.validate_factura_form()
            if errors:
                error_message = "\n".join(errors)
                try:
                    show_copyable_error(self.window, get_text("error"), error_message)
                except Exception as e:
                    self.logger.error(f"Error mostrando errores de validación: {e}")
                    # Fallback con messagebox estándar
                    self._show_message("error", get_text("error"), error_message)
                return

            # Mostrar resumen de impacto en stock antes de guardar
            self.logger.info("🔧 DEBUG: Mostrando resumen de impacto en stock...")
            stock_summary_result = self.show_stock_impact_summary()
            self.logger.info(f"🔧 DEBUG: Resultado del resumen de stock: {stock_summary_result}")

            if not stock_summary_result:
                self.logger.info("🔧 DEBUG: Usuario CANCELÓ el diálogo de confirmación de stock")
                return  # Usuario canceló

            self.logger.info("🔧 DEBUG: Usuario CONFIRMÓ continuar con la factura")
            
            # Crear o actualizar factura
            if not self.current_factura:
                self.current_factura = Factura()

            # Gestionar cliente (añadir automáticamente si es nuevo)
            cliente_id = self.auto_add_cliente_if_new()

            # Asignar datos básicos
            self.current_factura.numero_factura = FormHelper.get_entry_value(self.numero_entry)
            self.current_factura.fecha_factura = FormHelper.get_entry_value(self.fecha_entry)
            self.current_factura.cliente_id = cliente_id
            self.current_factura.nombre_cliente = FormHelper.get_entry_value(self.nombre_cliente_entry)
            self.current_factura.dni_nie_cliente = FormHelper.get_entry_value(self.dni_nie_entry)
            self.current_factura.direccion_cliente = FormHelper.get_text_value(self.direccion_cliente_text)
            self.current_factura.email_cliente = FormHelper.get_entry_value(self.email_cliente_entry)
            self.current_factura.telefono_cliente = FormHelper.get_entry_value(self.telefono_cliente_entry)
            self.current_factura.modo_pago = self.modo_pago_var.get()
            
            # Asignar items
            self.current_factura.items = self.factura_items.copy()
            
            # Calcular totales
            self.current_factura.calculate_totals()
            
            # Guardar en base de datos
            self.logger.info(f"💾 Guardando factura {self.current_factura.numero_factura} en base de datos...")
            self.current_factura.save()
            self.logger.info(f"✅ Factura guardada con ID: {self.current_factura.id}")

            # Actualizar stock
            self.logger.info(f"📊 Iniciando actualización de stock para factura {self.current_factura.numero_factura}...")
            self.update_stock_after_save()
            self.logger.info(f"✅ Actualización de stock completada")

            # Actualizar servicio de numeración
            factura_numbering_service.update_next_numero_after_save(self.current_factura.numero_factura)

            # Actualizar lista
            self.load_facturas()

            # Limpiar formulario y preparar siguiente factura
            self.nueva_factura()

            self._show_message("info", "Éxito", get_text("factura_generada"))

            log_database_operation("INSERT/UPDATE", "facturas",
                                 f"Factura {self.current_factura.numero_factura}")
            log_user_action("Factura guardada",
                          f"Número: {self.current_factura.numero_factura}")
            
        except Exception as e:
            log_exception(e, "guardar_factura")
            self._show_message("error", get_text("error"), f"Error al guardar factura: {str(e)}")
    
    def update_stock_after_save(self):
        """Actualiza el stock después de guardar la factura"""
        try:
            self.logger.info(f"🔄 INICIANDO actualización de stock para factura {self.current_factura.numero_factura}")
            self.logger.info(f"📦 Número de items a procesar: {len(self.factura_items)}")

            if not self.factura_items:
                self.logger.warning("⚠️ No hay items en la factura para actualizar stock")
                return

            for i, item in enumerate(self.factura_items, 1):
                self.logger.info(f"📊 Procesando item {i}/{len(self.factura_items)}")
                self.logger.info(f"   - Producto ID: {item.producto_id}")
                self.logger.info(f"   - Cantidad a descontar: {item.cantidad}")

                # Obtener stock antes de la actualización
                stock_antes = Stock.get_by_product(item.producto_id)
                self.logger.info(f"   - Stock antes: {stock_antes}")

                # Usar el método mejorado que registra movimientos automáticamente
                Stock.update_stock(item.producto_id, item.cantidad)

                # Verificar stock después de la actualización
                stock_despues = Stock.get_by_product(item.producto_id)
                self.logger.info(f"   - Stock después: {stock_despues}")

                # Verificar que la actualización fue correcta
                stock_esperado = max(0, stock_antes - item.cantidad)
                if stock_despues == stock_esperado:
                    self.logger.info(f"   ✅ Stock actualizado correctamente")
                else:
                    self.logger.error(f"   ❌ Error en actualización: esperado {stock_esperado}, obtenido {stock_despues}")

                # Obtener información del producto para el log
                producto = item.get_producto()
                producto_nombre = producto.nombre if producto else f"ID:{item.producto_id}"

                log_database_operation("UPDATE", "stock",
                                     f"Producto {producto_nombre}: {stock_antes}→{stock_despues} (Factura: {self.current_factura.numero_factura})")

                self.logger.info(f"Stock actualizado para producto {producto_nombre}: -{item.cantidad} unidades ({stock_antes}→{stock_despues})")

            self.logger.info(f"✅ COMPLETADA actualización de stock para factura {self.current_factura.numero_factura}")

        except Exception as e:
            log_exception(e, "update_stock_after_save")
            # Mostrar error al usuario para que sea visible
            self.logger.error(f"❌ Error actualizando stock después de guardar factura: {e}")
            self._show_message("error", "Error de Stock",
                             f"Error al actualizar stock después de guardar factura:\n{str(e)}\n\n"
                             f"La factura se guardó correctamente, pero el stock no se actualizó.")
            # Re-lanzar la excepción para debugging
            raise
    
    def eliminar_factura(self):
        """Elimina la factura seleccionada"""
        try:
            if not self.selected_factura:
                self._show_message("warning", "Advertencia", "Seleccione una factura para eliminar")
                return
            
            if self._show_message("yesno", "Confirmar", 
                                f"¿Eliminar la factura {self.selected_factura.numero_factura}?"):
                
                self.selected_factura.delete()
                self.load_facturas()
                self.limpiar_formulario()
                
                self._show_message("info", "Éxito", "Factura eliminada correctamente")
                
                log_database_operation("DELETE", "facturas", 
                                     f"Factura {self.selected_factura.numero_factura}")
                log_user_action("Factura eliminada", 
                              f"Número: {self.selected_factura.numero_factura}")
                
        except Exception as e:
            log_exception(e, "eliminar_factura")
            self._show_message("error", get_text("error"), f"Error al eliminar factura: {str(e)}")
    
    # Nota: La función editar_factura se ha eliminado porque la edición
    # se activa automáticamente al seleccionar una factura en la lista

    def exportar_pdf(self):
        """Exporta la factura seleccionada a PDF"""
        try:
            self.logger.info(f"🔍 DEBUG PDF: selected_factura = {self.selected_factura}")
            self.logger.info(f"🔍 DEBUG PDF: hasattr selected_factura = {hasattr(self, 'selected_factura')}")

            if not self.selected_factura:
                mensaje_seleccion = """⚠️ Seleccione una factura para exportar

Para exportar una factura a PDF, debe seguir estos pasos:

1. **Seleccionar una factura:**
   - En la lista de facturas (lado izquierdo)
   - Haga clic en la factura que desea exportar
   - La factura se cargará automáticamente en el formulario

2. **Exportar a PDF:**
   - Una vez seleccionada la factura
   - Haga clic en el botón "Exportar PDF"
   - Se mostrará la información de desarrollo

Estado actual:
- Facturas disponibles: {len(self.facturas)} facturas en la lista
- Factura seleccionada: Ninguna
- Acción requerida: Seleccionar una factura de la lista

Instrucciones adicionales:
✅ Las facturas aparecen en la lista del lado izquierdo
✅ Haga clic en una fila para seleccionar la factura
✅ El formulario se actualizará automáticamente
✅ Luego podrá usar "Exportar PDF"

Nota: La funcionalidad de PDF está en desarrollo, pero primero debe seleccionar una factura para ver los detalles del desarrollo.

Este mensaje puede ser copiado para referencia."""

                show_copyable_warning(self.window, "Advertencia - Seleccionar Factura", mensaje_seleccion)
                return

            # Generar PDF usando el nuevo generador
            try:
                pdf_generator = PDFGenerator()
                pdf_path = pdf_generator.generar_factura_pdf(self.selected_factura, auto_open=True)

                # Mensaje de éxito con detalles
                mensaje_exito = f"""✅ PDF generado exitosamente

La factura ha sido exportada a PDF correctamente.

Detalles de la factura:
- Número de factura: {self.selected_factura.numero_factura}
- Cliente: {self.selected_factura.nombre_cliente}
- Fecha: {self.selected_factura.fecha_factura}
- Total: {self.selected_factura.total_factura:.2f}€
- Productos: {len(self.selected_factura.items)} items

Archivo generado:
- Ubicación: {pdf_path}
- Tamaño: {self.get_file_size(pdf_path)}
- Formato: PDF (A4)
- Generado: {self.get_current_timestamp()}

Características incluidas:
✅ Diseño profesional de factura
✅ Información completa de empresa
✅ Datos detallados del cliente
✅ Tabla de productos con precios
✅ Cálculos de IVA desglosados
✅ Totales destacados
✅ Observaciones y pie de página

Acciones disponibles:
- El archivo se ha guardado automáticamente
- Puedes abrirlo desde el explorador de archivos
- Está listo para imprimir o enviar por email

Este mensaje puede ser copiado para referencia."""

                show_copyable_success(self.window, "PDF Generado Exitosamente", mensaje_exito)

                # El PDF ya se abre automáticamente desde el generador

            except ImportError as e:
                # Error de dependencia ReportLab
                mensaje_dependencia = f"""❌ Error: Dependencia ReportLab no encontrada

Para generar PDFs, es necesario instalar la librería ReportLab.

Detalles del error:
- Error: {str(e)}
- Módulo faltante: ReportLab
- Función: exportar_pdf()
- Timestamp: {self.get_current_timestamp()}

Solución:
1. Instalar ReportLab:
   pip install reportlab

2. O desde el directorio del proyecto:
   pip install -r requirements.txt

3. Reiniciar la aplicación

Información técnica:
- ReportLab es necesario para la generación de PDF
- Versión requerida: 4.0.9 o superior
- Alternativa: Usar exportación de datos a Excel

Una vez instalado ReportLab:
✅ Podrás generar PDFs profesionales
✅ Formato automático de facturas
✅ Diseño personalizable
✅ Integración completa con los datos

Copie este mensaje para instalar la dependencia."""

                show_copyable_error(self.window, "Error - Dependencia Faltante", mensaje_dependencia)

            except Exception as e:
                # Otros errores de generación
                mensaje_error_pdf = f"""❌ Error generando PDF

Se produjo un error durante la generación del PDF.

Detalles del error:
- Factura: {self.selected_factura.numero_factura}
- Cliente: {self.selected_factura.nombre_cliente}
- Error: {str(e)}
- Tipo: {type(e).__name__}
- Función: exportar_pdf()
- Timestamp: {self.get_current_timestamp()}

Información de la factura:
- Items: {len(self.selected_factura.items)} productos
- Total: {self.selected_factura.total_factura:.2f}€
- Estado: Guardada en base de datos

Posibles causas:
- Permisos de escritura en directorio
- Espacio insuficiente en disco
- Caracteres especiales en nombres
- Datos corruptos en la factura

Acciones recomendadas:
1. Verificar permisos de escritura
2. Comprobar espacio en disco
3. Intentar con otra factura
4. Contactar soporte técnico

Los datos de la factura están seguros en la base de datos.
Copie este mensaje para soporte técnico."""

                show_copyable_error(self.window, "Error Generando PDF", mensaje_error_pdf)

        except Exception as e:
            log_exception(e, "exportar_pdf")
            error_message = f"""❌ Error al exportar PDF

Se produjo un error al intentar exportar la factura a PDF.

Detalles del error:
- Factura: {self.selected_factura.numero_factura if self.selected_factura else 'N/A'}
- Función: exportar_pdf()
- Error: {str(e)}
- Módulo: ui.facturas_methods
- Timestamp: {self.get_current_timestamp()}

Información técnica:
- Tipo de error: {type(e).__name__}
- Descripción: {str(e)}

Nota: La funcionalidad de PDF está en desarrollo.
Si el error persiste, copie este mensaje para soporte técnico."""

            show_copyable_error(self.window, get_text("error"), error_message)
    
    def generar_pdf(self):
        """Genera PDF de la factura actual"""
        try:
            if not self.current_factura or not self.current_factura.id:
                show_copyable_warning(self.window, "Advertencia",
                                    "Guarde la factura antes de generar el PDF.\n\n"
                                    "Para generar un PDF:\n"
                                    "1. Complete todos los datos de la factura\n"
                                    "2. Agregue al menos un producto\n"
                                    "3. Haga clic en 'Guardar'\n"
                                    "4. Luego podrá generar el PDF")
                return

            # Generar PDF de la factura actual
            try:
                pdf_generator = PDFGenerator()
                pdf_path = pdf_generator.generar_factura_pdf(self.current_factura, auto_open=True)

                # Mensaje de éxito detallado
                mensaje_exito = f"""✅ PDF de factura generado exitosamente

La factura actual ha sido convertida a PDF correctamente.

Detalles de la factura generada:
- Número de factura: {self.current_factura.numero_factura}
- Cliente: {self.current_factura.nombre_cliente}
- DNI/NIE: {self.current_factura.dni_nie_cliente or 'N/A'}
- Fecha: {self.current_factura.fecha_factura}
- Productos: {len(self.current_factura.items)} items
- Subtotal: {self.current_factura.subtotal:.2f}€
- IVA: {self.current_factura.total_iva:.2f}€
- Total: {self.current_factura.total_factura:.2f}€

Archivo PDF generado:
- Ubicación: {pdf_path}
- Tamaño: {self.get_file_size(pdf_path)}
- Formato: A4, profesional
- Generado: {self.get_current_timestamp()}

Contenido incluido:
✅ Encabezado con datos de empresa
✅ Información completa del cliente
✅ Tabla detallada de productos
✅ Cálculos de IVA por item
✅ Totales destacados y claros
✅ Pie de página con observaciones
✅ Diseño profesional y limpio

Acciones realizadas:
- PDF guardado automáticamente
- Formato optimizado para impresión
- Listo para envío por email
- Compatible con todos los lectores PDF

Próximos pasos:
- El archivo está disponible para usar
- Puedes imprimirlo directamente
- Enviarlo por email al cliente
- Archivarlo para tus registros

Este mensaje puede ser copiado para documentación."""

                show_copyable_success(self.window, "PDF Generado - Factura Actual", mensaje_exito)

                # El PDF ya se abre automáticamente desde el generador

            except ImportError as e:
                # Error de dependencia
                mensaje_dependencia = f"""❌ Error: ReportLab no instalado

Para generar PDFs de facturas, necesitas instalar ReportLab.

Detalles del error:
- Factura: {self.current_factura.numero_factura}
- Error: {str(e)}
- Módulo faltante: ReportLab
- Función: generar_pdf()
- Timestamp: {self.get_current_timestamp()}

Instalación requerida:
1. Opción 1 - Instalar directamente:
   pip install reportlab==4.0.9

2. Opción 2 - Desde requirements.txt:
   pip install -r requirements.txt

3. Reiniciar la aplicación

Información de la factura:
- La factura está guardada correctamente
- Todos los datos están disponibles
- Solo falta la librería para PDF

Una vez instalado ReportLab:
✅ Generación automática de PDF
✅ Diseño profesional incluido
✅ Todos los datos integrados
✅ Formato listo para imprimir

Alternativas mientras tanto:
- Exportar datos a Excel
- Usar la vista de factura en pantalla
- Copiar información manualmente

Copie este mensaje para instalar la dependencia."""

                show_copyable_error(self.window, "Error - ReportLab No Instalado", mensaje_dependencia)

            except Exception as e:
                # Otros errores
                mensaje_error = f"""❌ Error generando PDF de factura actual

Se produjo un error durante la generación del PDF.

Detalles del error:
- Factura: {self.current_factura.numero_factura}
- Cliente: {self.current_factura.nombre_cliente}
- Error: {str(e)}
- Tipo: {type(e).__name__}
- Función: generar_pdf()
- Timestamp: {self.get_current_timestamp()}

Estado de la factura:
- Número: {self.current_factura.numero_factura}
- Items: {len(self.current_factura.items)} productos
- Total: {self.current_factura.total_factura:.2f}€
- Estado: Guardada correctamente

Diagnóstico:
- Los datos de la factura están íntegros
- El error ocurrió durante la generación PDF
- La factura sigue disponible en el sistema

Posibles causas:
- Permisos de escritura insuficientes
- Espacio en disco insuficiente
- Caracteres especiales en datos
- Problema temporal del sistema

Acciones recomendadas:
1. Verificar espacio en disco
2. Comprobar permisos de escritura
3. Intentar generar PDF de otra factura
4. Reiniciar la aplicación si persiste
5. Contactar soporte técnico

La factura está segura en la base de datos.
Copie este mensaje para soporte técnico."""

                show_copyable_error(self.window, "Error Generando PDF", mensaje_error)

        except Exception as e:
            log_exception(e, "generar_pdf")
            error_message = f"""❌ Error al generar PDF

Se produjo un error al intentar generar el PDF de la factura.

Detalles del error:
- Factura: {self.current_factura.numero_factura if self.current_factura else 'N/A'}
- Función: generar_pdf()
- Error: {str(e)}
- Módulo: ui.facturas_methods
- Timestamp: {self.get_current_timestamp()}

Información técnica:
- Tipo de error: {type(e).__name__}
- Descripción: {str(e)}
- Estado de la factura: {'Guardada' if self.current_factura and self.current_factura.id else 'No guardada'}

Contexto:
- La funcionalidad de PDF está en desarrollo
- Los datos de la factura están seguros
- El error no afecta otras funcionalidades

Acciones recomendadas:
1. Verificar que la factura esté guardada
2. Intentar nuevamente más tarde
3. Contactar soporte si el problema persiste

Copie este mensaje para soporte técnico si es necesario."""

            show_copyable_error(self.window, get_text("error"), error_message)

    def get_current_timestamp(self):
        """Obtiene el timestamp actual formateado"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_file_size(self, file_path):
        """Obtiene el tamaño de un archivo formateado"""
        try:
            import os
            size_bytes = os.path.getsize(file_path)

            # Convertir a KB o MB según el tamaño
            if size_bytes < 1024:
                return f"{size_bytes} bytes"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"

        except Exception as e:
            self.logger.error(f"Error obteniendo tamaño de archivo: {e}")
            return "Tamaño desconocido"

    def open_pdf_file(self, pdf_path):
        """Abre el archivo PDF con el visor predeterminado"""
        try:
            import os
            import platform
            import subprocess

            system = platform.system()

            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux y otros
                subprocess.run(["xdg-open", pdf_path])

            self.logger.info(f"PDF abierto: {pdf_path}")

        except Exception as e:
            self.logger.error(f"Error abriendo PDF: {e}")
            # No mostrar error al usuario, es opcional
