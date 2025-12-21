#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de comportement complet pour la synchronisation des stocks après migration
"""

import sys
import os
import sqlite3
import pytest

# Ajouter le répertoire racine au path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(current_dir, '..', '..')
sys.path.insert(0, root_dir)

from database.test_database import get_test_database
from database.migration_manager import MigrationManager
from database.database_improved import DatabaseImproved
from database.models import Stock
from utils.event_manager_pyqt5 import event_manager

def test_complete_stock_synchronization():
    """Test complet de synchronisation des stocks"""
    print("🧪 TEST COMPORTEMENT SYNCHRONISATION STOCKS COMPLÈTE")
    print("=" * 60)
    
    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path
    
    try:
        # 1. Exécuter la migration
        print("1. 🔄 Exécution de la migration...")
        migration_manager = MigrationManager(db_path)
        migration_manager.remove_stock_columns_from_productos()
        print("   ✅ Migration terminée")
        
        # 2. Créer des produits de test
        print("\n2. 📦 Création de produits de test...")
        db_improved = DatabaseImproved(db_path)
        
        products_data = [
            {
                'nombre': 'Producto Sync Test 1',
                'referencia': 'SYNC001',
                'precio': 25.50,
                'categoria': 'Test',
                'stock_actual': 100
            },
            {
                'nombre': 'Producto Sync Test 2',
                'referencia': 'SYNC002',
                'precio': 15.75,
                'categoria': 'Test',
                'stock_actual': 50
            }
        ]
        
        product_ids = []
        for product_data in products_data:
            product_id = db_improved.add_product(product_data)
            product_ids.append(product_id)
            print(f"   ✅ Produit créé: {product_data['nombre']} (ID: {product_id})")
        
        # 3. Test get_all_products (simulation fenêtre Productos)
        print("\n3. 📋 Test récupération produits (fenêtre Productos)...")
        products = db_improved.get_all_products()
        print(f"   Nombre de produits récupérés: {len(products)}")
        
        for product in products:
            if product['id'] in product_ids:
                print(f"   - {product['nombre']}: Stock {product['stock_actual']}")
                assert 'stock_actual' in product, "stock_actual devrait être présent"
                assert product['stock_actual'] > 0, "stock_actual devrait être > 0"
        
        print("   ✅ get_all_products() fonctionne correctement")
        
        # 4. Test ajustement stock (simulation fenêtre Stock)
        print("\n4. 📊 Test ajustement stock (fenêtre Stock)...")
        product_id = product_ids[0]
        old_stock = Stock.get_by_product(product_id, db_path)
        new_stock = 75
        
        print(f"   Stock avant ajustement: {old_stock}")
        Stock.update_stock_direct(product_id, new_stock, db_path)
        updated_stock = Stock.get_by_product(product_id, db_path)
        print(f"   Stock après ajustement: {updated_stock}")
        
        assert updated_stock == new_stock, f"Stock devrait être {new_stock}, obtenu: {updated_stock}"
        print("   ✅ Ajustement stock fonctionne")
        
        # 5. Test synchronisation via get_all_products
        print("\n5. 🔄 Test synchronisation (fenêtre Productos après ajustement)...")
        products_after = db_improved.get_all_products()
        
        updated_product = next((p for p in products_after if p['id'] == product_id), None)
        assert updated_product is not None, "Produit devrait être trouvé"
        assert updated_product['stock_actual'] == new_stock, f"Stock synchronisé devrait être {new_stock}, obtenu: {updated_product['stock_actual']}"
        
        print(f"   Stock synchronisé: {updated_product['stock_actual']}")
        print("   ✅ Synchronisation automatique fonctionne")
        
        # 6. Test bouton Actualizar (simulation)
        print("\n6. 🔄 Test bouton Actualizar...")
        
        # Simuler un autre changement de stock
        Stock.update_stock_direct(product_id, 90, db_path)
        
        # Simuler le clic sur Actualizar (recharger les données)
        refreshed_products = db_improved.get_all_products()
        refreshed_product = next((p for p in refreshed_products if p['id'] == product_id), None)
        
        assert refreshed_product['stock_actual'] == 90, f"Stock après Actualizar devrait être 90, obtenu: {refreshed_product['stock_actual']}"
        print(f"   Stock après Actualizar: {refreshed_product['stock_actual']}")
        print("   ✅ Bouton Actualizar fonctionne")
        
        # 7. Test événements (simulation)
        print("\n7. 📡 Test système d'événements...")
        
        # Simuler l'émission d'un signal stock_adjusted
        event_received = []
        
        def on_stock_adjusted(product_id, old_stock, new_stock):
            event_received.append((product_id, old_stock, new_stock))
        
        # Connecter temporairement le signal
        event_manager.stock_adjusted.connect(on_stock_adjusted)
        
        # Émettre le signal
        event_manager.emit_stock_adjusted(product_id, 90, 95)
        
        # Vérifier que le signal a été reçu
        assert len(event_received) == 1, "Signal devrait être reçu"
        assert event_received[0] == (product_id, 90, 95), "Signal devrait contenir les bonnes données"
        
        print(f"   Signal reçu: {event_received[0]}")
        print("   ✅ Système d'événements fonctionne")
        
        # Déconnecter le signal
        event_manager.stock_adjusted.disconnect(on_stock_adjusted)
        
        print("\n" + "=" * 60)
        print("🎉 TOUS LES TESTS DE COMPORTEMENT PASSENT !")
        print("✅ Migration: OK")
        print("✅ Récupération produits: OK")
        print("✅ Ajustement stock: OK")
        print("✅ Synchronisation automatique: OK")
        print("✅ Bouton Actualizar: OK")
        print("✅ Système d'événements: OK")
        print("\n🚀 LA SYNCHRONISATION STOCKS EST FONCTIONNELLE !")

        # Test passes - no return value needed

    except Exception as e:
        print(f"\n❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"Test échoué: {e}")

    finally:
        test_db.cleanup()

def main():
    """Fonction principale"""
    success = test_complete_stock_synchronization()
    
    if success:
        print("\n🎯 CONCLUSION:")
        print("Les corrections apportées ont résolu les problèmes de synchronisation.")
        print("Les fenêtres Stock et Productos devraient maintenant se synchroniser correctement.")
        print("\n📝 ACTIONS RECOMMANDÉES:")
        print("1. Tester manuellement l'interface graphique")
        print("2. Vérifier que les changements dans Stock se reflètent dans Productos")
        print("3. Confirmer que le bouton Actualizar fonctionne dans les deux fenêtres")
    else:
        print("\n❌ Des problèmes subsistent. Vérifiez les logs ci-dessus.")

if __name__ == '__main__':
    main()
