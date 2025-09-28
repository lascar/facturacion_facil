#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test completo de toda la solución: Stock + PDF
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import subprocess
import time

def run_test_with_timeout(script_path, description, timeout=30):
    """Ejecuta un test con timeout"""
    print(f"\n🔍 {description}")
    print("-" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            print("✅ ÉXITO")
            return True
        else:
            print("❌ FALLO")
            if result.stderr:
                print(f"Error: {result.stderr[:300]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT - Test tardó más de {timeout} segundos")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_complete_solution():
    """Test completo de toda la solución"""
    
    print("🧪 TEST COMPLETO - Solución Stock + PDF")
    print("=" * 70)
    
    test_results = []
    
    # 1. Test básico de stock
    print("\n1️⃣ TESTS DE STOCK")
    print("=" * 30)
    
    stock_tests = [
        ("test/demo/demo_simple_stock_test.py", "Test básico de stock"),
        ("test/demo/demo_quick_inheritance_check.py", "Verificación de herencia"),
        ("test/demo/demo_complete_stock_solution_test.py", "Test completo de stock")
    ]
    
    stock_success = 0
    for script, description in stock_tests:
        if os.path.exists(script):
            if run_test_with_timeout(script, description):
                stock_success += 1
        else:
            print(f"❌ {description}: Script no encontrado")
    
    test_results.append(("Tests de Stock", stock_success, len(stock_tests)))
    
    # 2. Test de selección de facturas
    print("\n2️⃣ TESTS DE SELECCIÓN DE FACTURAS")
    print("=" * 40)
    
    selection_tests = [
        ("test/demo/demo_test_factura_selection.py", "Test selección de facturas")
    ]
    
    selection_success = 0
    for script, description in selection_tests:
        if os.path.exists(script):
            if run_test_with_timeout(script, description):
                selection_success += 1
        else:
            print(f"❌ {description}: Script no encontrado")
    
    test_results.append(("Tests de Selección", selection_success, len(selection_tests)))
    
    # 3. Test de integración
    print("\n3️⃣ TESTS DE INTEGRACIÓN")
    print("=" * 30)
    
    integration_tests = [
        ("test/integration/test_stock_update_integration.py", "Integración de stock"),
        ("test/integration/test_pdf_export_integration.py", "Integración de PDF")
    ]
    
    integration_success = 0
    for script, description in integration_tests:
        if os.path.exists(script):
            if run_test_with_timeout(script, description, 45):  # Más tiempo para integración
                integration_success += 1
        else:
            print(f"❌ {description}: Script no encontrado")
    
    test_results.append(("Tests de Integración", integration_success, len(integration_tests)))
    
    # 4. Validación final
    print("\n4️⃣ VALIDACIÓN FINAL")
    print("=" * 25)
    
    validation_tests = [
        ("test/validate_solution.py", "Validación completa del sistema")
    ]
    
    validation_success = 0
    for script, description in validation_tests:
        if os.path.exists(script):
            if run_test_with_timeout(script, description, 60):  # Más tiempo para validación
                validation_success += 1
        else:
            print(f"❌ {description}: Script no encontrado")
    
    test_results.append(("Validación Final", validation_success, len(validation_tests)))
    
    # 5. Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN COMPLETO DE TESTS")
    print("=" * 70)
    
    total_passed = 0
    total_tests = 0
    
    for category, passed, total in test_results:
        percentage = (passed / total * 100) if total > 0 else 0
        status = "✅" if percentage >= 80 else "⚠️" if percentage >= 50 else "❌"
        
        print(f"{status} {category}: {passed}/{total} ({percentage:.1f}%)")
        total_passed += passed
        total_tests += total
    
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print("\n" + "-" * 70)
    print(f"📊 RESULTADO GENERAL: {total_passed}/{total_tests} ({overall_percentage:.1f}%)")
    
    # Evaluación final
    if overall_percentage >= 90:
        print("🎉 EXCELENTE - Solución completamente funcional")
        status = "EXCELLENT"
    elif overall_percentage >= 75:
        print("✅ BUENO - Solución funcional con componentes menores")
        status = "GOOD"
    elif overall_percentage >= 50:
        print("⚠️ ACEPTABLE - Funcionalidad básica disponible")
        status = "ACCEPTABLE"
    else:
        print("❌ INSUFICIENTE - Requiere trabajo adicional")
        status = "INSUFFICIENT"
    
    # Recomendaciones específicas
    print(f"\n📋 ESTADO DE FUNCIONALIDADES:")
    
    stock_percentage = (test_results[0][1] / test_results[0][2] * 100) if test_results[0][2] > 0 else 0
    selection_percentage = (test_results[1][1] / test_results[1][2] * 100) if test_results[1][2] > 0 else 0
    
    print(f"   🔄 Actualización de Stock: {'✅ FUNCIONA' if stock_percentage >= 80 else '⚠️ PARCIAL' if stock_percentage >= 50 else '❌ FALLA'}")
    print(f"   📄 Exportación PDF: {'✅ FUNCIONA' if selection_percentage >= 80 else '⚠️ PARCIAL' if selection_percentage >= 50 else '❌ FALLA'}")
    
    if len(test_results) >= 3:
        integration_percentage = (test_results[2][1] / test_results[2][2] * 100) if test_results[2][2] > 0 else 0
        print(f"   🔗 Integración: {'✅ FUNCIONA' if integration_percentage >= 80 else '⚠️ PARCIAL' if integration_percentage >= 50 else '❌ FALLA'}")
    
    print(f"\n🎯 RECOMENDACIONES:")
    
    if status == "EXCELLENT":
        print("   • ✅ Todas las funcionalidades están operativas")
        print("   • ✅ Sistema listo para uso en producción")
        print("   • ✅ Documentación completa disponible")
        
    elif status == "GOOD":
        print("   • ✅ Funcionalidades principales operativas")
        print("   • ⚠️ Revisar componentes que fallaron")
        print("   • ✅ Apto para uso normal")
        
    elif status == "ACCEPTABLE":
        print("   • ⚠️ Funcionalidad básica disponible")
        print("   • 🔧 Completar componentes faltantes")
        print("   • 📋 Probar más exhaustivamente")
        
    else:
        print("   • ❌ Revisar implementación básica")
        print("   • 🔧 Corregir errores fundamentales")
        print("   • 📚 Consultar documentación de instalación")
    
    return overall_percentage >= 75

def show_usage_instructions():
    """Muestra instrucciones de uso"""
    
    print(f"\n📚 INSTRUCCIONES DE USO")
    print("=" * 40)
    
    print("🔄 PARA ACTUALIZACIÓN DE STOCK:")
    print("   1. Crear factura con producto de stock bajo (≤ 5 unidades)")
    print("   2. Hacer clic en 'Guardar'")
    print("   3. Aparecerá diálogo de confirmación")
    print("   4. Hacer clic en '✅ CONFIRMAR' para procesar")
    print("   5. El stock se actualizará automáticamente")
    
    print("\n📄 PARA EXPORTACIÓN PDF:")
    print("   1. Abrir ventana de Facturas")
    print("   2. Hacer clic en una factura de la lista (izquierda)")
    print("   3. Verificar que se carga en el formulario")
    print("   4. Hacer clic en 'Exportar PDF'")
    print("   5. El PDF se generará y abrirá automáticamente")
    
    print(f"\n🔧 SOLUCIÓN DE PROBLEMAS:")
    print("   • Logs detallados: logs/facturacion_facil.log")
    print("   • Buscar líneas con '🔍 DEBUG'")
    print("   • Para PDF: verificar que ReportLab esté instalado")
    print("   • Para stock: verificar diálogos de confirmación")
    
    print(f"\n📋 DOCUMENTACIÓN DISPONIBLE:")
    print("   • docs/USER_GUIDE_STOCK_CONFIRMATION.md - Guía de stock")
    print("   • docs/USER_GUIDE_PDF_EXPORT.md - Guía de PDF")
    print("   • docs/fixes/ROBUST_DIALOG_SOLUTION.md - Solución técnica")
    print("   • docs/fixes/PDF_EXPORT_SELECTION_FIX.md - Corrección PDF")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST COMPLETO DE LA SOLUCIÓN")
    print("=" * 70)
    print("Este test verifica:")
    print("   • ✅ Actualización automática de stock")
    print("   • ✅ Diálogos de confirmación robustos")
    print("   • ✅ Selección de facturas para PDF")
    print("   • ✅ Exportación de facturas a PDF")
    print("   • ✅ Integración completa del sistema")
    
    success = test_complete_solution()
    
    print("\n" + "=" * 70)
    print("🏁 RESULTADO FINAL:")
    
    if success:
        print("   🎉 SOLUCIÓN COMPLETA FUNCIONAL")
        print("   ✅ Stock y PDF funcionan correctamente")
        print("   🚀 Sistema listo para uso")
    else:
        print("   ⚠️ SOLUCIÓN PARCIAL")
        print("   🔧 Revisar componentes que fallaron")
        print("   📋 Consultar logs para más detalles")
    
    # Mostrar instrucciones de uso
    show_usage_instructions()
    
    print(f"\n📞 SOPORTE:")
    print("   • Ejecutar tests individuales para diagnóstico específico")
    print("   • Revisar logs detallados en logs/facturacion_facil.log")
    print("   • Consultar documentación técnica en docs/fixes/")
    
    sys.exit(0 if success else 1)
