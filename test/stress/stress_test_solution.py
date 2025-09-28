#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Stress test de la solución completa
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import threading
import random
from datetime import datetime, timedelta
from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from utils.logger import get_logger

class StressTest:
    """Stress test del sistema"""
    
    def __init__(self):
        self.logger = get_logger("stress_test")
        self.running = False
        self.results = {
            'facturas_created': 0,
            'stock_updates': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        self.threads = []
    
    def run_stress_test(self, duration_minutes=5, concurrent_threads=3):
        """Ejecuta el stress test"""
        print("💥 STRESS TEST - Facturación Fácil")
        print("=" * 60)
        print(f"Configuración:")
        print(f"   • Duración: {duration_minutes} minutos")
        print(f"   • Threads concurrentes: {concurrent_threads}")
        print(f"   • Operaciones: Creación de facturas + actualización de stock")
        print("\nPresiona Ctrl+C para detener antes de tiempo")
        print("-" * 60)
        
        # Inicializar
        db.init_database()
        self.running = True
        self.results['start_time'] = datetime.now()
        
        # Verificar que hay productos disponibles
        productos = Producto.get_all()
        if len(productos) < 5:
            print("⚠️ Se necesitan al menos 5 productos para el stress test")
            print("Creando productos de test...")
            self._create_test_products()
            productos = Producto.get_all()
        
        print(f"✅ Productos disponibles: {len(productos)}")
        
        try:
            # Crear threads de stress test
            for i in range(concurrent_threads):
                thread = threading.Thread(
                    target=self._stress_worker,
                    args=(f"Worker-{i+1}", duration_minutes * 60)
                )
                thread.daemon = True
                self.threads.append(thread)
                thread.start()
            
            # Monitor de progreso
            self._monitor_progress(duration_minutes * 60)
            
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo stress test...")
        finally:
            self.stop_stress_test()
    
    def stop_stress_test(self):
        """Detiene el stress test"""
        self.running = False
        self.results['end_time'] = datetime.now()
        
        # Esperar a que terminen los threads
        for thread in self.threads:
            thread.join(timeout=5)
        
        self._show_results()
    
    def _create_test_products(self):
        """Crea productos de test si no hay suficientes"""
        test_products = [
            ("Producto Stress A", "STRESS-A", 25.99, "Test", 21.0),
            ("Producto Stress B", "STRESS-B", 45.50, "Test", 21.0),
            ("Producto Stress C", "STRESS-C", 15.75, "Test", 10.0),
            ("Producto Stress D", "STRESS-D", 89.99, "Test", 21.0),
            ("Producto Stress E", "STRESS-E", 12.30, "Test", 4.0),
        ]
        
        for nombre, ref, precio, cat, iva in test_products:
            try:
                producto = Producto(
                    nombre=nombre,
                    referencia=ref,
                    precio=precio,
                    categoria=cat,
                    iva_recomendado=iva,
                    descripcion=f"Producto creado para stress test"
                )
                producto.save()
                
                # Stock inicial alto para el test
                Stock.update_stock(producto.id, 1000, "INICIAL", "Stock para stress test")
                
            except Exception as e:
                self.logger.error(f"Error creando producto de test: {e}")
    
    def _stress_worker(self, worker_name, duration_seconds):
        """Worker que ejecuta operaciones de stress"""
        end_time = time.time() + duration_seconds
        worker_stats = {'facturas': 0, 'errors': 0}
        
        while self.running and time.time() < end_time:
            try:
                # Crear factura aleatoria
                if self._create_random_factura():
                    worker_stats['facturas'] += 1
                    self.results['facturas_created'] += 1
                
                # Pausa aleatoria entre operaciones
                time.sleep(random.uniform(0.5, 2.0))
                
            except Exception as e:
                worker_stats['errors'] += 1
                self.results['errors'] += 1
                self.logger.error(f"{worker_name} error: {e}")
                time.sleep(1)  # Pausa más larga en caso de error
        
        print(f"🔧 {worker_name} terminado: {worker_stats['facturas']} facturas, {worker_stats['errors']} errores")
    
    def _create_random_factura(self):
        """Crea una factura aleatoria"""
        try:
            productos = Producto.get_all()
            if not productos:
                return False
            
            # Datos aleatorios de cliente
            clientes = [
                "Juan Pérez", "María García", "Carlos López", "Ana Martín",
                "Pedro Sánchez", "Laura Rodríguez", "Miguel Torres", "Carmen Ruiz"
            ]
            
            cliente = random.choice(clientes)
            timestamp = int(time.time())
            
            # Crear factura
            factura = Factura(
                numero_factura=f"STRESS-{timestamp}-{random.randint(1000, 9999)}",
                nombre_cliente=cliente,
                dni_nie_cliente=f"{random.randint(10000000, 99999999)}A",
                fecha_factura=datetime.now().strftime("%Y-%m-%d"),
                modo_pago=random.choice(["efectivo", "tarjeta", "transferencia"])
            )
            
            # Agregar items aleatorios
            num_items = random.randint(1, 4)
            items = []
            
            for _ in range(num_items):
                producto = random.choice(productos)
                cantidad = random.randint(1, 5)
                
                # Verificar stock disponible
                stock_actual = Stock.get_by_product(producto.id)
                if stock_actual < cantidad:
                    cantidad = max(1, stock_actual)
                
                if cantidad > 0:
                    item = FacturaItem(
                        producto_id=producto.id,
                        cantidad=cantidad,
                        precio_unitario=producto.precio,
                        iva_aplicado=producto.iva_recomendado
                    )
                    item.calculate_totals()
                    items.append(item)
            
            if items:
                factura.items = items
                factura.calculate_totals()
                factura.save()
                
                # Actualizar stock
                for item in items:
                    try:
                        stock_actual = Stock.get_by_product(item.producto_id)
                        nuevo_stock = stock_actual - item.cantidad
                        Stock.update_stock(
                            item.producto_id, 
                            nuevo_stock, 
                            "VENTA", 
                            f"Factura {factura.numero_factura}"
                        )
                        self.results['stock_updates'] += 1
                    except Exception as e:
                        self.logger.error(f"Error actualizando stock: {e}")
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error creando factura aleatoria: {e}")
            return False
    
    def _monitor_progress(self, duration_seconds):
        """Monitorea el progreso del stress test"""
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration_seconds:
            elapsed = time.time() - start_time
            remaining = duration_seconds - elapsed
            
            progress = (elapsed / duration_seconds) * 100
            
            print(f"\r⏱️  Progreso: {progress:.1f}% | "
                  f"Facturas: {self.results['facturas_created']} | "
                  f"Stock: {self.results['stock_updates']} | "
                  f"Errores: {self.results['errors']} | "
                  f"Restante: {remaining:.0f}s", end="", flush=True)
            
            time.sleep(2)
        
        print()  # Nueva línea al final
    
    def _show_results(self):
        """Muestra los resultados del stress test"""
        print("\n" + "=" * 60)
        print("📊 RESULTADOS DEL STRESS TEST")
        print("=" * 60)
        
        if self.results['start_time'] and self.results['end_time']:
            duration = self.results['end_time'] - self.results['start_time']
            duration_seconds = duration.total_seconds()
            
            print(f"⏱️  Duración real: {duration_seconds:.1f} segundos")
            print(f"📊 Facturas creadas: {self.results['facturas_created']}")
            print(f"🔄 Actualizaciones de stock: {self.results['stock_updates']}")
            print(f"❌ Errores: {self.results['errors']}")
            
            # Métricas de performance
            if duration_seconds > 0:
                facturas_per_second = self.results['facturas_created'] / duration_seconds
                stock_per_second = self.results['stock_updates'] / duration_seconds
                
                print(f"\n📈 MÉTRICAS DE PERFORMANCE:")
                print(f"   • Facturas/segundo: {facturas_per_second:.2f}")
                print(f"   • Actualizaciones stock/segundo: {stock_per_second:.2f}")
                
                if self.results['facturas_created'] > 0:
                    error_rate = (self.results['errors'] / self.results['facturas_created']) * 100
                    print(f"   • Tasa de error: {error_rate:.2f}%")
                    
                    stock_ratio = self.results['stock_updates'] / self.results['facturas_created']
                    print(f"   • Ratio stock/factura: {stock_ratio:.2f}")
            
            # Análisis de resultados
            print(f"\n🎯 ANÁLISIS:")
            
            if self.results['errors'] == 0:
                print(f"   ✅ Sin errores durante el stress test")
                print(f"   ✅ Sistema estable bajo carga")
            elif self.results['errors'] < self.results['facturas_created'] * 0.05:
                print(f"   ⚠️ Pocos errores ({self.results['errors']}) - Aceptable")
            else:
                print(f"   ❌ Muchos errores ({self.results['errors']}) - Revisar estabilidad")
            
            if facturas_per_second >= 0.5:
                print(f"   ✅ Throughput bueno ({facturas_per_second:.2f} facturas/s)")
            elif facturas_per_second >= 0.2:
                print(f"   ⚠️ Throughput moderado ({facturas_per_second:.2f} facturas/s)")
            else:
                print(f"   ❌ Throughput bajo ({facturas_per_second:.2f} facturas/s)")
            
            if stock_ratio >= 0.8:
                print(f"   ✅ Stock se actualiza correctamente")
            else:
                print(f"   ⚠️ Algunas facturas no actualizaron stock")
            
            # Recomendaciones
            print(f"\n💡 RECOMENDACIONES:")
            
            if self.results['errors'] > 0:
                print(f"   • Revisar logs para identificar causas de errores")
                print(f"   • Considerar manejo de concurrencia mejorado")
            
            if facturas_per_second < 0.3:
                print(f"   • Optimizar operaciones de base de datos")
                print(f"   • Considerar índices adicionales")
            
            if stock_ratio < 0.9:
                print(f"   • Verificar transacciones de stock")
                print(f"   • Mejorar manejo de errores en actualización")
            
            # Estado final
            total_operations = self.results['facturas_created'] + self.results['stock_updates']
            success_rate = ((total_operations - self.results['errors']) / max(total_operations, 1)) * 100
            
            print(f"\n📊 RESULTADO GENERAL:")
            if success_rate >= 95:
                print(f"   🎉 EXCELENTE ({success_rate:.1f}% éxito)")
                print(f"   Sistema muy estable bajo carga")
            elif success_rate >= 85:
                print(f"   ✅ BUENO ({success_rate:.1f}% éxito)")
                print(f"   Sistema estable con mejoras menores")
            elif success_rate >= 70:
                print(f"   ⚠️ ACEPTABLE ({success_rate:.1f}% éxito)")
                print(f"   Sistema funcional pero necesita optimización")
            else:
                print(f"   ❌ INSUFICIENTE ({success_rate:.1f}% éxito)")
                print(f"   Sistema requiere mejoras significativas")

def main():
    """Función principal"""
    print("🚀 INICIANDO STRESS TEST")
    print("Este test simula carga alta en el sistema:")
    print("   • Múltiples threads creando facturas simultáneamente")
    print("   • Actualización concurrente de stock")
    print("   • Medición de performance bajo carga")
    print("   • Detección de errores y problemas de concurrencia")
    
    # Configuración del test
    duration = 3  # minutos
    threads = 2   # threads concurrentes
    
    print(f"\nConfiguración por defecto:")
    print(f"   • Duración: {duration} minutos")
    print(f"   • Threads: {threads}")
    
    response = input("\n¿Usar configuración por defecto? (s/n): ").lower().strip()
    
    if response == 'n':
        try:
            duration = int(input("Duración en minutos (1-10): "))
            duration = max(1, min(10, duration))
            
            threads = int(input("Número de threads (1-5): "))
            threads = max(1, min(5, threads))
        except ValueError:
            print("Usando configuración por defecto")
    
    stress_test = StressTest()
    stress_test.run_stress_test(duration, threads)

if __name__ == "__main__":
    main()
