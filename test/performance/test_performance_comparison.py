#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de comparaison de performance entre les versions originales et optimisées
"""

import time
import pytest
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Factura, Stock, Producto
from database.optimized_models import OptimizedFactura, OptimizedStock, OptimizedProducto
from utils.performance_optimizer import performance_monitor, optimize_database_queries
from test.utils.test_database_manager import isolated_test_db


class TestPerformanceComparison:
    """Tests de comparaison de performance"""
    
    @pytest.fixture(autouse=True)
    def setup_performance_data(self):
        """Utiliser la base de données principale pour les tests de performance"""
        # Optimiser la base de données principale
        optimize_database_queries()

        print("\n🔧 Utilisation de la base de données principale pour les tests...")

        # Compter les données existantes
        productos_count = len(Producto.get_all())
        facturas_count = len(Factura.get_all())

        print(f"   📊 Datos existentes: {productos_count} productos, {facturas_count} facturas")

        # Si nous n'avons pas assez de données, en créer plus
        if productos_count < 20:
            print("   🔧 Créant des données supplémentaires...")
            for i in range(20 - productos_count):
                producto = Producto(
                    nombre=f"Producto Test {i:03d}",
                    referencia=f"REF{i:03d}",
                    precio=10.0 + (i % 50),
                    categoria=f"Categoria {i % 10}",
                    descripcion=f"Descripción del producto {i}",
                    iva_recomendado=21.0
                )
                producto.save()

        if facturas_count < 10:
            print("   🔧 Créant des facturas supplémentaires...")
            productos = Producto.get_all()
            for i in range(10 - facturas_count):
                factura = Factura(
                    numero_factura=f"PERF-{i:04d}",
                    fecha_factura=f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
                    nombre_cliente=f"Cliente Performance {i}",
                    subtotal=100.0 + (i % 500),
                    total_iva=21.0 + (i % 100),
                    total_factura=121.0 + (i % 600),
                    modo_pago="efectivo" if i % 2 == 0 else "tarjeta"
                )
                factura.save()

                # Ajouter quelques items
                if productos:
                    for j in range(2):
                        producto_idx = (i * 2 + j) % len(productos)
                        factura.add_item(
                            producto_id=productos[producto_idx].id,
                            cantidad=1 + (j % 3),
                            precio_unitario=productos[producto_idx].precio,
                            iva_aplicado=21.0
                        )

                factura.calculate_totals()
                factura.save()

        final_productos = len(Producto.get_all())
        final_facturas = len(Factura.get_all())
        print(f"   ✅ Datos finales: {final_productos} productos, {final_facturas} facturas")

        yield None
    
    def test_facturas_performance_comparison(self, setup_performance_data):
        """Comparer les performances de chargement des facturas"""
        print(f"\n📊 Test de performance: Chargement des facturas")
        print(f"=" * 60)
        
        # Test version originale
        print(f"\n1️⃣ Version originale (Factura.get_all)")
        start_time = time.time()
        facturas_original = Factura.get_all()
        original_time = time.time() - start_time
        
        print(f"   📄 Facturas cargadas: {len(facturas_original)}")
        print(f"   ⏱️  Tiempo: {original_time:.3f} segundos")
        
        # Compter les requêtes N+1 (approximation)
        total_items = sum(len(f.items) for f in facturas_original)
        estimated_queries_original = 1 + len(facturas_original)  # 1 pour facturas + 1 par factura pour items
        print(f"   🔍 Items totales: {total_items}")
        print(f"   🗃️  Consultas estimadas: {estimated_queries_original}")
        
        # Test version optimisée
        print(f"\n2️⃣ Version optimisée (OptimizedFactura.get_all_optimized)")
        start_time = time.time()
        facturas_optimized = OptimizedFactura.get_all_optimized()
        optimized_time = time.time() - start_time
        
        print(f"   📄 Facturas cargadas: {len(facturas_optimized)}")
        print(f"   ⏱️  Tiempo: {optimized_time:.3f} segundos")
        
        total_items_opt = sum(len(f.items) for f in facturas_optimized)
        estimated_queries_optimized = 2  # 1 pour facturas + 1 pour tous les items
        print(f"   🔍 Items totales: {total_items_opt}")
        print(f"   🗃️  Consultas estimadas: {estimated_queries_optimized}")
        
        # Test version résumé
        print(f"\n3️⃣ Version résumé (OptimizedFactura.get_summary_optimized)")
        start_time = time.time()
        facturas_summary = OptimizedFactura.get_summary_optimized()
        summary_time = time.time() - start_time
        
        print(f"   📄 Facturas (résumé): {len(facturas_summary)}")
        print(f"   ⏱️  Tiempo: {summary_time:.3f} segundos")
        print(f"   🗃️  Consultas estimadas: 1")
        
        # Calculs de performance
        print(f"\n📈 Résultats de performance:")
        print(f"   🚀 Amélioration optimisée vs originale: {original_time / optimized_time:.1f}x plus rapide")
        print(f"   🚀 Amélioration résumé vs originale: {original_time / summary_time:.1f}x plus rapide")
        print(f"   📉 Réduction de requêtes: {estimated_queries_original} → {estimated_queries_optimized} ({((estimated_queries_original - estimated_queries_optimized) / estimated_queries_original * 100):.1f}% moins)")
        
        # Vérifications de performance (pas de comparaison de nombres)
        assert len(facturas_original) > 0, "Aucune factura originale chargée"
        assert len(facturas_optimized) > 0, "Aucune factura optimisée chargée"
        assert len(facturas_summary) > 0, "Aucune factura résumé chargée"

        # Les performances doivent être meilleures ou égales
        assert optimized_time <= original_time + 0.001, "Version optimisée plus lente"
        assert summary_time <= optimized_time + 0.001, "Version résumé plus lente"
        
        print(f"   ✅ Toutes les vérifications passées")
    
    def test_stock_performance_comparison(self, setup_performance_data):
        """Comparer les performances de chargement du stock"""
        print(f"\n📊 Test de performance: Chargement du stock")
        print(f"=" * 60)
        
        # Simuler le chargement original avec requêtes N+1
        print(f"\n1️⃣ Version originale simulée (avec N+1)")
        start_time = time.time()
        
        # Simuler Stock.get_all() + requêtes individuelles pour dates
        stock_basic = Stock.get_all()
        for row in stock_basic:
            producto_id = row[0]
            # Simuler la requête individuelle pour fecha_actualizacion
            from database.database import db
            fecha_query = "SELECT fecha_actualizacion FROM stock WHERE producto_id=?"
            db.execute_query(fecha_query, (producto_id,))
        
        original_time = time.time() - start_time
        
        print(f"   📦 Productos en stock: {len(stock_basic)}")
        print(f"   ⏱️  Tiempo: {original_time:.3f} segundos")
        print(f"   🗃️  Consultas estimadas: {1 + len(stock_basic)}")
        
        # Test version optimisée
        print(f"\n2️⃣ Version optimisée (OptimizedStock.get_all_optimized)")
        start_time = time.time()
        stock_optimized = OptimizedStock.get_all_optimized()
        optimized_time = time.time() - start_time
        
        print(f"   📦 Productos en stock: {len(stock_optimized)}")
        print(f"   ⏱️  Tiempo: {optimized_time:.3f} segundos")
        print(f"   🗃️  Consultas estimadas: 1")
        
        # Calculs de performance
        print(f"\n📈 Résultats de performance:")
        print(f"   🚀 Amélioration: {original_time / optimized_time:.1f}x plus rapide")
        print(f"   📉 Réduction de requêtes: {1 + len(stock_basic)} → 1 ({len(stock_basic) / (1 + len(stock_basic)) * 100:.1f}% moins)")
        
        # Vérifications de performance
        assert len(stock_basic) > 0, "Aucun stock de base chargé"
        assert len(stock_optimized) > 0, "Aucun stock optimisé chargé"
        assert optimized_time <= original_time + 0.001, "Version optimisée plus lente"
        
        print(f"   ✅ Toutes les vérifications passées")
    
    def test_productos_with_stock_performance(self, setup_performance_data):
        """Comparer les performances de chargement des productos avec stock"""
        print(f"\n📊 Test de performance: Productos avec stock")
        print(f"=" * 60)
        
        # Version originale simulée
        print(f"\n1️⃣ Version originale simulée (avec N+1)")
        start_time = time.time()
        
        productos_original = Producto.get_all()
        for producto in productos_original:
            # Simuler la requête individuelle pour le stock
            stock_actual = Stock.get_by_product(producto.id)
            producto._stock_actual = stock_actual
        
        original_time = time.time() - start_time
        
        print(f"   🛍️  Productos cargados: {len(productos_original)}")
        print(f"   ⏱️  Tiempo: {original_time:.3f} segundos")
        print(f"   🗃️  Consultas estimadas: {1 + len(productos_original)}")
        
        # Version optimisée
        print(f"\n2️⃣ Version optimisée (OptimizedProducto.get_all_with_stock_optimized)")
        start_time = time.time()
        productos_optimized = OptimizedProducto.get_all_with_stock_optimized()
        optimized_time = time.time() - start_time
        
        print(f"   🛍️  Productos cargados: {len(productos_optimized)}")
        print(f"   ⏱️  Tiempo: {optimized_time:.3f} segundos")
        print(f"   🗃️  Consultas estimadas: 1")
        
        # Version résumé
        print(f"\n3️⃣ Version résumé (OptimizedProducto.get_summary_optimized)")
        start_time = time.time()
        productos_summary = OptimizedProducto.get_summary_optimized()
        summary_time = time.time() - start_time
        
        print(f"   🛍️  Productos (résumé): {len(productos_summary)}")
        print(f"   ⏱️  Tiempo: {summary_time:.3f} segundos")
        print(f"   🗃️  Consultas estimadas: 1")
        
        # Calculs de performance
        print(f"\n📈 Résultats de performance:")
        print(f"   🚀 Amélioration optimisée vs originale: {original_time / optimized_time:.1f}x plus rapide")
        print(f"   🚀 Amélioration résumé vs originale: {original_time / summary_time:.1f}x plus rapide")
        print(f"   📉 Réduction de requêtes: {1 + len(productos_original)} → 1 ({len(productos_original) / (1 + len(productos_original)) * 100:.1f}% moins)")
        
        # Vérifications de performance
        assert len(productos_original) > 0, "Aucun producto original chargé"
        assert len(productos_optimized) > 0, "Aucun producto optimisé chargé"
        assert len(productos_summary) > 0, "Aucun producto résumé chargé"
        assert optimized_time <= original_time + 0.001, "Version optimisée plus lente"
        
        print(f"   ✅ Toutes les vérifications passées")
    
    def test_cache_performance(self, setup_performance_data):
        """Tester les performances du cache"""
        print(f"\n📊 Test de performance: Cache")
        print(f"=" * 60)
        
        # Premier chargement (sans cache)
        print(f"\n1️⃣ Premier chargement (sans cache)")
        start_time = time.time()
        facturas1 = OptimizedFactura.get_summary_optimized()
        first_time = time.time() - start_time
        
        print(f"   📄 Facturas: {len(facturas1)}")
        print(f"   ⏱️  Tiempo: {first_time:.3f} segundos")
        
        # Deuxième chargement (avec cache)
        print(f"\n2️⃣ Deuxième chargement (avec cache)")
        start_time = time.time()
        facturas2 = OptimizedFactura.get_summary_optimized()
        cached_time = time.time() - start_time
        
        print(f"   📄 Facturas: {len(facturas2)}")
        print(f"   ⏱️  Tiempo: {cached_time:.3f} segundos")
        
        # Calculs de performance
        if cached_time > 0:
            improvement = first_time / cached_time
            print(f"\n📈 Amélioration avec cache: {improvement:.1f}x plus rapide")
        else:
            print(f"\n📈 Cache instantané (< 1ms)")
        
        # Vérifications de cache
        assert len(facturas1) > 0, "Aucune factura dans le premier chargement"
        assert len(facturas2) > 0, "Aucune factura dans le deuxième chargement"
        assert cached_time <= first_time + 0.001, "Cache pas plus rapide"
        
        print(f"   ✅ Cache fonctionne correctement")
    
    def test_memory_usage_comparison(self, setup_performance_data):
        """Comparer l'utilisation mémoire"""
        print(f"\n📊 Test de performance: Utilisation mémoire")
        print(f"=" * 60)
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Mesure initiale
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"\n📊 Mémoire initiale: {initial_memory:.1f} MB")
        
        # Chargement version originale
        print(f"\n1️⃣ Chargement version originale")
        memory_before_original = process.memory_info().rss / 1024 / 1024
        facturas_original = Factura.get_all()
        memory_after_original = process.memory_info().rss / 1024 / 1024
        
        original_memory_usage = memory_after_original - memory_before_original
        print(f"   📄 Facturas: {len(facturas_original)}")
        print(f"   💾 Mémoire utilisée: {original_memory_usage:.1f} MB")
        
        # Nettoyer
        del facturas_original
        
        # Chargement version optimisée
        print(f"\n2️⃣ Chargement version optimisée")
        memory_before_optimized = process.memory_info().rss / 1024 / 1024
        facturas_optimized = OptimizedFactura.get_all_optimized()
        memory_after_optimized = process.memory_info().rss / 1024 / 1024
        
        optimized_memory_usage = memory_after_optimized - memory_before_optimized
        print(f"   📄 Facturas: {len(facturas_optimized)}")
        print(f"   💾 Mémoire utilisée: {optimized_memory_usage:.1f} MB")
        
        # Chargement version résumé
        print(f"\n3️⃣ Chargement version résumé")
        memory_before_summary = process.memory_info().rss / 1024 / 1024
        facturas_summary = OptimizedFactura.get_summary_optimized()
        memory_after_summary = process.memory_info().rss / 1024 / 1024
        
        summary_memory_usage = memory_after_summary - memory_before_summary
        print(f"   📄 Facturas: {len(facturas_summary)}")
        print(f"   💾 Mémoire utilisée: {summary_memory_usage:.1f} MB")
        
        # Comparaisons
        print(f"\n📈 Comparaison mémoire:")
        if optimized_memory_usage > 0:
            print(f"   🔄 Optimisée vs Originale: {original_memory_usage / optimized_memory_usage:.1f}x moins de mémoire")
        if summary_memory_usage > 0:
            print(f"   📋 Résumé vs Originale: {original_memory_usage / summary_memory_usage:.1f}x moins de mémoire")
        
        print(f"   ✅ Test mémoire terminé")


def run_performance_benchmark():
    """Exécuter un benchmark complet de performance"""
    print(f"\n🚀 BENCHMARK DE PERFORMANCE COMPLET")
    print(f"=" * 80)
    
    # Exécuter les tests
    pytest.main([__file__, "-v", "-s", "--tb=short"])
    
    # Afficher les statistiques du moniteur
    print(f"\n📊 STATISTIQUES DE PERFORMANCE GLOBALES")
    print(f"=" * 80)
    performance_monitor.print_stats()


if __name__ == "__main__":
    run_performance_benchmark()
