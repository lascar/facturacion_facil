#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialogue de configuration des états de factures - Version PyQt5
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QLineEdit, QTextEdit, QPushButton, QCheckBox, QSpinBox,
    QColorDialog, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from utils.logger import get_logger
from utils.invoice_status_manager import invoice_status_manager


class InvoiceStatusDialogPyQt5(QDialog):
    """Dialogue pour créer/éditer un état de facture"""
    
    def __init__(self, parent=None, status_data=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.status_data = status_data or {}
        self.selected_color = self.status_data.get('color', '#007bff')
        
        self.setWindowTitle("Configurar Estado de Factura")
        self.setModal(True)
        self.resize(500, 400)
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = "Editar Estado" if self.status_data.get('id') else "Nuevo Estado"
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Formulaire
        form_layout = QGridLayout()
        
        # Nom de l'état
        form_layout.addWidget(QLabel("Nombre del Estado:"), 0, 0)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ej: Borrador, Enviada, Pagada...")
        form_layout.addWidget(self.name_edit, 0, 1)
        
        # Description
        form_layout.addWidget(QLabel("Descripción:"), 1, 0)
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText("Descripción del estado...")
        form_layout.addWidget(self.description_edit, 1, 1)
        
        # Permet modification
        form_layout.addWidget(QLabel("Permite Modificación:"), 2, 0)
        self.allow_modification_cb = QCheckBox("Permitir editar facturas en este estado")
        self.allow_modification_cb.setChecked(True)
        form_layout.addWidget(self.allow_modification_cb, 2, 1)
        
        # Couleur
        form_layout.addWidget(QLabel("Color:"), 3, 0)
        color_layout = QHBoxLayout()
        
        self.color_preview = QPushButton()
        self.color_preview.setFixedSize(50, 30)
        self.color_preview.clicked.connect(self.choose_color)
        
        self.color_choose_btn = QPushButton("🎨 Elegir Color")
        self.color_choose_btn.clicked.connect(self.choose_color)
        
        color_layout.addWidget(self.color_preview)
        color_layout.addWidget(self.color_choose_btn)
        color_layout.addStretch()
        
        color_widget = QFrame()
        color_widget.setLayout(color_layout)
        form_layout.addWidget(color_widget, 3, 1)
        
        # Ordre
        form_layout.addWidget(QLabel("Orden:"), 4, 0)
        self.order_spin = QSpinBox()
        self.order_spin.setMinimum(1)
        self.order_spin.setMaximum(100)
        self.order_spin.setValue(1)
        form_layout.addWidget(self.order_spin, 4, 1)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Guardar")
        self.save_btn.clicked.connect(self.save_status)
        
        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # Appliquer le style
        self.apply_style()
        
    def apply_style(self):
        """Appliquer le style au dialogue"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-weight: bold;
                color: #495057;
            }
            QLineEdit, QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QCheckBox {
                font-size: 12px;
                color: #495057;
            }
            QSpinBox {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        
        # Mettre à jour la couleur de prévisualisation
        self.update_color_preview()
        
    def update_color_preview(self):
        """Mettre à jour la prévisualisation de couleur"""
        self.color_preview.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.selected_color};
                border: 2px solid #dee2e6;
                border-radius: 6px;
            }}
        """)
        
    def choose_color(self):
        """Ouvrir le dialogue de sélection de couleur"""
        color = QColorDialog.getColor(QColor(self.selected_color), self)
        if color.isValid():
            self.selected_color = color.name()
            self.update_color_preview()
            
    def load_data(self):
        """Charger les données de l'état à éditer"""
        if self.status_data.get('id'):
            self.name_edit.setText(self.status_data.get('nombre', ''))
            self.description_edit.setPlainText(self.status_data.get('descripcion', ''))
            self.allow_modification_cb.setChecked(self.status_data.get('permite_modificacion', True))
            self.selected_color = self.status_data.get('color', '#007bff')
            self.order_spin.setValue(self.status_data.get('orden', 1))
            self.update_color_preview()
            
    def save_status(self):
        """Sauvegarder l'état de facture"""
        try:
            # Validation des données
            name = self.name_edit.text().strip()
            if not name:
                QMessageBox.warning(self, "Validación", "El nombre del estado es obligatorio")
                return
            
            description = self.description_edit.toPlainText().strip()
            if not description:
                description = name
            
            # Préparer les données
            status_data = {
                'nombre': name,
                'descripcion': description,
                'permite_modificacion': self.allow_modification_cb.isChecked(),
                'color': self.selected_color,
                'orden': self.order_spin.value()
            }
            
            # Si on édite, inclure l'ID
            if self.status_data.get('id'):
                status_data['id'] = self.status_data['id']
            
            # Sauvegarder
            if invoice_status_manager.save_status(status_data):
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo guardar el estado")
                
        except Exception as e:
            self.logger.error(f"Error guardando estado: {e}")
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
