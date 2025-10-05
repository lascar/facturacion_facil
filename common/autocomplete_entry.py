# -*- coding: utf-8 -*-
"""
Composant d'autocomplétion pour CustomTkinter
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Callable, Optional, Any
from utils.logger import get_logger

logger = get_logger("autocomplete_entry")

class AutocompleteEntry(ctk.CTkFrame):
    """
    Widget d'autocomplétion avec dropdown pour CustomTkinter
    """
    
    def __init__(self, parent,
                 placeholder_text: str = "Tapez pour rechercher...",
                 max_suggestions: int = 10,
                 min_chars: int = 1,
                 width: int = 300,
                 height: int = 40,
                 **kwargs):
        # Filtrar kwargs para CTkFrame (solo pasar argumentos válidos)
        valid_frame_args = ['fg_color', 'border_color', 'border_width', 'corner_radius',
                           'background_corner_colors', 'width', 'height']
        frame_kwargs = {k: v for k, v in kwargs.items() if k in valid_frame_args}
        super().__init__(parent, **frame_kwargs)
        
        self.placeholder_text = placeholder_text
        self.max_suggestions = max_suggestions
        self.min_chars = min_chars
        self.width = width
        self.height = height
        
        # Variables
        self.suggestions_data: List[Dict] = []
        self.filtered_suggestions: List[Dict] = []
        self.selected_item: Optional[Dict] = None
        self.on_select_callback: Optional[Callable] = None
        self.search_fields: List[str] = ['text']  # Campos por defecto para buscar
        
        # Variables de control
        self.dropdown_visible = False
        self.ignore_focus_out = False
        
        self.create_widgets()
        self.setup_bindings()
    
    def create_widgets(self):
        """Crea los widgets del componente"""
        # Entry principal
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=self.placeholder_text,
            width=self.width,
            height=self.height
        )
        self.entry.pack(fill="x", padx=2, pady=2)
        
        # Frame para dropdown (inicialmente oculto)
        self.dropdown_frame = tk.Toplevel(self.winfo_toplevel())
        self.dropdown_frame.withdraw()  # Ocultar inicialmente
        self.dropdown_frame.overrideredirect(True)  # Sin decoraciones de ventana
        self.dropdown_frame.configure(bg='white', relief='solid', bd=1)
        
        # Listbox para sugerencias
        self.suggestions_listbox = tk.Listbox(
            self.dropdown_frame,
            height=min(self.max_suggestions, 8),
            font=("Arial", 10),
            selectmode=tk.SINGLE,
            activestyle='dotbox'
        )
        self.suggestions_listbox.pack(fill="both", expand=True)
        
        # Scrollbar para listbox
        scrollbar = tk.Scrollbar(self.dropdown_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.suggestions_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.suggestions_listbox.yview)
    
    def setup_bindings(self):
        """Configura los eventos"""
        # Entry events
        self.entry.bind('<KeyRelease>', self.on_key_release)
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<Button-1>', self.on_entry_click)
        
        # Navegación con teclado
        self.entry.bind('<Down>', self.on_arrow_down)
        self.entry.bind('<Up>', self.on_arrow_up)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Escape>', self.on_escape)
        
        # Listbox events
        self.suggestions_listbox.bind('<Double-Button-1>', self.on_listbox_select)
        self.suggestions_listbox.bind('<Return>', self.on_listbox_select)
        self.suggestions_listbox.bind('<Button-1>', self.on_listbox_click)
        
        # Dropdown frame events
        self.dropdown_frame.bind('<FocusOut>', self.on_dropdown_focus_out)
    
    def set_suggestions_data(self, data: List[Dict], search_fields: List[str] = None):
        """
        Establece los datos para autocompletado
        
        Args:
            data: Lista de diccionarios con los datos
            search_fields: Campos en los que buscar (por defecto ['text'])
        """
        self.suggestions_data = data
        if search_fields:
            self.search_fields = search_fields
        
        logger.debug(f"Configurados {len(data)} elementos para autocompletado")
    
    def set_on_select_callback(self, callback: Callable[[Dict], None]):
        """Establece el callback que se ejecuta al seleccionar un elemento"""
        self.on_select_callback = callback
    
    def filter_suggestions(self, query: str):
        """Filtra las sugerencias basándose en la consulta"""
        if len(query) < self.min_chars:
            self.filtered_suggestions = []
            return
        
        query_lower = query.lower()
        self.filtered_suggestions = []
        
        for item in self.suggestions_data:
            # Buscar en todos los campos especificados
            match_found = False
            for field in self.search_fields:
                if field in item:
                    field_value = str(item[field]).lower()
                    if query_lower in field_value:
                        match_found = True
                        break
            
            if match_found:
                self.filtered_suggestions.append(item)
                
                # Limitar número de sugerencias
                if len(self.filtered_suggestions) >= self.max_suggestions:
                    break
        
        logger.debug(f"Filtradas {len(self.filtered_suggestions)} sugerencias para '{query}'")
    
    def update_dropdown(self):
        """Actualiza el contenido del dropdown"""
        # Limpiar listbox
        self.suggestions_listbox.delete(0, tk.END)
        
        if not self.filtered_suggestions:
            self.hide_dropdown()
            return
        
        # Añadir sugerencias
        for item in self.filtered_suggestions:
            # Crear texto de display
            display_text = self.format_suggestion_display(item)
            self.suggestions_listbox.insert(tk.END, display_text)
        
        # Mostrar dropdown
        self.show_dropdown()
    
    def format_suggestion_display(self, item: Dict) -> str:
        """
        Formatea cómo se muestra cada sugerencia
        Puede ser sobrescrito por subclases
        """
        if 'display_text' in item:
            return item['display_text']
        elif 'text' in item:
            return item['text']
        else:
            return str(item)
    
    def show_dropdown(self):
        """Muestra el dropdown de sugerencias"""
        if self.dropdown_visible:
            return
        
        # Calcular posición
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        width = self.entry.winfo_width()
        
        # Configurar geometría
        self.dropdown_frame.geometry(f"{width}x200+{x}+{y}")
        self.dropdown_frame.deiconify()
        self.dropdown_frame.lift()
        
        self.dropdown_visible = True
        logger.debug("Dropdown mostrado")
    
    def hide_dropdown(self):
        """Oculta el dropdown de sugerencias"""
        if not self.dropdown_visible:
            return
        
        self.dropdown_frame.withdraw()
        self.dropdown_visible = False
        logger.debug("Dropdown ocultado")
    
    def select_suggestion(self, index: int):
        """Selecciona una sugerencia por índice"""
        if 0 <= index < len(self.filtered_suggestions):
            selected_item = self.filtered_suggestions[index]
            self.selected_item = selected_item
            
            # Actualizar texto del entry
            display_text = self.get_selected_display_text(selected_item)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, display_text)
            
            # Ocultar dropdown
            self.hide_dropdown()
            
            # Ejecutar callback
            if self.on_select_callback:
                self.on_select_callback(selected_item)
            
            logger.info(f"Seleccionado: {display_text}")
    
    def get_selected_display_text(self, item: Dict) -> str:
        """
        Obtiene el texto que se muestra en el entry al seleccionar
        Puede ser sobrescrito por subclases
        """
        return self.format_suggestion_display(item)
    
    # Event handlers
    def on_key_release(self, event):
        """Maneja la liberación de teclas en el entry"""
        query = self.entry.get()
        self.filter_suggestions(query)
        self.update_dropdown()
    
    def on_focus_in(self, event):
        """Maneja el foco en el entry"""
        query = self.entry.get()
        if query:
            self.filter_suggestions(query)
            self.update_dropdown()
    
    def on_focus_out(self, event):
        """Maneja la pérdida de foco del entry"""
        if not self.ignore_focus_out:
            # Pequeño delay para permitir clicks en el dropdown
            self.after(100, self.hide_dropdown)
    
    def on_entry_click(self, event):
        """Maneja clicks en el entry"""
        query = self.entry.get()
        if query:
            self.filter_suggestions(query)
            self.update_dropdown()
    
    def on_arrow_down(self, event):
        """Maneja flecha abajo - navegar en sugerencias"""
        if self.dropdown_visible and self.suggestions_listbox.size() > 0:
            current = self.suggestions_listbox.curselection()
            if current:
                next_index = min(current[0] + 1, self.suggestions_listbox.size() - 1)
            else:
                next_index = 0
            
            self.suggestions_listbox.selection_clear(0, tk.END)
            self.suggestions_listbox.selection_set(next_index)
            self.suggestions_listbox.see(next_index)
        return "break"
    
    def on_arrow_up(self, event):
        """Maneja flecha arriba - navegar en sugerencias"""
        if self.dropdown_visible and self.suggestions_listbox.size() > 0:
            current = self.suggestions_listbox.curselection()
            if current:
                prev_index = max(current[0] - 1, 0)
            else:
                prev_index = self.suggestions_listbox.size() - 1
            
            self.suggestions_listbox.selection_clear(0, tk.END)
            self.suggestions_listbox.selection_set(prev_index)
            self.suggestions_listbox.see(prev_index)
        return "break"
    
    def on_enter(self, event):
        """Maneja Enter - seleccionar sugerencia actual"""
        if self.dropdown_visible:
            current = self.suggestions_listbox.curselection()
            if current:
                self.select_suggestion(current[0])
        return "break"
    
    def on_escape(self, event):
        """Maneja Escape - ocultar dropdown"""
        self.hide_dropdown()
        return "break"
    
    def on_listbox_select(self, event):
        """Maneja selección en el listbox"""
        selection = self.suggestions_listbox.curselection()
        if selection:
            self.select_suggestion(selection[0])
    
    def on_listbox_click(self, event):
        """Maneja clicks en el listbox"""
        self.ignore_focus_out = True
        self.after(100, lambda: setattr(self, 'ignore_focus_out', False))
    
    def on_dropdown_focus_out(self, event):
        """Maneja pérdida de foco del dropdown"""
        if not self.ignore_focus_out:
            self.hide_dropdown()
    
    # Métodos públicos
    def get_value(self) -> str:
        """Obtiene el valor actual del entry"""
        return self.entry.get()
    
    def set_value(self, value: str):
        """Establece el valor del entry"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def get_selected_item(self) -> Optional[Dict]:
        """Obtiene el elemento seleccionado"""
        return self.selected_item
    
    def clear(self):
        """Limpia el entry y la selección"""
        self.entry.delete(0, tk.END)
        self.selected_item = None
        self.hide_dropdown()
    
    def focus(self):
        """Pone el foco en el entry"""
        self.entry.focus()
    
    def configure_entry(self, **kwargs):
        """Configura el entry interno"""
        self.entry.configure(**kwargs)
