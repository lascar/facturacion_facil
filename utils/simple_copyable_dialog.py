#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Diálogo copiable simple alternativo
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

def show_simple_copyable_warning(parent, title, message):
    """Versión simple alternativa de diálogo copiable"""
    print("🔍 DEBUG: show_simple_copyable_warning iniciado")
    
    try:
        # Crear ventana de diálogo simple
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        if parent:
            dialog.transient(parent)
            dialog.grab_set()
        
        print("✅ DEBUG: Ventana de diálogo simple creada")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Mensaje
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=12),
            wraplength=350,
            justify="left"
        )
        message_label.pack(pady=(0, 20))
        
        # Frame de botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        result = {"clicked": None}
        
        def copy_message():
            """Copiar mensaje al portapapeles"""
            try:
                dialog.clipboard_clear()
                dialog.clipboard_append(f"{title}\n\n{message}")
                print("✅ DEBUG: Mensaje copiado al portapapeles")
                
                # Cambiar texto del botón temporalmente
                copy_btn.configure(text="✅ COPIADO")
                dialog.after(1500, lambda: copy_btn.configure(text="📋 COPIAR"))
                
            except Exception as e:
                print(f"❌ DEBUG: Error copiando: {e}")
        
        def ok_clicked():
            result["clicked"] = "ok"
            dialog.destroy()
        
        # Botón COPIAR - MUY VISIBLE
        copy_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 COPIAR",
            command=copy_message,
            width=120,
            height=40,
            fg_color="#FF4444",  # Rojo brillante
            hover_color="#FF6666",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        copy_btn.pack(side="left", padx=10, pady=10)
        
        # Botón OK
        ok_btn = ctk.CTkButton(
            buttons_frame,
            text="OK",
            command=ok_clicked,
            width=80,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        ok_btn.pack(side="right", padx=10, pady=10)
        
        print("✅ DEBUG: Botones creados - COPIAR debería ser MUY VISIBLE (rojo)")
        
        # Centrar en parent
        if parent:
            dialog.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        # Mostrar diálogo
        dialog.focus()
        dialog.wait_window()
        
        print("✅ DEBUG: Diálogo simple cerrado")
        return result["clicked"]
        
    except Exception as e:
        print(f"❌ DEBUG: Error en diálogo simple: {e}")
        import traceback
        print(f"❌ DEBUG: Traceback: {traceback.format_exc()}")
        
        # Fallback a messagebox estándar
        return messagebox.showwarning(title, message, parent=parent)

if __name__ == "__main__":
    print("🧪 Test: Diálogo Copiable Simple")
    
    try:
        import customtkinter as ctk
        
        root = ctk.CTk()
        root.title("Test")
        root.geometry("300x200")
        root.withdraw()
        
        # Test del diálogo simple
        result = show_simple_copyable_warning(
            root,
            "Test Warning",
            "Este es un mensaje de prueba.\n\nDebe tener un botón COPIAR muy visible (rojo)."
        )
        
        print(f"Resultado: {result}")
        
    except Exception as e:
        print(f"Error en test: {e}")
        import traceback
        traceback.print_exc()
