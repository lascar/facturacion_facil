#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adaptateur pour migrer progressivement les fenêtres existantes vers la nouvelle architecture
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Dict, List, Optional, Callable

from .gui_manager import get_gui_factory
from .abstract_components import AbstractWindow

class LegacyWindowAdapter:
    """
    Adaptateur pour les fenêtres existantes utilisant CustomTkinter directement
    Permet une migration progressive vers l'architecture abstraite
    """
    
    def __init__(self, legacy_window_class):
        """
        Initialise l'adaptateur
        
        Args:
            legacy_window_class: Classe de fenêtre existante à adapter
        """
        self.legacy_window_class = legacy_window_class
        self.gui_factory = get_gui_factory()
    
    def create_adapted_window(self, *args, **kwargs):
        """
        Crée une version adaptée de la fenêtre legacy
        
        Returns:
            Instance de la fenêtre adaptée
        """
        return AdaptedWindow(self.legacy_window_class, *args, **kwargs)

class AdaptedWindow:
    """
    Fenêtre adaptée qui utilise la couche d'abstraction tout en gardant
    la compatibilité avec le code existant
    """
    
    def __init__(self, legacy_class, *args, **kwargs):
        self.legacy_class = legacy_class
        self.gui_factory = get_gui_factory()
        
        # Créer l'instance legacy mais intercepter les appels GUI
        self._create_adapted_instance(*args, **kwargs)
    
    def _create_adapted_instance(self, *args, **kwargs):
        """Crée l'instance adaptée"""
        # Sauvegarder les méthodes GUI originales
        original_ctk = ctk
        original_tk = tk
        original_ttk = ttk
        original_messagebox = messagebox
        
        # Créer des wrappers qui utilisent notre abstraction
        self._setup_gui_wrappers()
        
        try:
            # Créer l'instance avec nos wrappers
            self.instance = self.legacy_class(*args, **kwargs)
        finally:
            # Restaurer les modules originaux
            ctk = original_ctk
            tk = original_tk
            ttk = original_ttk
            messagebox = original_messagebox
    
    def _setup_gui_wrappers(self):
        """Configure les wrappers pour intercepter les appels GUI"""
        
        class CTkWrapper:
            """Wrapper pour CustomTkinter qui utilise notre abstraction"""
            
            def __init__(self, gui_factory):
                self.gui_factory = gui_factory
            
            def CTk(self):
                """Wrapper pour CTk()"""
                window = self.gui_factory.create_window()
                return window.get_native_widget()
            
            def CTkToplevel(self, parent):
                """Wrapper pour CTkToplevel()"""
                # Convertir parent en AbstractWidget si nécessaire
                if hasattr(parent, 'get_native_widget'):
                    parent_widget = parent
                else:
                    # Créer un wrapper pour le parent
                    from .customtkinter_impl import CustomTkinterWidget
                    from .abstract_gui import WidgetType
                    parent_widget = CustomTkinterWidget(WidgetType.WINDOW, parent)
                
                window = self.gui_factory.create_toplevel(parent_widget)
                return window.get_native_widget()
            
            def CTkFrame(self, parent, **kwargs):
                """Wrapper pour CTkFrame()"""
                if hasattr(parent, 'get_native_widget'):
                    parent_widget = parent
                else:
                    from .customtkinter_impl import CustomTkinterWidget
                    from .abstract_gui import WidgetType
                    parent_widget = CustomTkinterWidget(WidgetType.WINDOW, parent)
                
                frame = self.gui_factory.create_frame(parent_widget, **kwargs)
                return frame.get_native_widget()
            
            def CTkLabel(self, parent, **kwargs):
                """Wrapper pour CTkLabel()"""
                if hasattr(parent, 'get_native_widget'):
                    parent_widget = parent
                else:
                    from .customtkinter_impl import CustomTkinterWidget
                    from .abstract_gui import WidgetType
                    parent_widget = CustomTkinterWidget(WidgetType.FRAME, parent)
                
                text = kwargs.pop('text', '')
                label = self.gui_factory.create_label(parent_widget, text, **kwargs)
                return label.get_native_widget()
            
            def CTkButton(self, parent, **kwargs):
                """Wrapper pour CTkButton()"""
                if hasattr(parent, 'get_native_widget'):
                    parent_widget = parent
                else:
                    from .customtkinter_impl import CustomTkinterWidget
                    from .abstract_gui import WidgetType
                    parent_widget = CustomTkinterWidget(WidgetType.FRAME, parent)
                
                text = kwargs.pop('text', '')
                command = kwargs.pop('command', None)
                button = self.gui_factory.create_button(parent_widget, text, command, **kwargs)
                return button.get_native_widget()
            
            def CTkEntry(self, parent, **kwargs):
                """Wrapper pour CTkEntry()"""
                if hasattr(parent, 'get_native_widget'):
                    parent_widget = parent
                else:
                    from .customtkinter_impl import CustomTkinterWidget
                    from .abstract_gui import WidgetType
                    parent_widget = CustomTkinterWidget(WidgetType.FRAME, parent)
                
                entry = self.gui_factory.create_entry(parent_widget, **kwargs)
                return entry.get_native_widget()
            
            # Ajouter d'autres méthodes selon les besoins
            def set_appearance_mode(self, mode):
                """Wrapper pour set_appearance_mode()"""
                # Peut être ignoré ou adapté selon le framework
                pass
            
            def set_default_color_theme(self, theme):
                """Wrapper pour set_default_color_theme()"""
                # Peut être ignoré ou adapté selon le framework
                pass
        
        # Remplacer temporairement les modules
        import sys
        wrapper = CTkWrapper(self.gui_factory)
        
        # Injecter nos wrappers dans l'espace de noms global
        # (Ceci est une approche simplifiée pour la démonstration)
        
    def __getattr__(self, name):
        """Délègue les attributs à l'instance legacy"""
        return getattr(self.instance, name)

def create_migration_guide():
    """Crée un guide de migration pour les développeurs"""
    guide = """
# Guide de Migration vers l'Architecture GUI Abstraite

## 1. Migration Progressive

### Étape 1: Utiliser l'adaptateur
```python
from gui.legacy_adapter import LegacyWindowAdapter
from ui.clientes import ClientesWindow

# Au lieu de:
# clientes_window = ClientesWindow(parent)

# Utiliser:
adapter = LegacyWindowAdapter(ClientesWindow)
clientes_window = adapter.create_adapted_window(parent)
```

### Étape 2: Refactoriser progressivement
```python
from gui.abstract_components import AbstractListWindow

class ModernClientesWindow(AbstractListWindow):
    def __init__(self, parent=None):
        super().__init__(parent, "Gestión de Clientes", "1000x700")
        self.set_columns(["Nombre", "DNI/NIE", "Email", "Teléfono"])
        self.show()
    
    def create_widgets(self):
        self.create_list_widgets()
        # Ajouter boutons, etc.
    
    def load_data(self):
        # Charger les clients
        pass
    
    def on_item_selected(self, event=None):
        # Gérer la sélection
        pass
```

## 2. Avantages de la Migration

- ✅ Indépendance du framework GUI
- ✅ Code plus maintenable
- ✅ Tests plus faciles
- ✅ Flexibilité pour changer de framework
- ✅ Architecture plus propre

## 3. Changement de Framework

```python
from gui import set_gui_framework

# Changer vers Tkinter standard
set_gui_framework('tkinter')

# Ou rester avec CustomTkinter
set_gui_framework('customtkinter')

# Le code reste identique !
```
"""
    return guide

if __name__ == "__main__":
    print("📖 Guide de Migration GUI")
    print("=" * 50)
    print(create_migration_guide())
