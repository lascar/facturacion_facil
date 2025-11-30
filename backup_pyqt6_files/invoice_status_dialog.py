#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diálogo para configurar estados de facturas
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QCheckBox, QSpinBox, QColorDialog, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from utils.logger import get_logger
from utils.invoice_status_manager import invoice_status_manager
from ui.base_pyqt6_window import BasePyQt6Window

class InvoiceStatusDialog(BasePyQt6Window):
    """Diálogo para configurar un estado de factura"""
    
    def __init__(self, parent=None, status_data=None):
        super().__init__(parent, title="Configurar Estado de Factura", width=400, height=300)
        self.logger = get_logger("invoice_status_dialog")
        self.status_data = status_data or {}
        self.selected_color = self.status_data.get('color', '#007bff')

        self.setModal(True)

        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Vérifier s'il y a déjà un layout
        if self.layout() is not None:
            # Supprimer le layout existant
            QWidget().setLayout(self.layout())

        layout = QVBoxLayout(self)
        
        # Formulario
        form_layout = QGridLayout()
        
        # Nombre del estado
        form_layout.addWidget(QLabel("Nombre del Estado:"), 0, 0)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ej: Borrador, Pendiente, Pagada...")
        form_layout.addWidget(self.name_edit, 0, 1)
        
        # Descripción
        form_layout.addWidget(QLabel("Descripción:"), 1, 0)
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        self.description_edit.setPlaceholderText("Descripción del estado...")
        form_layout.addWidget(self.description_edit, 1, 1)
        
        # Permite modificación
        form_layout.addWidget(QLabel("Permite Modificación:"), 2, 0)
        self.allow_modification_cb = QCheckBox("Las facturas con este estado pueden ser modificadas")
        form_layout.addWidget(self.allow_modification_cb, 2, 1)
        
        # Color
        form_layout.addWidget(QLabel("Color:"), 3, 0)
        color_layout = QHBoxLayout()
        self.color_btn = QPushButton("Seleccionar Color")
        self.color_btn.clicked.connect(self.select_color)
        self.color_preview = QPushButton()
        self.color_preview.setMaximumSize(30, 25)
        self.color_preview.setEnabled(False)
        color_layout.addWidget(self.color_btn)
        color_layout.addWidget(self.color_preview)
        color_layout.addStretch()
        form_layout.addLayout(color_layout, 3, 1)
        
        # Orden
        form_layout.addWidget(QLabel("Orden:"), 4, 0)
        self.order_spin = QSpinBox()
        self.order_spin.setMinimum(1)
        self.order_spin.setMaximum(100)
        self.order_spin.setValue(1)
        form_layout.addWidget(self.order_spin, 4, 1)
        
        layout.addLayout(form_layout)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Guardar")
        save_btn.clicked.connect(self.save_status)
        buttons_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_data(self):
        """Carga los datos del estado si está editando"""
        if self.status_data:
            self.name_edit.setText(self.status_data.get('nombre', ''))
            self.description_edit.setPlainText(self.status_data.get('descripcion', ''))
            self.allow_modification_cb.setChecked(self.status_data.get('permite_modificacion', False))
            self.order_spin.setValue(self.status_data.get('orden', 1))
            
            color = self.status_data.get('color', '#007bff')
            self.selected_color = color

        # Actualizar vista previa del color (siempre al final)
        self.update_color_preview()
    
    def select_color(self):
        """Abre el diálogo de selección de color"""
        color = QColorDialog.getColor(QColor(self.selected_color), self)
        if color.isValid():
            self.selected_color = color.name()
            self.update_color_preview()
    
    def update_color_preview(self):
        """Actualiza la vista previa del color"""
        self.color_preview.setStyleSheet(
            f"background-color: {self.selected_color}; border: 1px solid #ccc;"
        )

    def get_status_data(self):
        """Obtiene los datos del estado del formulario"""
        return {
            'nombre': self.name_edit.text().strip(),
            'descripcion': self.description_edit.toPlainText().strip(),
            'permite_modificacion': self.allow_modification_cb.isChecked(),
            'color': self.selected_color,
            'orden': self.order_spin.value()
        }
    
    def save_status(self):
        """Guarda el estado de factura"""
        try:
            # Validar datos
            name = self.name_edit.text().strip()
            if not name:
                self.show_warning("Validación", "El nombre del estado es obligatorio")
                return
            
            description = self.description_edit.toPlainText().strip()
            if not description:
                description = name
            
            # Preparar datos
            status_data = {
                'nombre': name,
                'descripcion': description,
                'permite_modificacion': self.allow_modification_cb.isChecked(),
                'color': self.selected_color,
                'orden': self.order_spin.value()
            }
            
            # Si estamos editando, incluir el ID
            if self.status_data.get('id'):
                status_data['id'] = self.status_data['id']
            
            # Guardar
            success = invoice_status_manager.save_status(status_data)
            
            if success:
                action = "actualizado" if self.status_data.get('id') else "creado"
                self.show_info("Éxito", f"Estado '{name}' {action} correctamente")
                self.accept()
            else:
                self.show_error("Error", "No se pudo guardar el estado")
        
        except Exception as e:
            self.logger.error(f"Error guardando estado: {e}")
            self.show_error("Error", f"Error al guardar estado: {e}")
