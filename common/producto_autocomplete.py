#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'autocompletion pour les produits - Version PyQt6
"""

class ProductoAutocomplete:
    """Classe pour l'autocompletion des produits"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.productos = []
        print("ProductoAutocomplete inicializado")
    
    def set_productos(self, productos):
        """Etablit la liste des produits pour l'autocompletion"""
        self.productos = productos
        print(f"Productos configurados: {len(productos)}")
    
    def get_suggestions(self, query):
        """Obtient les suggestions d'autocompletion"""
        if not query:
            return []
        
        suggestions = []
        query_lower = query.lower()
        
        for producto in self.productos:
            if query_lower in producto.get('nombre', '').lower():
                suggestions.append(producto)
        
        return suggestions[:10]  # Limiter à 10 suggestions
    
    def clear_suggestions(self):
        """Efface les suggestions"""
        print("Suggestions effacées")
    
    def enable_autocomplete(self, widget):
        """Active l'autocompletion sur un widget"""
        print(f"Autocompletion activée sur {widget}")
        return True
    
    def disable_autocomplete(self, widget):
        """Désactive l'autocompletion sur un widget"""
        print(f"Autocompletion désactivée sur {widget}")
        return True
