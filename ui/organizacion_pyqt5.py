# -*- coding: utf-8 -*-
"""
Fenêtre de configuration de l'organisation - Version PyQt5 native
Utilise UNIQUEMENT config/config.json comme source de vérité
"""

import os
import shutil
import json
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QFrame, QWidget, QTextEdit, QFileDialog,
    QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem,
    QCheckBox, QHeaderView, QAbstractItemView, QColorDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtGui import QFont, QPixmap, QTransform, QColor

from ui.base_pyqt5_window import BasePyQt5Window
from utils.logger import get_logger
from utils.invoice_status_manager import invoice_status_manager
from ui.data_cleanup_dialog import DataCleanupDialog
from ui.todo_editor_dialog import TodoEditorDialog
from services.organizacion_service import OrganizacionService
from database.database import db

class OrganizacionPyQt5Window(BasePyQt5Window):
    """Fenêtre de configuration de l'organisation avec PyQt5 - Utilise uniquement config.json"""

    # Signaux
    organizacion_updated = Signal()

    def __init__(self, parent=None, config_file=None):
        self.logger = get_logger(self.__class__.__name__)
        super().__init__(parent, "Configuración de la Organización", 800, 600)

        # Variables
        self.organizacion_data = {}
        # Utiliser config_test.json en mode test, sinon config.json
        import os
        self.config_file = config_file or os.environ.get('CONFIG_FILE', 'config/config.json')

        # ⚠️ PROTECTION PRODUCTION: Vérifier qu'on n'utilise pas config.json en mode test
        if os.environ.get('PYTEST_RUNNING') == '1':
            if self.config_file == 'config/config.json':
                raise RuntimeError("❌ ERREUR CRITIQUE: Les tests ne doivent JAMAIS utiliser config/config.json de production !")
            if 'test' not in self.config_file.lower() and 'tmp' not in self.config_file.lower():
                raise RuntimeError(f"❌ ERREUR CRITIQUE: Le fichier config en mode test doit contenir 'test' ou 'tmp' ! Chemin: {self.config_file}")

        self.logger.info(f"📁 OrganizacionPyQt5Window utilise le fichier: {self.config_file}")

        # Charger les données
        self.load_organizacion()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Activer le scroll pour cette fenêtre (contenu long)
        self.enable_window_scroll(enable_horizontal=False, enable_vertical=True)

        # Obtenir le layout de contenu (scrollable ou normal)
        main_layout = self.get_content_layout()

        # Titre
        title_label = QLabel("Configuración de la Empresa")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title_label)

        # Configuration des sections
        self.setup_company_form(main_layout)
        self.setup_invoice_statuses_section(main_layout)

        # Boutons (toujours visibles en bas)
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("💾 Guardar Configuración")
        self.reset_btn = QPushButton("🔄 Restablecer")

        # Bouton pour éditer le TODO
        self.todo_btn = QPushButton("📝 Editar TODO")
        self.todo_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)

        # Bouton rouge pour la suppression de données
        self.cleanup_btn = QPushButton("🗑️ Limpiar Datos")
        self.cleanup_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border: none;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)

        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.todo_btn)
        buttons_layout.addWidget(self.cleanup_btn)

        main_layout.addLayout(buttons_layout)

        # Connexions
        self.setup_connections()

        # Appliquer le style
        self.apply_style()
        
    def setup_company_form(self, parent_layout):
        """Configurer le formulaire de l'entreprise"""
        # GroupBox pour les informations de base
        basic_group = QGroupBox("Información Básica")
        basic_layout = QGridLayout(basic_group)
        
        # Champs de base
        self.nombre_edit = QLineEdit()
        self.cif_edit = QLineEdit()
        self.telefono_edit = QLineEdit()
        self.email_edit = QLineEdit()
        
        basic_layout.addWidget(QLabel("Nombre de la Empresa:"), 0, 0)
        basic_layout.addWidget(self.nombre_edit, 0, 1)
        
        basic_layout.addWidget(QLabel("CIF/NIF:"), 1, 0)
        basic_layout.addWidget(self.cif_edit, 1, 1)
        
        basic_layout.addWidget(QLabel("Teléfono:"), 2, 0)
        basic_layout.addWidget(self.telefono_edit, 2, 1)
        
        basic_layout.addWidget(QLabel("Email:"), 3, 0)
        basic_layout.addWidget(self.email_edit, 3, 1)
        
        parent_layout.addWidget(basic_group)
        
        # GroupBox pour l'adresse
        address_group = QGroupBox("Dirección")
        address_layout = QVBoxLayout(address_group)
        
        self.direccion_edit = QTextEdit()
        self.direccion_edit.setMaximumHeight(100)
        address_layout.addWidget(self.direccion_edit)
        
        parent_layout.addWidget(address_group)

        # GroupBox pour les conditions de paiement
        payment_group = QGroupBox("Condiciones de Pago")
        payment_layout = QVBoxLayout(payment_group)

        self.condiciones_pago_edit = QTextEdit()
        self.condiciones_pago_edit.setMaximumHeight(100)
        self.condiciones_pago_edit.setPlaceholderText("Ej: El pago deberá realizarse antes de la fecha de vencimiento...")
        payment_layout.addWidget(self.condiciones_pago_edit)

        # Case à cocher pour la visibilité dans les PDFs
        self.condiciones_pago_visible_checkbox = QCheckBox("✓ Visible en los PDF")
        self.condiciones_pago_visible_checkbox.setChecked(True)  # Coché par défaut
        payment_layout.addWidget(self.condiciones_pago_visible_checkbox)

        parent_layout.addWidget(payment_group)

        # GroupBox pour l'information légale
        legal_group = QGroupBox("Información Legal")
        legal_layout = QVBoxLayout(legal_group)

        self.informacion_legal_edit = QTextEdit()
        self.informacion_legal_edit.setMaximumHeight(100)
        self.informacion_legal_edit.setPlaceholderText("Ej: Esta factura se emite de acuerdo con la normativa fiscal vigente...")
        legal_layout.addWidget(self.informacion_legal_edit)

        # Case à cocher pour la visibilité dans les PDFs
        self.informacion_legal_visible_checkbox = QCheckBox("✓ Visible en los PDF")
        self.informacion_legal_visible_checkbox.setChecked(True)  # Coché par défaut
        legal_layout.addWidget(self.informacion_legal_visible_checkbox)

        parent_layout.addWidget(legal_group)

        # GroupBox pour la configuration
        config_group = QGroupBox("Configuración")
        config_layout = QGridLayout(config_group)

        # Logo section
        self.logo_path_edit = QLineEdit()
        self.logo_browse_btn = QPushButton("📁 Buscar")

        # Logo orientation options
        self.logo_landscape_radio = QRadioButton("🖼️ Horizontal (Landscape)")
        self.logo_portrait_radio = QRadioButton("📱 Vertical (Portrait)")
        self.logo_landscape_radio.setChecked(True)  # Default

        # Group for radio buttons
        self.logo_orientation_group = QButtonGroup()
        self.logo_orientation_group.addButton(self.logo_landscape_radio)
        self.logo_orientation_group.addButton(self.logo_portrait_radio)

        # Logo preview
        self.logo_preview = QLabel()
        self.logo_preview.setFixedSize(180, 180)  # Taille fixe carrée
        self.logo_preview.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                text-align: center;
            }
        """)
        self.logo_preview.setText("Sin logo\nseleccionado")
        self.logo_preview.setAlignment(Qt.AlignCenter)
        self.logo_preview.setScaledContents(False)  # Important: ne pas déformer

        self.numero_factura_edit = QLineEdit()
        self.numero_factura_edit.setPlaceholderText("Ej: 1, fact-2005-1, FAC-2025-001")

        config_layout.addWidget(QLabel("Logo de la Empresa:"), 0, 0)
        config_layout.addWidget(self.logo_path_edit, 0, 1)
        config_layout.addWidget(self.logo_browse_btn, 0, 2)
        config_layout.addWidget(self.logo_preview, 0, 3, 4, 1)  # Span 4 rows

        config_layout.addWidget(QLabel("Orientación del Logo:"), 1, 0)
        orientation_layout = QHBoxLayout()
        orientation_layout.addWidget(self.logo_landscape_radio)
        orientation_layout.addWidget(self.logo_portrait_radio)
        orientation_widget = QWidget()
        orientation_widget.setLayout(orientation_layout)
        config_layout.addWidget(orientation_widget, 1, 1, 1, 2)  # Span 2 columns

        config_layout.addWidget(QLabel("Número Inicial de Factura:"), 2, 0)
        config_layout.addWidget(self.numero_factura_edit, 2, 1)

        parent_layout.addWidget(config_group)

        # GroupBox pour les répertoires
        directories_group = QGroupBox("Configuración de Directorios")
        directories_layout = QGridLayout(directories_group)

        # Répertoire des images par défaut
        self.images_dir_edit = QLineEdit()
        self.images_dir_edit.setPlaceholderText("Directorio donde buscar imágenes por defecto")
        self.images_dir_browse_btn = QPushButton("📁 Buscar")

        # Répertoire de stockage des logos
        self.logos_storage_dir_edit = QLineEdit()
        self.logos_storage_dir_edit.setPlaceholderText("Directorio donde guardar los logos")
        self.logos_storage_dir_browse_btn = QPushButton("📁 Buscar")

        # Répertoire des PDFs
        self.pdfs_dir_edit = QLineEdit()
        self.pdfs_dir_edit.setPlaceholderText("Directorio donde guardar las facturas PDF")
        self.pdfs_dir_browse_btn = QPushButton("📁 Buscar")

        # Répertoire des Informes
        self.informes_dir_edit = QLineEdit()
        self.informes_dir_edit.setPlaceholderText("Directorio donde guardar los informes PDF")
        self.informes_dir_browse_btn = QPushButton("📁 Buscar")

        directories_layout.addWidget(QLabel("Directorio de Imágenes:"), 0, 0)
        directories_layout.addWidget(self.images_dir_edit, 0, 1)
        directories_layout.addWidget(self.images_dir_browse_btn, 0, 2)

        directories_layout.addWidget(QLabel("Directorio de Logos:"), 1, 0)
        directories_layout.addWidget(self.logos_storage_dir_edit, 1, 1)
        directories_layout.addWidget(self.logos_storage_dir_browse_btn, 1, 2)

        directories_layout.addWidget(QLabel("Directorio de PDFs:"), 2, 0)
        directories_layout.addWidget(self.pdfs_dir_edit, 2, 1)
        directories_layout.addWidget(self.pdfs_dir_browse_btn, 2, 2)

        directories_layout.addWidget(QLabel("Directorio de Informes:"), 3, 0)
        directories_layout.addWidget(self.informes_dir_edit, 3, 1)
        directories_layout.addWidget(self.informes_dir_browse_btn, 3, 2)

        parent_layout.addWidget(directories_group)

    def setup_invoice_statuses_section(self, parent_layout):
        """Configurer la section des états de factures"""
        # GroupBox pour les états de factures
        statuses_group = QGroupBox("Configuración de Estados de Facturas")
        statuses_layout = QVBoxLayout(statuses_group)

        # Description
        desc_label = QLabel("Configure los estados posibles para las facturas y determine cuáles permiten modificación:")
        desc_label.setWordWrap(True)
        statuses_layout.addWidget(desc_label)

        # Table des états
        self.statuses_table = QTableWidget()
        self.statuses_table.setColumnCount(5)
        self.statuses_table.setHorizontalHeaderLabels([
            "Estado", "Descripción", "Permite Modificación", "Color", "Orden"
        ])

        # Configuration de la table
        header = self.statuses_table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Estado
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Descripción
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Permite Modificación
        header.setSectionResizeMode(3, QHeaderView.Fixed)  # Color - taille fixe pour éviter débordement
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Orden

        # Définir une largeur fixe pour la colonne Color (60px pour afficher le titre complet)
        header.resizeSection(3, 60)

        self.statuses_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.statuses_table.setAlternatingRowColors(True)

        # Définir une hauteur de ligne minimale pour les boutons de couleur
        self.statuses_table.verticalHeader().setDefaultSectionSize(30)  # Réduit pour éviter débordement

        statuses_layout.addWidget(self.statuses_table)

        # Boutons d'action pour les états
        statuses_buttons_layout = QHBoxLayout()

        self.add_status_btn = QPushButton("➕ Agregar Estado")
        self.edit_status_btn = QPushButton("✏️ Editar Estado")
        self.delete_status_btn = QPushButton("🗑️ Eliminar Estado")

        statuses_buttons_layout.addWidget(self.add_status_btn)
        statuses_buttons_layout.addWidget(self.edit_status_btn)
        statuses_buttons_layout.addWidget(self.delete_status_btn)
        statuses_buttons_layout.addStretch()

        statuses_layout.addLayout(statuses_buttons_layout)

        parent_layout.addWidget(statuses_group)

        # Charger les états existants
        self.load_invoice_statuses()

    def setup_connections(self):
        """Configurer les connexions de signaux"""
        # Vérifier si les connexions ont déjà été faites
        if hasattr(self, '_connections_setup'):
            return

        self.save_btn.clicked.connect(self.save_organizacion)
        self.reset_btn.clicked.connect(self.load_organizacion)
        self.todo_btn.clicked.connect(self.open_todo_editor)
        self.cleanup_btn.clicked.connect(self.open_data_cleanup_dialog)
        self.logo_browse_btn.clicked.connect(self.browse_logo)
        print("DEBUG: logo_browse_btn connecté à browse_logo")
        self.logo_landscape_radio.toggled.connect(self.on_orientation_changed)
        self.logo_portrait_radio.toggled.connect(self.on_orientation_changed)

        # Connexions pour les répertoires
        self.images_dir_browse_btn.clicked.connect(self.browse_images_directory)
        self.logos_storage_dir_browse_btn.clicked.connect(self.browse_logos_storage_directory)
        self.pdfs_dir_browse_btn.clicked.connect(self.browse_pdfs_directory)
        self.informes_dir_browse_btn.clicked.connect(self.browse_informes_directory)

        # Connecter les changements de données
        self.nombre_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.cif_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.telefono_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.email_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.direccion_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.logo_path_edit.textChanged.connect(self.on_logo_path_changed)
        self.numero_factura_edit.textChanged.connect(lambda: self.set_data_modified(True))

        # Connexions pour les changements de répertoires
        self.images_dir_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.logos_storage_dir_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.pdfs_dir_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.informes_dir_edit.textChanged.connect(lambda: self.set_data_modified(True))

        # Connexions pour les états de factures
        self.add_status_btn.clicked.connect(self.add_invoice_status)
        self.edit_status_btn.clicked.connect(self.edit_invoice_status)
        self.delete_status_btn.clicked.connect(self.delete_invoice_status)

        # Marquer les connexions comme configurées
        self._connections_setup = True
        
    def get_default_config(self):
        """Obtenir la configuration par défaut"""
        return {
            'nombre': 'Mi Empresa',
            'direccion': 'Calle Principal, 123\n12345 Ciudad',
            'telefono': '+34 123 456 789',
            'email': 'contacto@miempresa.com',
            'cif': 'B12345678',
            'numero_factura_inicial': '1',
            'directorio_imagenes_defecto': 'images',
            'directorio_descargas_pdf': 'facturas/',
            'directorio_informes': 'informes/',
            'directorio_logos_storage': 'logo/',
            'logo_path': 'logo/logo.png',
            'logo_orientation': 'landscape',
            'visor_pdf_personalizado': '',
            'condiciones_pago': '• El pago de esta factura deberá realizarse antes de la fecha de vencimiento.\n• Pasados 30 días de la fecha de vencimiento, se aplicarán intereses de demora.\n• Para cualquier consulta, contacte con nosotros.',
            'informacion_legal': '• Esta factura se emite de acuerdo con la normativa fiscal vigente.\n• Conserve este documento para sus registros contables.',
            'condiciones_pago_visible': 1,
            'informacion_legal_visible': 1
        }

    def load_config_json(self):
        """Charger les données depuis config.json avec fusion intelligente des défauts"""
        try:
            # Obtenir les valeurs par défaut
            defaults = self.get_default_config()

            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    org_defaults = config.get('organizacion_defaults', {})

                    self.logger.info(f"📖 Lecture du fichier: {self.config_file}")
                    self.logger.info(f"📖 Contenu brut org_defaults: {org_defaults}")

                    # Fusionner : defaults + valeurs existantes (les existantes ont priorité)
                    merged = defaults.copy()
                    merged.update(org_defaults)

                    self.logger.info(f"📖 Chargement config.json - nombre dans org_defaults: '{org_defaults.get('nombre', 'N/A')}'")
                    self.logger.info(f"📖 Chargement config.json - nombre dans merged: '{merged.get('nombre', 'N/A')}'")

                    # NE PAS réécrire le fichier lors du chargement
                    # Cela cause des problèmes avec les tests et écrase les données utilisateur
                    # La sauvegarde se fait uniquement via save_all_to_config_json()

                    return merged
            else:
                # Créer le fichier avec les valeurs par défaut
                self.logger.info("Création de config.json avec les valeurs par défaut")
                os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
                config = {'organizacion_defaults': defaults}
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                return defaults

        except Exception as e:
            self.logger.error(f"Erreur chargement config.json: {e}")
            return self.get_default_config()

    def save_all_to_config_json(self, organizacion_data):
        """Sauvegarder TOUTES les données de l'organisation dans config.json"""
        try:
            self.logger.info(f"💾 save_all_to_config_json appelé - nombre à sauvegarder: '{organizacion_data.get('nombre', 'N/A')}'")
            self.logger.info(f"💾 Fichier cible: {self.config_file}")

            # Créer le répertoire si nécessaire
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            # Charger le fichier existant ou créer un nouveau
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"💾 Fichier existant chargé - nombre actuel: '{config.get('organizacion_defaults', {}).get('nombre', 'N/A')}'")

            # Mettre à jour toutes les valeurs dans organizacion_defaults
            config['organizacion_defaults'] = organizacion_data
            self.logger.info(f"💾 Config mise à jour - nombre dans config: '{config['organizacion_defaults'].get('nombre', 'N/A')}'")

            # Sauvegarder
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            # Vérifier immédiatement après l'écriture
            with open(self.config_file, 'r', encoding='utf-8') as f:
                verification = json.load(f)
            self.logger.info(f"✅ Fichier écrit et vérifié - nombre dans fichier: '{verification.get('organizacion_defaults', {}).get('nombre', 'N/A')}'")

            self.logger.info("Config.json sauvegardé avec succès (toutes les données)")
            return True
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde config.json: {e}")
            return False

    def save_config_json(self, condiciones_pago, informacion_legal):
        """Sauvegarder condiciones_pago et informacion_legal dans config.json (DEPRECATED - utiliser save_all_to_config_json)"""
        try:
            # Charger le fichier existant
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

            # Mettre à jour les valeurs
            if 'organizacion_defaults' not in config:
                config['organizacion_defaults'] = {}

            config['organizacion_defaults']['condiciones_pago'] = condiciones_pago
            config['organizacion_defaults']['informacion_legal'] = informacion_legal

            # Sauvegarder
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            self.logger.info("Config.json sauvegardé avec succès")
            return True
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde config.json: {e}")
            return False

    def load_organizacion(self):
        """Charger les données de l'organisation depuis config.json UNIQUEMENT"""
        import traceback
        self.logger.info(f"🔄 load_organizacion() appelé depuis:\n{''.join(traceback.format_stack()[-3:-1])}")

        try:
            # Charger les données depuis config.json (source unique de vérité)
            config_data = self.load_config_json()

            if config_data:
                self.logger.info("Chargement de la configuration depuis config.json")
                self.load_organization_data(config_data)
            else:
                # Aucune donnée disponible, formulaire vide
                self.logger.warning("Aucune configuration trouvée dans config.json")
                self.clear_form()

        except Exception as e:
            self.logger.error(f"Erreur chargement organisation: {e}")
            self.show_error("Error", f"Error inesperado: {str(e)}")
            
    def load_organization_data(self, data):
        """Charger les données dans le formulaire"""
        self.logger.info(f"📝 load_organization_data appelé avec nombre: '{data.get('nombre', 'N/A')}'")

        # Bloquer temporairement tous les signaux pour éviter de déclencher data_modified
        widgets_to_block = [
            self.nombre_edit, self.cif_edit, self.telefono_edit, self.email_edit,
            self.direccion_edit, self.logo_path_edit, self.numero_factura_edit,
            self.images_dir_edit, self.logos_storage_dir_edit, self.pdfs_dir_edit,
            self.informes_dir_edit, self.condiciones_pago_edit, self.informacion_legal_edit
        ]

        # Bloquer les signaux
        for widget in widgets_to_block:
            widget.blockSignals(True)

        try:
            self.nombre_edit.setText(str(data.get('nombre', '')))
            self.logger.info(f"✅ Widget nombre_edit défini à: '{self.nombre_edit.text()}'")
            self.cif_edit.setText(str(data.get('cif', '')))
            self.telefono_edit.setText(str(data.get('telefono', '')))
            self.email_edit.setText(str(data.get('email', '')))
            self.direccion_edit.setPlainText(str(data.get('direccion', '')))
            self.logo_path_edit.setText(str(data.get('logo_path', '')))
            self.numero_factura_edit.setText(str(data.get('numero_factura_inicial', '1')))

            # Charger l'orientation du logo (nouveau champ)
            logo_orientation = data.get('logo_orientation', 'landscape')
            self.set_logo_orientation(logo_orientation)

            # Charger les répertoires
            self.images_dir_edit.setText(str(data.get('directorio_imagenes_defecto', '')))
            self.logos_storage_dir_edit.setText(str(data.get('directorio_logos_storage', '')))
            self.pdfs_dir_edit.setText(str(data.get('directorio_descargas_pdf', '')))
            self.informes_dir_edit.setText(str(data.get('directorio_informes', '')))

            # Charger les conditions de paiement et informations légales
            self.condiciones_pago_edit.setPlainText(str(data.get('condiciones_pago', '')))
            self.informacion_legal_edit.setPlainText(str(data.get('informacion_legal', '')))

            # Charger les flags de visibilité (par défaut à True/1)
            condiciones_visible = data.get('condiciones_pago_visible', 1)
            informacion_visible = data.get('informacion_legal_visible', 1)
            self.condiciones_pago_visible_checkbox.setChecked(bool(condiciones_visible))
            self.informacion_legal_visible_checkbox.setChecked(bool(informacion_visible))

            # Mettre à jour l'aperçu du logo
            self.update_logo_preview()

            self.logger.info(f"✅ Fin load_organization_data - Widget nombre_edit contient: '{self.nombre_edit.text()}'")

        finally:
            # Débloquer les signaux
            for widget in widgets_to_block:
                widget.blockSignals(False)

            self.logger.info(f"✅ Signaux débloqués - Widget nombre_edit contient: '{self.nombre_edit.text()}'")


            # Maintenant marquer comme non modifié
            self.set_data_modified(False)
        
    def clear_form(self):
        """Vider le formulaire"""
        # Bloquer temporairement tous les signaux pour éviter de déclencher data_modified
        widgets_to_block = [
            self.nombre_edit, self.cif_edit, self.telefono_edit, self.email_edit,
            self.direccion_edit, self.logo_path_edit, self.numero_factura_edit,
            self.images_dir_edit, self.logos_storage_dir_edit, self.pdfs_dir_edit,
            self.informes_dir_edit
        ]

        # Bloquer les signaux
        for widget in widgets_to_block:
            widget.blockSignals(True)

        try:
            self.nombre_edit.clear()
            self.cif_edit.clear()
            self.telefono_edit.clear()
            self.email_edit.clear()
            self.direccion_edit.clear()
            self.logo_path_edit.clear()
            self.numero_factura_edit.setText("1")
            self.images_dir_edit.clear()
            self.logos_storage_dir_edit.clear()
            self.pdfs_dir_edit.clear()
            self.informes_dir_edit.clear()

        finally:
            # Débloquer les signaux
            for widget in widgets_to_block:
                widget.blockSignals(False)

            # Maintenant marquer comme non modifié
            self.set_data_modified(False)

    def browse_logo(self):
        """Parcourir pour sélectionner un logo"""
        print("DEBUG: browse_logo() appelée")
        try:
            # Utiliser le répertoire d'images par défaut s'il est défini
            start_dir = self.images_dir_edit.text().strip()
            if not start_dir or not os.path.exists(start_dir):
                start_dir = ""

            # Utiliser le dialogue natif pour éviter les problèmes de fermeture
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Seleccionar Logo")
            dialog.setFileMode(QFileDialog.ExistingFile)
            dialog.setNameFilter("Imágenes (*.png *.jpg *.jpeg *.gif *.bmp);;Todos los archivos (*)")
            dialog.setViewMode(QFileDialog.Detail)
            dialog.setOption(QFileDialog.DontUseNativeDialog, False)  # Utiliser le dialogue natif

            if start_dir:
                dialog.setDirectory(start_dir)

            if dialog.exec_() == QFileDialog.Accepted:
                selected_files = dialog.selectedFiles()
                file_path = selected_files[0] if selected_files else ""
            else:
                file_path = ""

            print(f"DEBUG: Fichier sélectionné: {file_path}")
            if file_path:
                # Copier le logo dans le répertoire de stockage s'il est défini
                final_logo_path = self.copy_logo_to_storage(file_path)

                # Bloquer temporairement les signaux pour éviter la double ouverture
                self.logo_path_edit.blockSignals(True)
                self.logo_path_edit.setText(final_logo_path)
                self.logo_path_edit.blockSignals(False)

                # Mettre à jour manuellement l'aperçu
                self.update_logo_preview()
                self.set_data_modified(True)

                print(f"DEBUG: Chemin final du logo: {final_logo_path}")
        except Exception as e:
            print(f"DEBUG: Erreur dans browse_logo: {e}")
            self.logger.error(f"Erreur sélection logo: {e}")

    def on_orientation_changed(self):
        """Gérer le changement d'orientation du logo"""
        self.update_logo_preview()
        self.set_data_modified(True)

    def on_logo_path_changed(self):
        """Gérer le changement du chemin du logo"""
        self.set_data_modified(True)
        self.update_logo_preview()

    def copy_logo_to_storage(self, source_path):
        """Copier le logo dans le répertoire de stockage"""
        try:
            storage_dir = self.logos_storage_dir_edit.text().strip()

            # Si pas de répertoire de stockage défini, utiliser le chemin original
            if not storage_dir:
                print("DEBUG: Pas de répertoire de stockage défini, utilisation du chemin original")
                return source_path

            # Créer le répertoire s'il n'existe pas
            if not os.path.exists(storage_dir):
                os.makedirs(storage_dir)
                print(f"DEBUG: Répertoire créé: {storage_dir}")

            # Générer le nom du fichier de destination
            filename = os.path.basename(source_path)
            name, ext = os.path.splitext(filename)

            # Ajouter un timestamp pour éviter les conflits
            import time
            timestamp = int(time.time())
            new_filename = f"logo_{timestamp}{ext}"

            destination_path = os.path.join(storage_dir, new_filename)

            # Copier le fichier
            shutil.copy2(source_path, destination_path)
            print(f"DEBUG: Logo copié de {source_path} vers {destination_path}")

            return destination_path

        except Exception as e:
            print(f"DEBUG: Erreur copie logo: {e}")
            self.logger.error(f"Erreur copie logo: {e}")
            return source_path  # Retourner le chemin original en cas d'erreur

    def browse_images_directory(self):
        """Parcourir pour sélectionner le répertoire d'images par défaut"""
        try:
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Seleccionar Directorio de Imágenes")
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setOption(QFileDialog.DontUseNativeDialog, False)

            current_dir = self.images_dir_edit.text().strip()
            if current_dir and os.path.exists(current_dir):
                dialog.setDirectory(current_dir)

            if dialog.exec_() == QFileDialog.Accepted:
                selected_dirs = dialog.selectedFiles()
                directory = selected_dirs[0] if selected_dirs else ""
                if directory:
                    self.images_dir_edit.setText(directory)
                    print(f"DEBUG: Répertoire d'images défini: {directory}")
        except Exception as e:
            self.logger.error(f"Erreur sélection répertoire images: {e}")

    def browse_logos_storage_directory(self):
        """Parcourir pour sélectionner le répertoire de stockage des logos"""
        try:
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Seleccionar Directorio de Almacenamiento de Logos")
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setOption(QFileDialog.DontUseNativeDialog, False)

            current_dir = self.logos_storage_dir_edit.text().strip()
            if current_dir and os.path.exists(current_dir):
                dialog.setDirectory(current_dir)

            if dialog.exec_() == QFileDialog.Accepted:
                selected_dirs = dialog.selectedFiles()
                directory = selected_dirs[0] if selected_dirs else ""
                if directory:
                    self.logos_storage_dir_edit.setText(directory)
                    print(f"DEBUG: Répertoire de stockage logos défini: {directory}")
        except Exception as e:
            self.logger.error(f"Erreur sélection répertoire logos: {e}")

    def browse_pdfs_directory(self):
        """Parcourir pour sélectionner le répertoire des PDFs"""
        try:
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Seleccionar Directorio de PDFs")
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setOption(QFileDialog.DontUseNativeDialog, False)

            current_dir = self.pdfs_dir_edit.text().strip()
            if current_dir and os.path.exists(current_dir):
                dialog.setDirectory(current_dir)

            if dialog.exec_() == QFileDialog.Accepted:
                selected_dirs = dialog.selectedFiles()
                directory = selected_dirs[0] if selected_dirs else ""
                if directory:
                    self.pdfs_dir_edit.setText(directory)
                    print(f"DEBUG: Répertoire PDFs défini: {directory}")
        except Exception as e:
            self.logger.error(f"Erreur sélection répertoire PDFs: {e}")

    def browse_informes_directory(self):
        """Parcourir pour sélectionner le répertoire des Informes"""
        try:
            dialog = QFileDialog(self)
            dialog.setWindowTitle("Seleccionar Directorio de Informes")
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setOption(QFileDialog.ShowDirsOnly, True)
            dialog.setOption(QFileDialog.DontUseNativeDialog, False)

            current_dir = self.informes_dir_edit.text().strip()
            if current_dir and os.path.exists(current_dir):
                dialog.setDirectory(current_dir)

            if dialog.exec_() == QFileDialog.Accepted:
                selected_dirs = dialog.selectedFiles()
                directory = selected_dirs[0] if selected_dirs else ""
                if directory:
                    self.informes_dir_edit.setText(directory)
                    print(f"DEBUG: Répertoire Informes défini: {directory}")
        except Exception as e:
            self.logger.error(f"Erreur sélection répertoire Informes: {e}")

    def get_logo_orientation(self):
        """Obtenir l'orientation sélectionnée"""
        return "landscape" if self.logo_landscape_radio.isChecked() else "portrait"

    def set_logo_orientation(self, orientation):
        """Définir l'orientation du logo"""
        if orientation == "portrait":
            self.logo_portrait_radio.setChecked(True)
        else:
            self.logo_landscape_radio.setChecked(True)

    def update_logo_preview(self):
        """Mettre à jour l'aperçu du logo"""
        # Éviter les appels multiples simultanés
        if hasattr(self, '_updating_preview') and self._updating_preview:
            return

        self._updating_preview = True
        try:
            logo_path = self.logo_path_edit.text().strip()
            if logo_path and os.path.exists(logo_path):
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    # Obtenir l'orientation sélectionnée
                    is_portrait = self.logo_portrait_radio.isChecked()

                    # Appliquer la rotation si nécessaire
                    if is_portrait:
                        # Rotation de 90° pour passer en portrait
                        transform = QTransform()
                        transform.rotate(90)
                        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

                    # Redimensionner en gardant les proportions dans le conteneur carré
                    preview_size = self.logo_preview.size()
                    scaled_pixmap = pixmap.scaled(
                        preview_size,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )

                    self.logo_preview.setPixmap(scaled_pixmap)
                    self.logo_preview.setText("")

                    # Afficher info sur l'orientation
                    orientation_text = "Portrait (90°)" if is_portrait else "Landscape"
                    print(f"DEBUG: Logo affiché en {orientation_text}")

                else:
                    self.logo_preview.clear()
                    self.logo_preview.setText("Image non\nvalide")
            else:
                self.logo_preview.clear()
                self.logo_preview.setText("Sin logo\nseleccionado")
        except Exception as e:
            self.logger.error(f"Erreur mise à jour aperçu logo: {e}")
            self.logo_preview.clear()
            self.logo_preview.setText("Erreur\nchargement")
        finally:
            self._updating_preview = False

    def save_organizacion(self):
        """Sauvegarder la configuration de l'organisation dans config.json ET la base de données"""
        try:
            self.logger.info(f"💾 save_organizacion() appelé - Widget nombre_edit contient: '{self.nombre_edit.text()}'")

            # Validation basique
            if not self.nombre_edit.text().strip():
                self.show_warning("Validation", "Le nom de l'entreprise est requis")
                return

            # Préparer les données pour config.json
            organizacion_data = {
                'nombre': self.nombre_edit.text().strip(),
                'cif': self.cif_edit.text().strip(),
                'telefono': self.telefono_edit.text().strip(),
                'email': self.email_edit.text().strip(),
                'direccion': self.direccion_edit.toPlainText().strip(),
                'logo_path': self.logo_path_edit.text().strip(),
                'logo_orientation': self.get_logo_orientation(),
                'numero_factura_inicial': self.numero_factura_edit.text().strip() or '1',
                'directorio_imagenes_defecto': self.images_dir_edit.text().strip(),
                'directorio_logos_storage': self.logos_storage_dir_edit.text().strip(),
                'directorio_descargas_pdf': self.pdfs_dir_edit.text().strip(),
                'directorio_informes': self.informes_dir_edit.text().strip(),
                'condiciones_pago': self.condiciones_pago_edit.toPlainText().strip(),
                'informacion_legal': self.informacion_legal_edit.toPlainText().strip(),
                'condiciones_pago_visible': 1 if self.condiciones_pago_visible_checkbox.isChecked() else 0,
                'informacion_legal_visible': 1 if self.informacion_legal_visible_checkbox.isChecked() else 0
            }

            self.logger.info(f"💾 Données préparées - nombre: '{organizacion_data.get('nombre')}'")

            # Sauvegarder dans config.json
            config_saved = self.save_all_to_config_json(organizacion_data)
            
            # Sauvegarder aussi dans la base de données pour la numérotation des factures
            db_saved = self._save_organizacion_to_database(organizacion_data)
            
            if config_saved and db_saved:
                self.logger.info("💾 Sauvegarde réussie (config.json + base de données)")
                self.show_info("Éxito", "Configuración actualizada correctamente")
                # Recharger les données
                self.logger.info("💾 Rechargement des données avec load_organizacion()")
                self.load_organizacion()
                self.logger.info(f"💾 Après rechargement - Widget nombre_edit contient: '{self.nombre_edit.text()}'")
                self.organizacion_updated.emit()
            else:
                self.show_error("Error", "Error al guardar la configuración")

        except Exception as e:
            self.logger.error(f"Erreur sauvegarde organisation: {e}")
            self.show_error("Error", f"Error inesperado: {str(e)}")
    
    def _save_organizacion_to_database(self, organizacion_data):
        """
        Sauvegarde les données d'organisation dans la base de données.
        Nécessaire pour que le numéro de facture initial soit utilisé.
        
        ⚠️ PRODUCTION: Utilise db (base de données de production)
        """
        try:
            # Préparer les données pour la base de données
            db_data = {
                'nombre': organizacion_data.get('nombre', ''),
                'direccion': organizacion_data.get('direccion', ''),
                'telefono': organizacion_data.get('telefono', ''),
                'email': organizacion_data.get('email', ''),
                'cif': organizacion_data.get('cif', ''),
                'logo_path': organizacion_data.get('logo_path', ''),
                'logo_orientation': organizacion_data.get('logo_orientation', 'landscape'),
                'numero_factura_inicial': organizacion_data.get('numero_factura_inicial', '1'),
                'directorio_imagenes_defecto': organizacion_data.get('directorio_imagenes_defecto', ''),
                'directorio_logos_storage': organizacion_data.get('directorio_logos_storage', ''),
                'directorio_descargas_pdf': organizacion_data.get('directorio_descargas_pdf', ''),
                'visor_pdf_personalizado': organizacion_data.get('visor_pdf_personalizado', ''),
            }
            
            # Utiliser le service d'organisation
            org_service = OrganizacionService(db)
            
            # Vérifier si l'organisation existe déjà
            existing = org_service.get_organizacion()
            
            if existing and existing.get('id'):
                # Mettre à jour
                db_data['id'] = existing['id']
                success = org_service.update_organizacion(db_data)
                self.logger.info(f"💾 Organisation mise à jour dans la base de données: {success}")
            else:
                # Créer
                success = org_service.create_organizacion(db_data)
                self.logger.info(f"💾 Organisation créée dans la base de données: {success}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur sauvegarde organisation dans la DB: {e}")
            # Ne pas bloquer la sauvegarde dans config.json si la DB échoue
            # mais retourner False pour informer
            return False

    # ==================== MÉTODOS PARA ESTADOS DE FACTURAS ====================

    def load_invoice_statuses(self):
        """Cargar los estados de facturas en la tabla"""
        try:
            statuses = invoice_status_manager.get_all_statuses()

            self.statuses_table.setRowCount(len(statuses))

            for row, status in enumerate(statuses):
                # Nombre del estado
                name_item = QTableWidgetItem(status['nombre'])
                name_item.setData(Qt.UserRole, status['id'])  # Guardar ID
                self.statuses_table.setItem(row, 0, name_item)

                # Descripción
                desc_item = QTableWidgetItem(status['descripcion'])
                self.statuses_table.setItem(row, 1, desc_item)

                # Permite modificación (checkbox)
                checkbox = QCheckBox()
                checkbox.setChecked(status['permite_modificacion'])
                checkbox.setEnabled(False)  # Solo lectura en la tabla
                self.statuses_table.setCellWidget(row, 2, checkbox)

                # Color (widget con color de fondo)
                color_widget = QLabel()
                color_widget.setFixedSize(30, 18)  # Taille réduite pour éviter débordement
                color_widget.setStyleSheet(f"""
                    QLabel {{
                        background-color: {status['color']};
                        border: 1px solid #999;
                        border-radius: 2px;
                        margin: 1px;
                    }}
                """)
                color_widget.setToolTip(f"Color: {status['color']}")  # Tooltip informatif
                self.statuses_table.setCellWidget(row, 3, color_widget)

                # Orden
                order_item = QTableWidgetItem(str(status['orden']))
                self.statuses_table.setItem(row, 4, order_item)

            self.logger.info(f"Cargados {len(statuses)} estados de facturas")

        except Exception as e:
            self.logger.error(f"Error cargando estados de facturas: {e}")
            self.show_error("Error", f"Error al cargar estados: {str(e)}")

    def add_invoice_status(self):
        """Agregar un nuevo estado de factura"""
        try:
            from ui.invoice_status_dialog_pyqt5 import InvoiceStatusDialogPyQt5

            dialog = InvoiceStatusDialogPyQt5(self)
            if dialog.exec_() == dialog.Accepted:
                # Recargar la tabla
                self.load_invoice_statuses()
                self.show_info("Éxito", "Estado agregado correctamente")

        except Exception as e:
            self.logger.error(f"Error agregando estado: {e}")
            self.show_error("Error", f"Error al agregar estado: {str(e)}")

    def edit_invoice_status(self):
        """Editar el estado seleccionado"""
        try:
            current_row = self.statuses_table.currentRow()
            if current_row < 0:
                self.show_warning("Selección", "Por favor seleccione un estado para editar")
                return

            # Obtener el ID del estado
            name_item = self.statuses_table.item(current_row, 0)
            status_id = name_item.data(Qt.UserRole)

            # Obtener los datos del estado
            status_data = {
                'id': status_id,
                'nombre': self.statuses_table.item(current_row, 0).text(),
                'descripcion': self.statuses_table.item(current_row, 1).text(),
                'permite_modificacion': self.statuses_table.cellWidget(current_row, 2).isChecked(),
                'orden': int(self.statuses_table.item(current_row, 4).text())
            }

            from ui.invoice_status_dialog_pyqt5 import InvoiceStatusDialogPyQt5

            dialog = InvoiceStatusDialogPyQt5(self, status_data)
            if dialog.exec_() == dialog.Accepted:
                # Recargar la tabla
                self.load_invoice_statuses()
                self.show_info("Éxito", "Estado actualizado correctamente")

        except Exception as e:
            self.logger.error(f"Error editando estado: {e}")
            self.show_error("Error", f"Error al editar estado: {str(e)}")

    def delete_invoice_status(self):
        """Eliminar el estado seleccionado"""
        try:
            current_row = self.statuses_table.currentRow()
            if current_row < 0:
                self.show_warning("Selección", "Por favor seleccione un estado para eliminar")
                return

            # Obtener el nombre del estado
            status_name = self.statuses_table.item(current_row, 0).text()

            # Confirmar eliminación
            reply = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                f"¿Está seguro de que desea eliminar el estado '{status_name}'?\n\n"
                "Esta acción no se puede deshacer.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Obtener el ID del estado
                name_item = self.statuses_table.item(current_row, 0)
                status_id = name_item.data(Qt.UserRole)

                # Eliminar el estado
                if invoice_status_manager.delete_status(status_id):
                    # Recargar la tabla
                    self.load_invoice_statuses()
                    self.show_info("Éxito", "Estado eliminado correctamente")
                else:
                    self.show_error("Error", "No se pudo eliminar el estado")

        except Exception as e:
            self.logger.error(f"Error eliminando estado: {e}")
            self.show_error("Error", f"Error al eliminar estado: {str(e)}")

    def open_todo_editor(self):
        """Abre el editor de TODO"""
        try:
            self.logger.info("Abriendo editor de TODO")

            # Crear y mostrar el diálogo
            dialog = TodoEditorDialog(self)
            result = dialog.exec_()

            if result == dialog.Accepted:
                self.logger.info("TODO editado y guardado")
                # Message de confirmation unique
                self.show_info("TODO Actualizado",
                             "El archivo TODO.md ha sido actualizado exitosamente.")
            else:
                self.logger.info("Edición de TODO cancelada")

        except Exception as e:
            self.logger.error(f"Error abriendo editor de TODO: {e}")
            self.show_error("Error", f"Error al abrir el editor de TODO: {str(e)}")

    def open_data_cleanup_dialog(self):
        """Abre el diálogo de limpieza de datos"""
        try:
            self.logger.info("Abriendo diálogo de limpieza de datos")

            # Crear y mostrar el diálogo
            dialog = DataCleanupDialog(self)
            result = dialog.exec_()

            if result == dialog.Accepted:
                self.logger.info("Limpieza de datos completada")
                # Opcional: mostrar mensaje de confirmación
                self.show_info("Limpieza Completada",
                             "La limpieza de datos se ha completado exitosamente.")
            else:
                self.logger.info("Limpieza de datos cancelada")

        except Exception as e:
            self.logger.error(f"Error abriendo diálogo de limpieza: {e}")
            self.show_error("Error", f"Error al abrir el diálogo de limpieza: {str(e)}")
