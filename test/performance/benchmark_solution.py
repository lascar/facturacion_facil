#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Benchmark de performance de la solución completa
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import statistics
from datetime import datetime
from database.database import db
from database.models import Producto, Stock, Factura, FacturaItem
from ui.facturas_methods import FacturasMethodsMixin
from utils.logger import get_logger

class PerformanceBenchmark:
    """Benchmark de performance del sistema"""
    
    def __init__(self):
        self.logger = get_logger("performance_benchmark")
        self.results = {}
        
        # Mock para tests
        class MockWindow:
            def __init__(self):
                pass
        
        class TestableFacturasMethodsMixin(FacturasMethodsMixin):
            def __init__(self):
                self.logger = get_logger("benchmark_test")
                self.selected_factura = None
                self.window = MockWindow()
            
            def _show_message(self, msg_type, title, message):
                return True
        
        self.test_instance = TestableFacturasMethodsMixin()
    
    def run_benchmark(self):
        """Ejecuta el benchmark completo"""
        print("⚡ BENCHMARK DE PERFORMANCE - Facturación Fácil")
        print("=" * 60)
        
        # Inicializar base de datos
        db.init_database()
        
        # Tests de performance
        self.benchmark_database_operations()
        self.benchmark_factura_operations()
        self.benchmark_stock_operations()
        self.benchmark_pdf_operations()
        
        # Mostrar resultados
        self.show_results()
    
    def benchmark_database_operations(self):
        """Benchmark de operaciones de base de datos"""
        print("\n1️⃣ BENCHMARK - Operaciones de Base de Datos")
        print("-" * 50)
        
        # Test 1: Lectura de productos
        times = []
        for i in range(10):
            start_time = time.time()
            productos = Producto.get_all()
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['db_read_productos'] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'count': len(productos) if productos else 0
        }
        
        print(f"   📊 Lectura de productos:")
        print(f"      Tiempo promedio: {self.results['db_read_productos']['avg_time']:.4f}s")
        print(f"      Productos leídos: {self.results['db_read_productos']['count']}")
        
        # Test 2: Lectura de facturas
        times = []
        for i in range(10):
            start_time = time.time()
            facturas = Factura.get_all()
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['db_read_facturas'] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'count': len(facturas) if facturas else 0
        }
        
        print(f"   📋 Lectura de facturas:")
        print(f"      Tiempo promedio: {self.results['db_read_facturas']['avg_time']:.4f}s")
        print(f"      Facturas leídas: {self.results['db_read_facturas']['count']}")
        
        # Test 3: Búsqueda por número de factura
        if facturas and len(facturas) > 0:
            primera_factura = facturas[0]
            times = []
            for i in range(20):
                start_time = time.time()
                factura_found = Factura.get_by_numero(primera_factura.numero_factura)
                end_time = time.time()
                times.append(end_time - start_time)
            
            self.results['db_search_factura'] = {
                'avg_time': statistics.mean(times),
                'min_time': min(times),
                'max_time': max(times),
                'success': factura_found is not None
            }
            
            print(f"   🔍 Búsqueda por número:")
            print(f"      Tiempo promedio: {self.results['db_search_factura']['avg_time']:.4f}s")
            print(f"      Éxito: {'✅' if self.results['db_search_factura']['success'] else '❌'}")
    
    def benchmark_factura_operations(self):
        """Benchmark de operaciones de factura"""
        print("\n2️⃣ BENCHMARK - Operaciones de Factura")
        print("-" * 50)
        
        # Crear factura de test
        productos = Producto.get_all()
        if not productos:
            print("   ⚠️ No hay productos para test de facturas")
            return
        
        # Test 1: Creación de factura
        times = []
        facturas_test = []
        
        for i in range(5):  # Crear 5 facturas de test
            start_time = time.time()
            
            factura = Factura(
                numero_factura=f"BENCH-{int(time.time())}-{i}",
                nombre_cliente=f"Cliente Benchmark {i}",
                fecha_factura=datetime.now().strftime("%Y-%m-%d"),
                subtotal=100.0,
                total_iva=21.0,
                total_factura=121.0
            )
            
            # Agregar item
            item = FacturaItem(
                producto_id=productos[0].id,
                cantidad=2,
                precio_unitario=50.0,
                iva_aplicado=21.0
            )
            item.calculate_totals()
            factura.items = [item]
            factura.calculate_totals()
            factura.save()
            
            end_time = time.time()
            times.append(end_time - start_time)
            facturas_test.append(factura)
        
        self.results['factura_creation'] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'count': len(facturas_test)
        }
        
        print(f"   📝 Creación de facturas:")
        print(f"      Tiempo promedio: {self.results['factura_creation']['avg_time']:.4f}s")
        print(f"      Facturas creadas: {self.results['factura_creation']['count']}")
        
        # Test 2: Carga de factura para edición
        if facturas_test:
            times = []
            for factura in facturas_test:
                start_time = time.time()
                factura_loaded = Factura.get_by_numero(factura.numero_factura)
                if factura_loaded:
                    # Simular carga en formulario
                    items_count = len(factura_loaded.items)
                end_time = time.time()
                times.append(end_time - start_time)
            
            self.results['factura_load'] = {
                'avg_time': statistics.mean(times),
                'min_time': min(times),
                'max_time': max(times)
            }
            
            print(f"   📂 Carga para edición:")
            print(f"      Tiempo promedio: {self.results['factura_load']['avg_time']:.4f}s")
        
        # Limpiar facturas de test
        for factura in facturas_test:
            try:
                factura.delete()
            except:
                pass
    
    def benchmark_stock_operations(self):
        """Benchmark de operaciones de stock"""
        print("\n3️⃣ BENCHMARK - Operaciones de Stock")
        print("-" * 50)
        
        productos = Producto.get_all()
        if not productos:
            print("   ⚠️ No hay productos para test de stock")
            return
        
        # Test 1: Lectura de stock
        times = []
        for i in range(20):
            start_time = time.time()
            stock_actual = Stock.get_by_product(productos[0].id)
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['stock_read'] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times)
        }
        
        print(f"   📊 Lectura de stock:")
        print(f"      Tiempo promedio: {self.results['stock_read']['avg_time']:.4f}s")
        
        # Test 2: Actualización de stock
        original_stock = Stock.get_by_product(productos[0].id)
        times = []
        
        for i in range(10):
            start_time = time.time()
            # Simular actualización
            new_stock = original_stock - 1
            Stock.update_stock(productos[0].id, new_stock, "VENTA", "Benchmark test")
            end_time = time.time()
            times.append(end_time - start_time)
            
            # Restaurar stock
            Stock.update_stock(productos[0].id, original_stock, "AJUSTE", "Restaurar benchmark")
        
        self.results['stock_update'] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times)
        }
        
        print(f"   🔄 Actualización de stock:")
        print(f"      Tiempo promedio: {self.results['stock_update']['avg_time']:.4f}s")
    
    def benchmark_pdf_operations(self):
        """Benchmark de operaciones PDF"""
        print("\n4️⃣ BENCHMARK - Operaciones PDF")
        print("-" * 50)
        
        facturas = Factura.get_all()
        if not facturas:
            print("   ⚠️ No hay facturas para test de PDF")
            return
        
        # Test 1: Selección de factura para PDF
        times = []
        for i in range(10):
            factura = facturas[i % len(facturas)]
            start_time = time.time()
            self.test_instance.selected_factura = factura
            # Verificar que la selección es válida
            is_valid = (self.test_instance.selected_factura is not None and 
                       hasattr(self.test_instance.selected_factura, 'numero_factura'))
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['pdf_selection'] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'success_rate': 1.0 if is_valid else 0.0
        }
        
        print(f"   📄 Selección para PDF:")
        print(f"      Tiempo promedio: {self.results['pdf_selection']['avg_time']:.4f}s")
        print(f"      Tasa de éxito: {self.results['pdf_selection']['success_rate']:.2%}")
        
        # Test 2: Validación de datos para PDF
        times = []
        for i in range(10):
            factura = facturas[i % len(facturas)]
            start_time = time.time()
            
            # Verificar campos requeridos
            required_fields = ['numero_factura', 'nombre_cliente', 'fecha_factura', 'total_factura']
            all_valid = all(hasattr(factura, field) and getattr(factura, field) for field in required_fields)
            has_items = hasattr(factura, 'items') and len(factura.items) > 0
            
            end_time = time.time()
            times.append(end_time - start_time)
        
        self.results['pdf_validation'] = {
            'avg_time': statistics.mean(times),
            'min_time': min(times),
            'max_time': max(times),
            'data_complete': all_valid and has_items
        }
        
        print(f"   ✅ Validación de datos:")
        print(f"      Tiempo promedio: {self.results['pdf_validation']['avg_time']:.4f}s")
        print(f"      Datos completos: {'✅' if self.results['pdf_validation']['data_complete'] else '❌'}")
    
    def show_results(self):
        """Muestra el resumen de resultados"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE BENCHMARK DE PERFORMANCE")
        print("=" * 60)
        
        # Análisis general
        total_operations = len(self.results)
        fast_operations = sum(1 for r in self.results.values() 
                             if isinstance(r, dict) and r.get('avg_time', 1) < 0.1)
        
        print(f"🎯 Operaciones analizadas: {total_operations}")
        print(f"⚡ Operaciones rápidas (<0.1s): {fast_operations}")
        print(f"📈 Ratio de performance: {fast_operations/total_operations:.2%}")
        
        # Operaciones más lentas
        slow_ops = [(name, data['avg_time']) for name, data in self.results.items() 
                   if isinstance(data, dict) and data.get('avg_time', 0) > 0.05]
        
        if slow_ops:
            slow_ops.sort(key=lambda x: x[1], reverse=True)
            print(f"\n⚠️ Operaciones más lentas:")
            for op_name, avg_time in slow_ops[:3]:
                print(f"   • {op_name}: {avg_time:.4f}s")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        
        db_read_time = self.results.get('db_read_facturas', {}).get('avg_time', 0)
        if db_read_time > 0.5:
            print(f"   • ⚠️ Lectura de facturas lenta ({db_read_time:.3f}s)")
            print(f"     - Considerar optimización de consultas")
            print(f"     - Implementar paginación para listas grandes")
        else:
            print(f"   • ✅ Lectura de base de datos eficiente")
        
        search_time = self.results.get('db_search_factura', {}).get('avg_time', 0)
        if search_time > 0.1:
            print(f"   • ⚠️ Búsqueda por número lenta ({search_time:.3f}s)")
            print(f"     - Considerar índices en base de datos")
        else:
            print(f"   • ✅ Búsqueda de facturas eficiente")
        
        stock_time = self.results.get('stock_update', {}).get('avg_time', 0)
        if stock_time > 0.2:
            print(f"   • ⚠️ Actualización de stock lenta ({stock_time:.3f}s)")
            print(f"     - Optimizar transacciones de stock")
        else:
            print(f"   • ✅ Actualización de stock eficiente")
        
        # Estado general
        if fast_operations / total_operations >= 0.8:
            print(f"\n🎉 PERFORMANCE EXCELENTE")
            print(f"   El sistema responde de manera eficiente")
        elif fast_operations / total_operations >= 0.6:
            print(f"\n✅ PERFORMANCE BUENA")
            print(f"   El sistema funciona correctamente")
        else:
            print(f"\n⚠️ PERFORMANCE MEJORABLE")
            print(f"   Considerar optimizaciones")
        
        print(f"\n📋 Benchmark completado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Función principal"""
    print("🚀 INICIANDO BENCHMARK DE PERFORMANCE")
    print("Este benchmark mide:")
    print("   • Velocidad de operaciones de base de datos")
    print("   • Performance de creación y carga de facturas")
    print("   • Eficiencia de operaciones de stock")
    print("   • Tiempo de selección y validación para PDF")
    
    benchmark = PerformanceBenchmark()
    benchmark.run_benchmark()

if __name__ == "__main__":
    main()
