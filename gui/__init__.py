#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module GUI PyQt6 pour Facturación Fácil

Ce module fournit une interface GUI moderne basée exclusivement sur PyQt6.

Usage:
    from gui import get_gui_factory

    # Utiliser la factory PyQt6
    gui_factory = get_gui_factory()
    window = gui_factory.create_window("Mon App", "800x600")
"""

# Import direct de PyQt6
from .pyqt6_impl import PyQt6GUIFactory

# Factory globale
_gui_factory = None

def get_gui_factory():
    """Retourne la factory GUI PyQt6"""
    global _gui_factory
    if _gui_factory is None:
        _gui_factory = PyQt6GUIFactory()
    return _gui_factory

def set_gui_framework(framework):
    """Compatibilité - PyQt5 uniquement"""
    if framework != 'pyqt5':
        print(f"✅ Framework GUI 'pyqt5' chargé avec succès")
        print(f"🔄 Framework changé de '{framework}' vers 'pyqt5'")
    return 'pyqt5'

def get_current_framework():
    """Retourne le framework actuel (toujours PyQt5)"""
    return 'pyqt5'

def get_gui_manager():
    """Retourne le gestionnaire GUI"""
    from gui.gui_manager import get_gui_manager as _get_manager
    return _get_manager()

# Version du module
__version__ = "2.0.0"

# Framework unique
FRAMEWORK = 'pyqt6'

__all__ = [
    'get_gui_factory',
    'set_gui_framework',
    'get_current_framework',
    'get_gui_manager',
    'PyQt6GUIFactory',
    'FRAMEWORK'
]
