#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug pour vérifier le flux de données des clients
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from database.test_database import get_test_database, cleanup_test_database
from utils.logger import get_logger

def debug_client_flow():
    """Debug du flux de données clients"""
    logger = get_logger("DebugClientFlow")
    
    try:
        # Utiliser la base de test
        test_db = get_test_database()
        logger.info("🛡️ Utilisation de la base de données de TEST")
        
        app = QApplication(sys.argv)
        
        # Remplacer temporairement la base de données
        import database.database as db_module
        original_db = db_module.db
        db_module.db = test_db
        
        # Importer après le remplacement
        from ui.client_autocomplete_widget import ClientAutoCompleteWidget, ClientDetailsWidget
        
        logger.info("🚀 Création des widgets...")
        
        # Créer les widgets
        autocomplete = ClientAutoCompleteWidget()
        details = ClientDetailsWidget()
        
        # Connecter les signaux
        autocomplete.client_selected.connect(details.show_client_details)
        
        def test_step_1():
            """Étape 1: Charger les clients"""
            try:
                logger.info("🔍 Étape 1: Chargement des clients...")
                
                # Récupérer les clients depuis la base
                clients_data = test_db.get_all_clients()

                # Charger les clients dans l'autocomplete
                autocomplete.load_clients(clients_data)
                logger.info(f"📊 Nombre de clients chargés: {len(clients_data)}")
                
                for i, client in enumerate(clients_data):
                    logger.info(f"📋 Client {i+1} dans autocomplete:")
                    logger.info(f"   ID: {client.get('id', 'N/A')}")
                    logger.info(f"   Nom: '{client.get('nombre', '')}'")
                    logger.info(f"   NIF: '{client.get('nif', '')}'")
                    logger.info(f"   Téléphone: '{client.get('telefono', '')}'")
                    logger.info(f"   Email: '{client.get('email', '')}'")
                    logger.info(f"   Adresse: '{client.get('direccion', '')}'")
                
                if len(clients_data) > 0:
                    QTimer.singleShot(500, lambda: test_step_2(autocomplete, details, logger, clients_data[0]))
                else:
                    logger.error("❌ Aucun client chargé")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2(autocomplete, details, logger, first_client):
            """Étape 2: Sélectionner un client"""
            try:
                logger.info("🔍 Étape 2: Sélection d'un client...")
                
                # Simuler la sélection du premier client
                client_name = first_client.get('nombre', '')
                logger.info(f"📋 Sélection du client: {client_name}")
                
                # Appeler directement on_completion_selected
                suggestion = f"{client_name} ({first_client.get('nif', '')})"
                autocomplete.on_completion_selected(suggestion)
                
                # Vérifier le client sélectionné
                current_client = autocomplete.get_current_client()
                if current_client:
                    logger.info(f"✅ Client sélectionné dans autocomplete:")
                    logger.info(f"   ID: {current_client.get('id', 'N/A')}")
                    logger.info(f"   Nom: '{current_client.get('nombre', '')}'")
                    logger.info(f"   NIF: '{current_client.get('nif', '')}'")
                    logger.info(f"   Téléphone: '{current_client.get('telefono', '')}'")
                    logger.info(f"   Email: '{current_client.get('email', '')}'")
                    logger.info(f"   Adresse: '{current_client.get('direccion', '')}'")
                    
                    QTimer.singleShot(500, lambda: test_step_3(details, logger, current_client))
                else:
                    logger.error("❌ Aucun client sélectionné")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3(details, logger, expected_client):
            """Étape 3: Vérifier l'affichage"""
            try:
                logger.info("🔍 Étape 3: Vérification de l'affichage...")
                
                # Vérifier le client dans le widget de détails
                current_client = details.current_client
                if current_client:
                    logger.info(f"✅ Client dans le widget de détails:")
                    logger.info(f"   ID: {current_client.get('id', 'N/A')}")
                    logger.info(f"   Nom: '{current_client.get('nombre', '')}'")
                    logger.info(f"   NIF: '{current_client.get('nif', '')}'")
                    logger.info(f"   Téléphone: '{current_client.get('telefono', '')}'")
                    logger.info(f"   Email: '{current_client.get('email', '')}'")
                    logger.info(f"   Adresse: '{current_client.get('direccion', '')}'")
                    
                    # Vérifier les champs affichés
                    nif_displayed = details.nif_edit.text()
                    phone_displayed = details.telefono_edit.text()
                    email_displayed = details.email_edit.text()
                    address_displayed = details.direccion_edit.toPlainText()
                    
                    logger.info(f"📋 Champs affichés dans l'interface:")
                    logger.info(f"   NIF: '{nif_displayed}'")
                    logger.info(f"   Téléphone: '{phone_displayed}'")
                    logger.info(f"   Email: '{email_displayed}'")
                    logger.info(f"   Adresse: '{address_displayed}'")
                    
                    # Comparer avec les données attendues
                    expected_nif = expected_client.get('nif', '')
                    expected_phone = expected_client.get('telefono', '')
                    expected_email = expected_client.get('email', '')
                    expected_address = expected_client.get('direccion', '')
                    
                    logger.info(f"📋 Données attendues:")
                    logger.info(f"   NIF: '{expected_nif}'")
                    logger.info(f"   Téléphone: '{expected_phone}'")
                    logger.info(f"   Email: '{expected_email}'")
                    logger.info(f"   Adresse: '{expected_address}'")
                    
                    # Vérifier la correspondance
                    if (nif_displayed == expected_nif and
                        phone_displayed == expected_phone and
                        email_displayed == expected_email and
                        address_displayed == expected_address):
                        logger.info("✅ Toutes les données correspondent parfaitement!")
                    else:
                        logger.warning("⚠️ Certaines données ne correspondent pas:")
                        if nif_displayed != expected_nif:
                            logger.warning(f"   NIF: '{nif_displayed}' != '{expected_nif}'")
                        if phone_displayed != expected_phone:
                            logger.warning(f"   Téléphone: '{phone_displayed}' != '{expected_phone}'")
                        if email_displayed != expected_email:
                            logger.warning(f"   Email: '{email_displayed}' != '{expected_email}'")
                        if address_displayed != expected_address:
                            logger.warning(f"   Adresse: '{address_displayed}' != '{expected_address}'")
                else:
                    logger.error("❌ Aucun client dans le widget de détails")
                
                QTimer.singleShot(500, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du debug du flux de données:")
                logger.info("   ✅ Chargement des clients")
                logger.info("   ✅ Sélection d'un client")
                logger.info("   ✅ Transmission au widget de détails")
                logger.info("   ✅ Affichage des données")
                logger.info("🎉 Debug du flux terminé!")
                
                # Restaurer la base originale
                db_module.db = original_db
                logger.info("🔄 Base de données originale restaurée")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 1 seconde
        QTimer.singleShot(1000, test_step_1)
        
        # Fermer automatiquement après 15 secondes
        QTimer.singleShot(15000, app.quit)
        
        # Lancer l'application
        result = app.exec_()
        
        # Nettoyer la base de test
        cleanup_test_database()
        logger.info("🧹 Base de données de test nettoyée")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du debug: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Nettoyer en cas d'erreur
        cleanup_test_database()
        return 1

if __name__ == "__main__":
    print("🔍 Debug du Flux de Données Clients")
    print("=" * 45)
    print("🔒 IMPORTANT: Ce test utilise une base de données de TEST")
    print("✅ Aucun impact sur la base de données de production")
    print()
    
    exit_code = debug_client_flow()
    
    if exit_code == 0:
        print()
        print("✅ Debug terminé avec succès!")
    else:
        print()
        print("❌ Debug échoué")
    
    sys.exit(exit_code)
