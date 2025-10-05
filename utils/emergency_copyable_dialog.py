#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diálogo copiable de emergencia usando tkinter puro
"""

import tkinter as tk
from tkinter import ttk

def show_emergency_copyable_warning(parent, title, message):
    """Diálogo copiable de emergencia usando tkinter puro"""
    print("🚨 EMERGENCY: Usando diálogo de emergencia tkinter puro")
    
    try:
        # Crear ventana de diálogo con tkinter puro
        dialog = tk.Toplevel(parent if parent else None)
        dialog.title(title)
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        
        if parent:
            dialog.transient(parent)
            dialog.grab_set()
        
        # Centrar en pantalla
        dialog.geometry("+300+200")
        
        print("✅ EMERGENCY: Ventana tkinter creada")
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text=title,
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Mensaje en Text widget (copiable)
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        text_widget = tk.Text(
            text_frame,
            height=8,
            width=50,
            wrap="word",
            font=("Arial", 11),
            relief="sunken",
            borderwidth=2
        )
        text_widget.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Insertar mensaje
        text_widget.insert("1.0", message)
        text_widget.configure(state="disabled")  # Solo lectura pero seleccionable
        
        # Frame de botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x")
        
        result = {"clicked": None}
        
        def copy_message():
            """Copiar mensaje al portapapeles"""
            try:
                dialog.clipboard_clear()
                dialog.clipboard_append(f"{title}\n\n{message}")
                print("✅ EMERGENCY: Mensaje copiado al portapapeles")
                
                # Cambiar texto del botón temporalmente
                copy_btn.configure(text="✅ COPIADO")
                dialog.after(1500, lambda: copy_btn.configure(text="📋 COPIAR"))
                
            except Exception as e:
                print(f"❌ EMERGENCY: Error copiando: {e}")
        
        def ok_clicked():
            result["clicked"] = "ok"
            dialog.destroy()
        
        # Botón COPIAR - ESTILO LLAMATIVO
        copy_btn = tk.Button(
            buttons_frame,
            text="📋 COPIAR",
            command=copy_message,
            font=("Arial", 12, "bold"),
            bg="#FF4444",  # Rojo brillante
            fg="white",
            activebackground="#FF6666",
            activeforeground="white",
            relief="raised",
            borderwidth=3,
            padx=20,
            pady=10
        )
        copy_btn.pack(side="left", padx=(0, 10))
        
        # Botón OK
        ok_btn = tk.Button(
            buttons_frame,
            text="OK",
            command=ok_clicked,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            activebackground="#66BB6A",
            activeforeground="white",
            relief="raised",
            borderwidth=2,
            padx=20,
            pady=10
        )
        ok_btn.pack(side="right")
        
        print("✅ EMERGENCY: Botones creados - COPIAR debería ser MUY VISIBLE (rojo)")
        
        # Focus en OK
        ok_btn.focus()
        
        # Mostrar diálogo
        dialog.focus()
        dialog.lift()
        
        print("🔍 EMERGENCY: Mostrando diálogo tkinter...")
        dialog.wait_window()
        
        print("✅ EMERGENCY: Diálogo tkinter cerrado")
        return result["clicked"]
        
    except Exception as e:
        print(f"❌ EMERGENCY: Error en diálogo de emergencia: {e}")
        import traceback
        print(f"❌ EMERGENCY: Traceback: {traceback.format_exc()}")
        
        # Último recurso: messagebox estándar
        import tkinter.messagebox as messagebox
        return messagebox.showwarning(title, message, parent=parent)

if __name__ == "__main__":
    print("🧪 Test: Diálogo de Emergencia Tkinter")
    
    try:
        import tkinter as tk
        
        root = tk.Tk()
        root.title("Test Emergency")
        root.geometry("300x200")
        root.withdraw()
        
        # Test del diálogo de emergencia
        result = show_emergency_copyable_warning(
            root,
            "Emergency Test",
            "Este es un diálogo de emergencia usando tkinter puro.\n\nDebe tener un botón COPIAR rojo muy visible.\n\nEste es el último recurso si CustomTkinter falla."
        )
        
        print(f"Resultado: {result}")
        
    except Exception as e:
        print(f"Error en test: {e}")
        import traceback
        traceback.print_exc()
