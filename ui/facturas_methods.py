# -*- coding: utf-8 -*-
"""
Métodos adicionales para la gestión de facturas
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from utils.translations import get_text
from utils.logger import log_user_action, log_database_operation, log_exception
from utils.factura_numbering import factura_numbering_service
from database.models import Producto, Stock, Factura
from common.validators import FormValidator, CalculationHelper
from common.ui_components import FormHelper
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
        
        return errors
    
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
                stock = Stock.get_by_product(producto_id)
                if stock and stock.cantidad_disponible < cantidad:
                    if not messagebox.askyesno("Stock Insuficiente", 
                                             f"Stock disponible: {stock.cantidad_disponible}\n"
                                             f"Cantidad solicitada: {cantidad}\n\n"
                                             "¿Desea continuar de todos modos?",
                                             parent=self.window):
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
            selection = self.productos_tree.selection()
            if not selection:
                self._show_message("warning", "Advertencia", "Seleccione un producto para editar")
                return
            
            item_index = self.productos_tree.index(selection[0])
            item = self.factura_items[item_index]
            
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
            selection = self.productos_tree.selection()
            if not selection:
                self._show_message("warning", "Advertencia", "Seleccione un producto para eliminar")
                return
            
            if self._show_message("yesno", "Confirmar", "¿Eliminar este producto de la factura?"):
                item_index = self.productos_tree.index(selection[0])
                removed_item = self.factura_items.pop(item_index)
                
                self.update_productos_tree()
                self.update_totales()
                
                log_user_action("Producto eliminado de factura", 
                              f"Producto ID: {removed_item.producto_id}")
                
        except Exception as e:
            log_exception(e, "eliminar_producto_factura")
            self._show_message("error", get_text("error"), f"Error al eliminar producto: {str(e)}")
    
    def update_productos_tree(self):
        """Actualiza la lista de productos en la factura"""
        try:
            # Limpiar lista
            for item in self.productos_tree.get_children():
                self.productos_tree.delete(item)
            
            # Agregar items
            for item in self.factura_items:
                producto = item.get_producto()
                if producto:
                    self.productos_tree.insert("", "end", values=(
                        f"{producto.nombre} ({producto.referencia})",
                        str(item.cantidad),
                        CalculationHelper.format_currency(item.precio_unitario),
                        CalculationHelper.format_percentage(item.iva_aplicado),
                        CalculationHelper.format_percentage(item.descuento),
                        CalculationHelper.format_currency(item.total)
                    ))
                    
        except Exception as e:
            log_exception(e, "update_productos_tree")
    
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
                self._show_message("error", get_text("error"), "\n".join(errors))
                return
            
            # Crear o actualizar factura
            if not self.current_factura:
                self.current_factura = Factura()
            
            # Asignar datos básicos
            self.current_factura.numero_factura = FormHelper.get_entry_value(self.numero_entry)
            self.current_factura.fecha_factura = FormHelper.get_entry_value(self.fecha_entry)
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
            self.current_factura.save()
            
            # Actualizar stock
            self.update_stock_after_save()
            
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
            for item in self.factura_items:
                stock = Stock.get_by_product(item.producto_id)
                if stock:
                    # Reducir stock
                    stock.cantidad_disponible = max(0, stock.cantidad_disponible - item.cantidad)
                    stock.save()
                    
                    log_database_operation("UPDATE", "stock", 
                                         f"Producto {item.producto_id}: -{item.cantidad}")
                    
        except Exception as e:
            log_exception(e, "update_stock_after_save")
            # No mostrar error al usuario, solo loggear
    
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
            if not self.selected_factura:
                self._show_message("warning", "Advertencia", "Seleccione una factura para exportar")
                return
            
            # TODO: Implementar generación de PDF
            self._show_message("info", "Información", 
                             "Funcionalidad de PDF en desarrollo.\n"
                             f"Factura: {self.selected_factura.numero_factura}")
            
        except Exception as e:
            log_exception(e, "exportar_pdf")
            self._show_message("error", get_text("error"), f"Error al exportar PDF: {str(e)}")
    
    def generar_pdf(self):
        """Genera PDF de la factura actual"""
        try:
            if not self.current_factura or not self.current_factura.id:
                self._show_message("warning", "Advertencia", "Guarde la factura antes de generar el PDF")
                return
            
            # TODO: Implementar generación de PDF
            self._show_message("info", "Información", 
                             "Funcionalidad de PDF en desarrollo.\n"
                             f"Factura: {self.current_factura.numero_factura}")
            
        except Exception as e:
            log_exception(e, "generar_pdf")
            self._show_message("error", get_text("error"), f"Error al generar PDF: {str(e)}")
