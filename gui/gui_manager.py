#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de GUI pour changer facilement de framework
"""

import os
from typing import Type, Dict, Any
from .abstract_gui import AbstractGUIFactory, AbstractApplication

class GUIManager:
    """Gestionnaire pour changer de framework GUI"""
    
    # Frameworks disponibles
    AVAILABLE_FRAMEWORKS = {
        'customtkinter': {
            'factory_class': 'CustomTkinterGUIFactory',
            'app_class': 'CustomTkinterApplication',
            'module': 'gui.customtkinter_impl'
        },
        'tkinter': {
            'factory_class': 'TkinterGUIFactory',
            'app_class': 'TkinterApplication',
            'module': 'gui.tkinter_impl'
        }
    }
    
    def __init__(self, framework: str = None):
        """
        Initialise le gestionnaire GUI
        
        Args:
            framework: Framework à utiliser ('customtkinter', 'tkinter', etc.)
                      Si None, utilise la variable d'environnement GUI_FRAMEWORK
                      ou 'customtkinter' par défaut
        """
        if framework is None:
            framework = os.getenv('GUI_FRAMEWORK', 'customtkinter')
        
        self.framework = framework.lower()
        self._factory = None
        self._app_class = None
        
        self._load_framework()
    
    def _load_framework(self):
        """Charge le framework GUI sélectionné"""
        if self.framework not in self.AVAILABLE_FRAMEWORKS:
            available = ', '.join(self.AVAILABLE_FRAMEWORKS.keys())
            raise ValueError(f"Framework '{self.framework}' non supporté. "
                           f"Frameworks disponibles: {available}")
        
        framework_info = self.AVAILABLE_FRAMEWORKS[self.framework]
        
        try:
            # Importer le module
            module = __import__(framework_info['module'], fromlist=[
                framework_info['factory_class'],
                framework_info['app_class']
            ])
            
            # Obtenir les classes
            factory_class = getattr(module, framework_info['factory_class'])
            app_class = getattr(module, framework_info['app_class'])
            
            # Créer la factory
            self._factory = factory_class()
            self._app_class = app_class
            
            print(f"✅ Framework GUI '{self.framework}' chargé avec succès")
            
        except ImportError as e:
            raise ImportError(f"Impossible d'importer le framework '{self.framework}': {e}")
        except AttributeError as e:
            raise AttributeError(f"Classes manquantes dans le framework '{self.framework}': {e}")
    
    def get_factory(self) -> AbstractGUIFactory:
        """Retourne la factory GUI"""
        return self._factory
    
    def create_application(self) -> AbstractApplication:
        """Crée une nouvelle application"""
        return self._app_class()
    
    def get_current_framework(self) -> str:
        """Retourne le framework actuellement utilisé"""
        return self.framework
    
    def get_available_frameworks(self) -> list:
        """Retourne la liste des frameworks disponibles"""
        return list(self.AVAILABLE_FRAMEWORKS.keys())
    
    def switch_framework(self, new_framework: str):
        """Change de framework GUI"""
        old_framework = self.framework
        self.framework = new_framework.lower()
        
        try:
            self._load_framework()
            print(f"🔄 Framework changé de '{old_framework}' vers '{new_framework}'")
        except Exception as e:
            # Revenir à l'ancien framework en cas d'erreur
            self.framework = old_framework
            self._load_framework()
            raise e

# Instance globale du gestionnaire GUI
_gui_manager = None

def get_gui_manager(framework: str = None) -> GUIManager:
    """
    Obtient l'instance globale du gestionnaire GUI
    
    Args:
        framework: Framework à utiliser (seulement au premier appel)
    
    Returns:
        Instance du GUIManager
    """
    global _gui_manager
    
    if _gui_manager is None:
        _gui_manager = GUIManager(framework)
    elif framework is not None and framework != _gui_manager.get_current_framework():
        # Changer de framework si demandé
        _gui_manager.switch_framework(framework)
    
    return _gui_manager

def set_gui_framework(framework: str):
    """
    Définit le framework GUI à utiliser
    
    Args:
        framework: Nom du framework ('customtkinter', 'tkinter', etc.)
    """
    global _gui_manager
    
    if _gui_manager is None:
        _gui_manager = GUIManager(framework)
    else:
        _gui_manager.switch_framework(framework)

def get_gui_factory() -> AbstractGUIFactory:
    """Raccourci pour obtenir la factory GUI"""
    return get_gui_manager().get_factory()

def create_gui_application() -> AbstractApplication:
    """Raccourci pour créer une application GUI"""
    return get_gui_manager().create_application()

# Configuration par défaut
DEFAULT_FRAMEWORK = 'customtkinter'

# Fonction utilitaire pour les tests
def test_framework_switching():
    """Teste le changement de framework"""
    print("🧪 Test du changement de framework")
    
    # Test CustomTkinter
    manager = get_gui_manager('customtkinter')
    print(f"Framework actuel: {manager.get_current_framework()}")
    
    factory = manager.get_factory()
    print(f"Factory: {type(factory).__name__}")
    
    # Test Tkinter
    manager.switch_framework('tkinter')
    print(f"Framework après changement: {manager.get_current_framework()}")
    
    factory = manager.get_factory()
    print(f"Nouvelle factory: {type(factory).__name__}")
    
    print("✅ Test de changement de framework réussi")

if __name__ == "__main__":
    test_framework_switching()
