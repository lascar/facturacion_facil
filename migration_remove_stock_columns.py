#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migration pour supprimer les colonnes stock de la table productos
et ne conserver que la table stock dédiée.

⚠️ ATTENTION : Ce script modifie la structure de la base de données !
- Crée automatiquement une sauvegarde avant migration
- Migre les données stock_actual vers la table stock
- Supprime les colonnes stock_actual et stock_minimo de productos
"""

import sys
import os
from datetime import datetime

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.migration_manager import MigrationManager
from utils.logger import get_logger

def main():
    """Fonction principale de migration"""
    logger = get_logger(__name__)
    
    print("=" * 60)
    print("🔄 MIGRATION: Suppression colonnes stock de productos")
    print("=" * 60)
    print()
    
    # Chemin de la base de données de production
    db_path = "base_de_datos/facturacion.db"
    
    # Vérifier que la base existe
    if not os.path.exists(db_path):
        print(f"❌ Erreur: Base de données {db_path} non trouvée")
        print("   Assurez-vous d'être dans le bon répertoire")
        return False
    
    print(f"📁 Base de données: {db_path}")
    print(f"📊 Taille actuelle: {os.path.getsize(db_path)} bytes")
    print()
    
    # Demander confirmation
    print("⚠️  ATTENTION: Cette migration va:")
    print("   1. Créer une sauvegarde automatique")
    print("   2. Migrer les données stock_actual vers la table stock")
    print("   3. Supprimer les colonnes stock_actual et stock_minimo de productos")
    print("   4. Conserver uniquement la table stock pour la gestion des stocks")
    print()
    
    confirmation = input("Voulez-vous continuer ? (oui/non): ").lower().strip()
    if confirmation not in ['oui', 'o', 'yes', 'y']:
        print("❌ Migration annulée par l'utilisateur")
        return False
    
    print()
    print("🚀 Début de la migration...")
    
    try:
        # Créer le gestionnaire de migration
        migration_manager = MigrationManager(db_path)
        
        # Exécuter la migration
        success = migration_manager.remove_stock_columns_from_productos()
        
        if success:
            print()
            print("✅ Migration terminée avec succès !")
            print()
            print("📋 Résumé des changements:")
            print("   • Colonnes stock_actual et stock_minimo supprimées de productos")
            print("   • Données migrées vers la table stock")
            print("   • Sauvegarde créée dans base_de_datos/backups/")
            print()
            print("🔍 Vérifications recommandées:")
            print("   • Tester l'application pour s'assurer que tout fonctionne")
            print("   • Vérifier que les stocks s'affichent correctement")
            print("   • Contrôler les fonctionnalités de mise à jour de stock")
            print()
            return True
        else:
            print()
            print("❌ Erreur durant la migration")
            print("   Consultez les logs pour plus de détails")
            print("   La base de données n'a pas été modifiée")
            return False
            
    except Exception as e:
        logger.error(f"Erreur critique durant la migration: {e}")
        print(f"❌ Erreur critique: {e}")
        print("   La migration a été interrompue")
        return False

if __name__ == "__main__":
    print(f"🕒 Démarrage: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = main()
    
    print()
    print(f"🕒 Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("🎉 Migration réussie !")
        sys.exit(0)
    else:
        print("💥 Migration échouée !")
        sys.exit(1)
