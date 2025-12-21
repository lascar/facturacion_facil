#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple des corrections pour la synchronisation des stocks
"""

import sys
import os
import sqlite3

# Ajouter le répertoire racine au path
sys.path.append('.')

from database.test_database import get_test_database
from database.migration_manager import MigrationManager
from database.models import Stock

def test_stock_operations_after_migration():
    """Test complet des opérations stock après migration"""
    print("🔧 TEST OPÉRATIONS STOCK APRÈS MIGRATION")
    print("=" * 50)
    
    # Créer une base de test
    test_db = get_test_database()
    db_path = test_db.db_path
    
    try:
        # Exécuter la migration
        print("1. Exécution de la migration...")
        migration_manager = MigrationManager(db_path)
        migration_manager.remove_stock_columns_from_productos()
        print("   ✅ Migration terminée")
        
        # Créer un produit manuellement
        print("\n2. Création d'un produit avec stock...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO productos (nombre, referencia, precio, categoria)
            VALUES (?, ?, ?, ?)
        """, ('Test Product', 'TEST001', 25.50, 'Test'))
        product_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (product_id, 100))
        
        conn.commit()
        conn.close()
        print(f"   ✅ Produit créé (ID: {product_id}) avec stock initial: 100")
        
        # Test Stock.get_by_product
        print("\n3. Test Stock.get_by_product()...")
        stock = Stock.get_by_product(product_id, db_path)
        print(f"   Stock récupéré: {stock}")
        assert stock == 100, f"Stock devrait être 100, obtenu: {stock}"
        print("   ✅ Stock.get_by_product() fonctionne")
        
        # Test Stock.update_stock_direct
        print("\n4. Test Stock.update_stock_direct()...")
        Stock.update_stock_direct(product_id, 75, db_path)
        new_stock = Stock.get_by_product(product_id, db_path)
        print(f"   Nouveau stock: {new_stock}")
        assert new_stock == 75, f"Stock devrait être 75, obtenu: {new_stock}"
        print("   ✅ Stock.update_stock_direct() fonctionne")
        
        # Test récupération avec JOIN
        print("\n5. Test récupération produits avec stock (JOIN)...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, p.referencia, 
                   COALESCE(s.cantidad_disponible, 0) as stock_actual
            FROM productos p
            LEFT JOIN stock s ON p.id = s.producto_id
            WHERE p.id = ?
        """, (product_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"   Produit: {result[1]} (ID: {result[0]})")
            print(f"   Stock via JOIN: {result[3]}")
            assert result[3] == 75, f"Stock via JOIN devrait être 75, obtenu: {result[3]}"
            print("   ✅ JOIN productos-stock fonctionne")
        else:
            raise AssertionError("Aucun résultat trouvé avec JOIN")
        
        # Test Stock.get_all
        print("\n6. Test Stock.get_all()...")
        all_stock = Stock.get_all(db_path)
        print(f"   Nombre d'entrées stock: {len(all_stock)}")
        assert len(all_stock) > 0, "Devrait avoir au moins une entrée stock"
        
        stock_entry = next((s for s in all_stock if s[0] == product_id), None)
        assert stock_entry is not None, "Devrait trouver l'entrée stock du produit"
        assert stock_entry[1] == 75, f"Stock dans get_all devrait être 75, obtenu: {stock_entry[1]}"
        print("   ✅ Stock.get_all() fonctionne")
        
        print("\n" + "=" * 50)
        print("🎉 TOUS LES TESTS PASSENT !")
        print("✅ Les opérations stock fonctionnent correctement après migration")
        print("\n🔄 Prochaines étapes:")
        print("   1. Tester l'interface graphique")
        print("   2. Vérifier la synchronisation entre fenêtres")
        print("   3. Tester le bouton Actualizar")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur durant le test: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        test_db.cleanup()

def test_ui_code_analysis():
    """Analyser le code UI pour vérifier les corrections"""
    print("\n🔍 ANALYSE CODE UI APRÈS CORRECTIONS")
    print("=" * 50)
    
    corrections_applied = []
    remaining_issues = []
    
    # Vérifier stock_pyqt5.py
    try:
        with open('ui/stock_pyqt5.py', 'r', encoding='utf-8') as f:
            stock_code = f.read()
        
        if "from database.database_improved import DatabaseImproved" in stock_code:
            corrections_applied.append("✅ stock_pyqt5.py: Import DatabaseImproved")
        else:
            remaining_issues.append("❌ stock_pyqt5.py: N'importe pas DatabaseImproved")
        
        if "db_improved.get_all_products()" in stock_code:
            corrections_applied.append("✅ stock_pyqt5.py: Utilise db_improved.get_all_products()")
        else:
            remaining_issues.append("❌ stock_pyqt5.py: N'utilise pas db_improved.get_all_products()")
        
        if "Stock.update_stock_direct" in stock_code:
            corrections_applied.append("✅ stock_pyqt5.py: Utilise Stock.update_stock_direct")
        else:
            remaining_issues.append("❌ stock_pyqt5.py: N'utilise pas Stock.update_stock_direct")
            
    except Exception as e:
        remaining_issues.append(f"❌ Erreur lecture stock_pyqt5.py: {e}")
    
    print("Corrections appliquées:")
    for correction in corrections_applied:
        print(f"   {correction}")
    
    if remaining_issues:
        print("\nProblèmes restants:")
        for issue in remaining_issues:
            print(f"   {issue}")
    else:
        print("\n🎉 Toutes les corrections ont été appliquées !")
    
    return len(remaining_issues) == 0

def main():
    """Fonction principale"""
    print("🧪 TEST COMPLET CORRECTIONS SYNCHRONISATION STOCKS")
    print("=" * 60)
    
    # Test 1: Opérations stock
    test1_ok = test_stock_operations_after_migration()
    
    # Test 2: Analyse code UI
    test2_ok = test_ui_code_analysis()
    
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ FINAL")
    print("=" * 60)
    
    if test1_ok and test2_ok:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Base de données: Migration et opérations OK")
        print("✅ Code UI: Corrections appliquées")
        print("\n🚀 PRÊT POUR LES TESTS D'INTERFACE")
    else:
        print("❌ Des problèmes subsistent")
        if not test1_ok:
            print("   - Problèmes avec les opérations stock")
        if not test2_ok:
            print("   - Corrections UI incomplètes")

if __name__ == '__main__':
    main()
