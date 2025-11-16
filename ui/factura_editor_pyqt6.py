# -*- coding: utf-8 -*-
"""
Fenêtre d'édition/création de factures - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QDateEdit, QDoubleSpinBox, QTextEdit, QGroupBox,
    QSplitter, QSpinBox, QFrame, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from ui.base_pyqt6_window import BasePyQt6Window
from ui.widgets.client_autocomplete import ClientAutoCompleteWidget
from database.database import db
from utils.logger import get_logger
from utils.pdf_generator import pdf_generator
from datetime import datetime
import uuid
import os

class FacturaEditorPyQt6Window(BasePyQt6Window):
    """Fenêtre d'édition/création de factures en PyQt6 natif"""
    
    # Signal émis quand une facture est sauvegardée
    factura_saved = pyqtSignal()
    
    def __init__(self, parent=None, factura_data=None):
        # Initialiser les attributs avant d'appeler super().__init__
        self.logger = get_logger("factura_editor_pyqt6")
        self.factura_data = factura_data
        self.is_editing = factura_data is not None
        self.items_factura = []

        # Données de clients et produits
        self.clientes_data = []
        self.productos_data = []

        # Maintenant appeler super().__init__ qui va appeler setup_ui()
        super().__init__(parent, "Editor de Facturas", 1200, 950)  # Augmenté de 900 à 950 pixels pour les lignes plus hautes

        self.logger.info(f"Inicializando editor de facturas - Modo: {'Edición' if self.is_editing else 'Creación'}")
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre dynamique
        title = "Editar Factura" if self.is_editing else "Nueva Factura"
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_layout.addWidget(main_splitter)

        # Partie supérieure - Informations de la facture
        self.create_invoice_info_panel(main_splitter)

        # Partie inférieure - Lignes de la facture
        self.create_invoice_items_panel(main_splitter)

        # Ajuster les proportions du splitter (25% info, 75% lignes)
        main_splitter.setSizes([220, 680])  # Plus d'espace pour les lignes plus hautes
        
        # Boutons d'action
        self.create_action_buttons()
        
        # Charger les données
        self.load_initial_data()
    
    def create_invoice_info_panel(self, parent):
        """Crée le panneau d'informations de la facture"""
        info_widget = QWidget()
        info_layout = QHBoxLayout(info_widget)
        
        # Informations générales
        general_group = QGroupBox("Información General")
        general_layout = QGridLayout(general_group)
        
        # Numéro de facture
        general_layout.addWidget(QLabel("Número:"), 0, 0)
        self.numero_edit = QLineEdit()
        self.numero_edit.setReadOnly(True)
        if not self.is_editing:
            self.numero_edit.setText(self.generate_invoice_number())
        general_layout.addWidget(self.numero_edit, 0, 1)
        
        # Date
        general_layout.addWidget(QLabel("Fecha:"), 1, 0)
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        general_layout.addWidget(self.fecha_edit, 1, 1)
        
        # Date d'échéance
        general_layout.addWidget(QLabel("Vencimiento:"), 2, 0)
        self.vencimiento_edit = QDateEdit()
        self.vencimiento_edit.setDate(QDate.currentDate().addDays(30))
        self.vencimiento_edit.setCalendarPopup(True)
        general_layout.addWidget(self.vencimiento_edit, 2, 1)
        
        info_layout.addWidget(general_group)
        
        # Informations client
        client_group = QGroupBox("Cliente")
        client_layout = QGridLayout(client_group)
        
        # Sélection client avec autocomplétion
        client_layout.addWidget(QLabel("Cliente:"), 0, 0)
        self.cliente_autocomplete = ClientAutoCompleteWidget()
        self.cliente_autocomplete.client_selected.connect(self.on_client_selected)
        self.cliente_autocomplete.client_created.connect(self.on_client_created)

        # S'assurer que le widget peut recevoir le focus
        self.cliente_autocomplete.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        client_layout.addWidget(self.cliente_autocomplete, 0, 1)

        # Bouton pour créer un nouveau client
        self.new_client_btn = QPushButton("➕ Nuevo")
        self.new_client_btn.setMaximumWidth(80)
        self.new_client_btn.clicked.connect(self.create_new_client)
        client_layout.addWidget(self.new_client_btn, 0, 2)
        
        # Informations client (lecture seule)
        client_layout.addWidget(QLabel("NIF/CIF:"), 1, 0)
        self.cliente_nif_label = QLabel("-")
        client_layout.addWidget(self.cliente_nif_label, 1, 1)
        
        client_layout.addWidget(QLabel("Dirección:"), 2, 0)
        self.cliente_direccion_label = QLabel("-")
        self.cliente_direccion_label.setWordWrap(True)
        client_layout.addWidget(self.cliente_direccion_label, 2, 1)
        
        info_layout.addWidget(client_group)
        
        # Totaux
        totals_group = QGroupBox("Totales")
        totals_layout = QGridLayout(totals_group)
        
        totals_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        self.subtotal_label = QLabel("0.00 €")
        self.subtotal_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        totals_layout.addWidget(self.subtotal_label, 0, 1)
        
        totals_layout.addWidget(QLabel("IVA:"), 1, 0)
        self.iva_label = QLabel("0.00 €")
        self.iva_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        totals_layout.addWidget(self.iva_label, 1, 1)
        
        totals_layout.addWidget(QLabel("TOTAL:"), 2, 0)
        self.total_label = QLabel("0.00 €")
        self.total_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #0078d4;")
        totals_layout.addWidget(self.total_label, 2, 1)
        
        info_layout.addWidget(totals_group)
        
        parent.addWidget(info_widget)
    
    def create_invoice_items_panel(self, parent):
        """Crée le panneau des lignes de facture"""
        items_widget = QWidget()
        items_layout = QVBoxLayout(items_widget)
        
        # Titre et boutons
        header_layout = QHBoxLayout()
        
        items_title = QLabel("Líneas de Factura")
        items_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        header_layout.addWidget(items_title)
        
        header_layout.addStretch()
        
        add_item_btn = QPushButton("➕ Añadir Línea")
        add_item_btn.clicked.connect(self.add_invoice_item)
        header_layout.addWidget(add_item_btn)
        
        remove_item_btn = QPushButton("➖ Eliminar Línea")
        remove_item_btn.clicked.connect(self.remove_invoice_item)
        header_layout.addWidget(remove_item_btn)
        
        items_layout.addLayout(header_layout)
        
        # Table des lignes
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7)
        self.items_table.setHorizontalHeaderLabels([
            "Producto", "Descripción", "Cantidad", "Precio Unit.", "Descuento %", "IVA %", "Total"
        ])
        
        # Configuration de la table
        header = self.items_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        
        self.items_table.setAlternatingRowColors(True)
        self.items_table.setMinimumHeight(400)  # Augmenté de 350 à 400 pixels pour les lignes plus hautes

        # Hauteur de ligne plus confortable
        self.items_table.verticalHeader().setDefaultSectionSize(45)  # 45 pixels par ligne (augmenté de 35 à 45)
        
        items_layout.addWidget(self.items_table)

        # Bouton pour ajouter une ligne
        add_line_btn = QPushButton("➕ Añadir línea")
        add_line_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        add_line_btn.clicked.connect(self.add_invoice_item)
        items_layout.addWidget(add_line_btn)

        parent.addWidget(items_widget)
    
    def create_action_buttons(self):
        """Crée les boutons d'action"""
        buttons_config = [
            ("💾 Guardar", self.save_invoice, "success"),
            ("🖨️ Vista Previa", self.preview_invoice, "primary"),
            ("📄 Imprimir", self.print_invoice, "secondary"),
            ("❌ Cancelar", self.close, "secondary")
        ]
        
        button_layout = self.create_button_layout(buttons_config)
        self.main_layout.addLayout(button_layout)
    
    def load_initial_data(self):
        """Charge les données initiales"""
        try:
            # Charger les clients
            self.load_clients()
            
            # Charger les produits
            self.load_products()
            
            # Si on édite une facture, charger ses données
            if self.is_editing and self.factura_data:
                self.load_invoice_data()
            else:
                # Ajouter une ligne vide pour commencer
                self.add_invoice_item()

            # Donner le focus au champ client pour faciliter la saisie
            if hasattr(self, 'cliente_autocomplete'):
                self.cliente_autocomplete.setFocus()
            
        except Exception as e:
            self.logger.error(f"Error cargando datos iniciales: {e}")
            self.show_error("Error", f"Error al cargar datos: {e}")
    
    def load_clients(self):
        """Charge la liste des clients"""
        try:
            # Charger les clients depuis la base de données
            db_clients = db.get_all_clients()

            # Si pas de clients en base, créer quelques clients de démo
            if not db_clients:
                demo_clients = [
                    {"nombre": "Juan Pérez", "nif": "12345678A", "direccion": "Calle Mayor, 1\n28001 Madrid", "telefono": "91 123 45 67", "email": "juan@email.com"},
                    {"nombre": "María García", "nif": "87654321B", "direccion": "Avenida Principal, 25\n28002 Madrid", "telefono": "91 234 56 78", "email": "maria@email.com"},
                    {"nombre": "Empresa ABC S.L.", "nif": "A12345678", "direccion": "Polígono Industrial, 15\n28003 Madrid", "telefono": "91 345 67 89", "email": "info@abc.com"},
                ]

                # Créer les clients de démo en base
                for demo_client in demo_clients:
                    try:
                        client_id = db.add_client(demo_client)
                        demo_client['id'] = client_id
                        self.logger.info(f"Cliente de demo creado: {demo_client['nombre']}")
                    except Exception as e:
                        self.logger.error(f"Error creando cliente de demo: {e}")

                self.clientes_data = demo_clients
            else:
                self.clientes_data = db_clients

            # Charger les clients dans le widget d'autocomplétion
            self.cliente_autocomplete.load_clients(self.clientes_data)

            self.logger.info(f"Cargados {len(self.clientes_data)} clientes")

        except Exception as e:
            self.logger.error(f"Error cargando clientes: {e}")
            # Fallback con clientes de demo locales
            demo_clients = [
                {"id": 1, "nombre": "Juan Pérez", "nif": "12345678A", "direccion": "Calle Mayor, 1\n28001 Madrid"},
                {"id": 2, "nombre": "María García", "nif": "87654321B", "direccion": "Avenida Principal, 25\n28002 Madrid"},
            ]
            self.clientes_data = demo_clients
            self.cliente_autocomplete.load_clients(demo_clients)
    
    def load_products(self):
        """Charge la liste des produits"""
        try:
            # Utiliser les produits de la base de données
            self.productos_data = db.get_all_products()
            
            if not self.productos_data:
                # Données de démo si pas de produits en base
                self.productos_data = [
                    {"id": 1, "nombre": "Producto A", "referencia": "P001", "precio_venta": 25.00, "iva_recomendado": 21.0},
                    {"id": 2, "nombre": "Producto B", "referencia": "P002", "precio_venta": 35.50, "iva_recomendado": 21.0},
                    {"id": 3, "nombre": "Servicio C", "referencia": "S001", "precio_venta": 50.00, "iva_recomendado": 21.0},
                ]
            
            self.logger.info(f"Cargados {len(self.productos_data)} productos")
            
        except Exception as e:
            self.logger.error(f"Error cargando productos: {e}")
            self.productos_data = []

    def generate_invoice_number(self):
        """Génère un numéro de facture unique"""
        try:
            # Utiliser la méthode de la base de données si disponible
            if hasattr(db, 'get_next_invoice_number'):
                return db.get_next_invoice_number()
            else:
                # Générer un numéro basé sur la date et l'heure
                now = datetime.now()
                return f"F-{now.year}-{now.month:02d}-{now.day:02d}-{now.hour:02d}{now.minute:02d}"
        except Exception as e:
            self.logger.error(f"Error generando número de factura: {e}")
            return f"F-{datetime.now().strftime('%Y%m%d%H%M')}"

    def on_client_selected(self, client_data):
        """Gère la sélection d'un client existant"""
        if client_data:
            # Récupérer les données du client
            nif = client_data.get("nif", "").strip()
            direccion = client_data.get("direccion", "").strip()
            email = client_data.get("email", "").strip()
            telefono = client_data.get("telefono", "").strip()

            # Afficher les informations (ou "-" si vide)
            self.cliente_nif_label.setText(nif if nif else "-")
            self.cliente_direccion_label.setText(direccion if direccion else "-")

            # Log détaillé pour diagnostic
            self.logger.info(f"Cliente seleccionado: {client_data.get('nombre', 'N/A')} (ID: {client_data.get('id', 'N/A')})")
            self.logger.info(f"  • NIF: '{nif}' {'(vacío)' if not nif else ''}")
            self.logger.info(f"  • Dirección: '{direccion}' {'(vacía)' if not direccion else ''}")
            self.logger.info(f"  • Email: '{email}' {'(vacío)' if not email else ''}")
            self.logger.info(f"  • Teléfono: '{telefono}' {'(vacío)' if not telefono else ''}")
        else:
            self.cliente_nif_label.setText("-")
            self.cliente_direccion_label.setText("-")
            self.logger.warning("Cliente seleccionado sin datos")

    def on_client_created(self, client_data):
        """Gère la création d'un nouveau client"""
        if client_data:
            self.cliente_nif_label.setText(client_data.get("nif", "-"))
            self.cliente_direccion_label.setText(client_data.get("direccion", "-"))
            self.logger.info(f"Nuevo cliente creado: {client_data.get('nombre', 'N/A')}")

            # Sauvegarder immédiatement le nouveau client en base de données
            self.save_new_client_to_database(client_data)

    def create_new_client(self):
        """Ouvre le dialogue de création de nouveau client"""
        new_client = self.cliente_autocomplete.create_new_client_dialog()
        if new_client:
            self.show_info("Cliente Creado", f"Nuevo cliente creado:\n{new_client['nombre']}")

    def save_new_client_to_database(self, client_data):
        """Sauvegarde un nouveau client en base de données"""
        try:
            # Sauvegarder le client en base de données
            client_id = db.add_client(client_data)
            client_data['id'] = client_id

            # Ajouter à la liste locale pour l'autocomplétion
            self.clientes_data.append(client_data)
            self.cliente_autocomplete.load_clients(self.clientes_data)

            self.logger.info(f"Cliente guardado en base de datos con ID: {client_id}")
            return client_id

        except Exception as e:
            self.logger.error(f"Error guardando cliente: {e}")
            # Simuler un ID pour continuer
            client_data['id'] = len(self.clientes_data) + 1000  # ID temporaire
            self.clientes_data.append(client_data)
            self.logger.warning(f"Cliente añadido solo localmente: {client_data['nombre']}")
            return client_data['id']

    def add_invoice_item(self):
        """Ajoute une nouvelle ligne à la facture"""
        try:
            row = self.items_table.rowCount()
            self.items_table.insertRow(row)

            # Colonne Producto (ComboBox)
            product_combo = QComboBox()
            product_combo.addItem("Seleccionar producto...", None)

            for product in self.productos_data:
                display_text = f"{product.get('referencia', '')} - {product.get('nombre', '')}"
                product_combo.addItem(display_text, product)

            product_combo.currentTextChanged.connect(lambda: self.on_product_changed(row))
            self.items_table.setCellWidget(row, 0, product_combo)

            # Colonne Descripción
            desc_item = QTableWidgetItem("")
            self.items_table.setItem(row, 1, desc_item)

            # Colonne Cantidad (SpinBox)
            cantidad_spin = QSpinBox()
            cantidad_spin.setMinimum(1)
            cantidad_spin.setMaximum(9999)
            cantidad_spin.setValue(1)
            cantidad_spin.valueChanged.connect(lambda: self.calculate_line_total(row))
            self.items_table.setCellWidget(row, 2, cantidad_spin)

            # Colonne Precio Unit. (DoubleSpinBox)
            precio_spin = QDoubleSpinBox()
            precio_spin.setMinimum(0.00)
            precio_spin.setMaximum(999999.99)
            precio_spin.setDecimals(2)
            precio_spin.setSuffix(" €")
            precio_spin.valueChanged.connect(lambda: self.calculate_line_total(row))
            self.items_table.setCellWidget(row, 3, precio_spin)

            # Colonne Descuento % (DoubleSpinBox)
            descuento_spin = QDoubleSpinBox()
            descuento_spin.setMinimum(0.00)
            descuento_spin.setMaximum(100.00)
            descuento_spin.setDecimals(2)
            descuento_spin.setSuffix(" %")
            descuento_spin.valueChanged.connect(lambda: self.calculate_line_total(row))
            self.items_table.setCellWidget(row, 4, descuento_spin)

            # Colonne IVA % (DoubleSpinBox)
            iva_spin = QDoubleSpinBox()
            iva_spin.setMinimum(0.00)
            iva_spin.setMaximum(100.00)
            iva_spin.setDecimals(2)
            iva_spin.setValue(21.00)  # IVA par défaut
            iva_spin.setSuffix(" %")
            iva_spin.valueChanged.connect(lambda: self.calculate_line_total(row))
            self.items_table.setCellWidget(row, 5, iva_spin)

            # Colonne Total (lecture seule)
            total_item = QTableWidgetItem("0.00 €")
            total_item.setFlags(total_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.items_table.setItem(row, 6, total_item)

            self.logger.info(f"Línea de factura añadida en fila {row}")

        except Exception as e:
            self.logger.error(f"Error añadiendo línea de factura: {e}")
            self.show_error("Error", f"Error al añadir línea: {e}")

    def remove_invoice_item(self):
        """Supprime la ligne sélectionnée"""
        current_row = self.items_table.currentRow()

        if current_row >= 0:
            if self.ask_question("Confirmar", "¿Eliminar la línea seleccionada?"):
                self.items_table.removeRow(current_row)
                self.calculate_totals()
                self.logger.info(f"Línea de factura eliminada: fila {current_row}")
        else:
            self.show_warning("Selección", "Selecciona una línea para eliminar")

    def on_product_changed(self, row):
        """Gère le changement de produit dans une ligne"""
        try:
            product_combo = self.items_table.cellWidget(row, 0)
            product_data = product_combo.currentData()

            if product_data:
                # Remplir la description
                desc_item = self.items_table.item(row, 1)
                if desc_item:
                    desc_item.setText(product_data.get('descripcion', product_data.get('nombre', '')))

                # Remplir le prix
                precio_spin = self.items_table.cellWidget(row, 3)
                if precio_spin:
                    precio_spin.setValue(float(product_data.get('precio_venta', 0)))

                # Remplir l'IVA
                iva_spin = self.items_table.cellWidget(row, 5)
                if iva_spin:
                    iva_spin.setValue(float(product_data.get('iva_recomendado', 21.0)))

                # Recalculer le total de la ligne
                self.calculate_line_total(row)

        except Exception as e:
            self.logger.error(f"Error cambiando producto en fila {row}: {e}")

    def calculate_line_total(self, row):
        """Calcule le total d'une ligne"""
        try:
            # Récupérer les valeurs
            cantidad_spin = self.items_table.cellWidget(row, 2)
            precio_spin = self.items_table.cellWidget(row, 3)
            descuento_spin = self.items_table.cellWidget(row, 4)
            iva_spin = self.items_table.cellWidget(row, 5)

            if not all([cantidad_spin, precio_spin, descuento_spin, iva_spin]):
                return

            cantidad = cantidad_spin.value()
            precio_unit = precio_spin.value()
            descuento_pct = descuento_spin.value()
            iva_pct = iva_spin.value()

            # Calculs
            subtotal_linea = cantidad * precio_unit
            descuento_amount = subtotal_linea * (descuento_pct / 100)
            subtotal_con_descuento = subtotal_linea - descuento_amount
            iva_amount = subtotal_con_descuento * (iva_pct / 100)
            total_linea = subtotal_con_descuento + iva_amount

            # Mettre à jour l'affichage
            total_item = self.items_table.item(row, 6)
            if total_item:
                total_item.setText(f"{total_linea:.2f} €")

            # Recalculer les totaux généraux
            self.calculate_totals()

        except Exception as e:
            self.logger.error(f"Error calculando total de línea {row}: {e}")

    def calculate_totals(self):
        """Calcule les totaux généraux de la facture"""
        try:
            subtotal_total = 0.0
            iva_total = 0.0

            for row in range(self.items_table.rowCount()):
                # Récupérer les valeurs de chaque ligne
                cantidad_spin = self.items_table.cellWidget(row, 2)
                precio_spin = self.items_table.cellWidget(row, 3)
                descuento_spin = self.items_table.cellWidget(row, 4)
                iva_spin = self.items_table.cellWidget(row, 5)

                if not all([cantidad_spin, precio_spin, descuento_spin, iva_spin]):
                    continue

                cantidad = cantidad_spin.value()
                precio_unit = precio_spin.value()
                descuento_pct = descuento_spin.value()
                iva_pct = iva_spin.value()

                # Calculs pour cette ligne
                subtotal_linea = cantidad * precio_unit
                descuento_amount = subtotal_linea * (descuento_pct / 100)
                subtotal_con_descuento = subtotal_linea - descuento_amount
                iva_amount = subtotal_con_descuento * (iva_pct / 100)

                subtotal_total += subtotal_con_descuento
                iva_total += iva_amount

            total_general = subtotal_total + iva_total

            # Mettre à jour l'affichage
            self.subtotal_label.setText(f"{subtotal_total:.2f} €")
            self.iva_label.setText(f"{iva_total:.2f} €")
            self.total_label.setText(f"{total_general:.2f} €")

        except Exception as e:
            self.logger.error(f"Error calculando totales: {e}")

    def save_invoice(self):
        """Sauvegarde la facture"""
        try:
            # Validation
            if not self.validate_invoice():
                return

            # Préparer les données de la facture
            invoice_data = self.prepare_invoice_data()

            # Vérifier si le client est nouveau et le sauvegarder
            client_data = invoice_data['cliente']
            if client_data.get('is_new') or not client_data.get('id'):
                # Vérifier si le client existe déjà par nom
                existing_client = db.get_client_by_name(client_data['nombre'])
                if existing_client:
                    # Utiliser le client existant
                    invoice_data['cliente'] = existing_client
                    self.logger.info(f"Cliente existente encontrado: {existing_client['nombre']}")
                else:
                    # Créer le nouveau client
                    client_id = self.save_new_client_to_database(client_data)
                    client_data['id'] = client_id
                    self.logger.info(f"Nuevo cliente creado con ID: {client_id}")

            # Sauvegarder la facture en base de données
            if self.is_editing and self.factura_data and self.factura_data.get('id'):
                # Mode édition : mettre à jour la facture existante
                factura_id = self.factura_data['id']
                invoice_data['id'] = factura_id
                success = db.update_invoice(invoice_data)

                if success:
                    self.logger.info(f"Factura actualizada: {invoice_data['numero']} (ID: {factura_id})")
                    # Afficher le résumé de succès pour modification
                    self.show_invoice_updated_summary(invoice_data, factura_id)
                else:
                    raise Exception("No se pudo actualizar la factura")
            else:
                # Mode création : créer une nouvelle facture
                factura_id = db.add_invoice(invoice_data)
                self.logger.info(f"Nueva factura creada: {invoice_data['numero']} (ID: {factura_id})")
                # Afficher le résumé de succès pour création
                self.show_invoice_saved_summary(invoice_data, factura_id)

            # Émettre le signal de sauvegarde
            self.factura_saved.emit()

            # Fermer la fenêtre
            self.close()

        except Exception as e:
            self.logger.error(f"Error guardando factura: {e}")
            self.show_error("Error", f"Error al guardar factura: {e}")

    def show_invoice_updated_summary(self, invoice_data, factura_id):
        """Affiche un résumé de la facture modifiée"""
        summary = f"""FACTURA ACTUALIZADA EXITOSAMENTE

ID en Base de Datos: {factura_id}
Número: {invoice_data['numero']}
Fecha: {invoice_data['fecha']}
Cliente: {invoice_data['cliente']['nombre']}
Total: {invoice_data['total']:.2f} €

La factura ha sido actualizada correctamente."""

        self.show_info("Factura Actualizada", summary)

    def show_invoice_saved_summary(self, invoice_data, factura_id):
        """Affiche un résumé de la facture sauvegardée"""
        summary = f"""FACTURA GUARDADA EXITOSAMENTE

ID en Base de Datos: {factura_id}
Número: {invoice_data['numero']}
Fecha: {invoice_data['fecha']}
Cliente: {invoice_data['cliente']['nombre']}

Líneas: {len(invoice_data['lineas'])}
Subtotal: {invoice_data['subtotal']:.2f} €
IVA: {invoice_data['iva_total']:.2f} €
TOTAL: {invoice_data['total']:.2f} €

La factura ha sido guardada en la base de datos."""

        self.show_info("Factura Guardada", summary)

    def validate_invoice(self):
        """Valide les données de la facture"""
        # Vérifier qu'un client est sélectionné ou saisi
        client_data = self.cliente_autocomplete.get_client_data_for_invoice()
        if not client_data or not client_data.get('nombre', '').strip():
            self.show_warning("Validación", "Ingrese el nombre del cliente")
            return False

        # Vérifier qu'il y a au moins une ligne
        if self.items_table.rowCount() == 0:
            self.show_warning("Validación", "Añade al menos una línea a la factura")
            return False

        # Vérifier que les lignes avec des données ont un produit sélectionné
        valid_lines = 0
        for row in range(self.items_table.rowCount()):
            product_combo = self.items_table.cellWidget(row, 0)
            cantidad_spin = self.items_table.cellWidget(row, 2)
            precio_spin = self.items_table.cellWidget(row, 3)

            # Vérifier si la ligne a des données (quantité > 0 ou prix > 0)
            has_quantity = cantidad_spin and cantidad_spin.value() > 0
            has_price = precio_spin and precio_spin.value() > 0
            has_product = product_combo and product_combo.currentData()

            # Si la ligne a des données mais pas de produit, c'est une erreur
            if (has_quantity or has_price) and not has_product:
                self.show_warning("Validación", f"Selecciona un producto en la línea {row + 1}")
                return False

            # Si la ligne a un produit, c'est une ligne valide
            if has_product:
                valid_lines += 1

        # Vérifier qu'il y a au moins une ligne valide
        if valid_lines == 0:
            self.show_warning("Validación", "Añade al menos una línea con producto a la factura")
            return False

        return True

    def prepare_invoice_data(self):
        """Prépare les données de la facture pour la sauvegarde"""
        client_data = self.cliente_autocomplete.get_client_data_for_invoice()

        # Si c'est un nouveau client, s'assurer qu'il est sauvegardé
        if client_data and client_data.get('is_new', False):
            # Double vérification pour éviter les doublons
            existing_client = db.get_client_by_name(client_data['nombre'])
            if existing_client:
                # Utiliser le client existant
                client_data = existing_client
                self.logger.info(f"Cliente existente encontrado: {existing_client['nombre']} (ID: {existing_client['id']})")
            else:
                # Vérifier une dernière fois avant de créer
                all_clients = db.get_all_clients()
                duplicate_client = None
                for client in all_clients:
                    if client['nombre'].lower().strip() == client_data['nombre'].lower().strip():
                        duplicate_client = client
                        break

                if duplicate_client:
                    # Utiliser le client trouvé
                    client_data = duplicate_client
                    self.logger.info(f"Cliente duplicado evitado: {duplicate_client['nombre']} (ID: {duplicate_client['id']})")
                else:
                    # Sauvegarder le nouveau client
                    client_id = self.save_new_client_to_database(client_data)
                    if client_id:
                        client_data['id'] = client_id
                        client_data['is_new'] = False  # Marquer comme sauvegardé
                        self.logger.info(f"Nuevo cliente guardado con ID: {client_id}")
                    else:
                        self.logger.error("Error guardando nuevo cliente")
                        return None

        invoice_data = {
            'numero': self.numero_edit.text(),
            'fecha': self.fecha_edit.date().toString('yyyy-MM-dd'),
            'vencimiento': self.vencimiento_edit.date().toString('yyyy-MM-dd'),
            'cliente': {
                'id': client_data['id'],
                'nombre': client_data['nombre'],
                'nif': client_data['nif'],
                'direccion': client_data['direccion']
            },
            'lineas': [],
            'subtotal': 0.0,
            'iva_total': 0.0,
            'total': 0.0
        }

        # En mode édition, préserver l'ID de la facture
        if self.is_editing and self.factura_data and self.factura_data.get('id'):
            invoice_data['id'] = self.factura_data['id']

        # Ajouter les lignes
        subtotal_total = 0.0
        iva_total = 0.0

        for row in range(self.items_table.rowCount()):
            product_combo = self.items_table.cellWidget(row, 0)
            product_data = product_combo.currentData()

            if not product_data:
                continue

            desc_item = self.items_table.item(row, 1)
            cantidad_spin = self.items_table.cellWidget(row, 2)
            precio_spin = self.items_table.cellWidget(row, 3)
            descuento_spin = self.items_table.cellWidget(row, 4)
            iva_spin = self.items_table.cellWidget(row, 5)

            cantidad = cantidad_spin.value()
            precio_unit = precio_spin.value()
            descuento_pct = descuento_spin.value()
            iva_pct = iva_spin.value()

            # Calculs
            subtotal_linea = cantidad * precio_unit
            descuento_amount = subtotal_linea * (descuento_pct / 100)
            subtotal_con_descuento = subtotal_linea - descuento_amount
            iva_amount = subtotal_con_descuento * (iva_pct / 100)
            total_linea = subtotal_con_descuento + iva_amount

            linea_data = {
                'producto_id': product_data['id'],
                'producto_nombre': product_data['nombre'],
                'producto_referencia': product_data.get('referencia', ''),
                'descripcion': desc_item.text() if desc_item else '',
                'cantidad': cantidad,
                'precio_unitario': precio_unit,
                'descuento_pct': descuento_pct,
                'iva_pct': iva_pct,
                'subtotal': subtotal_con_descuento,
                'iva_amount': iva_amount,
                'total': total_linea
            }

            invoice_data['lineas'].append(linea_data)
            subtotal_total += subtotal_con_descuento
            iva_total += iva_amount

        invoice_data['subtotal'] = subtotal_total
        invoice_data['iva_total'] = iva_total
        invoice_data['total'] = subtotal_total + iva_total

        return invoice_data

    def show_invoice_summary(self, invoice_data):
        """Affiche un résumé de la facture créée"""
        summary = f"""FACTURA CREADA EXITOSAMENTE

Número: {invoice_data['numero']}
Fecha: {invoice_data['fecha']}
Cliente: {invoice_data['cliente']['nombre']}

Líneas: {len(invoice_data['lineas'])}
Subtotal: {invoice_data['subtotal']:.2f} €
IVA: {invoice_data['iva_total']:.2f} €
TOTAL: {invoice_data['total']:.2f} €

La factura ha sido guardada correctamente."""

        self.show_info("Factura Guardada", summary)

    def preview_invoice(self):
        """Muestra una vista previa de la factura"""
        if not self.validate_invoice():
            return

        invoice_data = self.prepare_invoice_data()

        # Crear una vista previa simple
        preview_text = self.generate_invoice_preview(invoice_data)

        # Mostrar en un diálogo
        preview_dialog = QMessageBox(self)
        preview_dialog.setWindowTitle("Vista Previa de Factura")
        preview_dialog.setText("Vista previa de la factura:")
        preview_dialog.setDetailedText(preview_text)
        preview_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        preview_dialog.exec()

    def generate_invoice_preview(self, invoice_data):
        """Génère un aperçu textuel de la facture"""
        preview = f"""
FACTURA: {invoice_data['numero']}
Fecha: {invoice_data['fecha']}
Vencimiento: {invoice_data['vencimiento']}

CLIENTE:
{invoice_data['cliente']['nombre']}
NIF/CIF: {invoice_data['cliente']['nif']}
{invoice_data['cliente']['direccion']}

LÍNEAS DE FACTURA:
{'='*60}
"""

        for i, linea in enumerate(invoice_data['lineas'], 1):
            preview += f"""
{i}. {linea['producto_referencia']} - {linea['producto_nombre']}
   Descripción: {linea['descripcion']}
   Cantidad: {linea['cantidad']} x {linea['precio_unitario']:.2f} €
   Descuento: {linea['descuento_pct']:.1f}%
   IVA: {linea['iva_pct']:.1f}%
   Total línea: {linea['total']:.2f} €
"""

        preview += f"""
{'='*60}
SUBTOTAL: {invoice_data['subtotal']:.2f} €
IVA TOTAL: {invoice_data['iva_total']:.2f} €
TOTAL: {invoice_data['total']:.2f} €
"""

        return preview

    def print_invoice(self):
        """Imprime la facture en PDF"""
        if not self.validate_invoice():
            return

        try:
            # Préparer les données de la facture
            invoice_data = self.prepare_invoice_data()

            # Créer le dossier de sortie s'il n'existe pas
            output_dir = "facturas_pdf"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Nom du fichier PDF
            invoice_number = invoice_data['numero'].replace('/', '_').replace('-', '_')
            pdf_filename = f"Factura_{invoice_number}.pdf"
            pdf_path = os.path.join(output_dir, pdf_filename)

            # Générer le PDF
            self.logger.info(f"Generando PDF: {pdf_path}")
            success = pdf_generator.generate_invoice_pdf(invoice_data, pdf_path)

            if success:
                # Demander si ouvrir le PDF
                if self.ask_question("PDF Generado",
                                   f"PDF generado exitosamente:\n{pdf_path}\n\n¿Desea abrir el archivo?"):
                    self.open_pdf_file(pdf_path)
                else:
                    self.show_info("PDF Generado", f"PDF guardado en:\n{pdf_path}")
            else:
                self.show_error("Error", "Error al generar el PDF")

        except Exception as e:
            self.logger.error(f"Error generando PDF: {e}")
            self.show_error("Error", f"Error al generar PDF:\n{str(e)}")

    def open_pdf_file(self, pdf_path):
        """Ouvre le fichier PDF avec l'application par défaut"""
        try:
            import subprocess
            import platform

            system = platform.system()
            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])

            self.logger.info(f"PDF abierto: {pdf_path}")

        except Exception as e:
            self.logger.error(f"Error abriendo PDF: {e}")
            self.show_warning("Advertencia", f"PDF generado pero no se pudo abrir automáticamente:\n{pdf_path}")

    def load_invoice_data(self):
        """Charge les données d'une facture existante pour édition"""
        if not self.factura_data:
            return

        try:
            # Charger les données de base
            self.numero_edit.setText(self.factura_data.get('numero', ''))

            # Charger la date
            fecha = self.factura_data.get('fecha', '')
            if fecha:
                try:
                    from PyQt6.QtCore import QDate
                    # Convertir la date string en QDate
                    if isinstance(fecha, str):
                        # Format attendu: YYYY-MM-DD
                        date_parts = fecha.split('-')
                        if len(date_parts) == 3:
                            year, month, day = map(int, date_parts)
                            qdate = QDate(year, month, day)
                            self.fecha_edit.setDate(qdate)
                except Exception as e:
                    self.logger.warning(f"Error cargando fecha: {e}")

            # Charger les données du client
            cliente_data = self.factura_data.get('cliente', {})
            if cliente_data:
                # Définir le client dans l'autocomplétion
                cliente_nombre = cliente_data.get('nombre', '')
                if cliente_nombre:
                    self.cliente_autocomplete.setText(cliente_nombre)
                    self.cliente_autocomplete.current_client = cliente_data

                    # Mettre à jour les labels d'information client
                    self.cliente_nif_label.setText(cliente_data.get('nif', '-'))
                    self.cliente_direccion_label.setText(cliente_data.get('direccion', '-'))

                    # Marquer le widget comme ayant un client valide
                    self.cliente_autocomplete.setProperty("hasClient", True)
                    self.cliente_autocomplete.setProperty("isNew", False)
                    self.cliente_autocomplete.style().polish(self.cliente_autocomplete)

            # Charger les totaux (lecture seule, calculés automatiquement)
            subtotal = self.factura_data.get('subtotal', 0.0)
            iva_total = self.factura_data.get('iva_total', 0.0)
            total = self.factura_data.get('total', 0.0)

            # Mettre à jour les labels de totaux
            self.subtotal_label.setText(f"{subtotal:.2f} €")
            self.iva_label.setText(f"{iva_total:.2f} €")
            self.total_label.setText(f"{total:.2f} €")

            # Charger les lignes de facture (si disponibles)
            lineas = self.factura_data.get('lineas', [])
            if lineas:
                # Supprimer les lignes existantes
                self.items_table.setRowCount(0)
                self.items_factura.clear()

                # Ajouter chaque ligne
                for linea in lineas:
                    self.add_invoice_item()
                    row = self.items_table.rowCount() - 1

                    # Remplir les données de la ligne
                    self.load_invoice_line_data(row, linea)

                # En mode édition, ne pas ajouter de ligne vide automatiquement
                # L'utilisateur peut utiliser le bouton "Añadir línea" s'il le souhaite
            else:
                # Si pas de lignes, ajouter une ligne vide pour commencer (mode création uniquement)
                if not self.is_editing and self.items_table.rowCount() == 0:
                    self.add_invoice_item()

            self.logger.info(f"Datos de factura cargados para edición: {self.factura_data.get('numero', 'N/A')}")

        except Exception as e:
            self.logger.error(f"Error cargando datos de factura: {e}")
            self.show_error("Error", f"Error al cargar factura: {e}")

    def load_invoice_line_data(self, row, linea_data):
        """Charge les données d'une ligne de facture dans la table"""
        try:
            # Récupérer les widgets de la ligne
            product_combo = self.items_table.cellWidget(row, 0)
            descripcion_edit = self.items_table.cellWidget(row, 1)
            cantidad_spin = self.items_table.cellWidget(row, 2)
            precio_spin = self.items_table.cellWidget(row, 3)
            total_label = self.items_table.cellWidget(row, 4)

            # Charger le produit
            if product_combo and linea_data.get('producto_id'):
                # Chercher le produit dans le combo
                for i in range(product_combo.count()):
                    product_data = product_combo.itemData(i)
                    if product_data and product_data.get('id') == linea_data['producto_id']:
                        product_combo.setCurrentIndex(i)
                        break
                else:
                    # Si le produit n'est pas trouvé, ajouter une entrée temporaire
                    product_name = linea_data.get('producto_nombre', 'Producto eliminado')
                    product_ref = linea_data.get('producto_referencia', 'N/A')
                    display_text = f"{product_ref} - {product_name}"

                    # Créer des données temporaires pour le produit
                    temp_product_data = {
                        'id': linea_data['producto_id'],
                        'nombre': product_name,
                        'referencia': product_ref,
                        'precio': linea_data.get('precio_unitario', 0.0)
                    }

                    product_combo.addItem(display_text, temp_product_data)
                    product_combo.setCurrentIndex(product_combo.count() - 1)

            # Charger la quantité
            if cantidad_spin:
                cantidad_spin.setValue(linea_data.get('cantidad', 1))

            # Charger le prix
            if precio_spin:
                precio_spin.setValue(linea_data.get('precio_unitario', 0.0))

            # Le total sera calculé automatiquement par les signaux

            self.logger.info(f"Línea de factura cargada: {linea_data.get('producto_nombre', 'N/A')} x {linea_data.get('cantidad', 0)}")

        except Exception as e:
            self.logger.error(f"Error cargando línea de factura: {e}")
