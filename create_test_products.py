#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer des produits de test pour vérifier la synchronisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import db

def create_test_products():
    """Créer des produits de test"""
    
    print("🧪 CRÉATION DE PRODUITS DE TEST")
    print("=" * 50)
    
    # Produits de test
    test_products = [
        {
            'nombre': 'Producto Test 1',
            'referencia': 'TEST001',
            'precio': 10.50,
            'stock_actual': 25,
            'stock_minimo': 5,
            'categoria': 'Test',
            'descripcion': 'Producto de prueba para sincronización'
        },
        {
            'nombre': 'Producto Test 2',
            'referencia': 'TEST002',
            'precio': 15.75,
            'stock_actual': 10,
            'stock_minimo': 3,
            'categoria': 'Test',
            'descripcion': 'Segundo producto de prueba'
        },
        {
            'nombre': 'Producto Test 3',
            'referencia': None,  # Test sans référence
            'precio': 8.25,
            'stock_actual': 50,
            'stock_minimo': 10,
            'categoria': 'Test',
            'descripcion': 'Producto sin referencia'
        }
    ]
    
    created_count = 0
    
    for product_data in test_products:
        try:
            # Vérifier si le produit existe déjà
            all_products = db.get_all_products()
            existing = any(p.get('nombre') == product_data['nombre'] for p in all_products)
            if existing:
                print(f"   ⚠️  Produit existe déjà: {product_data['nombre']}")
                continue

            # Créer le produit
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, referencia, precio, stock_actual, stock_minimo, categoria, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product_data['nombre'],
                product_data['referencia'],
                product_data['precio'],
                product_data['stock_actual'],
                product_data['stock_minimo'],
                product_data['categoria'],
                product_data['descripcion']
            ))
            product_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"   ✅ Créé: {product_data['nombre']} (ID: {product_id})")
            created_count += 1
            
        except Exception as e:
            print(f"   ❌ Erreur création {product_data['nombre']}: {e}")
    
    print(f"\n📊 Résumé:")
    print(f"   ✅ Produits créés: {created_count}")
    
    # Afficher tous les produits
    all_products = db.get_all_products()
    print(f"   📦 Total produits: {len(all_products)}")
    
    if all_products:
        print("\n📋 Produits disponibles:")
        for product in all_products[:5]:  # Afficher les 5 premiers
            stock = product.get('stock_actual', 0)
            print(f"   • {product.get('nombre', 'N/A')} - Stock: {stock}")
    
    print(f"\n🎯 SUCCÈS!")
    print("   • Produits de test créés")
    print("   • Prêt pour tester la synchronisation")
    print("   • Ouvrez les fenêtres Stock et Productos")

if __name__ == "__main__":
    create_test_products()
