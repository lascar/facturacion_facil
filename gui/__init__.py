#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module GUI PyQt5 pour Facturación Fácil

Ce module fournit une interface GUI moderne basée exclusivement sur PyQt5.

Usage:
    from gui import set_gui_framework

    # L'application utilise uniquement PyQt5
    set_gui_framework('pyqt5')
"""

# Factory globale (non utilisée - compatibilité uniquement)
_gui_factory = None

def get_gui_factory():
    """Retourne None - L'application utilise PyQt5 natif"""
    return None

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
FRAMEWORK = 'pyqt5'

__all__ = [
    'get_gui_factory',
    'set_gui_framework',
    'get_current_framework',
    'get_gui_manager',
    'FRAMEWORK'
]
