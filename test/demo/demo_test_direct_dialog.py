#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test del diálogo directo con botones CONFIRMAR/CANCELAR
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk

def create_direct_stock_dialog(parent, title, message):
    """Crea el diálogo directo con botones CONFIRMAR/CANCELAR"""
    try:
        # Crear diálogo personalizado directamente
        dialog = ctk.CTkToplevel(parent)
        dialog.title(title)
        dialog.geometry("600x400")
        dialog.transient(parent)
        dialog.grab_set()
        
        # Variable para el resultado
        result = None
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título con icono
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.pack(fill="x", pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"📦 {title}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Área de texto
        text_widget = ctk.CTkTextbox(
            main_frame,
            height=200,
            font=ctk.CTkFont(size=11, family="Consolas")
        )
        text_widget.pack(fill="both", expand=True, pady=(0, 15))
        text_widget.insert("1.0", message)
        text_widget.configure(state="disabled")
        
        # Frame de botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x")
        
        def confirmar_clicked():
            nonlocal result
            result = True
            dialog.destroy()
        
        def cancelar_clicked():
            nonlocal result
            result = False
            dialog.destroy()
        
        def copiar_clicked():
            try:
                dialog.clipboard_clear()
                dialog.clipboard_append(message)
                dialog.update()
                print("📋 Mensaje copiado al portapapeles")
            except Exception as e:
                print(f"Error copiando: {e}")
        
        # Botón Copiar (izquierda)
        copiar_btn = ctk.CTkButton(
            buttons_frame,
            text="📋 Copiar",
            command=copiar_clicked,
            width=100,
            height=35,
            fg_color="gray",
            hover_color="darkgray"
        )
        copiar_btn.pack(side="left", padx=15, pady=15)
        
        # Botón CANCELAR (derecha)
        cancelar_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ CANCELAR",
            command=cancelar_clicked,
            width=140,
            height=40,
            fg_color="#DC143C",
            hover_color="#B22222",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        cancelar_btn.pack(side="right", padx=(5, 15), pady=15)
        
        # Botón CONFIRMAR (derecha)
        confirmar_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ CONFIRMAR",
            command=confirmar_clicked,
            width=140,
            height=40,
            fg_color="#2E8B57",
            hover_color="#228B22",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        confirmar_btn.pack(side="right", padx=5, pady=15)
        
        # Focus en CONFIRMAR
        confirmar_btn.focus()
        
        # Bind teclas
        dialog.bind("<Return>", lambda e: confirmar_clicked())
        dialog.bind("<Escape>", lambda e: cancelar_clicked())
        
        # Centrar el diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"600x400+{x}+{y}")
        
        # Esperar resultado
        dialog.wait_window()
        
        return result
        
    except Exception as e:
        print(f"Error creando diálogo directo: {e}")
        return None

def test_direct_dialog():
    """Test del diálogo directo"""
    
    print("🧪 TEST - Diálogo Directo con Botones CONFIRMAR/CANCELAR")
    print("=" * 70)
    
    try:
        # Crear aplicación de test
        app = ctk.CTk()
        app.title("Test Diálogo Directo")
        app.geometry("500x300")
        
        # Mensaje de test
        test_message = """📦 IMPACTO EN STOCK:

• nuevo prod 270925 1:
  Stock actual: 2 → Después: 1 unidades
  Estado: 🟠 STOCK BAJO (1)


==================================================
🔄 ACCIÓN A REALIZAR:
• Se guardará la factura
• Se actualizará automáticamente el stock
• Se registrarán los movimientos de stock

¿Desea continuar y procesar la factura?"""
        
        # Label de información
        info_label = ctk.CTkLabel(
            app,
            text="TEST DEL DIÁLOGO DIRECTO\n\n"
                 "Este diálogo debe mostrar:\n"
                 "✅ CONFIRMAR (verde)\n"
                 "❌ CANCELAR (rojo)\n"
                 "📋 Copiar (gris)\n\n"
                 "Haz clic para probar:",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        info_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Variable para resultado
        dialog_result = None
        
        def show_dialog():
            nonlocal dialog_result
            print("\n🔄 Mostrando diálogo directo...")
            
            result = create_direct_stock_dialog(
                app,
                "Confirmar Procesamiento de Factura",
                test_message
            )
            
            dialog_result = result
            print(f"📊 Resultado: {result}")
            
            if result is True:
                print("✅ Usuario hizo clic en CONFIRMAR")
                result_label.configure(
                    text="✅ CONFIRMADO\nLa factura se procesaría",
                    text_color="green"
                )
            elif result is False:
                print("❌ Usuario hizo clic en CANCELAR")
                result_label.configure(
                    text="❌ CANCELADO\nLa operación fue cancelada",
                    text_color="red"
                )
            else:
                print("⚠️ Diálogo cerrado sin selección")
                result_label.configure(
                    text="⚠️ Sin selección",
                    text_color="orange"
                )
        
        # Botón de test
        test_btn = ctk.CTkButton(
            app,
            text="🔍 Mostrar Diálogo Directo",
            command=show_dialog,
            fg_color="#2E8B57",
            hover_color="#228B22",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        test_btn.pack(pady=15)
        
        # Label de resultado
        result_label = ctk.CTkLabel(
            app,
            text="Resultado aparecerá aquí",
            font=ctk.CTkFont(size=12)
        )
        result_label.pack(pady=10)
        
        print("\n🚀 Aplicación iniciada")
        print("💡 Haz clic en el botón para ver el diálogo con botones CONFIRMAR/CANCELAR")
        
        # Ejecutar aplicación
        app.mainloop()
        
        return dialog_result
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🚀 INICIANDO TEST DE DIÁLOGO DIRECTO")
    print("=" * 70)
    
    result = test_direct_dialog()
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN:")
    
    if result is True:
        print("   ✅ CONFIRMADO - El diálogo funciona correctamente")
    elif result is False:
        print("   ❌ CANCELADO - El diálogo funciona correctamente")
    else:
        print("   ⚠️ SIN RESULTADO - Verificar implementación")
    
    print("\n🎯 CARACTERÍSTICAS DEL DIÁLOGO:")
    print("   • Botón '✅ CONFIRMAR' en verde")
    print("   • Botón '❌ CANCELAR' en rojo")
    print("   • Botón '📋 Copiar' en gris")
    print("   • Texto seleccionable")
    print("   • Atajos: Enter=Confirmar, Escape=Cancelar")
    
    print("\n📋 PARA USAR EN LA APLICACIÓN:")
    print("   1. Reiniciar la aplicación")
    print("   2. Crear factura con producto de stock bajo")
    print("   3. Hacer clic en 'Guardar'")
    print("   4. Debe aparecer el diálogo con botones CONFIRMAR/CANCELAR")
    print("   5. Hacer clic en '✅ CONFIRMAR' para procesar la factura")
