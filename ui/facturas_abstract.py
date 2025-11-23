# -*- coding: utf-8 -*-
"""
Ventana de Facturas usando PyQt6 puro
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QTextEdit, QPushButton, QTreeWidget,
                            QTreeWidgetItem, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from utils.translations import get_text
from utils.logger import get_logger, log_user_action
from database.models import Factura, FacturaItem, Producto, Organizacion
from common.validators import FormValidator, CalculationHelper

class PyQt6FacturasWindow(QWidget):
    """Ventana de facturas usando PyQt6 puro"""

    def __init__(self, parent=None, title="Gestión de Facturas"):
        # Compatibilidad con tests - si parent no es un QWidget real, usar None
        if parent and not hasattr(parent, 'isWidgetType'):
            parent = None
        super().__init__(parent)
        self.logger = get_logger("facturas_pyqt6")

        # Configurar ventana
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1000, 900)

        # Variables de la interfaz
        self.facturas_tree = None
        self.numero_entry = None
        self.cliente_entry = None
        self.fecha_entry = None
        self.items_tree = None

        # Variables de estado
        self.current_factura = None

        # Crear la interfaz
        self.create_widgets()
        self.load_facturas()

    @property
    def window(self):
        """Compatibilidad con tests"""
        return self
    
    def create_widgets(self):
        """Crea los widgets de la interfaz usando PyQt6"""
        try:
            # Layout principal
            main_layout = QVBoxLayout(self)

            # Título
            title_label = QLabel(get_text("facturas"))
            title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
            main_layout.addWidget(title_label)

            # Frame para la lista de facturas (disposición vertical)
            list_frame = QFrame()
            list_layout = QVBoxLayout(list_frame)

            # TreeWidget para mostrar facturas con altura reducida
            self.facturas_tree = QTreeWidget()
            self.facturas_tree.setHeaderLabels(["Número", "Cliente", "Fecha", "Total"])
            self.facturas_tree.setMaximumHeight(200)  # Altura reducida
            list_layout.addWidget(self.facturas_tree)
            main_layout.addWidget(list_frame)

            # Frame para el formulario de factura
            form_frame = QFrame()
            form_layout = QVBoxLayout(form_frame)

            # Campos del formulario
            form_layout.addWidget(QLabel(get_text("numero_factura")))
            self.numero_entry = QLineEdit()
            form_layout.addWidget(self.numero_entry)

            form_layout.addWidget(QLabel(get_text("cliente")))
            self.cliente_entry = QLineEdit()
            form_layout.addWidget(self.cliente_entry)

            form_layout.addWidget(QLabel(get_text("fecha")))
            self.fecha_entry = QLineEdit()
            form_layout.addWidget(self.fecha_entry)

            main_layout.addWidget(form_frame)

            # Frame para items de factura
            items_frame = QFrame()
            items_layout = QVBoxLayout(items_frame)
            items_layout.addWidget(QLabel("Items de Factura"))
            self.items_tree = QTreeWidget()
            self.items_tree.setHeaderLabels(["Producto", "Cantidad", "Precio", "Total"])
            self.items_tree.setMaximumHeight(150)
            items_layout.addWidget(self.items_tree)
            main_layout.addWidget(items_frame)

            # Botones
            buttons_frame = QFrame()
            buttons_layout = QHBoxLayout(buttons_frame)

            save_btn = QPushButton(get_text("guardar"))
            save_btn.clicked.connect(self.guardar_factura)
            buttons_layout.addWidget(save_btn)

            new_btn = QPushButton(get_text("nueva_factura"))
            new_btn.clicked.connect(self.nueva_factura)
            buttons_layout.addWidget(new_btn)

            delete_btn = QPushButton(get_text("eliminar"))
            delete_btn.clicked.connect(self.eliminar_factura)
            buttons_layout.addWidget(delete_btn)

            main_layout.addWidget(buttons_frame)

            self.logger.info("Interfaz de facturas creada con PyQt6")

        except Exception as e:
            self.logger.error(f"Error creando widgets: {e}")
    
    def load_facturas(self):
        """Carga la lista de facturas"""
        try:
            facturas = Factura.get_all()

            # Limpiar el tree widget
            self.facturas_tree.clear()

            # Cargar facturas en el tree widget
            for factura in facturas:
                # Usar los atributos correctos del modelo Factura
                total = getattr(factura, 'total', getattr(factura, 'total_factura', 0.0))
                item = QTreeWidgetItem([
                    factura.numero_factura or "",
                    factura.nombre_cliente or "",
                    factura.fecha or "",
                    f"€{total:.2f}"
                ])
                item.setData(0, Qt.ItemDataRole.UserRole, factura.id)
                self.facturas_tree.addTopLevelItem(item)

            self.logger.info(f"Cargadas {len(facturas)} facturas")

        except Exception as e:
            self.logger.error(f"Error cargando facturas: {e}")
    
    def guardar_factura(self):
        """Guarda una factura"""
        try:
            # Obtener valores del formulario
            numero = self.numero_entry.text().strip()
            cliente = self.cliente_entry.text().strip()
            fecha = self.fecha_entry.text().strip()

            # Validar
            if not numero:
                QMessageBox.critical(self, "Error", "El número de factura es requerido")
                return

            if not cliente:
                QMessageBox.critical(self, "Error", "El cliente es requerido")
                return

            # Crear factura básica para test
            factura = Factura(
                numero_factura=numero,
                nombre_cliente=cliente,
                fecha=fecha or "2024-01-01",
                subtotal=0.0,
                iva_total=0.0,
                total_factura=0.0  # Usar el atributo correcto
            )

            factura.save()

            # Recargar lista
            self.load_facturas()

            # Limpiar formulario
            self.nueva_factura()

            QMessageBox.information(self, "Éxito", "Factura guardada correctamente")
            log_user_action(f"Factura guardada: {numero}")

        except Exception as e:
            self.logger.error(f"Error guardando factura: {e}")
            QMessageBox.critical(self, "Error", f"Error guardando factura: {str(e)}")

    def nueva_factura(self):
        """Limpia el formulario para una nueva factura"""
        try:
            self.numero_entry.clear()
            self.cliente_entry.clear()
            self.fecha_entry.clear()
            self.items_tree.clear()

            # Generar nuevo número de factura
            try:
                next_number = Factura.get_next_numero()
                self.numero_entry.setText(next_number)
            except:
                pass

        except Exception as e:
            self.logger.error(f"Error limpiando formulario: {e}")

    def eliminar_factura(self):
        """Elimina la factura seleccionada"""
        try:
            current_item = self.facturas_tree.currentItem()
            if not current_item:
                QMessageBox.warning(self, "Advertencia", "Seleccione una factura para eliminar")
                return

            factura_id = current_item.data(0, Qt.ItemDataRole.UserRole)
            numero = current_item.text(0)

            reply = QMessageBox.question(
                self, "Confirmar",
                f"¿Está seguro de eliminar la factura '{numero}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                factura = Factura.get_by_id(factura_id)
                if factura:
                    factura.delete()
                    self.load_facturas()
                    QMessageBox.information(self, "Éxito", "Factura eliminada correctamente")
                    log_user_action(f"Factura eliminada: {numero}")

        except Exception as e:
            self.logger.error(f"Error eliminando factura: {e}")
            QMessageBox.critical(self, "Error", f"Error eliminando factura: {str(e)}")

# Alias para compatibilidad
FacturasWindow = PyQt6FacturasWindow
AbstractFacturasWindow = PyQt6FacturasWindow
