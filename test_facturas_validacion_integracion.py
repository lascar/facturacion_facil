#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de integración para verificar que la validación opcional funciona
en la interfaz de facturas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_facturas_validacion_integracion():
    """Test de integración de validación opcional en facturas"""
    print("🧪 Probando integración de validación opcional en interfaz de facturas")
    print("=" * 75)
    
    try:
        # Importar módulos necesarios
        import customtkinter as ctk
        from ui.facturas import FacturasWindow
        from common.ui_components import FormHelper
        from datetime import datetime
        
        print("✅ Módulos importados correctamente")
        
        # Test 1: Crear ventana de facturas
        print("\n1️⃣ Test: Crear ventana de facturas")
        
        root = ctk.CTk()
        root.withdraw()
        
        facturas_window = FacturasWindow(root)
        
        # Verificar que la ventana se creó correctamente
        assert facturas_window.window is not None
        assert hasattr(facturas_window, 'validate_factura_form')
        
        print("   ✅ Ventana de facturas creada correctamente")
        print("   ✅ Método de validación existe")
        print("   ✅ Test 1 PASADO")
        
        # Test 2: Validar formulario con campos opcionales vacíos
        print("\n2️⃣ Test: Formulario válido con campos opcionales vacíos")
        
        # Llenar solo campos obligatorios
        FormHelper.set_entry_value(facturas_window.numero_entry, "FACT-001-2025")
        FormHelper.set_entry_value(facturas_window.fecha_entry, datetime.now().strftime("%Y-%m-%d"))
        FormHelper.set_entry_value(facturas_window.nombre_cliente_entry, "Cliente Test")
        
        # Dejar campos opcionales vacíos
        FormHelper.set_entry_value(facturas_window.dni_nie_entry, "")
        FormHelper.set_entry_value(facturas_window.email_cliente_entry, "")
        FormHelper.set_entry_value(facturas_window.telefono_cliente_entry, "")
        
        # Validar formulario
        errors = facturas_window.validate_factura_form()
        
        # Solo debería haber errores de productos (no de campos opcionales)
        optional_field_errors = [error for error in errors if any(field in error.lower() 
                                for field in ['dni', 'nie', 'nif', 'email', 'teléfono', 'telefono'])]
        
        assert len(optional_field_errors) == 0, f"No debería haber errores de campos opcionales: {optional_field_errors}"
        
        print("   ✅ Campos opcionales vacíos no generan errores")
        print("   ✅ Test 2 PASADO")
        
        # Test 3: Validar con formatos válidos en campos opcionales
        print("\n3️⃣ Test: Formatos válidos en campos opcionales")
        
        # Llenar campos opcionales con formatos válidos
        FormHelper.set_entry_value(facturas_window.dni_nie_entry, "12345678Z")
        FormHelper.set_entry_value(facturas_window.email_cliente_entry, "cliente@test.com")
        FormHelper.set_entry_value(facturas_window.telefono_cliente_entry, "+34 123 456 789")
        
        # Validar formulario
        errors = facturas_window.validate_factura_form()
        
        # No debería haber errores de campos opcionales
        optional_field_errors = [error for error in errors if any(field in error.lower() 
                                for field in ['dni', 'nie', 'nif', 'email', 'teléfono', 'telefono'])]
        
        assert len(optional_field_errors) == 0, f"No debería haber errores con formatos válidos: {optional_field_errors}"
        
        print("   ✅ Formatos válidos en campos opcionales aceptados")
        print("   ✅ Test 3 PASADO")
        
        # Test 4: Validar con formatos inválidos en campos opcionales
        print("\n4️⃣ Test: Formatos inválidos en campos opcionales")
        
        # Llenar campos opcionales con formatos inválidos
        FormHelper.set_entry_value(facturas_window.dni_nie_entry, "123456")  # Muy corto
        FormHelper.set_entry_value(facturas_window.email_cliente_entry, "email_invalido")  # Sin @
        FormHelper.set_entry_value(facturas_window.telefono_cliente_entry, "abc123")  # Con letras
        
        # Validar formulario
        errors = facturas_window.validate_factura_form()
        
        # Debería haber errores de campos opcionales
        dni_errors = [error for error in errors if 'dni' in error.lower() or 'nie' in error.lower()]
        email_errors = [error for error in errors if 'email' in error.lower()]
        phone_errors = [error for error in errors if 'teléfono' in error.lower() or 'telefono' in error.lower()]
        
        assert len(dni_errors) > 0, "Debería haber error de DNI/NIE inválido"
        assert len(email_errors) > 0, "Debería haber error de email inválido"
        assert len(phone_errors) > 0, "Debería haber error de teléfono inválido"
        
        print(f"   📝 Errores DNI/NIE: {len(dni_errors)}")
        print(f"   📝 Errores Email: {len(email_errors)}")
        print(f"   📝 Errores Teléfono: {len(phone_errors)}")
        print("   ✅ Formatos inválidos generan errores correctamente")
        print("   ✅ Test 4 PASADO")
        
        # Test 5: Verificar mensajes de error informativos
        print("\n5️⃣ Test: Mensajes de error informativos")
        
        # Verificar que los mensajes de error son informativos
        all_errors = dni_errors + email_errors + phone_errors

        for error in all_errors:
            assert len(error) > 10, f"Mensaje de error muy corto: {error}"
            # Verificar que el mensaje contiene información útil
            informative_words = ['formato', 'inválido', 'incorrecto', 'debe', 'caracteres', 'ejemplo', 'permitido']
            assert any(word in error.lower() for word in informative_words), \
                   f"Mensaje de error no es informativo: {error}"
        
        print("   ✅ Mensajes de error son informativos")
        print("   ✅ Test 5 PASADO")
        
        # Test 6: Verificar que campos obligatorios siguen siendo obligatorios
        print("\n6️⃣ Test: Campos obligatorios siguen siendo obligatorios")
        
        # Limpiar campos obligatorios
        FormHelper.set_entry_value(facturas_window.numero_entry, "")
        FormHelper.set_entry_value(facturas_window.nombre_cliente_entry, "")
        
        # Poner campos opcionales válidos
        FormHelper.set_entry_value(facturas_window.dni_nie_entry, "12345678Z")
        FormHelper.set_entry_value(facturas_window.email_cliente_entry, "cliente@test.com")
        FormHelper.set_entry_value(facturas_window.telefono_cliente_entry, "+34 123 456 789")
        
        # Validar formulario
        errors = facturas_window.validate_factura_form()
        
        # Debería haber errores de campos obligatorios
        required_errors = [error for error in errors if any(field in error.lower() 
                          for field in ['número', 'numero', 'nombre', 'cliente'])]
        
        assert len(required_errors) > 0, "Debería haber errores de campos obligatorios"
        
        print(f"   📝 Errores de campos obligatorios: {len(required_errors)}")
        print("   ✅ Campos obligatorios siguen siendo obligatorios")
        print("   ✅ Test 6 PASADO")
        
        # Limpiar
        facturas_window.window.destroy()
        root.destroy()
        
        print("\n" + "=" * 75)
        print("🎉 TODOS LOS TESTS DE INTEGRACIÓN PASARON")
        print("📋 Funcionalidades verificadas:")
        print("   ✅ Interfaz de facturas funciona correctamente")
        print("   ✅ Campos opcionales vacíos no generan errores")
        print("   ✅ Formatos válidos en campos opcionales aceptados")
        print("   ✅ Formatos inválidos en campos opcionales rechazados")
        print("   ✅ Mensajes de error informativos")
        print("   ✅ Campos obligatorios siguen siendo obligatorios")
        print("\n✨ La validación opcional está perfectamente integrada!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_facturas_validacion_integracion()
    sys.exit(0 if success else 1)
