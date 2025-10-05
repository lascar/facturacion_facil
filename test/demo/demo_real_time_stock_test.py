#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test en temps réel du problème de stock dans l'interface de facturation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
import threading
import time
from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from ui.facturas import FacturasWindow
from utils.logger import get_logger

def setup_test_data():
    """Créer des données de test"""
    print("🔧 Configurando datos de test...")
    
    # Initialiser la base de données
    db.initialize()
    
    # Créer un produit de test
    producto_test = Producto(
        nombre="Producto Test Real Time",
        referencia="TEST-RT-001",
        precio=25.99,
        categoria="Test",
        iva_recomendado=21.0,
        descripcion="Producto para test en tiempo real"
    )
    producto_test.save()
    
    # Établir stock initial
    stock_inicial = 100
    stock_obj = Stock(producto_test.id, stock_inicial)
    stock_obj.save()
    
    print(f"   📦 Producto creado: {producto_test.nombre} (ID: {producto_test.id})")
    print(f"   📊 Stock inicial: {Stock.get_by_product(producto_test.id)} unidades")
    
    return producto_test

def monitor_stock_changes(producto_id, duration=60):
    """Monitorer les changements de stock en temps réel"""
    print(f"\n🔍 Monitoreando cambios de stock para producto ID {producto_id}...")
    print("   (Duración: {} segundos)".format(duration))
    
    stock_inicial = Stock.get_by_product(producto_id)
    print(f"   📊 Stock inicial: {stock_inicial}")
    
    start_time = time.time()
    last_stock = stock_inicial
    
    while time.time() - start_time < duration:
        current_stock = Stock.get_by_product(producto_id)
        
        if current_stock != last_stock:
            timestamp = time.strftime("%H:%M:%S")
            print(f"   🔄 [{timestamp}] Stock cambió: {last_stock} → {current_stock}")
            last_stock = current_stock
        
        time.sleep(1)  # Vérifier chaque seconde
    
    stock_final = Stock.get_by_product(producto_id)
    print(f"   📊 Stock final: {stock_final}")
    
    if stock_final != stock_inicial:
        print(f"   ✅ CAMBIO DETECTADO: {stock_inicial} → {stock_final}")
    else:
        print(f"   ❌ NO HAY CAMBIOS: Stock se mantuvo en {stock_inicial}")

def demo_real_time_stock_update():
    """Test en temps réel avec interface graphique"""
    
    print("🧪 TEST EN TIEMPO REAL - Actualización de Stock")
    print("=" * 60)
    
    try:
        # Configurer les données de test
        producto_test = setup_test_data()
        
        print("\n📋 INSTRUCCIONES PARA EL TEST:")
        print("1. Se abrirá la ventana de facturas")
        print("2. Crea una nueva factura")
        print("3. Agrega el producto 'Producto Test Real Time'")
        print("4. Guarda la factura")
        print("5. El monitor mostrará si el stock cambia")
        print("\n⏰ El monitor funcionará durante 60 segundos...")
        print("🔍 Presiona Enter para continuar...")
        input()
        
        # Créer l'application principale
        app = ctk.CTk()
        app.title("Test Stock - Facturación Fácil")
        app.geometry("300x200")
        
        # Créer un label d'information
        info_label = ctk.CTkLabel(
            app,
            text="Monitor de Stock Activo\n\n"
                 f"Producto: {producto_test.nombre}\n"
                 f"Stock inicial: {Stock.get_by_product(producto_test.id)}\n\n"
                 "Abre la ventana de facturas\ny crea una factura con este producto",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        info_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Bouton pour ouvrir la fenêtre de facturas
        def open_facturas():
            try:
                facturas_window = FacturasWindow(app, nueva_factura=True)
                print("✅ Ventana de facturas abierta")
            except Exception as e:
                print(f"❌ Error abriendo ventana de facturas: {e}")
        
        open_btn = ctk.CTkButton(
            app,
            text="🧾 Abrir Facturas",
            command=open_facturas,
            fg_color="#2E8B57",
            hover_color="#228B22"
        )
        open_btn.pack(pady=10)
        
        # Démarrer le monitoring en arrière-plan
        monitor_thread = threading.Thread(
            target=monitor_stock_changes,
            args=(producto_test.id, 60),
            daemon=True
        )
        monitor_thread.start()
        
        # Fonction pour fermer proprement
        def on_closing():
            print("\n🔚 Cerrando aplicación...")
            app.quit()
            app.destroy()
        
        app.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("\n🚀 Iniciando aplicación...")
        print("💡 Tip: Mira la consola para ver los cambios de stock en tiempo real")
        
        # Démarrer l'application
        app.mainloop()
        
        # Attendre que le thread de monitoring se termine
        if monitor_thread.is_alive():
            print("⏳ Esperando que termine el monitor...")
            monitor_thread.join(timeout=5)
        
        # Vérification finale
        stock_final = Stock.get_by_product(producto_test.id)
        print(f"\n📊 RESULTADO FINAL:")
        print(f"   Stock inicial: 100")
        print(f"   Stock final: {stock_final}")
        
        if stock_final < 100:
            print("   ✅ ÉXITO: El stock se actualizó correctamente")
        else:
            print("   ❌ PROBLEMA: El stock no se actualizó")
        
        # Nettoyer
        print("\n🧹 Limpiando datos de test...")
        producto_test.delete()
        print("   ✅ Datos eliminados")
        
        return stock_final < 100
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_direct_stock_update():
    """Test direct pour vérifier que Stock.update_stock fonctionne"""
    print("\n🔬 TEST DIRECTO - Verificación de Stock.update_stock")
    print("-" * 50)
    
    try:
        # Créer produit de test
        producto = Producto(
            nombre="Test Directo Stock",
            referencia="TEST-DIRECT-002",
            precio=10.0
        )
        producto.save()
        
        # Stock initial
        stock_inicial = 50
        stock_obj = Stock(producto.id, stock_inicial)
        stock_obj.save()
        
        print(f"Stock inicial: {Stock.get_by_product(producto.id)}")
        
        # Test de mise à jour
        cantidad_venta = 15
        print(f"Actualizando stock: -{cantidad_venta}")
        Stock.update_stock(producto.id, cantidad_venta)
        
        stock_final = Stock.get_by_product(producto.id)
        print(f"Stock final: {stock_final}")
        
        # Vérification
        stock_esperado = stock_inicial - cantidad_venta
        if stock_final == stock_esperado:
            print(f"✅ ÉXITO: Stock actualizado correctamente ({stock_inicial} → {stock_final})")
            resultado = True
        else:
            print(f"❌ ERROR: Esperado {stock_esperado}, obtenido {stock_final}")
            resultado = False
        
        # Vérifier les mouvements
        from database.models import StockMovement
        movimientos = StockMovement.get_by_product(producto.id, limit=3)
        print(f"Movimientos registrados: {len(movimientos)}")
        for mov in movimientos:
            print(f"   - {mov.tipo}: {mov.cantidad} ({mov.descripcion})")
        
        # Nettoyer
        producto.delete()
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error en test directo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TESTS DE STOCK EN TIEMPO REAL")
    print("=" * 60)
    
    # Test 1: Vérification directe
    print("FASE 1: Verificación del método Stock.update_stock")
    success1 = demo_direct_stock_update()
    
    if not success1:
        print("\n❌ El método básico no funciona. No continuar con test de interfaz.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("FASE 2: Test en tiempo real con interfaz gráfica")
    
    # Test 2: Interface en temps réel
    success2 = demo_real_time_stock_update()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL:")
    print(f"   Test método directo: {'✅ ÉXITO' if success1 else '❌ FALLO'}")
    print(f"   Test interfaz gráfica: {'✅ ÉXITO' if success2 else '❌ FALLO'}")
    
    if success1 and success2:
        print("\n🎉 TODOS LOS TESTS EXITOSOS")
        print("El problema de stock está resuelto.")
    elif success1 and not success2:
        print("\n⚠️ PROBLEMA EN LA INTERFAZ")
        print("El método funciona, pero hay un problema en la interfaz gráfica.")
        print("Revisar el flujo de guardar_factura() y update_stock_after_save()")
    else:
        print("\n❌ PROBLEMAS DETECTADOS")
        print("Revisar la implementación de Stock.update_stock()")
    
    print("\n📚 Información adicional:")
    print("   • Logs en logs/facturacion_facil.log")
    print("   • Código en ui/facturas_methods.py")
    print("   • Base de datos en database/facturacion.db")
