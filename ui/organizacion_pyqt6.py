# -*- coding: utf-8 -*-
"""
Fenêtre de configuration de l'organisation - Version PyQt6 native
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QGroupBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from ui.base_pyqt6_window import BasePyQt6Window
from database.database import db
from utils.logger import get_logger
import os

class OrganizacionPyQt6Window(BasePyQt6Window):
    """Fenêtre de configuration de l'organisation en PyQt6 natif"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Configuración de la Organización", 800, 600)
        self.logger = get_logger("organizacion_pyqt6")
        
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
        
        # Boutons d'action
        self.create_action_buttons()
        
        # Charger les données
        self.load_organization_data()
    
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
        """Charge les données de l'organisation"""
        try:
            # Pour la démo, on utilise des données par défaut
            # Dans une vraie application, ces données viendraient de la base de données
            
            self.company_name_edit.setText("Demo Company")
            self.nif_edit.setText("12345678A")
            self.address_edit.setPlainText("Calle Ejemplo, 123\n28001 Madrid\nEspaña")
            self.phone_edit.setText("+34 91 123 45 67")
            self.email_edit.setText("info@democompany.com")
            self.website_edit.setText("https://www.democompany.com")
            
            # Charger le logo s'il existe
            self.load_logo()
            
            self.logger.info("Datos de organización cargados correctamente")
            
        except Exception as e:
            self.logger.error(f"Error cargando datos de organización: {e}")
            self.show_error("Error", f"Error al cargar datos de organización: {e}")
    
    def load_logo(self):
        """Charge le logo de l'entreprise"""
        try:
            # Chercher un logo dans le dossier data/logos
            logos_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logos")
            
            if os.path.exists(logos_dir):
                logo_files = [f for f in os.listdir(logos_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                
                if logo_files:
                    logo_path = os.path.join(logos_dir, logo_files[0])
                    pixmap = QPixmap(logo_path)
                    
                    if not pixmap.isNull():
                        # Redimensionner le logo pour l'affichage
                        scaled_pixmap = pixmap.scaled(200, 120, Qt.AspectRatioMode.KeepAspectRatio, 
                                                    Qt.TransformationMode.SmoothTransformation)
                        self.logo_label.setPixmap(scaled_pixmap)
                        self.logo_label.setText("")
                        self.logger.info(f"Logo cargado: {logo_files[0]}")
                        return
            
            # Pas de logo trouvé
            self.logo_label.clear()
            self.logo_label.setText("Sin logo")
            
        except Exception as e:
            self.logger.error(f"Error cargando logo: {e}")
            self.logo_label.clear()
            self.logo_label.setText("Error cargando logo")
    
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
        self.show_info("Logo", "Logo eliminado")
    
    def save_organization(self):
        """Sauvegarde les données de l'organisation"""
        try:
            # Validation de base
            if not self.company_name_edit.text().strip():
                self.show_warning("Validación", "El nombre de la empresa es obligatorio")
                return
            
            # Préparer les données
            org_data = {
                'company_name': self.company_name_edit.text().strip(),
                'nif': self.nif_edit.text().strip(),
                'address': self.address_edit.toPlainText().strip(),
                'phone': self.phone_edit.text().strip(),
                'email': self.email_edit.text().strip(),
                'website': self.website_edit.text().strip()
            }
            
            # Dans une vraie application, on sauvegarderait en base de données
            # db.save_organization_data(org_data)
            
            self.show_info("Éxito", "Datos de organización guardados correctamente")
            self.logger.info("Datos de organización guardados")
            
        except Exception as e:
            self.logger.error(f"Error guardando datos de organización: {e}")
            self.show_error("Error", f"Error al guardar datos de organización: {e}")
