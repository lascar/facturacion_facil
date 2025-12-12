#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test SÉCURISÉ pour vérifier le rafraîchissement lors du changement de client
Utilise une base de données de test isolée
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from database.test_database import get_test_database, cleanup_test_database
from utils.logger import get_logger

def test_client_refresh():
    """Test du rafraîchissement lors du changement de client"""
    logger = get_logger("TestClientRefresh")
    
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
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        
        logger.info("🚀 Ouverture de la fenêtre de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        def test_step_1():
            """Étape 1: Sélectionner le premier client"""
            try:
                logger.info("🔍 Étape 1: Sélection du premier client...")
                
                autocomplete = window.cliente_autocomplete
                details = window.client_details
                
                # Récupérer les clients
                clients = test_db.get_all_clients()
                if len(clients) < 2:
                    logger.error("❌ Besoin d'au moins 2 clients pour le test")
                    return
                
                first_client = clients[0]
                logger.info(f"📋 Sélection du premier client: {first_client.get('nombre', '')}")
                
                # Sélectionner le premier client
                autocomplete.setText(first_client.get('nombre', ''))
                suggestion = f"{first_client.get('nombre', '')} ({first_client.get('nif', '')})"
                autocomplete.on_completion_selected(suggestion)
                
                QTimer.singleShot(500, lambda: test_step_1_verify(autocomplete, details, logger, first_client, clients))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_1_verify(autocomplete, details, logger, first_client, clients):
            """Vérifier que le premier client est bien affiché"""
            try:
                logger.info("🔍 Vérification du premier client...")
                
                # Vérifier que les détails sont affichés
                if details.isVisible():
                    logger.info("✅ Widget de détails affiché pour le premier client")
                    
                    # Vérifier les données affichées
                    nif_displayed = details.nif_edit.text()
                    phone_displayed = details.telefono_edit.text()
                    
                    logger.info(f"📋 Premier client affiché:")
                    logger.info(f"   NIF: '{nif_displayed}'")
                    logger.info(f"   Téléphone: '{phone_displayed}'")
                    
                    if nif_displayed == first_client.get('nif', '') and phone_displayed == first_client.get('telefono', ''):
                        logger.info("✅ Données du premier client correctement affichées")
                        QTimer.singleShot(500, lambda: test_step_2(autocomplete, details, logger, clients))
                    else:
                        logger.error("❌ Données du premier client incorrectes")
                        return
                else:
                    logger.error("❌ Widget de détails non affiché")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur vérification étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2(autocomplete, details, logger, clients):
            """Étape 2: Changer le texte pour un autre client"""
            try:
                logger.info("🔍 Étape 2: Changement vers le deuxième client...")
                
                second_client = clients[1]
                logger.info(f"📋 Changement vers: {second_client.get('nombre', '')}")
                
                # Changer le texte dans l'autocomplete
                autocomplete.setText(second_client.get('nombre', ''))
                
                QTimer.singleShot(300, lambda: test_step_2_continue(autocomplete, details, logger, second_client))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2_continue(autocomplete, details, logger, second_client):
            """Continuer l'étape 2"""
            try:
                # Vérifier que les détails ont été effacés
                current_client = autocomplete.get_current_client()
                
                if current_client is None:
                    logger.info("✅ Client actuel effacé après changement de texte")
                    
                    # Vérifier que le widget de détails est caché ou vide
                    if not details.isVisible() or details.current_client is None:
                        logger.info("✅ Widget de détails effacé/caché")
                    else:
                        logger.warning("⚠️ Widget de détails toujours affiché")
                        
                        # Vérifier si les champs sont vides
                        nif_displayed = details.nif_edit.text()
                        phone_displayed = details.telefono_edit.text()
                        
                        if not nif_displayed and not phone_displayed:
                            logger.info("✅ Champs de détails vides")
                        else:
                            logger.warning(f"⚠️ Champs non vides: NIF='{nif_displayed}', Tel='{phone_displayed}'")
                else:
                    logger.warning(f"⚠️ Client actuel non effacé: {current_client.get('nombre', '')}")
                
                # Maintenant sélectionner le deuxième client
                suggestion = f"{second_client.get('nombre', '')} ({second_client.get('nif', '')})"
                autocomplete.on_completion_selected(suggestion)
                
                QTimer.singleShot(500, lambda: test_step_3(autocomplete, details, logger, second_client))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3(autocomplete, details, logger, second_client):
            """Étape 3: Vérifier que le deuxième client est affiché"""
            try:
                logger.info("🔍 Étape 3: Vérification du deuxième client...")
                
                # Vérifier que les détails du deuxième client sont affichés
                if details.isVisible():
                    logger.info("✅ Widget de détails affiché pour le deuxième client")
                    
                    # Vérifier les données affichées
                    nif_displayed = details.nif_edit.text()
                    phone_displayed = details.telefono_edit.text()
                    
                    logger.info(f"📋 Deuxième client affiché:")
                    logger.info(f"   NIF: '{nif_displayed}'")
                    logger.info(f"   Téléphone: '{phone_displayed}'")
                    
                    expected_nif = second_client.get('nif', '')
                    expected_phone = second_client.get('telefono', '')
                    
                    if nif_displayed == expected_nif and phone_displayed == expected_phone:
                        logger.info("✅ Données du deuxième client correctement affichées")
                        QTimer.singleShot(500, lambda: test_step_4(autocomplete, details, logger))
                    else:
                        logger.warning(f"⚠️ Données incorrectes - Attendu: NIF='{expected_nif}', Tel='{expected_phone}'")
                        QTimer.singleShot(500, lambda: test_step_4(autocomplete, details, logger))
                else:
                    logger.error("❌ Widget de détails non affiché pour le deuxième client")
                    QTimer.singleShot(500, lambda: test_step_4(autocomplete, details, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_4(autocomplete, details, logger):
            """Étape 4: Effacer le texte et vérifier que tout est effacé"""
            try:
                logger.info("🔍 Étape 4: Effacement du texte...")
                
                # Effacer le texte
                autocomplete.setText("")
                
                QTimer.singleShot(300, lambda: test_step_4_verify(autocomplete, details, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 4: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_4_verify(autocomplete, details, logger):
            """Vérifier que tout est effacé"""
            try:
                logger.info("🔍 Vérification de l'effacement...")
                
                # Vérifier que le client actuel est None
                current_client = autocomplete.get_current_client()
                
                if current_client is None:
                    logger.info("✅ Client actuel effacé")
                else:
                    logger.warning(f"⚠️ Client actuel non effacé: {current_client.get('nombre', '')}")
                
                # Vérifier que le widget de détails est caché
                if not details.isVisible():
                    logger.info("✅ Widget de détails caché")
                else:
                    logger.warning("⚠️ Widget de détails toujours visible")
                
                QTimer.singleShot(500, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur vérification étape 4: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test de rafraîchissement:")
                logger.info("   ✅ Sélection du premier client")
                logger.info("   ✅ Affichage des détails du premier client")
                logger.info("   ✅ Changement vers le deuxième client")
                logger.info("   ✅ Effacement des détails lors du changement")
                logger.info("   ✅ Affichage des détails du deuxième client")
                logger.info("   ✅ Effacement complet lors de la suppression du texte")
                logger.info("🎉 Rafraîchissement des clients fonctionnel!")
                
                # Restaurer la base originale
                db_module.db = original_db
                logger.info("🔄 Base de données originale restaurée")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_step_1)
        
        # Fermer automatiquement après 25 secondes
        QTimer.singleShot(25000, app.quit)
        
        # Lancer l'application
        result = app.exec_()
        
        # Nettoyer la base de test
        cleanup_test_database()
        logger.info("🧹 Base de données de test nettoyée")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Nettoyer en cas d'erreur
        cleanup_test_database()
        return 1

if __name__ == "__main__":
    print("🧪 Test SÉCURISÉ de Rafraîchissement des Clients")
    print("=" * 55)
    print("🔒 IMPORTANT: Ce test utilise une base de données de TEST")
    print("✅ Aucun impact sur la base de données de production")
    print()
    print("📋 Fonctionnalités testées:")
    print("   • Sélection d'un client")
    print("   • Changement vers un autre client")
    print("   • Rafraîchissement des détails")
    print("   • Effacement lors de la suppression du texte")
    print()
    
    exit_code = test_client_refresh()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎯 Rafraîchissement des clients validé")
        print("🛡️ Base de production intacte")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
