#!/usr/bin/env python3
"""
Test simple pour l'interface de gestion des stocks
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from ui.stock import StockWindow
from database.models import Producto, Stock

def test_stock_interface():
    """Test de l'interface de stock"""
    
    # Créer quelques produits de test s'ils n'existent pas
    productos_test = [
        {
            'nombre': 'Producto Test 1',
            'referencia': 'TEST001',
            'precio': 10.50,
            'categoria': 'Test',
            'descripcion': 'Producto de prueba 1'
        },
        {
            'nombre': 'Producto Test 2', 
            'referencia': 'TEST002',
            'precio': 25.00,
            'categoria': 'Test',
            'descripcion': 'Producto de prueba 2'
        },
        {
            'nombre': 'Producto Test 3',
            'referencia': 'TEST003', 
            'precio': 5.75,
            'categoria': 'Test',
            'descripcion': 'Producto de prueba 3'
        }
    ]
    
    print("Creando productos de test...")
    for prod_data in productos_test:
        # Verificar si ya existe
        productos_existentes = Producto.get_all()
        existe = any(p.referencia == prod_data['referencia'] for p in productos_existentes)
        
        if not existe:
            producto = Producto(**prod_data)
            producto.save()
            print(f"Producto creado: {prod_data['nombre']}")
            
            # Establecer stock inicial
            stock = Stock(producto.id, 15)  # 15 unidades iniciales
            stock.save()
            print(f"Stock inicial establecido: 15 unidades")
    
    # Configurar CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Crear ventana principal
    root = ctk.CTk()
    root.title("Test Stock Interface")
    root.geometry("400x300")
    
    # Botón para abrir stock
    def open_stock():
        stock_window = StockWindow(root)
    
    open_btn = ctk.CTkButton(
        root,
        text="Abrir Gestión de Stock",
        command=open_stock,
        font=ctk.CTkFont(size=16, weight="bold"),
        height=50
    )
    open_btn.pack(expand=True)
    
    info_label = ctk.CTkLabel(
        root,
        text="Haz clic en el botón para abrir\nla interfaz de gestión de stock",
        font=ctk.CTkFont(size=12)
    )
    info_label.pack(pady=20)
    
    print("Interfaz de test iniciada. Haz clic en 'Abrir Gestión de Stock'")
    root.mainloop()

if __name__ == "__main__":
    test_stock_interface()
