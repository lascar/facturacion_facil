#!/usr/bin/env python3
"""
Test final para verificar que el problema de stock está completamente resuelto
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

from database.database import Database
from database.models import Stock

def test_stock_problema_resuelto():
    """Test completo del problema de stock resuelto"""
    print("🧪 TEST FINAL: Problema de Stock Resuelto")
    print("=" * 50)
    
    try:
        db = Database()
        productos = db.get_all_products()
        
        print(f"📦 Productos disponibles: {len(productos)}")
        print()
        
        # Test 1: Verificar que ambos métodos retornan lo mismo
        print("🔍 TEST 1: Consistencia de métodos")
        print("-" * 30)
        
        all_consistent = True
        productos_con_stock = []
        
        for producto in productos:
            producto_id = producto['id']
            nombre = producto['nombre']
            stock_actual = producto.get('stock_actual', 0)
            stock_from_table = Stock.get_by_product(producto_id)
            
            consistent = stock_actual == stock_from_table
            status = "✅" if consistent else "❌"
            
            print(f"{status} {nombre} (ID {producto_id}):")
            print(f"   productos.stock_actual: {stock_actual}")
            print(f"   Stock.get_by_product(): {stock_from_table}")
            
            if not consistent:
                all_consistent = False
            
            if stock_actual > 0:
                productos_con_stock.append(producto)
        
        print(f"\n📊 Resultado: {'✅ CONSISTENTE' if all_consistent else '❌ INCONSISTENTE'}")
        
        # Test 2: Simular agregar producto con stock
        print(f"\n🎯 TEST 2: Simulación agregar producto")
        print("-" * 30)
        
        if productos_con_stock:
            producto_test = productos_con_stock[0]
            producto_id = producto_test['id']
            nombre = producto_test['nombre']
            stock_disponible = producto_test.get('stock_actual', 0)
            
            print(f"📦 Producto de prueba: {nombre}")
            print(f"📊 Stock disponible: {stock_disponible}")
            
            # Simular verificación como en CrearFacturaDialog.agregar_producto()
            cantidad_solicitada = 1
            
            print(f"\n🔍 Verificación método CrearFacturaDialog:")
            print(f"   cantidad_solicitada = {cantidad_solicitada}")
            print(f"   stock_actual = producto_data.get('stock_actual', 0) = {stock_disponible}")
            
            if cantidad_solicitada <= stock_disponible:
                print("   ✅ VERIFICACIÓN PASADA - Puede agregar producto")
            else:
                print("   ❌ VERIFICACIÓN FALLIDA - Stock insuficiente")
            
            # Simular verificación como en otros métodos que usan Stock.get_by_product()
            print(f"\n🔍 Verificación método Stock.get_by_product():")
            stock_from_table = Stock.get_by_product(producto_id)
            print(f"   Stock.get_by_product({producto_id}) = {stock_from_table}")
            
            if cantidad_solicitada <= stock_from_table:
                print("   ✅ VERIFICACIÓN PASADA - Puede agregar producto")
            else:
                print("   ❌ VERIFICACIÓN FALLIDA - Stock insuficiente")
            
            # Resultado final
            both_pass = (cantidad_solicitada <= stock_disponible) and (cantidad_solicitada <= stock_from_table)
            print(f"\n🎯 RESULTADO FINAL: {'✅ AMBOS MÉTODOS PASAN' if both_pass else '❌ INCONSISTENCIA'}")
            
        else:
            print("⚠️  No hay productos con stock para probar")
        
        # Test 3: Verificar formato de combo
        print(f"\n📋 TEST 3: Formato combo productos")
        print("-" * 30)
        
        print("🎯 Formato esperado en dropdown:")
        for producto in productos:
            stock = producto.get('stock_actual', 0)
            precio = producto.get('precio_venta', 0)
            formato = f"{producto['nombre']} - {precio:.2f}€ (Stock: {stock})"
            print(f"   {formato}")
        
        return all_consistent and len(productos_con_stock) > 0
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN FINAL DEL PROBLEMA DE STOCK")
    print("=" * 60)
    
    print("📋 PROBLEMA ORIGINAL:")
    print("   'nueva factura agregar un producto (stock 10) => stock insuficiente disponible 0'")
    print()
    
    print("🔧 CORRECCIÓN APLICADA:")
    print("   - Sincronizada tabla stock con productos.stock_actual")
    print("   - Stock.get_by_product() ahora retorna valores correctos")
    print()
    
    success = test_stock_problema_resuelto()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 PROBLEMA COMPLETAMENTE RESUELTO")
        print("\n✅ CONFIRMACIÓN:")
        print("   - Ambos métodos de verificación de stock son consistentes")
        print("   - Productos con stock están disponibles")
        print("   - No debería aparecer más 'stock insuficiente disponible 0'")
        print("\n🚀 PRUEBA MANUAL:")
        print("   1. Ejecute: python main.py")
        print("   2. Vaya a: Gestión de Facturas → Crear Nueva Factura")
        print("   3. Seleccione un producto con stock > 0")
        print("   4. Intente agregarlo con cantidad = 1")
        print("   5. Debería agregarse sin errores")
    else:
        print("⚠️  PROBLEMA PARCIALMENTE RESUELTO")
        print("   Revisar inconsistencias detectadas arriba")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
