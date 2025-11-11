#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Couche d'abstraction GUI pour rendre l'interface indépendante du framework
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable, Tuple
from enum import Enum

class WidgetType(Enum):
    """Types de widgets supportés"""
    WINDOW = "window"
    FRAME = "frame"
    LABEL = "label"
    BUTTON = "button"
    ENTRY = "entry"
    TEXT = "text"
    COMBOBOX = "combobox"
    TREEVIEW = "treeview"
    SCROLLBAR = "scrollbar"
    CHECKBOX = "checkbox"
    RADIOBUTTON = "radiobutton"
    SCALE = "scale"
    PROGRESSBAR = "progressbar"
    SEPARATOR = "separator"
    NOTEBOOK = "notebook"
    CANVAS = "canvas"

class PackSide(Enum):
    """Options pour pack side"""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

class Anchor(Enum):
    """Options d'ancrage"""
    N = "n"
    S = "s"
    E = "e"
    W = "w"
    NE = "ne"
    NW = "nw"
    SE = "se"
    SW = "sw"
    CENTER = "center"

class Fill(Enum):
    """Options de remplissage"""
    NONE = "none"
    X = "x"
    Y = "y"
    BOTH = "both"

class AbstractWidget(ABC):
    """Classe abstraite pour tous les widgets"""
    
    def __init__(self, widget_type: WidgetType):
        self.widget_type = widget_type
        self._native_widget = None
        self._parent = None
        self._children = []
        self._properties = {}
    
    @abstractmethod
    def create_native_widget(self, parent=None, **kwargs) -> Any:
        """Crée le widget natif du framework"""
        pass
    
    @abstractmethod
    def pack(self, **kwargs):
        """Empaquette le widget"""
        pass
    
    @abstractmethod
    def grid(self, **kwargs):
        """Place le widget en grille"""
        pass
    
    @abstractmethod
    def place(self, **kwargs):
        """Place le widget avec coordonnées absolues"""
        pass
    
    @abstractmethod
    def configure(self, **kwargs):
        """Configure les propriétés du widget"""
        pass
    
    @abstractmethod
    def get_native_widget(self) -> Any:
        """Retourne le widget natif"""
        pass
    
    def add_child(self, child: 'AbstractWidget'):
        """Ajoute un widget enfant"""
        self._children.append(child)
        child._parent = self
    
    def get_children(self) -> List['AbstractWidget']:
        """Retourne la liste des enfants"""
        return self._children.copy()
    
    def get_parent(self) -> Optional['AbstractWidget']:
        """Retourne le parent"""
        return self._parent

class AbstractGUIFactory(ABC):
    """Factory abstraite pour créer des widgets"""
    
    @abstractmethod
    def create_window(self, title: str = "", geometry: str = "800x600", **kwargs) -> AbstractWidget:
        """Crée une fenêtre principale"""
        pass
    
    @abstractmethod
    def create_toplevel(self, parent: AbstractWidget, title: str = "", geometry: str = "400x300", **kwargs) -> AbstractWidget:
        """Crée une fenêtre secondaire"""
        pass
    
    @abstractmethod
    def create_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame"""
        pass
    
    @abstractmethod
    def create_scrollable_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame scrollable"""
        pass
    
    @abstractmethod
    def create_label(self, parent: AbstractWidget, text: str = "", **kwargs) -> AbstractWidget:
        """Crée un label"""
        pass
    
    @abstractmethod
    def create_button(self, parent: AbstractWidget, text: str = "", command: Callable = None, **kwargs) -> AbstractWidget:
        """Crée un bouton"""
        pass
    
    @abstractmethod
    def create_entry(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un champ de saisie"""
        pass
    
    @abstractmethod
    def create_text(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un widget texte multiligne"""
        pass
    
    @abstractmethod
    def create_combobox(self, parent: AbstractWidget, values: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée une combobox"""
        pass
    
    @abstractmethod
    def create_treeview(self, parent: AbstractWidget, columns: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée un treeview"""
        pass
    
    @abstractmethod
    def create_scrollbar(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée une scrollbar"""
        pass
    
    @abstractmethod
    def show_message(self, message_type: str, title: str, message: str, **kwargs) -> Any:
        """Affiche un message"""
        pass
    
    @abstractmethod
    def ask_file(self, **kwargs) -> Optional[str]:
        """Demande de sélectionner un fichier"""
        pass
    
    @abstractmethod
    def ask_directory(self, **kwargs) -> Optional[str]:
        """Demande de sélectionner un répertoire"""
        pass

class AbstractApplication(ABC):
    """Application abstraite"""
    
    def __init__(self, gui_factory: AbstractGUIFactory):
        self.gui_factory = gui_factory
        self.main_window = None
    
    @abstractmethod
    def initialize(self):
        """Initialise l'application"""
        pass
    
    @abstractmethod
    def run(self):
        """Lance la boucle principale"""
        pass
    
    @abstractmethod
    def quit(self):
        """Quitte l'application"""
        pass
