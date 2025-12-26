# -*- coding: utf-8 -*-
"""
Ventana de selección de informes
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QGroupBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from utils.logger import get_logger


class InformesSelectorDialog(QDialog):
    """Diálogo para seleccionar el tipo de informe"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        self.selected_type = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar la interfaz"""
        self.setWindowTitle("Informes")
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel("Seleccione el tipo de informe")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(20)
        
        # Grupo de opciones
        options_group = QGroupBox("Tipo de Informe")
        options_layout = QVBoxLayout()
        
        # Grupo de botones radio
        self.button_group = QButtonGroup()
        
        # Opción 1: Informe de Facturación
        self.facturacion_radio = QRadioButton("Informe de Facturación")
        self.facturacion_radio.setChecked(True)
        facturacion_desc = QLabel("   Generar un informe de facturación por período de tiempo")
        facturacion_desc.setStyleSheet("color: gray; font-size: 10pt;")
        
        self.button_group.addButton(self.facturacion_radio, 1)
        options_layout.addWidget(self.facturacion_radio)
        options_layout.addWidget(facturacion_desc)
        options_layout.addSpacing(15)
        
        # Opción 2: Informe de Stock
        self.stock_radio = QRadioButton("Informe de Stock")
        stock_desc = QLabel("   Generar un informe de stock de productos")
        stock_desc.setStyleSheet("color: gray; font-size: 10pt;")
        
        self.button_group.addButton(self.stock_radio, 2)
        options_layout.addWidget(self.stock_radio)
        options_layout.addWidget(stock_desc)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        layout.addStretch()
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        generate_btn = QPushButton("Generar Informe")
        generate_btn.setDefault(True)
        generate_btn.clicked.connect(self.accept_selection)
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        buttons_layout.addWidget(generate_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def accept_selection(self):
        """Aceptar la selección"""
        if self.facturacion_radio.isChecked():
            self.selected_type = 'facturacion'
        elif self.stock_radio.isChecked():
            self.selected_type = 'stock'
        
        self.accept()
    
    def get_selected_type(self):
        """Obtener el tipo de informe seleccionado"""
        return self.selected_type

