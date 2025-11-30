# -*- coding: utf-8 -*-
"""
Fenêtre de base PyQt6 pour toutes les fenêtres secondaires
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QScrollArea, QWidget, QSplitter, QTabWidget,
    QMessageBox, QFileDialog, QProgressBar, QCheckBox,
    QSpinBox, QDoubleSpinBox, QDateEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
from utils.logger import get_logger
import os

class BasePyQt6Window(QDialog):
    """Classe de base pour toutes les fenêtres secondaires PyQt6"""
    
    def __init__(self, parent=None, title="Ventana", width=800, height=600):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)
        
        # Configuration de base
        self.setWindowTitle(title)
        self.setModal(False)  # Non-modal par défaut
        self.resize(width, height)
        
        # Style moderne
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 9pt;
            }
            
            QLabel {
                color: #333333;
                font-weight: 500;
            }
            
            QLineEdit, QTextEdit, QComboBox {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
                font-size: 9pt;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #0078d4;
                outline: none;
            }
            
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 9pt;
            }
            
            QPushButton:hover {
                background-color: #106ebe;
            }
            
            QPushButton:pressed {
                background-color: #005a9e;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                alternate-background-color: #f9f9f9;
                gridline-color: #e0e0e0;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            
            QTableWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 8px;
                font-weight: 600;
            }
            
            QGroupBox {
                font-weight: 600;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 8px 16px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
        """)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Initialiser l'interface
        self.setup_ui()
        
        # Centrer la fenêtre
        self.center_window()
    
    def setup_ui(self):
        """À surcharger dans les classes filles"""
        pass
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        if self.parent():
            # Centrer par rapport au parent
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(max(0, x), max(0, y))
        else:
            # Centrer sur l'écran
            screen = self.screen().availableGeometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(x, y)
    
    def create_button_layout(self, buttons_config):
        """
        Crée un layout de boutons
        buttons_config: liste de tuples (text, callback, style_class)
        """
        layout = QHBoxLayout()
        layout.addStretch()
        
        for config in buttons_config:
            if len(config) == 2:
                text, callback = config
                style_class = "primary"
            else:
                text, callback, style_class = config
            
            button = QPushButton(text)
            button.clicked.connect(callback)
            
            # Styles spéciaux
            if style_class == "secondary":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #6c757d;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #5a6268;
                    }
                """)
            elif style_class == "danger":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #dc3545;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #c82333;
                    }
                """)
            elif style_class == "success":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #218838;
                    }
                """)
            elif style_class == "info":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #17a2b8;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #138496;
                    }
                """)
            elif style_class == "primary":
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #007bff;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #0056b3;
                    }
                """)

            layout.addWidget(button)
        
        return layout
    
    def show_message(self, title, message, msg_type="info"):
        """Affiche un message PyQt6 natif"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if msg_type == "info":
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif msg_type == "question":
            msg_box.setIcon(QMessageBox.Icon.Question)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            return msg_box.exec() == QMessageBox.StandardButton.Yes
        
        msg_box.exec()
        return True
    
    def show_error(self, title, message):
        """Affiche un message d'erreur"""
        self.show_message(title, message, "error")
    
    def show_warning(self, title, message):
        """Affiche un avertissement"""
        self.show_message(title, message, "warning")
    
    def show_info(self, title, message):
        """Affiche une information"""
        self.show_message(title, message, "info")
    
    def ask_question(self, title, message):
        """Pose une question Oui/Non"""
        return self.show_message(title, message, "question")
