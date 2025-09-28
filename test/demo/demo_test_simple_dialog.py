#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test del diálogo simple de confirmación de stock
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tkinter as tk
from tkinter import messagebox

def test_simple_dialog():
    """Test del diálogo simple con tkinter estándar"""
    
    print("🧪 TEST - Diálogo Simple de Confirmación")
    print("=" * 50)
    
    # Mensaje de test
    test_message = """📦 IMPACTO EN STOCK:

• Producto PDF Económico 787449:
  Stock actual: 2 → Después: 1 unidades
  Estado: 🟠 STOCK BAJO (1)

==================================================
🔄 ACCIÓN A REALIZAR:
• Se guardará la factura
• Se actualizará automáticamente el stock
• Se registrarán los movimientos de stock"""
    
    try:
        print("🔄 Mostrando diálogo simple...")
        print("💡 Este diálogo usa tkinter estándar y siempre funciona")
        
        # Crear ventana temporal
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        root.attributes('-topmost', True)
        
        # Mostrar diálogo
        result = messagebox.askyesno(
            "Confirmar Procesamiento de Factura",
            f"{test_message}\n\n¿Desea continuar y procesar la factura?\n\n"
            f"• SÍ = Confirmar y procesar\n"
            f"• NO = Cancelar operación",
            icon='question'
        )
        
        root.destroy()
        
        print(f"📊 Resultado: {result}")
        
        if result:
            print("✅ Usuario hizo clic en 'SÍ' - Factura se procesaría")
        else:
            print("❌ Usuario hizo clic en 'NO' - Operación cancelada")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en diálogo simple: {e}")
        return None

def test_console_fallback():
    """Test del fallback por consola"""
    
    print("\n🧪 TEST - Fallback por Consola")
    print("-" * 30)
    
    test_message = """📦 IMPACTO EN STOCK:
• Producto: Stock 2 → 1 unidades
• Estado: STOCK BAJO"""
    
    print("🔄 Simulando fallback por consola...")
    print(f"📦 CONFIRMACIÓN DE STOCK:")
    print(test_message)
    print(f"\n¿Desea continuar y procesar la factura? (s/n): ", end="")
    
    try:
        response = input().lower().strip()
        result = response in ['s', 'si', 'sí', 'y', 'yes']
        
        print(f"📊 Respuesta: '{response}' → {result}")
        
        if result:
            print("✅ Usuario confirmó - Factura se procesaría")
        else:
            print("❌ Usuario canceló - Operación cancelada")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en fallback: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TESTS DE DIÁLOGOS ALTERNATIVOS")
    print("=" * 60)
    
    # Test 1: Diálogo simple con tkinter
    print("FASE 1: Diálogo simple con tkinter estándar")
    success1 = test_simple_dialog()
    
    # Test 2: Fallback por consola
    print("\nFASE 2: Fallback por consola")
    success2 = test_console_fallback()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"   Diálogo simple: {'✅ FUNCIONA' if success1 is not None else '❌ ERROR'}")
    print(f"   Fallback consola: {'✅ FUNCIONA' if success2 is not None else '❌ ERROR'}")
    
    if success1 is not None:
        print("\n✅ El diálogo simple funciona correctamente")
        print("🎯 Este será el fallback cuando el diálogo CustomTkinter falle")
    
    print("\n📋 CARACTERÍSTICAS DEL DIÁLOGO SIMPLE:")
    print("   • Usa tkinter estándar (siempre disponible)")
    print("   • Botones 'SÍ' y 'NO' claros")
    print("   • Mensaje detallado sobre las acciones")
    print("   • Siempre aparece encima de otras ventanas")
    print("   • Fallback por consola si todo falla")
    
    print("\n🔧 EN LA APLICACIÓN:")
    print("   1. Primero intenta diálogo CustomTkinter con botones CONFIRMAR/CANCELAR")
    print("   2. Si falla, usa diálogo tkinter simple con botones SÍ/NO")
    print("   3. Si todo falla, pregunta por consola")
    print("   4. Garantiza que el usuario siempre pueda confirmar o cancelar")
