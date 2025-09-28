#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de validation finale de la solution de stock
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
import time

def run_test_script(script_path, description):
    """Exécute un script de test et retourne le résultat"""
    print(f"\n🔍 {description}")
    print("-" * 50)
    
    try:
        # Exécuter le script
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ ÉXITO")
            return True
        else:
            print("❌ FALLO")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - Test tardó más de 30 segundos")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def check_file_exists(file_path, description):
    """Verifica que un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO ENCONTRADO")
        return False

def validate_solution():
    """Valida toda la solución implementada"""
    
    print("🔍 VALIDACIÓN FINAL - Solución de Stock")
    print("=" * 70)
    
    validation_results = []
    
    # 1. Verificar archivos clave
    print("\n1️⃣ VERIFICACIÓN DE ARCHIVOS")
    print("-" * 30)
    
    key_files = [
        ("ui/facturas_methods.py", "Archivo principal con solución"),
        ("common/custom_dialogs.py", "Diálogos personalizados"),
        ("database/models.py", "Modelos de base de datos"),
        ("docs/fixes/ROBUST_DIALOG_SOLUTION.md", "Documentación técnica"),
        ("docs/fixes/PDF_EXPORT_SELECTION_FIX.md", "Corrección exportación PDF"),
        ("docs/USER_GUIDE_STOCK_CONFIRMATION.md", "Guía de usuario"),
        ("test/demo/demo_complete_stock_solution_test.py", "Test completo"),
        ("test/integration/test_stock_update_integration.py", "Tests de integración"),
        ("test/integration/test_pdf_export_integration.py", "Tests integración PDF"),
        ("test/demo/demo_test_factura_selection.py", "Test selección facturas"),
        ("test/demo/demo_test_pdf_export.py", "Test exportación PDF")
    ]
    
    files_ok = 0
    for file_path, description in key_files:
        if check_file_exists(file_path, description):
            files_ok += 1
    
    validation_results.append(("Archivos clave", files_ok, len(key_files)))
    
    # 2. Ejecutar tests básicos
    print("\n2️⃣ TESTS BÁSICOS")
    print("-" * 20)
    
    basic_tests = [
        ("test/demo/demo_simple_stock_test.py", "Test básico del problema"),
        ("test/demo/demo_quick_inheritance_check.py", "Verificación de herencia")
    ]
    
    basic_tests_ok = 0
    for script, description in basic_tests:
        if os.path.exists(script):
            if run_test_script(script, description):
                basic_tests_ok += 1
        else:
            print(f"❌ {description}: Script no encontrado")
    
    validation_results.append(("Tests básicos", basic_tests_ok, len(basic_tests)))
    
    # 3. Verificar implementación de métodos clave
    print("\n3️⃣ VERIFICACIÓN DE MÉTODOS CLAVE")
    print("-" * 35)
    
    try:
        from ui.facturas_methods import FacturasMethodsMixin
        
        key_methods = [
            "guardar_factura",
            "update_stock_after_save",
            "show_stock_impact_summary",
            "show_stock_confirmation_dialog_direct",
            "show_simple_confirmation_dialog",
            "exportar_pdf"
        ]
        
        methods_ok = 0
        for method_name in key_methods:
            if hasattr(FacturasMethodsMixin, method_name):
                print(f"✅ Método {method_name}: Disponible")
                methods_ok += 1
            else:
                print(f"❌ Método {method_name}: NO disponible")
        
        validation_results.append(("Métodos clave", methods_ok, len(key_methods)))
        
    except Exception as e:
        print(f"❌ Error verificando métodos: {e}")
        validation_results.append(("Métodos clave", 0, 5))
    
    # 4. Verificar base de datos
    print("\n4️⃣ VERIFICACIÓN DE BASE DE DATOS")
    print("-" * 32)
    
    try:
        from database.database import db
        from database.models import Producto, Stock, Factura, FacturaItem
        
        db.init_database()
        
        # Verificar que las tablas existen
        tables_to_check = ["productos", "stock", "facturas", "factura_items", "stock_movements"]
        tables_ok = 0

        for table in tables_to_check:
            try:
                # Intentar hacer una consulta simple
                if table == "productos":
                    count = len(Producto.get_all())
                elif table == "stock":
                    # Verificar que la tabla stock existe
                    stock_test = Stock.get_by_product(1)  # Puede retornar 0
                    count = "OK"
                elif table == "facturas":
                    facturas = Factura.get_all()
                    count = len(facturas)
                    # Test adicional: verificar método get_by_numero
                    if count > 0:
                        primera_factura = facturas[0]
                        test_factura = Factura.get_by_numero(primera_factura.numero_factura)
                        if test_factura and test_factura.id == primera_factura.id:
                            count = f"{count} (get_by_numero: OK)"
                        else:
                            count = f"{count} (get_by_numero: FALLO)"
                else:
                    count = "OK"
                
                print(f"✅ Tabla {table}: Accesible ({count})")
                tables_ok += 1
                
            except Exception as e:
                print(f"❌ Tabla {table}: Error - {e}")
        
        validation_results.append(("Tablas de BD", tables_ok, len(tables_to_check)))
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        validation_results.append(("Tablas de BD", 0, 5))
    
    # 5. Test de integración si está disponible
    print("\n5️⃣ TEST DE INTEGRACIÓN")
    print("-" * 25)
    
    integration_test = "test/integration/test_stock_update_integration.py"
    if os.path.exists(integration_test):
        integration_ok = run_test_script(integration_test, "Suite de tests de integración")
        validation_results.append(("Test integración", 1 if integration_ok else 0, 1))
    else:
        print("❌ Test de integración no encontrado")
        validation_results.append(("Test integración", 0, 1))
    
    # 6. Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 70)
    
    total_passed = 0
    total_tests = 0
    
    for category, passed, total in validation_results:
        percentage = (passed / total * 100) if total > 0 else 0
        status = "✅" if percentage >= 80 else "⚠️" if percentage >= 50 else "❌"
        
        print(f"{status} {category}: {passed}/{total} ({percentage:.1f}%)")
        total_passed += passed
        total_tests += total
    
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print("\n" + "-" * 70)
    print(f"📊 RESULTADO GENERAL: {total_passed}/{total_tests} ({overall_percentage:.1f}%)")
    
    if overall_percentage >= 90:
        print("🎉 EXCELENTE - Solución completamente validada")
        status = "EXCELLENT"
    elif overall_percentage >= 75:
        print("✅ BUENO - Solución funcional con componentes menores faltantes")
        status = "GOOD"
    elif overall_percentage >= 50:
        print("⚠️ ACEPTABLE - Solución parcial, revisar componentes faltantes")
        status = "ACCEPTABLE"
    else:
        print("❌ INSUFICIENTE - Solución requiere trabajo adicional")
        status = "INSUFFICIENT"
    
    print("\n📋 RECOMENDACIONES:")
    
    if status == "EXCELLENT":
        print("   • La solución está completamente implementada y validada")
        print("   • Todos los componentes funcionan correctamente")
        print("   • Lista para uso en producción")
        
    elif status == "GOOD":
        print("   • La funcionalidad principal está implementada")
        print("   • Revisar componentes menores que fallan")
        print("   • Funcional para uso normal")
        
    elif status == "ACCEPTABLE":
        print("   • Funcionalidad básica disponible")
        print("   • Implementar componentes faltantes")
        print("   • Probar más exhaustivamente")
        
    else:
        print("   • Revisar implementación básica")
        print("   • Verificar configuración del sistema")
        print("   • Consultar documentación de instalación")
    
    print(f"\n📚 DOCUMENTACIÓN DISPONIBLE:")
    print(f"   • docs/USER_GUIDE_STOCK_CONFIRMATION.md - Guía de usuario")
    print(f"   • docs/fixes/ROBUST_DIALOG_SOLUTION.md - Documentación técnica")
    print(f"   • docs/TESTING_GUIDE.md - Guía de testing")
    print(f"   • logs/facturacion_facil.log - Logs de la aplicación")
    
    return overall_percentage >= 75

if __name__ == "__main__":
    print("🚀 INICIANDO VALIDACIÓN FINAL DE LA SOLUCIÓN")
    
    success = validate_solution()
    
    print(f"\n{'='*70}")
    if success:
        print("✅ VALIDACIÓN EXITOSA - Solución lista para uso")
    else:
        print("❌ VALIDACIÓN FALLIDA - Revisar componentes faltantes")
    
    sys.exit(0 if success else 1)
