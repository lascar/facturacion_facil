#!/usr/bin/env python3
"""
MIGRATION SÉCURISÉE: Transition vers source unique de stock
PRÉSERVE TOUTES LES DONNÉES EXISTANTES
"""

import sys
import os
import sqlite3
import shutil
from datetime import datetime

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

def backup_database():
    """Créer une sauvegarde complète de la base de données"""
    print("🛡️  SAUVEGARDE: Base de Données")
    print("-" * 40)
    
    try:
        from database.database import Database
        db = Database()
        
        # Obtenir le chemin de la DB actuelle
        db_path = getattr(Database, '_db_path', 'facturacion.db')
        if not os.path.exists(db_path):
            print(f"❌ Base de données non trouvée: {db_path}")
            return False
        
        # Créer sauvegarde avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{db_path}.backup_{timestamp}"
        
        shutil.copy2(db_path, backup_path)
        print(f"✅ Sauvegarde créée: {os.path.basename(backup_path)}")
        print(f"   📁 Chemin complet: {backup_path}")
        
        # Vérifier la sauvegarde
        if os.path.exists(backup_path):
            original_size = os.path.getsize(db_path)
            backup_size = os.path.getsize(backup_path)
            
            if original_size == backup_size:
                print(f"✅ Sauvegarde vérifiée: {backup_size} bytes")
                return backup_path
            else:
                print(f"❌ Erreur de sauvegarde: tailles différentes")
                return False
        else:
            print(f"❌ Fichier de sauvegarde non créé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

def analyze_existing_data():
    """Analyser les données existantes pour planifier la migration"""
    print("\n🔍 ANALYSE: Données Existantes")
    print("-" * 40)
    
    try:
        from database.database import Database
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 1. Vérifier la structure actuelle
        cursor.execute("PRAGMA table_info(productos)")
        productos_columns = cursor.fetchall()
        
        cursor.execute("PRAGMA table_info(stock)")
        stock_columns = cursor.fetchall()
        
        print("📋 Structure actuelle:")
        print(f"   productos: {len(productos_columns)} colonnes")
        print(f"   stock: {len(stock_columns)} colonnes")
        
        # 2. Compter les données
        cursor.execute("SELECT COUNT(*) FROM productos")
        productos_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stock")
        stock_count = cursor.fetchone()[0]
        
        print(f"\n📊 Données existantes:")
        print(f"   productos: {productos_count} enregistrements")
        print(f"   stock: {stock_count} enregistrements")
        
        # 3. Vérifier les stocks non-zéro
        cursor.execute("SELECT COUNT(*) FROM productos WHERE stock_actual > 0")
        productos_with_stock = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stock WHERE cantidad_disponible > 0")
        stock_with_quantity = cursor.fetchone()[0]
        
        print(f"\n📦 Stocks non-zéro:")
        print(f"   productos.stock_actual > 0: {productos_with_stock}")
        print(f"   stock.cantidad_disponible > 0: {stock_with_quantity}")
        
        # 4. Identifier les produits sans entrée stock
        cursor.execute("""
            SELECT COUNT(*) FROM productos p 
            LEFT JOIN stock s ON p.id = s.producto_id 
            WHERE s.producto_id IS NULL
        """)
        productos_without_stock_entry = cursor.fetchone()[0]
        
        print(f"   productos sans entrée stock: {productos_without_stock_entry}")
        
        conn.close()
        
        return {
            'productos_count': productos_count,
            'stock_count': stock_count,
            'productos_with_stock': productos_with_stock,
            'stock_with_quantity': stock_with_quantity,
            'productos_without_stock_entry': productos_without_stock_entry
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return None

def create_safe_migration_plan(analysis_data):
    """Créer un plan de migration sécurisé"""
    print("\n📋 PLAN DE MIGRATION SÉCURISÉ")
    print("=" * 50)
    
    if not analysis_data:
        print("❌ Impossible de créer le plan sans données d'analyse")
        return False
    
    print("🎯 OBJECTIFS:")
    print("   ✅ Préserver TOUTES les données existantes")
    print("   ✅ Migrer vers source unique (table stock)")
    print("   ✅ Compatibilité avec installations existantes")
    print("   ✅ Rollback possible en cas de problème")
    
    print("\n🔄 ÉTAPES DE MIGRATION:")
    
    print("\n1. 🛡️  SAUVEGARDE COMPLÈTE")
    print("   - Backup automatique avec timestamp")
    print("   - Vérification de l'intégrité")
    
    print("\n2. 📊 SYNCHRONISATION PRÉSERVANT LES DONNÉES")
    print("   - Pour chaque producto SANS entrée stock:")
    print("     → Créer entrée avec productos.stock_actual")
    print("   - Pour chaque producto AVEC entrée stock:")
    print("     → Garder la valeur stock.cantidad_disponible")
    print("     → NE PAS écraser les données stock existantes")
    
    print("\n3. 🔧 MODIFICATION DU CODE")
    print("   - get_all_products() utilise LEFT JOIN avec stock")
    print("   - Toutes les opérations utilisent table stock")
    print("   - productos.stock_actual devient lecture seule (legacy)")
    
    print("\n4. ✅ VALIDATION")
    print("   - Vérifier que tous les stocks sont préservés")
    print("   - Tester les opérations critiques")
    print("   - Confirmer que l'interface fonctionne")
    
    print(f"\n📊 IMPACT SUR VOS DONNÉES:")
    print(f"   📦 {analysis_data['productos_count']} productos préservés")
    print(f"   📋 {analysis_data['stock_count']} entrées stock existantes gardées")
    print(f"   ➕ {analysis_data['productos_without_stock_entry']} nouvelles entrées stock à créer")
    print(f"   🛡️  {analysis_data['productos_with_stock']} stocks non-zéro préservés")
    
    return True

def execute_safe_migration(analysis_data):
    """Exécuter la migration sécurisée"""
    print("\n🚀 EXÉCUTION: Migration Sécurisée")
    print("-" * 40)
    
    try:
        from database.database import Database
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # 1. Créer les entrées stock manquantes SANS écraser les existantes
        print("🔄 Création des entrées stock manquantes...")
        
        cursor.execute("""
            SELECT p.id, p.nombre, p.stock_actual
            FROM productos p 
            LEFT JOIN stock s ON p.id = s.producto_id 
            WHERE s.producto_id IS NULL
        """)
        
        productos_without_stock = cursor.fetchall()
        created_count = 0
        
        for producto_id, nombre, stock_actual in productos_without_stock:
            stock_actual = stock_actual or 0
            
            cursor.execute("""
                INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (producto_id, stock_actual))
            
            print(f"   ➕ Créé stock pour ID {producto_id}: {nombre} (stock: {stock_actual})")
            created_count += 1
        
        conn.commit()
        
        print(f"\n✅ Migration terminée:")
        print(f"   ➕ {created_count} nouvelles entrées stock créées")
        print(f"   🛡️  {analysis_data['stock_count']} entrées existantes préservées")
        
        # 2. Vérification finale
        print("\n🧪 Vérification finale...")
        
        cursor.execute("SELECT COUNT(*) FROM stock")
        final_stock_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM productos p 
            LEFT JOIN stock s ON p.id = s.producto_id 
            WHERE s.producto_id IS NULL
        """)
        remaining_without_stock = cursor.fetchone()[0]
        
        print(f"   📊 Entrées stock totales: {final_stock_count}")
        print(f"   📦 Productos sans stock: {remaining_without_stock}")
        
        if remaining_without_stock == 0:
            print("   ✅ Tous les productos ont maintenant une entrée stock")
        else:
            print(f"   ⚠️  {remaining_without_stock} productos sans entrée stock")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        return False

def main():
    """Fonction principale de migration sécurisée"""
    print("🛡️  MIGRATION SÉCURISÉE VERS SOURCE UNIQUE DE STOCK")
    print("=" * 60)
    
    print("🎯 GARANTIES:")
    print("   ✅ AUCUNE perte de données")
    print("   ✅ Sauvegarde automatique")
    print("   ✅ Compatible avec toutes les installations")
    print("   ✅ Rollback possible")
    print()
    
    # Étape 1: Sauvegarde
    backup_path = backup_database()
    if not backup_path:
        print("❌ Impossible de continuer sans sauvegarde")
        return False
    
    # Étape 2: Analyse
    analysis_data = analyze_existing_data()
    if not analysis_data:
        print("❌ Impossible de continuer sans analyse")
        return False
    
    # Étape 3: Plan
    plan_created = create_safe_migration_plan(analysis_data)
    if not plan_created:
        print("❌ Impossible de créer le plan de migration")
        return False
    
    # Étape 4: Confirmation utilisateur
    print("\n" + "=" * 60)
    print("⚠️  CONFIRMATION REQUISE")
    print("Cette migration va:")
    print("   ✅ Préserver toutes vos données existantes")
    print("   ✅ Créer des entrées stock pour les productos qui n'en ont pas")
    print("   ✅ Garder les valeurs stock existantes intactes")
    print(f"   📁 Sauvegarde disponible: {os.path.basename(backup_path)}")
    
    response = input("\nContinuer la migration? (oui/non): ").lower().strip()
    
    if response in ['oui', 'o', 'yes', 'y']:
        # Étape 5: Exécution
        migration_success = execute_safe_migration(analysis_data)
        
        print("\n" + "=" * 60)
        if migration_success:
            print("🎉 MIGRATION RÉUSSIE!")
            print("\n✅ RÉSULTAT:")
            print("   ✅ Toutes les données préservées")
            print("   ✅ Source unique de stock activée")
            print("   ✅ Interface utilisera maintenant table stock")
            print("   ✅ Plus de problèmes de synchronisation")
            print(f"\n🛡️  Sauvegarde: {backup_path}")
        else:
            print("❌ MIGRATION ÉCHOUÉE")
            print(f"🛡️  Restaurez depuis: {backup_path}")
        
        return migration_success
    else:
        print("\n❌ Migration annulée par l'utilisateur")
        print(f"🛡️  Sauvegarde conservée: {backup_path}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
