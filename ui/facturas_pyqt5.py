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
from utils.invoice_status_manager import invoice_status_manager

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
        # Activer le scroll pour cette fenêtre (contenu très long)
        self.enable_window_scroll(enable_horizontal=False, enable_vertical=True)

        # Obtenir le layout de contenu (scrollable ou normal)
        main_layout = self.get_content_layout()

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
        self.edit_btn = QPushButton("✏️ Editar")
        self.eliminar_btn = QPushButton("🗑️ Eliminar")
        self.refresh_btn = QPushButton("🔄 Actualizar")

        buttons_layout.addWidget(self.new_btn)
        buttons_layout.addWidget(self.view_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.eliminar_btn)
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
        self.edit_btn.clicked.connect(self.edit_factura)
        self.eliminar_btn.clicked.connect(self.eliminar_factura)
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
        self.logger.debug("new_factura() appelée - Ouverture dialogue création")
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

    def edit_factura(self):
        """Editar la factura seleccionada"""
        if not self.selected_factura_id:
            self.show_warning("Selección", "Seleccione una factura para editar")
            return

        try:
            self.logger.debug(f"edit_factura() - Editando factura ID: {self.selected_factura_id}")

            # Désactiver temporairement le bouton Nueva Factura pour éviter l'activation accidentelle
            self.new_btn.setEnabled(False)
            self.logger.debug("edit_factura() - Bouton Nueva Factura désactivé temporairement")

            factura = db.get_invoice_by_id(self.selected_factura_id)
            if factura:
                dialog = EditarFacturaDialog(factura, self)
                result = dialog.exec_()
                self.logger.debug(f"edit_factura() - Resultado del diálogo: {result}")
                if result == QDialog.Accepted:
                    # Recharger les factures après modification
                    self.logger.debug("edit_factura() - Recargando facturas...")
                    self.load_facturas()
                    self.logger.debug("edit_factura() - Facturas recargadas, terminado")
            else:
                self.show_error("Error", "No se pudo cargar la factura")

        except Exception as e:
            self.logger.error(f"Error editando factura: {e}")
            self.show_error("Error", f"Error al editar la factura: {str(e)}")
        finally:
            # Réactiver le bouton Nueva Factura
            self.new_btn.setEnabled(True)
            self.logger.debug("edit_factura() - Bouton Nueva Factura réactivé")

            # S'assurer que le focus n'est pas sur le bouton Nueva Factura
            if self.new_btn.hasFocus():
                self.facturas_table.setFocus()
                self.logger.debug("edit_factura() - Focus déplacé du bouton Nueva Factura vers la table")

    def eliminar_factura(self):
        """Eliminar la factura seleccionada"""
        # Vérifier si une suppression est déjà en cours
        if hasattr(self, '_deleting_invoice') and self._deleting_invoice:
            return

        # Vérifier si le bouton est désactivé (protection supplémentaire)
        if not self.eliminar_btn.isEnabled():
            return

        if not self.selected_factura_id:
            self.show_warning("Selección", "Seleccione una factura para eliminar")
            return

        try:
            # Marquer qu'une suppression est en cours et désactiver le bouton
            self._deleting_invoice = True
            self.eliminar_btn.setEnabled(False)
            # Obtener información de la factura para confirmación
            current_row = self.facturas_table.currentRow()
            if current_row < 0 or current_row >= len(self.facturas):
                self.show_error("Error", "No se pudo obtener la información de la factura")
                return

            factura = self.facturas[current_row]
            numero_factura = factura.get('numero', 'N/A')
            cliente_nombre = factura.get('cliente', 'N/A')

            # Confirmar eliminación
            from PyQt5.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar la factura?\n\n"
                f"Número: {numero_factura}\n"
                f"Cliente: {cliente_nombre}\n\n"
                f"Esta acción no se puede deshacer.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            # Vérifier que l'utilisateur a bien confirmé
            if reply != QMessageBox.Yes:
                return

            # Eliminar de la base de datos
            success = db.delete_invoice(self.selected_factura_id)

            if success:
                self.show_info("Éxito", f"Factura {numero_factura} eliminada correctamente")

                # Bloquer temporairement les signaux de sélection
                self.facturas_table.blockSignals(True)

                # Recargar la lista de facturas
                self.load_facturas()

                # Limpiar selección
                self.selected_factura_id = None
                self.clear_factura_info()

                # Réactiver les signaux après un délai
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(500, lambda: self.facturas_table.blockSignals(False))

            else:
                self.show_error("Error", "No se pudo eliminar la factura")

        except Exception as e:
            self.logger.error(f"Error eliminando factura: {e}")
            self.show_error("Error", f"Error al eliminar la factura: {str(e)}")
        finally:
            # Réinitialiser le flag de suppression
            self._deleting_invoice = False

            # Réactiver le bouton après un délai pour éviter les clics multiples
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(1000, lambda: self.eliminar_btn.setEnabled(True))

    def clear_factura_info(self):
        """Limpiar la información de la factura"""
        self.numero_label.setText("Número: -")
        self.cliente_label.setText("Cliente: -")
        self.fecha_label.setText("Fecha: -")
        self.total_label.setText("Total: 0.00€")
        self.estado_label.setText("Estado: -")


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

        # Connecter les changements dans la table
        self.productos_table.itemChanged.connect(self.on_table_item_changed)

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

    def get_available_stock_for_product(self, producto_id):
        """Calcular el stock disponible para un producto (para creación = stock actual)"""
        try:
            # Para creación de factura, solo necesitamos el stock actual
            for producto in self.productos:
                if producto.get('id') == producto_id:
                    stock_actual = producto.get('stock_actual', 0)
                    self.logger.debug(f"CrearFacturaDialog - Stock para producto {producto_id}: actual={stock_actual}")
                    return stock_actual

            # Si no se encuentra el producto
            self.logger.warning(f"CrearFacturaDialog - Producto {producto_id} no encontrado")
            return 0

        except Exception as e:
            self.logger.error(f"Error calculando stock disponible: {e}")
            return 0

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
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.logger.debug(f"[{timestamp}] CrearFacturaDialog - Llamando db.get_all_products()")
            self.productos = db.get_all_products()
            self.logger.debug(f"[{timestamp}] CrearFacturaDialog - Recibidos {len(self.productos)} productos")
            self.producto_combo.clear()
            self.producto_combo.addItem("Seleccionar producto...", None)
            for producto in self.productos:
                stock = producto.get('stock_actual', 0)
                from datetime import datetime
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                self.logger.debug(f"[{timestamp}] CrearFacturaDialog - Producto: {producto['nombre']}, Stock: {stock}, ID: {producto.get('id')}")
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

    def on_table_item_changed(self, item):
        """Gestionar cambios en la tabla de productos"""
        if not item:
            return

        row = item.row()
        col = item.column()

        if row >= len(self.lineas_factura):
            return

        try:
            if col == 1:  # Cantidad
                nueva_cantidad = int(item.text())
                if nueva_cantidad <= 0:
                    item.setText(str(self.lineas_factura[row]['cantidad']))
                    return

                # Verificar stock
                producto_id = self.lineas_factura[row]['producto_id']
                producto_data = None
                for i in range(self.producto_combo.count()):
                    data = self.producto_combo.itemData(i)
                    if data and data.get('id') == producto_id:
                        producto_data = data
                        break

                if producto_data:
                    stock_actual = producto_data.get('stock_actual', 0)
                    if nueva_cantidad > stock_actual:
                        from PyQt5.QtWidgets import QMessageBox
                        QMessageBox.warning(self, "Stock insuficiente",
                                          f"Stock disponible: {stock_actual}")
                        item.setText(str(self.lineas_factura[row]['cantidad']))
                        return

                self.lineas_factura[row]['cantidad'] = nueva_cantidad
                self.recalcular_linea(row)

            elif col == 3:  # IVA
                nuevo_iva = float(item.text().replace('%', ''))
                if nuevo_iva < 0 or nuevo_iva > 100:
                    item.setText(f"{self.lineas_factura[row]['iva_aplicado']:.1f}")
                    return

                self.lineas_factura[row]['iva_aplicado'] = nuevo_iva
                self.recalcular_linea(row)

        except ValueError:
            # Restaurer la valeur précédente en cas d'erreur
            if col == 1:
                item.setText(str(self.lineas_factura[row]['cantidad']))
            elif col == 3:
                item.setText(f"{self.lineas_factura[row]['iva_aplicado']:.1f}")

    def recalcular_linea(self, row):
        """Recalculer les totaux d'une ligne"""
        linea = self.lineas_factura[row]

        # Recalculer les montants
        subtotal = linea['precio_unitario'] * linea['cantidad']
        iva_amount = subtotal * (linea['iva_aplicado'] / 100)
        total = subtotal + iva_amount

        # Mettre à jour la ligne
        linea['subtotal'] = subtotal
        linea['iva_amount'] = iva_amount
        linea['total'] = total

        # Mettre à jour l'affichage
        self.productos_table.setItem(row, 4, QTableWidgetItem(f"{total:.2f}€"))

        # Recalculer les totaux généraux
        self.calculate_totals()

    def update_productos_table(self):
        """Actualizar tabla de productos"""
        self.productos_table.setRowCount(len(self.lineas_factura))

        for row, linea in enumerate(self.lineas_factura):
            # Producto (no editable)
            item_producto = QTableWidgetItem(linea['producto_nombre'])
            item_producto.setFlags(item_producto.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 0, item_producto)

            # Cantidad (editable)
            item_cantidad = QTableWidgetItem(str(linea['cantidad']))
            self.productos_table.setItem(row, 1, item_cantidad)

            # Precio (no editable)
            item_precio = QTableWidgetItem(f"{linea['precio_unitario']:.2f}€")
            item_precio.setFlags(item_precio.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 2, item_precio)

            # IVA (editable)
            item_iva = QTableWidgetItem(f"{linea['iva_aplicado']:.1f}")
            self.productos_table.setItem(row, 3, item_iva)

            # Total (no editable)
            item_total = QTableWidgetItem(f"{linea['total']:.2f}€")
            item_total.setFlags(item_total.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 4, item_total)

            # Botón eliminar centrado
            eliminar_btn = QPushButton("🗑️")
            eliminar_btn.setFixedSize(40, 30)
            eliminar_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)
            eliminar_btn.clicked.connect(lambda checked, r=row: self.eliminar_linea(r))

            # Crear un widget contenedor para centrar el botón
            container_widget = QWidget()
            container_layout = QHBoxLayout(container_widget)
            container_layout.addWidget(eliminar_btn)
            container_layout.setAlignment(Qt.AlignCenter)
            container_layout.setContentsMargins(5, 2, 5, 2)

            self.productos_table.setCellWidget(row, 5, container_widget)

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


class EditarFacturaDialog(QDialog):
    """Dialog para editar una factura existente"""

    def __init__(self, factura_data, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.factura_data = factura_data
        self.setWindowTitle(f"Editar Factura {factura_data['numero']}")
        self.setModal(True)
        self.resize(800, 600)

        # Variables
        self.clientes = []
        self.productos = []
        self.lineas_factura = []

        self.setup_ui()
        self.load_data()
        self.load_factura_data()

    def setup_ui(self):
        """Configurar la interfaz"""
        layout = QVBoxLayout(self)

        # Información de la factura
        info_group = QGroupBox("Información de la Factura")
        info_layout = QGridLayout(info_group)

        # Número de factura (no editable)
        self.numero_edit = QLineEdit()
        self.numero_edit.setText(self.factura_data['numero'])
        self.numero_edit.setReadOnly(True)

        # Fecha
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)

        # Cliente
        self.cliente_combo = QComboBox()

        # Estado de la factura
        self.estado_combo = QComboBox()

        info_layout.addWidget(QLabel("Número:"), 0, 0)
        info_layout.addWidget(self.numero_edit, 0, 1)
        info_layout.addWidget(QLabel("Fecha:"), 0, 2)
        info_layout.addWidget(self.fecha_edit, 0, 3)
        info_layout.addWidget(QLabel("Cliente:"), 1, 0)
        info_layout.addWidget(self.cliente_combo, 1, 1, 1, 2)
        info_layout.addWidget(QLabel("Estado:"), 1, 3)
        info_layout.addWidget(self.estado_combo, 1, 4)

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

        # Connecter les changements dans la table
        self.productos_table.itemChanged.connect(self.on_table_item_changed)

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

            # Charger les états de factures
            self.estados = invoice_status_manager.get_all_statuses()
            self.estado_combo.clear()
            for estado in self.estados:
                self.estado_combo.addItem(estado['nombre'], estado)

            # Charger les produits
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.logger.debug(f"[{timestamp}] EditarFacturaDialog - Llamando db.get_all_products()")
            self.productos = db.get_all_products()
            self.logger.debug(f"[{timestamp}] EditarFacturaDialog - Recibidos {len(self.productos)} productos")
            self.producto_combo.clear()
            self.producto_combo.addItem("Seleccionar producto...", None)
            for producto in self.productos:
                stock = producto.get('stock_actual', 0)
                from datetime import datetime
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                self.logger.debug(f"[{timestamp}] EditarFacturaDialog - Producto: {producto['nombre']}, Stock: {stock}, ID: {producto.get('id')}")
                self.producto_combo.addItem(
                    f"{producto['nombre']} - {producto['precio_venta']:.2f}€ (Stock: {stock})",
                    producto
                )

        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")

    def get_available_stock_for_product(self, producto_id):
        """Calcular el stock disponible para un producto considerando la factura actual"""
        try:
            # Obtener el stock actual del producto
            for producto in self.productos:
                if producto.get('id') == producto_id:
                    stock_actual = producto.get('stock_actual', 0)
                    break
            else:
                return 0

            # Buscar si este producto ya está en la factura original
            cantidad_original = 0
            for linea in self.factura_data.get('lineas', []):
                if linea.get('producto_id') == producto_id:
                    cantidad_original += linea.get('cantidad', 0)

            # El stock disponible es el stock actual + la cantidad que se va a liberar
            stock_disponible = stock_actual + cantidad_original

            self.logger.debug(f"Stock para producto {producto_id}: actual={stock_actual}, original={cantidad_original}, disponible={stock_disponible}")

            return stock_disponible

        except Exception as e:
            self.logger.error(f"Error calculando stock disponible: {e}")
            return 0

    def load_factura_data(self):
        """Cargar los datos de la factura a editar"""
        try:
            # Cargar fecha
            fecha_str = self.factura_data.get('fecha', '')
            if fecha_str:
                try:
                    # Convertir fecha string a QDate
                    date_parts = fecha_str.split('-')
                    if len(date_parts) == 3:
                        year, month, day = map(int, date_parts)
                        qdate = QDate(year, month, day)
                        self.fecha_edit.setDate(qdate)
                except Exception as e:
                    self.logger.warning(f"Error cargando fecha: {e}")
                    self.fecha_edit.setDate(QDate.currentDate())
            else:
                self.fecha_edit.setDate(QDate.currentDate())

            # Seleccionar cliente
            cliente_factura = self.factura_data.get('cliente', {})
            cliente_id = cliente_factura.get('id')
            if cliente_id:
                for i in range(self.cliente_combo.count()):
                    cliente_data = self.cliente_combo.itemData(i)
                    if cliente_data and cliente_data.get('id') == cliente_id:
                        self.cliente_combo.setCurrentIndex(i)
                        break

            # Seleccionar estado actual
            estado_actual = self.factura_data.get('estado', 'Borrador')
            for i in range(self.estado_combo.count()):
                estado_data = self.estado_combo.itemData(i)
                if estado_data and estado_data.get('nombre') == estado_actual:
                    self.estado_combo.setCurrentIndex(i)
                    break

            # Controlar permisos basados en el estado
            self.update_permissions()

            # Conectar cambio de estado para actualizar permisos
            self.estado_combo.currentIndexChanged.connect(self.update_permissions)

            # Cargar líneas de productos
            self.lineas_factura = []
            lineas_originales = self.factura_data.get('lineas', [])
            for linea in lineas_originales:
                linea_editada = {
                    'producto_id': linea.get('producto_id'),
                    'producto_nombre': linea.get('producto_nombre', 'Producto desconocido'),
                    'cantidad': linea.get('cantidad', 1),
                    'precio_unitario': linea.get('precio_unitario', 0.0),
                    'iva_aplicado': linea.get('iva_aplicado', 21.0),
                    'subtotal': linea.get('subtotal', 0.0),
                    'iva_amount': linea.get('iva_amount', 0.0),
                    'total': linea.get('total', 0.0)
                }
                self.lineas_factura.append(linea_editada)

            # Actualizar la tabla y los totales
            self.update_productos_table()
            self.calculate_totals()

        except Exception as e:
            self.logger.error(f"Error cargando datos de factura: {e}")

    def update_permissions(self):
        """Actualizar permisos basados en el estado seleccionado"""
        try:
            estado_data = self.estado_combo.currentData()
            if estado_data:
                permite_modificacion = estado_data.get('permite_modificacion', True)

                # Habilitar/deshabilitar campos según permisos
                self.fecha_edit.setEnabled(permite_modificacion)
                self.cliente_combo.setEnabled(permite_modificacion)
                self.productos_table.setEnabled(permite_modificacion)
                self.agregar_producto_btn.setEnabled(permite_modificacion)
                self.eliminar_producto_btn.setEnabled(permite_modificacion)

                # Actualizar estilo visual
                if not permite_modificacion:
                    self.setStyleSheet(self.styleSheet() + """
                        QDateEdit:disabled, QComboBox:disabled, QTableWidget:disabled {
                            background-color: #f5f5f5;
                            color: #666;
                        }
                    """)

        except Exception as e:
            self.logger.error(f"Error actualizando permisos: {e}")

    def agregar_producto(self):
        """Agregar producto a la factura"""
        producto_data = self.producto_combo.currentData()
        if not producto_data:
            return

        cantidad = self.cantidad_spin.value()
        producto_id = producto_data.get('id')

        # Calcular stock disponible considerando la factura actual
        stock_disponible = self.get_available_stock_for_product(producto_id)

        # Verificar stock disponible
        if cantidad > stock_disponible:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Stock insuficiente",
                              f"Stock disponible para edición: {stock_disponible}\nCantidad solicitada: {cantidad}")
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

    def on_table_item_changed(self, item):
        """Gestionar cambios en la tabla de productos"""
        if not item:
            return

        row = item.row()
        col = item.column()

        if row >= len(self.lineas_factura):
            return

        try:
            if col == 1:  # Cantidad
                nueva_cantidad = int(item.text())
                if nueva_cantidad <= 0:
                    item.setText(str(self.lineas_factura[row]['cantidad']))
                    return

                # Verificar stock disponible considerando la factura actual
                producto_id = self.lineas_factura[row]['producto_id']
                cantidad_original_linea = self.lineas_factura[row]['cantidad']

                # Calcular stock disponible para este producto
                stock_disponible = self.get_available_stock_for_product(producto_id)

                # El stock disponible ya incluye la cantidad original que se va a liberar
                # Solo necesitamos verificar si la nueva cantidad es mayor al stock disponible
                if nueva_cantidad > stock_disponible:
                    from PyQt5.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Stock insuficiente",
                                      f"Stock disponible para edición: {stock_disponible}\n"
                                      f"Cantidad solicitada: {nueva_cantidad}")
                    item.setText(str(self.lineas_factura[row]['cantidad']))
                    return

                self.lineas_factura[row]['cantidad'] = nueva_cantidad
                self.recalcular_linea(row)

            elif col == 3:  # IVA
                nuevo_iva = float(item.text().replace('%', ''))
                if nuevo_iva < 0 or nuevo_iva > 100:
                    item.setText(f"{self.lineas_factura[row]['iva_aplicado']:.1f}")
                    return

                self.lineas_factura[row]['iva_aplicado'] = nuevo_iva
                self.recalcular_linea(row)

        except ValueError:
            # Restaurer la valeur précédente en cas d'erreur
            if col == 1:
                item.setText(str(self.lineas_factura[row]['cantidad']))
            elif col == 3:
                item.setText(f"{self.lineas_factura[row]['iva_aplicado']:.1f}")

    def recalcular_linea(self, row):
        """Recalculer les totaux d'une ligne"""
        linea = self.lineas_factura[row]

        # Recalculer les montants
        subtotal = linea['precio_unitario'] * linea['cantidad']
        iva_amount = subtotal * (linea['iva_aplicado'] / 100)
        total = subtotal + iva_amount

        # Mettre à jour la ligne
        linea['subtotal'] = subtotal
        linea['iva_amount'] = iva_amount
        linea['total'] = total

        # Mettre à jour l'affichage
        self.productos_table.setItem(row, 4, QTableWidgetItem(f"{total:.2f}€"))

        # Recalculer les totaux généraux
        self.calculate_totals()

    def update_productos_table(self):
        """Actualizar tabla de productos"""
        self.productos_table.setRowCount(len(self.lineas_factura))

        for row, linea in enumerate(self.lineas_factura):
            # Producto (no editable)
            item_producto = QTableWidgetItem(linea['producto_nombre'])
            item_producto.setFlags(item_producto.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 0, item_producto)

            # Cantidad (editable)
            item_cantidad = QTableWidgetItem(str(linea['cantidad']))
            self.productos_table.setItem(row, 1, item_cantidad)

            # Precio (no editable)
            item_precio = QTableWidgetItem(f"{linea['precio_unitario']:.2f}€")
            item_precio.setFlags(item_precio.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 2, item_precio)

            # IVA (editable)
            item_iva = QTableWidgetItem(f"{linea['iva_aplicado']:.1f}")
            self.productos_table.setItem(row, 3, item_iva)

            # Total (no editable)
            item_total = QTableWidgetItem(f"{linea['total']:.2f}€")
            item_total.setFlags(item_total.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 4, item_total)

            # Botón eliminar centrado
            eliminar_btn = QPushButton("🗑️")
            eliminar_btn.setFixedSize(40, 30)
            eliminar_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)
            eliminar_btn.clicked.connect(lambda checked, r=row: self.eliminar_linea(r))

            # Crear un widget contenedor para centrar el botón
            container_widget = QWidget()
            container_layout = QHBoxLayout(container_widget)
            container_layout.addWidget(eliminar_btn)
            container_layout.setAlignment(Qt.AlignCenter)
            container_layout.setContentsMargins(5, 2, 5, 2)

            self.productos_table.setCellWidget(row, 5, container_widget)

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
        """Guardar los cambios en la factura"""
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

            # Obtener estado seleccionado
            estado_data = self.estado_combo.currentData()
            estado_nombre = estado_data.get('nombre', 'Borrador') if estado_data else 'Borrador'

            factura_data = {
                'id': self.factura_data['id'],  # ID de la factura existente
                'numero': self.numero_edit.text(),
                'fecha': self.fecha_edit.date().toString('yyyy-MM-dd'),
                'cliente': cliente_data,
                'estado': estado_nombre,
                'subtotal': subtotal,
                'iva_total': iva_total,
                'total': total,
                'estado': self.factura_data.get('estado', 'Borrador'),
                'lineas': self.lineas_factura
            }

            # Actualizar en la base de datos
            success = db.update_invoice(factura_data)

            from PyQt5.QtWidgets import QMessageBox
            if success:
                QMessageBox.information(self, "Éxito", f"Factura {self.numero_edit.text()} actualizada correctamente")
                self.accept()  # Ferme la fenêtre d'édition et retourne à la fenêtre des factures
            else:
                QMessageBox.critical(self, "Error", "No se pudo actualizar la factura")

        except Exception as e:
            self.logger.error(f"Error actualizando factura: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al actualizar la factura: {str(e)}")


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
