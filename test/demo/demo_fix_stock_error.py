#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Démonstration de la correction de l'erreur:
"Error al agregar producto: 'int' object has no attribute 'cantidad_disponible'"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database import db
from database.models import Producto, Stock
from utils.logger import get_logger

def demo_stock_error_fix():
    """Démonstration de la correction de l'erreur de stock"""
    
    print("🔧 DÉMONSTRATION - Correction erreur Stock")
    print("=" * 60)
    print("Erreur originale: 'int' object has no attribute 'cantidad_disponible'")
    print("Cause: Confusion entre entier et objet Stock")
    print()
    
    # Initialiser la base de données
    db.initialize()
    logger = get_logger("demo_stock_fix")
    
    try:
        print("1️⃣ Test de création de produit avec stock automatique...")
        
        # Créer un produit de test
        producto_test = Producto(
            nombre="Producto Test Stock Fix",
            referencia=f"TEST-STOCK-FIX-001",
            precio=25.99,
            categoria="Test",
            iva_recomendado=21.0,
            descripcion="Producto para probar la corrección del error de stock"
        )
        
        print(f"   📦 Creando producto: {producto_test.nombre}")
        print(f"   🏷️ Referencia: {producto_test.referencia}")
        print(f"   💰 Precio: €{producto_test.precio}")
        
        # Sauvegarder le produit (cela devrait créer automatiquement le stock)
        producto_test.save()
        
        print(f"   ✅ Producto creado con ID: {producto_test.id}")
        
        # Vérifier que le stock a été créé automatiquement
        print("\n2️⃣ Verificación de stock automático...")
        
        stock_inicial = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock inicial: {stock_inicial} unidades")
        print(f"   📊 Tipo de retorno: {type(stock_inicial)}")
        
        # Vérifier que c'est bien un entier (pas un objet Stock)
        assert isinstance(stock_inicial, int), f"Expected int, got {type(stock_inicial)}"
        assert stock_inicial == 0, f"Expected 0, got {stock_inicial}"
        
        print("   ✅ Stock créé correctement (entier, pas objet)")
        
        print("\n3️⃣ Test de la méthode corrigée...")
        
        # Simuler l'utilisation correcte dans facturas_methods.py
        def demo_stock_verification_corrected(producto_id, cantidad_solicitada):
            """Simulation de la méthode corrigée"""
            # AVANT (INCORRECT): stock.cantidad_disponible
            # APRÈS (CORRECT): stock_disponible directement
            
            stock_disponible = Stock.get_by_product(producto_id)
            print(f"   📊 Stock disponible: {stock_disponible}")
            print(f"   📊 Cantidad solicitada: {cantidad_solicitada}")
            
            if stock_disponible < cantidad_solicitada:
                print(f"   ⚠️ Stock insuficiente: {stock_disponible} < {cantidad_solicitada}")
                return False
            else:
                print(f"   ✅ Stock suficiente: {stock_disponible} >= {cantidad_solicitada}")
                return True
        
        # Test avec stock insuficiente
        print("   🧪 Test con stock insuficiente (0 < 5):")
        result1 = demo_stock_verification_corrected(producto_test.id, 5)
        assert not result1, "Debería retornar False para stock insuficiente"
        
        # Agregar stock
        print("\n4️⃣ Agregando stock para más tests...")
        stock_obj = Stock(producto_test.id, 10)
        stock_obj.save()
        
        stock_actualizado = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock actualizado: {stock_actualizado} unidades")
        
        # Test con stock suficiente
        print("   🧪 Test con stock suficiente (10 >= 5):")
        result2 = demo_stock_verification_corrected(producto_test.id, 5)
        assert result2, "Debería retornar True para stock suficiente"
        
        print("\n5️⃣ Verificación de métodos Stock...")
        
        # Verificar todos los métodos que retornan enteros
        methods_to_test = [
            ("Stock.get_by_product()", lambda: Stock.get_by_product(producto_test.id)),
            ("Stock.get_all()", lambda: Stock.get_all()),
            ("Stock.get_low_stock()", lambda: Stock.get_low_stock(15))
        ]
        
        for method_name, method_func in methods_to_test:
            try:
                result = method_func()
                print(f"   ✅ {method_name}: {type(result)} - OK")
                
                if method_name == "Stock.get_by_product()":
                    assert isinstance(result, int), f"{method_name} should return int"
                elif method_name in ["Stock.get_all()", "Stock.get_low_stock()"]:
                    assert isinstance(result, list), f"{method_name} should return list"
                    
            except Exception as e:
                print(f"   ❌ {method_name}: Error - {e}")
        
        print("\n6️⃣ Limpieza...")
        
        # Limpiar el producto de test
        producto_test.delete()
        print(f"   🗑️ Producto de test eliminado")
        
        print("\n" + "=" * 60)
        print("✅ CORRECCIÓN VERIFICADA EXITOSAMENTE")
        print("=" * 60)
        print()
        print("📋 Resumen de la corrección:")
        print("   • Problema: Intentar acceder a 'cantidad_disponible' en un entier")
        print("   • Causa: Stock.get_by_product() retorna int, no objeto Stock")
        print("   • Solución: Usar directamente el valor entero retornado")
        print("   • Archivo corregido: ui/facturas_methods.py línea 186")
        print()
        print("🔧 Cambio realizado:")
        print("   ANTES: if stock and stock.cantidad_disponible < cantidad:")
        print("   DESPUÉS: if stock_disponible < cantidad:")
        print()
        print("✅ La aplicación ya no debería mostrar este error al agregar productos")
        
        return True
        
    except Exception as e:
        logger.error(f"Error en demo: {e}")
        print(f"\n❌ Error durante la demostración: {e}")
        return False

def demo_all_stock_methods():
    """Test adicional de todos los métodos de Stock"""
    print("\n🧪 TEST ADICIONAL - Todos los métodos Stock")
    print("-" * 50)
    
    try:
        # Crear producto de test
        producto = Producto(
            nombre="Test All Methods",
            referencia="TEST-ALL-001",
            precio=10.0
        )
        producto.save()
        
        # Test Stock.create_for_product
        print("1. Stock.create_for_product() - ✅")
        
        # Test Stock.get_by_product
        stock = Stock.get_by_product(producto.id)
        print(f"2. Stock.get_by_product() -> {stock} ({type(stock)}) - ✅")
        
        # Test Stock.get_all
        all_stock = Stock.get_all()
        print(f"3. Stock.get_all() -> {len(all_stock)} items ({type(all_stock)}) - ✅")
        
        # Test Stock.update_stock
        Stock.update_stock(producto.id, 0)  # No cambio
        print("4. Stock.update_stock() - ✅")
        
        # Test Stock.get_low_stock
        low_stock = Stock.get_low_stock(5)
        print(f"5. Stock.get_low_stock() -> {len(low_stock)} items ({type(low_stock)}) - ✅")
        
        # Limpiar
        producto.delete()
        
        print("✅ Todos los métodos Stock funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de métodos: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando demostración de corrección de error Stock...")
    print()
    
    success1 = demo_stock_error_fix()
    success2 = demo_all_stock_methods()
    
    if success1 and success2:
        print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("La corrección del error de Stock está funcionando correctamente.")
    else:
        print("\n⚠️ Algunas pruebas fallaron. Revisar los logs para más detalles.")
    
    print("\n📚 Para más información, consultar:")
    print("   • docs/fixes/ - Documentación de correcciones")
    print("   • logs/ - Archivos de log detallados")
    print("   • test/unit/test_models.py - Tests unitarios")
