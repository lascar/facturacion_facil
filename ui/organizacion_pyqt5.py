# -*- coding: utf-8 -*-
"""
Fenêtre de configuration de l'organisation - Version PyQt5 native
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QGroupBox, QFrame, QWidget, QTextEdit, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal as Signal
from PyQt5.QtGui import QFont

from ui.base_pyqt5_window import BasePyQt5Window
from database.database import db
from utils.logger import get_logger

class OrganizacionPyQt5Window(BasePyQt5Window):
    """Fenêtre de configuration de l'organisation avec PyQt5"""
    
    # Signaux
    organizacion_updated = Signal()
    
    def __init__(self, parent=None):
        self.logger = get_logger(self.__class__.__name__)
        super().__init__(parent, "Configuración de la Organización", 800, 600)
        
        # Variables
        self.organizacion_data = {}
        
        # Charger les données
        self.load_organizacion()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Titre
        title_label = QLabel("Configuración de la Empresa")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # Configuration des sections
        self.setup_company_form(main_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Guardar Configuración")
        self.reset_btn = QPushButton("🔄 Restablecer")
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.reset_btn)
        buttons_layout.addStretch()
        
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
        
        # GroupBox pour la configuration
        config_group = QGroupBox("Configuración")
        config_layout = QGridLayout(config_group)
        
        self.logo_path_edit = QLineEdit()
        self.logo_browse_btn = QPushButton("📁 Buscar")
        
        self.numero_factura_edit = QLineEdit()
        self.numero_factura_edit.setPlaceholderText("Ej: 1")
        
        config_layout.addWidget(QLabel("Logo de la Empresa:"), 0, 0)
        config_layout.addWidget(self.logo_path_edit, 0, 1)
        config_layout.addWidget(self.logo_browse_btn, 0, 2)
        
        config_layout.addWidget(QLabel("Número Inicial de Factura:"), 1, 0)
        config_layout.addWidget(self.numero_factura_edit, 1, 1)
        
        parent_layout.addWidget(config_group)
        
    def setup_connections(self):
        """Configurer les connexions de signaux"""
        self.save_btn.clicked.connect(self.save_organizacion)
        self.reset_btn.clicked.connect(self.load_organizacion)
        self.logo_browse_btn.clicked.connect(self.browse_logo)
        
        # Connecter les changements de données
        self.nombre_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.cif_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.telefono_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.email_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.direccion_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.logo_path_edit.textChanged.connect(lambda: self.set_data_modified(True))
        self.numero_factura_edit.textChanged.connect(lambda: self.set_data_modified(True))
        
    def load_organizacion(self):
        """Charger les données de l'organisation depuis la base de données"""
        try:
            self.organizacion_data = db.get_organization_info()
            if self.organizacion_data:
                self.load_organization_data(self.organizacion_data)
            else:
                # Données par défaut si aucune organisation n'existe
                self.clear_form()
        except Exception as e:
            self.logger.error(f"Erreur chargement organisation: {e}")
            self.show_error("Erreur", f"Impossible de charger les données: {str(e)}")
            
    def load_organization_data(self, data):
        """Charger les données dans le formulaire"""
        self.nombre_edit.setText(str(data.get('nombre', '')))
        self.cif_edit.setText(str(data.get('cif', '')))
        self.telefono_edit.setText(str(data.get('telefono', '')))
        self.email_edit.setText(str(data.get('email', '')))
        self.direccion_edit.setPlainText(str(data.get('direccion', '')))
        self.logo_path_edit.setText(str(data.get('logo_path', '')))
        self.numero_factura_edit.setText(str(data.get('numero_factura_inicial', '1')))
        self.set_data_modified(False)
        
    def clear_form(self):
        """Vider le formulaire"""
        self.nombre_edit.clear()
        self.cif_edit.clear()
        self.telefono_edit.clear()
        self.email_edit.clear()
        self.direccion_edit.clear()
        self.logo_path_edit.clear()
        self.numero_factura_edit.setText("1")
        self.set_data_modified(False)

    def browse_logo(self):
        """Parcourir pour sélectionner un logo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Logo",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            self.logo_path_edit.setText(file_path)

    def save_organizacion(self):
        """Sauvegarder la configuration de l'organisation"""
        try:
            # Validation basique
            if not self.nombre_edit.text().strip():
                self.show_warning("Validation", "Le nom de l'entreprise est requis")
                return

            # Préparer les données
            organizacion_data = {
                'nombre': self.nombre_edit.text().strip(),
                'cif': self.cif_edit.text().strip(),
                'telefono': self.telefono_edit.text().strip(),
                'email': self.email_edit.text().strip(),
                'direccion': self.direccion_edit.toPlainText().strip(),
                'logo_path': self.logo_path_edit.text().strip(),
                'numero_factura_inicial': self.numero_factura_edit.text().strip() or '1'
            }

            # Sauvegarder
            if self.organizacion_data and self.organizacion_data.get('id'):
                # Mise à jour
                organizacion_data['id'] = self.organizacion_data['id']
                db.update_organization(organizacion_data)
                self.show_info("Éxito", "Configuración actualizada correctamente")
            else:
                # Nouvelle organisation
                db.create_organization(organizacion_data)
                self.show_info("Éxito", "Configuración creada correctamente")

            # Recharger les données
            self.load_organizacion()
            self.organizacion_updated.emit()

        except Exception as e:
            self.logger.error(f"Erreur sauvegarde organisation: {e}")
            self.show_error("Error", f"Error al guardar la configuración: {str(e)}")
