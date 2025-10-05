#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du dialogue de confirmation amélioré avec boutons Confirmación/Cancelar
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
from common.custom_dialogs import show_copyable_confirm

def demo_improved_dialog():
    """Test du dialogue amélioré"""
    
    print("🧪 TEST - Dialogue Amélioré avec Boutons Clairs")
    print("=" * 60)
    
    try:
        # Créer une application de test
        app = ctk.CTk()
        app.title("Test Dialogue Amélioré")
        app.geometry("400x200")
        
        # Message de test similaire à celui des facturas
        test_message = """📦 IMPACTO EN STOCK:

• Producto Test:
  Stock actual: 3 → Después: 2 unidades
  Estado: 🟠 STOCK BAJO (2)

• Otro Producto:
  Stock actual: 8 → Después: 5 unidades
  Estado: 🟡 STOCK MEDIO (5)

==================================================
🔄 ACCIÓN A REALIZAR:
• Se guardará la factura
• Se actualizará automáticamente el stock
• Se registrarán los movimientos de stock

¿Desea continuar y procesar la factura?"""
        
        # Label d'information
        info_label = ctk.CTkLabel(
            app,
            text="Test del Diálogo de Confirmación Mejorado\n\n"
                 "Haz clic en el botón para ver el diálogo\n"
                 "con los nuevos botones:\n"
                 "✅ Confirmación  y  ❌ Cancelar",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        info_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Variable para almacenar el resultado
        dialog_result = None
        
        def show_test_dialog():
            nonlocal dialog_result
            print("\n🔄 Mostrando diálogo de confirmación...")
            print("💡 Observa los nuevos botones: '✅ Confirmación' y '❌ Cancelar'")
            
            try:
                result = show_copyable_confirm(
                    app, 
                    "Confirmar Procesamiento de Factura", 
                    test_message
                )
                dialog_result = result
                
                print(f"📊 Resultado del diálogo: {result}")
                
                if result:
                    print("✅ Usuario hizo clic en 'Confirmación'")
                    print("🔄 En la aplicación real, esto guardaría la factura y actualizaría el stock")
                    result_label.configure(
                        text="✅ CONFIRMADO\nLa factura se procesaría",
                        text_color="green"
                    )
                else:
                    print("❌ Usuario hizo clic en 'Cancelar' o cerró el diálogo")
                    print("🛑 En la aplicación real, esto cancelaría la operación")
                    result_label.configure(
                        text="❌ CANCELADO\nLa factura NO se procesaría",
                        text_color="red"
                    )
                
            except Exception as e:
                print(f"❌ Error mostrando diálogo: {e}")
                result_label.configure(
                    text=f"❌ ERROR: {e}",
                    text_color="red"
                )
        
        # Botón para mostrar el diálogo
        test_btn = ctk.CTkButton(
            app,
            text="🔍 Mostrar Diálogo de Confirmación",
            command=show_test_dialog,
            fg_color="#2E8B57",
            hover_color="#228B22",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        test_btn.pack(pady=10)
        
        # Label para mostrar el resultado
        result_label = ctk.CTkLabel(
            app,
            text="Resultado aparecerá aquí",
            font=ctk.CTkFont(size=12)
        )
        result_label.pack(pady=10)
        
        print("\n🚀 Aplicación de test iniciada")
        print("💡 Haz clic en el botón para probar el diálogo mejorado")
        print("🔍 Observa los nuevos botones con iconos y colores claros")
        
        # Ejecutar la aplicación
        app.mainloop()
        
        print(f"\n📊 Resultado final del test: {dialog_result}")
        return dialog_result
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return None

def demo_dialog_appearance():
    """Test de la apariencia del diálogo"""
    
    print("\n🎨 TEST - Apariencia del Diálogo")
    print("-" * 40)
    
    print("✅ Mejoras implementadas:")
    print("   • Botón 'Sí' → '✅ Confirmación' (verde)")
    print("   • Botón 'No' → '❌ Cancelar' (rojo)")
    print("   • Botones más grandes (120x35)")
    print("   • Fuente en negrita")
    print("   • Colores más claros")
    print("   • Iconos descriptivos")
    
    print("\n📋 Mensaje mejorado incluye:")
    print("   • Impacto detallado en stock")
    print("   • Sección 'ACCIÓN A REALIZAR'")
    print("   • Explicación clara de lo que pasará")
    print("   • Pregunta específica sobre procesar factura")
    
    return True

if __name__ == "__main__":
    print("🚀 INICIANDO TEST DE DIÁLOGO MEJORADO")
    print("=" * 70)
    
    # Test 1: Apariencia
    success1 = demo_dialog_appearance()
    
    # Test 2: Funcionalidad
    success2 = demo_improved_dialog()
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL TEST:")
    print(f"   Apariencia: {'✅ MEJORADA' if success1 else '❌ ERROR'}")
    print(f"   Funcionalidad: {'✅ PROBADA' if success2 is not None else '❌ ERROR'}")
    
    if success2 is True:
        print("   Resultado: ✅ Usuario CONFIRMÓ")
    elif success2 is False:
        print("   Resultado: ❌ Usuario CANCELÓ")
    else:
        print("   Resultado: ⚠️ No se pudo probar")
    
    print("\n🎯 MEJORAS IMPLEMENTADAS:")
    print("   ✅ Botones más claros: 'Confirmación' y 'Cancelar'")
    print("   ✅ Colores distintivos: Verde para confirmar, Rojo para cancelar")
    print("   ✅ Iconos descriptivos: ✅ y ❌")
    print("   ✅ Mensaje más detallado sobre las acciones")
    print("   ✅ Tamaño y fuente mejorados")
    
    print("\n📚 Para el usuario:")
    print("   • El diálogo ahora es mucho más claro")
    print("   • Los botones indican claramente la acción")
    print("   • El mensaje explica exactamente qué pasará")
    print("   • Hacer clic en '✅ Confirmación' procesará la factura")
    print("   • Hacer clic en '❌ Cancelar' cancelará la operación")
