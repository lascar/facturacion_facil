#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la relation entre stocks et factures
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_relation_stocks_factures():
    """Test de la relation stocks-factures"""
    print("🔗 TEST RELATION STOCKS-FACTURES")
    print("="*50)
    
    try:
        from database.database import db
        import datetime
        
        # Test 1: Vérifier les méthodes de gestion des stocks
        print("\n--- Test 1: Méthodes de Gestion des Stocks ---")
        
        methods_to_check = [
            'process_invoice_stock_movement',
            'reverse_invoice_stock_movement'
        ]
        
        for method_name in methods_to_check:
            if hasattr(db, method_name):
                print(f"✅ Méthode {method_name} disponible")
            else:
                print(f"❌ Méthode {method_name} manquante")
                return False
        
        # Test 2: Vérifier les stocks initiaux
        print("\n--- Test 2: Stocks Initiaux ---")
        
        products = db.get_all_products()
        if len(products) < 2:
            print("❌ Pas assez de produits pour le test")
            return False
        
        product1 = products[0]
        product2 = products[1]
        
        print(f"✅ Produit 1: {product1['nombre']} (ID: {product1['id']})")
        print(f"   Stock initial: {product1.get('stock_actual', 0)}")
        
        print(f"✅ Produit 2: {product2['nombre']} (ID: {product2['id']})")
        print(f"   Stock initial: {product2.get('stock_actual', 0)}")
        
        # Sauvegarder les stocks initiaux (récupérer les vrais stocks actuels)
        products_fresh = db.get_all_products()
        product1_fresh = next(p for p in products_fresh if p['id'] == product1['id'])
        product2_fresh = next(p for p in products_fresh if p['id'] == product2['id'])

        stock_initial_1 = product1_fresh.get('stock_actual', 0)
        stock_initial_2 = product2_fresh.get('stock_actual', 0)

        print(f"✅ Stocks réels initiaux:")
        print(f"   • Produit 1: {stock_initial_1}")
        print(f"   • Produit 2: {stock_initial_2}")
        
        # Test 3: Créer une facture avec produits
        print("\n--- Test 3: Création Facture avec Produits ---")
        
        clients = db.get_all_clients()
        if not clients:
            print("❌ Aucun client disponible")
            return False
        
        timestamp = datetime.datetime.now().strftime('%H%M%S')
        
        facture_test = {
            'numero': f'F-STOCK-TEST-{timestamp}',
            'fecha': '2024-11-16',
            'vencimiento': '2024-12-16',
            'cliente': {
                'id': clients[0]['id'],
                'nombre': clients[0]['nombre'],
                'nif': clients[0].get('nif', ''),
                'direccion': clients[0].get('direccion', '')
            },
            'lineas': [
                {
                    'producto_id': product1['id'],
                    'cantidad': 2,  # Vendre 2 unités
                    'precio_unitario': 15.0,
                    'iva_aplicado': 21.0,
                    'descuento': 0.0,
                    'subtotal': 30.0,
                    'iva_amount': 6.3,
                    'total': 36.3
                },
                {
                    'producto_id': product2['id'],
                    'cantidad': 1,  # Vendre 1 unité
                    'precio_unitario': 25.0,
                    'iva_aplicado': 21.0,
                    'descuento': 0.0,
                    'subtotal': 25.0,
                    'iva_amount': 5.25,
                    'total': 30.25
                }
            ],
            'subtotal': 55.0,
            'iva_total': 11.55,
            'total': 66.55
        }
        
        print(f"📄 Création facture: {facture_test['numero']}")
        print(f"   • Produit 1: {product1['nombre']} x 2")
        print(f"   • Produit 2: {product2['nombre']} x 1")
        
        # Créer la facture (devrait diminuer les stocks)
        facture_id = db.add_invoice(facture_test)
        print(f"✅ Facture créée avec ID: {facture_id}")
        
        # Test 4: Vérifier les stocks après création
        print("\n--- Test 4: Stocks Après Création ---")

        # Attendre un peu pour que la transaction soit commitée
        time.sleep(0.1)

        # Récupérer les stocks mis à jour
        products_updated = db.get_all_products()
        product1_updated = next(p for p in products_updated if p['id'] == product1['id'])
        product2_updated = next(p for p in products_updated if p['id'] == product2['id'])
        
        stock_apres_1 = product1_updated.get('stock_actual', 0)
        stock_apres_2 = product2_updated.get('stock_actual', 0)
        
        print(f"✅ Produit 1: {product1['nombre']}")
        print(f"   Stock avant: {stock_initial_1}")
        print(f"   Stock après: {stock_apres_1}")
        print(f"   Différence: {stock_apres_1 - stock_initial_1} (attendu: -2)")
        
        print(f"✅ Produit 2: {product2['nombre']}")
        print(f"   Stock avant: {stock_initial_2}")
        print(f"   Stock après: {stock_apres_2}")
        print(f"   Différence: {stock_apres_2 - stock_initial_2} (attendu: -1)")
        
        # Vérifier les diminutions
        diminution_1_correcte = (stock_apres_1 == max(0, stock_initial_1 - 2))
        diminution_2_correcte = (stock_apres_2 == max(0, stock_initial_2 - 1))
        
        if diminution_1_correcte and diminution_2_correcte:
            print("🎉 STOCKS DIMINUÉS CORRECTEMENT !")
            creation_success = True
        else:
            print("❌ PROBLÈME: Stocks non diminués correctement")
            creation_success = False
        
        # Test 5: Modifier la facture
        print("\n--- Test 5: Modification de Facture ---")
        
        # Modifier les quantités
        facture_modifiee = facture_test.copy()
        facture_modifiee['id'] = facture_id
        facture_modifiee['lineas'] = [
            {
                'producto_id': product1['id'],
                'cantidad': 3,  # Changer de 2 à 3
                'precio_unitario': 15.0,
                'iva_aplicado': 21.0,
                'descuento': 0.0,
                'subtotal': 45.0,
                'iva_amount': 9.45,
                'total': 54.45
            },
            {
                'producto_id': product2['id'],
                'cantidad': 2,  # Changer de 1 à 2
                'precio_unitario': 25.0,
                'iva_aplicado': 21.0,
                'descuento': 0.0,
                'subtotal': 50.0,
                'iva_amount': 10.5,
                'total': 60.5
            }
        ]
        facture_modifiee['subtotal'] = 95.0
        facture_modifiee['iva_total'] = 19.95
        facture_modifiee['total'] = 114.95
        
        print(f"📝 Modification facture:")
        print(f"   • Produit 1: 2 → 3 unités")
        print(f"   • Produit 2: 1 → 2 unités")
        
        # Mettre à jour la facture
        success = db.update_invoice(facture_modifiee)
        if success:
            print("✅ Facture modifiée avec succès")
        else:
            print("❌ Erreur modification facture")
            return False
        
        # Test 6: Vérifier les stocks après modification
        print("\n--- Test 6: Stocks Après Modification ---")

        # Attendre un peu pour que la transaction soit commitée
        time.sleep(0.1)

        # Récupérer les stocks finaux
        products_final = db.get_all_products()
        product1_final = next(p for p in products_final if p['id'] == product1['id'])
        product2_final = next(p for p in products_final if p['id'] == product2['id'])
        
        stock_final_1 = product1_final.get('stock_actual', 0)
        stock_final_2 = product2_final.get('stock_actual', 0)
        
        print(f"✅ Produit 1: {product1['nombre']}")
        print(f"   Stock initial: {stock_initial_1}")
        print(f"   Stock final: {stock_final_1}")
        print(f"   Différence totale: {stock_final_1 - stock_initial_1} (attendu: -3)")
        
        print(f"✅ Produit 2: {product2['nombre']}")
        print(f"   Stock initial: {stock_initial_2}")
        print(f"   Stock final: {stock_final_2}")
        print(f"   Différence totale: {stock_final_2 - stock_initial_2} (attendu: -2)")
        
        # Vérifier les diminutions finales
        diminution_finale_1_correcte = (stock_final_1 == max(0, stock_initial_1 - 3))
        diminution_finale_2_correcte = (stock_final_2 == max(0, stock_initial_2 - 2))
        
        if diminution_finale_1_correcte and diminution_finale_2_correcte:
            print("🎉 MODIFICATION AVEC STOCKS CORRECTE !")
            modification_success = True
        else:
            print("❌ PROBLÈME: Stocks après modification incorrects")
            modification_success = False
        
        return creation_success and modification_success
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_relation_stocks_factures()
        
        print("\n" + "="*50)
        print("RÉSUMÉ DU TEST RELATION STOCKS-FACTURES")
        print("="*50)
        
        if success:
            print("🎉 TEST RELATION STOCKS-FACTURES RÉUSSI !")
            print("\n✨ FONCTIONNALITÉS VALIDÉES :")
            print("   ✅ Méthodes de gestion des stocks")
            print("   ✅ Diminution automatique lors de création")
            print("   ✅ Reversion et nouveau calcul lors de modification")
            print("   ✅ Stocks cohérents avec les ventes")
            print("   ✅ Protection contre stock négatif")
            
            print("\n🔗 RELATION STOCKS-FACTURES OPÉRATIONNELLE !")
            print("\n📦 FONCTIONNEMENT :")
            print("   • Création facture → Stock diminué automatiquement")
            print("   • Modification facture → Stock revertí puis recalculé")
            print("   • Suppression facture → Stock restauré (à implémenter)")
            print("   • Stock minimum 0 → Protection intégrée")
            
            print("\n🚀 UTILISATION :")
            print("   1. Créez une facture avec produits")
            print("   2. Vérifiez les stocks → Diminués automatiquement")
            print("   3. Modifiez la facture → Stocks recalculés")
            print("   4. Gestion automatique et transparente")
            
            return 0
        else:
            print("❌ TEST RELATION STOCKS-FACTURES ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
