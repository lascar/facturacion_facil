# -*- coding: utf-8 -*-
"""
Ventana de Clientes usando PyQt6 puro
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QTextEdit, QPushButton, QTreeWidget,
                            QTreeWidgetItem, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from utils.translations import get_text
from utils.logger import get_logger, log_user_action
from database.models import Cliente
from common.validators import FormValidator

class PyQt6ClientesWindow(QWidget):
    """Ventana de clientes usando PyQt6 puro"""

    def __init__(self, parent=None, title="Gestión de Clientes"):
        # Compatibilidad con tests - si parent no es un QWidget real, usar None
        if parent and not hasattr(parent, 'isWidgetType'):
            parent = None
        super().__init__(parent)
        self.logger = get_logger("clientes_pyqt6")

        # Configurar ventana
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)

        # Variables de la interfaz
        self.clientes_tree = None
        self.nombre_entry = None
        self.email_entry = None
        self.telefono_entry = None
        self.direccion_text = None

        # Crear la interfaz
        self.create_widgets()
        self.load_clientes()

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
            title_label = QLabel(get_text("clientes"))
            title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
            main_layout.addWidget(title_label)

            # Frame para la lista de clientes
            list_frame = QFrame()
            list_layout = QVBoxLayout(list_frame)

            # TreeWidget para mostrar clientes
            self.clientes_tree = QTreeWidget()
            self.clientes_tree.setHeaderLabels(["Nombre", "Email", "Teléfono"])
            self.clientes_tree.setMaximumHeight(200)
            list_layout.addWidget(self.clientes_tree)
            main_layout.addWidget(list_frame)

            # Frame para el formulario
            form_frame = QFrame()
            form_layout = QVBoxLayout(form_frame)

            # Campos del formulario
            form_layout.addWidget(QLabel(get_text("nombre")))
            self.nombre_entry = QLineEdit()
            form_layout.addWidget(self.nombre_entry)

            form_layout.addWidget(QLabel(get_text("email")))
            self.email_entry = QLineEdit()
            form_layout.addWidget(self.email_entry)

            form_layout.addWidget(QLabel(get_text("telefono")))
            self.telefono_entry = QLineEdit()
            form_layout.addWidget(self.telefono_entry)

            form_layout.addWidget(QLabel(get_text("direccion")))
            self.direccion_text = QTextEdit()
            self.direccion_text.setMaximumHeight(100)
            form_layout.addWidget(self.direccion_text)

            main_layout.addWidget(form_frame)

            # Botones
            buttons_frame = QFrame()
            buttons_layout = QHBoxLayout(buttons_frame)

            save_btn = QPushButton(get_text("guardar"))
            save_btn.clicked.connect(self.guardar_cliente)
            buttons_layout.addWidget(save_btn)

            new_btn = QPushButton(get_text("nuevo"))
            new_btn.clicked.connect(self.nuevo_cliente)
            buttons_layout.addWidget(new_btn)

            delete_btn = QPushButton(get_text("eliminar"))
            delete_btn.clicked.connect(self.eliminar_cliente)
            buttons_layout.addWidget(delete_btn)

            main_layout.addWidget(buttons_frame)

            self.logger.info("Interfaz de clientes creada con PyQt6")

        except Exception as e:
            self.logger.error(f"Error creando widgets: {e}")
    
    def load_clientes(self):
        """Carga la lista de clientes"""
        try:
            clientes = Cliente.get_all()

            # Limpiar el tree widget
            self.clientes_tree.clear()

            # Cargar clientes en el tree widget
            for cliente in clientes:
                item = QTreeWidgetItem([
                    cliente.nombre or "",
                    cliente.email or "",
                    cliente.telefono or ""
                ])
                item.setData(0, Qt.ItemDataRole.UserRole, cliente.id)
                self.clientes_tree.addTopLevelItem(item)

            self.logger.info(f"Cargados {len(clientes)} clientes")

        except Exception as e:
            self.logger.error(f"Error cargando clientes: {e}")
    
    def guardar_cliente(self):
        """Guarda un cliente"""
        try:
            # Obtener valores del formulario
            nombre = self.nombre_entry.text().strip()
            email = self.email_entry.text().strip()
            telefono = self.telefono_entry.text().strip()
            direccion = self.direccion_text.toPlainText().strip()

            # Validar
            if not nombre:
                QMessageBox.critical(self, "Error", "El nombre es requerido")
                return

            # Crear cliente
            cliente = Cliente(
                nombre=nombre,
                email=email,
                telefono=telefono,
                direccion=direccion
            )

            cliente.save()

            # Recargar lista
            self.load_clientes()

            # Limpiar formulario
            self.nuevo_cliente()

            QMessageBox.information(self, "Éxito", "Cliente guardado correctamente")
            log_user_action(f"Cliente guardado: {nombre}")

        except Exception as e:
            self.logger.error(f"Error guardando cliente: {e}")
            QMessageBox.critical(self, "Error", f"Error guardando cliente: {str(e)}")

    def nuevo_cliente(self):
        """Limpia el formulario para un nuevo cliente"""
        try:
            self.nombre_entry.clear()
            self.email_entry.clear()
            self.telefono_entry.clear()
            self.direccion_text.clear()

        except Exception as e:
            self.logger.error(f"Error limpiando formulario: {e}")

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        try:
            current_item = self.clientes_tree.currentItem()
            if not current_item:
                QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para eliminar")
                return

            cliente_id = current_item.data(0, Qt.ItemDataRole.UserRole)
            nombre = current_item.text(0)

            reply = QMessageBox.question(
                self, "Confirmar",
                f"¿Está seguro de eliminar el cliente '{nombre}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                cliente = Cliente.get_by_id(cliente_id)
                if cliente:
                    cliente.delete()
                    self.load_clientes()
                    QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                    log_user_action(f"Cliente eliminado: {nombre}")

        except Exception as e:
            self.logger.error(f"Error eliminando cliente: {e}")
            QMessageBox.critical(self, "Error", f"Error eliminando cliente: {str(e)}")

    def validate_form(self):
        """Valida el formulario - compatibilidad con tests"""
        errors = []
        if not self.nombre_entry.text().strip():
            errors.append("El nombre es requerido")
        return errors

# Alias para compatibilidad
ClientesWindow = PyQt6ClientesWindow
AbstractClientesWindow = PyQt6ClientesWindow
