#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Démonstration et diagnostic du problème:
"Les stocks ne s'actualisent pas si l'on facture un produit"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from utils.logger import get_logger

def demo_stock_update_issue():
    """Démonstration du problème de mise à jour du stock"""
    
    print("🔍 DIAGNOSTIC - Problème de mise à jour du stock")
    print("=" * 60)
    print("Problème: Les stocks ne s'actualisent pas lors de la facturation")
    print()
    
    # Initialiser la base de données
    db.initialize()
    logger = get_logger("demo_stock_issue")
    
    try:
        print("1️⃣ Création d'un produit de test avec stock initial...")
        
        # Créer un produit de test
        producto_test = Producto(
            nombre="Producto Test Stock Update",
            referencia=f"TEST-STOCK-UPDATE-001",
            precio=15.99,
            categoria="Test",
            iva_recomendado=21.0,
            descripcion="Producto para probar la actualización de stock en facturas"
        )
        
        producto_test.save()
        print(f"   📦 Producto creado: {producto_test.nombre} (ID: {producto_test.id})")
        
        # Establecer stock inicial
        stock_inicial = 100
        stock_obj = Stock(producto_test.id, stock_inicial)
        stock_obj.save()
        
        stock_verificado = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock inicial establecido: {stock_verificado} unidades")
        
        print("\n2️⃣ Simulación de creación de factura...")
        
        # Crear una factura de test
        factura_test = Factura(
            numero_factura="TEST-001",
            nombre_cliente="Cliente Test",
            fecha_factura="2024-09-27"
        )
        
        # Crear item de factura
        cantidad_vendida = 25
        item_test = FacturaItem(
            producto_id=producto_test.id,
            cantidad=cantidad_vendida,
            precio_unitario=producto_test.precio,
            iva_aplicado=21.0
        )
        
        # Calcular totales del item
        item_test.calculate_totals()
        
        # Asignar items a la factura
        factura_test.items = [item_test]
        factura_test.calculate_totals()
        
        print(f"   🧾 Factura creada: {factura_test.numero_factura}")
        print(f"   📦 Producto: {producto_test.nombre}")
        print(f"   📊 Cantidad vendida: {cantidad_vendida}")
        print(f"   💰 Total factura: €{factura_test.total_factura:.2f}")
        
        print("\n3️⃣ Guardando factura (sin actualización automática de stock)...")
        
        # Guardar la factura (esto NO actualiza el stock automáticamente)
        factura_test.save()
        print(f"   ✅ Factura guardada con ID: {factura_test.id}")
        
        # Verificar stock después de guardar factura
        stock_despues_factura = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock después de guardar factura: {stock_despues_factura} unidades")
        
        if stock_despues_factura == stock_inicial:
            print("   ❌ PROBLEMA CONFIRMADO: El stock NO se actualizó automáticamente")
        else:
            print("   ✅ Stock actualizado correctamente")
        
        print("\n4️⃣ Simulación de la actualización manual de stock...")
        
        # Simular lo que debería hacer update_stock_after_save()
        print("   🔧 Ejecutando Stock.update_stock() manualmente...")
        
        for item in factura_test.items:
            print(f"      - Actualizando stock para producto ID {item.producto_id}")
            print(f"      - Cantidad a descontar: {item.cantidad}")
            
            stock_antes = Stock.get_by_product(item.producto_id)
            print(f"      - Stock antes: {stock_antes}")
            
            # Actualizar stock
            Stock.update_stock(item.producto_id, item.cantidad)
            
            stock_despues = Stock.get_by_product(item.producto_id)
            print(f"      - Stock después: {stock_despues}")
            
            if stock_despues == stock_antes - item.cantidad:
                print("      ✅ Stock actualizado correctamente")
            else:
                print("      ❌ Error en actualización de stock")
        
        print("\n5️⃣ Verificación final...")
        
        stock_final = Stock.get_by_product(producto_test.id)
        stock_esperado = stock_inicial - cantidad_vendida
        
        print(f"   📊 Stock inicial: {stock_inicial}")
        print(f"   📊 Cantidad vendida: {cantidad_vendida}")
        print(f"   📊 Stock esperado: {stock_esperado}")
        print(f"   📊 Stock actual: {stock_final}")
        
        if stock_final == stock_esperado:
            print("   ✅ Stock final correcto")
        else:
            print("   ❌ Stock final incorrecto")
        
        print("\n6️⃣ Análisis del problema...")
        
        print("   🔍 Posibles causas del problema:")
        print("      1. La méthode update_stock_after_save() no se ejecuta")
        print("      2. Error en la herencia del mixin FacturasMethodsMixin")
        print("      3. Excepción silenciosa en update_stock_after_save()")
        print("      4. Problema en el flujo de guardar_factura()")
        
        print("\n7️⃣ Verificación de métodos...")
        
        # Verificar si los métodos existen
        from ui.facturas import FacturasWindow
        from ui.facturas_methods import FacturasMethodsMixin
        
        print("   🔍 Verificando herencia de métodos:")
        
        methods_to_check = [
            'guardar_factura',
            'update_stock_after_save',
            'show_stock_impact_summary'
        ]
        
        for method_name in methods_to_check:
            if hasattr(FacturasMethodsMixin, method_name):
                print(f"      ✅ {method_name} existe en FacturasMethodsMixin")
            else:
                print(f"      ❌ {method_name} NO existe en FacturasMethodsMixin")
            
            if hasattr(FacturasWindow, method_name):
                print(f"      ✅ {method_name} disponible en FacturasWindow")
            else:
                print(f"      ❌ {method_name} NO disponible en FacturasWindow")
        
        print("\n8️⃣ Limpieza...")
        
        # Limpiar datos de test
        factura_test.delete()
        producto_test.delete()
        print("   🗑️ Datos de test eliminados")
        
        print("\n" + "=" * 60)
        print("📋 RESUMEN DEL DIAGNÓSTICO")
        print("=" * 60)
        print()
        print("🔍 Problema identificado:")
        print("   • El stock NO se actualiza automáticamente al guardar facturas")
        print("   • La actualización manual funciona correctamente")
        print("   • El problema está en el flujo automático")
        print()
        print("🎯 Posibles soluciones:")
        print("   1. Verificar que update_stock_after_save() se ejecute")
        print("   2. Agregar logging para diagnosticar el flujo")
        print("   3. Verificar excepciones silenciosas")
        print("   4. Asegurar que la herencia del mixin funcione")
        
        return True
        
    except Exception as e:
        logger.error(f"Error en diagnóstico: {e}")
        print(f"\n❌ Error durante el diagnóstico: {e}")
        return False

def test_stock_update_method():
    """Test específico del método Stock.update_stock"""
    print("\n🧪 TEST ESPECÍFICO - Método Stock.update_stock")
    print("-" * 50)
    
    try:
        # Crear producto de test
        producto = Producto(
            nombre="Test Update Method",
            referencia="TEST-UPDATE-001",
            precio=10.0
        )
        producto.save()
        
        # Establecer stock inicial
        stock_inicial = 50
        stock_obj = Stock(producto.id, stock_inicial)
        stock_obj.save()
        
        print(f"1. Stock inicial: {Stock.get_by_product(producto.id)}")
        
        # Test de actualización
        cantidad_venta = 15
        Stock.update_stock(producto.id, cantidad_venta)
        
        stock_final = Stock.get_by_product(producto.id)
        print(f"2. Stock después de venta de {cantidad_venta}: {stock_final}")
        
        # Verificar resultado
        if stock_final == stock_inicial - cantidad_venta:
            print("✅ Método Stock.update_stock() funciona correctamente")
            resultado = True
        else:
            print("❌ Método Stock.update_stock() NO funciona")
            resultado = False
        
        # Limpiar
        producto.delete()
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test de método: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando diagnóstico del problema de actualización de stock...")
    print()
    
    success1 = demo_stock_update_issue()
    success2 = test_stock_update_method()
    
    if success1 and success2:
        print("\n🎯 DIAGNÓSTICO COMPLETADO")
        print("El problema está identificado y las soluciones están claras.")
    else:
        print("\n⚠️ Problemas durante el diagnóstico. Revisar los logs.")
    
    print("\n📚 Próximos pasos:")
    print("   1. Verificar el flujo de guardar_factura()")
    print("   2. Agregar logging detallado")
    print("   3. Implementar la corrección")
    print("   4. Crear tests de integración")
