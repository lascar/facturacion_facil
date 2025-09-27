#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration des améliorations de performance
"""

import time
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Factura, Stock, Producto
from database.optimized_models import OptimizedFactura, OptimizedStock, OptimizedProducto
from utils.performance_optimizer import performance_monitor, optimize_database_queries


def demo_performance_comparison():
    """Démonstration comparative des performances"""
    print("🚀 DÉMONSTRATION DES AMÉLIORATIONS DE PERFORMANCE")
    print("=" * 70)
    print("Cette démonstration compare les performances avant et après optimisation")
    print()
    
    # Optimiser la base de données
    print("🔧 Optimisation de la base de données...")
    optimize_database_queries()
    print("✅ Index créés")
    print()
    
    # Test 1: Facturas
    print("📊 TEST 1: CHARGEMENT DES FACTURAS")
    print("-" * 50)
    
    # Version originale
    print("🐌 Version originale (avec problèmes N+1):")
    start_time = time.time()
    facturas_original = Factura.get_all()
    original_time = time.time() - start_time
    
    total_items_original = sum(len(f.items) for f in facturas_original)
    print(f"   📄 Facturas chargées: {len(facturas_original)}")
    print(f"   🛒 Items totaux: {total_items_original}")
    print(f"   ⏱️  Temps: {original_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimées: {1 + len(facturas_original)} (N+1)")
    
    # Version optimisée
    print("\n🚀 Version optimisée (requêtes optimisées):")
    start_time = time.time()
    facturas_optimized = OptimizedFactura.get_all_optimized()
    optimized_time = time.time() - start_time
    
    total_items_optimized = sum(len(f.items) for f in facturas_optimized)
    print(f"   📄 Facturas chargées: {len(facturas_optimized)}")
    print(f"   🛒 Items totaux: {total_items_optimized}")
    print(f"   ⏱️  Temps: {optimized_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimées: 2 (optimisées)")
    
    # Version résumé
    print("\n⚡ Version résumé (affichage rapide):")
    start_time = time.time()
    facturas_summary = OptimizedFactura.get_summary_optimized()
    summary_time = time.time() - start_time
    
    print(f"   📄 Facturas (résumé): {len(facturas_summary)}")
    print(f"   ⏱️  Temps: {summary_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimées: 1 (résumé)")
    
    # Calculs de performance
    if optimized_time > 0:
        improvement_opt = original_time / optimized_time
        print(f"\n📈 AMÉLIORATION OPTIMISÉE: {improvement_opt:.1f}x plus rapide")
    
    if summary_time > 0:
        improvement_sum = original_time / summary_time
        print(f"📈 AMÉLIORATION RÉSUMÉ: {improvement_sum:.1f}x plus rapide")
    
    print()
    
    # Test 2: Stock
    print("📊 TEST 2: CHARGEMENT DU STOCK")
    print("-" * 50)
    
    # Version originale simulée
    print("🐌 Version originale (avec N+1 simulé):")
    start_time = time.time()
    stock_basic = Stock.get_all()
    # Simuler les requêtes N+1 pour les dates
    for row in stock_basic:
        producto_id = row[0]
        # Simuler la requête individuelle
        from database.database import db
        fecha_query = "SELECT fecha_actualizacion FROM stock WHERE producto_id=?"
        db.execute_query(fecha_query, (producto_id,))
    
    stock_original_time = time.time() - start_time
    
    print(f"   📦 Productos en stock: {len(stock_basic)}")
    print(f"   ⏱️  Temps: {stock_original_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimées: {1 + len(stock_basic)} (N+1)")
    
    # Version optimisée
    print("\n🚀 Version optimisée (JOIN optimisé):")
    start_time = time.time()
    stock_optimized = OptimizedStock.get_all_optimized()
    stock_optimized_time = time.time() - start_time
    
    print(f"   📦 Productos en stock: {len(stock_optimized)}")
    print(f"   ⏱️  Temps: {stock_optimized_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimées: 1 (JOIN)")
    
    # Calculs de performance
    if stock_optimized_time > 0:
        stock_improvement = stock_original_time / stock_optimized_time
        print(f"\n📈 AMÉLIORATION STOCK: {stock_improvement:.1f}x plus rapide")
    
    print()
    
    # Test 3: Productos avec stock
    print("📊 TEST 3: PRODUCTOS AVEC STOCK")
    print("-" * 50)
    
    # Version originale simulée
    print("🐌 Version originale (avec N+1 simulé):")
    start_time = time.time()
    productos_original = Producto.get_all()
    for producto in productos_original:
        # Simuler la requête individuelle pour le stock
        stock_actual = Stock.get_by_product(producto.id)
        producto._stock_actual = stock_actual
    
    productos_original_time = time.time() - start_time
    
    print(f"   🛍️  Productos chargés: {len(productos_original)}")
    print(f"   ⏱️  Temps: {productos_original_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimées: {1 + len(productos_original)} (N+1)")
    
    # Version optimisée
    print("\n🚀 Version optimisée (LEFT JOIN):")
    start_time = time.time()
    productos_optimized = OptimizedProducto.get_all_with_stock_optimized()
    productos_optimized_time = time.time() - start_time
    
    print(f"   🛍️  Productos chargés: {len(productos_optimized)}")
    print(f"   ⏱️  Temps: {productos_optimized_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimadas: 1 (LEFT JOIN)")
    
    # Version résumé
    print("\n⚡ Version résumé (affichage rapide):")
    start_time = time.time()
    productos_summary = OptimizedProducto.get_summary_optimized()
    productos_summary_time = time.time() - start_time
    
    print(f"   🛍️  Productos (résumé): {len(productos_summary)}")
    print(f"   ⏱️  Temps: {productos_summary_time:.3f} secondes")
    print(f"   🗃️  Requêtes estimadas: 1 (résumé)")
    
    # Calculs de performance
    if productos_optimized_time > 0:
        productos_improvement = productos_original_time / productos_optimized_time
        print(f"\n📈 AMÉLIORATION PRODUCTOS: {productos_improvement:.1f}x plus rapide")
    
    print()
    
    # Test 4: Cache
    print("📊 TEST 4: PERFORMANCE DU CACHE")
    print("-" * 50)
    
    # Premier chargement (sans cache)
    print("🔄 Premier chargement (sans cache):")
    start_time = time.time()
    facturas_cache_1 = OptimizedFactura.get_summary_optimized()
    cache_first_time = time.time() - start_time
    
    print(f"   📄 Facturas: {len(facturas_cache_1)}")
    print(f"   ⏱️  Temps: {cache_first_time:.3f} secondes")
    
    # Deuxième chargement (avec cache)
    print("\n⚡ Deuxième chargement (avec cache):")
    start_time = time.time()
    facturas_cache_2 = OptimizedFactura.get_summary_optimized()
    cache_second_time = time.time() - start_time
    
    print(f"   📄 Facturas: {len(facturas_cache_2)}")
    print(f"   ⏱️  Temps: {cache_second_time:.3f} secondes")
    
    # Calculs de performance du cache
    if cache_second_time > 0:
        cache_improvement = cache_first_time / cache_second_time
        print(f"\n📈 AMÉLIORATION CACHE: {cache_improvement:.1f}x plus rapide")
    else:
        print(f"\n📈 CACHE INSTANTANÉ: < 1ms")
    
    print()
    
    # Résumé final
    print("🎉 RÉSUMÉ DES AMÉLIORATIONS")
    print("=" * 70)
    
    improvements = []
    
    if optimized_time > 0:
        improvements.append(f"📄 Facturas optimisées: {original_time / optimized_time:.1f}x plus rapide")
    
    if summary_time > 0:
        improvements.append(f"📄 Facturas résumé: {original_time / summary_time:.1f}x plus rapide")
    
    if stock_optimized_time > 0:
        improvements.append(f"📦 Stock optimisé: {stock_original_time / stock_optimized_time:.1f}x plus rapide")
    
    if productos_optimized_time > 0:
        improvements.append(f"🛍️  Productos optimisés: {productos_original_time / productos_optimized_time:.1f}x plus rapide")
    
    for improvement in improvements:
        print(f"   🚀 {improvement}")
    
    print(f"\n📉 Réduction de requêtes:")
    print(f"   🗃️  Facturas: {1 + len(facturas_original)} → 2 requêtes ({((1 + len(facturas_original) - 2) / (1 + len(facturas_original)) * 100):.0f}% moins)")
    print(f"   🗃️  Stock: {1 + len(stock_basic)} → 1 requête ({len(stock_basic) / (1 + len(stock_basic)) * 100:.0f}% moins)")
    print(f"   🗃️  Productos: {1 + len(productos_original)} → 1 requête ({len(productos_original) / (1 + len(productos_original)) * 100:.0f}% moins)")
    
    print(f"\n💡 IMPACT UTILISATEUR:")
    print(f"   ⚡ Chargement quasi-instantané des listes")
    print(f"   🔍 Recherche en temps réel sans latence")
    print(f"   📱 Interface fluide même avec des milliers d'enregistrements")
    print(f"   🚀 Expérience utilisateur transformée!")
    
    print(f"\n🔧 POUR APPLIQUER CES OPTIMISATIONS:")
    print(f"   python utils/apply_performance_optimizations.py")
    
    # Afficher les statistiques du moniteur
    print(f"\n📊 STATISTIQUES DÉTAILLÉES:")
    print("=" * 70)
    performance_monitor.print_stats()


def demo_cache_behavior():
    """Démonstration du comportement du cache"""
    print("\n🔄 DÉMONSTRATION DU CACHE")
    print("=" * 50)
    
    from utils.performance_optimizer import performance_optimizer
    
    # Vider le cache
    performance_optimizer.clear_cache()
    print("🧹 Cache vidé")
    
    # Test avec différents TTL
    print("\n⏰ Test avec TTL court (5 secondes):")
    
    @performance_optimizer.cache_result("demo_cache", ttl=5)
    def slow_function():
        time.sleep(0.1)  # Simuler une opération lente
        return "Résultat calculé"
    
    # Premier appel
    start = time.time()
    result1 = slow_function()
    time1 = time.time() - start
    print(f"   1er appel: {time1:.3f}s - {result1}")
    
    # Deuxième appel (cache)
    start = time.time()
    result2 = slow_function()
    time2 = time.time() - start
    print(f"   2ème appel: {time2:.3f}s - {result2} (cache)")
    
    # Attendre expiration
    print("   ⏳ Attente expiration cache (5s)...")
    time.sleep(5.1)
    
    # Troisième appel (cache expiré)
    start = time.time()
    result3 = slow_function()
    time3 = time.time() - start
    print(f"   3ème appel: {time3:.3f}s - {result3} (cache expiré)")
    
    print(f"\n📈 Amélioration cache: {time1 / time2:.1f}x plus rapide")


if __name__ == "__main__":
    try:
        demo_performance_comparison()
        demo_cache_behavior()
        
        print(f"\n🎉 DÉMONSTRATION TERMINÉE!")
        print(f"Les optimisations de performance sont prêtes à être appliquées.")
        
    except Exception as e:
        print(f"\n❌ Erreur pendant la démonstration: {e}")
        import traceback
        traceback.print_exc()
