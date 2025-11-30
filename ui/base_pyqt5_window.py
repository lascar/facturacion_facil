# -*- coding: utf-8 -*-
"""
Fenêtre de base PyQt5 pour toutes les fenêtres secondaires avec support du scroll
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame,
    QScrollArea, QWidget, QSplitter, QTabWidget,
    QMessageBox, QFileDialog, QProgressBar, QCheckBox,
    QSpinBox, QDoubleSpinBox, QDateEdit, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal as Signal
from PyQt5.QtGui import QFont, QIcon, QPixmap
from utils.logger import get_logger
from ui.scroll_mixin_pyqt5 import ScrollableMixin
import os

class BasePyQt5Window(ScrollableMixin, QDialog):
    """Classe de base pour toutes les fenêtres secondaires PySide2"""
    
    # Signaux PySide2
    window_closed = Signal()
    data_changed = Signal()
    
    def __init__(self, parent=None, title="Ventana", width=800, height=600, enable_scroll=True):
        super().__init__(parent)
        self.logger = get_logger(self.__class__.__name__)

        # Configuration de base
        self.setWindowTitle(title)
        self.setModal(False)
        self.resize(width, height)

        # Variables communes
        self.data_modified = False
        self.enable_scroll = enable_scroll

        # Appliquer les styles globaux
        self.apply_global_styles()

        # Configuration de l'interface
        self.setup_ui()
        self.setup_connections()

        # Centrer la fenêtre
        self.center_window()
        
    def apply_global_styles(self):
        """Appliquer les styles globaux pour améliorer la lisibilité"""
        global_style = """
            QLineEdit {
                min-height: 28px;
                padding: 4px 8px;
                font-size: 13px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }

            QLineEdit:focus {
                border: 2px solid #0078d4;
                background-color: #f8f9fa;
            }

            QLineEdit:disabled {
                background-color: #f5f5f5;
                color: #666;
            }

            QTextEdit {
                min-height: 80px;
                padding: 4px 8px;
                font-size: 13px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }

            QTextEdit:focus {
                border: 2px solid #0078d4;
                background-color: #f8f9fa;
            }

            QComboBox {
                min-height: 28px;
                padding: 4px 8px;
                font-size: 13px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }

            QComboBox:focus {
                border: 2px solid #0078d4;
            }

            QSpinBox, QDoubleSpinBox {
                min-height: 28px;
                padding: 4px 8px;
                font-size: 13px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }

            QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #0078d4;
            }

            QPushButton {
                min-height: 32px;
                padding: 6px 12px;
                font-size: 13px;
                font-weight: 500;
                border: 1px solid #0078d4;
                border-radius: 4px;
                background-color: #0078d4;
                color: white;
            }

            QPushButton:hover {
                background-color: #106ebe;
                border-color: #106ebe;
            }

            QPushButton:pressed {
                background-color: #005a9e;
                border-color: #005a9e;
            }

            QPushButton:disabled {
                background-color: #f5f5f5;
                border-color: #ccc;
                color: #666;
            }

            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: white;
            }

            QLabel {
                font-size: 13px;
                color: #333;
            }

            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
                selection-background-color: #0078d4;
                selection-color: white;
                font-size: 12px;
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
                background-color: #f1f3f4;
                padding: 8px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
                font-size: 12px;
            }
        """

        self.setStyleSheet(global_style)

    def setup_ui(self):
        """À implémenter dans les classes filles"""
        pass

    def setup_connections(self):
        """À implémenter dans les classes filles"""
        pass

    def enable_window_scroll(self, enable_horizontal=False, enable_vertical=True):
        """
        Active le scroll pour la fenêtre.
        À appeler dans setup_ui() des classes filles si nécessaire.

        Args:
            enable_horizontal (bool): Activer le scroll horizontal
            enable_vertical (bool): Activer le scroll vertical
        """
        if self.enable_scroll:
            self.setup_scrollable_content(enable_horizontal, enable_vertical)
            self.logger.debug(f"Scroll activé pour {self.__class__.__name__}")

    def get_content_layout(self):
        """
        Retourne le layout où ajouter le contenu.
        Si le scroll est activé, retourne le layout scrollable.
        Sinon, retourne le layout principal de la fenêtre.
        """
        if self.enable_scroll and hasattr(self, 'scrollable_widget') and self.scrollable_widget:
            return self.get_scrollable_layout()
        else:
            # Créer un layout principal si aucun n'existe
            if not self.layout():
                layout = QVBoxLayout(self)
                layout.setContentsMargins(10, 10, 10, 10)
                layout.setSpacing(10)
            return self.layout()

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
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes
    
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
        """Appliquer le style de base moderne"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            }

            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4a90e2, stop: 1 #357abd);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px;
                min-height: 35px;
            }

            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5ba0f2, stop: 1 #4a90e2);
            }

            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #357abd, stop: 1 #2c6aa0);
            }

            QPushButton:disabled {
                background-color: #e9ecef;
                color: #6c757d;
            }

            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 10pt;
            }

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus,
            QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #4a90e2;
                background-color: #f8f9ff;
            }

            QTableWidget {
                gridline-color: #dee2e6;
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                selection-background-color: #e3f2fd;
            }

            QHeaderView::section {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f1f3f4, stop: 1 #e9ecef);
                padding: 8px;
                border: 1px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }

            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #495057;
            }

            QLabel {
                color: #495057;
                font-weight: 500;
            }

            QScrollBar:vertical {
                background-color: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical {
                background-color: #ced4da;
                border-radius: 6px;
                min-height: 20px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #adb5bd;
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
        table.setSelectionBehavior(QTableWidget.SelectRows)
        
        return table
