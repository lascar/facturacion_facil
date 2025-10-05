#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de la sélection de factura et exportation PDF
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database import db
from database.models import Factura, FacturaItem, Producto, Stock
from utils.logger import get_logger

def demo_factura_selection():
    """Test de la sélection de factura"""
    
    print("🧪 TEST - Sélection de Factura et Exportation PDF")
    print("=" * 60)
    
    # Initialiser la base de données
    db.init_database()
    logger = get_logger("test_factura_selection")
    
    try:
        print("1️⃣ Vérification des facturas existantes...")
        
        # Obtenir toutes les facturas
        facturas = Factura.get_all()
        print(f"   📊 Facturas en base de datos: {len(facturas)}")
        
        if len(facturas) == 0:
            print("   ⚠️ No hay facturas en la base de datos")
            print("   💡 Crear al menos una factura para probar la exportación PDF")
            return False
        
        # Mostrar las primeras facturas
        print("   📋 Primeras facturas disponibles:")
        for i, factura in enumerate(facturas[:5], 1):
            print(f"      {i}. {factura.numero_factura} - {factura.nombre_cliente} - €{factura.total_factura:.2f}")
        
        print("\n2️⃣ Test de la méthode get_by_numero...")
        
        # Tester la méthode get_by_numero avec la première factura
        primera_factura = facturas[0]
        numero_test = primera_factura.numero_factura
        
        print(f"   🔍 Buscando factura con número: {numero_test}")
        
        # Test de la méthode
        factura_encontrada = Factura.get_by_numero(numero_test)
        
        if factura_encontrada:
            print(f"   ✅ Factura encontrada:")
            print(f"      ID: {factura_encontrada.id}")
            print(f"      Número: {factura_encontrada.numero_factura}")
            print(f"      Cliente: {factura_encontrada.nombre_cliente}")
            print(f"      Total: €{factura_encontrada.total_factura:.2f}")
            print(f"      Items: {len(factura_encontrada.items)} productos")
            
            # Vérifier que c'est la même factura
            if factura_encontrada.id == primera_factura.id:
                print("   ✅ La factura encontrada coincide con la original")
            else:
                print("   ❌ ERROR: La factura encontrada NO coincide con la original")
                return False
                
        else:
            print(f"   ❌ ERROR: No se encontró la factura con número {numero_test}")
            return False
        
        print("\n3️⃣ Test de simulación de sélection...")
        
        # Simuler la sélection comme dans l'interface
        class MockFacturasWindow:
            def __init__(self):
                self.logger = logger
                self.selected_factura = None
            
            def simulate_selection(self, numero_factura):
                """Simule la sélection d'une factura"""
                print(f"   🔄 Simulando selección de factura: {numero_factura}")
                
                # Buscar la factura (como en on_factura_select)
                self.selected_factura = Factura.get_by_numero(numero_factura)
                
                if self.selected_factura:
                    print(f"   ✅ Factura seleccionada: {self.selected_factura.numero_factura}")
                    print(f"      Cliente: {self.selected_factura.nombre_cliente}")
                    print(f"      Items: {len(self.selected_factura.items)}")
                    return True
                else:
                    print(f"   ❌ No se pudo seleccionar la factura")
                    return False
            
            def check_pdf_export_ready(self):
                """Verifica si está listo para exportar PDF"""
                print(f"   🔍 Verificando estado para exportación PDF...")
                print(f"      selected_factura: {self.selected_factura is not None}")
                
                if self.selected_factura:
                    print(f"      Número: {self.selected_factura.numero_factura}")
                    print(f"      ID: {self.selected_factura.id}")
                    print(f"      Items: {len(self.selected_factura.items)}")
                    print(f"   ✅ Listo para exportar PDF")
                    return True
                else:
                    print(f"   ❌ NO listo para exportar PDF - No hay factura seleccionada")
                    return False
        
        # Crear instancia mock
        mock_window = MockFacturasWindow()
        
        # Simular sélection
        selection_success = mock_window.simulate_selection(numero_test)
        
        if selection_success:
            # Verificar estado para PDF
            pdf_ready = mock_window.check_pdf_export_ready()
            
            if pdf_ready:
                print("   ✅ Simulación de selección exitosa")
                print("   ✅ Estado correcto para exportación PDF")
            else:
                print("   ❌ ERROR: Estado incorrecto para exportación PDF")
                return False
        else:
            print("   ❌ ERROR: Simulación de selección falló")
            return False
        
        print("\n4️⃣ Test con múltiples facturas...")
        
        # Tester avec plusieurs facturas
        test_count = min(3, len(facturas))
        success_count = 0
        
        for i in range(test_count):
            factura = facturas[i]
            print(f"   🔍 Test {i+1}: {factura.numero_factura}")
            
            found = Factura.get_by_numero(factura.numero_factura)
            if found and found.id == factura.id:
                print(f"      ✅ OK")
                success_count += 1
            else:
                print(f"      ❌ FALLO")
        
        print(f"   📊 Resultado: {success_count}/{test_count} tests exitosos")
        
        if success_count == test_count:
            print("   ✅ Todos los tests de búsqueda exitosos")
        else:
            print("   ❌ Algunos tests de búsqueda fallaron")
            return False
        
        print("\n5️⃣ Verificación de datos de factura...")
        
        # Verificar que la factura tiene todos los datos necesarios para PDF
        factura_test = facturas[0]
        
        print(f"   📋 Verificando datos de: {factura_test.numero_factura}")
        
        required_fields = [
            ('numero_factura', factura_test.numero_factura),
            ('nombre_cliente', factura_test.nombre_cliente),
            ('fecha_factura', factura_test.fecha_factura),
            ('total_factura', factura_test.total_factura),
            ('items', factura_test.items)
        ]
        
        all_fields_ok = True
        for field_name, field_value in required_fields:
            if field_value is None or (isinstance(field_value, list) and len(field_value) == 0):
                print(f"      ❌ {field_name}: Vacío o None")
                all_fields_ok = False
            else:
                if field_name == 'items':
                    print(f"      ✅ {field_name}: {len(field_value)} items")
                else:
                    print(f"      ✅ {field_name}: {field_value}")
        
        if all_fields_ok:
            print("   ✅ Todos los campos requeridos están presentes")
        else:
            print("   ⚠️ Algunos campos están vacíos - puede afectar la generación de PDF")
        
        print("\n" + "=" * 60)
        print("📊 RESUMEN DEL TEST:")
        print(f"   Facturas disponibles: ✅ {len(facturas)}")
        print(f"   Método get_by_numero: ✅ Funciona")
        print(f"   Simulación selección: ✅ Exitosa")
        print(f"   Estado para PDF: ✅ Correcto")
        print(f"   Datos completos: {'✅ Sí' if all_fields_ok else '⚠️ Parcial'}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_pdf_export_instructions():
    """Muestra instrucciones para la exportación PDF"""
    
    print("\n📚 INSTRUCCIONES PARA EXPORTACIÓN PDF")
    print("=" * 50)
    
    print("🎯 PASOS PARA EXPORTAR PDF:")
    print("1. Abrir la ventana de Facturas")
    print("2. En la lista de la izquierda, hacer clic en una factura")
    print("3. La factura se cargará automáticamente en el formulario")
    print("4. Hacer clic en el botón 'Exportar PDF'")
    print("5. El PDF se generará y abrirá automáticamente")
    
    print("\n🔍 DIAGNÓSTICO SI NO FUNCIONA:")
    print("• Verificar que aparezcan logs como:")
    print("  '🔍 DEBUG: Buscando factura con número: ...'")
    print("  '🔍 DEBUG: Factura encontrada: True'")
    print("  '🔍 DEBUG PDF: selected_factura = <Factura object>'")
    
    print("\n⚠️ POSIBLES PROBLEMAS:")
    print("• Si selected_factura es None:")
    print("  - La factura no se seleccionó correctamente")
    print("  - Problema en el método get_by_numero")
    print("  - Error en on_factura_select")
    
    print("• Si aparece el mensaje de 'Seleccione una factura':")
    print("  - La variable selected_factura no se está estableciendo")
    print("  - Verificar los logs de selección")
    
    print("\n📋 LOGS IMPORTANTES:")
    print("• logs/facturacion_facil.log")
    print("• Buscar líneas con '🔍 DEBUG'")
    print("• Verificar errores durante la selección")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST DE SELECCIÓN DE FACTURA")
    print("=" * 70)
    
    success = demo_factura_selection()
    
    if success:
        print("\n✅ TEST EXITOSO")
        print("🎉 La selección de facturas funciona correctamente")
        print("🔧 Si el PDF no funciona, revisar logs durante el uso real")
    else:
        print("\n❌ TEST FALLIDO")
        print("🔧 Hay problemas con la selección de facturas")
        print("📋 Revisar los errores mostrados arriba")
    
    # Mostrar instrucciones
    show_pdf_export_instructions()
    
    print("\n📚 PRÓXIMOS PASOS:")
    if success:
        print("1. Probar la exportación PDF en la aplicación real")
        print("2. Revisar logs durante la selección y exportación")
        print("3. Verificar que ReportLab esté instalado si hay errores de PDF")
    else:
        print("1. Corregir los problemas de selección identificados")
        print("2. Volver a ejecutar este test")
        print("3. Luego probar en la aplicación real")
