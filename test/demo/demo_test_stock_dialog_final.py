#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test final del diálogo de confirmación de stock con botones CONFIRMAR/CANCELAR
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
from common.custom_dialogs import show_stock_confirmation_dialog

def test_final_stock_dialog():
    """Test del diálogo final de confirmación de stock"""
    
    print("🧪 TEST FINAL - Diálogo de Stock con Botones CONFIRMAR/CANCELAR")
    print("=" * 70)
    
    try:
        # Créer une application de test
        app = ctk.CTk()
        app.title("Test Diálogo Final de Stock")
        app.geometry("500x300")
        
        # Message de test exacto como aparece en la aplicación
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
        
        # Label d'information
        info_label = ctk.CTkLabel(
            app,
            text="TEST DEL DIÁLOGO FINAL DE CONFIRMACIÓN DE STOCK\n\n"
                 "Este diálogo debe mostrar:\n"
                 "✅ CONFIRMAR (verde) - Procesa la factura\n"
                 "❌ CANCELAR (rojo) - Cancela la operación\n"
                 "📋 Copiar - Copia el mensaje\n\n"
                 "Haz clic en el botón para probar:",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        info_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Variable para almacenar el resultado
        dialog_result = None
        
        def show_final_dialog():
            nonlocal dialog_result
            print("\n🔄 Mostrando diálogo FINAL de confirmación de stock...")
            print("💡 Debe mostrar botones: '✅ CONFIRMAR' y '❌ CANCELAR'")
            
            try:
                result = show_stock_confirmation_dialog(
                    app, 
                    "Confirmar Procesamiento de Factura", 
                    test_message
                )
                dialog_result = result
                
                print(f"📊 Resultado del diálogo: {result}")
                
                if result:
                    print("✅ Usuario hizo clic en 'CONFIRMAR'")
                    print("🔄 En la aplicación real: factura se guarda y stock se actualiza")
                    result_label.configure(
                        text="✅ CONFIRMADO\n\nLa factura se procesaría correctamente.\nEl stock se actualizaría de 2 → 1 unidades.",
                        text_color="green"
                    )
                elif result is False:
                    print("❌ Usuario hizo clic en 'CANCELAR'")
                    print("🛑 En la aplicación real: operación cancelada")
                    result_label.configure(
                        text="❌ CANCELADO\n\nLa operación fue cancelada.\nLa factura NO se procesó.",
                        text_color="red"
                    )
                else:
                    print("⚠️ Diálogo cerrado sin selección")
                    result_label.configure(
                        text="⚠️ SIN SELECCIÓN\n\nEl diálogo fue cerrado sin hacer clic en ningún botón.",
                        text_color="orange"
                    )
                
            except Exception as e:
                print(f"❌ Error mostrando diálogo: {e}")
                import traceback
                traceback.print_exc()
                result_label.configure(
                    text=f"❌ ERROR\n\n{str(e)}",
                    text_color="red"
                )
        
        # Botón para mostrar el diálogo
        test_btn = ctk.CTkButton(
            app,
            text="🔍 Mostrar Diálogo Final de Stock",
            command=show_final_dialog,
            fg_color="#2E8B57",
            hover_color="#228B22",
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        test_btn.pack(pady=15)
        
        # Label para mostrar el resultado
        result_label = ctk.CTkLabel(
            app,
            text="Resultado aparecerá aquí después de probar el diálogo",
            font=ctk.CTkFont(size=11),
            justify="center"
        )
        result_label.pack(pady=10)
        
        print("\n🚀 Aplicación de test iniciada")
        print("💡 Haz clic en el botón para probar el diálogo final")
        print("🔍 Verifica que los botones sean: '✅ CONFIRMAR' y '❌ CANCELAR'")
        print("📋 También debe haber un botón 'Copiar' para copiar el mensaje")
        
        # Ejecutar la aplicación
        app.mainloop()
        
        print(f"\n📊 Resultado final del test: {dialog_result}")
        return dialog_result
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return None

def show_expected_appearance():
    """Muestra cómo debe verse el diálogo"""
    
    print("\n🎨 APARIENCIA ESPERADA DEL DIÁLOGO")
    print("=" * 50)
    
    print("""
┌─────────────────────────────────────────────────────────┐
│ 📦 Confirmar Procesamiento de Factura                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 📦 IMPACTO EN STOCK:                                   │
│                                                         │
│ • nuevo prod 270925 1:                                 │
│   Stock actual: 2 → Después: 1 unidades               │
│   Estado: 🟠 STOCK BAJO (1)                           │
│                                                         │
│ ================================================       │
│ 🔄 ACCIÓN A REALIZAR:                                  │
│ • Se guardará la factura                               │
│ • Se actualizará automáticamente el stock             │
│ • Se registrarán los movimientos de stock             │
│                                                         │
│ ¿Desea continuar y procesar la factura?               │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [📋 Copiar]              [✅ CONFIRMAR] [❌ CANCELAR]  │
└─────────────────────────────────────────────────────────┘
""")
    
    print("🎯 CARACTERÍSTICAS CLAVE:")
    print("   • Botón '✅ CONFIRMAR' en VERDE")
    print("   • Botón '❌ CANCELAR' en ROJO")
    print("   • Botón '📋 Copiar' en gris")
    print("   • Texto seleccionable y copiable")
    print("   • Tamaño de botones: 140x40 píxeles")
    print("   • Fuente en negrita para los botones principales")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST FINAL DEL DIÁLOGO DE STOCK")
    print("=" * 70)
    
    # Mostrar apariencia esperada
    show_expected_appearance()
    
    # Test funcional
    success = test_final_stock_dialog()
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL TEST:")
    
    if success is True:
        print("   ✅ ÉXITO: Usuario confirmó el procesamiento")
        print("   🎯 El diálogo funciona correctamente")
        print("   ✅ Los botones son claros y funcionales")
    elif success is False:
        print("   ❌ CANCELADO: Usuario canceló la operación")
        print("   🎯 El diálogo funciona correctamente")
        print("   ✅ Los botones son claros y funcionales")
    else:
        print("   ⚠️ ERROR O SIN PRUEBA: Revisar implementación")
        print("   🔧 Puede haber problemas con el diálogo")
    
    print("\n🎉 RESULTADO ESPERADO:")
    print("   • El diálogo debe mostrar botones '✅ CONFIRMAR' y '❌ CANCELAR'")
    print("   • Los colores deben ser verde y rojo respectivamente")
    print("   • El mensaje debe ser claro sobre las acciones")
    print("   • Debe funcionar correctamente en la aplicación real")
    
    print("\n📚 Para usar en la aplicación:")
    print("   1. Crear una factura con producto de stock bajo")
    print("   2. Hacer clic en 'Guardar'")
    print("   3. Aparecerá el diálogo mejorado")
    print("   4. Hacer clic en '✅ CONFIRMAR' para procesar")
    print("   5. O hacer clic en '❌ CANCELAR' para cancelar")
