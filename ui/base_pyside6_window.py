# -*- coding: utf-8 -*-
"""
Fenêtre de base PySide6 pour toutes les fenêtres secondaires
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QScrollArea, QWidget, QSplitter, QTabWidget,
    QMessageBox, QFileDialog, QProgressBar, QCheckBox,
    QSpinBox, QDoubleSpinBox, QDateEdit, QGroupBox
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap
from utils.logger import get_logger
import os

class BasePySide6Window(QDialog):
    """Classe de base pour toutes les fenêtres secondaires PySide6"""
    
    # Signaux PySide6
    window_closed = Signal()
    data_changed = Signal()
    
    def __init__(self, parent=None, title="Ventana", width=800, height=600):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        
        # Configuration de base
        self.setWindowTitle(title)
        self.setModal(False)
        self.resize(width, height)
        
        # Variables communes
        self.data_modified = False
        
        # Configuration de l'interface
        self.setup_ui()
        self.setup_connections()
        
        # Centrer la fenêtre
        self.center_window()
        
    def setup_ui(self):
        """À implémenter dans les classes filles"""
        pass
        
    def setup_connections(self):
        """À implémenter dans les classes filles"""
        pass
        
    def center_window(self):
        """Centrer la fenêtre sur l'écran"""
        try:
            # Obtenir la géométrie de l'écran
            screen = self.screen()
            if screen:
                screen_geometry = screen.availableGeometry()
                window_geometry = self.frameGeometry()
                
                # Calculer la position centrale
                center_point = screen_geometry.center()
                window_geometry.moveCenter(center_point)
                
                # Déplacer la fenêtre
                self.move(window_geometry.topLeft())
        except Exception as e:
            self.logger.warning(f"Impossible de centrer la fenêtre: {e}")
    
    def create_button_layout(self, buttons_config):
        """
        Créer un layout de boutons
        buttons_config: liste de tuples (text, callback, enabled)
        """
        layout = QHBoxLayout()
        
        for config in buttons_config:
            if len(config) >= 2:
                text, callback = config[:2]
                enabled = config[2] if len(config) > 2 else True
                
                button = QPushButton(text)
                button.clicked.connect(callback)
                button.setEnabled(enabled)
                layout.addWidget(button)
        
        layout.addStretch()
        return layout
    
    def create_form_row(self, label_text, widget, layout=None):
        """Créer une ligne de formulaire avec label et widget"""
        if layout is None:
            layout = QHBoxLayout()
        
        label = QLabel(label_text)
        label.setMinimumWidth(120)
        layout.addWidget(label)
        layout.addWidget(widget)
        
        return layout
    
    def show_info(self, title, message):
        """Afficher un message d'information"""
        QMessageBox.information(self, title, message)
    
    def show_warning(self, title, message):
        """Afficher un avertissement"""
        QMessageBox.warning(self, title, message)
    
    def show_error(self, title, message):
        """Afficher une erreur"""
        QMessageBox.critical(self, title, message)
    
    def ask_confirmation(self, title, message):
        """Demander une confirmation"""
        reply = QMessageBox.question(
            self, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
    
    def set_data_modified(self, modified=True):
        """Marquer les données comme modifiées"""
        self.data_modified = modified
        if modified:
            self.data_changed.emit()
    
    def closeEvent(self, event):
        """Gérer la fermeture de la fenêtre"""
        if self.data_modified:
            if self.ask_confirmation(
                "Données modifiées", 
                "Des modifications non sauvegardées seront perdues.\nVoulez-vous vraiment fermer?"
            ):
                self.window_closed.emit()
                event.accept()
            else:
                event.ignore()
        else:
            self.window_closed.emit()
            event.accept()
    
    def apply_style(self):
        """Appliquer le style de base"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #ccc;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #d4edda;
                border-color: #c3e6cb;
            }
            QPushButton:pressed {
                background-color: #c3e6cb;
            }
            QPushButton:disabled {
                background-color: #f8f9fa;
                color: #6c757d;
                border-color: #dee2e6;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #ccc;
                padding: 4px;
                border-radius: 4px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #007bff;
            }
            QTableWidget {
                gridline-color: #ddd;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 4px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
    
    def setup_table_widget(self, table, headers):
        """Configurer un QTableWidget avec les en-têtes"""
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        # Configuration de l'en-tête
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        
        # Permettre la sélection de lignes entières
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        return table
