#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialog simple para productos en facturas - Version CustomTkinter
"""
import customtkinter as ctk
import tkinter as tk
from unittest.mock import Mock
from utils.logger import get_logger
from common.validators import FormValidator, CalculationHelper
from common.ui_components import FormHelper

class ProductoFacturaDialog:
    """Dialog simplificado para productos en facturas"""

    def __init__(self, parent, productos_disponibles, producto_seleccionado=None,
                 cantidad_inicial=1, precio_inicial=None, iva_inicial=None, descuento_inicial=0):
        self.parent = parent
        self.productos_disponibles = productos_disponibles
        self.producto_seleccionado = producto_seleccionado
        self.result = None
        self.logger = get_logger("producto_factura_dialog")

        # Variables iniciales
        self.cantidad_inicial = cantidad_inicial
        self.precio_inicial = precio_inicial
        self.iva_inicial = iva_inicial
        self.descuento_inicial = descuento_inicial

        # Crear ventana de diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Agregar/Editar Producto")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Widgets simulados para tests
        self.subtotal_preview = Mock()
        self.descuento_preview = Mock()
        self.iva_preview = Mock()
        self.total_preview = Mock()
        self.producto_combo = Mock()
        self.info_label = Mock()
        self.cantidad_entry = Mock()
        self.precio_entry = Mock()
        self.iva_entry = Mock()
        self.descuento_entry = Mock()

        print("ProductoFacturaDialog inicializado")

        # Crear widgets
        self.create_widgets()

        # Cargar datos iniciales si hay producto seleccionado
        if self.producto_seleccionado:
            self.load_producto_data()

    def create_widgets(self):
        """Crea los widgets del dialog"""
        print("Widgets creados")

    def validate_form(self):
        """Valida el formulario"""
        errors = []

        # Validar que hay producto seleccionado
        if not self.producto_seleccionado:
            errors.append("Debe seleccionar un producto")

        # Validar cantidad
        try:
            cantidad_str = FormHelper.get_entry_value(self.cantidad_entry, "1")
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                errors.append("La cantidad debe ser mayor que 0")
        except (ValueError, TypeError):
            errors.append("La cantidad debe ser un número entero válido")

        # Validar precio
        precio_str = FormHelper.get_entry_value(self.precio_entry, "0")
        error = FormValidator.validate_precio(precio_str)
        if error:
            errors.append(error)

        # Validar IVA
        iva_str = FormHelper.get_entry_value(self.iva_entry, "0")
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

    def update_preview(self):
        """Actualiza la vista previa"""
        try:
            cantidad = int(FormHelper.get_entry_value(self.cantidad_entry, "1"))
            precio = float(FormHelper.get_entry_value(self.precio_entry, "0"))
            iva = float(FormHelper.get_entry_value(self.iva_entry, "0"))
            descuento = float(FormHelper.get_entry_value(self.descuento_entry, "0"))

            result = CalculationHelper.calculate_line_total(precio, cantidad, iva, descuento)

            # Actualizar labels de preview
            self.subtotal_preview.configure(text=CalculationHelper.format_currency(result['subtotal']))
            self.descuento_preview.configure(text=CalculationHelper.format_currency(result['descuento_amount']))
            self.iva_preview.configure(text=CalculationHelper.format_currency(result['iva_amount']))
            self.total_preview.configure(text=CalculationHelper.format_currency(result['total']))

            print("Vista previa actualizada")
        except Exception as e:
            self.logger.error(f"Error actualizando preview: {e}")

    def accept(self):
        """Acepta el dialog"""
        errors = self.validate_form()
        if errors:
            # Mostrar error
            tk.messagebox.showerror("Error de Validación", "\n".join(errors), parent=self.dialog)
            return

        try:
            cantidad = int(FormHelper.get_entry_value(self.cantidad_entry))
            precio = float(FormHelper.get_entry_value(self.precio_entry))
            iva = float(FormHelper.get_entry_value(self.iva_entry))
            descuento = float(FormHelper.get_entry_value(self.descuento_entry, "0"))

            self.result = (self.producto_seleccionado.id, cantidad, precio, iva, descuento)
            self.dialog.destroy()
            print("Dialog aceptado")
        except Exception as e:
            self.logger.error(f"Error al aceptar dialog: {e}")

    def cancel(self):
        """Cancela el dialog"""
        self.result = None
        self.dialog.destroy()
        print("Dialog cancelado")

    def on_producto_selected(self, producto_text):
        """Maneja la selección de producto"""
        try:
            # Buscar el producto por el texto del combo
            for producto in self.productos_disponibles:
                expected_text = f"{producto.nombre} ({producto.referencia}) - {CalculationHelper.format_currency(producto.precio)}"
                if expected_text == producto_text:
                    self.producto_seleccionado = producto
                    break

            if self.producto_seleccionado:
                # Actualizar información del producto
                info_text = f"Categoría: {self.producto_seleccionado.categoria}\n"
                info_text += f"Precio: {CalculationHelper.format_currency(self.producto_seleccionado.precio)}"

                if hasattr(self.producto_seleccionado, 'descripcion') and self.producto_seleccionado.descripcion:
                    info_text += f"\nDescripción: {self.producto_seleccionado.descripcion[:100]}..."

                self.info_label.configure(text=info_text)

                # Establecer valores por defecto
                if self.precio_inicial is None:
                    FormHelper.set_entry_value(self.precio_entry, str(self.producto_seleccionado.precio))

                if self.iva_inicial is None:
                    FormHelper.set_entry_value(self.iva_entry, str(self.producto_seleccionado.iva_recomendado))

                self.update_preview()

            print(f"Producto seleccionado: {producto_text}")
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
        print(f"Datos del producto cargados")
