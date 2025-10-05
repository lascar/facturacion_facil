# -*- coding: utf-8 -*-
"""
Composant d'autocomplétion spécialisé pour la sélection de produits
"""
import customtkinter as ctk
from typing import List, Dict, Callable, Optional
from common.autocomplete_entry import AutocompleteEntry
from database.models import Producto
from utils.logger import get_logger

logger = get_logger("producto_autocomplete")

class ProductoAutocomplete(AutocompleteEntry):
    """
    Widget d'autocomplétion spécialisé pour sélectionner produits
    """
    
    def __init__(self, parent,
                 placeholder_text: str = "Buscar producto por nombre o referencia...",
                 include_stock_info: bool = True,
                 width: int = 300,
                 height: int = 40,
                 max_suggestions: int = 15,
                 min_chars: int = 2,
                 **kwargs):

        self.include_stock_info = include_stock_info
        self.productos_data: List[Producto] = []

        # Filtrar kwargs para evitar conflictos
        safe_kwargs = {k: v for k, v in kwargs.items()
                      if k in ['fg_color', 'border_color', 'border_width', 'corner_radius']}

        super().__init__(
            parent,
            placeholder_text=placeholder_text,
            max_suggestions=max_suggestions,
            min_chars=min_chars,
            width=width,
            height=height,
            **safe_kwargs
        )

        # Configurar campos de búsqueda después de la inicialización
        self.search_fields = ['search_text']  # Usaremos un campo combinado

        self.load_productos_data()
    
    def load_productos_data(self):
        """Carga los datos de productos desde la base de datos"""
        try:
            self.productos_data = Producto.get_all()
            
            # Convertir a formato para autocompletado
            suggestions_data = []
            for producto in self.productos_data:
                # Obtener información de stock si se requiere
                stock_info = ""
                if self.include_stock_info:
                    try:
                        from database.models import Stock
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
                    'producto_obj': producto,  # Referencia al objeto completo
                    'stock_info': stock_info,
                    'display_text': self.create_display_text(producto, stock_info),
                    'search_text': f"{producto.nombre} {producto.referencia} {producto.categoria or ''}".lower()
                }
                
                suggestions_data.append(suggestion)
            
            # Configurar datos en el componente base
            self.set_suggestions_data(suggestions_data)
            # Los search_fields ya están configurados en __init__
            
            logger.info(f"Cargados {len(suggestions_data)} productos para autocompletado")
            
        except Exception as e:
            logger.error(f"Error cargando datos de productos: {e}")
            self.set_suggestions_data([])
    
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
    
    def format_suggestion_display(self, item: Dict) -> str:
        """Formatea cómo se muestra cada sugerencia en el dropdown"""
        return item['display_text']
    
    def get_selected_display_text(self, item: Dict) -> str:
        """Texto que se muestra en el entry al seleccionar"""
        # Solo mostrar nombre y referencia en el entry
        return f"{item['nombre']} - {item['referencia']}"
    
    def get_selected_producto(self) -> Optional[Producto]:
        """Obtiene el producto seleccionado"""
        selected = self.get_selected_item()
        if selected and 'producto_obj' in selected:
            return selected['producto_obj']
        return None
    
    def get_selected_producto_id(self) -> Optional[int]:
        """Obtiene el ID del producto seleccionado"""
        selected = self.get_selected_item()
        if selected and 'id' in selected:
            return selected['id']
        return None
    
    def get_selected_producto_info(self) -> Optional[Dict]:
        """Obtiene información completa del producto seleccionado"""
        selected = self.get_selected_item()
        if selected:
            return {
                'id': selected['id'],
                'nombre': selected['nombre'],
                'referencia': selected['referencia'],
                'precio': selected['precio'],
                'categoria': selected['categoria'],
                'descripcion': selected['descripcion'],
                'iva_recomendado': selected['iva_recomendado'],
                'imagen_path': selected['imagen_path'],
                'producto': selected['producto_obj']
            }
        return None
    
    def refresh_data(self):
        """Refresca los datos de productos desde la base de datos"""
        logger.info("Refrescando datos de productos...")
        self.load_productos_data()
    
    def filter_by_categoria(self, categoria: str):
        """Filtra productos por categoría"""
        if not categoria:
            self.load_productos_data()
            return
        
        try:
            productos_filtrados = [p for p in self.productos_data if p.categoria == categoria]
            
            # Convertir a formato para autocompletado
            suggestions_data = []
            for producto in productos_filtrados:
                stock_info = ""
                if self.include_stock_info:
                    try:
                        from database.models import Stock
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
                    except Exception:
                        stock_info = ""
                
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
                
                suggestions_data.append(suggestion)
            
            self.set_suggestions_data(suggestions_data)
            logger.info(f"Filtrados {len(suggestions_data)} productos por categoría '{categoria}'")
            
        except Exception as e:
            logger.error(f"Error filtrando por categoría: {e}")
    
    def set_producto_by_id(self, producto_id: int):
        """Establece un producto por su ID"""
        try:
            for suggestion in self.suggestions_data:
                if suggestion['id'] == producto_id:
                    self.selected_item = suggestion
                    display_text = self.get_selected_display_text(suggestion)
                    self.set_value(display_text)
                    
                    # Ejecutar callback si existe
                    if self.on_select_callback:
                        self.on_select_callback(suggestion)
                    
                    logger.info(f"Producto establecido por ID: {producto_id}")
                    return True
            
            logger.warning(f"Producto con ID {producto_id} no encontrado")
            return False
            
        except Exception as e:
            logger.error(f"Error estableciendo producto por ID: {e}")
            return False
    
    def set_producto_by_referencia(self, referencia: str):
        """Establece un producto por su referencia"""
        try:
            for suggestion in self.suggestions_data:
                if suggestion['referencia'].lower() == referencia.lower():
                    self.selected_item = suggestion
                    display_text = self.get_selected_display_text(suggestion)
                    self.set_value(display_text)
                    
                    # Ejecutar callback si existe
                    if self.on_select_callback:
                        self.on_select_callback(suggestion)
                    
                    logger.info(f"Producto establecido por referencia: {referencia}")
                    return True
            
            logger.warning(f"Producto con referencia '{referencia}' no encontrado")
            return False
            
        except Exception as e:
            logger.error(f"Error estableciendo producto por referencia: {e}")
            return False
    
    def validate_selection(self) -> bool:
        """Valida que hay un producto seleccionado válido"""
        selected = self.get_selected_item()
        current_text = self.get_value().strip()
        
        if not selected or not current_text:
            return False
        
        # Verificar que el texto actual coincide con la selección
        expected_text = self.get_selected_display_text(selected)
        return current_text == expected_text
    
    def get_validation_error(self) -> str:
        """Obtiene mensaje de error de validación"""
        if not self.get_value().strip():
            return "Debe seleccionar un producto"
        
        if not self.validate_selection():
            return "Debe seleccionar un producto válido de la lista"
        
        return ""
