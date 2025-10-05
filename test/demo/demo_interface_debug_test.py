#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test avec l'interface de debug pour identifier le problème de stock
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
from database.database import db
from database.models import Producto, Stock
from ui.facturas import FacturasWindow
from utils.logger import get_logger
import threading
import time

def setup_test_data():
    """Créer des données de test pour l'interface"""
    print("🔧 Configurando datos de test para interfaz...")
    
    # Initialiser la base de données
    db.init_database()
    
    # Créer quelques produits de test
    productos_test = [
        {
            "nombre": "Producto Debug 1",
            "referencia": "DEBUG-001",
            "precio": 15.99,
            "categoria": "Debug",
            "stock_inicial": 100
        },
        {
            "nombre": "Producto Debug 2", 
            "referencia": "DEBUG-002",
            "precio": 25.50,
            "categoria": "Debug",
            "stock_inicial": 75
        },
        {
            "nombre": "Producto Debug 3",
            "referencia": "DEBUG-003", 
            "precio": 8.75,
            "categoria": "Debug",
            "stock_inicial": 50
        }
    ]
    
    productos_creados = []
    
    for producto_data in productos_test:
        # Créer le produit
        producto = Producto(
            nombre=producto_data["nombre"],
            referencia=producto_data["referencia"],
            precio=producto_data["precio"],
            categoria=producto_data["categoria"],
            iva_recomendado=21.0,
            descripcion=f"Producto de test para debug - {producto_data['referencia']}"
        )
        producto.save()
        
        # Établir stock initial
        stock_obj = Stock(producto.id, producto_data["stock_inicial"])
        stock_obj.save()
        
        productos_creados.append({
            'producto': producto,
            'stock_inicial': producto_data["stock_inicial"]
        })
        
        print(f"   📦 {producto.nombre} (ID: {producto.id}) - Stock: {Stock.get_by_product(producto.id)}")
    
    return productos_creados

def monitor_stock_changes(productos_data, duration=120):
    """Monitorer les changements de stock en temps réel"""
    print(f"\n🔍 Monitoreando cambios de stock durante {duration} segundos...")
    print("   Productos monitoreados:")
    
    # État initial
    stock_inicial = {}
    for data in productos_data:
        producto = data['producto']
        stock_actual = Stock.get_by_product(producto.id)
        stock_inicial[producto.id] = stock_actual
        print(f"      - {producto.nombre}: {stock_actual} unidades")
    
    print("\n   🔄 Iniciando monitoreo... (Crea facturas con estos productos)")
    print("   " + "-" * 60)
    
    start_time = time.time()
    last_stocks = stock_inicial.copy()
    
    while time.time() - start_time < duration:
        cambios_detectados = False
        
        for data in productos_data:
            producto = data['producto']
            current_stock = Stock.get_by_product(producto.id)
            
            if current_stock != last_stocks[producto.id]:
                timestamp = time.strftime("%H:%M:%S")
                print(f"   🔄 [{timestamp}] {producto.nombre}: {last_stocks[producto.id]} → {current_stock}")
                last_stocks[producto.id] = current_stock
                cambios_detectados = True
        
        if cambios_detectados:
            print("   " + "-" * 60)
        
        time.sleep(2)  # Vérifier toutes les 2 secondes
    
    print(f"\n📊 RESUMEN FINAL:")
    cambios_totales = False
    for data in productos_data:
        producto = data['producto']
        stock_final = Stock.get_by_product(producto.id)
        stock_inicial_prod = stock_inicial[producto.id]
        
        if stock_final != stock_inicial_prod:
            print(f"   ✅ {producto.nombre}: {stock_inicial_prod} → {stock_final} (CAMBIÓ)")
            cambios_totales = True
        else:
            print(f"   ❌ {producto.nombre}: {stock_inicial_prod} (SIN CAMBIOS)")
    
    if cambios_totales:
        print("\n✅ SE DETECTARON CAMBIOS - El problema podría estar resuelto")
    else:
        print("\n❌ NO SE DETECTARON CAMBIOS - El problema persiste")
    
    return cambios_totales

def demo_interface_with_debug():
    """Test con interfaz gráfica y debug activado"""
    
    print("🧪 TEST INTERFAZ CON DEBUG - Problema de Stock")
    print("=" * 70)
    
    try:
        # Configurar datos de test
        productos_data = setup_test_data()
        
        print("\n📋 INSTRUCCIONES PARA EL TEST:")
        print("1. Se abrirá la aplicación principal")
        print("2. Ve a 'Facturas' para abrir la ventana de facturas")
        print("3. Crea una nueva factura")
        print("4. Agrega algunos de los productos de debug:")
        for data in productos_data:
            print(f"   - {data['producto'].nombre} (Stock: {data['stock_inicial']})")
        print("5. Guarda la factura (el botón ahora usa debug_guardar_factura)")
        print("6. Revisa los logs en la consola y en logs/facturacion_facil.log")
        print("7. El monitor mostrará si el stock cambia")
        print("\n⏰ El monitor funcionará durante 2 minutos...")
        print("🔍 Presiona Enter para continuar...")
        input()
        
        # Créer l'application principale
        app = ctk.CTk()
        app.title("Test Debug Stock - Facturación Fácil")
        app.geometry("400x300")
        
        # Créer un label d'information
        info_text = "Monitor de Stock Activo\n\n"
        info_text += "Productos de test creados:\n"
        for data in productos_data:
            info_text += f"• {data['producto'].nombre}\n"
            info_text += f"  Stock inicial: {data['stock_inicial']}\n"
        info_text += "\nAbre Facturas y crea una factura\ncon estos productos"
        
        info_label = ctk.CTkLabel(
            app,
            text=info_text,
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        info_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Bouton pour ouvrir la fenêtre de facturas
        def open_facturas():
            try:
                facturas_window = FacturasWindow(app, nueva_factura=True)
                print("✅ Ventana de facturas abierta con DEBUG ACTIVADO")
                print("💡 El botón 'Guardar' ahora usa debug_guardar_factura()")
                print("📋 Revisa los logs para ver el flujo de ejecución detallado")
            except Exception as e:
                print(f"❌ Error abriendo ventana de facturas: {e}")
                import traceback
                traceback.print_exc()
        
        open_btn = ctk.CTkButton(
            app,
            text="🧾 Abrir Facturas (con Debug)",
            command=open_facturas,
            fg_color="#2E8B57",
            hover_color="#228B22",
            height=40
        )
        open_btn.pack(pady=10)
        
        # Bouton pour voir les logs
        def show_logs():
            try:
                import subprocess
                log_file = "logs/facturacion_facil.log"
                if os.path.exists(log_file):
                    # Ouvrir le fichier de log avec l'éditeur par défaut
                    if sys.platform.startswith('linux'):
                        subprocess.run(['xdg-open', log_file])
                    elif sys.platform.startswith('win'):
                        subprocess.run(['notepad', log_file])
                    elif sys.platform.startswith('darwin'):
                        subprocess.run(['open', log_file])
                    print("📄 Archivo de logs abierto")
                else:
                    print("❌ Archivo de logs no encontrado")
            except Exception as e:
                print(f"❌ Error abriendo logs: {e}")
        
        logs_btn = ctk.CTkButton(
            app,
            text="📄 Ver Logs",
            command=show_logs,
            fg_color="#4169E1",
            hover_color="#1E90FF"
        )
        logs_btn.pack(pady=5)
        
        # Démarrer le monitoring en arrière-plan
        monitor_thread = threading.Thread(
            target=monitor_stock_changes,
            args=(productos_data, 120),  # 2 minutes
            daemon=True
        )
        monitor_thread.start()
        
        # Fonction pour fermer proprement
        def on_closing():
            print("\n🔚 Cerrando aplicación de test...")
            app.quit()
            app.destroy()
        
        app.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("\n🚀 Iniciando aplicación con debug...")
        print("💡 Tips:")
        print("   - Mira la consola para cambios de stock en tiempo real")
        print("   - Revisa logs/facturacion_facil.log para logs detallados")
        print("   - El botón 'Guardar' en facturas ahora tiene debug activado")
        
        # Démarrer l'application
        app.mainloop()
        
        # Attendre que le thread de monitoring se termine
        if monitor_thread.is_alive():
            print("⏳ Esperando que termine el monitor...")
            monitor_thread.join(timeout=5)
        
        # Nettoyer les données de test
        print("\n🧹 Limpiando datos de test...")
        for data in productos_data:
            try:
                data['producto'].delete()
            except:
                pass
        print("   ✅ Datos de test eliminados")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante el test de interfaz: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TEST DE INTERFAZ CON DEBUG")
    print("=" * 70)
    
    success = demo_interface_with_debug()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ TEST DE INTERFAZ COMPLETADO")
        print("\n📋 Qué revisar:")
        print("   1. ¿Aparecieron logs de debug en la consola?")
        print("   2. ¿Se detectaron cambios de stock durante el test?")
        print("   3. ¿Hay errores en logs/facturacion_facil.log?")
        print("\n🎯 Basado en los resultados:")
        print("   • Si NO aparecen logs de debug → Problema de herencia")
        print("   • Si aparecen logs pero NO cambia stock → Problema en update_stock_after_save")
        print("   • Si todo funciona → Problema resuelto")
    else:
        print("❌ ERROR EN TEST DE INTERFAZ")
        print("Revisar los errores mostrados arriba")
    
    print("\n📚 Recursos:")
    print("   • Logs detallados: logs/facturacion_facil.log")
    print("   • Código debug: ui/facturas.py (debug_guardar_factura)")
    print("   • Base de datos: database/facturacion.db")
