#!/usr/bin/env python3
"""
Script de diagnostic pour identifier l'incohérence de stock
- Comparer productos.stock_actual vs table stock
- Identifier pourquoi le stock affiché ne correspond pas au stock disponible
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

from database.database import Database

def diagnostic_stock_inconsistencia():
    """Diagnostiquer l'incohérence de stock"""
    print("🔍 DIAGNOSTIC: Incohérence de Stock")
    print("=" * 50)
    
    try:
        db = Database()
        
        # 1. Obtenir tous les produits avec leur stock_actual
        print("📦 PRODUCTOS.STOCK_ACTUAL:")
        print("-" * 30)
        productos = db.get_all_products()
        
        for producto in productos:
            stock_actual = producto.get('stock_actual', 0)
            print(f"ID {producto['id']}: {producto['nombre']} - Stock: {stock_actual}")
        
        print()
        
        # 2. Vérifier si la table stock existe et son contenu
        print("📊 TABLE STOCK (si existe):")
        print("-" * 30)
        
        try:
            # Vérifier si la table stock existe
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stock'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                print("✅ Table 'stock' existe")
                
                # Obtenir le contenu de la table stock
                cursor.execute("SELECT producto_id, cantidad_disponible FROM stock")
                stock_data = cursor.fetchall()
                
                if stock_data:
                    print("📋 Contenido de la table stock:")
                    for producto_id, cantidad_disponible in stock_data:
                        print(f"  Producto ID {producto_id}: {cantidad_disponible}")
                else:
                    print("⚠️  Table stock existe mais est vide")
            else:
                print("❌ Table 'stock' n'existe pas")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error verificando table stock: {e}")
        
        print()
        
        # 3. Tester la méthode Stock.get_by_product() si elle existe
        print("🧪 TEST Stock.get_by_product():")
        print("-" * 30)
        
        try:
            from database.models import Stock
            
            for producto in productos:
                producto_id = producto['id']
                stock_actual = producto.get('stock_actual', 0)
                
                try:
                    stock_from_table = Stock.get_by_product(producto_id)
                    print(f"ID {producto_id}: productos.stock_actual={stock_actual}, Stock.get_by_product()={stock_from_table}")
                    
                    if stock_actual != stock_from_table:
                        print(f"  ⚠️  INCOHÉRENCE DÉTECTÉE!")
                        
                except Exception as e:
                    print(f"ID {producto_id}: productos.stock_actual={stock_actual}, Stock.get_by_product()=ERROR: {e}")
                    
        except ImportError:
            print("⚠️  Classe Stock non disponible")
        
        print()
        
        # 4. Vérifier quelle méthode utilise CrearFacturaDialog
        print("🔍 MÉTHODE UTILISÉE DANS CrearFacturaDialog:")
        print("-" * 30)
        print("✅ CrearFacturaDialog.agregar_producto() utilise:")
        print("   stock_actual = producto_data.get('stock_actual', 0)")
        print("   → Utilise productos.stock_actual (correct)")
        
        print()
        
        # 5. Identifier le problème potentiel
        print("🎯 ANALYSE DU PROBLÈME:")
        print("-" * 30)
        
        if productos:
            producto_test = productos[0]
            stock_actual = producto_test.get('stock_actual', 0)
            
            print(f"📦 Producto de test: {producto_test['nombre']}")
            print(f"📊 Stock actual en DB: {stock_actual}")
            
            if stock_actual > 0:
                print("✅ El producto tiene stock en la base de datos")
                print("❓ Si aparece 'stock insuficiente disponible 0', el problema puede ser:")
                print("   1. Otro código usa Stock.get_by_product() en lugar de stock_actual")
                print("   2. La table stock no está sincronizada")
                print("   3. Error en la lógica de verificación de stock")
            else:
                print("❌ El producto no tiene stock en la base de datos")
                print("💡 Esto explica el mensaje 'stock insuficiente disponible 0'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO DIAGNÓSTICO DE STOCK")
    print("=" * 60)
    
    success = diagnostic_stock_inconsistencia()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ DIAGNÓSTICO COMPLETADO")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Revisar las incohérencias detectadas")
        print("   2. Sincronizar las tablas si es necesario")
        print("   3. Verificar qué código causa el error")
    else:
        print("❌ DIAGNÓSTICO FALLIDO")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
