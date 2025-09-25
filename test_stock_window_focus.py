#!/usr/bin/env python3
"""
Test pour vérifier que la fenêtre de stock s'affiche correctement au premier plan
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from ui.stock import StockWindow
from database.models import Producto, Stock

def test_stock_window_focus():
    """Test de l'affichage correct de la fenêtre de stock"""
    
    print("=== Test de focus de la fenêtre de stock ===\n")
    
    # Créer quelques produits de test s'ils n'existent pas
    productos_test = [
        {
            'nombre': 'Producto Focus Test 1',
            'referencia': 'FOCUS001',
            'precio': 12.50,
            'categoria': 'Test Focus',
            'descripcion': 'Producto para test de focus'
        },
        {
            'nombre': 'Producto Focus Test 2', 
            'referencia': 'FOCUS002',
            'precio': 18.75,
            'categoria': 'Test Focus',
            'descripcion': 'Producto para test de focus'
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
            stock = Stock(producto.id, 25)  # 25 unidades iniciales
            stock.save()
            print(f"Stock inicial establecido: 25 unidades")
    
    # Configurar CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Crear ventana principal
    root = ctk.CTk()
    root.title("Test Stock Window Focus")
    root.geometry("600x400")
    
    # Centrar la ventana principal
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Variables para controlar las ventanas
    stock_window = None
    
    def open_stock():
        nonlocal stock_window
        print("Abriendo ventana de stock...")
        stock_window = StockWindow(root)
        print("✅ Ventana de stock creada")
        print("   - La ventana debería aparecer al frente")
        print("   - Debería estar centrada en la pantalla")
        print("   - Debería tener foco automáticamente")
    
    def test_multiple_windows():
        """Test para abrir múltiples ventanas y verificar el focus"""
        print("Probando múltiples ventanas...")
        
        # Crear ventana secundaria que podría interferir
        secondary = ctk.CTkToplevel(root)
        secondary.title("Ventana Secundaria")
        secondary.geometry("300x200")
        secondary.lift()
        secondary.focus_force()
        
        print("   - Ventana secundaria creada (debería estar al frente)")
        
        # Ahora abrir stock - debería aparecer por encima
        root.after(2000, open_stock)  # Esperar 2 segundos
        
    def close_all():
        """Cerrar todas las ventanas"""
        if stock_window and hasattr(stock_window, 'window'):
            try:
                stock_window.window.destroy()
            except:
                pass
        root.quit()
    
    # Crear interfaz de test
    title_label = ctk.CTkLabel(
        root,
        text="Test de Focus - Ventana de Stock",
        font=ctk.CTkFont(size=20, weight="bold")
    )
    title_label.pack(pady=30)
    
    info_label = ctk.CTkLabel(
        root,
        text="Este test verifica que la ventana de stock\nse muestre correctamente al primer plan",
        font=ctk.CTkFont(size=12)
    )
    info_label.pack(pady=10)
    
    # Botones de test
    buttons_frame = ctk.CTkFrame(root)
    buttons_frame.pack(pady=30)
    
    open_btn = ctk.CTkButton(
        buttons_frame,
        text="🪟 Abrir Ventana de Stock",
        command=open_stock,
        font=ctk.CTkFont(size=14, weight="bold"),
        height=40,
        width=200
    )
    open_btn.pack(pady=10)
    
    multiple_btn = ctk.CTkButton(
        buttons_frame,
        text="🔄 Test Múltiples Ventanas",
        command=test_multiple_windows,
        font=ctk.CTkFont(size=14),
        height=40,
        width=200
    )
    multiple_btn.pack(pady=10)
    
    close_btn = ctk.CTkButton(
        buttons_frame,
        text="❌ Cerrar Todo",
        command=close_all,
        font=ctk.CTkFont(size=14),
        height=40,
        width=200,
        fg_color="red",
        hover_color="darkred"
    )
    close_btn.pack(pady=10)
    
    # Instrucciones
    instructions_frame = ctk.CTkFrame(root)
    instructions_frame.pack(fill="x", padx=20, pady=20)
    
    instructions_text = """
📋 INSTRUCCIONES DE TEST:

1. Haz clic en "Abrir Ventana de Stock"
   ✅ La ventana debería aparecer al frente
   ✅ Debería estar centrada
   ✅ Debería tener foco inmediato

2. Prueba "Test Múltiples Ventanas"
   ✅ Se abre una ventana secundaria
   ✅ Después de 2 segundos, la ventana de stock debería aparecer por encima

3. En la ventana de stock, prueba:
   ✅ Los diálogos de modificación de stock
   ✅ La ventana de historial
   ✅ Los mensajes de confirmación

4. Verifica que todos los diálogos aparezcan al frente
    """
    
    instructions_label = ctk.CTkLabel(
        instructions_frame,
        text=instructions_text,
        font=ctk.CTkFont(size=10),
        justify="left"
    )
    instructions_label.pack(padx=10, pady=10)
    
    print("Interfaz de test iniciada.")
    print("Sigue las instrucciones en pantalla para probar el focus de las ventanas.")
    
    root.mainloop()

if __name__ == "__main__":
    test_stock_window_focus()
