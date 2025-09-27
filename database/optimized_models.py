#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèles optimisés pour améliorer les performances
"""

from .database import db
from .models import Factura, FacturaItem, Producto, Stock
from utils.performance_optimizer import performance_monitor, performance_optimizer


class OptimizedFactura(Factura):
    """Version optimisée de Factura qui évite les requêtes N+1"""
    
    @staticmethod
    @performance_monitor.time_function("get_all_facturas_optimized")
    def get_all_optimized():
        """Obtient toutes les facturas avec leurs items en requêtes optimisées"""
        # Requête principale pour les facturas
        facturas_query = """
            SELECT f.id, f.numero_factura, f.fecha_factura, f.nombre_cliente,
                   f.dni_nie_cliente, f.direccion_cliente, f.email_cliente, f.telefono_cliente,
                   f.subtotal, f.total_iva, f.total_factura, f.modo_pago, f.fecha_creacion
            FROM facturas f
            ORDER BY f.fecha_factura DESC, f.numero_factura DESC
        """
        
        facturas_results = db.execute_query(facturas_query)
        
        if not facturas_results:
            return []
        
        # Obtenir tous les IDs de facturas
        factura_ids = [row[0] for row in facturas_results]
        
        # Requête pour tous les items de ces facturas (une seule requête)
        if factura_ids:
            placeholders = ','.join(['?'] * len(factura_ids))
            items_query = f"""
                SELECT fi.id, fi.factura_id, fi.producto_id, fi.cantidad,
                       fi.precio_unitario, fi.iva_aplicado, fi.descuento,
                       fi.subtotal, fi.descuento_amount, fi.iva_amount, fi.total,
                       p.nombre as producto_nombre, p.referencia as producto_referencia
                FROM factura_items fi
                LEFT JOIN productos p ON fi.producto_id = p.id
                WHERE fi.factura_id IN ({placeholders})
                ORDER BY fi.factura_id, fi.id
            """
            
            items_results = db.execute_query(items_query, factura_ids)
        else:
            items_results = []
        
        # Organizar items por factura_id
        items_by_factura = {}
        for item_row in items_results:
            factura_id = item_row[1]
            if factura_id not in items_by_factura:
                items_by_factura[factura_id] = []
            
            item = FacturaItem(
                id=item_row[0], factura_id=item_row[1], producto_id=item_row[2],
                cantidad=item_row[3], precio_unitario=item_row[4], iva_aplicado=item_row[5],
                descuento=item_row[6]
            )
            # Valores calculados
            item.subtotal = item_row[7] or 0.0
            item.descuento_amount = item_row[8] or 0.0
            item.iva_amount = item_row[9] or 0.0
            item.total = item_row[10] or 0.0
            
            # Información del producto (evita otra consulta)
            if item_row[11]:  # Si hay nombre de producto
                item.producto = Producto(
                    id=item_row[2], nombre=item_row[11], referencia=item_row[12] or ""
                )
            
            items_by_factura[factura_id].append(item)
        
        # Crear facturas con sus items
        facturas = []
        for row in facturas_results:
            factura = Factura(
                id=row[0], numero_factura=row[1], fecha_factura=row[2], nombre_cliente=row[3],
                dni_nie_cliente=row[4] or "", direccion_cliente=row[5] or "", 
                email_cliente=row[6] or "", telefono_cliente=row[7] or "",
                subtotal=row[8] or 0.0, total_iva=row[9] or 0.0, total_factura=row[10] or 0.0,
                modo_pago=row[11] or "efectivo", fecha_creacion=row[12] or ""
            )
            # Asignar items (sin consulta adicional)
            factura.items = items_by_factura.get(factura.id, [])
            facturas.append(factura)
        
        return facturas
    
    @staticmethod
    @performance_optimizer.cache_result("facturas_summary", ttl=60)
    def get_summary_optimized():
        """Obtient un résumé des facturas pour l'affichage rapide"""
        query = """
            SELECT id, numero_factura, fecha_factura, nombre_cliente, total_factura
            FROM facturas
            ORDER BY fecha_factura DESC, numero_factura DESC
        """
        
        results = db.execute_query(query)
        facturas_summary = []
        
        for row in results:
            facturas_summary.append({
                'id': row[0],
                'numero_factura': row[1],
                'fecha_factura': row[2],
                'nombre_cliente': row[3],
                'total_factura': row[4]
            })
        
        return facturas_summary


class OptimizedStock:
    """Version optimisée de Stock qui évite les requêtes N+1"""
    
    @staticmethod
    @performance_monitor.time_function("get_all_stock_optimized")
    def get_all_optimized():
        """Obtient tout le stock avec informations complètes en une seule requête"""
        query = """
            SELECT s.producto_id, s.cantidad_disponible, s.fecha_actualizacion,
                   p.nombre, p.referencia, p.precio, p.categoria, p.descripcion
            FROM stock s 
            JOIN productos p ON s.producto_id = p.id 
            ORDER BY p.nombre
        """
        
        results = db.execute_query(query)
        stock_data = []
        
        for row in results:
            stock_data.append({
                'producto_id': row[0],
                'cantidad': row[1] or 0,
                'fecha_actualizacion': row[2] or "N/A",
                'nombre': row[3] or "",
                'referencia': row[4] or "",
                'precio': row[5] or 0.0,
                'categoria': row[6] or "",
                'descripcion': row[7] or ""
            })
        
        return stock_data
    
    @staticmethod
    @performance_optimizer.cache_result("low_stock", ttl=300)
    def get_low_stock_optimized(threshold=5):
        """Obtient les produits avec stock bas (avec cache)"""
        query = """
            SELECT s.producto_id, s.cantidad_disponible, s.fecha_actualizacion,
                   p.nombre, p.referencia, p.precio
            FROM stock s
            JOIN productos p ON s.producto_id = p.id
            WHERE s.cantidad_disponible <= ?
            ORDER BY s.cantidad_disponible ASC, p.nombre
        """
        
        results = db.execute_query(query, (threshold,))
        low_stock_data = []
        
        for row in results:
            low_stock_data.append({
                'producto_id': row[0],
                'cantidad': row[1],
                'fecha_actualizacion': row[2] or "N/A",
                'nombre': row[3],
                'referencia': row[4],
                'precio': row[5]
            })
        
        return low_stock_data


class OptimizedProducto:
    """Version optimisée de Producto avec stock intégré"""
    
    @staticmethod
    @performance_monitor.time_function("get_all_productos_with_stock")
    def get_all_with_stock_optimized():
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
            producto = Producto(
                id=row[0], nombre=row[1] or "", referencia=row[2] or "", 
                precio=row[3] or 0.0, categoria=row[4] or "", 
                descripcion=row[5] or "", imagen_path=row[6] or "",
                iva_recomendado=row[7] or 21.0
            )
            # Ajouter le stock sans requête supplémentaire
            producto._stock_actual = row[8] or 0
            productos.append(producto)
        
        return productos
    
    @staticmethod
    @performance_optimizer.cache_result("productos_summary", ttl=300)
    def get_summary_optimized():
        """Obtient un résumé des productos pour l'affichage rapide"""
        query = """
            SELECT p.id, p.nombre, p.referencia, p.precio, 
                   COALESCE(s.cantidad_disponible, 0) as stock
            FROM productos p
            LEFT JOIN stock s ON p.id = s.producto_id
            ORDER BY p.nombre
        """
        
        results = db.execute_query(query)
        productos_summary = []
        
        for row in results:
            productos_summary.append({
                'id': row[0],
                'nombre': row[1],
                'referencia': row[2],
                'precio': row[3],
                'stock': row[4]
            })
        
        return productos_summary


class BatchOperations:
    """Opérations par lot pour améliorer les performances"""
    
    @staticmethod
    def update_multiple_stock(updates: list):
        """Met à jour plusieurs stocks en une seule transaction"""
        if not updates:
            return
        
        # Préparer la requête batch
        query = """
            UPDATE stock 
            SET cantidad_disponible = ?, fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE producto_id = ?
        """
        
        # Préparer les paramètres
        params_list = [(update['cantidad'], update['producto_id']) for update in updates]
        
        # Exécuter en transaction
        try:
            db.connection.execute("BEGIN TRANSACTION")
            
            for params in params_list:
                db.execute_query(query, params)
            
            db.connection.execute("COMMIT")
            
            # Vider le cache lié au stock
            performance_optimizer.clear_cache("stock")
            performance_optimizer.clear_cache("low_stock")
            
        except Exception as e:
            db.connection.execute("ROLLBACK")
            raise e
    
    @staticmethod
    def create_multiple_stock_movements(movements: list):
        """Crée plusieurs mouvements de stock en une seule transaction"""
        if not movements:
            return
        
        query = """
            INSERT INTO stock_movements (producto_id, cantidad, tipo, descripcion)
            VALUES (?, ?, ?, ?)
        """
        
        params_list = [
            (mov['producto_id'], mov['cantidad'], mov['tipo'], mov['descripcion'])
            for mov in movements
        ]
        
        try:
            db.connection.execute("BEGIN TRANSACTION")
            
            for params in params_list:
                db.execute_query(query, params)
            
            db.connection.execute("COMMIT")
            
        except Exception as e:
            db.connection.execute("ROLLBACK")
            raise e


class QueryOptimizer:
    """Optimiseur de requêtes pour analyser et améliorer les performances"""
    
    @staticmethod
    def analyze_query_performance(query: str, params=None):
        """Analyse les performances d'une requête"""
        import time
        
        # Mesurer le temps d'exécution
        start_time = time.time()
        
        # Exécuter EXPLAIN QUERY PLAN
        explain_query = f"EXPLAIN QUERY PLAN {query}"
        explain_results = db.execute_query(explain_query, params)
        
        # Exécuter la requête réelle
        results = db.execute_query(query, params)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            'execution_time': execution_time,
            'row_count': len(results) if results else 0,
            'query_plan': explain_results,
            'is_slow': execution_time > 0.1
        }
    
    @staticmethod
    def suggest_indexes():
        """Suggère des index pour améliorer les performances"""
        suggestions = []
        
        # Analyser les requêtes courantes
        common_queries = [
            ("SELECT * FROM facturas ORDER BY fecha_factura DESC", "idx_facturas_fecha"),
            ("SELECT * FROM productos WHERE nombre LIKE ?", "idx_productos_nombre"),
            ("SELECT * FROM stock WHERE producto_id = ?", "idx_stock_producto_id"),
            ("SELECT * FROM factura_items WHERE factura_id = ?", "idx_factura_items_factura_id")
        ]
        
        for query, suggested_index in common_queries:
            try:
                analysis = QueryOptimizer.analyze_query_performance(query)
                if analysis['is_slow']:
                    suggestions.append({
                        'query': query,
                        'suggested_index': suggested_index,
                        'execution_time': analysis['execution_time']
                    })
            except:
                pass
        
        return suggestions


def clear_all_caches():
    """Vider tous les caches de performance"""
    performance_optimizer.clear_cache()
    print("✅ Tous les caches vidés")


def warm_up_caches():
    """Préchauffer les caches avec les données couramment utilisées"""
    print("🔥 Préchauffage des caches...")
    
    # Charger les données couramment utilisées
    try:
        OptimizedFactura.get_summary_optimized()
        OptimizedProducto.get_summary_optimized()
        OptimizedStock.get_low_stock_optimized()
        print("✅ Caches préchauffés")
    except Exception as e:
        print(f"⚠️ Erreur lors du préchauffage: {e}")


if __name__ == "__main__":
    # Tester les performances
    print("🚀 Test des modèles optimisés")
    
    # Tester les facturas optimisées
    start = time.time()
    facturas = OptimizedFactura.get_all_optimized()
    end = time.time()
    print(f"Facturas optimisées: {len(facturas)} en {end-start:.3f}s")
    
    # Tester le stock optimisé
    start = time.time()
    stock = OptimizedStock.get_all_optimized()
    end = time.time()
    print(f"Stock optimisé: {len(stock)} en {end-start:.3f}s")
    
    # Afficher les statistiques
    performance_monitor.print_stats()
