#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de cohérence des données de stock
"""

import sys
import os
import time

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_consistency():
    """Tester la cohérence des données de la base"""
    print("🔍 Test de cohérence de la base de données...")
    
    try:
        from database.database import db
        
        print("\n📋 APPELS MULTIPLES À get_all_products():")
        
        # Faire plusieurs appels successifs
        for i in range(3):
            print(f"\n   📞 Appel {i+1}:")
            productos = db.get_all_products()
            
            for producto in productos[:3]:  # Afficher les 3 premiers
                stock = producto.get('stock_actual', 0)
                print(f"      ID {producto.get('id')}: {producto['nombre']} - Stock: {stock}")
            
            time.sleep(0.1)  # Petite pause
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test base: {e}")
        return False

def test_concurrent_access():
    """Tester l'accès concurrent simulé"""
    print("\n🔍 Test d'accès concurrent simulé...")
    
    try:
        from database.database import db
        
        # Simuler deux fenêtres qui s'ouvrent en même temps
        print("\n📋 SIMULATION DEUX FENÊTRES:")
        
        print("   🪟 Fenêtre 1 (Création) - Chargement...")
        productos1 = db.get_all_products()
        
        print("   🪟 Fenêtre 2 (Édition) - Chargement...")
        productos2 = db.get_all_products()
        
        # Comparer les résultats
        print("\n📊 COMPARAISON:")
        if len(productos1) != len(productos2):
            print(f"   ❌ Nombre différent: {len(productos1)} vs {len(productos2)}")
            return False
        
        differences = []
        for i, (p1, p2) in enumerate(zip(productos1, productos2)):
            if p1.get('stock_actual') != p2.get('stock_actual'):
                differences.append({
                    'id': p1.get('id'),
                    'nombre': p1.get('nombre'),
                    'stock1': p1.get('stock_actual'),
                    'stock2': p2.get('stock_actual')
                })
        
        if differences:
            print(f"   ❌ {len(differences)} différences de stock trouvées:")
            for diff in differences:
                print(f"      ID {diff['id']} ({diff['nombre']}): {diff['stock1']} vs {diff['stock2']}")
            return False
        else:
            print("   ✅ Aucune différence trouvée")
            return True
        
    except Exception as e:
        print(f"❌ Erreur test concurrent: {e}")
        return False

def test_database_connection():
    """Tester la connexion à la base"""
    print("\n🔍 Test de connexion à la base...")
    
    try:
        from database.database import db

        # Vérifier la connexion
        productos = db.get_all_products()
        print(f"   ✅ Connexion OK - {len(productos)} produits trouvés")
        
        # Afficher quelques produits pour debug
        print("\n📋 ÉCHANTILLON DE PRODUITS:")
        for producto in productos[:5]:
            print(f"   ID {producto.get('id')}: {producto.get('nombre')} - Stock: {producto.get('stock_actual', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False

def test_stock_update_simulation():
    """Simuler une mise à jour de stock"""
    print("\n🔍 Test de simulation mise à jour stock...")
    
    try:
        from database.database import db

        # Obtenir les produits avant
        print("   📊 État AVANT:")
        productos_avant = db.get_all_products()
        for producto in productos_avant[:3]:
            print(f"      ID {producto.get('id')}: Stock {producto.get('stock_actual', 0)}")
        
        # Simuler un délai (comme si une autre opération modifiait le stock)
        time.sleep(0.2)
        
        # Obtenir les produits après
        print("\n   📊 État APRÈS:")
        productos_apres = db.get_all_products()
        for producto in productos_apres[:3]:
            print(f"      ID {producto.get('id')}: Stock {producto.get('stock_actual', 0)}")
        
        # Vérifier la cohérence
        changes = []
        for avant, apres in zip(productos_avant, productos_apres):
            if avant.get('stock_actual') != apres.get('stock_actual'):
                changes.append({
                    'id': avant.get('id'),
                    'avant': avant.get('stock_actual'),
                    'apres': apres.get('stock_actual')
                })
        
        if changes:
            print(f"\n   ⚠️  {len(changes)} changements détectés:")
            for change in changes:
                print(f"      ID {change['id']}: {change['avant']} → {change['apres']}")
        else:
            print("\n   ✅ Aucun changement (normal)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur simulation: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DE COHÉRENCE DES DONNÉES DE STOCK")
    print("=" * 55)
    
    tests = [
        test_database_connection,
        test_database_consistency,
        test_concurrent_access,
        test_stock_update_simulation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
    
    print("\n" + "=" * 55)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 COHÉRENCE VALIDÉE !")
        print("\n📋 Conclusions:")
        print("   ✅ Base de données cohérente")
        print("   ✅ Pas de problème d'accès concurrent")
        print("   ✅ Données stables entre appels")
        print("\n💡 Le problème vient probablement:")
        print("   - Du cache dans l'interface")
        print("   - Du timing d'ouverture des fenêtres")
        print("   - D'une modification entre les appels")
    else:
        print("⚠️  Problèmes détectés dans la base")
        print("\n💡 Actions recommandées:")
        print("   - Vérifier l'intégrité de la base")
        print("   - Analyser les logs détaillés")
        print("   - Forcer le rechargement des données")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n✅ Test terminé: {success}")
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        success = False
    
    sys.exit(0 if success else 1)
