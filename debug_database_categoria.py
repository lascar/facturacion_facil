#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug spécifique pour la récupération des catégories depuis la base de données
"""

from database.database_improved import DatabaseImproved
import sqlite3

def debug_database_direct():
    """Debug direct de la base de données"""
    print("🔍 DEBUG DIRECT BASE DE DONNÉES")
    print("=" * 35)
    
    try:
        # Connexion directe SQLite
        print("\n1️⃣ Connexion SQLite directe:")
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nombre, categoria FROM productos")
        rows = cursor.fetchall()
        
        print(f"   📊 Produits trouvés: {len(rows)}")
        for row in rows:
            print(f"   📝 ID: {row[0]}, Nom: {row[1]}, Catégorie: '{row[2]}' (type: {type(row[2])})")
        
        conn.close()
        
        # Test avec DatabaseImproved
        print("\n2️⃣ Test DatabaseImproved:")
        db = DatabaseImproved()
        products = db.get_all_products()
        
        print(f"   📊 Produits via DatabaseImproved: {len(products)}")
        for product in products:
            print(f"   📝 ID: {product['id']}, Nom: {product['nombre']}, Catégorie: '{product.get('categoria')}' (type: {type(product.get('categoria'))})")
        
        # Test get_product_categories
        print("\n3️⃣ Test get_product_categories:")
        categories = db.get_product_categories()
        print(f"   📊 Catégories: {len(categories)}")
        for cat in categories:
            print(f"   📝 Catégorie: '{cat}' (type: {type(cat)})")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur debug DB: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_multiple_instances():
    """Debug avec plusieurs instances de DatabaseImproved"""
    print("\n🔍 DEBUG INSTANCES MULTIPLES")
    print("=" * 35)
    
    try:
        # Instance 1
        print("\n1️⃣ Instance 1:")
        db1 = DatabaseImproved()
        products1 = db1.get_all_products()
        
        if products1:
            product1 = products1[0]
            print(f"   📝 Produit: {product1['nombre']}, Catégorie: '{product1.get('categoria')}'")
        
        # Instance 2
        print("\n2️⃣ Instance 2:")
        db2 = DatabaseImproved()
        products2 = db2.get_all_products()
        
        if products2:
            product2 = products2[0]
            print(f"   📝 Produit: {product2['nombre']}, Catégorie: '{product2.get('categoria')}'")
        
        # Comparaison
        if products1 and products2:
            cat1 = products1[0].get('categoria')
            cat2 = products2[0].get('categoria')
            
            if cat1 == cat2:
                print(f"   ✅ Cohérence entre instances: '{cat1}'")
                return True
            else:
                print(f"   ❌ Incohérence: instance1='{cat1}', instance2='{cat2}'")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur debug instances: {e}")
        return False

def debug_schema():
    """Debug du schéma de la table"""
    print("\n🔍 DEBUG SCHÉMA TABLE")
    print("=" * 25)
    
    try:
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        
        # Schéma de la table
        cursor.execute("PRAGMA table_info(productos)")
        columns = cursor.fetchall()
        
        print("   📊 Colonnes de la table productos:")
        for col in columns:
            print(f"      {col[1]} ({col[2]}) - NULL: {col[3] == 0}")
        
        # Vérifier spécifiquement la colonne categoria
        categoria_col = None
        for col in columns:
            if col[1] == 'categoria':
                categoria_col = col
                break
        
        if categoria_col:
            print(f"\n   📝 Colonne categoria:")
            print(f"      Type: {categoria_col[2]}")
            print(f"      Peut être NULL: {categoria_col[3] == 0}")
            print(f"      Valeur par défaut: {categoria_col[4]}")
        else:
            print("   ❌ Colonne categoria non trouvée!")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur debug schéma: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DEBUG COMPLET BASE DE DONNÉES - CATÉGORIES")
    print("=" * 50)
    
    # Test 1: Base de données directe
    test1 = debug_database_direct()
    
    # Test 2: Instances multiples
    test2 = debug_multiple_instances()
    
    # Test 3: Schéma
    test3 = debug_schema()
    
    print(f"\n🎯 RÉSUMÉ DEBUG:")
    print(f"   Test DB directe: {'✅ OK' if test1 else '❌ ÉCHEC'}")
    print(f"   Test instances: {'✅ OK' if test2 else '❌ ÉCHEC'}")
    print(f"   Test schéma: {'✅ OK' if test3 else '❌ ÉCHEC'}")
    
    if test1 and test2 and test3:
        print("\n🎉 TOUS LES TESTS DB RÉUSSIS")
        print("   La base de données fonctionne correctement")
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS")
        print("   Vérifier les détails ci-dessus")
    
    return test1 and test2 and test3

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
