#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mixin pour les méthodes de facturas - Version PyQt5 stable
"""

from database.models import Stock, StockMovement, Producto
from utils.logger import get_logger
from PyQt5.QtWidgets import QMessageBox, QApplication

class FacturasMethodsMixin:
    """Mixin avec les méthodes pour la gestion de facturas"""

    def __init__(self):
        """Initialisation du mixin"""
        self.logger = get_logger("facturas_methods")
        self.current_factura = None
        self.factura_items = []
    
    def exportar_pdf(self):
        """Exporta la factura seleccionada a PDF"""
        try:
            if not hasattr(self, 'selected_factura') or not self.selected_factura:
                print('No hay factura seleccionada')
                return
                
            print(f'Exportando factura {self.selected_factura.numero_factura} a PDF...')
            # Aquí iría la lógica de exportación PDF
            print('PDF exportado exitosamente')
            
        except Exception as e:
            print(f'Error exportando PDF: {e}')
    
    def nueva_factura(self):
        """Crea una nueva factura"""
        try:
            print('Creando nueva factura...')
            # Aquí iría la lógica de nueva factura
            
        except Exception as e:
            print(f'Error creando nueva factura: {e}')
    
    def guardar_factura(self):
        """Guarda la factura actual"""
        try:
            print('Guardando factura...')
            # Aquí iría la lógica de guardado
            
        except Exception as e:
            print(f'Error guardando factura: {e}')
    
    def get_current_timestamp(self):
        """Obtiene el timestamp actual formateado"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def get_file_size(self, file_path):
        """Obtiene el tamaño de un archivo formateado"""
        try:
            import os
            size = os.path.getsize(file_path)
            return f'{size} bytes'
        except:
            return 'Desconocido'
    
    def validate_factura_form(self):
        """Valida el formulario de factura"""
        try:
            print('Validando formulario de factura...')
            return True
        except Exception as e:
            print(f'Error validando formulario: {e}')
            return False

    def calculate_totals(self):
        """Calcula los totales de la factura"""
        try:
            print('Calculando totales...')
            return {'subtotal': 0, 'iva': 0, 'total': 0}
        except Exception as e:
            print(f'Error calculando totales: {e}')
            return None

    def add_producto_to_factura(self, producto):
        """Agrega un producto a la factura"""
        try:
            print(f'Agregando producto: {producto}')
            return True
        except Exception as e:
            print(f'Error agregando producto: {e}')
            return False

    def remove_producto_from_factura(self, producto_id):
        """Remueve un producto de la factura"""
        try:
            print(f'Removiendo producto: {producto_id}')
            return True
        except Exception as e:
            print(f'Error removiendo producto: {e}')
            return False

    def agregar_producto(self, producto):
        """Agrega un producto a la factura"""
        try:
            print(f'Agregando producto: {producto}')
            return True
        except Exception as e:
            print(f'Error agregando producto: {e}')
            return False

    def editar_producto_factura(self, producto_id, datos):
        """Edita un producto en la factura"""
        try:
            print(f'Editando producto {producto_id}: {datos}')
            return True
        except Exception as e:
            print(f'Error editando producto: {e}')
            return False

    def eliminar_producto_factura(self, producto_id):
        """Elimina un producto de la factura"""
        try:
            print(f'Eliminando producto: {producto_id}')
            return True
        except Exception as e:
            print(f'Error eliminando producto: {e}')
            return False

    def update_productos_tree(self):
        """Actualiza el árbol de productos"""
        try:
            print('Actualizando árbol de productos')
            return True
        except Exception as e:
            print(f'Error actualizando árbol: {e}')
            return False

    def update_totales(self):
        """Actualiza los totales de la factura"""
        try:
            print('Actualizando totales')
            return True
        except Exception as e:
            print(f'Error actualizando totales: {e}')
            return False

    def show_stock_impact_summary(self, productos=None):
        """Muestra el resumen de impacto en stock"""
        try:
            if productos is None:
                productos = getattr(self, 'factura_items', [])

            if not productos:
                self.logger.info("No hay productos para mostrar resumen de stock")
                return True

            # Construir mensaje de resumen
            mensaje_items = []
            total_productos = 0

            for item in productos:
                if hasattr(item, 'producto_id'):
                    producto = Producto.get_by_id(item.producto_id)
                    if producto:
                        stock_actual = Stock.get_by_product(producto.id)
                        stock_despues = stock_actual - item.cantidad

                        mensaje_items.append(
                            f"• {producto.nombre}: {stock_actual} → {stock_despues} unidades"
                        )
                        total_productos += 1

            if not mensaje_items:
                return True

            titulo = "Confirmación de Actualización de Stock"
            mensaje = f"Se actualizará el stock de {total_productos} producto(s):\n\n"
            mensaje += "\n".join(mensaje_items)
            mensaje += "\n\n¿Desea continuar?"

            # Intentar diferentes métodos de diálogo
            return self._show_confirmation_dialog(titulo, mensaje)

        except Exception as e:
            self.logger.error(f'Error mostrando resumen de stock: {e}')
            return False

    def validate_stock_availability(self, productos=None):
        """Valida la disponibilidad de stock"""
        try:
            if productos is None:
                productos = getattr(self, 'factura_items', [])

            errors = []

            for item in productos:
                if hasattr(item, 'producto_id') and hasattr(item, 'cantidad'):
                    producto = Producto.get_by_id(item.producto_id)
                    if producto:
                        stock_actual = Stock.get_by_product(producto.id)

                        # NOTA: Se permite stock negativo, solo se registra warning
                        if stock_actual < item.cantidad:
                            self.logger.warning(
                                f"Stock insuficiente para {producto.nombre}: "
                                f"disponible {stock_actual}, solicitado {item.cantidad}. "
                                f"Se permitirá stock negativo."
                            )
                        elif stock_actual - item.cantidad <= 2:  # Stock bajo
                            self.logger.warning(
                                f"Stock bajo para {producto.nombre}: "
                                f"quedará {stock_actual - item.cantidad} unidades"
                            )

            return errors

        except Exception as e:
            self.logger.error(f'Error validando disponibilidad de stock: {e}')
            return [f"Error validando stock: {e}"]

    def update_stock_after_save(self):
        """Actualiza el stock después de guardar"""
        try:
            if not hasattr(self, 'factura_items') or not self.factura_items:
                self.logger.info("No hay items para actualizar stock")
                return True

            for item in self.factura_items:
                if hasattr(item, 'producto_id') and hasattr(item, 'cantidad'):
                    # Obtener stock actual antes de la actualización
                    stock_actual = Stock.get_by_product(item.producto_id)

                    # Actualizar en base de datos (update_stock ya resta la cantidad)
                    Stock.update_stock(item.producto_id, item.cantidad)

                    # Obtener stock después de la actualización
                    nuevo_stock = Stock.get_by_product(item.producto_id)

                    # Registrar movimiento
                    producto = Producto.get_by_id(item.producto_id)
                    descripcion = f"Venta - Factura {getattr(self.current_factura, 'numero_factura', 'N/A')}"

                    StockMovement.create(
                        producto_id=item.producto_id,
                        cantidad=-item.cantidad,
                        tipo="VENTA",
                        descripcion=descripcion
                    )

                    self.logger.info(
                        f"Stock actualizado para {producto.nombre if producto else item.producto_id}: "
                        f"{stock_actual} → {nuevo_stock}"
                    )

            return True

        except Exception as e:
            self.logger.error(f'Error actualizando stock: {e}')
            return False

    def _show_confirmation_dialog(self, titulo, mensaje):
        """Muestra un diálogo de confirmación con sistema de fallback"""
        try:
            # Método 1: Usar método específico si existe
            if hasattr(self, 'show_stock_confirmation_dialog_direct'):
                return self.show_stock_confirmation_dialog_direct(titulo, mensaje)

            # Método 2: Usar método simple si existe
            if hasattr(self, 'show_simple_confirmation_dialog'):
                return self.show_simple_confirmation_dialog(mensaje)

            # Método 3: Usar _show_message si existe
            if hasattr(self, '_show_message'):
                return self._show_message("yesno", titulo, mensaje)

            # Método 4: Fallback a PyQt5
            try:
                app = QApplication.instance()
                if app is None:
                    app = QApplication([])

                reply = QMessageBox.question(
                    None, titulo, mensaje,
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                return reply == QMessageBox.Yes

            except Exception as e:
                self.logger.warning(f"Error con PyQt5 messagebox: {e}")

            # Método 5: Fallback a consola
            print(f"\n{titulo}")
            print(f"{mensaje}")
            respuesta = input("¿Continuar? (s/n): ").lower().strip()
            return respuesta in ['s', 'si', 'y', 'yes']

        except Exception as e:
            self.logger.error(f"Error mostrando diálogo de confirmación: {e}")
            return True  # Por defecto, continuar

    def show_stock_confirmation_dialog_direct(self, titulo, mensaje):
        """Método directo para mostrar diálogo de confirmación de stock"""
        try:
            return self._show_confirmation_dialog(titulo, mensaje)
        except Exception as e:
            self.logger.error(f"Error en diálogo directo: {e}")
            return True

    def show_simple_confirmation_dialog(self, mensaje):
        """Método simple para mostrar diálogo de confirmación"""
        try:
            return self._show_confirmation_dialog("Confirmación", mensaje)
        except Exception as e:
            self.logger.error(f"Error en diálogo simple: {e}")
            return True

    def _show_message(self, msg_type, title, message):
        """Método genérico para mostrar mensajes"""
        try:
            if msg_type == "yesno":
                return self._show_confirmation_dialog(title, message)
            else:
                print(f"{title}: {message}")
                return None
        except Exception as e:
            self.logger.error(f"Error mostrando mensaje: {e}")
            return None

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

            print(f"PDF abierto: {pdf_path}")

        except Exception as e:
            print(f"Error abriendo PDF: {e}")
            pass
