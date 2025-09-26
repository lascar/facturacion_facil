#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test con ejemplos prácticos de validación opcional en facturas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ejemplos_validacion_facturas():
    """Test con ejemplos prácticos de validación"""
    print("🧪 Ejemplos prácticos de validación opcional en facturas")
    print("=" * 65)
    
    try:
        from common.validators import FormValidator
        
        print("✅ Módulos importados correctamente")
        
        # Ejemplos de casos reales
        casos_prueba = [
            {
                "nombre": "Cliente sin datos opcionales",
                "dni": "",
                "email": "",
                "telefono": "",
                "esperado": "válido"
            },
            {
                "nombre": "Cliente con DNI español válido",
                "dni": "12345678Z",
                "email": "",
                "telefono": "",
                "esperado": "válido"
            },
            {
                "nombre": "Cliente con NIE válido",
                "dni": "X1234567L",
                "email": "",
                "telefono": "",
                "esperado": "válido"
            },
            {
                "nombre": "Cliente con email válido",
                "dni": "",
                "email": "cliente@empresa.com",
                "telefono": "",
                "esperado": "válido"
            },
            {
                "nombre": "Cliente con teléfono español",
                "dni": "",
                "email": "",
                "telefono": "+34 91 123 45 67",
                "esperado": "válido"
            },
            {
                "nombre": "Cliente completo válido",
                "dni": "12345678Z",
                "email": "juan.perez@email.com",
                "telefono": "91 123 45 67",
                "esperado": "válido"
            },
            {
                "nombre": "DNI inválido (muy corto)",
                "dni": "1234567",
                "email": "",
                "telefono": "",
                "esperado": "inválido"
            },
            {
                "nombre": "Email inválido (sin @)",
                "dni": "",
                "email": "cliente.email.com",
                "telefono": "",
                "esperado": "inválido"
            },
            {
                "nombre": "Teléfono inválido (con letras)",
                "dni": "",
                "email": "",
                "telefono": "91-abc-def",
                "esperado": "inválido"
            },
            {
                "nombre": "Múltiples errores",
                "dni": "123",
                "email": "email@",
                "telefono": "12345",
                "esperado": "inválido"
            }
        ]
        
        print(f"\n📋 Probando {len(casos_prueba)} casos de uso reales:")
        print("-" * 65)
        
        casos_pasados = 0
        
        for i, caso in enumerate(casos_prueba, 1):
            print(f"\n{i}️⃣ {caso['nombre']}")
            print(f"   📝 DNI/NIE: '{caso['dni']}'")
            print(f"   📝 Email: '{caso['email']}'")
            print(f"   📝 Teléfono: '{caso['telefono']}'")
            
            # Validar cada campo
            errores = []
            
            # Validar DNI/NIE
            error_dni = FormValidator.validate_dni_nie(caso['dni'])
            if error_dni:
                errores.append(error_dni)
            
            # Validar email
            error_email = FormValidator.validate_email(caso['email'])
            if error_email:
                errores.append(error_email)
            
            # Validar teléfono
            error_telefono = FormValidator.validate_phone(caso['telefono'])
            if error_telefono:
                errores.append(error_telefono)
            
            # Verificar resultado
            tiene_errores = len(errores) > 0
            resultado_esperado = caso['esperado'] == 'inválido'
            
            if tiene_errores == resultado_esperado:
                if tiene_errores:
                    print(f"   ❌ Errores encontrados (como se esperaba):")
                    for error in errores:
                        print(f"      • {error}")
                else:
                    print(f"   ✅ Sin errores (como se esperaba)")
                print(f"   ✅ Caso PASADO")
                casos_pasados += 1
            else:
                print(f"   ❌ Resultado inesperado:")
                print(f"      Esperado: {caso['esperado']}")
                print(f"      Obtenido: {'inválido' if tiene_errores else 'válido'}")
                if errores:
                    for error in errores:
                        print(f"      • {error}")
                print(f"   ❌ Caso FALLIDO")
        
        print("\n" + "=" * 65)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 65)
        print(f"Casos probados: {len(casos_prueba)}")
        print(f"Casos pasados: {casos_pasados}")
        print(f"Casos fallidos: {len(casos_prueba) - casos_pasados}")
        print(f"Porcentaje éxito: {(casos_pasados/len(casos_prueba))*100:.1f}%")
        
        if casos_pasados == len(casos_prueba):
            print("\n🎉 ¡TODOS LOS CASOS DE USO PASARON!")
            print("✨ La validación opcional funciona perfectamente en casos reales")
            
            # Mostrar ejemplos de uso
            print("\n📋 EJEMPLOS DE USO PARA EL USUARIO:")
            print("-" * 40)
            print("✅ VÁLIDOS (opcionales):")
            print("   • DNI/NIE: (vacío) - No es obligatorio")
            print("   • DNI: 12345678Z - Formato español correcto")
            print("   • NIE: X1234567L - Formato NIE correcto")
            print("   • Email: (vacío) - No es obligatorio")
            print("   • Email: usuario@dominio.com - Formato correcto")
            print("   • Teléfono: (vacío) - No es obligatorio")
            print("   • Teléfono: +34 91 123 45 67 - Con prefijo")
            print("   • Teléfono: 91 123 45 67 - Sin prefijo")
            print()
            print("❌ INVÁLIDOS (si se proporcionan):")
            print("   • DNI: 1234567 - Muy corto")
            print("   • DNI: 123456789A - Muy largo")
            print("   • Email: usuario@dominio - Sin extensión")
            print("   • Email: @dominio.com - Sin usuario")
            print("   • Teléfono: 12345 - Muy corto")
            print("   • Teléfono: abc123 - Con letras")
            
            return True
        else:
            print(f"\n⚠️ {len(casos_prueba) - casos_pasados} casos fallaron")
            return False
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ejemplos_validacion_facturas()
    sys.exit(0 if success else 1)
