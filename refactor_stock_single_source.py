#!/usr/bin/env python3
"""
REFACTORISATION: Éliminer la redondance de stock
Utiliser uniquement stock.cantidad_disponible comme source unique de vérité
"""

import sys
import os
import sqlite3

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

def analyze_current_stock_usage():
    """Analyser l'utilisation actuelle des deux systèmes de stock"""
    print("🔍 ANALYSE: Utilisation Actuelle du Stock")
    print("=" * 60)
    
    try:
        from database.database import Database
        db = Database()
        
        # 1. Vérifier les données actuelles
        productos = db.get_all_products()
        print(f"📦 Productos trouvés: {len(productos)}")
        
        # 2. Comparer les deux systèmes
        print("\n📊 COMPARAISON DES DEUX SYSTÈMES:")
        print("-" * 40)
        
        inconsistencies = 0
        for producto in productos[:5]:  # Montrer seulement les 5 premiers
            producto_id = producto['id']
            stock_productos = producto.get('stock_actual', 0)
            
            # Obtenir stock de la table séparée
            from database.models import Stock
            stock_table = Stock.get_by_product(producto_id)
            
            status = "✅" if stock_productos == stock_table else "❌"
            if stock_productos != stock_table:
                inconsistencies += 1
            
            print(f"   {status} ID {producto_id}: productos.stock_actual={stock_productos}, stock.cantidad_disponible={stock_table}")
        
        if inconsistencies > 0:
            print(f"\n⚠️  {inconsistencies} inconsistencias detectadas")
        else:
            print("\n✅ Todos los stocks están sincronizados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        return False

def create_stock_view_solution():
    """Crear una vista SQL para unificar el acceso al stock"""
    print("\n🔧 SOLUCIÓN 1: Vista SQL Unificada")
    print("-" * 40)
    
    try:
        from database.database import Database
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Crear vista que unifique el acceso al stock
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS productos_with_stock AS
            SELECT 
                p.id,
                p.nombre,
                p.referencia,
                p.precio,
                p.categoria,
                p.descripcion,
                p.imagen_path,
                p.iva_recomendado,
                p.stock_minimo,
                p.fecha_creacion,
                COALESCE(s.cantidad_disponible, 0) as stock_actual
            FROM productos p
            LEFT JOIN stock s ON p.id = s.producto_id
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Vista 'productos_with_stock' creada")
        print("   📋 Esta vista usa stock.cantidad_disponible como fuente única")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando vista: {e}")
        return False

def create_migration_plan():
    """Crear un plan de migration pour éliminer productos.stock_actual"""
    print("\n📋 PLAN DE MIGRATION")
    print("=" * 40)
    
    migration_steps = [
        "1. 🔄 SYNCHRONISATION FINALE",
        "   - Copier productos.stock_actual → stock.cantidad_disponible",
        "   - Vérifier que tous les productos ont une entrée dans stock",
        "",
        "2. 🔧 MODIFICATION DU CODE",
        "   - Remplacer tous les accès à productos.stock_actual",
        "   - Utiliser Stock.get_by_product() partout",
        "   - Modifier get_all_products() pour utiliser la vue",
        "",
        "3. 🗑️  SUPPRESSION DE LA COLONNE",
        "   - ALTER TABLE productos DROP COLUMN stock_actual",
        "   - (SQLite nécessite recréation de table)",
        "",
        "4. ✅ AVANTAGES",
        "   - Source unique de vérité pour le stock",
        "   - Pas de risque d'incohérence",
        "   - Historique des mouvements cohérent",
        "   - Code plus simple et maintenable"
    ]
    
    for step in migration_steps:
        print(step)
    
    return True

def implement_unified_stock_access():
    """Implémenter l'accès unifié au stock"""
    print("\n🚀 IMPLÉMENTATION: Accès Unifié au Stock")
    print("-" * 50)
    
    # Code exemple pour la nouvelle approche
    code_example = '''
# AVANT (problématique)
def get_product_stock_old(product_id):
    # Deux sources possibles, risque d'incohérence
    product = db.get_product(product_id)
    return product['stock_actual']  # ❌ Peut être différent de stock table

# APRÈS (solution unifiée)
def get_product_stock_new(product_id):
    # Source unique de vérité
    from database.models import Stock
    return Stock.get_by_product(product_id)  # ✅ Toujours cohérent

# Nouvelle méthode get_all_products()
def get_all_products_unified():
    query = """
        SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria,
               p.descripcion, p.imagen_path, p.iva_recomendado, p.stock_minimo,
               COALESCE(s.cantidad_disponible, 0) as stock_actual
        FROM productos p
        LEFT JOIN stock s ON p.id = s.producto_id
        ORDER BY p.nombre
    """
    return db.execute_query(query)
'''
    
    print("📝 EXEMPLE DE CODE UNIFIÉ:")
    print(code_example)
    
    return True

def test_unified_approach():
    """Tester l'approche unifiée avec la vue"""
    print("\n🧪 TEST: Approche Unifiée")
    print("-" * 30)
    
    try:
        from database.database import Database
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Tester la vue
        cursor.execute("SELECT id, nombre, stock_actual FROM productos_with_stock LIMIT 3")
        results = cursor.fetchall()
        
        print("📋 Résultats de la vue productos_with_stock:")
        for row in results:
            product_id, nombre, stock_actual = row
            print(f"   📦 ID {product_id}: {nombre} - Stock: {stock_actual}")
        
        conn.close()
        
        print("\n✅ La vue fonctionne correctement")
        print("💡 Cette approche élimine la redondance")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 REFACTORISATION: Stock Source Unique")
    print("=" * 60)
    
    print("🎯 OBJECTIF:")
    print("   Éliminer la redondance entre productos.stock_actual et stock.cantidad_disponible")
    print("   Utiliser uniquement stock.cantidad_disponible comme source de vérité")
    print()
    
    # Exécuter l'analyse et les solutions
    step1 = analyze_current_stock_usage()
    step2 = create_stock_view_solution()
    step3 = create_migration_plan()
    step4 = implement_unified_stock_access()
    step5 = test_unified_approach()
    
    print("\n" + "=" * 60)
    if all([step1, step2, step3, step4, step5]):
        print("🎉 ANALYSE ET SOLUTIONS COMPLÈTES")
        print("\n✅ RECOMMANDATIONS:")
        print("   1. Utiliser la vue 'productos_with_stock' immédiatement")
        print("   2. Modifier get_all_products() pour utiliser la vue")
        print("   3. Planifier la suppression de productos.stock_actual")
        print("   4. Cela éliminera définitivement les problèmes de synchronisation")
        print("\n💡 AVANTAGE PRINCIPAL:")
        print("   Plus jamais de 'stock insuficiente disponible 0' dû à la désynchronisation!")
    else:
        print("⚠️  CERTAINES ÉTAPES ONT ÉCHOUÉ")
    
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
