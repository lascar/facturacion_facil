#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimiseur de performance pour l'application
"""

import time
import functools
from typing import List, Dict, Any, Optional
from database.database import db


class PerformanceOptimizer:
    """Classe pour optimiser les performances de l'application"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {}  # Time to live pour chaque cache
        self.default_ttl = 300  # 5 minutes par défaut
    
    def cache_result(self, key: str, ttl: int = None):
        """Décorateur pour mettre en cache les résultats"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{key}_{hash(str(args) + str(kwargs))}"
                current_time = time.time()
                
                # Vérifier si le cache est valide
                if (cache_key in self.cache and 
                    cache_key in self.cache_ttl and
                    current_time < self.cache_ttl[cache_key]):
                    return self.cache[cache_key]
                
                # Exécuter la fonction et mettre en cache
                result = func(*args, **kwargs)
                self.cache[cache_key] = result
                self.cache_ttl[cache_key] = current_time + (ttl or self.default_ttl)
                
                return result
            return wrapper
        return decorator
    
    def clear_cache(self, pattern: str = None):
        """Vider le cache (optionnellement par pattern)"""
        if pattern:
            keys_to_remove = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_remove:
                self.cache.pop(key, None)
                self.cache_ttl.pop(key, None)
        else:
            self.cache.clear()
            self.cache_ttl.clear()


class OptimizedQueries:
    """Requêtes optimisées pour éviter les problèmes N+1"""
    
    @staticmethod
    def get_all_facturas_optimized():
        """Obtient toutes les facturas avec leurs items en une seule requête"""
        # Requête principale pour les facturas
        facturas_query = """
            SELECT f.id, f.numero_factura, f.fecha_factura, f.nombre_cliente,
                   f.dni_nie_cliente, f.direccion_cliente, f.email_cliente, f.telefono_cliente,
                   f.subtotal, f.total_iva, f.total_factura, f.modo_pago, f.fecha_creacion
            FROM facturas f
            ORDER BY f.fecha_factura DESC, f.numero_factura DESC
        """
        
        # Requête pour tous les items de toutes las facturas
        items_query = """
            SELECT fi.id, fi.factura_id, fi.producto_id, fi.cantidad,
                   fi.precio_unitario, fi.iva_aplicado, fi.descuento,
                   fi.subtotal, fi.descuento_amount, fi.iva_amount, fi.total,
                   p.nombre as producto_nombre, p.referencia as producto_referencia
            FROM factura_items fi
            LEFT JOIN productos p ON fi.producto_id = p.id
            ORDER BY fi.factura_id, fi.id
        """
        
        facturas_results = db.execute_query(facturas_query)
        items_results = db.execute_query(items_query)
        
        # Organizar items por factura_id
        items_by_factura = {}
        for item_row in items_results:
            factura_id = item_row[1]
            if factura_id not in items_by_factura:
                items_by_factura[factura_id] = []
            
            from database.models import FacturaItem
            item = FacturaItem(
                id=item_row[0], factura_id=item_row[1], producto_id=item_row[2],
                cantidad=item_row[3], precio_unitario=item_row[4], iva_aplicado=item_row[5],
                descuento=item_row[6]
            )
            # Valores calculados
            item.subtotal = item_row[7]
            item.descuento_amount = item_row[8]
            item.iva_amount = item_row[9]
            item.total = item_row[10]
            
            # Información del producto (evita otra consulta)
            if item_row[11]:  # Si hay nombre de producto
                from database.models import Producto
                item.producto = Producto(
                    id=item_row[2], nombre=item_row[11], referencia=item_row[12]
                )
            
            items_by_factura[factura_id].append(item)
        
        # Crear facturas con sus items
        facturas = []
        for row in facturas_results:
            from database.models import Factura
            factura = Factura(
                id=row[0], numero_factura=row[1], fecha_factura=row[2], nombre_cliente=row[3],
                dni_nie_cliente=row[4], direccion_cliente=row[5], email_cliente=row[6],
                telefono_cliente=row[7], subtotal=row[8], total_iva=row[9], total_factura=row[10],
                modo_pago=row[11], fecha_creacion=row[12]
            )
            # Asignar items (sin consulta adicional)
            factura.items = items_by_factura.get(factura.id, [])
            facturas.append(factura)
        
        return facturas
    
    @staticmethod
    def get_all_stock_optimized():
        """Obtient tout le stock avec informations complètes en une seule requête"""
        query = """
            SELECT s.producto_id, s.cantidad_disponible, s.fecha_actualizacion,
                   p.nombre, p.referencia, p.precio, p.categoria
            FROM stock s 
            JOIN productos p ON s.producto_id = p.id 
            ORDER BY p.nombre
        """
        
        results = db.execute_query(query)
        stock_data = []
        
        for row in results:
            stock_data.append({
                'producto_id': row[0],
                'cantidad': row[1],
                'fecha_actualizacion': row[2] or "N/A",
                'nombre': row[3],
                'referencia': row[4],
                'precio': row[5],
                'categoria': row[6]
            })
        
        return stock_data
    
    @staticmethod
    def get_all_productos_with_stock():
        """Obtient tous les productos avec leur stock en une seule requête"""
        query = """
            SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria, 
                   p.descripcion, p.imagen_path, p.iva_recomendado,
                   COALESCE(s.cantidad_disponible, 0) as stock_actual
            FROM productos p
            LEFT JOIN stock s ON p.id = s.producto_id
            ORDER BY p.nombre
        """
        
        results = db.execute_query(query)
        productos = []
        
        for row in results:
            from database.models import Producto
            producto = Producto(
                id=row[0], nombre=row[1], referencia=row[2], precio=row[3],
                categoria=row[4], descripcion=row[5], imagen_path=row[6],
                iva_recomendado=row[7]
            )
            # Ajouter le stock sans requête supplémentaire
            producto._stock_actual = row[8]
            productos.append(producto)
        
        return productos


class VirtualizedList:
    """Liste virtualisée pour afficher de grandes quantités de données"""
    
    def __init__(self, container, item_height=50, visible_items=20):
        self.container = container
        self.item_height = item_height
        self.visible_items = visible_items
        self.data = []
        self.filtered_data = []
        self.scroll_position = 0
        self.rendered_items = {}
        
    def set_data(self, data: List[Dict]):
        """Définir les données à afficher"""
        self.data = data
        self.filtered_data = data.copy()
        self.scroll_position = 0
        self.update_display()
    
    def filter_data(self, filter_func):
        """Filtrer les données"""
        self.filtered_data = [item for item in self.data if filter_func(item)]
        self.scroll_position = 0
        self.update_display()
    
    def update_display(self):
        """Mettre à jour l'affichage (seulement les éléments visibles)"""
        # Calculer quels éléments sont visibles
        start_index = max(0, self.scroll_position)
        end_index = min(len(self.filtered_data), start_index + self.visible_items)
        
        # Nettoyer les éléments non visibles
        for index in list(self.rendered_items.keys()):
            if index < start_index or index >= end_index:
                widget = self.rendered_items.pop(index)
                widget.destroy()
        
        # Créer les nouveaux éléments visibles
        for index in range(start_index, end_index):
            if index not in self.rendered_items:
                item_data = self.filtered_data[index]
                widget = self.create_item_widget(item_data, index)
                self.rendered_items[index] = widget
    
    def create_item_widget(self, item_data: Dict, index: int):
        """Créer un widget pour un élément (à surcharger)"""
        import customtkinter as ctk
        frame = ctk.CTkFrame(self.container)
        frame.pack(fill="x", padx=5, pady=2)
        
        label = ctk.CTkLabel(frame, text=str(item_data))
        label.pack(side="left", padx=10, pady=5)
        
        return frame
    
    def on_scroll(self, event):
        """Gérer le défilement"""
        # Calculer la nouvelle position
        delta = -1 * (event.delta / 120)  # Windows
        if event.num == 4:  # Linux scroll up
            delta = -1
        elif event.num == 5:  # Linux scroll down
            delta = 1
        
        new_position = self.scroll_position + delta
        new_position = max(0, min(len(self.filtered_data) - self.visible_items, new_position))
        
        if new_position != self.scroll_position:
            self.scroll_position = new_position
            self.update_display()


class PerformanceMonitor:
    """Moniteur de performance pour identifier les goulots d'étranglement"""
    
    def __init__(self):
        self.timings = {}
        self.call_counts = {}
    
    def time_function(self, name: str):
        """Décorateur pour mesurer le temps d'exécution"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                
                execution_time = end_time - start_time
                
                if name not in self.timings:
                    self.timings[name] = []
                    self.call_counts[name] = 0
                
                self.timings[name].append(execution_time)
                self.call_counts[name] += 1
                
                # Log si l'exécution est lente
                if execution_time > 0.1:  # Plus de 100ms
                    print(f"⚠️ Fonction lente: {name} - {execution_time:.3f}s")
                
                return result
            return wrapper
        return decorator
    
    def get_stats(self):
        """Obtenir les statistiques de performance"""
        stats = {}
        for name, times in self.timings.items():
            stats[name] = {
                'calls': self.call_counts[name],
                'total_time': sum(times),
                'avg_time': sum(times) / len(times),
                'max_time': max(times),
                'min_time': min(times)
            }
        return stats
    
    def print_stats(self):
        """Afficher les statistiques de performance"""
        print("\n📊 Statistiques de performance:")
        print("=" * 50)
        
        stats = self.get_stats()
        for name, data in sorted(stats.items(), key=lambda x: x[1]['total_time'], reverse=True):
            print(f"{name}:")
            print(f"  Appels: {data['calls']}")
            print(f"  Temps total: {data['total_time']:.3f}s")
            print(f"  Temps moyen: {data['avg_time']:.3f}s")
            print(f"  Temps max: {data['max_time']:.3f}s")
            print()


# Instance globale du moniteur de performance
performance_monitor = PerformanceMonitor()
performance_optimizer = PerformanceOptimizer()


def optimize_database_queries():
    """Optimiser les requêtes de base de données"""
    # Créer des index pour améliorer les performances
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_facturas_fecha ON facturas(fecha_factura)",
        "CREATE INDEX IF NOT EXISTS idx_facturas_numero ON facturas(numero_factura)",
        "CREATE INDEX IF NOT EXISTS idx_factura_items_factura_id ON factura_items(factura_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_producto_id ON stock(producto_id)",
        "CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre)",
        "CREATE INDEX IF NOT EXISTS idx_productos_referencia ON productos(referencia)",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_producto_id ON stock_movements(producto_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_movements_fecha ON stock_movements(fecha_movimiento)"
    ]
    
    for index_sql in indexes:
        try:
            db.execute_query(index_sql)
        except Exception as e:
            print(f"⚠️ Error creando índice: {e}")
    
    print("✅ Índices de base de datos optimizados")


def analyze_database_performance():
    """Analyser les performances de la base de données"""
    print("\n🔍 Análisis de rendimiento de base de datos:")
    print("=" * 50)
    
    # Analyser les tables
    tables = ['productos', 'facturas', 'factura_items', 'stock', 'stock_movements']
    
    for table in tables:
        try:
            # Compter les enregistrements
            count_query = f"SELECT COUNT(*) FROM {table}"
            count = db.execute_query(count_query)[0][0]
            
            # Analyser la table
            analyze_query = f"ANALYZE {table}"
            db.execute_query(analyze_query)
            
            print(f"{table}: {count} registros")
            
        except Exception as e:
            print(f"Error analizando {table}: {e}")
    
    print("\n✅ Análisis completado")


if __name__ == "__main__":
    # Optimiser la base de données
    optimize_database_queries()
    analyze_database_performance()
    
    # Afficher les statistiques
    performance_monitor.print_stats()
