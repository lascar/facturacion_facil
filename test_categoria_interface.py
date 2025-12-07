#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier l'affichage des catégories dans l'interface
"""

from database.database_improved import DatabaseImproved

def test_categoria_display():
    """Test l'affichage des catégories"""
    print("🧪 TEST AFFICHAGE CATÉGORIES DANS L'INTERFACE")
    print("=" * 50)
    
    db = DatabaseImproved()
    
    # 1. Vérifier les produits avec catégories
    print("\n1️⃣ Produits avec catégories:")
    try:
        products = db.get_all_products()
        print(f"   📊 Total produits: {len(products)}")
        
        products_with_category = [p for p in products if p.get('categoria')]
        print(f"   📊 Produits avec catégorie: {len(products_with_category)}")
        
        for product in products_with_category:
            print(f"   📝 {product['id']}: {product['nombre']} → Catégorie: '{product['categoria']}'")
            
    except Exception as e:
        print(f"   ❌ Erreur récupération produits: {e}")
        return False
    
    # 2. Vérifier les catégories disponibles
    print("\n2️⃣ Catégories disponibles:")
    try:
        categories = db.get_product_categories()
        print(f"   📊 Total catégories: {len(categories)}")
        
        for category in categories:
            print(f"   📝 Catégorie: '{category}'")
            
    except Exception as e:
        print(f"   ❌ Erreur récupération catégories: {e}")
        return False
    
    # 3. Test de cohérence
    print("\n3️⃣ Test de cohérence:")
    if products_with_category and categories:
        product_categories = set(p['categoria'] for p in products_with_category if p.get('categoria'))
        db_categories = set(categories)
        
        print(f"   📊 Catégories dans produits: {product_categories}")
        print(f"   📊 Catégories dans DB: {db_categories}")
        
        if product_categories == db_categories:
            print("   ✅ Cohérence parfaite")
            return True
        else:
            missing_in_db = product_categories - db_categories
            extra_in_db = db_categories - product_categories
            
            if missing_in_db:
                print(f"   ⚠️ Catégories manquantes dans DB: {missing_in_db}")
            if extra_in_db:
                print(f"   ⚠️ Catégories supplémentaires dans DB: {extra_in_db}")
            
            return len(missing_in_db) == 0  # OK si pas de catégories manquantes
    
    elif not products_with_category:
        print("   ⚠️ Aucun produit avec catégorie")
        return False
    elif not categories:
        print("   ⚠️ Aucune catégorie trouvée")
        return False
    
    return True

def test_interface_data_format():
    """Test le format des données pour l'interface"""
    print("\n🔍 TEST FORMAT DONNÉES INTERFACE")
    print("=" * 40)
    
    db = DatabaseImproved()
    
    try:
        products = db.get_all_products()
        
        if not products:
            print("   ⚠️ Aucun produit à tester")
            return True
        
        # Tester le premier produit
        product = products[0]
        print(f"   📝 Test produit: {product.get('nombre')}")
        
        # Vérifier les champs requis
        required_fields = ['id', 'nombre', 'categoria', 'precio_venta']
        missing_fields = []
        
        for field in required_fields:
            if field not in product:
                missing_fields.append(field)
            else:
                value = product[field]
                print(f"      {field}: {repr(value)} ({type(value).__name__})")
        
        if missing_fields:
            print(f"   ❌ Champs manquants: {missing_fields}")
            return False
        
        # Vérifier spécifiquement la catégorie
        categoria = product.get('categoria')
        if categoria is None:
            print("   ⚠️ Catégorie est None")
        elif categoria == '':
            print("   ⚠️ Catégorie est vide")
        else:
            print(f"   ✅ Catégorie valide: '{categoria}'")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur test format: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST COMPLET CATÉGORIES INTERFACE")
    print("=" * 50)
    
    # Test 1: Affichage des catégories
    test1_ok = test_categoria_display()
    
    # Test 2: Format des données
    test2_ok = test_interface_data_format()
    
    # Résumé
    print("\n🎯 RÉSUMÉ DES TESTS:")
    print(f"   Test affichage catégories: {'✅ OK' if test1_ok else '❌ ÉCHEC'}")
    print(f"   Test format données: {'✅ OK' if test2_ok else '❌ ÉCHEC'}")
    
    if test1_ok and test2_ok:
        print("\n🎉 TOUS LES TESTS RÉUSSIS")
        print("   Les catégories devraient s'afficher correctement dans l'interface")
        return True
    else:
        print("\n⚠️ PROBLÈMES DÉTECTÉS")
        print("   Il faut investiguer les erreurs ci-dessus")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
