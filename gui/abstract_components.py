#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composants UI abstraits de haut niveau
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable, Tuple
from .abstract_gui import AbstractWidget, AbstractGUIFactory
from .gui_manager import get_gui_factory

class AbstractWindow(ABC):
    """Fenêtre abstraite de base"""
    
    def __init__(self, parent: AbstractWidget = None, title: str = "", geometry: str = "800x600"):
        self.gui_factory = get_gui_factory()
        self.parent = parent
        self.title = title
        self.geometry = geometry
        self.window = None
        self.widgets = {}
        
        self._create_window()
    
    def _create_window(self):
        """Crée la fenêtre"""
        if self.parent:
            self.window = self.gui_factory.create_toplevel(
                self.parent, self.title, self.geometry
            )
        else:
            self.window = self.gui_factory.create_window(
                self.title, self.geometry
            )
    
    @abstractmethod
    def create_widgets(self):
        """Crée les widgets de la fenêtre"""
        pass
    
    def show(self):
        """Affiche la fenêtre"""
        if not self.widgets:
            self.create_widgets()
    
    def hide(self):
        """Cache la fenêtre"""
        if self.window:
            native = self.window.get_native_widget()
            if hasattr(native, 'withdraw'):
                native.withdraw()
    
    def destroy(self):
        """Détruit la fenêtre"""
        if self.window:
            native = self.window.get_native_widget()
            if hasattr(native, 'destroy'):
                native.destroy()
    
    def get_native_window(self):
        """Retourne la fenêtre native"""
        return self.window.get_native_widget() if self.window else None

class AbstractForm(AbstractWindow):
    """Formulaire abstrait"""
    
    def __init__(self, parent: AbstractWidget = None, title: str = "Formulaire", geometry: str = "600x400"):
        self.fields = {}
        self.buttons = {}
        super().__init__(parent, title, geometry)
    
    def add_field(self, name: str, label: str, field_type: str = "entry", **kwargs) -> AbstractWidget:
        """Ajoute un champ au formulaire"""
        if not hasattr(self, 'form_frame'):
            self.form_frame = self.gui_factory.create_frame(self.window)
            self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Créer le label
        label_widget = self.gui_factory.create_label(self.form_frame, text=label)
        label_widget.pack(anchor="w", padx=10, pady=(10, 0))
        
        # Créer le champ selon le type
        if field_type == "entry":
            field_widget = self.gui_factory.create_entry(self.form_frame, **kwargs)
        elif field_type == "text":
            field_widget = self.gui_factory.create_text(self.form_frame, **kwargs)
        elif field_type == "combobox":
            field_widget = self.gui_factory.create_combobox(self.form_frame, **kwargs)
        else:
            raise ValueError(f"Type de champ non supporté: {field_type}")
        
        field_widget.pack(fill="x", padx=10, pady=5)
        
        self.fields[name] = {
            'label': label_widget,
            'field': field_widget,
            'type': field_type
        }
        
        return field_widget
    
    def add_button(self, name: str, text: str, command: Callable = None, **kwargs) -> AbstractWidget:
        """Ajoute un bouton au formulaire"""
        if not hasattr(self, 'buttons_frame'):
            self.buttons_frame = self.gui_factory.create_frame(self.window)
            self.buttons_frame.pack(fill="x", padx=20, pady=10)
        
        button = self.gui_factory.create_button(
            self.buttons_frame, text=text, command=command, **kwargs
        )
        button.pack(side="left", padx=5)
        
        self.buttons[name] = button
        return button
    
    def get_field_value(self, name: str) -> str:
        """Obtient la valeur d'un champ"""
        if name not in self.fields:
            raise KeyError(f"Champ '{name}' non trouvé")
        
        field = self.fields[name]['field']
        native = field.get_native_widget()
        
        if hasattr(native, 'get'):
            return native.get()
        else:
            return ""
    
    def set_field_value(self, name: str, value: str):
        """Définit la valeur d'un champ"""
        if name not in self.fields:
            raise KeyError(f"Champ '{name}' non trouvé")
        
        field = self.fields[name]['field']
        native = field.get_native_widget()
        
        if hasattr(native, 'delete') and hasattr(native, 'insert'):
            native.delete(0, 'end')
            native.insert(0, value)
        elif hasattr(native, 'set'):
            native.set(value)
    
    def clear_form(self):
        """Vide tous les champs du formulaire"""
        for name in self.fields:
            self.set_field_value(name, "")
    
    def validate_form(self) -> List[str]:
        """Valide le formulaire et retourne les erreurs"""
        errors = []
        # À implémenter dans les classes dérivées
        return errors

class AbstractListWindow(AbstractWindow):
    """Fenêtre avec liste abstraite"""
    
    def __init__(self, parent: AbstractWidget = None, title: str = "Liste", geometry: str = "800x600"):
        self.columns = []
        self.treeview = None
        self.search_entry = None
        super().__init__(parent, title, geometry)
    
    def set_columns(self, columns: List[str]):
        """Définit les colonnes de la liste"""
        self.columns = columns
    
    def create_list_widgets(self):
        """Crée les widgets de la liste"""
        # Frame principal
        main_frame = self.gui_factory.create_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barre de recherche
        search_frame = self.gui_factory.create_frame(main_frame)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = self.gui_factory.create_label(search_frame, text="Buscar:")
        search_label.pack(side="left", padx=(0, 5))
        
        self.search_entry = self.gui_factory.create_entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # Liste
        list_frame = self.gui_factory.create_frame(main_frame)
        list_frame.pack(fill="both", expand=True)
        
        self.treeview = self.gui_factory.create_treeview(
            list_frame, columns=self.columns, show="headings"
        )
        
        # Configurer les colonnes
        native_tree = self.treeview.get_native_widget()
        for col in self.columns:
            native_tree.heading(col, text=col)
            native_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = self.gui_factory.create_scrollbar(list_frame, orient="vertical")
        
        # Connecter scrollbar et treeview
        native_tree.configure(yscrollcommand=scrollbar.get_native_widget().set)
        scrollbar.get_native_widget().configure(command=native_tree.yview)
        
        # Empaqueter
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_item(self, values: List[str], tags: Tuple = None):
        """Ajoute un élément à la liste"""
        if self.treeview:
            native_tree = self.treeview.get_native_widget()
            native_tree.insert("", "end", values=values, tags=tags or ())
    
    def clear_list(self):
        """Vide la liste"""
        if self.treeview:
            native_tree = self.treeview.get_native_widget()
            for item in native_tree.get_children():
                native_tree.delete(item)
    
    def get_selected_item(self):
        """Retourne l'élément sélectionné"""
        if self.treeview:
            native_tree = self.treeview.get_native_widget()
            selection = native_tree.selection()
            if selection:
                return native_tree.item(selection[0])
        return None
    
    @abstractmethod
    def load_data(self):
        """Charge les données dans la liste"""
        pass
    
    @abstractmethod
    def on_item_selected(self, event=None):
        """Gère la sélection d'un élément"""
        pass
