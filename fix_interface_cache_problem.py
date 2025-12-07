#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour diagnostiquer et corriger le problème de cache dans l'interface
"""

import sqlite3
from database.database_improved import DatabaseImproved

def diagnose_cache_problem():
    """Diagnostique le problème de cache dans l'interface"""
    print("🔍 DIAGNOSTIC DU PROBLÈME DE CACHE")
    print("=" * 40)
    
    # Vérifier la base de données directement
    print("\n1️⃣ Vérification directe de la base de données:")
    try:
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        
        # Compter les produits
        cursor.execute("SELECT COUNT(*) FROM productos")
        db_count = cursor.fetchone()[0]
        print(f"   📊 Produits dans la base: {db_count}")
        
        # Lister les produits s'il y en a
        if db_count > 0:
            cursor.execute("SELECT id, nombre FROM productos LIMIT 5")
            products = cursor.fetchall()
            print("   📝 Premiers produits:")
            for product in products:
                print(f"      - {product[0]}: {product[1]}")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
        return False
    
    # Vérifier via DatabaseImproved
    print("\n2️⃣ Vérification via DatabaseImproved:")
    try:
        db = DatabaseImproved()
        products = db.get_all_products()
        print(f"   📊 Produits via DatabaseImproved: {len(products)}")
        
        if products:
            print("   📝 Premiers produits:")
            for product in products[:5]:
                print(f"      - {product.get('id')}: {product.get('nombre')}")
        
    except Exception as e:
        print(f"   ❌ Erreur DatabaseImproved: {e}")
        return False
    
    # Diagnostic du problème
    print("\n3️⃣ Diagnostic:")
    if db_count == 0 and len(products) == 0:
        print("   ✅ Pas de problème: Base de données et interface cohérentes")
        print("   💡 Si tu vois encore des produits, c'est un problème de cache d'interface")
        return True
    elif db_count != len(products):
        print(f"   ⚠️ Incohérence détectée:")
        print(f"      Base directe: {db_count} produits")
        print(f"      DatabaseImproved: {len(products)} produits")
        return False
    else:
        print(f"   ✅ Cohérence: {db_count} produits dans les deux sources")
        return True

def force_interface_refresh():
    """Force le rafraîchissement de l'interface"""
    print("\n🔄 SOLUTION: RAFRAÎCHISSEMENT FORCÉ")
    print("=" * 40)
    
    print("Pour résoudre le problème de cache d'interface:")
    print("1. 🔄 Ferme complètement l'application")
    print("2. 🚀 Relance l'application")
    print("3. 📋 Ouvre la fenêtre des produits")
    print("4. ✅ Les produits devraient maintenant être vides")
    
    print("\nOu si l'application est ouverte:")
    print("1. 📋 Va dans la fenêtre des produits")
    print("2. 🔄 Clique sur le bouton 'Actualizar' ou 'Refresh'")
    print("3. ✅ La liste devrait se vider")

def create_interface_refresh_signal():
    """Crée un signal pour forcer le rafraîchissement de toutes les interfaces"""
    print("\n📡 CRÉATION D'UN SIGNAL DE RAFRAÎCHISSEMENT")
    print("=" * 45)
    
    try:
        # Importer le gestionnaire d'événements
        from utils.event_manager_pyqt5 import event_manager_pyqt5
        
        print("   📡 Émission du signal de rafraîchissement global...")
        
        # Émettre un signal pour forcer le rafraîchissement
        # Note: Ceci ne fonctionnera que si l'interface est ouverte
        try:
            # Simuler la suppression de tous les produits pour forcer le refresh
            for i in range(100):  # Supposer max 100 produits
                event_manager_pyqt5.emit_product_deleted(i)
            
            print("   ✅ Signaux de suppression émis")
            print("   💡 Si l'interface est ouverte, elle devrait se rafraîchir")
            
        except Exception as e:
            print(f"   ⚠️ Impossible d'émettre les signaux: {e}")
            print("   💡 L'interface n'est probablement pas ouverte")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Impossible d'importer le gestionnaire d'événements: {e}")
        return False

def verify_cleanup_function():
    """Vérifie que la fonction de nettoyage fonctionne correctement"""
    print("\n🧹 VÉRIFICATION DE LA FONCTION DE NETTOYAGE")
    print("=" * 45)
    
    try:
        # Vérifier que la fonction de nettoyage a bien fonctionné
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        
        # Vérifier toutes les tables
        tables_to_check = ['productos', 'facturas', 'clientes', 'stock', 'factura_items', 'stock_movements']
        
        print("   📊 État des tables après nettoyage:")
        all_empty = True
        
        for table in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                status = "✅ Vide" if count == 0 else f"⚠️ {count} enregistrements"
                print(f"      {table}: {status}")
                
                if count > 0:
                    all_empty = False
                    
            except Exception as e:
                print(f"      {table}: ❌ Erreur - {e}")
        
        conn.close()
        
        if all_empty:
            print("\n   🎉 NETTOYAGE RÉUSSI: Toutes les tables sont vides")
            print("   💡 Le problème est uniquement dans le cache de l'interface")
        else:
            print("\n   ⚠️ NETTOYAGE PARTIEL: Certaines tables contiennent encore des données")
        
        return all_empty
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC ET CORRECTION DU PROBLÈME DE CACHE")
    print("=" * 50)
    
    # Étape 1: Diagnostic
    diagnosis_ok = diagnose_cache_problem()
    
    # Étape 2: Vérification du nettoyage
    cleanup_ok = verify_cleanup_function()
    
    # Étape 3: Solution
    if diagnosis_ok and cleanup_ok:
        print("\n🎯 CONCLUSION:")
        print("   ✅ La base de données est correctement nettoyée")
        print("   ⚠️ Le problème est dans le cache de l'interface utilisateur")
        print("\n🔧 SOLUTIONS:")
        print("   1. Fermer et relancer l'application")
        print("   2. Utiliser le bouton 'Actualizar' dans l'interface des produits")
        print("   3. Forcer le rafraîchissement via les signaux")
        
        # Tenter le rafraîchissement automatique
        create_interface_refresh_signal()
        force_interface_refresh()
        
    else:
        print("\n⚠️ PROBLÈME DÉTECTÉ:")
        print("   Le nettoyage n'a pas fonctionné correctement")
        print("   Il faut investiguer plus en profondeur")
    
    return diagnosis_ok and cleanup_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
