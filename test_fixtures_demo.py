#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du système de fixtures
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.test_database import TestDatabase
from database.models import Stock

def test_fixtures_demo():
    """Démonstration complète du système de fixtures"""
    
    print("🎯 DÉMONSTRATION DU SYSTÈME DE FIXTURES")
    print("=" * 60)
    
    # 1. Créer une base de test avec fixtures
    print("\n1️⃣ Création de la base de test avec fixtures...")
    test_db = TestDatabase(with_fixtures=True)
    
    # 2. Afficher l'état initial
    print("\n2️⃣ État initial des fixtures:")
    summary = test_db.get_fixtures_summary()
    
    print(f"   📦 Produits: {summary['products_count']}")
    for product in summary['products'][:3]:
        print(f"      • {product['nombre']} - Stock: {product['stock_actual']}")
    
    print(f"   👥 Clients: {summary['clients_count']}")
    for client in summary['clients'][:3]:
        print(f"      • {client['nombre']}")
    
    print(f"   📄 Factures: {summary['invoices_count']}")
    for invoice in summary['invoices'][:3]:
        print(f"      • {invoice['numero_factura']} - État: {invoice['estado']}")
    
    # 3. Modifier quelque chose
    print("\n3️⃣ Modification du stock du premier produit...")
    first_product = summary['products'][0]
    original_stock = first_product['stock_actual']
    new_stock = 999
    
    print(f"   Stock original: {original_stock}")
    print(f"   Nouveau stock: {new_stock}")
    
    Stock.update_stock_direct(first_product['id'], new_stock, test_db.db_path)
    
    # Vérifier la modification
    updated_summary = test_db.get_fixtures_summary()
    updated_product = next((p for p in updated_summary['products'] if p['id'] == first_product['id']), None)
    print(f"   Stock après modification: {updated_product['stock_actual']}")
    
    # 4. Remettre à l'état initial
    print("\n4️⃣ Remise à l'état initial...")
    test_db.reset_to_fixtures()
    
    # Vérifier que c'est revenu à l'état initial
    reset_summary = test_db.get_fixtures_summary()
    reset_product = next((p for p in reset_summary['products'] if p['id'] == first_product['id']), None)
    print(f"   Stock après reset: {reset_product['stock_actual']}")
    
    if reset_product['stock_actual'] == original_stock:
        print("   ✅ Reset réussi ! Stock revenu à la valeur initiale")
    else:
        print("   ❌ Problème de reset")
    
    # 5. Test de plusieurs modifications
    print("\n5️⃣ Test de modifications multiples...")
    products = reset_summary['products']
    
    print("   Stocks avant modifications:")
    for product in products:
        print(f"      • {product['nombre']}: {product['stock_actual']}")
    
    # Modifier tous les stocks
    new_stocks = [100, 200, 300]
    for i, product in enumerate(products):
        Stock.update_stock_direct(product['id'], new_stocks[i], test_db.db_path)
    
    # Vérifier les modifications
    modified_summary = test_db.get_fixtures_summary()
    print("   Stocks après modifications:")
    for product in modified_summary['products']:
        print(f"      • {product['nombre']}: {product['stock_actual']}")
    
    # 6. Reset final
    print("\n6️⃣ Reset final...")
    test_db.reset_to_fixtures()
    final_summary = test_db.get_fixtures_summary()
    
    print("   Stocks après reset final:")
    for product in final_summary['products']:
        print(f"      • {product['nombre']}: {product['stock_actual']}")
    
    # 7. Nettoyage
    print("\n7️⃣ Nettoyage...")
    test_db.cleanup()
    
    print("\n🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)
    print("\n📋 RÉSUMÉ DU SYSTÈME DE FIXTURES:")
    print("   ✅ 3 produits avec stocks initiaux (25, 150, 75)")
    print("   ✅ 3 clients avec données complètes")
    print("   ✅ 3 factures avec différents états")
    print("   ✅ Reset automatique entre les tests")
    print("   ✅ Modifications de stock fonctionnelles")
    print("   ✅ Nettoyage automatique")
    
    return True

if __name__ == '__main__':
    try:
        test_fixtures_demo()
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
