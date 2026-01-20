# -*- coding: utf-8 -*-
"""
Fenêtre d'édition/création de facture unifiée
Gère à la fois la création et l'édition de factures
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QLineEdit, QDateEdit, QComboBox, QTableWidget, QTableWidgetItem,
                             QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox, QMessageBox, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QDate, QTimer
from PyQt5.QtGui import QFont
from ui.client_autocomplete_widget import ClientAutoCompleteWidget, ClientDetailsWidget
from ui.product_autocomplete_widget import ProductAutoCompleteWidget
from services.factura_service import FacturaService
from services.cliente_service import ClienteService
from services.producto_service import ProductoService
from utils.logger import get_logger
from utils.dialog_simple_foreground import SimpleDialogForegroundMixin
from utils.invoice_status_manager import invoice_status_manager
from datetime import datetime


class FacturaEditWindow(QDialog, SimpleDialogForegroundMixin):
    """Fenêtre unifiée pour créer ou éditer une facture"""
    
    # Signal émis quand une facture est sauvegardée
    factura_saved = Signal(int)  # ID de la facture sauvegardée
    
    def __init__(self, parent=None, database_instance=None, factura_data=None):
        """
        Initialise la fenêtre d'édition/création de facture
        
        Args:
            parent: Widget parent
            database_instance: Instance de la base de données
            factura_data: Données de la facture (None pour création, dict pour édition)
        """
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.factura_data = factura_data
        self.database = database_instance
        
        # Mode création ou édition
        self.is_edit_mode = factura_data is not None
        
        # Titre de la fenêtre
        if self.is_edit_mode:
            self.setWindowTitle(f"Editar Factura {factura_data['numero']}")
        else:
            self.setWindowTitle("Nueva Factura")
        
        self.resize(900, 700)
        
        # Services métier
        db_path = database_instance.db_path if hasattr(database_instance, 'db_path') else None
        self.factura_service = FacturaService(db_path)
        self.cliente_service = ClienteService(db_path)
        self.producto_service = ProductoService(db_path)
        
        # Variables
        self.clientes = []
        self.productos = []
        self.lineas_factura = []
        
        # Configuration de l'interface
        self.setup_ui()
        
        # Charger les données
        self.load_data()
        
        # Si mode édition, charger les données de la facture
        if self.is_edit_mode:
            self.load_factura_data()
        else:
            # Mode création : générer le numéro de facture
            self.generate_factura_number()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Section 1: Informations de la facture
        info_group = self.create_info_section()
        layout.addWidget(info_group)
        
        # Section 2: Client
        client_group = self.create_client_section()
        layout.addWidget(client_group)
        
        # Section 3: Produits
        products_group = self.create_products_section()
        layout.addWidget(products_group)
        
        # Section 4: Totaux
        totals_group = self.create_totals_section()
        layout.addWidget(totals_group)
        
        # Section 5: Boutons
        buttons_layout = self.create_buttons_section()
        layout.addLayout(buttons_layout)
    
    def create_info_section(self):
        """Crée la section d'informations de la facture"""
        info_group = QGroupBox("Información de la Factura")
        info_layout = QGridLayout(info_group)
        
        # Numéro de facture (lecture seule en mode édition)
        self.numero_edit = QLineEdit()
        if self.is_edit_mode:
            self.numero_edit.setReadOnly(True)
        
        # Date
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setCalendarPopup(True)
        self.fecha_edit.setDate(QDate.currentDate())
        
        # État
        self.estado_combo = QComboBox()
        
        info_layout.addWidget(QLabel("Número:"), 0, 0)
        info_layout.addWidget(self.numero_edit, 0, 1)
        info_layout.addWidget(QLabel("Fecha:"), 0, 2)
        info_layout.addWidget(self.fecha_edit, 0, 3)
        info_layout.addWidget(QLabel("Estado:"), 1, 0)
        info_layout.addWidget(self.estado_combo, 1, 1, 1, 3)
        
        return info_group
    
    def create_client_section(self):
        """Crée la section client"""
        client_group = QGroupBox("Cliente")
        client_layout = QVBoxLayout(client_group)
        
        # Widget d'autocomplétion pour le client
        client_input_layout = QHBoxLayout()
        client_input_layout.addWidget(QLabel("Cliente:"))
        
        self.cliente_autocomplete = ClientAutoCompleteWidget()
        client_input_layout.addWidget(self.cliente_autocomplete, 1)
        
        client_layout.addLayout(client_input_layout)
        
        # Widget pour les détails du client
        self.client_details = ClientDetailsWidget()
        client_layout.addWidget(self.client_details)

        # Connecter les signaux
        self.cliente_autocomplete.client_selected.connect(self.on_client_selected)
        self.cliente_autocomplete.client_created.connect(self.on_client_created)
        self.cliente_autocomplete.client_changed.connect(self.on_client_changed)
        self.client_details.client_updated.connect(self.on_client_updated)
        self.client_details.client_saved.connect(self.on_client_saved)

        return client_group

    def create_products_section(self):
        """Crée la section produits"""
        products_group = QGroupBox("Productos")
        products_layout = QVBoxLayout(products_group)

        # Sélecteur de produits
        selector_layout = QHBoxLayout()

        self.producto_autocomplete = ProductAutoCompleteWidget()
        self.cantidad_spin = QSpinBox()
        self.cantidad_spin.setMinimum(1)
        self.cantidad_spin.setMaximum(999)
        self.cantidad_spin.setValue(1)

        self.agregar_btn = QPushButton("➕ Agregar")
        self.agregar_btn.clicked.connect(self.agregar_producto)

        selector_layout.addWidget(QLabel("Producto:"))
        selector_layout.addWidget(self.producto_autocomplete, 2)
        selector_layout.addWidget(QLabel("Cantidad:"))
        selector_layout.addWidget(self.cantidad_spin)
        selector_layout.addWidget(self.agregar_btn)

        products_layout.addLayout(selector_layout)

        # Table des produits
        self.productos_table = QTableWidget()
        headers = ["Producto", "Cantidad", "Precio", "IVA", "Total", ""]
        self.productos_table.setColumnCount(len(headers))
        self.productos_table.setHorizontalHeaderLabels(headers)
        self.productos_table.horizontalHeader().setStretchLastSection(True)
        self.productos_table.itemChanged.connect(self.on_table_item_changed)

        products_layout.addWidget(self.productos_table)

        # Connecter les signaux du produit autocomplete
        self.producto_autocomplete.product_selected.connect(self.on_product_selected)

        return products_group

    def create_totals_section(self):
        """Crée la section des totaux"""
        totals_group = QGroupBox("Totales")
        totals_layout = QGridLayout(totals_group)

        self.subtotal_label = QLabel("0.00€")
        self.iva_label = QLabel("0.00€")
        self.total_label = QLabel("0.00€")
        self.total_label.setFont(QFont("Arial", 14, QFont.Bold))

        totals_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        totals_layout.addWidget(self.subtotal_label, 0, 1)
        totals_layout.addWidget(QLabel("IVA:"), 1, 0)
        totals_layout.addWidget(self.iva_label, 1, 1)
        totals_layout.addWidget(QLabel("TOTAL:"), 2, 0)
        totals_layout.addWidget(self.total_label, 2, 1)

        return totals_group

    def create_buttons_section(self):
        """Crée la section des boutons"""
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.clicked.connect(self.reject)

        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.clicked.connect(self.save_factura)
        self.guardar_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        buttons_layout.addWidget(self.cancelar_btn)
        buttons_layout.addWidget(self.guardar_btn)

        return buttons_layout

    def load_data(self):
        """Charge les données nécessaires"""
        try:
            # Charger les états de factures
            self.estados = invoice_status_manager.get_all_statuses()
            self.estado_combo.clear()
            for estado in self.estados:
                self.estado_combo.addItem(estado['nombre'], estado)

            # Charger les produits
            self.productos = self.producto_service.get_all_productos()
            self.producto_autocomplete.load_products(self.productos)

            self.logger.info(f"Datos cargados: {len(self.productos)} productos")

        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")

    def generate_factura_number(self):
        """Génère un nouveau numéro de facture"""
        try:
            numero = self.factura_service.generate_factura_number()
            self.numero_edit.setText(numero)
            self.logger.info(f"Número de factura generado: {numero}")
        except Exception as e:
            self.logger.error(f"Error generando número de factura: {e}")
            # Utiliser un timestamp en cas d'erreur
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            self.numero_edit.setText(f"FAC-{timestamp}")

    def load_factura_data(self):
        """Charge les données de la facture en mode édition"""
        try:
            # Charger le numéro
            self.numero_edit.setText(self.factura_data['numero'])

            # Charger la date
            fecha_str = self.factura_data.get('fecha', '')
            if fecha_str:
                try:
                    date_parts = fecha_str.split('-')
                    if len(date_parts) == 3:
                        year, month, day = map(int, date_parts)
                        qdate = QDate(year, month, day)
                        self.fecha_edit.setDate(qdate)
                except Exception as e:
                    self.logger.warning(f"Error cargando fecha: {e}")
                    self.fecha_edit.setDate(QDate.currentDate())

            # Charger le client
            cliente_factura = self.factura_data.get('cliente', {})
            if cliente_factura:
                self.cliente_autocomplete.set_client(cliente_factura)

            # Sélectionner l'état
            estado_actual = self.factura_data.get('estado', 'Borrador')
            for i in range(self.estado_combo.count()):
                estado_data = self.estado_combo.itemData(i)
                if estado_data and estado_data.get('nombre') == estado_actual:
                    self.estado_combo.setCurrentIndex(i)
                    break

            # Charger les lignes de produits
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

            # Actualiser l'affichage
            self.update_productos_table()
            self.calculate_totals()

            self.logger.info(f"Factura cargada: {self.factura_data['numero']}")

        except Exception as e:
            self.logger.error(f"Error cargando datos de factura: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar la factura: {str(e)}")

    # Gestionnaires d'événements pour le client
    def on_client_selected(self, client):
        """Gérer la sélection d'un client existant"""
        self.logger.info(f"Cliente seleccionado: {client.get('nombre', '')} (ID: {client.get('id', 'N/A')})")
        self.client_details.show_client_details(client)

    def on_client_created(self, client):
        """Gérer la création d'un nouveau client"""
        self.logger.info(f"Nuevo cliente creado: {client.get('nombre', '')}")
        self.client_details.show_client_details(client)

    def on_client_changed(self):
        """Gérer le changement de client"""
        current_client = self.cliente_autocomplete.get_current_client()
        if current_client:
            self.client_details.show_client_details(current_client)
        else:
            self.client_details.clear()

    def on_client_updated(self, client):
        """Gérer la mise à jour des données client"""
        self.logger.info(f"Datos del cliente actualizados: {client.get('nombre', '')}")

    def on_client_saved(self, client):
        """Gérer la sauvegarde d'un client"""
        try:
            self.logger.info(f"Guardando cliente: {client.get('nombre', '')}")

            # Si c'est un nouveau client, le créer
            if client.get('is_new', False):
                # Retirer le flag is_new avant de sauvegarder
                client_to_save = {k: v for k, v in client.items() if k != 'is_new'}
                cliente_id = self.cliente_service.create_cliente(client_to_save)
                client['id'] = cliente_id
                client['is_new'] = False
                self.logger.info(f"Cliente creado con ID: {cliente_id}")
            else:
                # Mettre à jour le client existant
                self.cliente_service.update_cliente(client)
                self.logger.info(f"Cliente actualizado: {client.get('id')}")

            # Mettre à jour le widget
            self.cliente_autocomplete.set_client(client)
            QMessageBox.information(self, "Éxito", "Cliente guardado correctamente")

        except Exception as e:
            self.logger.error(f"Error guardando cliente: {e}")
            QMessageBox.critical(self, "Error", f"Error al guardar el cliente: {str(e)}")

    # Gestionnaires d'événements pour les produits
    def on_product_selected(self, product):
        """Gérer la sélection d'un produit"""
        self.logger.info(f"Producto seleccionado: {product.get('nombre', '')}")

    def agregar_producto(self):
        """Ajouter un produit à la facture"""
        producto_data = self.producto_autocomplete.get_current_product()
        if not producto_data:
            QMessageBox.warning(self, "Validación", "Seleccione un producto")
            return

        cantidad = self.cantidad_spin.value()
        producto_id = producto_data.get('id')

        # Vérifier le stock si le produit gère le stock
        sin_stock = producto_data.get('sin_stock', 0)
        if not sin_stock:
            stock_actual = producto_data.get('stock_actual', 0)
            if cantidad > stock_actual:
                reply = QMessageBox.question(
                    self, "Stock insuficiente",
                    f"Stock disponible: {stock_actual}\n"
                    f"Cantidad solicitada: {cantidad}\n\n"
                    f"¿Desea continuar con stock negativo?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return

        # Calculer les prix
        precio_unitario = producto_data['precio_venta']
        iva_rate = producto_data.get('iva_recomendado', 21.0) / 100
        subtotal = precio_unitario * cantidad
        iva_amount = subtotal * iva_rate
        total = subtotal + iva_amount

        # Construire le nom du produit avec la taille si elle existe
        producto_nombre = producto_data['nombre']
        talla = producto_data.get('talla', '')
        if talla and talla.strip():
            producto_nombre = f"{producto_nombre} - {talla}"

        # Ajouter à la liste
        linea = {
            'producto_id': producto_data['id'],
            'producto_nombre': producto_nombre,
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

        # Réinitialiser la sélection
        self.producto_autocomplete.clear_product()
        self.cantidad_spin.setValue(1)

    def on_table_item_changed(self, item):
        """Gérer les changements dans la table de produits"""
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
        """Actualiser la table des produits"""
        self.productos_table.setRowCount(len(self.lineas_factura))

        for row, linea in enumerate(self.lineas_factura):
            # Producto (non éditable)
            item_producto = QTableWidgetItem(linea['producto_nombre'])
            item_producto.setFlags(item_producto.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 0, item_producto)

            # Cantidad (éditable)
            item_cantidad = QTableWidgetItem(str(linea['cantidad']))
            self.productos_table.setItem(row, 1, item_cantidad)

            # Precio (non éditable)
            item_precio = QTableWidgetItem(f"{linea['precio_unitario']:.2f}€")
            item_precio.setFlags(item_precio.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 2, item_precio)

            # IVA (éditable)
            item_iva = QTableWidgetItem(f"{linea['iva_aplicado']:.1f}")
            self.productos_table.setItem(row, 3, item_iva)

            # Total (non éditable)
            item_total = QTableWidgetItem(f"{linea['total']:.2f}€")
            item_total.setFlags(item_total.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 4, item_total)

            # Bouton supprimer
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
            """)
            eliminar_btn.clicked.connect(lambda checked, r=row: self.eliminar_linea(r))

            # Conteneur pour centrer le bouton
            container_widget = QWidget()
            container_layout = QHBoxLayout(container_widget)
            container_layout.addWidget(eliminar_btn)
            container_layout.setAlignment(Qt.AlignCenter)
            container_layout.setContentsMargins(5, 2, 5, 2)

            self.productos_table.setCellWidget(row, 5, container_widget)

    def eliminar_linea(self, row):
        """Supprimer une ligne de la facture"""
        if 0 <= row < len(self.lineas_factura):
            del self.lineas_factura[row]
            self.update_productos_table()
            self.calculate_totals()

    def calculate_totals(self):
        """Calculer les totaux de la facture"""
        subtotal = sum(linea['subtotal'] for linea in self.lineas_factura)
        iva_total = sum(linea['iva_amount'] for linea in self.lineas_factura)
        total = subtotal + iva_total

        self.subtotal_label.setText(f"{subtotal:.2f}€")
        self.iva_label.setText(f"{iva_total:.2f}€")
        self.total_label.setText(f"{total:.2f}€")

    def save_factura(self):
        """Sauvegarder la facture (création ou mise à jour)"""
        try:
            # Validation 1: Vérifier le client
            current_client = self.cliente_autocomplete.get_current_client()
            if not current_client:
                QMessageBox.warning(self, "Validación", "Seleccione un cliente")
                return

            # Si c'est un nouveau client, le sauvegarder d'abord
            if current_client.get('is_new', False):
                try:
                    client_to_save = {k: v for k, v in current_client.items() if k != 'is_new'}
                    cliente_id = self.cliente_service.create_cliente(client_to_save)
                    current_client['id'] = cliente_id
                    current_client['is_new'] = False
                    self.logger.info(f"Cliente creado automáticamente con ID: {cliente_id}")
                except Exception as e:
                    self.logger.error(f"Error creando cliente: {e}")
                    QMessageBox.critical(self, "Error", f"Error al crear el cliente: {str(e)}")
                    return

            # Validation 2: Vérifier les produits
            if not self.lineas_factura:
                QMessageBox.warning(self, "Validación", "Agregue al menos un producto")
                return

            # Calculer les totaux
            subtotal = sum(linea['subtotal'] for linea in self.lineas_factura)
            iva_total = sum(linea['iva_amount'] for linea in self.lineas_factura)
            total = subtotal + iva_total

            # Obtenir l'état sélectionné
            estado_data = self.estado_combo.currentData()
            estado_nombre = estado_data.get('nombre', 'Borrador') if estado_data else 'Borrador'

            # Préparer les données de la facture
            factura_data = {
                'numero': self.numero_edit.text(),
                'fecha': self.fecha_edit.date().toString('yyyy-MM-dd'),
                'cliente': current_client,
                'estado': estado_nombre,
                'subtotal': subtotal,
                'iva_total': iva_total,
                'total': total,
                'lineas': self.lineas_factura
            }

            # Mode édition : ajouter l'ID
            if self.is_edit_mode:
                factura_data['id'] = self.factura_data['id']

            # Sauvegarder via le service
            if self.is_edit_mode:
                # Mise à jour
                success = self.factura_service.update_factura(factura_data)
                if success:
                    # Émettre le signal et fermer AVANT d'afficher le message
                    factura_id = self.factura_data['id']
                    self.factura_saved.emit(factura_id)
                    self.close()

                    # Message de succès après fermeture (sera affiché sur la fenêtre parent)
                    QMessageBox.information(
                        self.parent(), "Éxito",
                        f"Factura {self.numero_edit.text()} actualizada correctamente"
                    )
                else:
                    QMessageBox.critical(self, "Error", "No se pudo actualizar la factura")
            else:
                # Création
                factura_id = self.factura_service.create_factura(factura_data)

                # Émettre le signal et fermer AVANT d'afficher le message
                self.factura_saved.emit(factura_id)
                self.close()

                # Message de succès après fermeture (sera affiché sur la fenêtre parent)
                QMessageBox.information(
                    self.parent(), "Éxito",
                    f"Factura {self.numero_edit.text()} creada correctamente"
                )

        except Exception as e:
            self.logger.error(f"Error guardando factura: {e}")
            QMessageBox.critical(self, "Error", f"Error al guardar la factura: {str(e)}")

