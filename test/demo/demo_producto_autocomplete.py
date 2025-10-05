#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración del sistema de autocompletado de productos
Ejecutar: python test/demo/demo_producto_autocomplete.py
"""
import sys
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from common.producto_autocomplete import ProductoAutocomplete
from database.models import Producto, Stock
from database.database import db

class ProductoAutocompleteDemo:
    """Demostración del autocompletado de productos"""
    
    def __init__(self):
        # Configurar CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title("Demo: Autocompletado de Productos")
        self.root.geometry("800x700")
        
        # Variables
        self.selected_producto_info = {}
        
        self.create_sample_data()
        self.create_widgets()
    
    def create_sample_data(self):
        """Crea datos de ejemplo si no existen"""
        try:
            # Verificar si ya hay productos
            productos_existentes = Producto.get_all()
            if len(productos_existentes) >= 5:
                print(f"✅ Ya existen {len(productos_existentes)} productos en la base de datos")
                return
            
            print("🔄 Creando datos de ejemplo...")
            
            # Productos de ejemplo
            productos_ejemplo = [
                {
                    'nombre': 'Laptop Dell Inspiron 15',
                    'referencia': 'DELL001',
                    'precio': 899.99,
                    'categoria': 'Informática',
                    'descripcion': 'Laptop para oficina con procesador Intel i5',
                    'iva_recomendado': 21.0,
                    'stock': 15
                },
                {
                    'nombre': 'Mouse Logitech MX Master',
                    'referencia': 'LOG001',
                    'precio': 89.99,
                    'categoria': 'Periféricos',
                    'descripcion': 'Mouse inalámbrico de alta precisión',
                    'iva_recomendado': 21.0,
                    'stock': 25
                },
                {
                    'nombre': 'Teclado Mecánico Corsair',
                    'referencia': 'COR001',
                    'precio': 129.99,
                    'categoria': 'Periféricos',
                    'descripcion': 'Teclado mecánico RGB para gaming',
                    'iva_recomendado': 21.0,
                    'stock': 8
                },
                {
                    'nombre': 'Monitor Samsung 27"',
                    'referencia': 'SAM001',
                    'precio': 299.99,
                    'categoria': 'Monitores',
                    'descripcion': 'Monitor 4K UHD de 27 pulgadas',
                    'iva_recomendado': 21.0,
                    'stock': 12
                },
                {
                    'nombre': 'Impresora HP LaserJet',
                    'referencia': 'HP001',
                    'precio': 199.99,
                    'categoria': 'Impresoras',
                    'descripcion': 'Impresora láser monocromática',
                    'iva_recomendado': 21.0,
                    'stock': 5
                },
                {
                    'nombre': 'Webcam Logitech C920',
                    'referencia': 'LOG002',
                    'precio': 79.99,
                    'categoria': 'Periféricos',
                    'descripcion': 'Webcam HD 1080p para videoconferencias',
                    'iva_recomendado': 21.0,
                    'stock': 20
                },
                {
                    'nombre': 'Disco Duro Externo 1TB',
                    'referencia': 'WD001',
                    'precio': 59.99,
                    'categoria': 'Almacenamiento',
                    'descripcion': 'Disco duro externo USB 3.0',
                    'iva_recomendado': 21.0,
                    'stock': 30
                },
                {
                    'nombre': 'Auriculares Sony WH-1000XM4',
                    'referencia': 'SONY001',
                    'precio': 349.99,
                    'categoria': 'Audio',
                    'descripcion': 'Auriculares inalámbricos con cancelación de ruido',
                    'iva_recomendado': 21.0,
                    'stock': 0  # Sin stock para probar
                }
            ]
            
            # Crear productos y stock
            for producto_data in productos_ejemplo:
                stock_cantidad = producto_data.pop('stock')
                
                # Crear producto
                producto = Producto(**producto_data)
                producto.save()
                
                # Crear stock
                stock = Stock(
                    producto_id=producto.id,
                    cantidad_disponible=stock_cantidad
                )
                stock.save()
                
                print(f"✅ Creado: {producto.nombre} (Stock: {stock_cantidad})")
            
            print(f"🎉 Creados {len(productos_ejemplo)} productos de ejemplo")
            
        except Exception as e:
            print(f"❌ Error creando datos de ejemplo: {e}")
    
    def create_widgets(self):
        """Crea la interfaz de la demostración"""
        # Título
        title_label = ctk.CTkLabel(
            self.root,
            text="🔍 Demostración de Autocompletado de Productos",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Instrucciones
        instructions = ctk.CTkLabel(
            self.root,
            text="Escriba el nombre, referencia o categoría de un producto para ver las sugerencias",
            font=ctk.CTkFont(size=14)
        )
        instructions.pack(pady=10)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sección de autocompletado
        self.create_autocomplete_section(main_frame)
        
        # Sección de información del producto
        self.create_info_section(main_frame)
        
        # Sección de acciones
        self.create_actions_section(main_frame)
    
    def create_autocomplete_section(self, parent):
        """Crea la sección de autocompletado"""
        # Título de sección
        autocomplete_label = ctk.CTkLabel(
            parent,
            text="🔍 Buscar Producto",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        autocomplete_label.pack(pady=(10, 5))
        
        # Widget de autocompletado
        self.producto_autocomplete = ProductoAutocomplete(
            parent,
            placeholder_text="Escriba para buscar productos...",
            include_stock_info=True,
            width=600,
            height=40
        )
        self.producto_autocomplete.pack(fill="x", padx=20, pady=10)
        
        # Configurar callback
        self.producto_autocomplete.set_on_select_callback(self.on_producto_selected)
        
        # Estado del autocompletado
        self.status_label = ctk.CTkLabel(
            parent,
            text="💡 Escriba al menos 2 caracteres para ver sugerencias",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
    
    def create_info_section(self, parent):
        """Crea la sección de información del producto"""
        # Título de sección
        info_label = ctk.CTkLabel(
            parent,
            text="📦 Información del Producto Seleccionado",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        info_label.pack(pady=(20, 5))
        
        # Frame de información
        self.info_frame = ctk.CTkFrame(parent)
        self.info_frame.pack(fill="x", padx=20, pady=10)
        
        # Texto de información
        self.info_text = ctk.CTkTextbox(
            self.info_frame,
            height=200,
            wrap="word"
        )
        self.info_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información inicial
        self.update_info_display("Seleccione un producto para ver su información detallada")
    
    def create_actions_section(self, parent):
        """Crea la sección de acciones"""
        # Frame de botones
        buttons_frame = ctk.CTkFrame(parent)
        buttons_frame.pack(fill="x", padx=20, pady=10)
        
        # Botón para refrescar datos
        refresh_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 Refrescar Datos",
            command=self.refresh_data,
            fg_color="#2E8B57",
            hover_color="#228B22"
        )
        refresh_btn.pack(side="left", padx=5, pady=10)
        
        # Botón para limpiar selección
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar",
            command=self.clear_selection
        )
        clear_btn.pack(side="left", padx=5, pady=10)
        
        # Botón para validar selección
        validate_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Validar Selección",
            command=self.validate_selection,
            fg_color="#1E90FF",
            hover_color="#4169E1"
        )
        validate_btn.pack(side="left", padx=5, pady=10)
        
        # Botón para mostrar estadísticas
        stats_btn = ctk.CTkButton(
            buttons_frame,
            text="📊 Estadísticas",
            command=self.show_statistics
        )
        stats_btn.pack(side="left", padx=5, pady=10)
        
        # Botón para salir
        exit_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ Salir",
            command=self.root.quit,
            fg_color="#DC143C",
            hover_color="#B22222"
        )
        exit_btn.pack(side="right", padx=5, pady=10)
    
    def on_producto_selected(self, producto_data):
        """Callback cuando se selecciona un producto"""
        try:
            self.selected_producto_info = producto_data
            
            # Actualizar información
            info_text = f"""
🏷️ INFORMACIÓN DEL PRODUCTO

📦 Nombre: {producto_data['nombre']}
🔖 Referencia: {producto_data['referencia']}
💰 Precio: €{producto_data['precio']:.2f}
📂 Categoría: {producto_data['categoria']}
📝 Descripción: {producto_data['descripcion']}
🧾 IVA Recomendado: {producto_data['iva_recomendado']}%

📊 INFORMACIÓN DE STOCK
{producto_data['stock_info']}

🆔 ID del Producto: {producto_data['id']}
            """.strip()
            
            self.update_info_display(info_text)
            self.status_label.configure(text=f"✅ Producto seleccionado: {producto_data['nombre']}")
            
            print(f"🎯 Producto seleccionado: {producto_data['nombre']} - {producto_data['referencia']}")
            
        except Exception as e:
            print(f"❌ Error al seleccionar producto: {e}")
            self.status_label.configure(text="❌ Error al seleccionar producto")
    
    def update_info_display(self, text):
        """Actualiza el display de información"""
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert("1.0", text)
    
    def refresh_data(self):
        """Refresca los datos de productos"""
        try:
            self.producto_autocomplete.refresh_data()
            self.status_label.configure(text="🔄 Datos actualizados correctamente")
            print("🔄 Datos de productos refrescados")
        except Exception as e:
            print(f"❌ Error refrescando datos: {e}")
            self.status_label.configure(text="❌ Error refrescando datos")
    
    def clear_selection(self):
        """Limpia la selección actual"""
        try:
            self.producto_autocomplete.clear()
            self.selected_producto_info = {}
            self.update_info_display("Seleccione un producto para ver su información detallada")
            self.status_label.configure(text="🗑️ Selección limpiada")
            print("🗑️ Selección limpiada")
        except Exception as e:
            print(f"❌ Error limpiando selección: {e}")
    
    def validate_selection(self):
        """Valida la selección actual"""
        try:
            is_valid = self.producto_autocomplete.validate_selection()
            
            if is_valid:
                producto = self.producto_autocomplete.get_selected_producto()
                messagebox.showinfo(
                    "Validación",
                    f"✅ Selección válida!\n\nProducto: {producto.nombre}\nReferencia: {producto.referencia}",
                    parent=self.root
                )
                self.status_label.configure(text="✅ Selección válida")
            else:
                error_msg = self.producto_autocomplete.get_validation_error()
                messagebox.showwarning(
                    "Validación",
                    f"❌ Selección inválida!\n\n{error_msg}",
                    parent=self.root
                )
                self.status_label.configure(text=f"❌ {error_msg}")
                
        except Exception as e:
            print(f"❌ Error validando selección: {e}")
            messagebox.showerror("Error", f"Error validando selección: {e}", parent=self.root)
    
    def show_statistics(self):
        """Muestra estadísticas del autocompletado"""
        try:
            total_productos = len(self.producto_autocomplete.suggestions_data)
            
            # Contar por categorías
            categorias = {}
            for item in self.producto_autocomplete.suggestions_data:
                cat = item['categoria'] or 'Sin categoría'
                categorias[cat] = categorias.get(cat, 0) + 1
            
            # Crear mensaje de estadísticas
            stats_text = f"📊 ESTADÍSTICAS\n\n"
            stats_text += f"Total de productos: {total_productos}\n\n"
            stats_text += "Por categorías:\n"
            
            for categoria, count in sorted(categorias.items()):
                stats_text += f"• {categoria}: {count} productos\n"
            
            messagebox.showinfo("Estadísticas", stats_text, parent=self.root)
            
        except Exception as e:
            print(f"❌ Error mostrando estadísticas: {e}")
            messagebox.showerror("Error", f"Error mostrando estadísticas: {e}", parent=self.root)
    
    def run(self):
        """Ejecuta la demostración"""
        print("🚀 Iniciando demostración de autocompletado de productos...")
        print("💡 Instrucciones:")
        print("   - Escriba en el campo de búsqueda para ver sugerencias")
        print("   - Use las flechas ↑↓ para navegar en las sugerencias")
        print("   - Presione Enter o haga clic para seleccionar")
        print("   - Pruebe buscar por nombre, referencia o categoría")
        print("   - Los productos sin stock aparecen marcados")
        
        self.root.mainloop()

def main():
    """Función principal"""
    demo = ProductoAutocompleteDemo()
    demo.run()

if __name__ == "__main__":
    main()
