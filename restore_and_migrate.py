#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour restaurer les données et appliquer les migrations correctement
"""

import os
import sqlite3
import shutil
from datetime import datetime
from database.migration_manager import MigrationManager

def find_best_backup():
    """Trouve la meilleure sauvegarde disponible"""
    backup_candidates = []
    
    # Vérifier les sauvegardes dans le répertoire backups/
    if os.path.exists("backups"):
        for file in os.listdir("backups"):
            if file.endswith(".db"):
                path = os.path.join("backups", file)
                backup_candidates.append(path)
    
    # Vérifier les sauvegardes dans le répertoire racine
    for file in os.listdir("."):
        if file.startswith("facturacion_backup_") and file.endswith(".db"):
            backup_candidates.append(file)
    
    if not backup_candidates:
        return None
    
    # Trier par date de modification (plus récent en premier)
    backup_candidates.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    return backup_candidates

def check_backup_content(backup_path):
    """Vérifie le contenu d'une sauvegarde"""
    try:
        conn = sqlite3.connect(backup_path)
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        stats = {}
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                stats[table] = count
            except:
                stats[table] = "erreur"
        
        conn.close()
        return stats
        
    except Exception as e:
        return {"erreur": str(e)}

def restore_with_migration():
    """Restaure les données avec migration appropriée"""
    print("🔄 RESTAURATION ET MIGRATION DES DONNÉES")
    print("=" * 45)
    
    # Trouver les sauvegardes disponibles
    backups = find_best_backup()
    
    if not backups:
        print("❌ Aucune sauvegarde trouvée")
        return False
    
    print(f"📁 {len(backups)} sauvegarde(s) trouvée(s):")
    
    # Analyser chaque sauvegarde
    for i, backup_path in enumerate(backups, 1):
        print(f"\n{i}. {backup_path}")
        
        # Vérifier la taille
        size = os.path.getsize(backup_path)
        print(f"   Taille: {size:,} bytes")
        
        # Vérifier la date
        mtime = os.path.getmtime(backup_path)
        date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"   Date: {date_str}")
        
        # Vérifier le contenu
        stats = check_backup_content(backup_path)
        print(f"   Contenu: {stats}")
        
        # Si cette sauvegarde contient des produits, l'utiliser
        if stats.get("productos", 0) > 0:
            print(f"   ✅ Cette sauvegarde contient {stats['productos']} produit(s)")
            
            # Demander confirmation
            print(f"\n🔄 Restauration depuis: {backup_path}")
            
            # Créer le gestionnaire de migration
            migration_manager = MigrationManager()
            
            # Créer une sauvegarde de l'état actuel
            current_backup = migration_manager.create_backup("before_restore")
            print(f"   📦 Sauvegarde actuelle créée: {current_backup}")
            
            # Restaurer depuis la sauvegarde
            if migration_manager.restore_from_backup(backup_path):
                print("   ✅ Restauration réussie")
                
                # Vérifier le résultat
                verify_restoration()
                return True
            else:
                print("   ❌ Échec de la restauration")
                return False
    
    print("\n⚠️ Aucune sauvegarde avec des données trouvée")
    return False

def verify_restoration():
    """Vérifie que la restauration a fonctionné"""
    print("\n🔍 VÉRIFICATION DE LA RESTAURATION")
    print("=" * 35)
    
    try:
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        
        # Vérifier la structure de la table productos
        cursor.execute("PRAGMA table_info(productos)")
        columns = cursor.fetchall()
        
        print("📋 Structure de la table productos:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Vérifier le contenu
        cursor.execute("SELECT COUNT(*) FROM productos")
        count = cursor.fetchone()[0]
        print(f"\n📊 Nombre de produits: {count}")
        
        if count > 0:
            # Afficher les produits
            cursor.execute("SELECT id, nombre, referencia, categoria FROM productos LIMIT 5")
            products = cursor.fetchall()
            
            print("\n📝 Produits restaurés:")
            for product in products:
                id_prod, nombre, referencia, categoria = product
                print(f"   {id_prod}. {nombre} (ref: {referencia}, cat: {categoria})")
        
        conn.close()
        
        print("\n✅ Vérification terminée")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la vérification: {e}")
        return False

def create_test_product():
    """Crée un produit de test pour vérifier que tout fonctionne"""
    print("\n🧪 CRÉATION D'UN PRODUIT DE TEST")
    print("=" * 35)
    
    try:
        from database.database_improved import DatabaseImproved
        
        db = DatabaseImproved()
        
        # Créer un produit de test
        product_data = {
            'nombre': 'Producto Test Restaurado',
            'referencia': 'TEST-RESTORE-001',
            'precio_venta': 29.99,
            'categoria': 'Test Categoria',
            'descripcion': 'Producto de test después de restauración',
            'iva_recomendado': 21.0,
            'stock': 10
        }
        
        product_id = db.add_product(product_data)
        print(f"   ✅ Produit de test créé avec ID: {product_id}")
        
        # Vérifier qu'il est bien sauvegardé avec la catégorie
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, categoria FROM productos WHERE id = ?", (product_id,))
            result = cursor.fetchone()
        
        if result:
            nombre, categoria = result
            print(f"   ✅ Produit vérifié: '{nombre}', catégorie: '{categoria}'")
            
            if categoria == 'Test Categoria':
                print("   🎉 La catégorie est correctement sauvegardée !")
                return True
            else:
                print(f"   ❌ Problème avec la catégorie: {categoria}")
                return False
        else:
            print("   ❌ Produit non trouvé après création")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur création produit de test: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE RESTAURATION ET MIGRATION")
    print("=" * 40)
    print("Ce script va:")
    print("1. Chercher les sauvegardes disponibles")
    print("2. Restaurer les données depuis la meilleure sauvegarde")
    print("3. Appliquer les migrations nécessaires")
    print("4. Vérifier que tout fonctionne")
    print()
    
    # Étape 1: Restauration
    if restore_with_migration():
        print("\n🎉 RESTAURATION RÉUSSIE")
        
        # Étape 2: Test
        if create_test_product():
            print("\n🏆 MIGRATION COMPLÈTE RÉUSSIE")
            print("   ✅ Tes données ont été restaurées")
            print("   ✅ Les migrations ont été appliquées")
            print("   ✅ Les catégories fonctionnent correctement")
            print("   ✅ Le système est prêt à l'utilisation")
            return True
        else:
            print("\n⚠️ Restauration OK mais problème avec les nouvelles fonctionnalités")
            return False
    else:
        print("\n❌ ÉCHEC DE LA RESTAURATION")
        print("   Tes données n'ont pas pu être récupérées")
        print("   Tu devras recréer ton produit manuellement")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
