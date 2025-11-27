# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des factures - Version PyQt5 native
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QSplitter, QFrame, QWidget, QComboBox, QDateEdit,
    QSpinBox, QDoubleSpinBox, QTextEdit, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QDate
from PyQt5.QtGui import QFont
from datetime import datetime

from ui.base_pyqt5_window import BasePyQt5Window
from database.database import db
from utils.logger import get_logger

class FacturasPyQt5Window(BasePyQt5Window):
    """Fenêtre de gestion des factures avec PyQt5"""
    
    # Signaux
    factura_selected = Signal(dict)
    factura_updated = Signal(int)
    
    def __init__(self, parent=None):
        self.logger = get_logger(self.__class__.__name__)
        super().__init__(parent, "Gestión de Facturas", 1200, 800)
        
        # Variables
        self.facturas = []
        self.selected_factura_id = None
        
        # Charger les données
        self.load_facturas()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Titre
        title_label = QLabel("Gestión de Facturas")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # Splitter pour diviser l'interface
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Configuration des sections
        self.setup_facturas_list(splitter)
        self.setup_factura_info(splitter)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.new_btn = QPushButton("➕ Nueva Factura")
        self.view_btn = QPushButton("👁️ Ver Detalles")
        self.refresh_btn = QPushButton("🔄 Actualizar")
        
        buttons_layout.addWidget(self.new_btn)
        buttons_layout.addWidget(self.view_btn)
        buttons_layout.addWidget(self.refresh_btn)
        buttons_layout.addStretch()
        
        main_layout.addLayout(buttons_layout)
        
        # Connexions
        self.setup_connections()
        
        # Appliquer le style
        self.apply_style()
        
    def setup_facturas_list(self, parent):
        """Configurer la liste des factures"""
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # Label
        list_label = QLabel("Lista de Facturas")
        list_label.setFont(QFont("Arial", 12, QFont.Bold))
        list_layout.addWidget(list_label)
        
        # Table des factures
        self.facturas_table = QTableWidget()
        headers = ["Número", "Cliente", "Fecha", "Total", "Estado"]
        self.setup_table_widget(self.facturas_table, headers)
        
        # Connecter la sélection
        self.facturas_table.itemSelectionChanged.connect(self.on_factura_selected)
        
        list_layout.addWidget(self.facturas_table)
        parent.addWidget(list_widget)
        
    def setup_factura_info(self, parent):
        """Configurer l'affichage des informations de facture"""
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        
        # GroupBox pour les informations
        info_group = QGroupBox("Información de la Factura")
        info_group_layout = QGridLayout(info_group)
        
        # Labels d'information
        self.numero_label = QLabel("Número: -")
        self.cliente_label = QLabel("Cliente: -")
        self.fecha_label = QLabel("Fecha: -")
        self.total_label = QLabel("Total: -")
        self.estado_label = QLabel("Estado: -")
        
        info_group_layout.addWidget(self.numero_label, 0, 0)
        info_group_layout.addWidget(self.cliente_label, 1, 0)
        info_group_layout.addWidget(self.fecha_label, 2, 0)
        info_group_layout.addWidget(self.total_label, 3, 0)
        info_group_layout.addWidget(self.estado_label, 4, 0)
        
        info_layout.addWidget(info_group)
        
        # Message pour la création de factures
        message_group = QGroupBox("Crear Nueva Factura")
        message_layout = QVBoxLayout(message_group)
        
        message_label = QLabel("""
        Para crear una nueva factura:
        1. Haga clic en "Nueva Factura"
        2. Seleccione un cliente
        3. Agregue productos
        4. Confirme la factura
        
        (Funcionalidad completa en desarrollo)
        """)
        message_label.setWordWrap(True)
        message_layout.addWidget(message_label)
        
        info_layout.addWidget(message_group)
        info_layout.addStretch()
        
        parent.addWidget(info_widget)
        
    def setup_connections(self):
        """Configurer les connexions de signaux"""
        self.new_btn.clicked.connect(self.new_factura)
        self.view_btn.clicked.connect(self.view_factura)
        self.refresh_btn.clicked.connect(self.load_facturas)
        
    def load_facturas(self):
        """Charger les factures depuis la base de données"""
        try:
            self.facturas = db.get_all_invoices()
            self.update_facturas_table()
        except Exception as e:
            self.logger.error(f"Erreur chargement factures: {e}")
            self.show_error("Erreur", f"Impossible de charger les factures: {str(e)}")

    def update_facturas_table(self):
        """Mettre à jour la table des factures"""
        self.facturas_table.setRowCount(len(self.facturas))

        for row, factura in enumerate(self.facturas):
            self.facturas_table.setItem(row, 0, QTableWidgetItem(str(factura.get('numero', ''))))
            self.facturas_table.setItem(row, 1, QTableWidgetItem(str(factura.get('cliente_nombre', ''))))
            self.facturas_table.setItem(row, 2, QTableWidgetItem(str(factura.get('fecha', ''))))
            self.facturas_table.setItem(row, 3, QTableWidgetItem(f"{factura.get('total', 0):.2f}€"))
            self.facturas_table.setItem(row, 4, QTableWidgetItem(str(factura.get('estado', ''))))

    def on_factura_selected(self):
        """Gérer la sélection d'une facture"""
        current_row = self.facturas_table.currentRow()
        if current_row >= 0 and current_row < len(self.facturas):
            factura = self.facturas[current_row]
            self.selected_factura_id = factura.get('id')
            self.load_factura_info(factura)
            self.factura_selected.emit(factura)

    def load_factura_info(self, factura):
        """Charger les informations d'une facture"""
        self.numero_label.setText(f"Número: {factura.get('numero', '-')}")
        self.cliente_label.setText(f"Cliente: {factura.get('cliente', '-')}")
        self.fecha_label.setText(f"Fecha: {factura.get('fecha', '-')}")
        self.total_label.setText(f"Total: {factura.get('total', 0):.2f}€")
        self.estado_label.setText(f"Estado: {factura.get('estado', '-')}")

    def new_factura(self):
        """Créer une nouvelle facture"""
        dialog = CrearFacturaDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Recharger les factures après création
            self.load_facturas()

    def view_factura(self):
        """Ver los detalles de la factura sélectionnée"""
        if not self.selected_factura_id:
            self.show_warning("Selección", "Seleccione una factura para ver los detalles")
            return

        try:
            factura = db.get_invoice_by_id(self.selected_factura_id)
            if factura:
                dialog = VerFacturaDialog(factura, self)
                dialog.exec_()
            else:
                self.show_error("Error", "No se pudo cargar la factura")
        except Exception as e:
            self.logger.error(f"Error cargando factura: {e}")
            self.show_error("Error", f"Error al cargar la factura: {str(e)}")


class CrearFacturaDialog(QDialog):
    """Dialog para crear una nueva factura"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.setWindowTitle("Crear Nueva Factura")
        self.setModal(True)
        self.resize(800, 600)

        # Variables
        self.clientes = []
        self.productos = []
        self.lineas_factura = []

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Configurar la interfaz"""
        layout = QVBoxLayout(self)

        # Información de la factura
        info_group = QGroupBox("Información de la Factura")
        info_layout = QGridLayout(info_group)

        # Número de factura (auto-generado)
        self.numero_edit = QLineEdit()
        self.numero_edit.setText(self.generate_invoice_number())
        self.numero_edit.setReadOnly(True)

        # Fecha
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)

        # Cliente
        self.cliente_combo = QComboBox()

        info_layout.addWidget(QLabel("Número:"), 0, 0)
        info_layout.addWidget(self.numero_edit, 0, 1)
        info_layout.addWidget(QLabel("Fecha:"), 0, 2)
        info_layout.addWidget(self.fecha_edit, 0, 3)
        info_layout.addWidget(QLabel("Cliente:"), 1, 0)
        info_layout.addWidget(self.cliente_combo, 1, 1, 1, 3)

        layout.addWidget(info_group)

        # Productos
        productos_group = QGroupBox("Productos")
        productos_layout = QVBoxLayout(productos_group)

        # Selector de productos
        selector_layout = QHBoxLayout()
        self.producto_combo = QComboBox()
        self.cantidad_spin = QSpinBox()
        self.cantidad_spin.setMinimum(1)
        self.cantidad_spin.setMaximum(999)
        self.cantidad_spin.setValue(1)

        self.agregar_btn = QPushButton("➕ Agregar")
        self.agregar_btn.clicked.connect(self.agregar_producto)

        selector_layout.addWidget(QLabel("Producto:"))
        selector_layout.addWidget(self.producto_combo, 2)
        selector_layout.addWidget(QLabel("Cantidad:"))
        selector_layout.addWidget(self.cantidad_spin)
        selector_layout.addWidget(self.agregar_btn)

        productos_layout.addLayout(selector_layout)

        # Tabla de productos
        self.productos_table = QTableWidget()
        headers = ["Producto", "Cantidad", "Precio", "IVA", "Total", ""]
        self.productos_table.setColumnCount(len(headers))
        self.productos_table.setHorizontalHeaderLabels(headers)
        self.productos_table.horizontalHeader().setStretchLastSection(True)

        productos_layout.addWidget(self.productos_table)
        layout.addWidget(productos_group)

        # Totales
        totales_group = QGroupBox("Totales")
        totales_layout = QGridLayout(totales_group)

        self.subtotal_label = QLabel("0.00€")
        self.iva_label = QLabel("0.00€")
        self.total_label = QLabel("0.00€")
        self.total_label.setFont(QFont("Arial", 12, QFont.Bold))

        totales_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        totales_layout.addWidget(self.subtotal_label, 0, 1)
        totales_layout.addWidget(QLabel("IVA:"), 1, 0)
        totales_layout.addWidget(self.iva_label, 1, 1)
        totales_layout.addWidget(QLabel("TOTAL:"), 2, 0)
        totales_layout.addWidget(self.total_label, 2, 1)

        layout.addWidget(totales_group)

        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.guardar_factura)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def load_data(self):
        """Charger les données nécessaires"""
        try:
            # Charger les clients
            self.clientes = db.get_all_clients()
            self.cliente_combo.clear()
            self.cliente_combo.addItem("Seleccionar cliente...", None)
            for cliente in self.clientes:
                self.cliente_combo.addItem(f"{cliente['nombre']} - {cliente['nif']}", cliente)

            # Charger les produits
            self.productos = db.get_all_products()
            self.producto_combo.clear()
            self.producto_combo.addItem("Seleccionar producto...", None)
            for producto in self.productos:
                stock = producto.get('stock_actual', 0)
                self.producto_combo.addItem(
                    f"{producto['nombre']} - {producto['precio_venta']:.2f}€ (Stock: {stock})",
                    producto
                )

        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")

    def generate_invoice_number(self):
        """Generar número de factura automático"""
        try:
            # Obtener el último número de factura
            facturas = db.get_all_invoices()
            if facturas:
                # Extraer números y encontrar el máximo
                numeros = []
                for f in facturas:
                    try:
                        num = int(f['numero'].replace('F', '').replace('-', ''))
                        numeros.append(num)
                    except:
                        pass
                if numeros:
                    next_num = max(numeros) + 1
                else:
                    next_num = 1
            else:
                next_num = 1

            return f"F-{next_num:04d}"
        except:
            return f"F-{datetime.now().strftime('%Y%m%d')}-001"

    def agregar_producto(self):
        """Agregar producto a la factura"""
        producto_data = self.producto_combo.currentData()
        if not producto_data:
            return

        cantidad = self.cantidad_spin.value()
        stock_actual = producto_data.get('stock_actual', 0)

        # Verificar stock
        if cantidad > stock_actual:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Stock insuficiente",
                              f"Stock disponible: {stock_actual}\nCantidad solicitada: {cantidad}")
            return

        # Calcular precios
        precio_unitario = producto_data['precio_venta']
        iva_rate = producto_data.get('iva_recomendado', 21.0) / 100
        subtotal = precio_unitario * cantidad
        iva_amount = subtotal * iva_rate
        total = subtotal + iva_amount

        # Agregar a la lista
        linea = {
            'producto_id': producto_data['id'],
            'producto_nombre': producto_data['nombre'],
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'iva_aplicado': producto_data.get('iva_recomendado', 21.0),
            'subtotal': subtotal,
            'iva_amount': iva_amount,
            'total': total
        }

        self.lineas_factura.append(linea)
        self.update_productos_table()
        self.calculate_totals()

        # Reset selección
        self.producto_combo.setCurrentIndex(0)
        self.cantidad_spin.setValue(1)

    def update_productos_table(self):
        """Actualizar tabla de productos"""
        self.productos_table.setRowCount(len(self.lineas_factura))

        for row, linea in enumerate(self.lineas_factura):
            self.productos_table.setItem(row, 0, QTableWidgetItem(linea['producto_nombre']))
            self.productos_table.setItem(row, 1, QTableWidgetItem(str(linea['cantidad'])))
            self.productos_table.setItem(row, 2, QTableWidgetItem(f"{linea['precio_unitario']:.2f}€"))
            self.productos_table.setItem(row, 3, QTableWidgetItem(f"{linea['iva_aplicado']:.1f}%"))
            self.productos_table.setItem(row, 4, QTableWidgetItem(f"{linea['total']:.2f}€"))

            # Botón eliminar
            eliminar_btn = QPushButton("🗑️")
            eliminar_btn.clicked.connect(lambda checked, r=row: self.eliminar_linea(r))
            self.productos_table.setCellWidget(row, 5, eliminar_btn)

    def eliminar_linea(self, row):
        """Eliminar línea de la factura"""
        if 0 <= row < len(self.lineas_factura):
            del self.lineas_factura[row]
            self.update_productos_table()
            self.calculate_totals()

    def calculate_totals(self):
        """Calcular totales de la factura"""
        subtotal = sum(linea['subtotal'] for linea in self.lineas_factura)
        iva_total = sum(linea['iva_amount'] for linea in self.lineas_factura)
        total = subtotal + iva_total

        self.subtotal_label.setText(f"{subtotal:.2f}€")
        self.iva_label.setText(f"{iva_total:.2f}€")
        self.total_label.setText(f"{total:.2f}€")

    def guardar_factura(self):
        """Guardar la factura"""
        try:
            # Validaciones
            cliente_data = self.cliente_combo.currentData()
            if not cliente_data:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Validación", "Seleccione un cliente")
                return

            if not self.lineas_factura:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Validación", "Agregue al menos un producto")
                return

            # Preparar datos de la factura
            subtotal = sum(linea['subtotal'] for linea in self.lineas_factura)
            iva_total = sum(linea['iva_amount'] for linea in self.lineas_factura)
            total = subtotal + iva_total

            factura_data = {
                'numero': self.numero_edit.text(),
                'fecha': self.fecha_edit.date().toString('yyyy-MM-dd'),
                'cliente': cliente_data,
                'subtotal': subtotal,
                'iva_total': iva_total,
                'total': total,
                'estado': 'Borrador',
                'lineas': self.lineas_factura
            }

            # Debug: Imprimir datos antes de guardar
            print(f"DEBUG: Guardando factura con {len(self.lineas_factura)} líneas")
            for i, linea in enumerate(self.lineas_factura):
                print(f"  Línea {i+1}: Producto ID {linea['producto_id']}, Cantidad {linea['cantidad']}")

            # Guardar en la base de datos
            factura_id = db.add_invoice(factura_data)

            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Éxito", f"Factura {self.numero_edit.text()} creada correctamente\nID: {factura_id}")

            self.accept()

        except Exception as e:
            self.logger.error(f"Error guardando factura: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al guardar la factura: {str(e)}")


class VerFacturaDialog(QDialog):
    """Dialog para ver detalles de una factura"""

    def __init__(self, factura_data, parent=None):
        super().__init__(parent)
        self.factura_data = factura_data
        self.setWindowTitle(f"Factura {factura_data['numero']}")
        self.setModal(True)
        self.resize(600, 500)

        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz"""
        layout = QVBoxLayout(self)

        # Información de la factura
        info_group = QGroupBox("Información")
        info_layout = QGridLayout(info_group)

        info_layout.addWidget(QLabel("Número:"), 0, 0)
        info_layout.addWidget(QLabel(self.factura_data['numero']), 0, 1)
        info_layout.addWidget(QLabel("Fecha:"), 0, 2)
        info_layout.addWidget(QLabel(self.factura_data['fecha']), 0, 3)

        info_layout.addWidget(QLabel("Cliente:"), 1, 0)
        info_layout.addWidget(QLabel(self.factura_data['cliente']['nombre']), 1, 1, 1, 3)

        info_layout.addWidget(QLabel("Estado:"), 2, 0)
        info_layout.addWidget(QLabel(self.factura_data['estado']), 2, 1)

        layout.addWidget(info_group)

        # Líneas de la factura
        lineas_group = QGroupBox("Productos")
        lineas_layout = QVBoxLayout(lineas_group)

        lineas_table = QTableWidget()
        headers = ["Producto", "Cantidad", "Precio", "IVA", "Total"]
        lineas_table.setColumnCount(len(headers))
        lineas_table.setHorizontalHeaderLabels(headers)
        lineas_table.horizontalHeader().setStretchLastSection(True)

        lineas = self.factura_data.get('lineas', [])
        lineas_table.setRowCount(len(lineas))

        for row, linea in enumerate(lineas):
            lineas_table.setItem(row, 0, QTableWidgetItem(linea.get('producto_nombre', 'N/A')))
            lineas_table.setItem(row, 1, QTableWidgetItem(str(linea.get('cantidad', 0))))
            lineas_table.setItem(row, 2, QTableWidgetItem(f"{linea.get('precio_unitario', 0):.2f}€"))
            lineas_table.setItem(row, 3, QTableWidgetItem(f"{linea.get('iva_aplicado', 0):.1f}%"))
            lineas_table.setItem(row, 4, QTableWidgetItem(f"{linea.get('total', 0):.2f}€"))

        lineas_layout.addWidget(lineas_table)
        layout.addWidget(lineas_group)

        # Totales
        totales_group = QGroupBox("Totales")
        totales_layout = QGridLayout(totales_group)

        totales_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        totales_layout.addWidget(QLabel(f"{self.factura_data.get('subtotal', 0):.2f}€"), 0, 1)
        totales_layout.addWidget(QLabel("IVA:"), 1, 0)
        totales_layout.addWidget(QLabel(f"{self.factura_data.get('iva_total', 0):.2f}€"), 1, 1)
        totales_layout.addWidget(QLabel("TOTAL:"), 2, 0)

        total_label = QLabel(f"{self.factura_data.get('total', 0):.2f}€")
        total_label.setFont(QFont("Arial", 12, QFont.Bold))
        totales_layout.addWidget(total_label, 2, 1)

        layout.addWidget(totales_group)

        # Botón cerrar
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
