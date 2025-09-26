#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar que la selección del primer producto funciona correctamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from database.models import Producto
from ui.producto_factura_dialog import ProductoFacturaDialog

def test_primer_producto_seleccion():
    """Test que verifica que el primer producto se selecciona automáticamente"""
    print("🧪 Probando selección automática del primer producto")
    print("=" * 60)
    
    try:
        # Crear productos de prueba
        productos_test = [
            Producto(
                id=1,
                nombre="Producto A",
                referencia="PROD-A",
                precio=10.0,
                categoria="Test",
                iva_recomendado=21.0,
                descripcion="Primer producto de prueba"
            ),
            Producto(
                id=2,
                nombre="Producto B", 
                referencia="PROD-B",
                precio=20.0,
                categoria="Test",
                iva_recomendado=21.0,
                descripcion="Segundo producto de prueba"
            ),
            Producto(
                id=3,
                nombre="Producto C",
                referencia="PROD-C", 
                precio=30.0,
                categoria="Test",
                iva_recomendado=10.0,
                descripcion="Tercer producto de prueba"
            )
        ]
        
        print(f"✅ Creados {len(productos_test)} productos de prueba")
        
        # Crear ventana raíz para el test
        root = ctk.CTk()
        root.withdraw()  # Ocultar la ventana principal
        
        print("✅ Ventana raíz creada")
        
        # Test 1: Crear diálogo sin producto pre-seleccionado
        print("\n1️⃣ Test: Diálogo sin producto pre-seleccionado")
        
        dialog = ProductoFacturaDialog(root, productos_test)
        
        # Verificar que el primer producto se seleccionó automáticamente
        if dialog.producto_seleccionado:
            print(f"   ✅ Producto seleccionado automáticamente: {dialog.producto_seleccionado.nombre}")
            print(f"   ✅ ID del producto: {dialog.producto_seleccionado.id}")
            assert dialog.producto_seleccionado.id == 1, "Debería seleccionar el primer producto"
            print("   ✅ Test 1 PASADO")
        else:
            print("   ❌ Test 1 FALLIDO: No se seleccionó ningún producto automáticamente")
            return False
        
        dialog.dialog.destroy()
        
        # Test 2: Verificar que el combo tiene el valor correcto
        print("\n2️⃣ Test: Valor del ComboBox")
        
        dialog2 = ProductoFacturaDialog(root, productos_test)
        combo_value = dialog2.producto_combo.get()
        expected_value = f"{productos_test[0].nombre} ({productos_test[0].referencia}) - €10,00"
        
        print(f"   📝 Valor del combo: {combo_value}")
        print(f"   📝 Valor esperado: {expected_value}")
        
        if combo_value and productos_test[0].nombre in combo_value:
            print("   ✅ ComboBox tiene el valor correcto")
            print("   ✅ Test 2 PASADO")
        else:
            print("   ❌ Test 2 FALLIDO: ComboBox no tiene el valor esperado")
            return False
        
        dialog2.dialog.destroy()
        
        # Test 3: Verificar validación del formulario
        print("\n3️⃣ Test: Validación del formulario")
        
        dialog3 = ProductoFacturaDialog(root, productos_test)
        
        # Simular valores en los campos
        from common.ui_components import FormHelper
        FormHelper.set_entry_value(dialog3.cantidad_entry, "2")
        FormHelper.set_entry_value(dialog3.precio_entry, "15.0")
        FormHelper.set_entry_value(dialog3.iva_entry, "21.0")
        FormHelper.set_entry_value(dialog3.descuento_entry, "0")
        
        errors = dialog3.validate_form()
        
        if not errors:
            print("   ✅ Formulario válido con primer producto seleccionado")
            print("   ✅ Test 3 PASADO")
        else:
            print(f"   ❌ Test 3 FALLIDO: Errores de validación: {errors}")
            return False
        
        dialog3.dialog.destroy()
        
        # Test 4: Cambio de selección manual
        print("\n4️⃣ Test: Cambio de selección manual")
        
        dialog4 = ProductoFacturaDialog(root, productos_test)
        
        # Cambiar a segundo producto
        segundo_producto_text = f"{productos_test[1].nombre} ({productos_test[1].referencia}) - €20,00"
        dialog4.producto_combo.set(segundo_producto_text)
        dialog4.on_producto_selected(segundo_producto_text)
        
        if dialog4.producto_seleccionado and dialog4.producto_seleccionado.id == 2:
            print(f"   ✅ Cambio a segundo producto exitoso: {dialog4.producto_seleccionado.nombre}")
            print("   ✅ Test 4 PASADO")
        else:
            print("   ❌ Test 4 FALLIDO: No se pudo cambiar al segundo producto")
            return False
        
        dialog4.dialog.destroy()
        root.destroy()
        
        print("\n" + "=" * 60)
        print("🎉 TODOS LOS TESTS PASARON")
        print("📋 Correcciones verificadas:")
        print("   ✅ Primer producto se selecciona automáticamente")
        print("   ✅ ComboBox muestra el valor correcto")
        print("   ✅ Validación funciona correctamente")
        print("   ✅ Cambio manual de selección funciona")
        print("\n✨ El problema de selección del primer producto está RESUELTO!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_primer_producto_seleccion()
    sys.exit(0 if success else 1)
