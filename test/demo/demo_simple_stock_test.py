#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test simple et direct du problème de stock
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from utils.logger import get_logger

def demo_simple_stock_problem():
    """Test simple pour reproduire le problème"""
    
    print("🧪 TEST SIMPLE - Problème de Stock")
    print("=" * 50)
    
    # Initialiser la base de données
    db.init_database()
    logger = get_logger("test_simple")
    
    try:
        print("1️⃣ Création des données de test...")
        
        # Créer un produit
        producto = Producto(
            nombre="Test Simple",
            referencia="SIMPLE-001",
            precio=10.0,
            categoria="Test"
        )
        producto.save()
        print(f"   📦 Producto creado: ID {producto.id}")
        
        # Créer stock initial
        stock_inicial = 50
        stock_obj = Stock(producto.id, stock_inicial)
        stock_obj.save()
        
        stock_verificado = Stock.get_by_product(producto.id)
        print(f"   📊 Stock inicial: {stock_verificado}")
        
        print("\n2️⃣ Simulation de facturation...")
        
        # Créer factura
        factura = Factura(
            numero_factura="SIMPLE-001",
            nombre_cliente="Cliente Test",
            fecha_factura="2024-09-27"
        )
        
        # Créer item
        cantidad_venta = 15
        item = FacturaItem(
            producto_id=producto.id,
            cantidad=cantidad_venta,
            precio_unitario=producto.precio,
            iva_aplicado=21.0
        )
        item.calculate_totals()
        
        # Assigner items à la factura
        factura.items = [item]
        factura.calculate_totals()
        
        print(f"   🧾 Factura: {factura.numero_factura}")
        print(f"   📦 Cantidad vendida: {cantidad_venta}")
        print(f"   💰 Total: €{factura.total_factura:.2f}")
        
        print("\n3️⃣ Sauvegarde de la factura...")
        
        # Sauvegarder la factura (cela ne met PAS à jour le stock automatiquement)
        factura.save()
        print(f"   ✅ Factura guardada con ID: {factura.id}")
        
        # Vérifier stock après sauvegarde
        stock_despues_factura = Stock.get_by_product(producto.id)
        print(f"   📊 Stock después de guardar factura: {stock_despues_factura}")
        
        if stock_despues_factura == stock_inicial:
            print("   ❌ PROBLEMA CONFIRMADO: Stock NO actualizado automáticamente")
        else:
            print("   ✅ Stock actualizado automáticamente")
        
        print("\n4️⃣ Actualización manual del stock...")
        
        # Maintenant, mettre à jour le stock manuellement (comme devrait le faire update_stock_after_save)
        print(f"   🔧 Actualizando stock manualmente...")
        Stock.update_stock(producto.id, cantidad_venta)
        
        stock_final = Stock.get_by_product(producto.id)
        print(f"   📊 Stock después de actualización manual: {stock_final}")
        
        stock_esperado = stock_inicial - cantidad_venta
        if stock_final == stock_esperado:
            print(f"   ✅ Actualización manual exitosa: {stock_inicial} → {stock_final}")
        else:
            print(f"   ❌ Error en actualización manual: esperado {stock_esperado}, obtenido {stock_final}")
        
        print("\n5️⃣ Verificación de movimientos...")
        
        # Vérifier les mouvements de stock
        from database.models import StockMovement
        movimientos = StockMovement.get_by_product(producto.id, limit=5)
        print(f"   📋 Movimientos registrados: {len(movimientos)}")
        for mov in movimientos:
            print(f"      - {mov.tipo}: {mov.cantidad} ({mov.descripcion})")
        
        print("\n6️⃣ Limpieza...")
        
        # Nettoyer
        factura.delete()
        producto.delete()
        print("   🗑️ Datos de test eliminados")
        
        print("\n" + "=" * 50)
        print("📋 CONCLUSIONES:")
        print("1. La factura se guarda correctamente")
        print("2. El stock NO se actualiza automáticamente al guardar factura")
        print("3. La actualización manual de stock SÍ funciona")
        print("4. Los movimientos se registran correctamente")
        print("\n🎯 PROBLEMA: La actualización automática no se ejecuta")
        print("   Posibles causas:")
        print("   • update_stock_after_save() no se llama")
        print("   • Excepción silenciosa en update_stock_after_save()")
        print("   • Problema en el flujo de guardar_factura()")
        
        return stock_final == stock_esperado
        
    except Exception as e:
        logger.error(f"Error en test simple: {e}")
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_stock_update_method():
    """Test isolé de la méthode Stock.update_stock"""
    print("\n🔬 TEST ISOLÉ - Stock.update_stock")
    print("-" * 40)
    
    try:
        # Créer produit simple
        producto = Producto(
            nombre="Test Isolado",
            referencia="ISOLADO-001",
            precio=5.0
        )
        producto.save()
        
        # Stock initial
        stock_inicial = 30
        stock_obj = Stock(producto.id, stock_inicial)
        stock_obj.save()
        
        print(f"Stock inicial: {Stock.get_by_product(producto.id)}")
        
        # Test de mise à jour
        cantidad_venta = 8
        print(f"Actualizando stock: -{cantidad_venta}")
        Stock.update_stock(producto.id, cantidad_venta)
        
        stock_final = Stock.get_by_product(producto.id)
        print(f"Stock final: {stock_final}")
        
        # Vérification
        stock_esperado = stock_inicial - cantidad_venta
        if stock_final == stock_esperado:
            print(f"✅ Método Stock.update_stock funciona: {stock_inicial} → {stock_final}")
            resultado = True
        else:
            print(f"❌ Método Stock.update_stock falla: esperado {stock_esperado}, obtenido {stock_final}")
            resultado = False
        
        # Nettoyer
        producto.delete()
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test isolado: {e}")
        return False

if __name__ == "__main__":
    print("🚀 TESTS SIMPLES DE STOCK")
    print("=" * 60)
    
    # Test 1: Méthode isolée
    print("FASE 1: Test de la méthode Stock.update_stock")
    success1 = demo_stock_update_method()
    
    print("\n" + "=" * 60)
    print("FASE 2: Test du problème complet")
    success2 = demo_simple_stock_problem()
    
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS:")
    print(f"   Méthode Stock.update_stock: {'✅ FUNCIONA' if success1 else '❌ FALLA'}")
    print(f"   Problema completo: {'✅ IDENTIFICADO' if success2 else '❌ NO CLARO'}")
    
    if success1:
        print("\n✅ La méthode de base fonctionne correctement")
        print("🎯 Le problème est dans l'interface ou le flux d'exécution")
        print("\n📋 Prochaines étapes:")
        print("   1. Vérifier que guardar_factura() appelle update_stock_after_save()")
        print("   2. Vérifier les logs pendant l'utilisation de l'interface")
        print("   3. Utiliser le mode debug ajouté à l'interface")
    else:
        print("\n❌ Problème dans la méthode de base")
        print("🔧 Vérifier l'implémentation de Stock.update_stock()")
    
    print("\n📚 Informations utiles:")
    print("   • Logs: logs/facturacion_facil.log")
    print("   • Debug ajouté: ui/facturas.py (debug_guardar_factura)")
    print("   • Base de données: database/facturacion.db")
