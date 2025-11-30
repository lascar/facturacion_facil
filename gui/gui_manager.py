#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire GUI pour PyQt6 - Version simplifiée
"""

class GUIManager:
    """Gestionnaire GUI simplifié pour PyQt6"""
    
    def __init__(self):
        self.current_framework = 'pyqt6'
        self.factory = None
        print("GUIManager inicializado")
    
    def set_framework(self, framework):
        """Définit le framework GUI"""
        self.current_framework = framework
        print(f"Framework configuré: {framework}")
        return True
    
    def get_framework(self):
        """Obtient le framework actuel"""
        return self.current_framework

    def get_current_framework(self):
        """Obtient le framework actuel (alias)"""
        return self.current_framework
    
    def get_factory(self):
        """Obtient la factory GUI"""
        if not self.factory:
            from gui import get_gui_factory
            self.factory = get_gui_factory()
        return self.factory
    
    def create_window(self, title="Window", geometry="800x600"):
        """Crée une fenêtre"""
        factory = self.get_factory()
        return factory.create_window(title, geometry)
    
    def create_dialog(self, parent=None, title="Dialog"):
        """Crée un dialog"""
        factory = self.get_factory()
        return factory.create_dialog(parent, title)
    
    def is_available(self, framework):
        """Vérifie si un framework est disponible - PyQt5 uniquement"""
        if framework == 'pyqt5':
            try:
                from PyQt5 import QtWidgets
                return True
            except ImportError:
                return False
        return False
    
    def switch_framework(self, framework):
        """Change de framework"""
        if self.is_available(framework):
            self.set_framework(framework)
            return True
        return False

# Instance globale
_gui_manager = None

def get_gui_manager():
    """Obtient l'instance globale du gestionnaire GUI"""
    global _gui_manager
    if _gui_manager is None:
        _gui_manager = GUIManager()
    return _gui_manager
