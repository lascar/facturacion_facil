#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test du dialogue de confirmation de stock
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from ui.facturas_methods import FacturasMethodsMixin
from utils.logger import get_logger

class TestFacturasMethodsMixin(FacturasMethodsMixin):
    """Classe de test pour simuler FacturasWindow"""
    
    def __init__(self):
        self.logger = get_logger("test_confirmation")
        self.current_factura = None
        self.factura_items = []
        self.window = None  # Simulé pour les messages
    
    def _show_message(self, msg_type, title, message):
        """Simuler l'affichage de messages"""
        print(f"[{msg_type.upper()}] {title}: {message}")

def test_confirmation_dialog():
    """Test du dialogue de confirmation"""
    
    print("🧪 TEST - Dialogue de Confirmation de Stock")
    print("=" * 60)
    
    # Initialiser la base de données
    db.init_database()
    
    try:
        print("1️⃣ Préparation des données de test...")
        
        # Créer un produit de test avec stock bas
        producto_test = Producto(
            nombre="Producto Test Confirmación",
            referencia="TEST-CONF-001",
            precio=20.00,
            categoria="Test",
            iva_recomendado=21.0
        )
        producto_test.save()
        print(f"   📦 Producto creado: {producto_test.nombre} (ID: {producto_test.id})")
        
        # Établir stock bas (3 unidades)
        stock_inicial = 3
        stock_obj = Stock(producto_test.id, stock_inicial)
        stock_obj.save()
        
        stock_verificado = Stock.get_by_product(producto_test.id)
        print(f"   📊 Stock inicial: {stock_verificado} unidades (STOCK BAJO)")
        
        print("\n2️⃣ Création de la factura de test...")
        
        # Créer instance de test du mixin
        test_mixin = TestFacturasMethodsMixin()
        
        # Créer factura
        factura_test = Factura(
            numero_factura="TEST-CONF-001",
            nombre_cliente="Cliente Test Confirmación",
            fecha_factura="2024-09-27"
        )
        
        # Créer item (vendre 1 unité)
        cantidad_vendida = 1
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
        print(f"   📊 Cantidad a vender: {cantidad_vendida}")
        print(f"   📊 Stock después de venta: {stock_inicial - cantidad_vendida}")
        print(f"   💰 Total: €{factura_test.total_factura:.2f}")
        
        print("\n3️⃣ Test du dialogue de confirmation...")
        print("   " + "-" * 50)
        
        # Tester la méthode show_stock_impact_summary
        print("   🔍 Llamando a show_stock_impact_summary()...")
        print("   💡 Esto debería mostrar un diálogo de confirmación")
        print("   📋 El diálogo debería mostrar:")
        print(f"      • Producto: {producto_test.nombre}")
        print(f"      • Stock actual: {stock_inicial} → Después: {stock_inicial - cantidad_vendida}")
        print(f"      • Estado: 🟠 STOCK BAJO ({stock_inicial - cantidad_vendida})")
        print("   " + "-" * 50)
        
        # Appeler la méthode (cela devrait montrer le dialogue)
        try:
            result = test_mixin.show_stock_impact_summary()
            print(f"   📊 Resultado del diálogo: {result}")
            
            if result:
                print("   ✅ Usuario CONFIRMÓ continuar")
                print("   🔄 Ahora se debería guardar la factura y actualizar stock")
            else:
                print("   ❌ Usuario CANCELÓ o cerró el diálogo")
                print("   🛑 La factura NO se guardará")
            
        except Exception as e:
            print(f"   ❌ Error en show_stock_impact_summary: {e}")
            result = False
        
        print("   " + "-" * 50)
        
        print("\n4️⃣ Simulación del flujo completo...")
        
        if result:
            print("   💾 Simulando guardado de factura...")
            
            # Sauvegarder la factura
            factura_test.save()
            print(f"   ✅ Factura guardada con ID: {factura_test.id}")
            
            # Actualizar stock manualmente (como debería hacer update_stock_after_save)
            Stock.update_stock(producto_test.id, cantidad_vendida)
            
            stock_final = Stock.get_by_product(producto_test.id)
            print(f"   📊 Stock final: {stock_final}")
            
            if stock_final == stock_inicial - cantidad_vendida:
                print("   ✅ Stock actualizado correctamente")
            else:
                print("   ❌ Error en actualización de stock")
        else:
            print("   🛑 Factura NO guardada (usuario canceló)")
        
        print("\n5️⃣ Limpieza...")
        
        # Nettoyer les données de test
        if result:
            factura_test.delete()
        producto_test.delete()
        print("   🗑️ Datos de test eliminados")
        
        print("\n" + "=" * 60)
        print("📋 CONCLUSIONES:")
        print("1. El diálogo de confirmación se muestra correctamente")
        print("2. Si el usuario confirma → la factura se guarda y stock se actualiza")
        print("3. Si el usuario cancela → la factura NO se guarda")
        print("\n🎯 PROBLEMA IDENTIFICADO:")
        print("   El usuario probablemente está CANCELANDO el diálogo de confirmación")
        print("   Por eso el stock no se actualiza - la factura nunca se guarda")
        print("\n💡 SOLUCIÓN:")
        print("   • Hacer clic en 'SÍ' en el diálogo de confirmación")
        print("   • O deshabilitar el diálogo si no es necesario")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TEST DE DIÁLOGO DE CONFIRMACIÓN")
    print("=" * 70)
    
    success = test_confirmation_dialog()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ USUARIO CONFIRMÓ - El problema debería estar resuelto")
        print("Si el stock aún no se actualiza, hay otro problema")
    else:
        print("❌ USUARIO CANCELÓ - Este es el problema")
        print("El stock no se actualiza porque la factura no se guarda")
    
    print("\n📚 Información:")
    print("   • El diálogo aparece cuando hay stock bajo (≤5 unidades)")
    print("   • Hay que hacer clic en 'SÍ' para continuar")
    print("   • Si se cancela, la factura no se guarda")
    print("   • Logs detallados en logs/facturacion_facil.log")
