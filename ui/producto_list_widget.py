#\!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget simple para lista de productos - Version PyQt6
"""

class ProductoListWidget:
    """Widget simplificado para lista de productos"""
    
    def __init__(self, parent=None):
        self.parent = parent
        print("ProductoListWidget inicializado")
    
    def add_producto(self, producto):
        """Agrega un producto a la lista"""
        print(f"Producto agregado: {producto}")
    
    def remove_producto(self, producto_id):
        """Remueve un producto de la lista"""
        print(f"Producto removido: {producto_id}")
    
    def get_selected_producto(self):
        """Obtiene el producto seleccionado"""
        return None
    
    def clear_list(self):
        """Limpia la lista"""
        print("Lista limpiada")
    
    def refresh_list(self):
        """Refresca la lista"""
        print("Lista refrescada")
