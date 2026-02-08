# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des factures - Version PyQt5 native
Refactorisée pour utiliser FacturaService, ClienteService, ProductoService (Phase 5)
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QGroupBox, QSplitter, QFrame, QWidget, QComboBox, QDateEdit,
    QSpinBox, QDoubleSpinBox, QTextEdit, QDialog, QDialogButtonBox,
    QApplication, QDesktopWidget, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal, QDate
from PyQt5.QtGui import QFont

from ui.client_autocomplete_widget import ClientAutoCompleteWidget, ClientDetailsWidget
from ui.product_autocomplete_widget import ProductAutoCompleteWidget
from datetime import datetime

from ui.base_pyqt5_window import BasePyQt5Window
from database.database import Database
from services.factura_service import FacturaService
from services.cliente_service import ClienteService
from services.producto_service import ProductoService
from utils.logger import get_logger
from utils.invoice_status_manager import invoice_status_manager
from utils.exceptions import (
    InvoiceValidationError, InvoiceNotFoundError,
    ClientValidationError, ClientNotFoundError,
    ProductValidationError, ProductNotFoundError,
    InsufficientStockError, DatabaseError
)
from utils.dialog_simple_foreground import SimpleDialogForegroundMixin, force_dialog_simple_foreground
from utils.dialog_no_glitch_foreground import NoGlitchDialogForegroundMixin, force_dialog_no_glitch_foreground
from utils.dialog_foreground_linux import force_dialog_to_foreground_linux

class FacturasPyQt5Window(BasePyQt5Window):
    """Fenêtre de gestion des factures avec PyQt5"""
    
    # Signaux
    factura_selected = Signal(dict)
    factura_updated = Signal(int)
    
    def __init__(self, parent=None):
        self.logger = get_logger(self.__class__.__name__)

        # Instance dédiée de base de données (évite les problèmes avec l'instance globale)
        # IMPORTANT: Doit être défini AVANT super().__init__() car setup_ui() l'utilise
        self.database = Database("base_de_datos/facturacion.db")

        # Services métier - utiliser le même chemin DB
        db_path = self.database.db_path if hasattr(self.database, 'db_path') else None
        self.factura_service = FacturaService(db_path)
        self.cliente_service = ClienteService(db_path)
        self.producto_service = ProductoService(db_path)

        super().__init__(parent, "Gestión de Facturas", 1200, 800)

        # Variables
        self.facturas = []
        self.selected_factura_id = None
        self.mostrar_archivadas = False  # False = actives, True = archivadas

        # Variables pour éviter les ouvertures multiples
        self.crear_dialog = None
        self.editar_dialog = None
        self.ver_dialog = None

        # Charger les données
        self.load_facturas()



    def setup_ui(self):
        """Configurer l'interface utilisateur - Liste scrollable"""
        # Activer le scroll pour la fenêtre
        self.setup_scrollable_content(enable_horizontal=False, enable_vertical=True)
        main_layout = self.get_content_layout()

        # Titre
        title_label = QLabel("Gestión de Facturas")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title_label)

        # Boutons d'action en haut
        top_buttons_layout = QHBoxLayout()

        self.new_btn = QPushButton("➕ Nueva Factura")
        self.new_btn.setMinimumHeight(40)
        self.new_btn.setStyleSheet("font-size: 14px; font-weight: bold; background-color: #4CAF50; color: white;")

        self.editar_btn = QPushButton("✏️ Editar")
        self.editar_btn.setMinimumHeight(40)
        self.editar_btn.setEnabled(False)

        self.view_btn = QPushButton("👁️ Ver Detalles")
        self.view_btn.setMinimumHeight(40)
        self.view_btn.setEnabled(False)

        self.pdf_btn = QPushButton("📄 Exportar PDF")
        self.pdf_btn.setMinimumHeight(40)
        self.pdf_btn.setEnabled(False)

        self.eliminar_btn = QPushButton("🗑️ Eliminar")
        self.eliminar_btn.setMinimumHeight(40)
        self.eliminar_btn.setEnabled(False)

        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setMinimumHeight(40)

        self.nuevo_anio_btn = QPushButton("📦 Empezar Nuevo Año")
        self.nuevo_anio_btn.setMinimumHeight(40)
        self.nuevo_anio_btn.setStyleSheet("font-size: 14px; font-weight: bold; background-color: #ff9800; color: white;")
        self.nuevo_anio_btn.setToolTip("Archiva todas las facturas actuales y empieza con una base limpia")

        self.ver_archivadas_btn = QPushButton("📁 Ver Archivadas")
        self.ver_archivadas_btn.setMinimumHeight(40)
        self.ver_archivadas_btn.setStyleSheet("font-size: 14px; background-color: #2196F3; color: white;")
        self.ver_archivadas_btn.setToolTip("Ver las facturas archivadas de años anteriores")

        top_buttons_layout.addWidget(self.new_btn)
        top_buttons_layout.addWidget(self.editar_btn)
        top_buttons_layout.addWidget(self.view_btn)
        top_buttons_layout.addWidget(self.pdf_btn)
        top_buttons_layout.addWidget(self.eliminar_btn)
        top_buttons_layout.addWidget(self.refresh_btn)
        top_buttons_layout.addWidget(self.ver_archivadas_btn)
        top_buttons_layout.addWidget(self.nuevo_anio_btn)
        top_buttons_layout.addStretch()

        main_layout.addLayout(top_buttons_layout)

        # Liste des factures
        self.setup_facturas_list_simple(main_layout)

        # Appliquer le style
        self.apply_style()
        
    def setup_factura_form(self, parent):
        """Configurer le formulaire d'édition/création de facture"""
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)

        # Bouton Nueva Factura en haut à gauche
        top_button_layout = QHBoxLayout()
        self.new_btn = QPushButton("➕ Nueva Factura")
        self.new_btn.setMinimumHeight(40)
        self.new_btn.setStyleSheet("font-size: 14px; font-weight: bold;")
        top_button_layout.addWidget(self.new_btn)
        top_button_layout.addStretch()
        form_layout.addLayout(top_button_layout)

        # Titre du formulaire
        self.form_title_label = QLabel("Seleccionar factura para editar o crear nueva")
        self.form_title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.form_title_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.form_title_label)

        # Section 1: Información de factura (sur une ligne)
        info_group = self.create_basic_info_section()
        form_layout.addWidget(info_group)

        # Section 2: Cliente (sans scroll individuel)
        client_group = self.create_client_section()
        form_layout.addWidget(client_group)

        # Section 3: Productos (sans scroll individuel)
        self.setup_products_section(form_layout)

        # Section 4: Totaux (sans scroll individuel)
        self.setup_totals_section(form_layout)

        parent.addWidget(form_widget)

    def setup_facturas_list_simple(self, parent_layout):
        """Configurer la liste des factures (version simplifiée)"""
        # Label
        list_label = QLabel("Lista de Facturas (doble clic para editar)")
        list_label.setFont(QFont("Arial", 12, QFont.Bold))
        parent_layout.addWidget(list_label)

        # Table des factures
        self.facturas_table = QTableWidget()
        headers = ["Número", "Cliente", "Fecha", "Total", "Estado"]
        self.setup_table_widget(self.facturas_table, headers)

        # Définir hauteur minimale pour afficher au moins 6 lignes
        # Hauteur = header (~40-50px) + 6 lignes * hauteur_ligne (~35-40px) + marges (~20px)
        self.facturas_table.setMinimumHeight(300)

        # Connecter la sélection
        self.facturas_table.itemSelectionChanged.connect(self.on_factura_selected)

        # Connecter le double-clic pour éditer
        self.facturas_table.itemDoubleClicked.connect(self.on_factura_double_clicked)

        parent_layout.addWidget(self.facturas_table)



    def apply_combo_style(self, combo_box):
        """Appliquer un style cohérent aux combo boxes pour éviter le texte blanc"""
        combo_box.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                color: #2c3e50;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #bdc3c7;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #ecf0f1;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #34495e;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #3498db;
                selection-background-color: #3498db;
                selection-color: white;
                color: #2c3e50;
                outline: none;
                padding: 5px;
            }
            QComboBox QAbstractItemView::item {
                background-color: white;
                color: #2c3e50;
                padding: 8px;
                border: none;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #3498db;
                color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)

    def create_basic_info_section(self):
        """Créer et retourner la section d'informations de base"""
        info_group = QGroupBox("Información de la Factura")
        info_layout = QGridLayout(info_group)

        # Número de factura (éditable)
        info_layout.addWidget(QLabel("Número:"), 0, 0)
        self.numero_edit = QLineEdit()
        self.numero_edit.setPlaceholderText("Haga clic en 'Nueva Factura' para generar")
        info_layout.addWidget(self.numero_edit, 0, 1)

        # Fecha
        info_layout.addWidget(QLabel("Fecha:"), 0, 2)
        self.fecha_edit = QDateEdit()
        self.fecha_edit.setDate(QDate.currentDate())
        self.fecha_edit.setCalendarPopup(True)
        info_layout.addWidget(self.fecha_edit, 0, 3)

        # Estado (sur la même ligne)
        info_layout.addWidget(QLabel("Estado:"), 0, 4)
        self.estado_combo = QComboBox()
        # Les états seront chargés depuis la configuration d'organisation
        self.apply_combo_style(self.estado_combo)
        info_layout.addWidget(self.estado_combo, 0, 5)

        return info_group

    def create_client_section(self):
        """Créer et retourner la section client"""
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
        self.client_details.client_changes_discarded.connect(self.on_client_changes_discarded)

        return client_group

    def setup_products_section(self, parent_layout):
        """Configurer la section produits"""
        products_group = QGroupBox("Productos")
        products_layout = QVBoxLayout(products_group)

        # Agregar producto
        add_product_layout = QHBoxLayout()
        add_product_layout.addWidget(QLabel("Producto:"))

        # Widget d'autocomplétion pour les produits
        self.producto_autocomplete = ProductAutoCompleteWidget()
        add_product_layout.addWidget(self.producto_autocomplete, 2)

        # Connecter les signaux du produit autocomplete
        self.producto_autocomplete.product_selected.connect(self.on_product_selected)
        self.producto_autocomplete.product_changed.connect(self.on_product_changed)

        add_product_layout.addWidget(QLabel("Cantidad:"))
        self.cantidad_spin = QSpinBox()
        self.cantidad_spin.setMinimum(1)
        self.cantidad_spin.setMaximum(9999)
        self.cantidad_spin.setValue(1)
        add_product_layout.addWidget(self.cantidad_spin)

        self.add_product_btn = QPushButton("➕ Agregar")
        add_product_layout.addWidget(self.add_product_btn)
        add_product_layout.addStretch()

        products_layout.addLayout(add_product_layout)

        # Tabla de productos
        self.productos_table = QTableWidget()
        productos_headers = ["Producto", "Cantidad", "Precio Unit.", "IVA %", "Total", "Acciones"]
        self.productos_table.setColumnCount(len(productos_headers))
        self.productos_table.setHorizontalHeaderLabels(productos_headers)
        self.productos_table.horizontalHeader().setStretchLastSection(False)
        self.productos_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.productos_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.productos_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.productos_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.productos_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.productos_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        # Définir hauteur minimale pour afficher au moins 4 lignes
        # Hauteur = header (~40-50px) + 4 lignes * hauteur_ligne (~35-40px) + marges (~20px)
        # Windows nécessite plus d'espace que Linux
        self.productos_table.setMinimumHeight(220)

        # Connecter le signal de changement pour recalculer les totaux
        self.productos_table.itemChanged.connect(self.on_product_table_item_changed)

        products_layout.addWidget(self.productos_table)
        parent_layout.addWidget(products_group)

    def setup_totals_section(self, parent_layout):
        """Configurer la section totaux"""
        totals_group = QGroupBox("Totales")
        totals_layout = QGridLayout(totals_group)

        # Subtotal
        totals_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        self.subtotal_label = QLabel("0.00 €")
        self.subtotal_label.setAlignment(Qt.AlignRight)
        totals_layout.addWidget(self.subtotal_label, 0, 1)

        # IVA
        totals_layout.addWidget(QLabel("IVA (21%):"), 1, 0)
        self.iva_label = QLabel("0.00 €")
        self.iva_label.setAlignment(Qt.AlignRight)
        totals_layout.addWidget(self.iva_label, 1, 1)

        # Total
        totals_layout.addWidget(QLabel("TOTAL:"), 2, 0)
        self.total_label = QLabel("0.00 €")
        self.total_label.setAlignment(Qt.AlignRight)
        self.total_label.setFont(QFont("Arial", 12, QFont.Bold))
        totals_layout.addWidget(self.total_label, 2, 1)

        parent_layout.addWidget(totals_group)

    def clear_form(self, reset_title=False):
        """Vider le formulaire

        Args:
            reset_title: Si True, met le titre à "Seleccionar factura...", sinon ne touche pas au titre
        """
        self.current_factura_id = None
        self.is_editing = False
        self.lineas_factura = []

        # Réinitialiser les champs
        self.numero_edit.clear()
        self.fecha_edit.setDate(QDate.currentDate())
        self.estado_combo.setCurrentIndex(0)  # Borrador
        self.cliente_autocomplete.clear_client()
        self.client_details.clear()
        self.producto_autocomplete.clear_product()

        # Vider la table des produits
        self.productos_table.setRowCount(0)

        # Réinitialiser les totaux
        self.update_totals()

        # Mettre à jour le titre seulement si demandé
        if reset_title:
            self.form_title_label.setText("Seleccionar factura para editar o crear nueva")

        # Activer/désactiver les boutons
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

    def load_form_data(self):
        """Charger les données pour les combos via services"""
        try:
            # Charger les clients dans le widget d'autocomplétion
            clientes = self.cliente_service.get_all_clientes()
            self.cliente_autocomplete.load_clients(clientes)

            # Charger les états de factures depuis la configuration d'organisation
            self.estado_combo.clear()
            estados = invoice_status_manager.get_all_statuses()
            for estado in estados:
                self.estado_combo.addItem(estado['nombre'], estado['id'])

            self.logger.info(f"Cargados {len(estados)} estados de facturas desde la configuración")

            # Charger les produits dans l'autocomplete
            productos = self.producto_service.get_all_productos()
            self.producto_autocomplete.load_products(productos)

        except DatabaseError as e:
            self.logger.error(f"Error base de datos: {e}")
            self.show_error("Error de Base de Datos", str(e))
        except Exception as e:
            self.logger.error(f"Error cargando datos del formulario: {e}")
            self.show_error("Error", f"Error inesperado: {str(e)}")

    def update_totals(self):
        """Actualizar los totales de la factura"""
        subtotal = 0.0
        total_iva = 0.0

        for row in range(self.productos_table.rowCount()):
            try:
                # Obtener cantidad, precio unitario e IVA
                cantidad_item = self.productos_table.item(row, 1)
                precio_item = self.productos_table.item(row, 2)
                iva_item = self.productos_table.item(row, 3)

                if not cantidad_item or not precio_item or not iva_item:
                    continue

                cantidad = float(cantidad_item.text())
                precio_unit = float(precio_item.text().replace('€', '').strip())
                iva_percent = float(iva_item.text().replace('%', '').strip())

                # Calcular subtotal de esta línea
                linea_subtotal = cantidad * precio_unit
                subtotal += linea_subtotal

                # Calcular IVA de esta línea
                linea_iva = linea_subtotal * (iva_percent / 100)
                total_iva += linea_iva

                # Actualizar el total de la línea (columna 4)
                linea_total = linea_subtotal + linea_iva
                total_item = self.productos_table.item(row, 4)
                if total_item:
                    # Desconectar temporairement le signal pour éviter la récursion
                    self.productos_table.blockSignals(True)
                    total_item.setText(f"{linea_total:.2f}€")
                    self.productos_table.blockSignals(False)

            except (ValueError, AttributeError):
                continue

        total = subtotal + total_iva

        self.subtotal_label.setText(f"{subtotal:.2f} €")
        self.iva_label.setText(f"{total_iva:.2f} €")
        self.total_label.setText(f"{total:.2f} €")

    def on_product_table_item_changed(self, item):
        """Gérer les changements dans la table de produits"""
        if not item:
            return

        row = item.row()
        col = item.column()

        # Si on modifie la quantité (col 1), le prix (col 2) ou l'IVA (col 3)
        if col in [1, 2, 3]:
            try:
                # Valider et recalculer
                if col == 1:  # Cantidad
                    cantidad = int(item.text())
                    if cantidad <= 0:
                        self.productos_table.blockSignals(True)
                        item.setText("1")
                        self.productos_table.blockSignals(False)
                elif col == 2:  # Precio
                    precio = float(item.text().replace('€', '').strip())
                    if precio < 0:
                        self.productos_table.blockSignals(True)
                        item.setText("0.00€")
                        self.productos_table.blockSignals(False)
                    else:
                        # Reformater avec le symbole €
                        self.productos_table.blockSignals(True)
                        item.setText(f"{precio:.2f}€")
                        self.productos_table.blockSignals(False)
                elif col == 3:  # IVA
                    iva = float(item.text().replace('%', '').strip())
                    if iva < 0:
                        self.productos_table.blockSignals(True)
                        item.setText("0%")
                        self.productos_table.blockSignals(False)
                    else:
                        # Reformater avec le symbole %
                        self.productos_table.blockSignals(True)
                        item.setText(f"{iva:.1f}%")
                        self.productos_table.blockSignals(False)

                # Recalculer les totaux
                self.update_totals()

            except ValueError:
                # Restaurer la valeur précédente si invalide
                self.productos_table.blockSignals(True)
                if col == 1:
                    item.setText("1")
                elif col == 2:
                    item.setText("0.00€")
                elif col == 3:
                    item.setText("0%")
                self.productos_table.blockSignals(False)

    def setup_connections(self):
        """Configurer les connexions de signaux"""
        # Boutons principaux
        self.new_btn.clicked.connect(self.open_new_factura_window)
        self.editar_btn.clicked.connect(self.open_edit_factura_window)
        self.view_btn.clicked.connect(self.view_factura)
        self.pdf_btn.clicked.connect(self.exportar_pdf)
        self.eliminar_btn.clicked.connect(self.eliminar_factura)
        self.refresh_btn.clicked.connect(self.load_facturas)
        self.nuevo_anio_btn.clicked.connect(self.on_nuevo_anio)
        self.ver_archivadas_btn.clicked.connect(self.on_toggle_archivadas)

    def open_new_factura_window(self):
        """Ouvrir une fenêtre pour créer une nouvelle facture"""
        try:
            self.logger.info("Abriendo ventana para nueva factura")

            # Créer une fenêtre d'édition sans données (nouvelle facture)
            from ui.factura_edit_window import FacturaEditWindow

            edit_window = FacturaEditWindow(
                parent=self,
                database_instance=self.database,
                factura_data=None  # None = nouvelle facture
            )

            # Connecter le signal de sauvegarde pour rafraîchir la liste
            edit_window.factura_saved.connect(self.on_factura_saved_from_window)

            # Garder une référence pour éviter que la fenêtre soit détruite
            self.current_edit_window = edit_window

            # Affichage simple au premier plan (sans glitch)
            edit_window.show()
            edit_window.raise_()
            edit_window.activateWindow()
            edit_window.setFocus()

        except Exception as e:
            self.logger.error(f"Error abriendo ventana de nueva factura: {e}")
            self.show_error("Error", f"Error al abrir ventana: {str(e)}")

    def open_edit_factura_window(self):
        """Ouvrir une fenêtre pour éditer la facture sélectionnée"""
        try:
            if not self.selected_factura_id:
                self.show_warning("Advertencia", "Por favor, seleccione una factura para editar")
                return

            self.logger.info(f"Abriendo ventana para editar factura ID: {self.selected_factura_id}")

            # Récupérer les données complètes de la facture
            factura_data = self.factura_service.get_factura_by_id(self.selected_factura_id)

            if not factura_data:
                self.show_error("Error", "No se pudo cargar la factura seleccionada")
                return

            # Créer une fenêtre d'édition avec les données
            from ui.factura_edit_window import FacturaEditWindow

            edit_window = FacturaEditWindow(
                parent=self,
                database_instance=self.database,
                factura_data=factura_data
            )

            # Connecter le signal de sauvegarde pour rafraîchir la liste
            edit_window.factura_saved.connect(self.on_factura_saved_from_window)

            # Garder une référence pour éviter que la fenêtre soit détruite
            self.current_edit_window = edit_window

            # Affichage simple au premier plan (sans glitch)
            edit_window.show()
            edit_window.raise_()
            edit_window.activateWindow()
            edit_window.setFocus()

        except Exception as e:
            self.logger.error(f"Error abriendo ventana de edición: {e}")
            self.show_error("Error", f"Error al abrir ventana: {str(e)}")



    def on_factura_double_clicked(self, item):
        """Gérer le double-clic sur une facture pour l'éditer"""
        self.open_edit_factura_window()

    def on_factura_saved_from_window(self, factura_id):
        """Callback appelé quand une facture est sauvegardée depuis la fenêtre d'édition"""
        self.logger.info(f"Factura guardada desde ventana: ID {factura_id}")
        # Rafraîchir la liste
        self.load_facturas()
        # Émettre le signal
        self.factura_updated.emit(factura_id)

    def new_factura_inline(self):
        """Créer une nouvelle facture dans le formulaire intégré

        Comportement:
        - Si un numéro de facture existe déjà: efface tout le formulaire
        - Si pas de numéro de facture: génère juste un nouveau numéro sans effacer les autres champs
        """
        try:
            self.logger.info("Iniciando creación de nueva factura")

            # Vérifier s'il y a déjà un numéro de facture
            current_numero = self.numero_edit.text().strip()

            if current_numero:
                # Si un numéro existe, effacer tout le formulaire
                self.logger.info(f"Número existente '{current_numero}' - limpiando formulario completo")
                self.clear_form()
                # Après clear_form, remettre la date actuelle
                self.fecha_edit.setDate(QDate.currentDate())
            else:
                # Si pas de numéro, on garde les champs existants
                self.logger.info("Sin número existente - solo generando nuevo número")

            # Générer un nouveau numéro de factura en utilisant le service de numeración
            # qui respecte la configuration de organizacion (número inicial, prefijo, etc.)
            numero = self.generate_invoice_number()
            self.numero_edit.setText(numero)
            self.logger.info(f"Nuevo número de factura generado: {numero}")

            # Activer le mode édition/création
            self.is_editing = True
            self.current_factura_id = None

            # Activer les boutons
            self.save_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)

            # Mettre à jour le titre
            self.form_title_label.setText("Nueva Factura")

        except Exception as e:
            self.logger.error(f"Error creando nueva factura: {e}")
            self.show_error("Error", f"Error al crear nueva factura: {str(e)}")

    def cancel_edit(self):
        """Annuler l'édition/création"""
        if self.ask_confirmation("Cancelar", "¿Está seguro de cancelar? Se perderán los cambios no guardados."):
            self.clear_form(reset_title=True)

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
        # Les données sont automatiquement mises à jour dans le widget

    def on_client_saved(self, client):
        """Gérer la sauvegarde d'un client"""
        try:
            self.logger.info(f"Guardando cliente: {client.get('nombre', '')}")

            if client.get('is_new', False):
                # Nouveau client - créer en base de données
                client_data = {
                    'nombre': client.get('nombre', ''),
                    'nif': client.get('nif', ''),
                    'direccion': client.get('direccion', ''),
                    'telefono': client.get('telefono', ''),
                    'email': client.get('email', '')
                }

                # Créer le client en base via ClienteService
                client_id = self.cliente_service.create_cliente(client_data)
                if client_id:
                    # Mettre à jour l'ID et marquer comme non nouveau
                    client['id'] = client_id
                    client['is_new'] = False

                    # Recharger la liste des clients pour l'autocomplétion
                    self.load_form_data()

                    self.logger.info(f"Nuevo cliente creado con ID: {client_id}")
                    self.show_message("Éxito", f"Cliente '{client.get('nombre', '')}' creado correctamente")
                else:
                    self.show_message("Error", "Error al crear el cliente")
                    return
            else:
                # Client existant - mettre à jour en base de données
                client_id = client.get('id')
                if client_id:
                    client_data = {
                        'id': client_id,
                        'nombre': client.get('nombre', ''),
                        'nif': client.get('nif', ''),
                        'direccion': client.get('direccion', ''),
                        'telefono': client.get('telefono', ''),
                        'email': client.get('email', '')
                    }

                    # Mettre à jour le client en base via ClienteService
                    if self.cliente_service.update_cliente(client_data):
                        # Recharger la liste des clients pour l'autocomplétion
                        self.load_form_data()

                        self.logger.info(f"Cliente actualizado: {client.get('nombre', '')}")
                        self.show_message("Éxito", f"Cliente '{client.get('nombre', '')}' actualizado correctamente")
                    else:
                        self.show_message("Error", "Error al actualizar el cliente")
                        return
                else:
                    self.show_message("Error", "ID de cliente no válido")
                    return

            # Actualizar la tabla de clientes si está abierta
            self.refresh_clients_table()

        except Exception as e:
            self.logger.error(f"Error al guardar cliente: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            self.show_message("Error", f"Error al guardar cliente: {str(e)}")

    def on_client_changes_discarded(self, client):
        """Gérer l'annulation des changements client"""
        self.logger.info(f"Cambios descartados para cliente: {client.get('nombre', '')}")
        # Les données ont été restaurées automatiquement dans le widget

    def refresh_clients_table(self):
        """Actualiser la table des clients si elle est ouverte"""
        try:
            # Vérifier si la fenêtre de clients est ouverte
            from ui.clientes_pyqt5 import ClientesPyQt5Window
            for widget in QApplication.allWidgets():
                if isinstance(widget, ClientesPyQt5Window) and widget.isVisible():
                    widget.load_clientes()
                    self.logger.info("Tabla de clientes actualizada")
                    break
        except Exception as e:
            self.logger.debug(f"No se pudo actualizar la tabla de clientes: {e}")

    def on_product_selected(self, product):
        """Gérer la sélection d'un produit"""
        try:
            self.logger.info(f"Producto seleccionado: {product.get('nombre', '')}")
            # Le produit est automatiquement stocké dans le widget
        except Exception as e:
            self.logger.error(f"Error al seleccionar producto: {e}")

    def on_product_changed(self):
        """Gérer le changement de produit"""
        # Rien de spécial à faire, le widget gère tout
        pass

    def show_message(self, title, message):
        """Afficher un message à l'utilisateur"""
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        if title == "Error":
            msg.setIcon(QMessageBox.Critical)
        else:
            msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def add_product_to_invoice(self):
        """Agregar producto a la factura"""
        # Obtener producto desde autocomplete
        producto = self.producto_autocomplete.get_current_product()
        cantidad = self.cantidad_spin.value()

        if not producto:
            self.show_warning("Validación", "Seleccione un producto")
            return

        try:
            producto_id = producto.get('id')
            if not producto_id:
                self.show_error("Error", "Producto no válido")
                return

            # Verificar stock (solo si el producto gestiona stock)
            sin_stock = producto.get('sin_stock', 0)
            stock_actual = producto.get('stock_actual', 0)

            if not sin_stock and cantidad > stock_actual:
                self.show_warning("Stock", f"Stock insuficiente. Disponible: {stock_actual}")
                return

            # Verificar si el producto ya está en la factura
            for row in range(self.productos_table.rowCount()):
                item = self.productos_table.item(row, 0)
                if item and item.data(Qt.UserRole) == producto_id:
                    # Producto ya existe, actualizar cantidad
                    cantidad_actual = int(self.productos_table.item(row, 1).text())
                    nueva_cantidad = cantidad_actual + cantidad

                    if not sin_stock and nueva_cantidad > stock_actual:
                        self.show_warning("Stock", f"Stock insuficiente. Disponible: {stock_actual}")
                        return

                    # Producto ya existe, actualizar cantidad
                    self.productos_table.blockSignals(True)
                    self.productos_table.item(row, 1).setText(str(nueva_cantidad))
                    self.productos_table.blockSignals(False)
                    self.update_totals()
                    return

            # Agregar nuevo producto
            row = self.productos_table.rowCount()
            self.productos_table.insertRow(row)

            precio_unit = producto.get('precio_venta', 0.0)
            iva_recomendado = producto.get('iva_recomendado', 21.0)  # IVA par défaut du produit

            # Construir nombre del producto con talla si existe
            producto_nombre = producto['nombre']
            talla = producto.get('talla', '')
            if talla and talla.strip():
                producto_nombre = f"{producto_nombre} - {talla}"

            # Bloquer les signaux pendant l'ajout
            self.productos_table.blockSignals(True)

            # Colonne 0: Nombre del producto (non éditable)
            nombre_item = QTableWidgetItem(producto_nombre)
            nombre_item.setData(Qt.UserRole, producto_id)
            nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 0, nombre_item)

            # Colonne 1: Cantidad (éditable)
            cantidad_item = QTableWidgetItem(str(cantidad))
            self.productos_table.setItem(row, 1, cantidad_item)

            # Colonne 2: Precio unitario (éditable)
            precio_item = QTableWidgetItem(f"{precio_unit:.2f}€")
            self.productos_table.setItem(row, 2, precio_item)

            # Colonne 3: IVA % (éditable, valeur par défaut du produit)
            iva_item = QTableWidgetItem(f"{iva_recomendado:.1f}%")
            self.productos_table.setItem(row, 3, iva_item)

            # Colonne 4: Total (non éditable, sera calculé)
            total_item = QTableWidgetItem("0.00€")
            total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
            self.productos_table.setItem(row, 4, total_item)

            # Colonne 5: Botón eliminar
            delete_btn = QPushButton("🗑️")
            delete_btn.clicked.connect(lambda: self.remove_product_from_invoice(row))
            self.productos_table.setCellWidget(row, 5, delete_btn)

            # Réactiver les signaux
            self.productos_table.blockSignals(False)

            # Actualizar totales
            self.update_totals()

            # Resetear selección
            self.producto_autocomplete.clear_product()
            self.cantidad_spin.setValue(1)

        except Exception as e:
            self.logger.error(f"Error agregando producto: {e}")
            self.show_error("Error", f"Error al agregar producto: {str(e)}")

    def remove_product_from_invoice(self, row):
        """Eliminar producto de la factura"""
        if self.ask_confirmation("Eliminar", "¿Eliminar este producto de la factura?"):
            self.productos_table.removeRow(row)
            self.update_totals()

            # Reconectar los botones (los índices de fila han changé)
            for i in range(self.productos_table.rowCount()):
                delete_btn = self.productos_table.cellWidget(i, 4)
                if delete_btn:
                    delete_btn.clicked.disconnect()
                    delete_btn.clicked.connect(lambda checked, r=i: self.remove_product_from_invoice(r))

    def generate_invoice_number(self):
        """Generar número de factura automático usando el servicio de numeración"""
        try:
            from utils.factura_numbering import FacturaNumberingService

            # Usar el servicio de numeración que respeta la configuración
            numbering_service = FacturaNumberingService()
            numero_factura = numbering_service.get_next_numero_factura()

            self.logger.info(f"Número de factura generado: {numero_factura}")
            return numero_factura

        except Exception as e:
            self.logger.error(f"Error generando número de factura: {e}")
            # Fallback simple en caso de error
            from datetime import datetime
            return f"F-{datetime.now().strftime('%Y%m%d')}-001"

    def load_facturas(self):
        """Charger les factures depuis la base de données via FacturaService"""
        try:
            if self.mostrar_archivadas:
                # Charger les factures archivées
                self.facturas = self.database.get_facturas_archivadas()
                self.logger.info(f"Cargadas {len(self.facturas)} facturas archivadas")
            else:
                # Charger les factures actives
                self.facturas = self.factura_service.get_all_facturas()
            self.update_facturas_table()
        except DatabaseError as e:
            self.logger.error(f"Erreur base de données: {e}")
            self.show_error("Error de Base de Datos", str(e))
        except Exception as e:
            self.logger.error(f"Erreur chargement factures: {e}")
            self.show_error("Error", f"Error inesperado: {str(e)}")

    def update_facturas_table(self):
        """Mettre à jour la table des factures"""
        self.facturas_table.setRowCount(len(self.facturas))

        for row, factura in enumerate(self.facturas):
            # Gérer les différences de noms entre factures actives et archivées
            numero = factura.get('numero', factura.get('numero_factura', ''))
            cliente = factura.get('cliente_nombre', factura.get('nombre_cliente', ''))
            fecha = factura.get('fecha', factura.get('fecha_factura', ''))
            total = factura.get('total', factura.get('total_factura', 0))
            estado = factura.get('estado', 'Archivada' if self.mostrar_archivadas else '')
            
            self.facturas_table.setItem(row, 0, QTableWidgetItem(str(numero)))
            self.facturas_table.setItem(row, 1, QTableWidgetItem(str(cliente)))
            self.facturas_table.setItem(row, 2, QTableWidgetItem(str(fecha)))
            self.facturas_table.setItem(row, 3, QTableWidgetItem(f"{total:.2f}€"))
            self.facturas_table.setItem(row, 4, QTableWidgetItem(str(estado)))

    def on_factura_selected(self):
        """Gérer la sélection d'une facture"""
        current_row = self.facturas_table.currentRow()
        if current_row >= 0 and current_row < len(self.facturas):
            factura = self.facturas[current_row]
            self.selected_factura_id = factura.get('id')

            # Activer les boutons d'action (lecture seule pour archivées)
            self.view_btn.setEnabled(True)
            self.pdf_btn.setEnabled(True)
            
            # Désactiver édition/suppression si en mode archivées
            if not self.mostrar_archivadas:
                self.editar_btn.setEnabled(True)
                self.eliminar_btn.setEnabled(True)
            else:
                self.editar_btn.setEnabled(False)
                self.eliminar_btn.setEnabled(False)

            # Émettre le signal
            self.factura_selected.emit(factura)
        else:
            # Aucune sélection
            self.selected_factura_id = None
            self.editar_btn.setEnabled(False)
            self.view_btn.setEnabled(False)
            self.pdf_btn.setEnabled(False)
            self.eliminar_btn.setEnabled(False)

    def load_factura_in_form(self, factura):
        """Charger une facture dans le formulaire pour édition"""
        try:
            self.is_editing = True
            self.current_factura_id = factura.get('id')

            # Charger les informations de base
            self.numero_edit.setText(factura.get('numero', ''))

            # Charger la date
            fecha_str = factura.get('fecha', '')
            if fecha_str:
                try:
                    from datetime import datetime
                    fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                    self.fecha_edit.setDate(QDate(fecha))
                except ValueError:
                    self.fecha_edit.setDate(QDate.currentDate())

            # Charger l'état
            estado = factura.get('estado', 'Borrador')
            index = self.estado_combo.findText(estado)
            if index >= 0:
                self.estado_combo.setCurrentIndex(index)
                self.logger.info(f"Estado seleccionado: {estado}")
            else:
                # Si l'état n'est pas trouvé, sélectionner le premier (par défaut)
                if self.estado_combo.count() > 0:
                    self.estado_combo.setCurrentIndex(0)
                    self.logger.warning(f"Estado '{estado}' no encontrado, usando el primero disponible")

            # Charger le client
            cliente_data = None

            # Essayer d'obtenir les données du client depuis la facture
            if 'cliente' in factura and isinstance(factura['cliente'], dict):
                cliente_data = factura['cliente']
            elif 'cliente_id' in factura:
                cliente_id = factura.get('cliente_id')
                if cliente_id:
                    try:
                        cliente_data = self.cliente_service.get_cliente_by_id(cliente_id)
                    except Exception as e:
                        self.logger.error(f"Error obteniendo cliente por ID {cliente_id}: {e}")

            if cliente_data:
                # Définir le client dans le widget d'autocomplétion
                self.cliente_autocomplete.set_client(cliente_data)
                self.logger.info(f"Cliente cargado: {cliente_data.get('nombre', '')}")
            else:
                # Fallback: buscar por nombre si no hay données complètes
                cliente_nombre = factura.get('cliente_nombre')
                if cliente_nombre:
                    # Créer des données de client minimales
                    cliente_data = {
                        'id': factura.get('cliente_id'),
                        'nombre': cliente_nombre,
                        'nif': '',
                        'telefono': '',
                        'email': '',
                        'direccion': ''
                    }
                    self.cliente_autocomplete.set_client(cliente_data)
                    self.logger.info(f"Cliente cargado por nombre: {cliente_nombre}")
                else:
                    self.logger.warning("No se pudo cargar información del cliente")

            # Charger les lignes de la facture
            self.load_factura_lines(factura.get('id'))

            # Mettre à jour l'interface
            self.form_title_label.setText(f"Editando Factura {factura.get('numero', '')}")
            self.save_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)

        except Exception as e:
            self.logger.error(f"Error cargando factura en formulario: {e}")
            self.show_error("Error", f"Error al cargar la factura: {str(e)}")

    def load_factura_lines(self, factura_id):
        """Charger les lignes d'une facture via FacturaService"""
        try:
            # Vider la table
            self.productos_table.setRowCount(0)

            # Obtenir la facture complète avec ses lignes via FacturaService
            factura = self.factura_service.get_factura_by_id(factura_id)
            lineas = factura.get('lineas', [])

            # Bloquer les signaux pendant le chargement
            self.productos_table.blockSignals(True)

            for linea in lineas:
                row = self.productos_table.rowCount()
                self.productos_table.insertRow(row)

                # Nom du produit (non éditable)
                producto_nombre = linea.get('producto_nombre', 'Producto desconocido')
                nombre_item = QTableWidgetItem(producto_nombre)
                nombre_item.setData(Qt.UserRole, linea.get('producto_id'))
                nombre_item.setFlags(nombre_item.flags() & ~Qt.ItemIsEditable)
                self.productos_table.setItem(row, 0, nombre_item)

                # Quantité (éditable)
                cantidad = linea.get('cantidad', 0)
                cantidad_item = QTableWidgetItem(str(cantidad))
                self.productos_table.setItem(row, 1, cantidad_item)

                # Prix unitaire (éditable)
                precio_unit = linea.get('precio_unitario', 0.0)
                precio_item = QTableWidgetItem(f"{precio_unit:.2f}€")
                self.productos_table.setItem(row, 2, precio_item)

                # IVA % (éditable)
                iva_aplicado = linea.get('iva_aplicado', 21.0)
                iva_item = QTableWidgetItem(f"{iva_aplicado:.1f}%")
                self.productos_table.setItem(row, 3, iva_item)

                # Total (non éditable, sera calculé)
                total_item = QTableWidgetItem("0.00€")
                total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
                self.productos_table.setItem(row, 4, total_item)

                # Bouton supprimer
                delete_btn = QPushButton("🗑️")
                delete_btn.clicked.connect(lambda checked, r=row: self.remove_product_from_invoice(r))
                self.productos_table.setCellWidget(row, 5, delete_btn)

            # Réactiver les signaux
            self.productos_table.blockSignals(False)

            # Mettre à jour les totaux
            self.update_totals()

        except Exception as e:
            self.logger.error(f"Error cargando líneas de factura: {e}")
            self.show_error("Error", f"Error al cargar las líneas de la factura: {str(e)}")

    def save_factura(self):
        """Sauvegarder la facture"""
        try:
            # Validation
            if not self.numero_edit.text().strip():
                self.show_warning("Validación", "El número de factura es requerido")
                return

            # Obtenir les données du client
            client_data = self.cliente_autocomplete.get_current_client()
            if not client_data or not client_data.get('nombre', '').strip():
                self.show_warning("Validación", "Seleccione o escriba un cliente")
                return

            # Obtenir les détails complets du client
            complete_client_data = self.client_details.get_client_data()
            if complete_client_data:
                client_data.update(complete_client_data)

            if self.productos_table.rowCount() == 0:
                self.show_warning("Validación", "Agregue al menos un producto")
                return

            # Sauvegarder le client s'il est nouveau
            if client_data.get('is_new', False):
                try:
                    # Créer le nouveau client dans la base de données via ClienteService
                    new_client_id = self.cliente_service.create_cliente({
                        'nombre': client_data['nombre'],
                        'nif': client_data.get('nif', ''),
                        'telefono': client_data.get('telefono', ''),
                        'email': client_data.get('email', ''),
                        'direccion': client_data.get('direccion', '')
                    })
                    client_data['id'] = new_client_id
                    client_data['is_new'] = False
                    self.logger.info(f"Nuevo cliente creado con ID: {new_client_id}")

                    # Recharger les clients dans l'autocomplétion
                    clientes = self.cliente_service.get_all_clientes()
                    self.cliente_autocomplete.load_clients(clientes)

                except Exception as e:
                    self.logger.error(f"Error creando nuevo cliente: {e}")
                    self.show_error("Error", f"Error al crear el cliente: {str(e)}")
                    return

            # Préparer les données de la facture
            factura_data = {
                'numero': self.numero_edit.text().strip(),
                'fecha': self.fecha_edit.date().toString('yyyy-MM-dd'),
                'cliente_id': client_data.get('id'),
                'estado': self.estado_combo.currentText(),
                'subtotal': float(self.subtotal_label.text().replace('€', '').strip()),
                'iva': float(self.iva_label.text().replace('€', '').strip()),
                'total': float(self.total_label.text().replace('€', '').strip())
            }

            # Préparer les lignes
            lineas = []
            for row in range(self.productos_table.rowCount()):
                producto_id = self.productos_table.item(row, 0).data(Qt.UserRole)
                cantidad = int(self.productos_table.item(row, 1).text())
                precio_unit = float(self.productos_table.item(row, 2).text().replace('€', '').strip())
                iva_percent = float(self.productos_table.item(row, 3).text().replace('%', '').strip())

                # Calculer les montants
                subtotal = cantidad * precio_unit
                iva_amount = subtotal * (iva_percent / 100)
                total = subtotal + iva_amount

                lineas.append({
                    'producto_id': producto_id,
                    'cantidad': cantidad,
                    'precio_unitario': precio_unit,
                    'iva_aplicado': iva_percent,
                    'subtotal': subtotal,
                    'iva_amount': iva_amount,
                    'total': total,
                    'descuento': 0.0,
                    'descuento_amount': 0.0
                })

            # Sauvegarder
            if self.is_editing and self.current_factura_id:
                # Mise à jour
                factura_data['id'] = self.current_factura_id
                # Adapter le format pour update_invoice
                factura_data['cliente'] = {
                    'id': client_data.get('id'),
                    'nombre': client_data.get('nombre', ''),
                    'nif': client_data.get('nif', ''),
                    'direccion': client_data.get('direccion', '')
                }
                factura_data['iva_total'] = factura_data.pop('iva')
                factura_data['lineas'] = lineas
                self.factura_service.update_factura(factura_data)
                self.show_info("Éxito", "Factura actualizada correctamente")
            else:
                # Nouvelle facture
                # Adapter le format pour add_invoice
                factura_data['cliente'] = {
                    'id': client_data.get('id'),
                    'nombre': client_data.get('nombre', ''),
                    'nif': client_data.get('nif', ''),
                    'direccion': client_data.get('direccion', '')
                }
                factura_data['iva_total'] = factura_data.pop('iva')
                factura_data['lineas'] = lineas
                factura_id = self.factura_service.create_factura(factura_data)
                self.current_factura_id = factura_id
                self.show_info("Éxito", "Factura creada correctamente")

            # Recharger la liste et nettoyer le formulaire
            self.load_facturas()
            self.clear_form(reset_title=False)
            self.form_title_label.setText("Factura guardada - Seleccionar otra o crear nueva")

        except Exception as e:
            self.logger.error(f"Error guardando factura: {e}")
            self.show_error("Error", f"Error al guardar la factura: {str(e)}")

    def new_factura(self):
        """Créer une nouvelle facture"""
        self.logger.debug("new_factura() appelée - Ouverture dialogue création")

        # Vérifier si un dialog de création est déjà ouvert
        if self.crear_dialog is not None and self.crear_dialog.isVisible():
            self.logger.debug("Dialog de création déjà ouvert - amener au premier plan")
            self.crear_dialog.raise_()
            self.crear_dialog.activateWindow()
            return

        # Créer un nouveau dialog SANS parent pour éviter les problèmes de hiérarchie
        # Le dialog s'affiche automatiquement au premier plan grâce à son constructeur
        self.crear_dialog = CrearFacturaDialog(self.database, None)

        # Connecter le signal de fermeture pour recharger les factures et nettoyer la référence
        def on_dialog_finished(result):
            if result == QDialog.Accepted:
                self.load_facturas()
            self.crear_dialog = None  # Nettoyer la référence

        self.crear_dialog.finished.connect(on_dialog_finished)

        # Afficher le dialog avec forçage sans glitch
        self.crear_dialog.show()
        # Forcer immédiatement au premier plan sans glitch
        force_dialog_no_glitch_foreground(self.crear_dialog)

    def view_factura(self):
        """Ver los detalles de la factura sélectionnée"""
        if not self.selected_factura_id:
            self.show_warning("Selección", "Seleccione una factura para ver los detalles")
            return

        try:
            # Vérifier si un dialog de visualisation est déjà ouvert
            if self.ver_dialog is not None and self.ver_dialog.isVisible():
                self.logger.debug("Dialog de visualisation déjà ouvert - amener au premier plan")
                self.ver_dialog.raise_()
                self.ver_dialog.activateWindow()
                return

            # Obtenir la facture (active ou archivée)
            if self.mostrar_archivadas:
                factura = self._get_factura_archivada_by_id(self.selected_factura_id)
            else:
                factura = self.factura_service.get_factura_by_id(self.selected_factura_id)
            
            if factura:
                self.ver_dialog = VerFacturaDialog(factura, None)

                # Connecter le signal de fermeture pour nettoyer la référence
                def on_ver_dialog_finished():
                    self.ver_dialog = None  # Nettoyer la référence

                self.ver_dialog.finished.connect(on_ver_dialog_finished)

                # Afficher le dialog avec forçage Linux optimisé
                self.ver_dialog.show()
                # Forcer immédiatement au premier plan avec techniques Linux
                force_dialog_to_foreground_linux(self.ver_dialog)
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

            # Vérifier si un dialog d'édition est déjà ouvert
            if self.editar_dialog is not None and self.editar_dialog.isVisible():
                self.logger.debug("Dialog d'édition déjà ouvert - amener au premier plan")
                self.editar_dialog.raise_()
                self.editar_dialog.activateWindow()
                return

            factura = self.factura_service.get_factura_by_id(self.selected_factura_id)
            if factura:
                self.editar_dialog = EditarFacturaDialog(factura, self.database, None)

                # Connecter le signal de fermeture pour recharger les factures et nettoyer la référence
                def on_edit_dialog_finished(result):
                    if result == QDialog.Accepted:
                        self.load_facturas()
                    self.editar_dialog = None  # Nettoyer la référence

                self.editar_dialog.finished.connect(on_edit_dialog_finished)

                # Afficher le dialog avec forçage sans glitch
                self.editar_dialog.show()
                # Forcer immédiatement au premier plan sans glitch
                force_dialog_no_glitch_foreground(self.editar_dialog)
                self.logger.debug("edit_factura() - Dialog d'édition ouvert avec forçage simple multiplateforme")
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

    def exportar_pdf(self):
        """Exportar la factura seleccionada a PDF"""
        if not self.selected_factura_id:
            self.show_warning("Selección", "Seleccione una factura para exportar a PDF")
            return

        try:
            # Obtener la factura seleccionada
            if self.mostrar_archivadas:
                # Factura archivada - récupérer depuis la base directement
                factura_data = self._get_factura_archivada_by_id(self.selected_factura_id)
            else:
                # Factura active - utiliser le service
                factura_data = self.factura_service.get_factura_by_id(self.selected_factura_id)
            
            if not factura_data:
                self.show_error("Error", "No se pudo cargar la factura seleccionada")
                return

            # Importar el generador PDF
            from utils.pdf_generator import PDFGenerator
            from database.models import Organizacion
            import os
            from datetime import datetime

            # Obtener el directorio configurado por el usuario
            organizacion = Organizacion.get()
            pdf_dir = organizacion.directorio_descargas_pdf.strip() if organizacion and organizacion.directorio_descargas_pdf else ""

            # Si no hay directorio configurado o no existe, usar el directorio por defecto
            if not pdf_dir or not os.path.exists(pdf_dir):
                pdf_dir = os.path.join(os.getcwd(), "pdfs")
                if organizacion and organizacion.directorio_descargas_pdf:
                    self.logger.warning(f"Directorio PDF configurado no existe: {organizacion.directorio_descargas_pdf}. Usando directorio por defecto: {pdf_dir}")

            # Crear el directorio si no existe
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
                self.logger.info(f"Directorio PDF creado: {pdf_dir}")

            # Generar nombre del archivo PDF
            numero_safe = str(factura_data.get('numero', 'SIN_NUMERO')).replace('/', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"Factura_{numero_safe}_{timestamp}.pdf"
            pdf_path = os.path.join(pdf_dir, pdf_filename)

            # Crear instancia del generador PDF
            pdf_generator = PDFGenerator()

            # Usar directamente generate_invoice_pdf que acepta un dictionnaire
            success = pdf_generator.generate_invoice_pdf(factura_data, pdf_path)

            if success:
                # Abrir el PDF automáticamente
                self.abrir_pdf(pdf_path)
                self.logger.info(f"PDF exportado y abierto: {pdf_path}")
            else:
                self.show_error("Error", "No se pudo generar el archivo PDF")

        except Exception as e:
            self.logger.error(f"Error exportando PDF: {e}")
            self.show_error("Error", f"Error al exportar PDF:\n{str(e)}")

    def _get_factura_archivada_by_id(self, factura_id: int) -> dict:
        """Obtener una factura archivada par son ID.
        
        Args:
            factura_id: ID de la factura archivada
            
        Returns:
            dict: Données de la factura formatées comme les factures actives
        """
        try:
            conn = self.database.get_connection()
            cursor = conn.cursor()
            
            # Récupérer la factura archivée
            cursor.execute('''
                SELECT * FROM facturas_archivadas WHERE id = ?
            ''', (factura_id,))
            
            row = cursor.fetchone()
            if not row:
                conn.close()
                return None
            
            # Convertir en dictionnaire
            columns = [description[0] for description in cursor.description]
            factura = dict(zip(columns, row))
            
            # Récupérer les items
            cursor.execute('''
                SELECT * FROM factura_items_archivadas 
                WHERE factura_archivada_id = ?
            ''', (factura_id,))
            
            items_rows = cursor.fetchall()
            items_columns = [description[0] for description in cursor.description]
            items = [dict(zip(items_columns, item_row)) for item_row in items_rows]
            
            conn.close()
            
            # Normaliser le format pour compatibilité avec le générateur PDF
            return {
                'id': factura['id'],
                'numero': factura['numero_factura'],
                'fecha': factura['fecha_factura'],
                'cliente': {
                    'id': factura['cliente_id'],
                    'nombre': factura['nombre_cliente'],
                    'nif': factura['dni_nie_cliente'],
                    'direccion': factura['direccion_cliente'],
                    'email': factura['email_cliente'],
                    'telefono': factura['telefono_cliente']
                },
                'subtotal': factura['subtotal'],
                'iva_total': factura['total_iva'],
                'total': factura['total_factura'],
                'estado': factura['estado'],
                'lineas': [
                    {
                        'producto_id': item['producto_id'],
                        'producto_nombre': f"Producto {item['producto_id']}",  # Nom par défaut
                        'cantidad': item['cantidad'],
                        'precio_unitario': item['precio_unitario'],
                        'iva_aplicado': item['iva_aplicado'],
                        'subtotal': item['subtotal'],
                        'iva_amount': item['iva_amount'],
                        'total': item['total']
                    }
                    for item in items
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo factura archivada: {e}")
            return None

    def abrir_pdf(self, pdf_path):
        """Abrir el archivo PDF con el visor predeterminado del sistema"""
        try:
            import subprocess
            import platform
            import os

            # Verificar que el archivo existe
            if not os.path.exists(pdf_path):
                self.logger.warning(f"Archivo PDF no encontrado: {pdf_path}")
                return False

            # Detectar el sistema operativo y usar el comando apropiado
            sistema = platform.system().lower()

            if sistema == "windows":
                # Windows: usar start
                os.startfile(pdf_path)
            elif sistema == "darwin":
                # macOS: usar open
                subprocess.run(["open", pdf_path], check=True)
            else:
                # Linux y otros: usar xdg-open
                subprocess.run(["xdg-open", pdf_path], check=True)

            self.logger.info(f"PDF abierto exitosamente: {pdf_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error abriendo PDF: {e}")
            # No mostrar error al usuario, solo registrar en log
            # El PDF se ha generado correctamente, solo falló la apertura
            return False

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

            # Eliminar de la base de datos via FacturaService
            success = self.factura_service.delete_factura(self.selected_factura_id)

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

    def on_nuevo_anio(self):
        """Archivar todas las facturas y empezar el nuevo año"""
        from datetime import datetime
        from PyQt5.QtWidgets import QMessageBox
        
        anio_actual = datetime.now().year
        
        # Demander confirmation avec avertissement clair
        reply = QMessageBox.warning(
            self,
            "⚠️ Empezar Nuevo Año",
            f"<b>Esta acción archivará TODAS las facturas del año {anio_actual}.</b><br><br>"
            f"Las facturas se moverán a la tabla de archivadas y "
            f"la lista de facturas actuales quedará vacía.<br><br>"
            f"<b>Esta acción no se puede deshacer.</b><br><br>"
            f"¿Está seguro de que desea continuar?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Double confirmation pour plus de sécurité
        reply2 = QMessageBox.question(
            self,
            "Confirmación Final",
            f"¿Está completamente seguro de archivar todas las facturas del año {anio_actual}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply2 != QMessageBox.Yes:
            return
        
        try:
            # Archiver les factures
            success, count, message = self.database.archivar_facturas_anio()
            
            if success:
                if count > 0:
                    QMessageBox.information(
                        self,
                        "✅ Archivado Completado",
                        f"<b>{message}</b><br><br>"
                        f"La lista de facturas ha sido limpiada. "
                        f"Puede comenzar a crear nuevas facturas para el nuevo año."
                    )
                else:
                    QMessageBox.information(
                        self,
                        "ℹ️ Sin Facturas",
                        "No hay facturas para archivar. La lista ya está vacía."
                    )
                
                # Rafraîchir la liste des factures
                self.load_facturas()
                
                # Réinitialiser la sélection
                self.selected_factura_id = None
                self.editar_btn.setEnabled(False)
                self.view_btn.setEnabled(False)
                self.pdf_btn.setEnabled(False)
                self.eliminar_btn.setEnabled(False)
                
                self.logger.info(f"Nuevo año iniciado: {count} facturas archivadas")
            else:
                QMessageBox.critical(
                    self,
                    "❌ Error",
                    f"No se pudieron archivar las facturas:<br><br>{message}"
                )
                
        except Exception as e:
            self.logger.error(f"Error en on_nuevo_anio: {e}")
            QMessageBox.critical(
                self,
                "❌ Error",
                f"Error inesperado al archivar facturas:<br><br>{str(e)}"
            )

    def on_toggle_archivadas(self):
        """Basculer entre les factures actives et archivées"""
        try:
            self.mostrar_archivadas = not self.mostrar_archivadas
            
            if self.mostrar_archivadas:
                # Passer à la vue des archivées
                self.ver_archivadas_btn.setText("📋 Ver Facturas Actuales")
                self.ver_archivadas_btn.setStyleSheet("font-size: 14px; background-color: #4CAF50; color: white;")
                self.ver_archivadas_btn.setToolTip("Volver a ver las facturas del año en curso")
                
                # Désactiver les boutons d'action (on ne peut pas modifier les archivées)
                self.new_btn.setEnabled(False)
                self.editar_btn.setEnabled(False)
                self.eliminar_btn.setEnabled(False)
                self.nuevo_anio_btn.setEnabled(False)
                
                self.logger.info("Mostrando facturas archivadas")
            else:
                # Revenir aux factures actives
                self.ver_archivadas_btn.setText("📁 Ver Archivadas")
                self.ver_archivadas_btn.setStyleSheet("font-size: 14px; background-color: #2196F3; color: white;")
                self.ver_archivadas_btn.setToolTip("Ver las facturas archivadas de años anteriores")
                
                # Réactiver les boutons d'action
                self.new_btn.setEnabled(True)
                self.nuevo_anio_btn.setEnabled(True)
                # Les autres boutons seront réactivés par on_factura_selected si une ligne est sélectionnée
                
                self.logger.info("Mostrando facturas actuales")
            
            # Recharger la liste
            self.load_facturas()
            
            # Réinitialiser la sélection
            self.selected_factura_id = None
            self.editar_btn.setEnabled(False)
            self.view_btn.setEnabled(False)
            self.pdf_btn.setEnabled(False)
            self.eliminar_btn.setEnabled(False)
            
        except Exception as e:
            self.logger.error(f"Error cambiando vista: {e}")
            self.show_error("Error", f"Error al cambiar la vista: {str(e)}")


class CrearFacturaDialog(QDialog, NoGlitchDialogForegroundMixin):
    """Dialog para crear una nueva factura"""

    def __init__(self, database_instance, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.setWindowTitle("Crear Nueva Factura")
        self.resize(800, 600)

        # Instance de base de données
        self.database = database_instance

        # Services métier - utiliser le même chemin DB
        db_path = database_instance.db_path if hasattr(database_instance, 'db_path') else None
        self.factura_service = FacturaService(db_path)
        self.cliente_service = ClienteService(db_path)
        self.producto_service = ProductoService(db_path)

        # Variables
        self.clientes = []
        self.productos = []
        self.lineas_factura = []

        self.setup_ui()

        # SOLUTION SANS GLITCH: Forçage au premier plan sans effets visuels
        # Fonctionne sur Windows, Linux, macOS sans glitch
        self.setup_no_glitch_foreground_display()

        # Charger les données de manière asynchrone après affichage
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self.load_data)  # Charger après 100ms

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
        # Améliorer la visibilité du texte sélectionné
        self.cliente_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
                color: #2c3e50;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #bdc3c7;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #ecf0f1;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #34495e;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #3498db;
                selection-background-color: #3498db;
                selection-color: white;
                color: #2c3e50;
                font-size: 13px;
                font-weight: normal;
                padding: 5px;
            }
        """)

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
            # Charger les clients via ClienteService
            self.clientes = self.cliente_service.get_all_clientes()
            self.cliente_combo.clear()
            self.cliente_combo.addItem("📋 Seleccionar cliente...", None)
            for cliente in self.clientes:
                # Format amélioré pour une meilleure lisibilité
                texto_cliente = f"👤 {cliente['nombre']} • NIF: {cliente['nif']}"
                self.cliente_combo.addItem(texto_cliente, cliente)

            # Charger les produits via ProductoService
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.logger.debug(f"[{timestamp}] CrearFacturaDialog - Llamando producto_service.get_all_productos()")
            self.productos = self.producto_service.get_all_productos()
            self.logger.debug(f"[{timestamp}] CrearFacturaDialog - Recibidos {len(self.productos)} productos")
            # Cargar productos en autocomplete
            self.producto_autocomplete.load_products(self.productos)

        except Exception as e:
            self.logger.error(f"Error cargando datos: {e}")

    def generate_invoice_number(self):
        """Generar número de factura automático usando el servicio de numeración"""
        try:
            from utils.factura_numbering import FacturaNumberingService

            # Usar el servicio de numeración avec la base de données de l'instance
            numbering_service = FacturaNumberingService(self.database)
            numero_factura = numbering_service.get_next_numero_factura()

            self.logger.info(f"Número de factura generado: {numero_factura}")
            return numero_factura

        except Exception as e:
            self.logger.error(f"Error generando número de factura: {e}")
            # Fallback simple en caso de error
            from datetime import datetime
            return f"F-{datetime.now().strftime('%Y%m%d')}-001"

    def agregar_producto(self):
        """Agregar producto a la factura"""
        producto_data = self.producto_autocomplete.get_current_product()
        if not producto_data:
            return

        cantidad = self.cantidad_spin.value()
        sin_stock = producto_data.get('sin_stock', 0)
        stock_actual = producto_data.get('stock_actual', 0)

        # Verificar stock (solo si el producto gestiona stock)
        if not sin_stock and cantidad > stock_actual:
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

        # Construir nombre del producto con talla si existe
        producto_nombre = producto_data['nombre']
        talla = producto_data.get('talla', '')
        if talla and talla.strip():
            producto_nombre = f"{producto_nombre} - {talla}"

        # Agregar a la lista
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

        # Reset selección
        self.producto_autocomplete.clear_product()
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
                # Buscar en la lista de productos cargados
                for producto in self.productos:
                    if producto.get('id') == producto_id:
                        producto_data = producto
                        break

                if producto_data:
                    # Verificar si el producto gestiona stock
                    sin_stock = producto_data.get('sin_stock', 0)
                    if not sin_stock:
                        stock_actual = producto_data.get('stock_actual', 0)
                        if nueva_cantidad > stock_actual:
                            from PyQt5.QtWidgets import QMessageBox
                            stock_resultante = stock_actual - nueva_cantidad
                            reply = QMessageBox.question(self, "Stock insuficiente",
                                                       f"Stock disponible: {stock_actual}\n"
                                                       f"Cantidad solicitada: {nueva_cantidad}\n"
                                                       f"Stock resultante: {stock_resultante}\n\n"
                                                       f"¿Desea continuar con stock negativo?",
                                                       QMessageBox.Yes | QMessageBox.No,
                                                       QMessageBox.No)
                            if reply != QMessageBox.Yes:
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

            # Guardar en la base de datos via FacturaService
            factura_id = self.factura_service.create_factura(factura_data)

            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Éxito", f"Factura {self.numero_edit.text()} creada correctamente\nID: {factura_id}")

            self.accept()

        except Exception as e:
            self.logger.error(f"Error guardando factura: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error al guardar la factura: {str(e)}")


class EditarFacturaDialog(QDialog, NoGlitchDialogForegroundMixin):
    """Dialog para editar una factura existente"""

    def __init__(self, factura_data, database_instance, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.factura_data = factura_data
        self.setWindowTitle(f"Editar Factura {factura_data['numero']}")
        self.resize(800, 600)

        # Instance de base de données
        self.database = database_instance

        # Services métier - utiliser le même chemin DB
        db_path = database_instance.db_path if hasattr(database_instance, 'db_path') else None
        self.factura_service = FacturaService(db_path)
        self.cliente_service = ClienteService(db_path)
        self.producto_service = ProductoService(db_path)

        # Variables
        self.clientes = []
        self.productos = []
        self.lineas_factura = []

        self.setup_ui()
        self.load_data()
        self.load_factura_data()

        # SOLUTION SANS GLITCH: Forçage au premier plan sans effets visuels
        # Fonctionne sur Windows, Linux, macOS sans glitch
        self.setup_no_glitch_foreground_display()

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
        # Améliorer la visibilité du texte sélectionné
        self.cliente_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #cccccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
                font-weight: bold;
                color: #2c3e50;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #bdc3c7;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: #ecf0f1;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #34495e;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #3498db;
                selection-background-color: #3498db;
                selection-color: white;
                color: #2c3e50;
                font-size: 13px;
                font-weight: normal;
                padding: 5px;
            }
        """)

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
            # Charger les clients via ClienteService
            self.clientes = self.cliente_service.get_all_clientes()
            self.cliente_combo.clear()
            self.cliente_combo.addItem("📋 Seleccionar cliente...", None)
            for cliente in self.clientes:
                # Format amélioré pour une meilleure lisibilité
                texto_cliente = f"👤 {cliente['nombre']} • NIF: {cliente['nif']}"
                self.cliente_combo.addItem(texto_cliente, cliente)

            # Charger les états de factures
            self.estados = invoice_status_manager.get_all_statuses()
            self.estado_combo.clear()
            for estado in self.estados:
                self.estado_combo.addItem(estado['nombre'], estado)

            # Charger les produits via ProductoService
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.logger.debug(f"[{timestamp}] EditarFacturaDialog - Llamando producto_service.get_all_productos()")
            self.productos = self.producto_service.get_all_productos()
            self.logger.debug(f"[{timestamp}] EditarFacturaDialog - Recibidos {len(self.productos)} productos")
            # Cargar productos en autocomplete
            self.producto_autocomplete.load_products(self.productos)

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

                # Usar los nombres correctos de los botones
                if hasattr(self, 'agregar_btn'):
                    self.agregar_btn.setEnabled(permite_modificacion)

                # Buscar botones de eliminar en la tabla (si existen)
                for i in range(self.productos_table.rowCount()):
                    eliminar_btn = self.productos_table.cellWidget(i, 5)  # Columna de acciones
                    if eliminar_btn:
                        eliminar_btn.setEnabled(permite_modificacion)

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
        producto_data = self.producto_autocomplete.get_current_product()
        if not producto_data:
            return

        cantidad = self.cantidad_spin.value()
        producto_id = producto_data.get('id')

        # Verificar si el producto gestiona stock
        sin_stock = producto_data.get('sin_stock', 0)

        if not sin_stock:
            # Calcular stock disponible considerando la factura actual
            stock_disponible = self.get_available_stock_for_product(producto_id)

            # Verificar stock disponible - permitir stocks negativos con confirmación
            if cantidad > stock_disponible:
                from PyQt5.QtWidgets import QMessageBox
                stock_resultante = stock_disponible - cantidad
                reply = QMessageBox.question(self, "Stock insuficiente",
                                           f"Stock disponible para edición: {stock_disponible}\n"
                                           f"Cantidad solicitada: {cantidad}\n"
                                           f"Stock resultante: {stock_resultante}\n\n"
                                           f"¿Desea continuar con stock negativo?",
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)
                if reply != QMessageBox.Yes:
                    return

        # Calcular precios
        precio_unitario = producto_data['precio_venta']
        iva_rate = producto_data.get('iva_recomendado', 21.0) / 100
        subtotal = precio_unitario * cantidad
        iva_amount = subtotal * iva_rate
        total = subtotal + iva_amount

        # Construir nombre del producto con talla si existe
        producto_nombre = producto_data['nombre']
        talla = producto_data.get('talla', '')
        if talla and talla.strip():
            producto_nombre = f"{producto_nombre} - {talla}"

        # Agregar a la lista
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

        # Reset selección
        self.producto_autocomplete.clear_product()
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
                # Permitir stocks negativos con confirmación del usuario
                if nueva_cantidad > stock_disponible:
                    from PyQt5.QtWidgets import QMessageBox
                    stock_resultante = stock_disponible - nueva_cantidad
                    reply = QMessageBox.question(self, "Stock insuficiente",
                                               f"Stock disponible para edición: {stock_disponible}\n"
                                               f"Cantidad solicitada: {nueva_cantidad}\n"
                                               f"Stock resultante: {stock_resultante}\n\n"
                                               f"¿Desea continuar con stock negativo?",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
                    if reply != QMessageBox.Yes:
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

            # Actualizar en la base de datos via FacturaService
            success = self.factura_service.update_factura(factura_data)

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


class VerFacturaDialog(QDialog, NoGlitchDialogForegroundMixin):
    """Dialog para ver detalles de una factura"""

    def __init__(self, factura_data, parent=None):
        super().__init__(parent)
        self.factura_data = factura_data
        self.setWindowTitle(f"Factura {factura_data['numero']}")
        self.setModal(False)  # Permitir acceso a otras ventanas
        self.resize(600, 500)

        # SOLUTION SANS GLITCH: Forçage au premier plan sans effets visuels
        # Fonctionne sur Windows, Linux, macOS sans glitch
        self.setup_no_glitch_foreground_display()

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
