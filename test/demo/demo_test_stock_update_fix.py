#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de la correction du problème de mise à jour du stock lors de la facturation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from ui.facturas_methods import FacturasMethodsMixin
from utils.logger import get_logger

class TestFacturasMethodsMixin(FacturasMethodsMixin):
    """Classe de test pour simuler FacturasWindow"""
    
    def __init__(self):
        self.logger = get_logger("test_facturas")
        self.current_factura = None
        self.factura_items = []
        self.window = None  # Simulé pour les messages
    
    def _show_message(self, msg_type, title, message):
        """Simuler l'affichage de messages"""
        print(f"[{msg_type.upper()}] {title}: {message}")

def demo_stock_update_with_logging():
    """Test complet avec logging détaillé"""
    
    print("🧪 TEST - Correction de mise à jour du stock avec logging")
    print("=" * 70)
    
    # Initialiser la base de données
    db.initialize()
    
    try:
        print("1️⃣ Préparation des données de test...")
        
        # Créer un produit de test
        producto_test = Producto(
            nombre="Producto Test Logging",
            referencia="TEST-LOG-001",
            precio=20.00,
            categoria="Test",
            iva_recomendado=21.0
        )
        producto_test.save()
        print(f"   📦 Producto creado: {producto_test.nombre} (ID: {producto_test.id})")
        
        # Établir stock initial
        stock_inicial = 75
        stock_obj = Stock(producto_test.id, stock_inicial)
        stock_obj.save()
        
        stock_verificado = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock inicial: {stock_verificado} unidades")
        
        print("\n2️⃣ Création de la factura de test...")
        
        # Créer instance de test du mixin
        test_mixin = TestFacturasMethodsMixin()
        
        # Créer factura
        factura_test = Factura(
            numero_factura="TEST-LOG-001",
            nombre_cliente="Cliente Test Logging",
            fecha_factura="2024-09-27"
        )
        
        # Créer item
        cantidad_vendida = 20
        item_test = FacturaItem(
            producto_id=producto_test.id,
            cantidad=cantidad_vendida,
            precio_unitario=producto_test.precio,
            iva_aplicado=21.0
        )
        item_test.calculate_totals()
        
        # Configurer le mixin
        test_mixin.current_factura = factura_test
        test_mixin.factura_items = [item_test]
        
        # Asignar items à la factura
        factura_test.items = [item_test]
        factura_test.calculate_totals()
        
        print(f"   🧾 Factura: {factura_test.numero_factura}")
        print(f"   📦 Producto: {producto_test.nombre}")
        print(f"   📊 Cantidad: {cantidad_vendida}")
        print(f"   💰 Total: €{factura_test.total_factura:.2f}")
        
        print("\n3️⃣ Simulación du processus de sauvegarde...")
        
        # Sauvegarder la factura
        print("   💾 Guardando factura...")
        factura_test.save()
        print(f"   ✅ Factura guardada con ID: {factura_test.id}")
        
        # Vérifier stock avant mise à jour
        stock_antes_update = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock antes de update_stock_after_save: {stock_antes_update}")
        
        print("\n4️⃣ Exécution de update_stock_after_save avec logging...")
        print("   " + "-" * 60)
        
        # Exécuter la méthode avec logging détaillé
        test_mixin.update_stock_after_save()
        
        print("   " + "-" * 60)
        
        # Vérifier stock après mise à jour
        stock_despues_update = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock después de update_stock_after_save: {stock_despues_update}")
        
        print("\n5️⃣ Vérification des résultats...")
        
        stock_esperado = stock_inicial - cantidad_vendida
        
        print(f"   📊 Stock inicial: {stock_inicial}")
        print(f"   📊 Cantidad vendida: {cantidad_vendida}")
        print(f"   📊 Stock esperado: {stock_esperado}")
        print(f"   📊 Stock obtenido: {stock_despues_update}")
        
        if stock_despues_update == stock_esperado:
            print("   ✅ ÉXITO: Stock actualizado correctamente")
            resultado = True
        else:
            print("   ❌ ERROR: Stock no actualizado correctamente")
            resultado = False
        
        print("\n6️⃣ Verificación de movimientos de stock...")
        
        # Vérifier les mouvements de stock
        from database.models import StockMovement
        movimientos = StockMovement.get_by_product(producto_test.id, limit=5)
        
        print(f"   📋 Movimientos registrados: {len(movimientos)}")
        for mov in movimientos:
            print(f"      - {mov.tipo}: {mov.cantidad} ({mov.descripcion})")
        
        print("\n7️⃣ Limpieza...")
        
        # Nettoyer les données de test
        factura_test.delete()
        producto_test.delete()
        print("   🗑️ Datos de test eliminados")
        
        print("\n" + "=" * 70)
        if resultado:
            print("✅ TEST EXITOSO - La corrección funciona correctamente")
        else:
            print("❌ TEST FALLIDO - El problema persiste")
        print("=" * 70)
        
        return resultado
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_direct_method_call():
    """Test directo del método Stock.update_stock"""
    print("\n🔬 TEST DIRECTO - Método Stock.update_stock")
    print("-" * 50)
    
    try:
        # Créer produit simple
        producto = Producto(
            nombre="Test Directo",
            referencia="TEST-DIRECT-001",
            precio=5.0
        )
        producto.save()
        
        # Stock initial
        stock_inicial = 30
        stock_obj = Stock(producto.id, stock_inicial)
        stock_obj.save()
        
        print(f"Stock inicial: {Stock.get_by_product(producto.id)}")
        
        # Appel direct
        cantidad_venta = 8
        Stock.update_stock(producto.id, cantidad_venta)
        
        stock_final = Stock.get_by_product(producto.id)
        print(f"Stock final: {stock_final}")
        
        # Vérification
        if stock_final == stock_inicial - cantidad_venta:
            print("✅ Método directo funciona")
            resultado = True
        else:
            print("❌ Método directo falla")
            resultado = False
        
        # Nettoyer
        producto.delete()
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test directo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando tests de corrección de stock...")
    print()
    
    # Test 1: Méthode directe
    success1 = demo_direct_method_call()
    
    # Test 2: Avec logging complet
    success2 = demo_stock_update_with_logging()
    
    print("\n📊 RESUMEN DE TESTS:")
    print(f"   Test método directo: {'✅ ÉXITO' if success1 else '❌ FALLO'}")
    print(f"   Test con logging: {'✅ ÉXITO' if success2 else '❌ FALLO'}")
    
    if success1 and success2:
        print("\n🎉 TODOS LOS TESTS EXITOSOS")
        print("La corrección del problema de stock está funcionando.")
        print("\n📋 Próximos pasos:")
        print("   1. Probar en la interfaz gráfica real")
        print("   2. Verificar logs durante uso normal")
        print("   3. Confirmar que el problema está resuelto")
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON")
        print("Revisar los logs y el código para identificar problemas.")
    
    print("\n📚 Información adicional:")
    print("   • Logs detallados en logs/facturacion_facil.log")
    print("   • Código modificado en ui/facturas_methods.py")
    print("   • Tests adicionales en test/demo/")
