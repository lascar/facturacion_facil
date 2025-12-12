#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug pour vérifier les données des clients
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.test_database import get_test_database, cleanup_test_database
from utils.logger import get_logger

def debug_client_data():
    """Debug des données clients"""
    logger = get_logger("DebugClientData")
    
    try:
        # Utiliser la base de test
        test_db = get_test_database()
        logger.info("🛡️ Utilisation de la base de données de TEST")
        
        # Vérifier tous les clients
        all_clients = test_db.get_all_clients()
        logger.info(f"📊 Nombre total de clients: {len(all_clients)}")
        
        for i, client in enumerate(all_clients):
            logger.info(f"📋 Client {i+1}:")
            logger.info(f"   ID: {client.get('id', 'N/A')}")
            logger.info(f"   Nom: '{client.get('nombre', '')}'")
            logger.info(f"   NIF: '{client.get('nif', '')}'")
            logger.info(f"   Téléphone: '{client.get('telefono', '')}'")
            logger.info(f"   Email: '{client.get('email', '')}'")
            logger.info(f"   Adresse: '{client.get('direccion', '')}'")
            logger.info(f"   Date création: {client.get('fecha_creacion', 'N/A')}")
            
            # Tester get_client_by_id
            if client.get('id'):
                full_client = test_db.get_client_by_id(client['id'])
                if full_client:
                    logger.info(f"🔍 Données complètes via get_client_by_id({client['id']}):")
                    logger.info(f"   ID: {full_client.get('id', 'N/A')}")
                    logger.info(f"   Nom: '{full_client.get('nombre', '')}'")
                    logger.info(f"   NIF: '{full_client.get('nif', '')}'")
                    logger.info(f"   Téléphone: '{full_client.get('telefono', '')}'")
                    logger.info(f"   Email: '{full_client.get('email', '')}'")
                    logger.info(f"   Adresse: '{full_client.get('direccion', '')}'")
                    logger.info(f"   Date création: {full_client.get('fecha_creacion', 'N/A')}")
                    
                    # Comparer les données
                    if (full_client.get('telefono', '') == client.get('telefono', '') and
                        full_client.get('email', '') == client.get('email', '') and
                        full_client.get('direccion', '') == client.get('direccion', '')):
                        logger.info("✅ Données cohérentes")
                    else:
                        logger.warning("⚠️ Données incohérentes!")
                        logger.warning(f"   get_all_clients téléphone: '{client.get('telefono', '')}'")
                        logger.warning(f"   get_client_by_id téléphone: '{full_client.get('telefono', '')}'")
                        logger.warning(f"   get_all_clients email: '{client.get('email', '')}'")
                        logger.warning(f"   get_client_by_id email: '{full_client.get('email', '')}'")
                        logger.warning(f"   get_all_clients adresse: '{client.get('direccion', '')}'")
                        logger.warning(f"   get_client_by_id adresse: '{full_client.get('direccion', '')}'")
                else:
                    logger.error(f"❌ get_client_by_id({client['id']}) a retourné None")
            
            logger.info("")
        
        # Vérifier la structure de la table
        logger.info("🔍 Vérification de la structure de la table clients:")
        conn = test_db.get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(clientes)")
        columns = cursor.fetchall()
        
        for col in columns:
            logger.info(f"   Colonne: {col[1]} ({col[2]}) - Nullable: {not col[3]}")
        
        # Vérifier les données brutes
        logger.info("🔍 Données brutes de la table clients:")
        cursor.execute("SELECT * FROM clientes")
        rows = cursor.fetchall()
        
        for i, row in enumerate(rows):
            logger.info(f"   Ligne {i+1}: {row}")
        
        conn.close()
        
        # Nettoyer
        cleanup_test_database()
        logger.info("🧹 Base de données de test nettoyée")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du debug: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Nettoyer en cas d'erreur
        cleanup_test_database()
        return 1

if __name__ == "__main__":
    print("🔍 Debug des Données Clients")
    print("=" * 40)
    print("🔒 IMPORTANT: Ce test utilise une base de données de TEST")
    print("✅ Aucun impact sur la base de données de production")
    print()
    
    exit_code = debug_client_data()
    
    if exit_code == 0:
        print()
        print("✅ Debug terminé avec succès!")
    else:
        print()
        print("❌ Debug échoué")
    
    sys.exit(exit_code)
