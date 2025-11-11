#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation Tkinter standard de la couche d'abstraction GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Any, Dict, List, Optional, Callable, Tuple

from .abstract_gui import (
    AbstractWidget, AbstractGUIFactory, AbstractApplication,
    WidgetType, PackSide, Anchor, Fill
)

class TkinterWidget(AbstractWidget):
    """Widget Tkinter standard"""
    
    def __init__(self, widget_type: WidgetType, native_widget: Any):
        super().__init__(widget_type)
        self._native_widget = native_widget
    
    def create_native_widget(self, parent=None, **kwargs) -> Any:
        """Le widget natif est déjà créé"""
        return self._native_widget
    
    def pack(self, **kwargs):
        """Empaquette le widget"""
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

class TkinterGUIFactory(AbstractGUIFactory):
    """Factory pour créer des widgets Tkinter standard"""
    
    def create_window(self, title: str = "", geometry: str = "800x600", **kwargs) -> AbstractWidget:
        """Crée une fenêtre principale"""
        window = tk.Tk()
        if title:
            window.title(title)
        window.geometry(geometry)
        
        return TkinterWidget(WidgetType.WINDOW, window)
    
    def create_toplevel(self, parent: AbstractWidget, title: str = "", geometry: str = "400x300", **kwargs) -> AbstractWidget:
        """Crée une fenêtre secondaire"""
        parent_native = parent.get_native_widget()
        window = tk.Toplevel(parent_native)
        if title:
            window.title(title)
        window.geometry(geometry)
        window.transient(parent_native)
        
        # Configuration par défaut pour les fenêtres secondaires
        window.lift()
        window.focus_force()
        
        return TkinterWidget(WidgetType.WINDOW, window)
    
    def create_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame"""
        parent_native = parent.get_native_widget()
        
        # Adapter les kwargs pour Tkinter standard
        tk_kwargs = self._adapt_frame_kwargs(kwargs)
        frame = tk.Frame(parent_native, **tk_kwargs)
        
        widget = TkinterWidget(WidgetType.FRAME, frame)
        parent.add_child(widget)
        return widget
    
    def create_scrollable_frame(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un frame scrollable (implémentation basique)"""
        parent_native = parent.get_native_widget()
        
        # Créer un canvas avec scrollbar pour simuler un frame scrollable
        canvas = tk.Canvas(parent_native)
        scrollbar = tk.Scrollbar(parent_native, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaqueter
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        widget = TkinterWidget(WidgetType.FRAME, scrollable_frame)
        parent.add_child(widget)
        return widget
    
    def create_label(self, parent: AbstractWidget, text: str = "", **kwargs) -> AbstractWidget:
        """Crée un label"""
        parent_native = parent.get_native_widget()
        
        # Adapter les kwargs pour Tkinter
        tk_kwargs = self._adapt_label_kwargs(kwargs)
        label = tk.Label(parent_native, text=text, **tk_kwargs)
        
        widget = TkinterWidget(WidgetType.LABEL, label)
        parent.add_child(widget)
        return widget
    
    def create_button(self, parent: AbstractWidget, text: str = "", command: Callable = None, **kwargs) -> AbstractWidget:
        """Crée un bouton"""
        parent_native = parent.get_native_widget()
        
        # Adapter les kwargs pour Tkinter
        tk_kwargs = self._adapt_button_kwargs(kwargs)
        button = tk.Button(parent_native, text=text, command=command, **tk_kwargs)
        
        widget = TkinterWidget(WidgetType.BUTTON, button)
        parent.add_child(widget)
        return widget
    
    def create_entry(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un champ de saisie"""
        parent_native = parent.get_native_widget()
        entry = tk.Entry(parent_native, **kwargs)
        widget = TkinterWidget(WidgetType.ENTRY, entry)
        parent.add_child(widget)
        return widget
    
    def create_text(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée un widget texte multiligne"""
        parent_native = parent.get_native_widget()
        text = tk.Text(parent_native, **kwargs)
        widget = TkinterWidget(WidgetType.TEXT, text)
        parent.add_child(widget)
        return widget
    
    def create_combobox(self, parent: AbstractWidget, values: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée une combobox"""
        parent_native = parent.get_native_widget()
        if values is None:
            values = []
        combobox = ttk.Combobox(parent_native, values=values, **kwargs)
        widget = TkinterWidget(WidgetType.COMBOBOX, combobox)
        parent.add_child(widget)
        return widget
    
    def create_treeview(self, parent: AbstractWidget, columns: List[str] = None, **kwargs) -> AbstractWidget:
        """Crée un treeview"""
        parent_native = parent.get_native_widget()
        if columns is None:
            columns = []
        treeview = ttk.Treeview(parent_native, columns=columns, **kwargs)
        widget = TkinterWidget(WidgetType.TREEVIEW, treeview)
        parent.add_child(widget)
        return widget
    
    def create_scrollbar(self, parent: AbstractWidget, **kwargs) -> AbstractWidget:
        """Crée une scrollbar"""
        parent_native = parent.get_native_widget()
        scrollbar = tk.Scrollbar(parent_native, **kwargs)
        widget = TkinterWidget(WidgetType.SCROLLBAR, scrollbar)
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
    
    def _adapt_frame_kwargs(self, kwargs: Dict) -> Dict:
        """Adapte les kwargs CustomTkinter pour Tkinter standard"""
        adapted = {}
        for key, value in kwargs.items():
            if key == "fg_color":
                adapted["bg"] = value
            elif key == "corner_radius":
                # Tkinter standard ne supporte pas les coins arrondis
                pass
            else:
                adapted[key] = value
        return adapted
    
    def _adapt_label_kwargs(self, kwargs: Dict) -> Dict:
        """Adapte les kwargs de label"""
        adapted = {}
        for key, value in kwargs.items():
            if key == "text_color":
                adapted["fg"] = value
            elif key == "font" and hasattr(value, "family"):
                # Convertir CTkFont en tuple Tkinter
                adapted["font"] = (value.family, value.size, value.weight)
            else:
                adapted[key] = value
        return adapted
    
    def _adapt_button_kwargs(self, kwargs: Dict) -> Dict:
        """Adapte les kwargs de bouton"""
        adapted = {}
        for key, value in kwargs.items():
            if key == "fg_color":
                adapted["bg"] = value
            elif key == "text_color":
                adapted["fg"] = value
            elif key == "hover_color":
                adapted["activebackground"] = value
            elif key == "font" and hasattr(value, "family"):
                adapted["font"] = (value.family, value.size, value.weight)
            else:
                adapted[key] = value
        return adapted

class TkinterApplication(AbstractApplication):
    """Application Tkinter standard"""
    
    def __init__(self):
        super().__init__(TkinterGUIFactory())
    
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
