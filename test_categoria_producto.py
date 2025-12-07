#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que la catégorie des produits est bien sauvegardée
"""

import sqlite3
from database.database_improved import DatabaseImproved
from database.database import Database

def test_categoria_con_database_original():
    """Test avec la classe Database originale"""
    print("🧪 Test avec Database originale...")
    
    try:
        db = Database()
        
        # Créer un produit de test avec catégorie
        product_data = {
            'nombre': 'Producto Test Categoria Original',
            'referencia': 'TEST-CAT-ORIG-001',
            'precio_venta': 25.50,
            'categoria': 'Categoria Test Original',
            'descripcion': 'Producto para test de categoria',
            'iva_recomendado': 21.0,
            'stock': 10
        }
        
        # Ajouter le produit
        product_id = db.add_product(product_data)
        print(f"   ✅ Produit créé avec ID: {product_id}")
        
        # Vérifier que la catégorie est sauvegardée
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT categoria FROM productos WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            print(f"   ✅ Catégorie sauvegardée: '{result[0]}'")
            return True
        else:
            print(f"   ❌ Catégorie non sauvegardée: {result}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_categoria_con_database_improved():
    """Test avec la classe DatabaseImproved"""
    print("🧪 Test avec DatabaseImproved...")
    
    try:
        db = DatabaseImproved()
        
        # Créer un produit de test avec catégorie
        product_data = {
            'nombre': 'Producto Test Categoria Improved',
            'referencia': 'TEST-CAT-IMP-001',
            'precio_venta': 35.75,
            'categoria': 'Categoria Test Improved',
            'descripcion': 'Producto para test de categoria mejorado',
            'iva_recomendado': 21.0,
            'stock': 15
        }
        
        # Ajouter le produit
        product_id = db.add_product(product_data)
        print(f"   ✅ Produit créé avec ID: {product_id}")
        
        # Vérifier que la catégorie est sauvegardée
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT categoria FROM productos WHERE id = ?", (product_id,))
            result = cursor.fetchone()
        
        if result and result[0]:
            print(f"   ✅ Catégorie sauvegardée: '{result[0]}'")
            return True
        else:
            print(f"   ❌ Catégorie non sauvegardée: {result}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_update_categoria():
    """Test de mise à jour de catégorie"""
    print("🧪 Test de mise à jour de catégorie...")
    
    try:
        db = DatabaseImproved()
        
        # Créer un produit de test
        product_data = {
            'nombre': 'Producto Test Update',
            'referencia': 'TEST-UPD-001',
            'precio_venta': 45.00,
            'categoria': 'Categoria Original',
            'descripcion': 'Producto para test de update',
            'iva_recomendado': 21.0,
            'stock': 20
        }
        
        # Ajouter le produit
        product_id = db.add_product(product_data)
        print(f"   ✅ Produit créé avec ID: {product_id}")
        
        # Mettre à jour avec nouvelle catégorie
        product_data['id'] = product_id
        product_data['categoria'] = 'Categoria Actualizada'
        product_data['nombre'] = 'Producto Test Update Modificado'
        
        success = db.update_product(product_data)
        print(f"   ✅ Mise à jour: {'réussie' if success else 'échouée'}")
        
        # Vérifier la nouvelle catégorie
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT categoria, nombre FROM productos WHERE id = ?", (product_id,))
            result = cursor.fetchone()
        
        if result and result[0] == 'Categoria Actualizada':
            print(f"   ✅ Catégorie mise à jour: '{result[0]}'")
            print(f"   ✅ Nom mis à jour: '{result[1]}'")
            return True
        else:
            print(f"   ❌ Catégorie non mise à jour: {result}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_get_categories():
    """Test de récupération des catégories"""
    print("🧪 Test de récupération des catégories...")
    
    try:
        db = DatabaseImproved()
        
        # Récupérer les catégories
        categories = db.get_product_categories()
        print(f"   ✅ Catégories trouvées: {len(categories)}")
        
        for i, cat in enumerate(categories, 1):
            print(f"      {i}. '{cat}'")
        
        return len(categories) > 0
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_categoria_vacia():
    """Test avec catégorie vide"""
    print("🧪 Test avec catégorie vide...")
    
    try:
        db = DatabaseImproved()
        
        # Créer un produit sans catégorie
        product_data = {
            'nombre': 'Producto Sin Categoria',
            'referencia': 'TEST-NO-CAT-001',
            'precio_venta': 15.00,
            'categoria': None,  # Catégorie vide
            'descripcion': 'Producto sin categoria',
            'iva_recomendado': 21.0,
            'stock': 5
        }
        
        # Ajouter le produit
        product_id = db.add_product(product_data)
        print(f"   ✅ Produit créé avec ID: {product_id}")
        
        # Vérifier que la catégorie est NULL
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT categoria FROM productos WHERE id = ?", (product_id,))
            result = cursor.fetchone()
        
        if result and result[0] is None:
            print(f"   ✅ Catégorie vide correctement sauvegardée (NULL)")
            return True
        else:
            print(f"   ❌ Catégorie vide mal gérée: {result}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def cleanup_test_products():
    """Nettoie les produits de test"""
    print("🧹 Nettoyage des produits de test...")
    
    try:
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        
        # Supprimer les produits de test
        cursor.execute("DELETE FROM productos WHERE referencia LIKE 'TEST-%'")
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"   ✅ {deleted_count} produits de test supprimés")
        
    except Exception as e:
        print(f"   ⚠️ Erreur lors du nettoyage: {e}")

def main():
    """Fonction principale de test"""
    print("🔍 TEST DE SAUVEGARDE DES CATÉGORIES DE PRODUITS")
    print("=" * 50)
    
    tests = [
        ("Database originale", test_categoria_con_database_original),
        ("DatabaseImproved", test_categoria_con_database_improved),
        ("Mise à jour catégorie", test_update_categoria),
        ("Récupération catégories", test_get_categories),
        ("Catégorie vide", test_categoria_vacia)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
    
    # Nettoyage
    cleanup_test_products()
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DES TESTS")
    print("=" * 20)
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS ONT RÉUSSI !")
        print("   Les catégories de produits sont correctement sauvegardées.")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) ont échoué.")
        print("   Il y a encore des problèmes avec la sauvegarde des catégories.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
