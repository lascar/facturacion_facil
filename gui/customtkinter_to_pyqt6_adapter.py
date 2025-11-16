#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptateur pour permettre aux fenêtres CustomTkinter existantes de fonctionner avec PyQt6
"""

from gui import get_gui_factory
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget
from PyQt6.QtCore import Qt

class CTkToplevelAdapter:
    """Adaptateur pour CTkToplevel vers PyQt6 QDialog"""
    
    def __init__(self, parent=None):
        self.factory = get_gui_factory()
        
        # Créer un QDialog au lieu d'une fenêtre normale
        if parent:
            # Si parent est un widget PyQt6, l'utiliser directement
            if hasattr(parent, 'get_native_widget'):
                parent_widget = parent.get_native_widget()
            else:
                parent_widget = parent
            self._dialog = QDialog(parent_widget)
        else:
            self._dialog = QDialog()
        
        # Configuration par défaut
        self._dialog.setModal(False)
        self._dialog.setWindowFlags(Qt.WindowType.Window)
        
        # Layout principal
        self._layout = QVBoxLayout(self._dialog)
        
    def title(self, text):
        """Définit le titre de la fenêtre"""
        self._dialog.setWindowTitle(text)
    
    def geometry(self, geometry_str):
        """Définit la géométrie (format: "800x600")"""
        if 'x' in geometry_str:
            width, height = map(int, geometry_str.split('x'))
            self._dialog.resize(width, height)
    
    def transient(self, parent):
        """Définit la fenêtre comme transitoire (modal)"""
        # Déjà géré dans __init__
        pass
    
    def lift(self):
        """Amène la fenêtre au premier plan"""
        self._dialog.raise_()
        self._dialog.activateWindow()
    
    def focus_force(self):
        """Force le focus sur la fenêtre"""
        self._dialog.setFocus()
    
    def attributes(self, attr, value=None):
        """Gère les attributs de fenêtre"""
        if attr == '-topmost':
            if value:
                self._dialog.setWindowFlags(self._dialog.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
            else:
                self._dialog.setWindowFlags(self._dialog.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
            self._dialog.show()
    
    def after(self, delay, callback):
        """Exécute un callback après un délai"""
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(delay, callback)
    
    def show(self):
        """Affiche la fenêtre"""
        self._dialog.show()
    
    def hide(self):
        """Cache la fenêtre"""
        self._dialog.hide()
    
    def destroy(self):
        """Détruit la fenêtre"""
        self._dialog.close()
        self._dialog.deleteLater()

class CTkFrameAdapter:
    """Adaptateur pour CTkFrame vers PyQt6"""
    
    def __init__(self, parent):
        self.factory = get_gui_factory()
        
        if hasattr(parent, '_dialog'):
            # Parent est un CTkToplevelAdapter
            self._frame = QWidget()
            parent._layout.addWidget(self._frame)
            self._layout = QVBoxLayout(self._frame)
        elif hasattr(parent, '_layout'):
            # Parent a déjà un layout
            self._frame = QWidget()
            parent._layout.addWidget(self._frame)
            self._layout = QVBoxLayout(self._frame)
        else:
            # Créer un frame normal
            self._frame = self.factory.create_frame(parent)
            self._layout = None
    
    def pack(self, **kwargs):
        """Empaquetage (géré automatiquement par les layouts)"""
        pass
    
    def grid(self, **kwargs):
        """Placement en grille"""
        if hasattr(self, '_frame') and hasattr(self._frame, 'grid'):
            self._frame.grid(**kwargs)

class CTkScrollableFrameAdapter:
    """Adaptateur pour CTkScrollableFrame vers PyQt6"""
    
    def __init__(self, parent):
        self.factory = get_gui_factory()
        self._scrollable_frame = self.factory.create_scrollable_frame(parent)
    
    def pack(self, **kwargs):
        """Empaquetage"""
        self._scrollable_frame.pack(**kwargs)
    
    def configure(self, **kwargs):
        """Configuration"""
        self._scrollable_frame.configure(**kwargs)

class CTkLabelAdapter:
    """Adaptateur pour CTkLabel vers PyQt6"""
    
    def __init__(self, parent, text="", **kwargs):
        self.factory = get_gui_factory()
        
        # Déterminer le parent réel
        if hasattr(parent, '_frame'):
            real_parent = parent._frame
        elif hasattr(parent, '_scrollable_frame'):
            real_parent = parent._scrollable_frame
        else:
            real_parent = parent
        
        # Créer le label via la factory
        self._label = self.factory.create_label(real_parent, text=text, **kwargs)
    
    def pack(self, **kwargs):
        """Empaquetage"""
        self._label.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Placement en grille"""
        self._label.grid(**kwargs)
    
    def configure(self, **kwargs):
        """Configuration"""
        self._label.configure(**kwargs)

class CTkButtonAdapter:
    """Adaptateur pour CTkButton vers PyQt6"""
    
    def __init__(self, parent, text="", command=None, **kwargs):
        self.factory = get_gui_factory()
        
        # Déterminer le parent réel
        if hasattr(parent, '_frame'):
            real_parent = parent._frame
        elif hasattr(parent, '_scrollable_frame'):
            real_parent = parent._scrollable_frame
        else:
            real_parent = parent
        
        # Créer le bouton via la factory
        self._button = self.factory.create_button(real_parent, text=text, command=command, **kwargs)
    
    def pack(self, **kwargs):
        """Empaquetage"""
        self._button.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Placement en grille"""
        self._button.grid(**kwargs)
    
    def configure(self, **kwargs):
        """Configuration"""
        self._button.configure(**kwargs)

# Fonction pour créer un module customtkinter simulé
def create_customtkinter_adapter():
    """Crée un module customtkinter adapté pour PyQt6"""
    import types
    
    # Créer un module simulé
    ctk_module = types.ModuleType('customtkinter_adapter')
    
    # Ajouter les classes adaptées
    ctk_module.CTkToplevel = CTkToplevelAdapter
    ctk_module.CTkFrame = CTkFrameAdapter
    ctk_module.CTkScrollableFrame = CTkScrollableFrameAdapter
    ctk_module.CTkLabel = CTkLabelAdapter
    ctk_module.CTkButton = CTkButtonAdapter
    
    # Fonctions de configuration (no-op pour PyQt6)
    ctk_module.set_appearance_mode = lambda mode: None
    ctk_module.set_default_color_theme = lambda theme: None
    
    return ctk_module
