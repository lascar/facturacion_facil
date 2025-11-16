#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation PyQt6 de la couche d'abstraction GUI
"""

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
        QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit, 
        QComboBox, QTreeWidget, QTreeWidgetItem, QScrollBar, QFrame,
        QScrollArea, QMessageBox, QFileDialog, QCheckBox, QRadioButton,
        QSlider, QProgressBar, QTabWidget
    )
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QFont
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False

from typing import Any, Dict, List, Optional, Callable, Tuple

from .abstract_gui import (
    AbstractWidget, AbstractGUIFactory, AbstractApplication,
    WidgetType, PackSide, Anchor, Fill
)

class PyQt6Widget(AbstractWidget):
    """Widget PyQt6 qui implémente AbstractWidget"""
    
    def __init__(self, widget_type: WidgetType, native_widget=None):
        super().__init__(widget_type)
        self._native_widget = native_widget
        self._layout = None
        
    def create_native_widget(self, parent=None, **kwargs) -> Any:
        """Crée le widget natif PyQt6"""
        parent_widget = parent.get_native_widget() if parent else None
        
        if self.widget_type == WidgetType.WINDOW:
            self._native_widget = QMainWindow()
        elif self.widget_type == WidgetType.FRAME:
            self._native_widget = QFrame(parent_widget)
            # Utiliser QVBoxLayout par défaut, mais permettre de changer
            self._layout = QVBoxLayout(self._native_widget)
            self._layout.setContentsMargins(10, 10, 10, 10)
            self._layout.setSpacing(10)
        elif self.widget_type == WidgetType.LABEL:
            self._native_widget = QLabel(kwargs.get('text', ''), parent_widget)
        elif self.widget_type == WidgetType.BUTTON:
            self._native_widget = QPushButton(kwargs.get('text', ''), parent_widget)
            if 'command' in kwargs and kwargs['command'] is not None:
                self._native_widget.clicked.connect(kwargs['command'])
        elif self.widget_type == WidgetType.ENTRY:
            self._native_widget = QLineEdit(parent_widget)
        elif self.widget_type == WidgetType.TEXT:
            self._native_widget = QTextEdit(parent_widget)
        elif self.widget_type == WidgetType.COMBOBOX:
            self._native_widget = QComboBox(parent_widget)
            if 'values' in kwargs:
                self._native_widget.addItems(kwargs['values'])
        elif self.widget_type == WidgetType.TREEVIEW:
            self._native_widget = QTreeWidget(parent_widget)
            if 'columns' in kwargs:
                columns = kwargs['columns']
                self._native_widget.setHeaderLabels(columns)
                self._native_widget.setColumnCount(len(columns))
                # Permettre la sélection de lignes entières
                from PyQt6.QtWidgets import QAbstractItemView
                self._native_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
                # Permettre le tri par colonnes
                self._native_widget.setSortingEnabled(True)
        else:
            self._native_widget = QWidget(parent_widget)
            
        return self._native_widget
    
    def pack(self, **kwargs):
        """Empaquette le widget (simulé avec layout)"""
        if self._parent and hasattr(self._parent, '_layout') and self._parent._layout:
            self._parent._layout.addWidget(self._native_widget)
    
    def grid(self, **kwargs):
        """Place le widget en grille"""
        if self._parent and hasattr(self._parent, '_layout'):
            # Si le parent n'a pas encore de QGridLayout, on le crée
            if not isinstance(self._parent._layout, QGridLayout):
                # Créer un nouveau QGridLayout
                parent_widget = self._parent._native_widget
                new_layout = QGridLayout()
                new_layout.setContentsMargins(10, 10, 10, 10)
                new_layout.setSpacing(10)

                # Remplacer le layout
                parent_widget.setLayout(new_layout)
                self._parent._layout = new_layout

            row = kwargs.get('row', 0)
            column = kwargs.get('column', 0)
            rowspan = kwargs.get('rowspan', 1)
            columnspan = kwargs.get('columnspan', 1)

            self._parent._layout.addWidget(self._native_widget, row, column, rowspan, columnspan)
    
    def place(self, **kwargs):
        """Place le widget avec coordonnées absolues"""
        if self._native_widget:
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            self._native_widget.move(x, y)
    
    def configure(self, **kwargs):
        """Configure les propriétés du widget"""
        if not self._native_widget:
            return
            
        if 'text' in kwargs:
            if hasattr(self._native_widget, 'setText'):
                self._native_widget.setText(kwargs['text'])
        
        if 'font' in kwargs:
            font_info = kwargs['font']
            if isinstance(font_info, tuple):
                family, size = font_info[:2]
                font = QFont(family, size)
                self._native_widget.setFont(font)
        
        if 'width' in kwargs and 'height' in kwargs:
            self._native_widget.resize(kwargs['width'], kwargs['height'])
    
    def get_native_widget(self) -> Any:
        """Retourne le widget natif PyQt6"""
        return self._native_widget


class PyQt6ScrollableFrame(PyQt6Widget):
    """Frame scrollable PyQt6"""

    def __init__(self):
        super().__init__(WidgetType.FRAME)

    def create_native_widget(self, parent=None, **kwargs) -> Any:
        """Crée un frame scrollable"""
        parent_widget = parent.get_native_widget() if parent else None

        # Créer le scroll area
        scroll_area = QScrollArea(parent_widget)
        scroll_area.setWidgetResizable(True)

        # Créer le widget contenu
        content_widget = QFrame()
        self._layout = QVBoxLayout(content_widget)

        # Associer le contenu au scroll area
        scroll_area.setWidget(content_widget)

        self._native_widget = scroll_area
        self._content_widget = content_widget

        return self._native_widget


class PyQt6GUIFactory(AbstractGUIFactory):
    """Factory pour créer des widgets PyQt6"""

    def __init__(self):
        if not PYQT6_AVAILABLE:
            raise ImportError("PyQt6 n'est pas disponible. Installez-le avec: pip install PyQt6")

        # Initialiser QApplication si nécessaire
        if not QApplication.instance():
            self._app = QApplication([])
        else:
            self._app = QApplication.instance()

    def create_window(self, title: str = "", geometry: str = "800x600", **kwargs) -> AbstractWidget:
        """Crée une fenêtre principale"""
        widget = PyQt6Widget(WidgetType.WINDOW)
        window = widget.create_native_widget(**kwargs)

        if title:
            window.setWindowTitle(title)

        # Parser la géométrie (format: "800x600")
        if 'x' in geometry:
            width, height = map(int, geometry.split('x'))
            window.resize(width, height)

        # Créer un widget central avec layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        window.setCentralWidget(central_widget)
        widget._layout = layout

        return widget

    def create_toplevel(self, parent: AbstractWidget, title: str = "", geometry: str = "400x300", **kwargs) -> AbstractWidget:
        """Crée une fenêtre secondaire"""
        widget = PyQt6Widget(WidgetType.WINDOW)
        window = widget.create_native_widget(**kwargs)

        if title:
            window.setWindowTitle(title)

        if 'x' in geometry:
            width, height = map(int, geometry.split('x'))
            window.resize(width, height)

        # Créer un widget central avec layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        window.setCentralWidget(central_widget)
        widget._layout = layout

        return widget

    def create_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame"""
        widget = PyQt6Widget(WidgetType.FRAME)
        widget.create_native_widget(parent, **kwargs)

        # Si on demande un layout horizontal
        if kwargs.get('layout') == 'horizontal':
            widget._layout = QHBoxLayout(widget._native_widget)
            widget._layout.setContentsMargins(5, 5, 5, 5)
            widget._layout.setSpacing(10)

        return widget

    def create_scrollable_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame scrollable"""
        widget = PyQt6ScrollableFrame()
        widget.create_native_widget(parent, **kwargs)
        return widget

    def create_label(self, parent: AbstractWidget, text: str = "", **kwargs) -> AbstractWidget:
        """Crée un label"""
        widget = PyQt6Widget(WidgetType.LABEL)
        widget.create_native_widget(parent, text=text, **kwargs)
        return widget

    def create_button(self, parent: AbstractWidget, text: str = "", command: Callable = None, **kwargs) -> AbstractWidget:
        """Crée un bouton"""
        widget = PyQt6Widget(WidgetType.BUTTON)
        widget.create_native_widget(parent, text=text, command=command, **kwargs)
        return widget

    def create_entry(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un champ de saisie"""
        widget = PyQt6Widget(WidgetType.ENTRY)
        widget.create_native_widget(parent, **kwargs)
        return widget

    def create_text(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un widget texte multiligne"""
        widget = PyQt6Widget(WidgetType.TEXT)
        widget.create_native_widget(parent, **kwargs)
        return widget

    def create_combobox(self, parent: AbstractWidget, values: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée une combobox"""
        widget = PyQt6Widget(WidgetType.COMBOBOX)
        widget.create_native_widget(parent, values=values, **kwargs)
        return widget

    def create_treeview(self, parent: AbstractWidget, columns: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée un treeview"""
        widget = PyQt6Widget(WidgetType.TREEVIEW)
        widget.create_native_widget(parent, columns=columns, **kwargs)
        return widget

    def create_scrollbar(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée une scrollbar"""
        widget = PyQt6Widget(WidgetType.SCROLLBAR)
        # Pour PyQt6, les scrollbars sont généralement intégrées
        scrollbar = QScrollBar(parent.get_native_widget() if parent else None)
        widget._native_widget = scrollbar
        return widget

    def show_message(self, message_type: str, title: str, message: str, **kwargs) -> Any:
        """Affiche un message"""
        if message_type.lower() == 'info':
            return QMessageBox.information(None, title, message)
        elif message_type.lower() == 'warning':
            return QMessageBox.warning(None, title, message)
        elif message_type.lower() == 'error':
            return QMessageBox.critical(None, title, message)
        elif message_type.lower() == 'question':
            return QMessageBox.question(None, title, message)
        else:
            return QMessageBox.information(None, title, message)

    def ask_file(self, **kwargs) -> Optional[str]:
        """Demande de sélectionner un fichier"""
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            kwargs.get('title', 'Sélectionner un fichier'),
            kwargs.get('initialdir', ''),
            kwargs.get('filetypes', 'Tous les fichiers (*)')
        )
        return file_path if file_path else None

    def ask_directory(self, **kwargs) -> Optional[str]:
        """Demande de sélectionner un répertoire"""
        directory = QFileDialog.getExistingDirectory(
            None,
            kwargs.get('title', 'Sélectionner un répertoire'),
            kwargs.get('initialdir', '')
        )
        return directory if directory else None


class PyQt6Application(AbstractApplication):
    """Application PyQt6"""

    def __init__(self):
        super().__init__(PyQt6GUIFactory())
        self._app = self.gui_factory._app

    def initialize(self):
        """Initialise l'application"""
        self.main_window = self.gui_factory.create_window(
            title="Facturación Fácil",
            geometry="800x600"
        )

    def run(self):
        """Lance la boucle principale"""
        if self.main_window:
            self.main_window.get_native_widget().show()
            return self._app.exec()

    def quit(self):
        """Quitte l'application"""
        if self._app:
            self._app.quit()
