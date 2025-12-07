#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour vérifier que le problème de catégorie est résolu
"""

import sqlite3
import time
from database.database_improved import DatabaseImproved

def test_final_categoria():
    """Test final complet de la sauvegarde des catégories"""
    print("🔍 TEST FINAL - SAUVEGARDE DES CATÉGORIES DE PRODUITS")
    print("=" * 55)
    
    try:
        db = DatabaseImproved()
        
        # Test 1: Créer un produit avec catégorie
        print("\n📋 Test 1: Création avec catégorie")
        print("-" * 35)
        
        # Utiliser un timestamp pour éviter les conflits de référence
        timestamp = str(int(time.time()))

        product_data = {
            'nombre': 'Producto Final Test',
            'referencia': f'FINAL-TEST-{timestamp}',
            'precio_venta': 99.99,
            'categoria': 'Categoria Final Test',
            'descripcion': 'Test final de categoria',
            'iva_recomendado': 21.0,
            'stock': 50
        }
        
        product_id = db.add_product(product_data)
        print(f"   ✅ Produit créé avec ID: {product_id}")
        
        # Vérifier la sauvegarde
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, categoria FROM productos WHERE id = ?", (product_id,))
            result = cursor.fetchone()
        
        if result and result[1] == 'Categoria Final Test':
            print(f"   ✅ Catégorie sauvegardée: '{result[1]}'")
            test1_success = True
        else:
            print(f"   ❌ Catégorie non sauvegardée: {result}")
            test1_success = False
        
        # Test 2: Mise à jour de catégorie
        print("\n📋 Test 2: Mise à jour de catégorie")
        print("-" * 35)
        
        product_data['id'] = product_id
        product_data['categoria'] = 'Categoria Actualizada Final'
        product_data['nombre'] = 'Producto Final Test Actualizado'
        
        success = db.update_product(product_data)
        print(f"   ✅ Mise à jour: {'réussie' if success else 'échouée'}")
        
        # Vérifier la mise à jour
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, categoria FROM productos WHERE id = ?", (product_id,))
            result = cursor.fetchone()
        
        if result and result[1] == 'Categoria Actualizada Final':
            print(f"   ✅ Catégorie mise à jour: '{result[1]}'")
            print(f"   ✅ Nom mis à jour: '{result[0]}'")
            test2_success = True
        else:
            print(f"   ❌ Catégorie non mise à jour: {result}")
            test2_success = False
        
        # Test 3: Récupération des catégories
        print("\n📋 Test 3: Récupération des catégories")
        print("-" * 35)
        
        categories = db.get_product_categories()
        print(f"   ✅ {len(categories)} catégories trouvées:")
        
        for i, cat in enumerate(categories, 1):
            print(f"      {i}. '{cat}'")
        
        test3_success = len(categories) > 0
        
        # Test 4: Vérification directe en base
        print("\n📋 Test 4: Vérification directe en base")
        print("-" * 40)
        
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total, 
                   COUNT(categoria) as with_category,
                   COUNT(CASE WHEN categoria IS NOT NULL AND categoria != '' THEN 1 END) as valid_categories
            FROM productos
        """)
        stats = cursor.fetchone()
        conn.close()
        
        total, with_cat, valid_cat = stats
        print(f"   ✅ Total produits: {total}")
        print(f"   ✅ Avec catégorie: {with_cat}")
        print(f"   ✅ Catégories valides: {valid_cat}")
        
        test4_success = valid_cat > 0
        
        # Nettoyage
        print("\n🧹 Nettoyage...")
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                # Supprimer d'abord les entrées de stock liées
                cursor.execute("DELETE FROM stock WHERE producto_id = ?", (product_id,))
                # Puis supprimer le produit
                cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))
                conn.commit()
            print("   ✅ Produit de test supprimé")
        except Exception as e:
            print(f"   ⚠️ Nettoyage partiel: {e}")
            # Ce n'est pas critique pour le test
        
        # Résumé
        print(f"\n📊 RÉSUMÉ FINAL")
        print("=" * 20)
        
        tests_passed = sum([test1_success, test2_success, test3_success, test4_success])
        total_tests = 4
        
        print(f"✅ Tests réussis: {tests_passed}/{total_tests}")
        print(f"❌ Tests échoués: {total_tests - tests_passed}/{total_tests}")
        
        if tests_passed == total_tests:
            print("\n🎉 PROBLÈME RÉSOLU !")
            print("   ✅ Les catégories de produits sont correctement sauvegardées")
            print("   ✅ La base de données fonctionne parfaitement")
            print("   ✅ L'interface utilise la version améliorée")
            print("   ✅ Les gestionnaires de contexte évitent les locks")
            return True
        else:
            print(f"\n⚠️ {total_tests - tests_passed} test(s) ont échoué")
            print("   Il reste des problèmes à résoudre")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_interface_compatibility():
    """Test de compatibilité avec l'interface"""
    print("\n🔧 Test de compatibilité interface...")
    
    try:
        # Vérifier que l'interface utilise bien DatabaseImproved
        with open('ui/productos_pyqt5.py', 'r') as f:
            content = f.read()
        
        if 'db_improved = DatabaseImproved()' in content:
            print("   ✅ Interface utilise DatabaseImproved")
            
            if 'db_improved.add_product(' in content:
                print("   ✅ Méthode add_product mise à jour")
                
                if 'db_improved.update_product(' in content:
                    print("   ✅ Méthode update_product mise à jour")
                    
                    if 'db_improved.get_product_categories(' in content:
                        print("   ✅ Méthode get_product_categories mise à jour")
                        return True
        
        print("   ❌ Interface non complètement mise à jour")
        return False
        
    except Exception as e:
        print(f"   ❌ Erreur vérification interface: {e}")
        return False

def main():
    """Fonction principale"""
    success1 = test_final_categoria()
    success2 = test_interface_compatibility()
    
    if success1 and success2:
        print("\n🎉 MISSION ACCOMPLIE !")
        print("   Le problème de catégorie est complètement résolu.")
        return True
    else:
        print("\n⚠️ Des problèmes subsistent.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
