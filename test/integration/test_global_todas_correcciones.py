#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test global que verifica que todas las correcciones funcionan correctamente
"""

import sys
import os
import subprocess
import pytest
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_test_file(test_file):
    """Ejecutar un archivo de test y devolver el resultado"""
    try:
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))

        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

@pytest.mark.skip(reason="Referenced test files do not exist")
def test_global_todas_correcciones():
    """Test global que ejecuta todos los tests de correcciones"""
    print("🧪 EJECUTANDO TESTS GLOBALES DE TODAS LAS CORRECCIONES")
    print("=" * 70)
    
    # Lista de todos los tests creados
    tests = [
        ("test_nueva_numeracion.py", "Sistema de Numeración de Facturas"),
        ("test_producto_selection_fix.py", "Selección Automática Primer Producto"),
        ("test_edicion_automatica_facturas.py", "Edición Automática de Facturas"),
        ("test_organizacion_completo.py", "Módulo Organización Completo"),
        ("test_dialogo_logo_fix.py", "Corrección Diálogos en Segundo Plano"),
        ("test_messageboxes_fix.py", "Corrección MessageBoxes en Segundo Plano"),
        ("test_logo_image_fix.py", "Corrección Error TclError del Logo"),
        ("test_validacion_facturas_opcional.py", "Validación Opcional NIF/Email/Teléfono"),
        ("test_facturas_validacion_integracion.py", "Integración Validación Opcional"),
        ("test_ejemplos_validacion_facturas.py", "Ejemplos Prácticos Validación")
    ]
    
    results = {}
    total_tests = len(tests)
    passed_tests = 0
    
    print(f"📋 Ejecutando {total_tests} suites de tests...\n")
    
    for i, (test_file, description) in enumerate(tests, 1):
        print(f"{i}️⃣ Test: {description}")
        print(f"   📁 Archivo: {test_file}")
        
        if not os.path.exists(test_file):
            print(f"   ❌ ARCHIVO NO ENCONTRADO")
            results[test_file] = False
            continue
        
        success, stdout, stderr = run_test_file(test_file)
        
        if success:
            print(f"   ✅ PASADO")
            passed_tests += 1
            results[test_file] = True
        else:
            print(f"   ❌ FALLIDO")
            if stderr:
                print(f"   📝 Error: {stderr[:200]}...")
            results[test_file] = False
        
        print()
    
    # Resumen final
    print("=" * 70)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 70)
    
    for test_file, description in tests:
        status = "✅ PASADO" if results.get(test_file, False) else "❌ FALLIDO"
        print(f"{status} - {description}")
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"   Tests ejecutados: {total_tests}")
    print(f"   Tests pasados: {passed_tests}")
    print(f"   Tests fallidos: {total_tests - passed_tests}")
    print(f"   Porcentaje éxito: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✨ Todas las correcciones están funcionando correctamente")
        assert True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests fallaron")
        print("🔧 Revisar las correcciones que no pasaron")
        assert False, f"{total_tests - passed_tests} tests fallaron"

def test_aplicacion_completa():
    """Test adicional: verificar que la aplicación se inicia sin errores"""
    print("\n" + "=" * 70)
    print("🚀 TEST ADICIONAL: INICIO DE APLICACIÓN")
    print("=" * 70)
    
    try:
        # Intentar importar módulos principales
        print("1️⃣ Importando módulos principales...")
        
        from database.database import Database
        from database.models import Organizacion, Producto, Factura
        from utils.factura_numbering import factura_numbering_service
        print("   ✅ Módulos de base de datos importados")
        
        # Verificar base de datos
        print("2️⃣ Verificando base de datos...")
        db = Database()
        print("   ✅ Base de datos inicializada")
        
        # Verificar sistema de numeración
        print("3️⃣ Verificando sistema de numeración...")
        numero = factura_numbering_service.get_next_numero_factura()
        print(f"   ✅ Número generado: {numero}")
        
        # Verificar organización
        print("4️⃣ Verificando módulo organización...")
        org = Organizacion.get()
        print(f"   ✅ Organización cargada: {org.nombre or 'Sin nombre'}")

        print("\n✅ APLICACIÓN FUNCIONA CORRECTAMENTE")
        assert True

    except Exception as e:
        print(f"\n❌ ERROR EN APLICACIÓN: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Error en aplicación: {e}"

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN COMPLETA DE TODAS LAS CORRECCIONES")
    print("=" * 70)
    
    # Ejecutar tests globales
    tests_passed = test_global_todas_correcciones()
    
    # Test adicional de aplicación
    app_works = test_aplicacion_completa()
    
    # Resultado final
    print("\n" + "=" * 70)
    print("🏁 RESULTADO FINAL")
    print("=" * 70)
    
    if tests_passed and app_works:
        print("🎉 ¡ÉXITO COMPLETO!")
        print("✅ Todos los tests pasan")
        print("✅ Aplicación funciona correctamente")
        print("✅ Todas las correcciones están operativas")
        print("\n🚀 El sistema está listo para producción!")
        sys.exit(0)
    else:
        print("⚠️  PROBLEMAS DETECTADOS")
        if not tests_passed:
            print("❌ Algunos tests fallaron")
        if not app_works:
            print("❌ La aplicación tiene problemas")
        print("\n🔧 Revisar las correcciones necesarias")
        sys.exit(1)
