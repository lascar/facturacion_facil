#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour identifier les problèmes de synchronisation des stocks après migration
"""

import sys
import os
import sqlite3

# Ajouter le répertoire racine au path
sys.path.append('.')

from database.test_database import get_test_database
from database.migration_manager import MigrationManager
from database.database_improved import DatabaseImproved

def test_database_structure_after_migration():
    """Tester la structure de la base après migration"""
    print("=== Test Structure Base de Données Après Migration ===")
    
    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path
    
    # Exécuter la migration
    migration_manager = MigrationManager(db_path)
    migration_manager.remove_stock_columns_from_productos()
    
    # Créer des données de test
    db_improved = DatabaseImproved(db_path)
    product_data = {
        'nombre': 'Test Product',
        'referencia': 'TEST001',
        'precio': 25.50,
        'categoria': 'Test',
        'stock_actual': 100
    }
    db_improved.add_product(product_data)
    
    # Vérifier la structure
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n1. Structure table productos:")
    cursor.execute("PRAGMA table_info(productos)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")
    
    column_names = [col[1] for col in columns]
    if 'stock_actual' in column_names:
        print("   ❌ PROBLÈME: stock_actual encore présent dans productos")
    else:
        print("   ✅ OK: stock_actual supprimé de productos")
    
    print("\n2. Données dans table stock:")
    cursor.execute("SELECT producto_id, cantidad_disponible FROM stock")
    stock_data = cursor.fetchall()
    print(f"   Nombre d'entrées: {len(stock_data)}")
    for row in stock_data:
        print(f"   - Produit {row[0]}: {row[1]} unités")
    
    print("\n3. Test récupération produits avec stock (JOIN):")
    cursor.execute("""
        SELECT p.id, p.nombre, p.referencia, 
               COALESCE(s.cantidad_disponible, 0) as stock_actual
        FROM productos p
        LEFT JOIN stock s ON p.id = s.producto_id
    """)
    products_with_stock = cursor.fetchall()
    for row in products_with_stock:
        print(f"   - {row[1]} (ID: {row[0]}): Stock {row[3]}")
    
    conn.close()
    test_db.cleanup()
    
    return len(stock_data) > 0 and 'stock_actual' not in column_names

def test_current_ui_code_issues():
    """Identifier les problèmes dans le code UI actuel"""
    print("\n=== Analyse Code UI Actuel ===")
    
    issues = []
    
    # Analyser stock_pyqt5.py
    try:
        with open('ui/stock_pyqt5.py', 'r', encoding='utf-8') as f:
            stock_code = f.read()
        
        if "producto.get('stock_actual'" in stock_code:
            issues.append("❌ stock_pyqt5.py: Utilise encore producto.get('stock_actual')")
        
        if "db.get_all_products()" in stock_code:
            issues.append("❌ stock_pyqt5.py: Utilise db.get_all_products() qui ne fait pas de JOIN")
        
        if "update_product_stock" in stock_code:
            issues.append("❌ stock_pyqt5.py: Utilise update_product_stock au lieu de Stock.update_stock")
            
    except Exception as e:
        issues.append(f"❌ Erreur lecture stock_pyqt5.py: {e}")
    
    # Analyser productos_pyqt5.py
    try:
        with open('ui/productos_pyqt5.py', 'r', encoding='utf-8') as f:
            productos_code = f.read()
        
        if "db_improved.get_all_products()" in productos_code:
            issues.append("❌ productos_pyqt5.py: get_all_products() ne fait peut-être pas de JOIN avec stock")
        
        if "stock_actual" in productos_code and "get('stock_actual'" in productos_code:
            issues.append("❌ productos_pyqt5.py: Assume que stock_actual est dans les données produit")
            
    except Exception as e:
        issues.append(f"❌ Erreur lecture productos_pyqt5.py: {e}")
    
    # Analyser database_improved.py
    try:
        with open('database/database_improved.py', 'r', encoding='utf-8') as f:
            db_code = f.read()
        
        if "get_all_products" in db_code:
            if "LEFT JOIN stock" not in db_code:
                issues.append("❌ database_improved.py: get_all_products() ne fait pas de JOIN avec stock")
            else:
                issues.append("✅ database_improved.py: get_all_products() fait un JOIN avec stock")
                
    except Exception as e:
        issues.append(f"❌ Erreur lecture database_improved.py: {e}")
    
    print("\nProblèmes identifiés:")
    for issue in issues:
        print(f"   {issue}")
    
    return issues

def main():
    """Fonction principale"""
    print("🔍 DIAGNOSTIC SYNCHRONISATION STOCKS APRÈS MIGRATION")
    print("=" * 60)
    
    # Test 1: Structure base de données
    db_ok = test_database_structure_after_migration()
    
    # Test 2: Problèmes code UI
    ui_issues = test_current_ui_code_issues()
    
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ")
    print("=" * 60)
    
    if db_ok:
        print("✅ Base de données: Migration OK, structure correcte")
    else:
        print("❌ Base de données: Problèmes détectés")
    
    if ui_issues:
        print(f"❌ Code UI: {len(ui_issues)} problèmes détectés")
        print("\n🔧 ACTIONS NÉCESSAIRES:")
        print("   1. Modifier stock_pyqt5.py pour utiliser la nouvelle structure")
        print("   2. Modifier productos_pyqt5.py pour récupérer les stocks via JOIN")
        print("   3. Adapter database_improved.py si nécessaire")
        print("   4. Tester la synchronisation entre fenêtres")
    else:
        print("✅ Code UI: Aucun problème détecté")

if __name__ == '__main__':
    main()
