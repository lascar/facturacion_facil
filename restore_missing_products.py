#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de restauration des produits et stocks manquants
Restaure les produits référencés dans les factures existantes
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import db
from utils.logger import get_logger

logger = get_logger("restore_products")

def get_missing_product_ids():
    """Obtient les IDs de produits référencés dans les factures mais manquants dans la table productos"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Obtenir les IDs de produits référencés dans les factures
        cursor.execute("""
            SELECT DISTINCT fi.producto_id 
            FROM factura_items fi 
            WHERE fi.producto_id IS NOT NULL
        """)
        referenced_ids = [row[0] for row in cursor.fetchall()]
        
        # Obtenir les IDs de produits existants
        cursor.execute("SELECT id FROM productos")
        existing_ids = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        # Trouver les IDs manquants
        missing_ids = [pid for pid in referenced_ids if pid not in existing_ids]
        
        return referenced_ids, existing_ids, missing_ids
        
    except Exception as e:
        logger.error(f"Error obteniendo IDs de productos: {e}")
        return [], [], []

def create_missing_products(missing_ids):
    """Crée les produits manquants avec des données par défaut"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        created_count = 0
        
        for product_id in missing_ids:
            # Créer un produit avec des données par défaut
            cursor.execute("""
                INSERT INTO productos (id, nombre, referencia, precio, categoria, descripcion, 
                                     imagen_path, iva_recomendado, stock_actual, stock_minimo, fecha_creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_id,
                f"Producto Restaurado {product_id}",
                f"REST-{product_id:03d}",
                25.0,  # Precio por defecto
                "Restaurados",
                f"Producto restaurado automáticamente (ID: {product_id})",
                "",  # Sin imagen
                21.0,  # IVA por defecto
                50,  # Stock inicial
                5,   # Stock mínimo
                datetime.now().isoformat()
            ))
            
            # Crear entrada en stock
            cursor.execute("""
                INSERT OR REPLACE INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                VALUES (?, ?, ?)
            """, (product_id, 50, datetime.now().isoformat()))
            
            created_count += 1
            logger.info(f"Producto {product_id} restaurado")
        
        conn.commit()
        conn.close()
        
        return created_count
        
    except Exception as e:
        logger.error(f"Error creando productos: {e}")
        return 0

def verify_data_integrity():
    """Vérifie l'intégrité des données après restauration"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Vérifier que tous les produits référencés existent
        cursor.execute("""
            SELECT fi.producto_id, COUNT(*) as count
            FROM factura_items fi
            LEFT JOIN productos p ON fi.producto_id = p.id
            WHERE p.id IS NULL
            GROUP BY fi.producto_id
        """)
        
        orphaned_references = cursor.fetchall()
        
        if orphaned_references:
            logger.warning(f"Références orphelines trouvées: {orphaned_references}")
            return False
        
        # Vérifier que tous les produits ont un stock
        cursor.execute("""
            SELECT p.id, p.nombre
            FROM productos p
            LEFT JOIN stock s ON p.id = s.producto_id
            WHERE s.producto_id IS NULL
        """)
        
        products_without_stock = cursor.fetchall()
        
        if products_without_stock:
            logger.warning(f"Produits sans stock: {products_without_stock}")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error verificando integridad: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 RESTAURATION DES PRODUITS ET STOCKS MANQUANTS")
    print("=" * 60)

    # Analyser la situation
    print("\n1️⃣ Analyse de la situation...")
    referenced_ids, existing_ids, missing_ids = get_missing_product_ids()

    print(f"   📊 Produits référencés dans les factures: {len(referenced_ids)}")
    print(f"   ✅ Produits existants: {len(existing_ids)}")
    print(f"   ❌ Produits manquants: {len(missing_ids)}")

    if referenced_ids:
        print(f"   🔍 IDs référencés: {sorted(referenced_ids)}")
    if existing_ids:
        print(f"   ✅ IDs existants: {sorted(existing_ids)}")
    if missing_ids:
        print(f"   ❌ IDs manquants: {sorted(missing_ids)}")

    if not missing_ids:
        print("\n✅ Aucun produit manquant détecté!")
        return True

    # Restauration automatique (pas de confirmation interactive)
    print(f"\n⚠️  {len(missing_ids)} produits manquants détectés.")
    print("🔄 Restauration automatique en cours...")
    
    # Restaurer les produits
    print("\n2️⃣ Restauration des produits...")
    created_count = create_missing_products(missing_ids)
    print(f"   ✅ {created_count} produits restaurés")
    
    # Vérifier l'intégrité
    print("\n3️⃣ Vérification de l'intégrité...")
    if verify_data_integrity():
        print("   ✅ Intégrité des données vérifiée")
    else:
        print("   ⚠️  Problèmes d'intégrité détectés (voir logs)")
    
    print("\n🎉 Restauration terminée!")
    print("\n💡 Conseil: Utilise l'option 6 du script clean_databases.sh")
    print("   pour créer une base propre à l'avenir.")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
        print(f"\n❌ Erreur critique: {e}")
        sys.exit(1)
