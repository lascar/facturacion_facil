#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración del sistema de ordenación de TreeView
Ejecutar: python test/demo/demo_treeview_sorting.py
"""
import sys
import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime, timedelta
import random

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.treeview_sorter import add_sorting_to_treeview

class TreeViewSortingDemo:
    """Demostración del sistema de ordenación de TreeView"""
    
    def __init__(self):
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title("Demo: Sistema de Ordenación TreeView")
        self.root.geometry("1000x700")
        
        self.create_widgets()
        self.populate_sample_data()
    
    def create_widgets(self):
        """Crea la interfaz de la demostración"""
        # Título
        title_label = ctk.CTkLabel(
            self.root,
            text="🔄 Demostración de Ordenación por Columnas",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Instrucciones
        instructions = ctk.CTkLabel(
            self.root,
            text="Haz clic en cualquier encabezado de columna para ordenar. Segundo clic invierte el orden.",
            font=ctk.CTkFont(size=14)
        )
        instructions.pack(pady=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # TreeView de productos
        self.create_productos_section(main_frame)
        
        # TreeView de facturas
        self.create_facturas_section(main_frame)
        
        # Botones de acción
        self.create_action_buttons(main_frame)
    
    def create_productos_section(self, parent):
        """Crea la sección de productos"""
        # Título de sección
        productos_label = ctk.CTkLabel(
            parent,
            text="📦 Productos (con ordenación)",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        productos_label.pack(pady=(10, 5))
        
        # Frame para TreeView
        productos_frame = tk.Frame(parent)
        productos_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # TreeView de productos
        columns = ('nombre', 'referencia', 'precio', 'categoria', 'stock')
        self.productos_tree = ttk.Treeview(productos_frame, columns=columns, show='headings', height=8)
        
        # Configurar encabezados
        self.productos_tree.heading('nombre', text='Nombre del Producto')
        self.productos_tree.heading('referencia', text='Referencia')
        self.productos_tree.heading('precio', text='Precio')
        self.productos_tree.heading('categoria', text='Categoría')
        self.productos_tree.heading('stock', text='Stock')
        
        # Configurar anchos
        self.productos_tree.column('nombre', width=200, minwidth=150)
        self.productos_tree.column('referencia', width=120, minwidth=100)
        self.productos_tree.column('precio', width=100, minwidth=80)
        self.productos_tree.column('categoria', width=150, minwidth=120)
        self.productos_tree.column('stock', width=80, minwidth=60)
        
        # Scrollbar
        productos_scrollbar = ttk.Scrollbar(productos_frame, orient="vertical", command=self.productos_tree.yview)
        self.productos_tree.configure(yscrollcommand=productos_scrollbar.set)
        
        self.productos_tree.pack(side="left", fill="both", expand=True)
        productos_scrollbar.pack(side="right", fill="y")
        
        # Añadir ordenación
        self.productos_sorter = add_sorting_to_treeview(self.productos_tree)
    
    def create_facturas_section(self, parent):
        """Crea la sección de facturas"""
        # Título de sección
        facturas_label = ctk.CTkLabel(
            parent,
            text="📄 Facturas (con ordenación)",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        facturas_label.pack(pady=(20, 5))
        
        # Frame para TreeView
        facturas_frame = tk.Frame(parent)
        facturas_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # TreeView de facturas
        columns = ('numero', 'fecha', 'cliente', 'total', 'estado')
        self.facturas_tree = ttk.Treeview(facturas_frame, columns=columns, show='headings', height=8)
        
        # Configurar encabezados
        self.facturas_tree.heading('numero', text='Número')
        self.facturas_tree.heading('fecha', text='Fecha')
        self.facturas_tree.heading('cliente', text='Cliente')
        self.facturas_tree.heading('total', text='Total')
        self.facturas_tree.heading('estado', text='Estado')
        
        # Configurar anchos
        self.facturas_tree.column('numero', width=100, minwidth=80)
        self.facturas_tree.column('fecha', width=120, minwidth=100)
        self.facturas_tree.column('cliente', width=200, minwidth=150)
        self.facturas_tree.column('total', width=100, minwidth=80)
        self.facturas_tree.column('estado', width=100, minwidth=80)
        
        # Scrollbar
        facturas_scrollbar = ttk.Scrollbar(facturas_frame, orient="vertical", command=self.facturas_tree.yview)
        self.facturas_tree.configure(yscrollcommand=facturas_scrollbar.set)
        
        self.facturas_tree.pack(side="left", fill="both", expand=True)
        facturas_scrollbar.pack(side="right", fill="y")
        
        # Añadir ordenación
        self.facturas_sorter = add_sorting_to_treeview(self.facturas_tree)
    
    def create_action_buttons(self, parent):
        """Crea los botones de acción"""
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón para regenerar datos
        regenerar_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Regenerar Datos",
            command=self.populate_sample_data,
            fg_color="#2E8B57",
            hover_color="#228B22"
        )
        regenerar_btn.pack(side="left", padx=5)
        
        # Botón para resetear ordenación
        reset_btn = ctk.CTkButton(
            buttons_frame,
            text="↺ Resetear Ordenación",
            command=self.reset_sorting
        )
        reset_btn.pack(side="left", padx=5)
        
        # Botón para salir
        salir_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Salir",
            command=self.root.quit,
            fg_color="#DC143C",
            hover_color="#B22222"
        )
        salir_btn.pack(side="right", padx=5)
    
    def populate_sample_data(self):
        """Llena los TreeView con datos de ejemplo"""
        self.populate_productos_data()
        self.populate_facturas_data()
    
    def populate_productos_data(self):
        """Llena el TreeView de productos con datos de ejemplo"""
        # Limpiar datos existentes
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        # Datos de ejemplo
        productos_sample = [
            "Laptop Dell Inspiron", "Mouse Logitech", "Teclado Mecánico", "Monitor Samsung",
            "Impresora HP", "Tablet iPad", "Smartphone Samsung", "Auriculares Sony",
            "Webcam Logitech", "Disco Duro Externo", "Memoria USB", "Router WiFi",
            "Altavoces Bluetooth", "Cargador Universal", "Cable HDMI"
        ]
        
        categorias = ["Informática", "Periféricos", "Audio", "Almacenamiento", "Conectividad"]
        
        for i, producto in enumerate(productos_sample):
            precio = round(random.uniform(15.99, 899.99), 2)
            stock = random.randint(0, 50)
            categoria = random.choice(categorias)
            referencia = f"REF{i+1:03d}"
            
            self.productos_tree.insert('', 'end', values=(
                producto,
                referencia,
                f"€{precio:.2f}",
                categoria,
                str(stock)
            ))
    
    def populate_facturas_data(self):
        """Llena el TreeView de facturas con datos de ejemplo"""
        # Limpiar datos existentes
        for item in self.facturas_tree.get_children():
            self.facturas_tree.delete(item)
        
        # Datos de ejemplo
        clientes = [
            "Juan Pérez", "María García", "Carlos López", "Ana Martínez",
            "Luis Rodríguez", "Carmen Sánchez", "José González", "Isabel Fernández",
            "Miguel Torres", "Laura Ruiz", "Antonio Moreno", "Pilar Jiménez"
        ]
        
        estados = ["Pagada", "Pendiente", "Vencida", "Cancelada"]
        
        for i in range(15):
            numero = f"FACT{i+1:04d}"
            fecha_base = datetime.now() - timedelta(days=random.randint(1, 90))
            fecha = fecha_base.strftime("%Y-%m-%d")
            cliente = random.choice(clientes)
            total = round(random.uniform(25.50, 1500.00), 2)
            estado = random.choice(estados)
            
            self.facturas_tree.insert('', 'end', values=(
                numero,
                fecha,
                cliente,
                f"€{total:.2f}",
                estado
            ))
    
    def reset_sorting(self):
        """Resetea la ordenación de ambos TreeView"""
        self.productos_sorter.reset_sorting()
        self.facturas_sorter.reset_sorting()
        print("🔄 Ordenación reseteada en ambas tablas")
    
    def run(self):
        """Ejecuta la demostración"""
        print("🚀 Iniciando demostración de ordenación TreeView...")
        print("💡 Instrucciones:")
        print("   - Haz clic en cualquier encabezado de columna para ordenar")
        print("   - Segundo clic en la misma columna invierte el orden")
        print("   - Los indicadores muestran: ↕ (ordenable), ↑ (ascendente), ↓ (descendente)")
        print("   - Usa los botones para regenerar datos o resetear ordenación")
        
        self.root.mainloop()

def main():
    """Función principal"""
    demo = TreeViewSortingDemo()
    demo.run()

if __name__ == "__main__":
    main()
