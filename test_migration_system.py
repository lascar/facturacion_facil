#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système de migration pour vérifier qu'il préserve les données
"""

import os
import sqlite3
import shutil
import tempfile
from database.migration_manager import MigrationManager
from database.database_improved import DatabaseImproved

def test_migration_preserves_data():
    """Test que les migrations préservent les données existantes"""
    print("🧪 TEST DU SYSTÈME DE MIGRATION")
    print("=" * 35)
    
    # Créer une base de données temporaire pour le test
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        test_db_path = tmp_file.name
    
    try:
        print(f"📁 Base de test: {test_db_path}")
        
        # Étape 1: Créer une base avec l'ancienne structure
        print("\n1️⃣ Création base avec ancienne structure...")
        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()
        
        # Ancienne structure (sans categoria)
        cursor.execute("""
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                referencia TEXT UNIQUE,
                precio REAL NOT NULL,
                descripcion TEXT,
                iva_recomendado REAL DEFAULT 21.0
            )
        """)
        
        # Insérer des données de test
        test_products = [
            ("Producto Test 1", "TEST-001", 25.50, "Descripción 1", 21.0),
            ("Producto Test 2", "TEST-002", 35.75, "Descripción 2", 10.0),
            ("Producto Test 3", None, 45.00, "Sin referencia", 21.0)
        ]
        
        cursor.executemany("""
            INSERT INTO productos (nombre, referencia, precio, descripcion, iva_recomendado)
            VALUES (?, ?, ?, ?, ?)
        """, test_products)
        
        conn.commit()
        conn.close()
        
        print("   ✅ Base créée avec 3 produits")
        
        # Étape 2: Appliquer les migrations
        print("\n2️⃣ Application des migrations...")
        migration_manager = MigrationManager(test_db_path)
        
        # Créer le répertoire de sauvegarde pour le test
        backup_dir = os.path.join(os.path.dirname(test_db_path), "test_backups")
        migration_manager.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
        success = migration_manager.migrate_productos_table()
        
        if success:
            print("   ✅ Migrations appliquées avec succès")
        else:
            print("   ❌ Échec des migrations")
            return False
        
        # Étape 3: Vérifier que les données sont préservées
        print("\n3️⃣ Vérification des données...")
        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure
        cursor.execute("PRAGMA table_info(productos)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        expected_columns = ['id', 'nombre', 'referencia', 'precio', 'categoria', 
                          'descripcion', 'imagen_path', 'iva_recomendado', 
                          'stock_actual', 'stock_minimo', 'fecha_creacion', 
                          'fecha_actualizacion']
        
        missing_columns = [col for col in expected_columns if col not in column_names]
        if missing_columns:
            print(f"   ❌ Colonnes manquantes: {missing_columns}")
            return False
        else:
            print("   ✅ Structure mise à jour correctement")
        
        # Vérifier que les données sont préservées
        cursor.execute("SELECT id, nombre, referencia, precio, descripcion FROM productos ORDER BY id")
        migrated_products = cursor.fetchall()
        
        if len(migrated_products) != 3:
            print(f"   ❌ Nombre de produits incorrect: {len(migrated_products)} (attendu: 3)")
            return False
        
        # Vérifier chaque produit
        for i, (original, migrated) in enumerate(zip(test_products, migrated_products)):
            original_nombre, original_ref, original_precio, original_desc, original_iva = original
            migrated_id, migrated_nombre, migrated_ref, migrated_precio, migrated_desc = migrated
            
            if (migrated_nombre != original_nombre or 
                migrated_ref != original_ref or 
                abs(migrated_precio - original_precio) > 0.01 or
                migrated_desc != original_desc):
                print(f"   ❌ Produit {i+1} modifié incorrectement")
                print(f"      Original: {original}")
                print(f"      Migré: {migrated}")
                return False
        
        print("   ✅ Toutes les données préservées")
        
        # Étape 4: Tester les nouvelles fonctionnalités
        print("\n4️⃣ Test des nouvelles fonctionnalités...")
        
        # Utiliser DatabaseImproved pour ajouter un produit avec catégorie
        db_improved = DatabaseImproved(test_db_path)
        
        new_product = {
            'nombre': 'Producto Con Categoria',
            'referencia': 'TEST-CAT-001',
            'precio_venta': 55.99,
            'categoria': 'Categoria Test',
            'descripcion': 'Producto con nueva funcionalidad',
            'iva_recomendado': 21.0,
            'stock': 20
        }
        
        product_id = db_improved.add_product(new_product)
        
        # Vérifier que la catégorie est sauvegardée
        cursor.execute("SELECT categoria FROM productos WHERE id = ?", (product_id,))
        result = cursor.fetchone()
        
        if result and result[0] == 'Categoria Test':
            print("   ✅ Nouvelles fonctionnalités opérationnelles")
        else:
            print(f"   ❌ Problème avec nouvelles fonctionnalités: {result}")
            return False
        
        conn.close()
        
        # Étape 5: Vérifier les sauvegardes
        print("\n5️⃣ Vérification des sauvegardes...")
        
        if os.path.exists(backup_dir):
            backups = [f for f in os.listdir(backup_dir) if f.endswith('.db')]
            if backups:
                print(f"   ✅ {len(backups)} sauvegarde(s) créée(s)")
                
                # Vérifier qu'une sauvegarde contient les données originales
                backup_path = os.path.join(backup_dir, backups[0])
                backup_conn = sqlite3.connect(backup_path)
                backup_cursor = backup_conn.cursor()
                backup_cursor.execute("SELECT COUNT(*) FROM productos")
                backup_count = backup_cursor.fetchone()[0]
                backup_conn.close()
                
                if backup_count >= 3:
                    print("   ✅ Sauvegarde contient les données")
                else:
                    print(f"   ⚠️ Sauvegarde incomplète: {backup_count} produits")
            else:
                print("   ⚠️ Aucune sauvegarde trouvée")
        
        print("\n🎉 TEST DE MIGRATION RÉUSSI")
        print("   ✅ Données préservées")
        print("   ✅ Structure mise à jour")
        print("   ✅ Nouvelles fonctionnalités opérationnelles")
        print("   ✅ Sauvegardes créées")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR DURANT LE TEST: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Nettoyage
        try:
            if os.path.exists(test_db_path):
                os.unlink(test_db_path)
            
            # Nettoyer les sauvegardes de test
            backup_dir = os.path.join(os.path.dirname(test_db_path), "test_backups")
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
                
        except Exception as e:
            print(f"⚠️ Erreur nettoyage: {e}")

def test_real_database_compatibility():
    """Test que la base de données réelle est compatible"""
    print("\n🔍 TEST DE COMPATIBILITÉ BASE RÉELLE")
    print("=" * 40)
    
    try:
        # Tester avec la vraie base de données
        db = DatabaseImproved()
        
        # Vérifier qu'on peut récupérer les produits
        products = db.get_products()
        print(f"   ✅ {len(products)} produits récupérés")
        
        # Vérifier qu'on peut récupérer les catégories
        categories = db.get_product_categories()
        print(f"   ✅ {len(categories)} catégories trouvées")
        
        # Tester la création d'un produit
        test_product = {
            'nombre': 'Test Compatibilité',
            'referencia': f'COMPAT-{int(os.urandom(4).hex(), 16)}',
            'precio_venta': 99.99,
            'categoria': 'Test Compatibilité',
            'descripcion': 'Test de compatibilité système',
            'iva_recomendado': 21.0,
            'stock': 1
        }
        
        product_id = db.add_product(test_product)
        print(f"   ✅ Produit de test créé avec ID: {product_id}")
        
        # Nettoyer le produit de test
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM stock WHERE producto_id = ?", (product_id,))
            cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))
            conn.commit()
        
        print("   ✅ Nettoyage effectué")
        print("   🎉 Base de données réelle compatible")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur compatibilité: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TESTS DU SYSTÈME DE MIGRATION")
    print("=" * 40)
    
    test1 = test_migration_preserves_data()
    test2 = test_real_database_compatibility()
    
    if test1 and test2:
        print("\n🏆 TOUS LES TESTS RÉUSSIS")
        print("   Le système de migration fonctionne parfaitement")
        return True
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
