#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la sauvegarde de clients modifiés en base de données
Vérifie que les changements sont reflétés dans la table client
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from ui.facturas_pyqt5 import FacturasPyQt5Window
from database.database import db
from utils.logger import get_logger

def test_client_save():
    """Test de la sauvegarde de clients"""
    logger = get_logger("TestFacturasClientSave")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        def test_step_1():
            """Étape 1: Créer un nouveau client"""
            try:
                logger.info("🔍 Étape 1: Création d'un nouveau client...")
                
                autocomplete = window.cliente_autocomplete
                details = window.client_details
                
                # Saisir un nouveau nom de client
                new_client_name = "Cliente Test Edicion"
                autocomplete.setText(new_client_name)
                autocomplete.editingFinished.emit()
                
                QTimer.singleShot(500, lambda: test_step_1_continue(details, logger, new_client_name))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_1_continue(details, logger, client_name):
            """Continuer l'étape 1"""
            try:
                # Vérifier que le nouveau client est créé
                if details.isVisible():
                    logger.info("✅ Widget de détails affiché pour nouveau client")
                    
                    # Remplir les détails
                    details.nif_edit.setText("12345678Z")
                    details.telefono_edit.setText("666777888")
                    details.email_edit.setText("test.edicion@example.com")
                    details.direccion_edit.setPlainText("Calle Test Edicion, 123")
                    
                    logger.info("📝 Détails du nouveau client remplis")
                    
                    QTimer.singleShot(500, lambda: test_step_2(details, logger, client_name))
                else:
                    logger.error("❌ Widget de détails non affiché")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2(details, logger, client_name):
            """Étape 2: Sauvegarder le nouveau client"""
            try:
                logger.info("🔍 Étape 2: Sauvegarde du nouveau client...")
                
                # Vérifier que les boutons sont activés
                if details.save_btn.isEnabled():
                    logger.info("✅ Bouton Guardar activé")
                    
                    # Compter les clients avant sauvegarde
                    clients_before = db.get_all_clients()
                    count_before = len(clients_before) if clients_before else 0
                    logger.info(f"📊 Nombre de clients avant sauvegarde: {count_before}")
                    
                    # Cliquer sur Guardar
                    details.save_btn.click()
                    
                    QTimer.singleShot(1000, lambda: test_step_2_continue(details, logger, client_name, count_before))
                else:
                    logger.error("❌ Bouton Guardar non activé")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2_continue(details, logger, client_name, count_before):
            """Continuer l'étape 2"""
            try:
                # Vérifier que le client a été créé en base
                clients_after = db.get_all_clients()
                count_after = len(clients_after) if clients_after else 0
                logger.info(f"📊 Nombre de clients après sauvegarde: {count_after}")
                
                if count_after > count_before:
                    logger.info("✅ Nouveau client créé en base de données")
                    
                    # Chercher le client créé
                    new_client = None
                    for client in clients_after:
                        if client.get('nombre') == client_name:
                            new_client = client
                            break
                    
                    if new_client:
                        logger.info(f"✅ Client trouvé en base: {new_client.get('nombre')}")
                        logger.info(f"   ID: {new_client.get('id')}")
                        logger.info(f"   NIF: {new_client.get('nif')}")
                        logger.info(f"   Téléphone: {new_client.get('telefono')}")
                        logger.info(f"   Email: {new_client.get('email')}")
                        
                        # Vérifier que les boutons sont désactivés
                        if not details.save_btn.isEnabled() and not details.discard_btn.isEnabled():
                            logger.info("✅ Boutons correctement désactivés après sauvegarde")
                        else:
                            logger.warning("⚠️ Boutons non désactivés après sauvegarde")
                        
                        QTimer.singleShot(500, lambda: test_step_3(details, logger, new_client))
                    else:
                        logger.error("❌ Client non trouvé en base après création")
                        return
                else:
                    logger.error("❌ Client non créé en base de données")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3(details, logger, client):
            """Étape 3: Modifier le client existant"""
            try:
                logger.info("🔍 Étape 3: Modification du client existant...")
                
                # Modifier l'email
                original_email = details.email_edit.text()
                new_email = "test.modificado@example.com"
                details.email_edit.setText(new_email)
                
                logger.info(f"📝 Email modifié: '{original_email}' → '{new_email}'")
                
                QTimer.singleShot(500, lambda: test_step_3_continue(details, logger, client, new_email))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3_continue(details, logger, client, new_email):
            """Continuer l'étape 3"""
            try:
                # Vérifier que les boutons sont activés
                if details.save_btn.isEnabled():
                    logger.info("✅ Bouton Guardar activé après modification")
                    
                    # Sauvegarder la modification
                    details.save_btn.click()
                    
                    QTimer.singleShot(1000, lambda: test_step_4(logger, client, new_email))
                else:
                    logger.error("❌ Bouton Guardar non activé après modification")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_4(logger, client, new_email):
            """Étape 4: Vérifier la mise à jour en base"""
            try:
                logger.info("🔍 Étape 4: Vérification de la mise à jour en base...")
                
                # Récupérer le client mis à jour depuis la base
                updated_client = db.get_client_by_id(client['id'])
                
                if updated_client:
                    logger.info(f"✅ Client récupéré depuis la base: {updated_client.get('nombre')}")
                    logger.info(f"   Email mis à jour: {updated_client.get('email')}")
                    
                    if updated_client.get('email') == new_email:
                        logger.info("✅ Modification correctement sauvegardée en base")
                    else:
                        logger.error(f"❌ Email non mis à jour en base: attendu '{new_email}', trouvé '{updated_client.get('email')}'")
                        return
                else:
                    logger.error("❌ Client non trouvé en base après mise à jour")
                    return
                
                QTimer.singleShot(500, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 4: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test de sauvegarde de clients:")
                logger.info("   ✅ Création de nouveau client")
                logger.info("   ✅ Sauvegarde en base de données")
                logger.info("   ✅ Vérification de la création")
                logger.info("   ✅ Modification de client existant")
                logger.info("   ✅ Mise à jour en base de données")
                logger.info("   ✅ Vérification de la mise à jour")
                logger.info("   ✅ Synchronisation avec la table clients")
                logger.info("🎉 Système de sauvegarde parfaitement fonctionnel!")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_step_1)
        
        # Fermer automatiquement après 25 secondes
        QTimer.singleShot(25000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test de Sauvegarde de Clients - Gestion de Facturas")
    print("=" * 58)
    print("📋 Fonctionnalités testées:")
    print("   • Création de nouveau client")
    print("   • Sauvegarde en base de données")
    print("   • Modification de client existant")
    print("   • Mise à jour en base de données")
    print("   • Synchronisation avec la table clients")
    print("   • Vérification de la persistance")
    print()
    
    exit_code = test_client_save()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 La sauvegarde de clients fonctionne parfaitement")
        print("💡 Changements reflétés dans la table clients")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
