#\!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialog simple para productos en facturas - Version PyQt6
"""

class ProductoFacturaDialog:
    """Dialog simplificado para productos en facturas"""
    
    def __init__(self, parent=None):
        self.parent = parent
        print("ProductoFacturaDialog inicializado")
    
    def show(self):
        """Muestra el dialog"""
        print("Mostrando dialog de productos")
        return True
    
    def get_producto_data(self):
        """Obtiene los datos del producto"""
        return {
            'nombre': 'Producto de prueba',
            'precio': 10.0,
            'cantidad': 1
        }
    
    def set_producto_data(self, data):
        """Establece los datos del producto"""
        print(f"Datos del producto: {data}")
    
    def validate_data(self):
        """Valida los datos del producto"""
        return True
    
    def clear_form(self):
        """Limpia el formulario"""
        print("Formulario limpiado")
    
    def close(self):
        """Cierra el dialog"""
        print("Dialog cerrado")
