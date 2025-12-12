#!/usr/bin/env python3
"""
Script para corregir el problema de sincronización entre:
- productos.stock_actual (correcto)
- tabla stock (vacía)

Este script sincroniza la tabla stock con productos.stock_actual
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

from database.database import Database

def fix_stock_synchronization():
    """Sincronizar tabla stock con productos.stock_actual"""
    print("🔧 CORRECCIÓN: Sincronización de Stock")
    print("=" * 50)
    
    try:
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 1. Obtener todos los productos con su stock_actual
        print("📦 Obteniendo productos...")
        cursor.execute("SELECT id, nombre, stock_actual FROM productos")
        productos = cursor.fetchall()
        
        print(f"✅ Encontrados {len(productos)} productos")
        
        # 2. Verificar estado actual de la tabla stock
        print("\n📊 Estado actual tabla stock:")
        cursor.execute("SELECT COUNT(*) FROM stock")
        stock_count = cursor.fetchone()[0]
        print(f"   Registros en tabla stock: {stock_count}")
        
        # 3. Sincronizar cada producto
        print("\n🔄 Sincronizando...")
        productos_sincronizados = 0
        productos_creados = 0
        
        for producto_id, nombre, stock_actual in productos:
            stock_actual = stock_actual or 0  # Convertir None a 0
            
            # Verificar si existe registro en tabla stock
            cursor.execute("SELECT cantidad_disponible FROM stock WHERE producto_id = ?", (producto_id,))
            stock_record = cursor.fetchone()
            
            if stock_record:
                # Actualizar registro existente
                stock_disponible = stock_record[0]
                if stock_disponible != stock_actual:
                    cursor.execute("""
                        UPDATE stock 
                        SET cantidad_disponible = ?, fecha_actualizacion = CURRENT_TIMESTAMP
                        WHERE producto_id = ?
                    """, (stock_actual, producto_id))
                    print(f"   📝 Actualizado ID {producto_id}: {stock_disponible} → {stock_actual}")
                    productos_sincronizados += 1
                else:
                    print(f"   ✅ ID {producto_id}: Ya sincronizado ({stock_actual})")
            else:
                # Crear nuevo registro
                cursor.execute("""
                    INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (producto_id, stock_actual))
                print(f"   ➕ Creado ID {producto_id}: {stock_actual}")
                productos_creados += 1
        
        # 4. Confirmar cambios
        conn.commit()
        
        print(f"\n✅ SINCRONIZACIÓN COMPLETADA:")
        print(f"   📝 Productos actualizados: {productos_sincronizados}")
        print(f"   ➕ Productos creados: {productos_creados}")
        print(f"   📊 Total procesados: {len(productos)}")
        
        # 5. Verificar resultado
        print("\n🧪 VERIFICACIÓN:")
        print("-" * 30)
        
        from database.models import Stock
        
        for producto_id, nombre, stock_actual in productos:
            stock_actual = stock_actual or 0
            stock_from_table = Stock.get_by_product(producto_id)
            
            if stock_actual == stock_from_table:
                print(f"   ✅ ID {producto_id}: {stock_actual} = {stock_from_table}")
            else:
                print(f"   ❌ ID {producto_id}: {stock_actual} ≠ {stock_from_table}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")
        return False

def test_after_fix():
    """Probar que el problema está resuelto"""
    print("\n🧪 TEST POST-CORRECCIÓN")
    print("=" * 30)
    
    try:
        from database.models import Stock
        db = Database()
        productos = db.get_all_products()
        
        print("📋 Comparación productos.stock_actual vs Stock.get_by_product():")
        
        all_match = True
        for producto in productos:
            producto_id = producto['id']
            stock_actual = producto.get('stock_actual', 0)
            stock_from_table = Stock.get_by_product(producto_id)
            
            match = "✅" if stock_actual == stock_from_table else "❌"
            print(f"   {match} ID {producto_id}: {stock_actual} vs {stock_from_table}")
            
            if stock_actual != stock_from_table:
                all_match = False
        
        if all_match:
            print("\n🎉 PROBLEMA RESUELTO: Todos los stocks coinciden")
            print("💡 Ahora Stock.get_by_product() debería funcionar correctamente")
        else:
            print("\n⚠️  Aún hay inconsistencias")
        
        return all_match
        
    except Exception as e:
        print(f"❌ Error en test post-corrección: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO CORRECCIÓN DE STOCK")
    print("=" * 60)
    
    print("🎯 PROBLEMA IDENTIFICADO:")
    print("   - productos.stock_actual tiene valores correctos")
    print("   - tabla stock está vacía o desincronizada")
    print("   - Stock.get_by_product() retorna 0")
    print("   - Esto causa 'stock insuficiente disponible 0'")
    print()
    
    # Ejecutar corrección
    success = fix_stock_synchronization()
    
    if success:
        # Probar que funciona
        test_success = test_after_fix()
        
        print("\n" + "=" * 60)
        if test_success:
            print("🎉 CORRECCIÓN EXITOSA")
            print("\n💡 PRÓXIMOS PASOS:")
            print("   1. Ejecute: python main.py")
            print("   2. Vaya a: Gestión de Facturas → Crear Nueva Factura")
            print("   3. Intente agregar un producto")
            print("   4. Debería funcionar sin 'stock insuficiente'")
        else:
            print("⚠️  CORRECCIÓN PARCIAL - Revisar inconsistencias")
    else:
        print("❌ CORRECCIÓN FALLIDA")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
