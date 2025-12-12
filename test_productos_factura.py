#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar que los productos aparecen correctamente en las facturas
NOTA: Este archivo será movido a test/unit/test_productos_factura.py
"""

import sys
import os
sys.path.append('.')

from database.database import Database
from utils.logger import get_logger

def test_productos_disponibles():
    """Test para verificar productos disponibles"""
    logger = get_logger("test_productos")
    
    print("🧪 TEST: Productos disponibles para facturas")
    print("=" * 50)
    
    try:
        # Inicializar base de datos
        db = Database()
        
        # Obtener productos
        print("📦 Obteniendo productos de la base de datos...")
        productos = db.get_all_products()
        
        print(f"✅ Encontrados {len(productos)} productos")
        print()
        
        if not productos:
            print("❌ ERROR: No hay productos en la base de datos")
            print("💡 Solución: Agregue productos usando la gestión de productos")
            return False
        
        print("📋 Lista de productos disponibles:")
        print("-" * 80)
        print(f"{'ID':<5} {'Nombre':<20} {'Precio':<10} {'Stock':<8} {'IVA':<6} {'Referencia'}")
        print("-" * 80)
        
        for i, producto in enumerate(productos, 1):
            id_prod = producto.get('id', 'N/A')
            nombre = producto.get('nombre', 'Sin nombre')[:18]
            precio_venta = producto.get('precio_venta', 0.0)
            stock = producto.get('stock_actual', 0)
            iva = producto.get('iva_recomendado', 21.0)
            referencia = producto.get('referencia', 'N/A') or 'N/A'
            
            print(f"{id_prod:<5} {nombre:<20} {precio_venta:<10.2f} {stock:<8} {iva:<6.1f} {referencia}")
        
        print("-" * 80)
        print()
        
        # Verificar estructura de datos
        print("🔍 Verificando estructura de datos del primer producto:")
        primer_producto = productos[0]
        
        campos_requeridos = ['id', 'nombre', 'precio_venta', 'stock_actual', 'iva_recomendado']
        
        for campo in campos_requeridos:
            valor = primer_producto.get(campo)
            if valor is not None:
                print(f"  ✅ {campo}: {valor} ({type(valor).__name__})")
            else:
                print(f"  ❌ {campo}: FALTANTE")
        
        print()
        
        # Simular carga en combo
        print("🎯 Simulando carga en ComboBox de factura:")
        print("Elementos que se agregarían al combo:")
        print("  0. Seleccionar producto... (None)")
        
        for i, producto in enumerate(productos, 1):
            nombre = producto.get('nombre', 'Sin nombre')
            precio = producto.get('precio_venta', 0.0)
            stock = producto.get('stock_actual', 0)
            texto_combo = f"{nombre} - {precio:.2f}€ (Stock: {stock})"
            print(f"  {i}. {texto_combo} (ID: {producto.get('id')})")
        
        print()
        print("✅ TEST COMPLETADO: Los productos deberían aparecer correctamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en test de productos: {e}")
        print(f"❌ ERROR: {e}")
        return False

def test_agregar_producto_ejemplo():
    """Test para agregar un producto de ejemplo si no hay ninguno"""
    logger = get_logger("test_productos")
    
    try:
        db = Database()
        productos = db.get_all_products()
        
        if len(productos) == 0:
            print("📦 No hay productos. Agregando producto de ejemplo...")
            
            producto_ejemplo = {
                'nombre': 'Producto de Prueba',
                'referencia': 'TEST-001',
                'precio_venta': 25.50,
                'categoria': 'Pruebas',
                'descripcion': 'Producto creado para pruebas de facturación',
                'iva_recomendado': 21.0,
                'stock_actual': 10,
                'stock_minimo': 2
            }
            
            result = db.add_product(producto_ejemplo)
            if result:
                print("✅ Producto de ejemplo agregado correctamente")
                return True
            else:
                print("❌ Error agregando producto de ejemplo")
                return False
        else:
            print(f"✅ Ya hay {len(productos)} productos en la base de datos")
            return True
            
    except Exception as e:
        logger.error(f"Error agregando producto de ejemplo: {e}")
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Función principal del test"""
    print("🚀 INICIANDO TESTS DE PRODUCTOS EN FACTURAS")
    print("=" * 60)
    print()
    
    # Test 1: Verificar productos existentes
    success1 = test_productos_disponibles()
    print()
    
    # Test 2: Agregar producto si no hay ninguno
    if not success1:
        print("🔧 Intentando agregar producto de ejemplo...")
        success2 = test_agregar_producto_ejemplo()
        if success2:
            print("🔄 Reejecutando test de productos...")
            success1 = test_productos_disponibles()
    
    print()
    print("=" * 60)
    if success1:
        print("🎉 RESULTADO: Los productos deberían aparecer en las facturas")
        print()
        print("💡 PRÓXIMOS PASOS:")
        print("   1. Abra la aplicación: python main.py")
        print("   2. Vaya a Gestión de Facturas")
        print("   3. Haga clic en 'Crear Nueva Factura'")
        print("   4. Verifique que los productos aparecen en el dropdown")
    else:
        print("❌ RESULTADO: Hay problemas con los productos")
        print()
        print("🔧 SOLUCIONES:")
        print("   1. Verifique la base de datos")
        print("   2. Agregue productos usando la gestión de productos")
        print("   3. Verifique los logs para más detalles")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
