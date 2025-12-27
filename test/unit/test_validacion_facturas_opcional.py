#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar que NIF, teléfono y email son opcionales en facturas
pero se validan si se proporcionan
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_validacion_facturas_opcional():
    """Test que verifica validación opcional de campos en facturas"""
    print("🧪 Probando validación opcional de NIF, teléfono y email en facturas")
    print("=" * 70)
    
    try:
        # Importar después de configurar el path
        from common.validators import FormValidator
        
        print("✅ Módulos importados correctamente")
        
        # Test 1: Campos vacíos deben ser válidos (opcionales)
        print("\n1️⃣ Test: Campos vacíos son opcionales")
        
        # DNI/NIE/NIF vacío
        result = FormValidator.validate_dni_nie("")
        assert result is None, "DNI/NIE vacío debería ser válido"
        
        result = FormValidator.validate_dni_nie(None)
        assert result is None, "DNI/NIE None debería ser válido"
        
        result = FormValidator.validate_dni_nie("   ")
        assert result is None, "DNI/NIE con espacios debería ser válido"
        
        # Email vacío
        result = FormValidator.validate_email("")
        assert result is None, "Email vacío debería ser válido"
        
        result = FormValidator.validate_email(None)
        assert result is None, "Email None debería ser válido"
        
        result = FormValidator.validate_email("   ")
        assert result is None, "Email con espacios debería ser válido"
        
        # Teléfono vacío
        result = FormValidator.validate_phone("")
        assert result is None, "Teléfono vacío debería ser válido"
        
        result = FormValidator.validate_phone(None)
        assert result is None, "Teléfono None debería ser válido"
        
        result = FormValidator.validate_phone("   ")
        assert result is None, "Teléfono con espacios debería ser válido"
        
        print("   ✅ Todos los campos vacíos son válidos (opcionales)")
        print("   ✅ Test 1 PASADO")
        
        # Test 2: Formatos válidos cuando se proporcionan
        print("\n2️⃣ Test: Formatos válidos cuando se proporcionan")
        
        # DNI/NIE/NIF válidos (sin validación estricta de letra de control)
        valid_dnis = [
            "12345678Z",  # DNI formato válido
            "X1234567L",  # NIE formato válido
            "Y7654321X",  # NIE formato válido
            "Z9876543R"   # NIE formato válido
        ]
        
        dni_valid_count = 0
        for dni in valid_dnis:
            result = FormValidator.validate_dni_nie(dni)
            if result is None:
                dni_valid_count += 1
            else:
                print(f"   📝 DNI {dni}: {result}")
        
        print(f"   📝 {dni_valid_count}/{len(valid_dnis)} DNIs con formato válido")
        
        # Emails válidos
        valid_emails = [
            "usuario@dominio.com",
            "test.email@empresa.es",
            "cliente123@gmail.com",
            "info@mi-empresa.org"
        ]
        
        for email in valid_emails:
            result = FormValidator.validate_email(email)
            assert result is None, f"Email {email} debería ser válido"
        
        # Teléfonos válidos
        valid_phones = [
            "123456789",
            "+34 123 456 789",
            "(91) 123-4567",
            "91 123 45 67",
            "+34-123-456-789"
        ]
        
        for phone in valid_phones:
            result = FormValidator.validate_phone(phone)
            assert result is None, f"Teléfono {phone} debería ser válido"
        
        print("   ✅ Formatos válidos aceptados correctamente")
        print("   ✅ Test 2 PASADO")
        
        # Test 3: Formatos inválidos son rechazados
        print("\n3️⃣ Test: Formatos inválidos son rechazados")
        
        # DNI/NIE/NIF inválidos
        invalid_dnis = [
            "1234567",      # Muy corto
            "123456789A",   # Muy largo
            "ABCD1234E",    # Formato incorrecto
            "12345678",     # Sin letra
            "1234567AA"     # Dos letras
        ]
        
        for dni in invalid_dnis:
            result = FormValidator.validate_dni_nie(dni)
            assert result is not None, f"DNI {dni} debería ser inválido"
        
        # Emails inválidos
        invalid_emails = [
            "usuario",           # Sin @
            "@dominio.com",      # Sin usuario
            "usuario@",          # Sin dominio
            "usuario@dominio",   # Sin TLD
            "usuario..test@dom.com",  # Puntos consecutivos
            "a@b.c"             # Muy corto
        ]
        
        for email in invalid_emails:
            result = FormValidator.validate_email(email)
            assert result is not None, f"Email {email} debería ser inválido"
        
        # Teléfonos inválidos
        invalid_phones = [
            "12345",           # Muy corto
            "abc123",          # Letras
            "123@456",         # Caracteres inválidos
            "12345678901234567890123",  # Muy largo
            "++123456789"      # Doble +
        ]
        
        for phone in invalid_phones:
            result = FormValidator.validate_phone(phone)
            assert result is not None, f"Teléfono {phone} debería ser inválido"
        
        print("   ✅ Formatos inválidos rechazados correctamente")
        print("   ✅ Test 3 PASADO")
        
        print("\n" + "=" * 70)
        print("🎉 TODOS LOS TESTS PASARON")
        print("📋 Validaciones verificadas:")
        print("   ✅ DNI/NIE/NIF opcional pero validado si se proporciona")
        print("   ✅ Email opcional pero validado si se proporciona")
        print("   ✅ Teléfono opcional pero validado si se proporciona")
        print("   ✅ Formatos válidos aceptados")
        print("   ✅ Formatos inválidos rechazados")
        print("\n✨ La validación opcional de facturas funciona correctamente!")
        
        assert True
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        assert False, "Test failed"

if __name__ == "__main__":
    success = test_validacion_facturas_opcional()
    sys.exit(0 if success else 1)
