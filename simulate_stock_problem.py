#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation du problème de stock pour debug
"""

import sys
import os
import time
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def simulate_window_opening():
    """Simuler l'ouverture des deux fenêtres"""
    print("🎭 SIMULATION DU PROBLÈME DE STOCK")
    print("=" * 50)
    
    try:
        from database.database import db
        
        # Vérifier s'il y a des données
        productos = db.get_all_products()
        if not productos:
            print("⚠️  Base de données vide - Création de données de test...")
            create_test_data()
            productos = db.get_all_products()
        
        print(f"📊 {len(productos)} produits trouvés dans la base")
        
        # Simuler fenêtre de création (gauche)
        print("\n🪟 SIMULATION FENÊTRE CRÉATION (GAUCHE)")
        print("-" * 40)
        timestamp1 = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp1}] CrearFacturaDialog - Llamando db.get_all_products()")
        
        productos_creation = db.get_all_products()
        print(f"[{timestamp1}] CrearFacturaDialog - Recibidos {len(productos_creation)} productos")
        
        for producto in productos_creation[:3]:  # Afficher les 3 premiers
            stock = producto.get('stock_actual', 0)
            print(f"[{timestamp1}] CrearFacturaDialog - Producto: {producto['nombre']}, Stock: {stock}, ID: {producto.get('id')}")
        
        # Petite pause pour simuler l'interaction utilisateur
        time.sleep(0.5)
        
        # Simuler fenêtre d'édition (droite)
        print("\n🪟 SIMULATION FENÊTRE ÉDITION (DROITE)")
        print("-" * 40)
        timestamp2 = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp2}] EditarFacturaDialog - Llamando db.get_all_products()")
        
        productos_edition = db.get_all_products()
        print(f"[{timestamp2}] EditarFacturaDialog - Recibidos {len(productos_edition)} productos")
        
        for producto in productos_edition[:3]:  # Afficher les 3 premiers
            stock = producto.get('stock_actual', 0)
            print(f"[{timestamp2}] EditarFacturaDialog - Producto: {producto['nombre']}, Stock: {stock}, ID: {producto.get('id')}")
        
        # Analyser les différences
        print("\n🔍 ANALYSE DES DIFFÉRENCES")
        print("-" * 30)
        
        differences_found = False
        for i, (p1, p2) in enumerate(zip(productos_creation, productos_edition)):
            stock1 = p1.get('stock_actual', 0)
            stock2 = p2.get('stock_actual', 0)
            
            if stock1 != stock2:
                print(f"❌ DIFFÉRENCE TROUVÉE:")
                print(f"   Produit: {p1['nombre']} (ID: {p1.get('id')})")
                print(f"   Création: {stock1}")
                print(f"   Édition: {stock2}")
                differences_found = True
        
        if not differences_found:
            print("✅ Aucune différence trouvée - Stocks identiques")
            print("\n💡 Le problème pourrait venir de:")
            print("   - Calcul de stock disponible vs stock réel")
            print("   - Cache dans l'interface utilisateur")
            print("   - Données affichées différemment")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur simulation: {e}")
        return False

def create_test_data():
    """Créer des données de test si la base est vide"""
    try:
        from database.database import db
        
        print("📝 Création de données de test...")
        
        # Créer quelques produits de test
        test_products = [
            {
                'nombre': 'Producto Test A',
                'descripcion': 'Producto de prueba A',
                'precio_venta': 10.50,
                'stock_actual': 2,  # Stock comme mentionné par l'utilisateur
                'stock_minimo': 1,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto Test B', 
                'descripcion': 'Producto de prueba B',
                'precio_venta': 25.00,
                'stock_actual': 3,  # Stock comme mentionné par l'utilisateur
                'stock_minimo': 2,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto Test C',
                'descripcion': 'Producto de prueba C', 
                'precio_venta': 15.75,
                'stock_actual': 5,
                'stock_minimo': 1,
                'categoria': 'Test'
            }
        ]
        
        for product in test_products:
            try:
                db.add_product(product)
                print(f"   ✅ Créé: {product['nombre']} (Stock: {product['stock_actual']})")
            except Exception as e:
                print(f"   ⚠️  Erreur création {product['nombre']}: {e}")
        
        print("✅ Données de test créées")
        
    except Exception as e:
        print(f"❌ Erreur création données test: {e}")

def simulate_stock_calculation():
    """Simuler le calcul de stock disponible pour édition"""
    print("\n🧮 SIMULATION CALCUL STOCK DISPONIBLE")
    print("-" * 40)
    
    try:
        from database.database import db
        
        productos = db.get_all_products()
        if not productos:
            print("⚠️  Aucun produit pour simulation")
            return
        
        # Prendre le premier produit
        producto = productos[0]
        stock_actual = producto.get('stock_actual', 0)
        
        print(f"📦 Produit: {producto['nombre']}")
        print(f"📊 Stock actuel en base: {stock_actual}")
        
        # Simuler une facture existante avec ce produit
        cantidad_en_factura = 7  # Exemple
        
        print(f"📋 Quantité dans facture existante: {cantidad_en_factura}")
        
        # Calcul pour fenêtre de création (stock réel)
        stock_creation = stock_actual
        print(f"🪟 Fenêtre création afficherait: {stock_creation}")
        
        # Calcul pour fenêtre d'édition (stock disponible)
        stock_edition = stock_actual + cantidad_en_factura
        print(f"🪟 Fenêtre édition afficherait: {stock_edition}")
        
        print(f"\n💡 Différence: {stock_edition - stock_creation} unités")
        print("   (Normal si le produit est dans la facture en cours d'édition)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur simulation calcul: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC PROBLÈME DE STOCK")
    print("=" * 50)
    
    # Test 1: Simulation ouverture fenêtres
    if not simulate_window_opening():
        return False
    
    # Test 2: Simulation calcul stock
    if not simulate_stock_calculation():
        return False
    
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSTIC TERMINÉ")
    print("\n📋 ACTIONS RECOMMANDÉES:")
    print("1. Vérifiez les logs de l'application réelle")
    print("2. Comparez avec cette simulation")
    print("3. Identifiez si c'est un calcul normal ou un bug")
    print("4. Appliquez la correction appropriée")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n✅ Simulation terminée: {success}")
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        success = False
    
    sys.exit(0 if success else 1)
