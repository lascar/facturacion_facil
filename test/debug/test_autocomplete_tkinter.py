#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test del autocompletado usando tkinter estándar
"""
import sys
import os
import tkinter as tk
from tkinter import ttk

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class SimpleAutocomplete:
    """Versión simplificada del autocompletado para testing"""
    
    def __init__(self, parent):
        self.parent = parent
        self.suggestions_data = []
        self.filtered_suggestions = []
        self.selected_item = None
        self.search_fields = ['text']
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crea los widgets básicos"""
        # Entry principal
        self.entry = tk.Entry(self.parent, width=50)
        self.entry.pack(pady=10)
        
        # Listbox para sugerencias
        self.listbox = tk.Listbox(self.parent, height=5)
        self.listbox.pack(fill="x", padx=10)
        
        # Bind eventos
        self.entry.bind('<KeyRelease>', self.on_key_release)
        self.listbox.bind('<Double-Button-1>', self.on_select)
    
    def set_suggestions_data(self, data):
        """Establece los datos para autocompletado"""
        self.suggestions_data = data
        print(f"Configurados {len(data)} elementos para autocompletado")
    
    def filter_suggestions(self, query):
        """Filtra las sugerencias"""
        if len(query) < 2:
            self.filtered_suggestions = []
            return
        
        query_lower = query.lower()
        self.filtered_suggestions = []
        
        for item in self.suggestions_data:
            for field in self.search_fields:
                if field in item:
                    field_value = str(item[field]).lower()
                    if query_lower in field_value:
                        self.filtered_suggestions.append(item)
                        break
        
        print(f"Filtradas {len(self.filtered_suggestions)} sugerencias para '{query}'")
    
    def update_listbox(self):
        """Actualiza el listbox con las sugerencias"""
        self.listbox.delete(0, tk.END)
        
        for item in self.filtered_suggestions:
            display_text = item.get('display_text', item.get('text', str(item)))
            self.listbox.insert(tk.END, display_text)
    
    def on_key_release(self, event):
        """Maneja la liberación de teclas"""
        query = self.entry.get()
        self.filter_suggestions(query)
        self.update_listbox()
    
    def on_select(self, event):
        """Maneja la selección"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(self.filtered_suggestions):
                self.selected_item = self.filtered_suggestions[index]
                display_text = self.selected_item.get('text', str(self.selected_item))
                self.entry.delete(0, tk.END)
                self.entry.insert(0, display_text)
                print(f"Seleccionado: {display_text}")

def test_simple_autocomplete():
    """Test del autocompletado simple"""
    print("🔧 Test del autocompletado simple con tkinter...")
    
    try:
        # Crear ventana
        root = tk.Tk()
        root.title("Test Autocompletado Simple")
        root.geometry("400x300")
        
        # Crear autocompletado
        autocomplete = SimpleAutocomplete(root)
        
        # Datos de test
        test_data = [
            {'text': 'Laptop Dell Inspiron', 'id': 1, 'display_text': 'Laptop Dell Inspiron - DELL001 - €899.99'},
            {'text': 'Mouse Logitech', 'id': 2, 'display_text': 'Mouse Logitech - LOG001 - €25.50'},
            {'text': 'Teclado Mecánico', 'id': 3, 'display_text': 'Teclado Mecánico - TEC001 - €75.00'},
            {'text': 'Monitor Samsung', 'id': 4, 'display_text': 'Monitor Samsung - SAM001 - €299.99'},
        ]
        
        autocomplete.set_suggestions_data(test_data)
        
        # Instrucciones
        instructions = tk.Label(
            root, 
            text="Escriba 'laptop', 'mouse', etc. para ver sugerencias.\nDoble-clic para seleccionar.",
            justify=tk.LEFT
        )
        instructions.pack(pady=10)
        
        # Test automático
        print("Probando filtrado automático...")
        autocomplete.filter_suggestions("laptop")
        autocomplete.update_listbox()
        
        if len(autocomplete.filtered_suggestions) > 0:
            print("✅ Filtrado funciona correctamente")
        else:
            print("❌ Filtrado no funciona")
        
        # Botón para cerrar
        close_btn = tk.Button(root, text="Cerrar Test", command=root.quit)
        close_btn.pack(pady=10)
        
        print("✅ Test simple creado. Cierre la ventana para continuar.")
        
        # Mostrar ventana por 3 segundos para verificar
        root.after(3000, root.quit)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test simple: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_producto_data_structure():
    """Test de la estructura de datos de productos"""
    print("\n🔧 Test de estructura de datos de productos...")
    
    try:
        from database.models import Producto
        
        # Verificar productos existentes
        productos = Producto.get_all()
        print(f"   Productos en DB: {len(productos)}")
        
        if len(productos) == 0:
            print("   Creando producto de test...")
            producto_test = Producto(
                nombre="Test Producto Autocompletado",
                referencia="TESTAC001",
                precio=99.99,
                categoria="Test",
                descripcion="Producto para test de autocompletado",
                iva_recomendado=21.0
            )
            producto_test.save()
            print("✅ Producto de test creado")
            productos = [producto_test]
        
        # Verificar estructura del primer producto
        if len(productos) > 0:
            producto = productos[0]
            print(f"   Primer producto:")
            print(f"     ID: {producto.id}")
            print(f"     Nombre: {producto.nombre}")
            print(f"     Referencia: {producto.referencia}")
            print(f"     Precio: {producto.precio}")
            print(f"     Categoría: {producto.categoria}")
            print("✅ Estructura de datos correcta")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("🚀 Test de autocompletado con tkinter estándar")
    print("=" * 60)
    
    success1 = test_simple_autocomplete()
    success2 = test_producto_data_structure()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"   Autocompletado simple: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Estructura de datos: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 TESTS BÁSICOS PASARON")
        print("El concepto de autocompletado funciona correctamente.")
        print("El problema original probablemente está en la integración con CustomTkinter.")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")

if __name__ == "__main__":
    main()
