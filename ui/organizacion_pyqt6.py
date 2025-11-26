# -*- coding: utf-8 -*-
"""
Fenêtre de configuration de l'organisation - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QGroupBox, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QCheckBox, QColorDialog, QSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ui.base_pyqt6_window import BasePyQt6Window
from database.database import db
from database.models import Organizacion
from utils.logger import get_logger
from utils.logo_manager import LogoManager
from utils.invoice_status_manager import invoice_status_manager
from ui.invoice_status_dialog import InvoiceStatusDialog
import os

class OrganizacionPyQt6Window(BasePyQt6Window):
    """Fenêtre de configuration de l'organisation en PyQt6 natif"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Configuración de la Organización", 800, 600)
        self.logger = get_logger("organizacion_pyqt6")

        # Variables pour la gestion du logo
        self.logo_manager = LogoManager()
        self.current_logo_path = None
        self.selected_logo_path = None

        self.logger.info("Inicializando ventana de configuración de organización PyQt6")
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre
        title_label = QLabel("Configuración de la Organización")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(title_label)
        
        # Informations de base
        self.create_basic_info_group()
        
        # Informations de contact
        self.create_contact_info_group()
        
        # Logo
        self.create_logo_group()

        # Configuration des statuts de factures
        self.create_invoice_statuses_group()

        # Boutons d'action
        self.create_action_buttons()
        
        # Charger les données
        self.load_organization_data()
        self.load_invoice_statuses()
    
    def create_basic_info_group(self):
        """Crée le groupe d'informations de base"""
        basic_group = QGroupBox("Información Básica")
        basic_layout = QGridLayout(basic_group)
        
        # Nom de l'entreprise
        basic_layout.addWidget(QLabel("Nombre de la Empresa:"), 0, 0)
        self.company_name_edit = QLineEdit()
        self.company_name_edit.setPlaceholderText("Nombre de su empresa")
        basic_layout.addWidget(self.company_name_edit, 0, 1)
        
        # NIF/CIF
        basic_layout.addWidget(QLabel("NIF/CIF:"), 1, 0)
        self.nif_edit = QLineEdit()
        self.nif_edit.setPlaceholderText("Número de identificación fiscal")
        basic_layout.addWidget(self.nif_edit, 1, 1)
        
        # Adresse
        basic_layout.addWidget(QLabel("Dirección:"), 2, 0)
        self.address_edit = QTextEdit()
        self.address_edit.setMaximumHeight(80)
        self.address_edit.setPlaceholderText("Dirección completa de la empresa")
        basic_layout.addWidget(self.address_edit, 2, 1)
        
        self.main_layout.addWidget(basic_group)
    
    def create_contact_info_group(self):
        """Crée le groupe d'informations de contact"""
        contact_group = QGroupBox("Información de Contacto")
        contact_layout = QGridLayout(contact_group)
        
        # Téléphone
        contact_layout.addWidget(QLabel("Teléfono:"), 0, 0)
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Número de teléfono")
        contact_layout.addWidget(self.phone_edit, 0, 1)
        
        # Email
        contact_layout.addWidget(QLabel("Email:"), 1, 0)
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Dirección de correo electrónico")
        contact_layout.addWidget(self.email_edit, 1, 1)
        
        # Site web
        contact_layout.addWidget(QLabel("Sitio Web:"), 2, 0)
        self.website_edit = QLineEdit()
        self.website_edit.setPlaceholderText("https://www.ejemplo.com")
        contact_layout.addWidget(self.website_edit, 2, 1)
        
        self.main_layout.addWidget(contact_group)
    
    def create_logo_group(self):
        """Crée le groupe de gestion du logo"""
        logo_group = QGroupBox("Logo de la Empresa")
        logo_layout = QVBoxLayout(logo_group)
        
        # Zone d'affichage du logo
        self.logo_label = QLabel("Sin logo")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setMinimumHeight(150)
        self.logo_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #ccc;
                border-radius: 8px;
                background-color: #f9f9f9;
                color: #666;
            }
        """)
        logo_layout.addWidget(self.logo_label)
        
        # Boutons de gestion du logo
        logo_buttons_layout = QHBoxLayout()
        
        select_logo_btn = QPushButton("Seleccionar Logo")
        select_logo_btn.clicked.connect(self.select_logo)
        logo_buttons_layout.addWidget(select_logo_btn)
        
        remove_logo_btn = QPushButton("Quitar Logo")
        remove_logo_btn.clicked.connect(self.remove_logo)
        logo_buttons_layout.addWidget(remove_logo_btn)
        
        logo_buttons_layout.addStretch()
        logo_layout.addLayout(logo_buttons_layout)
        
        self.main_layout.addWidget(logo_group)

    def create_invoice_statuses_group(self):
        """Crée le groupe de configuration des statuts de factures"""
        statuses_group = QGroupBox("Configuración de Estados de Facturas")
        statuses_layout = QVBoxLayout(statuses_group)

        # Description
        desc_label = QLabel("Configure los estados posibles para las facturas y determine cuáles permiten modificación:")
        desc_label.setWordWrap(True)
        statuses_layout.addWidget(desc_label)

        # Tableau des statuts
        self.statuses_table = QTableWidget()
        self.statuses_table.setColumnCount(5)
        self.statuses_table.setHorizontalHeaderLabels([
            "Estado", "Descripción", "Permite Modificación", "Color", "Orden"
        ])

        # Ajuster les colonnes
        header = self.statuses_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        statuses_layout.addWidget(self.statuses_table)

        # Boutons pour gérer les statuts
        buttons_layout = QHBoxLayout()

        add_status_btn = QPushButton("➕ Agregar Estado")
        add_status_btn.clicked.connect(self.add_invoice_status)
        buttons_layout.addWidget(add_status_btn)

        edit_status_btn = QPushButton("✏️ Editar Estado")
        edit_status_btn.clicked.connect(self.edit_invoice_status)
        buttons_layout.addWidget(edit_status_btn)

        delete_status_btn = QPushButton("🗑️ Eliminar Estado")
        delete_status_btn.clicked.connect(self.delete_invoice_status)
        buttons_layout.addWidget(delete_status_btn)

        buttons_layout.addStretch()
        statuses_layout.addLayout(buttons_layout)

        self.main_layout.addWidget(statuses_group)

    def create_action_buttons(self):
        """Crée les boutons d'action"""
        buttons_config = [
            ("Guardar", self.save_organization, "success"),
            ("Restaurar", self.load_organization_data, "secondary"),
            ("Cerrar", self.close, "secondary")
        ]
        
        button_layout = self.create_button_layout(buttons_config)
        self.main_layout.addLayout(button_layout)
    
    def load_organization_data(self):
        """Charge les données de l'organisation depuis la base de données"""
        try:
            # Charger les données depuis la base de données
            org = Organizacion.get()

            if org:
                self.company_name_edit.setText(org.nombre or "")
                self.nif_edit.setText(org.cif or "")
                self.address_edit.setPlainText(org.direccion or "")
                self.phone_edit.setText(org.telefono or "")
                self.email_edit.setText(org.email or "")
                self.website_edit.setText("")  # Pas encore dans le modèle

                # Charger le logo s'il existe
                self.current_logo_path = org.logo_path
                self.load_logo_from_path(org.logo_path)
            else:
                # Données par défaut si aucune organisation n'existe
                self.company_name_edit.setText("")
                self.nif_edit.setText("")
                self.address_edit.setPlainText("")
                self.phone_edit.setText("")
                self.email_edit.setText("")
                self.website_edit.setText("")
                self.current_logo_path = None
                self.load_logo_from_path(None)

            self.logger.info("Datos de organización cargados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error cargando datos de organización: {e}")
            self.show_error("Error", f"Error al cargar datos de organización: {e}")
    
    def load_logo_from_path(self, logo_path):
        """Charge le logo depuis un chemin spécifique"""
        try:
            if logo_path and os.path.exists(logo_path):
                pixmap = QPixmap(logo_path)

                if not pixmap.isNull():
                    # Redimensionner le logo pour l'affichage
                    scaled_pixmap = pixmap.scaled(200, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
                    self.logo_label.setPixmap(scaled_pixmap)
                    self.logo_label.setText("")
                    self.logger.info(f"Logo cargado: {os.path.basename(logo_path)}")
                    return

            # Aucun logo ou logo non trouvé
            self.logo_label.clear()
            self.logo_label.setText("Sin logo")

        except Exception as e:
            self.logger.error(f"Error cargando logo: {e}")
            self.logo_label.clear()
            self.logo_label.setText("Sin logo")
    
    def select_logo(self):
        """Sélectionne un nouveau logo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Logo",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            try:
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    # Redimensionner et afficher
                    scaled_pixmap = pixmap.scaled(200, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                                Qt.TransformationMode.SmoothTransformation)
                    self.logo_label.setPixmap(scaled_pixmap)
                    self.logo_label.setText("")

                    # Sauvegarder le chemin du logo sélectionné
                    self.selected_logo_path = file_path

                    self.show_info("Logo", "Logo seleccionado correctamente")
                else:
                    self.show_error("Error", "No se pudo cargar la imagen seleccionada")

            except Exception as e:
                self.logger.error(f"Error seleccionando logo: {e}")
                self.show_error("Error", f"Error al seleccionar logo: {e}")
    
    def remove_logo(self):
        """Supprime le logo actuel"""
        self.logo_label.clear()
        self.logo_label.setText("Sin logo")

        # Marquer pour suppression
        self.selected_logo_path = ""  # Chaîne vide = suppression

        self.show_info("Logo", "Logo eliminado")
    
    def save_organization(self):
        """Sauvegarde les données de l'organisation"""
        try:
            # Validation de base
            if not self.company_name_edit.text().strip():
                self.show_warning("Validación", "El nombre de la empresa es obligatorio")
                return

            # Créer l'objet organisation
            org = Organizacion(
                nombre=self.company_name_edit.text().strip(),
                cif=self.nif_edit.text().strip(),
                direccion=self.address_edit.toPlainText().strip(),
                telefono=self.phone_edit.text().strip(),
                email=self.email_edit.text().strip(),
                logo_path=self.current_logo_path or ""
            )

            # Gérer le logo si un nouveau a été sélectionné
            if self.selected_logo_path is not None:
                if self.selected_logo_path == "":
                    # Suppression du logo
                    if self.current_logo_path:
                        self.logo_manager.remove_logo(self.current_logo_path)
                    org.logo_path = ""
                    self.current_logo_path = None

                elif self.selected_logo_path != self.current_logo_path:
                    # Nouveau logo sélectionné
                    company_name = org.nombre or "organization"
                    permanent_logo_path = self.logo_manager.save_logo(self.selected_logo_path, company_name)

                    if permanent_logo_path:
                        # Supprimer l'ancien logo s'il existe
                        if self.current_logo_path and self.current_logo_path != permanent_logo_path:
                            self.logo_manager.remove_logo(self.current_logo_path)

                        org.logo_path = permanent_logo_path
                        self.current_logo_path = permanent_logo_path
                        self.logger.info(f"Logo guardado: {permanent_logo_path}")
                    else:
                        self.show_error("Error", "Error al guardar el logo")
                        return

            # Sauvegarder en base de données
            org.save()

            # Nettoyer les logos orphelins
            if org.logo_path:
                self.logo_manager.cleanup_orphaned_logos(org.logo_path)

            # Réinitialiser le flag de sélection
            self.selected_logo_path = None

            self.show_info("Éxito", "Datos de organización guardados correctamente")
            self.logger.info("Datos de organización guardados")

        except Exception as e:
            self.logger.error(f"Error guardando datos de organización: {e}")
            self.show_error("Error", f"Error al guardar datos de organización: {e}")

    # ==================== MÉTODOS PARA GESTIÓN DE ESTADOS DE FACTURAS ====================

    def load_invoice_statuses(self):
        """Carga los estados de facturas en la tabla"""
        try:
            statuses = invoice_status_manager.get_all_statuses()

            self.statuses_table.setRowCount(len(statuses))

            for row, status in enumerate(statuses):
                # Nombre del estado
                name_item = QTableWidgetItem(status['nombre'])
                self.statuses_table.setItem(row, 0, name_item)

                # Descripción
                desc_item = QTableWidgetItem(status['descripcion'])
                self.statuses_table.setItem(row, 1, desc_item)

                # Permite modificación (checkbox)
                checkbox = QCheckBox()
                checkbox.setChecked(status['permite_modificacion'])
                checkbox.setEnabled(False)  # Solo lectura en la tabla
                self.statuses_table.setCellWidget(row, 2, checkbox)

                # Color (botón con color de fondo)
                color_btn = QPushButton()
                color_btn.setStyleSheet(f"background-color: {status['color']}; border: 1px solid #ccc;")
                color_btn.setMaximumSize(30, 25)
                color_btn.setEnabled(False)  # Solo lectura en la tabla
                self.statuses_table.setCellWidget(row, 3, color_btn)

                # Orden
                order_item = QTableWidgetItem(str(status['orden']))
                self.statuses_table.setItem(row, 4, order_item)

                # Guarder l'ID dans les données de l'item
                name_item.setData(32, status['id'])  # Qt.UserRole = 32

            self.logger.info(f"Cargados {len(statuses)} estados de facturas")

        except Exception as e:
            self.logger.error(f"Error cargando estados de facturas: {e}")
            self.show_error("Error", f"Error al cargar estados de facturas: {e}")

    def add_invoice_status(self):
        """Abre el diálogo para agregar un nuevo estado"""
        dialog = InvoiceStatusDialog(self)
        if dialog.exec() == 1:  # Accepted
            self.load_invoice_statuses()

    def edit_invoice_status(self):
        """Abre el diálogo para editar el estado seleccionado"""
        current_row = self.statuses_table.currentRow()
        if current_row < 0:
            self.show_warning("Selección", "Por favor seleccione un estado para editar")
            return

        # Obtener el ID del estado
        name_item = self.statuses_table.item(current_row, 0)
        status_id = name_item.data(32)  # Qt.UserRole = 32

        # Obtener los datos del estado
        status_data = {
            'id': status_id,
            'nombre': self.statuses_table.item(current_row, 0).text(),
            'descripcion': self.statuses_table.item(current_row, 1).text(),
            'permite_modificacion': self.statuses_table.cellWidget(current_row, 2).isChecked(),
            'orden': int(self.statuses_table.item(current_row, 4).text())
        }

        dialog = InvoiceStatusDialog(self, status_data)
        if dialog.exec() == 1:  # Accepted
            self.load_invoice_statuses()

    def delete_invoice_status(self):
        """Elimina el estado seleccionado"""
        current_row = self.statuses_table.currentRow()
        if current_row < 0:
            self.show_warning("Selección", "Por favor seleccione un estado para eliminar")
            return

        # Obtener el nombre y ID del estado
        name_item = self.statuses_table.item(current_row, 0)
        status_name = name_item.text()
        status_id = name_item.data(32)  # Qt.UserRole = 32

        # Confirmar eliminación
        reply = self.ask_question("Confirmar",
                                 f"¿Está seguro de que desea eliminar el estado '{status_name}'?\n\n"
                                 "Esta acción no se puede deshacer.")

        if reply:
            try:
                success = invoice_status_manager.delete_status(status_id)
                if success:
                    self.show_info("Éxito", f"Estado '{status_name}' eliminado correctamente")
                    self.load_invoice_statuses()
                else:
                    self.show_error("Error", f"No se pudo eliminar el estado '{status_name}'")

            except Exception as e:
                self.logger.error(f"Error eliminando estado: {e}")
                self.show_error("Error", f"Error al eliminar estado: {e}")
