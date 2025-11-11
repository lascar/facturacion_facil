#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation CustomTkinter de la couche d'abstraction GUI
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Any, Dict, List, Optional, Callable, Tuple

from .abstract_gui import (
    AbstractWidget, AbstractGUIFactory, AbstractApplication,
    WidgetType, PackSide, Anchor, Fill
)

class CustomTkinterWidget(AbstractWidget):
    """Widget CustomTkinter"""
    
    def __init__(self, widget_type: WidgetType, native_widget: Any):
        super().__init__(widget_type)
        self._native_widget = native_widget
    
    def create_native_widget(self, parent=None, **kwargs) -> Any:
        """Le widget natif est déjà créé"""
        return self._native_widget
    
    def pack(self, **kwargs):
        """Empaquette le widget"""
        # Convertir les enums en valeurs
        converted_kwargs = self._convert_pack_kwargs(kwargs)
        self._native_widget.pack(**converted_kwargs)
    
    def grid(self, **kwargs):
        """Place le widget en grille"""
        self._native_widget.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place le widget avec coordonnées absolues"""
        self._native_widget.place(**kwargs)
    
    def configure(self, **kwargs):
        """Configure les propriétés du widget"""
        self._native_widget.configure(**kwargs)
    
    def get_native_widget(self) -> Any:
        """Retourne le widget natif"""
        return self._native_widget
    
    def _convert_pack_kwargs(self, kwargs: Dict) -> Dict:
        """Convertit les enums en valeurs pour pack"""
        converted = {}
        for key, value in kwargs.items():
            if isinstance(value, PackSide):
                converted[key] = value.value
            elif isinstance(value, Fill):
                converted[key] = value.value
            elif isinstance(value, Anchor):
                converted[key] = value.value
            else:
                converted[key] = value
        return converted

class CustomTkinterGUIFactory(AbstractGUIFactory):
    """Factory pour créer des widgets CustomTkinter"""
    
    def __init__(self):
        # Configuration par défaut de CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
    
    def create_window(self, title: str = "", geometry: str = "800x600", **kwargs) -> AbstractWidget:
        """Crée une fenêtre principale"""
        window = ctk.CTk()
        if title:
            window.title(title)
        window.geometry(geometry)
        
        # Appliquer les kwargs supplémentaires
        for key, value in kwargs.items():
            if hasattr(window, key):
                setattr(window, key, value)
        
        return CustomTkinterWidget(WidgetType.WINDOW, window)
    
    def create_toplevel(self, parent: AbstractWidget, title: str = "", geometry: str = "400x300", **kwargs) -> AbstractWidget:
        """Crée une fenêtre secondaire"""
        parent_native = parent.get_native_widget()
        window = ctk.CTkToplevel(parent_native)
        if title:
            window.title(title)
        window.geometry(geometry)
        window.transient(parent_native)
        
        # Configuration par défaut pour les fenêtres secondaires
        window.lift()
        window.focus_force()
        window.attributes('-topmost', True)
        window.after(100, lambda: window.attributes('-topmost', False))
        
        return CustomTkinterWidget(WidgetType.WINDOW, window)
    
    def create_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame"""
        parent_native = parent.get_native_widget()
        frame = ctk.CTkFrame(parent_native, **kwargs)
        widget = CustomTkinterWidget(WidgetType.FRAME, frame)
        parent.add_child(widget)
        return widget
    
    def create_scrollable_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame scrollable"""
        parent_native = parent.get_native_widget()
        frame = ctk.CTkScrollableFrame(parent_native, **kwargs)
        widget = CustomTkinterWidget(WidgetType.FRAME, frame)
        parent.add_child(widget)
        return widget
    
    def create_label(self, parent: AbstractWidget, text: str = "", **kwargs) -> AbstractWidget:
        """Crée un label"""
        parent_native = parent.get_native_widget()
        label = ctk.CTkLabel(parent_native, text=text, **kwargs)
        widget = CustomTkinterWidget(WidgetType.LABEL, label)
        parent.add_child(widget)
        return widget
    
    def create_button(self, parent: AbstractWidget, text: str = "", command: Callable = None, **kwargs) -> AbstractWidget:
        """Crée un bouton"""
        parent_native = parent.get_native_widget()
        button = ctk.CTkButton(parent_native, text=text, command=command, **kwargs)
        widget = CustomTkinterWidget(WidgetType.BUTTON, button)
        parent.add_child(widget)
        return widget
    
    def create_entry(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un champ de saisie"""
        parent_native = parent.get_native_widget()
        entry = ctk.CTkEntry(parent_native, **kwargs)
        widget = CustomTkinterWidget(WidgetType.ENTRY, entry)
        parent.add_child(widget)
        return widget
    
    def create_text(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un widget texte multiligne"""
        parent_native = parent.get_native_widget()
        text = ctk.CTkTextbox(parent_native, **kwargs)
        widget = CustomTkinterWidget(WidgetType.TEXT, text)
        parent.add_child(widget)
        return widget
    
    def create_combobox(self, parent: AbstractWidget, values: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée une combobox"""
        parent_native = parent.get_native_widget()
        if values is None:
            values = []
        combobox = ctk.CTkComboBox(parent_native, values=values, **kwargs)
        widget = CustomTkinterWidget(WidgetType.COMBOBOX, combobox)
        parent.add_child(widget)
        return widget
    
    def create_treeview(self, parent: AbstractWidget, columns: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée un treeview (utilise tkinter.ttk)"""
        parent_native = parent.get_native_widget()
        if columns is None:
            columns = []
        treeview = ttk.Treeview(parent_native, columns=columns, **kwargs)
        widget = CustomTkinterWidget(WidgetType.TREEVIEW, treeview)
        parent.add_child(widget)
        return widget
    
    def create_scrollbar(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée une scrollbar (utilise tkinter.ttk)"""
        parent_native = parent.get_native_widget()
        scrollbar = ttk.Scrollbar(parent_native, **kwargs)
        widget = CustomTkinterWidget(WidgetType.SCROLLBAR, scrollbar)
        parent.add_child(widget)
        return widget
    
    def show_message(self, message_type: str, title: str, message: str, **kwargs) -> Any:
        """Affiche un message"""
        if message_type == "info":
            return messagebox.showinfo(title, message)
        elif message_type == "warning":
            return messagebox.showwarning(title, message)
        elif message_type == "error":
            return messagebox.showerror(title, message)
        elif message_type == "question":
            return messagebox.askyesno(title, message)
        else:
            return messagebox.showinfo(title, message)
    
    def ask_file(self, **kwargs) -> Optional[str]:
        """Demande de sélectionner un fichier"""
        return filedialog.askopenfilename(**kwargs)
    
    def ask_directory(self, **kwargs) -> Optional[str]:
        """Demande de sélectionner un répertoire"""
        return filedialog.askdirectory(**kwargs)

class CustomTkinterApplication(AbstractApplication):
    """Application CustomTkinter"""
    
    def __init__(self):
        super().__init__(CustomTkinterGUIFactory())
    
    def initialize(self):
        """Initialise l'application"""
        self.main_window = self.gui_factory.create_window(
            title="Facturación Fácil",
            geometry="800x600"
        )
    
    def run(self):
        """Lance la boucle principale"""
        if self.main_window:
            self.main_window.get_native_widget().mainloop()
    
    def quit(self):
        """Quitte l'application"""
        if self.main_window:
            self.main_window.get_native_widget().quit()
