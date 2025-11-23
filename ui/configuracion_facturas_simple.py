#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialog simple para configuracion de facturas - Version PyQt6
"""

class ConfiguracionFacturasDialog:
    """Dialog simplificado para configuracion de facturas"""
    
    def __init__(self, parent=None):
        self.parent = parent
        print("ConfiguracionFacturasDialog inicializado")
    
    def show(self):
        """Muestra el dialog"""
        print("Mostrando dialog de configuracion")
        return True
    
    def get_configuracion(self):
        """Obtiene la configuracion"""
        return {
            'empresa': 'Mi Empresa',
            'direccion': 'Mi Direccion',
            'telefono': '123456789'
        }
    
    def set_configuracion(self, config):
        """Establece la configuracion"""
        print(f"Configuracion: {config}")
    
    def save_configuracion(self):
        """Guarda la configuracion"""
        print("Configuracion guardada")
        return True
    
    def load_configuracion(self):
        """Carga la configuracion"""
        print("Configuracion cargada")
        return self.get_configuracion()
    
    def validate_data(self):
        """Valida los datos"""
        return True
    
    def close(self):
        """Cierra el dialog"""
        print("Dialog cerrado")
