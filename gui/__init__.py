#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'abstraction GUI pour Facturación Fácil

Ce module fournit une couche d'abstraction pour rendre l'interface graphique
indépendante du framework GUI utilisé (CustomTkinter, Tkinter, etc.).

Usage:
    from gui import get_gui_manager, set_gui_framework
    from gui.abstract_components import AbstractForm, AbstractListWindow
    
    # Définir le framework
    set_gui_framework('customtkinter')  # ou 'tkinter'
    
    # Utiliser les composants abstraits
    class MyForm(AbstractForm):
        def create_widgets(self):
            self.add_field("name", "Nom:", "entry")
            self.add_button("save", "Sauvegarder", self.save)
"""

from .gui_manager import (
    get_gui_manager,
    set_gui_framework,
    get_gui_factory,
    create_gui_application,
    GUIManager
)

from .abstract_gui import (
    AbstractWidget,
    AbstractGUIFactory,
    AbstractApplication,
    WidgetType,
    PackSide,
    Anchor,
    Fill
)

from .abstract_components import (
    AbstractWindow,
    AbstractForm,
    AbstractListWindow
)

# Version du module
__version__ = "1.0.0"

# Frameworks supportés
SUPPORTED_FRAMEWORKS = ['customtkinter', 'tkinter']

# Framework par défaut
DEFAULT_FRAMEWORK = 'customtkinter'

__all__ = [
    # Gestionnaire principal
    'get_gui_manager',
    'set_gui_framework', 
    'get_gui_factory',
    'create_gui_application',
    'GUIManager',
    
    # Classes abstraites de base
    'AbstractWidget',
    'AbstractGUIFactory', 
    'AbstractApplication',
    
    # Composants de haut niveau
    'AbstractWindow',
    'AbstractForm',
    'AbstractListWindow',
    
    # Enums
    'WidgetType',
    'PackSide',
    'Anchor',
    'Fill',
    
    # Constantes
    'SUPPORTED_FRAMEWORKS',
    'DEFAULT_FRAMEWORK'
]
