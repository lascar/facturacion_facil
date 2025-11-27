# -*- coding: utf-8 -*-
"""
Fenêtre de gestion des clients - Version PySide6 native
"""

from PySide6.QtWidgets import QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.base_pyside6_window import BasePySide6Window

class ClientesPySide6Window(BasePySide6Window):
    """Fenêtre de gestion des clients avec PySide6"""
    
    def __init__(self, parent=None):
        super().__init__(parent, "Gestión de Clientes", 800, 600)
        
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre
        title_label = QLabel("Gestión de Clientes")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Message temporaire
        message_label = QLabel("Funcionalidad en desarrollo con PySide6")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message_label)
        
        layout.addStretch()
        
        # Appliquer le style
        self.apply_style()
