# -*- coding: utf-8 -*-
"""
Componente simple de autocompletado de productos para CustomTkinter
Versión simplificada que evita problemas de constructores
"""
import customtkinter as ctk
import tkinter as tk
from typing import List, Dict, Callable, Optional
from database.models import Producto, Stock
from utils.logger import get_logger

logger = get_logger("simple_producto_autocomplete")

class SimpleProductoAutocomplete(ctk.CTkFrame):
    """
    Widget simple de autocompletado para productos
    """
    
    def __init__(self, parent, **kwargs):
        # Solo pasar argumentos seguros al constructor padre
        safe_kwargs = {k: v for k, v in kwargs.items() 
                      if k in ['fg_color', 'border_color', 'border_width', 'corner_radius', 'width', 'height']}
        super().__init__(parent, **safe_kwargs)
        
        # Configuración
        self.placeholder_text = kwargs.get('placeholder_text', "Buscar producto...")
        self.include_stock_info = kwargs.get('include_stock_info', True)
        self.min_chars = kwargs.get('min_chars', 2)
        self.max_suggestions = kwargs.get('max_suggestions', 15)
        
        # Variables
        self.productos_data: List[Producto] = []
        self.suggestions_data: List[Dict] = []
        self.filtered_suggestions: List[Dict] = []
        self.selected_item: Optional[Dict] = None
        self.on_select_callback: Optional[Callable] = None
        
        # Estado del dropdown
        self.dropdown_visible = False
        
        self.create_widgets()
        self.load_productos_data()
    
    def create_widgets(self):
        """Crea los widgets del componente"""
        # Entry principal
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=self.placeholder_text,
            width=self.winfo_reqwidth() if hasattr(self, 'winfo_reqwidth') else 300
        )
        self.entry.pack(fill="x", padx=5, pady=5)
        
        # Frame para dropdown (inicialmente oculto)
        self.dropdown_frame = ctk.CTkFrame(self)
        # No hacer pack inicialmente
        
        # Textbox para mostrar sugerencias (más simple que Listbox)
        self.suggestions_text = ctk.CTkTextbox(
            self.dropdown_frame,
            height=150,
            wrap="none"
        )
        self.suggestions_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configurar eventos
        self.setup_bindings()
    
    def setup_bindings(self):
        """Configura los eventos"""
        self.entry.bind('<KeyRelease>', self.on_key_release)
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<Button-1>', self.on_entry_click)
        
        # Navegación básica
        self.entry.bind('<Down>', self.on_arrow_down)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Escape>', self.on_escape)
        
        # Eventos del textbox de sugerencias
        self.suggestions_text.bind('<Button-1>', self.on_suggestion_click)
        self.suggestions_text.bind('<Double-Button-1>', self.on_suggestion_double_click)
    
    def load_productos_data(self):
        """Carga los datos de productos desde la base de datos"""
        try:
            self.productos_data = Producto.get_all()
            
            # Convertir a formato para autocompletado
            self.suggestions_data = []
            for producto in self.productos_data:
                # Obtener información de stock si se requiere
                stock_info = ""
                if self.include_stock_info:
                    try:
                        stock = Stock.get_by_producto_id(producto.id)
                        if stock:
                            cantidad = stock.cantidad_disponible
                            if cantidad <= 0:
                                stock_info = " (Sin stock)"
                            elif cantidad <= 5:
                                stock_info = f" (Stock bajo: {cantidad})"
                            else:
                                stock_info = f" (Stock: {cantidad})"
                        else:
                            stock_info = " (Sin stock)"
                    except Exception as e:
                        logger.warning(f"Error obteniendo stock para producto {producto.id}: {e}")
                        stock_info = ""
                
                # Crear entrada para autocompletado
                suggestion = {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'referencia': producto.referencia,
                    'precio': producto.precio,
                    'categoria': producto.categoria or "",
                    'descripcion': producto.descripcion or "",
                    'iva_recomendado': producto.iva_recomendado,
                    'imagen_path': producto.imagen_path or "",
                    'producto_obj': producto,
                    'stock_info': stock_info,
                    'display_text': self.create_display_text(producto, stock_info),
                    'search_text': f"{producto.nombre} {producto.referencia} {producto.categoria or ''}".lower()
                }
                
                self.suggestions_data.append(suggestion)
            
            logger.info(f"Cargados {len(self.suggestions_data)} productos para autocompletado")
            
        except Exception as e:
            logger.error(f"Error cargando datos de productos: {e}")
            self.suggestions_data = []
    
    def create_display_text(self, producto: Producto, stock_info: str = "") -> str:
        """Crea el texto de display para un producto"""
        precio_text = f"€{producto.precio:.2f}" if producto.precio else "€0.00"
        
        # Formato: "Nombre - REF001 - €25.50 (Stock: 10)"
        display_parts = [
            producto.nombre,
            producto.referencia,
            precio_text
        ]
        
        if stock_info:
            display_parts.append(stock_info)
        
        return " - ".join(display_parts)
    
    def filter_suggestions(self, query: str):
        """Filtra las sugerencias basándose en la consulta"""
        if len(query) < self.min_chars:
            self.filtered_suggestions = []
            return
        
        query_lower = query.lower()
        self.filtered_suggestions = []
        
        for item in self.suggestions_data:
            if query_lower in item['search_text']:
                self.filtered_suggestions.append(item)
                
                # Limitar número de sugerencias
                if len(self.filtered_suggestions) >= self.max_suggestions:
                    break
        
        logger.debug(f"Filtradas {len(self.filtered_suggestions)} sugerencias para '{query}'")
    
    def update_suggestions_display(self):
        """Actualiza el display de sugerencias"""
        # Limpiar textbox
        self.suggestions_text.delete("1.0", tk.END)
        
        if not self.filtered_suggestions:
            self.hide_dropdown()
            return
        
        # Añadir sugerencias al textbox
        for i, item in enumerate(self.filtered_suggestions):
            display_text = item['display_text']
            self.suggestions_text.insert(tk.END, f"{i+1}. {display_text}\n")
        
        # Mostrar dropdown
        self.show_dropdown()
    
    def show_dropdown(self):
        """Muestra el dropdown de sugerencias"""
        if not self.dropdown_visible:
            self.dropdown_frame.pack(fill="x", padx=5, pady=(0, 5))
            self.dropdown_visible = True
            logger.debug("Dropdown mostrado")
    
    def hide_dropdown(self):
        """Oculta el dropdown de sugerencias"""
        if self.dropdown_visible:
            self.dropdown_frame.pack_forget()
            self.dropdown_visible = False
            logger.debug("Dropdown ocultado")
    
    def select_suggestion(self, index: int):
        """Selecciona una sugerencia por índice"""
        if 0 <= index < len(self.filtered_suggestions):
            selected_item = self.filtered_suggestions[index]
            self.selected_item = selected_item
            
            # Actualizar texto del entry
            display_text = f"{selected_item['nombre']} - {selected_item['referencia']}"
            self.entry.delete(0, tk.END)
            self.entry.insert(0, display_text)
            
            # Ocultar dropdown
            self.hide_dropdown()
            
            # Ejecutar callback
            if self.on_select_callback:
                self.on_select_callback(selected_item)
            
            logger.info(f"Seleccionado: {display_text}")
    
    # Event handlers
    def on_key_release(self, event):
        """Maneja la liberación de teclas en el entry"""
        query = self.entry.get()
        self.filter_suggestions(query)
        self.update_suggestions_display()
    
    def on_focus_in(self, event):
        """Maneja el foco en el entry"""
        query = self.entry.get()
        if query:
            self.filter_suggestions(query)
            self.update_suggestions_display()
    
    def on_focus_out(self, event):
        """Maneja la pérdida de foco del entry"""
        # Pequeño delay para permitir clicks en el dropdown
        self.after(200, self.hide_dropdown)
    
    def on_entry_click(self, event):
        """Maneja clicks en el entry"""
        query = self.entry.get()
        if query:
            self.filter_suggestions(query)
            self.update_suggestions_display()
    
    def on_arrow_down(self, event):
        """Maneja flecha abajo - mostrar sugerencias"""
        if not self.dropdown_visible:
            query = self.entry.get()
            if query:
                self.filter_suggestions(query)
                self.update_suggestions_display()
        return "break"
    
    def on_enter(self, event):
        """Maneja Enter - seleccionar primera sugerencia"""
        if self.dropdown_visible and self.filtered_suggestions:
            self.select_suggestion(0)
        return "break"
    
    def on_escape(self, event):
        """Maneja Escape - ocultar dropdown"""
        self.hide_dropdown()
        return "break"
    
    def on_suggestion_click(self, event):
        """Maneja clicks en las sugerencias"""
        # Obtener línea clickeada
        try:
            index = self.suggestions_text.index(tk.CURRENT).split('.')[0]
            line_num = int(index) - 1
            if 0 <= line_num < len(self.filtered_suggestions):
                self.select_suggestion(line_num)
        except (ValueError, IndexError):
            pass
    
    def on_suggestion_double_click(self, event):
        """Maneja doble-clicks en las sugerencias"""
        self.on_suggestion_click(event)
    
    # Métodos públicos
    def set_on_select_callback(self, callback: Callable[[Dict], None]):
        """Establece el callback que se ejecuta al seleccionar un elemento"""
        self.on_select_callback = callback
    
    def get_selected_producto(self) -> Optional[Producto]:
        """Obtiene el producto seleccionado"""
        if self.selected_item and 'producto_obj' in self.selected_item:
            return self.selected_item['producto_obj']
        return None
    
    def get_selected_producto_id(self) -> Optional[int]:
        """Obtiene el ID del producto seleccionado"""
        if self.selected_item and 'id' in self.selected_item:
            return self.selected_item['id']
        return None
    
    def get_selected_item(self) -> Optional[Dict]:
        """Obtiene el elemento seleccionado"""
        return self.selected_item
    
    def validate_selection(self) -> bool:
        """Valida que hay un producto seleccionado válido"""
        return self.selected_item is not None and self.get_value().strip() != ""
    
    def get_validation_error(self) -> str:
        """Obtiene mensaje de error de validación"""
        if not self.get_value().strip():
            return "Debe seleccionar un producto"
        
        if not self.validate_selection():
            return "Debe seleccionar un producto válido de la lista"
        
        return ""
    
    def get_value(self) -> str:
        """Obtiene el valor actual del entry"""
        return self.entry.get()
    
    def set_value(self, value: str):
        """Establece el valor del entry"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def clear(self):
        """Limpia el entry y la selección"""
        self.entry.delete(0, tk.END)
        self.selected_item = None
        self.hide_dropdown()
    
    def refresh_data(self):
        """Refresca los datos de productos desde la base de datos"""
        logger.info("Refrescando datos de productos...")
        self.load_productos_data()
    
    def focus(self):
        """Pone el foco en el entry"""
        self.entry.focus()
