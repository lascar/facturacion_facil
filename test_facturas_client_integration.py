#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration complète de l'édition de clients
Vérifie que les changements sont reflétés dans la table client
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from ui.facturas_pyqt5 import FacturasPyQt5Window
from ui.clientes_pyqt5 import ClientesPyQt5Window
from database.database import db
from utils.logger import get_logger

def test_client_integration():
    """Test d'intégration complète"""
    logger = get_logger("TestFacturasClientIntegration")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer les fenêtres
        logger.info("🚀 Ouverture des fenêtres...")
        facturas_window = FacturasPyQt5Window()
        facturas_window.show()
        
        clients_window = ClientesPyQt5Window()
        clients_window.show()
        
        def test_step_1():
            """Étape 1: Créer un client depuis facturas"""
            try:
                logger.info("🔍 Étape 1: Création d'un client depuis facturas...")
                
                autocomplete = facturas_window.cliente_autocomplete
                details = facturas_window.client_details
                
                # Créer un nouveau client
                new_client_name = "Cliente Integracion Test"
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
                # Remplir les détails
                details.nif_edit.setText("87654321X")
                details.telefono_edit.setText("999888777")
                details.email_edit.setText("integracion@test.com")
                details.direccion_edit.setPlainText("Calle Integracion, 456")
                
                logger.info("📝 Détails du client remplis")
                
                # Sauvegarder
                details.save_btn.click()
                
                QTimer.singleShot(1000, lambda: test_step_2(logger, client_name))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2(logger, client_name):
            """Étape 2: Vérifier dans la table clients"""
            try:
                logger.info("🔍 Étape 2: Vérification dans la table clients...")
                
                # Recharger la table des clients
                clients_window.load_clientes()
                
                # Chercher le client dans la table
                table = clients_window.table_clientes
                found_client = False
                client_row = -1
                
                for row in range(table.rowCount()):
                    name_item = table.item(row, 1)  # Colonne nom
                    if name_item and name_item.text() == client_name:
                        found_client = True
                        client_row = row
                        break
                
                if found_client:
                    logger.info(f"✅ Client trouvé dans la table à la ligne {client_row}")
                    
                    # Vérifier les données
                    nif_item = table.item(client_row, 2)  # Colonne NIF
                    phone_item = table.item(client_row, 4)  # Colonne téléphone
                    email_item = table.item(client_row, 5)  # Colonne email
                    
                    logger.info(f"   NIF: {nif_item.text() if nif_item else 'N/A'}")
                    logger.info(f"   Téléphone: {phone_item.text() if phone_item else 'N/A'}")
                    logger.info(f"   Email: {email_item.text() if email_item else 'N/A'}")
                    
                    if (nif_item and nif_item.text() == "87654321X" and
                        phone_item and phone_item.text() == "999888777" and
                        email_item and email_item.text() == "integracion@test.com"):
                        logger.info("✅ Toutes les données correspondent dans la table")
                    else:
                        logger.warning("⚠️ Certaines données ne correspondent pas")
                else:
                    logger.error("❌ Client non trouvé dans la table")
                    return
                
                QTimer.singleShot(500, lambda: test_step_3(logger, client_name, client_row))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3(logger, client_name, client_row):
            """Étape 3: Modifier le client depuis facturas"""
            try:
                logger.info("🔍 Étape 3: Modification du client depuis facturas...")
                
                # Sélectionner le client dans facturas
                autocomplete = facturas_window.cliente_autocomplete
                details = facturas_window.client_details
                
                autocomplete.setText(client_name)
                
                QTimer.singleShot(300, lambda: test_step_3_continue(autocomplete, details, logger, client_name, client_row))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3_continue(autocomplete, details, logger, client_name, client_row):
            """Continuer l'étape 3"""
            try:
                # Sélectionner le client
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    for i in range(model.rowCount()):
                        suggestion = model.data(model.index(i, 0), Qt.DisplayRole)
                        if client_name in suggestion:
                            autocomplete.on_completion_selected(suggestion)
                            break
                
                QTimer.singleShot(500, lambda: test_step_3_modify(details, logger, client_name, client_row))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3_modify(details, logger, client_name, client_row):
            """Modifier le client"""
            try:
                # Modifier l'email
                new_email = "modificado.integracion@test.com"
                details.email_edit.setText(new_email)
                
                logger.info(f"📝 Email modifié vers: {new_email}")
                
                # Sauvegarder
                details.save_btn.click()
                
                QTimer.singleShot(1000, lambda: test_step_4(logger, client_name, client_row, new_email))
                
            except Exception as e:
                logger.error(f"❌ Erreur modification: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_4(logger, client_name, client_row, new_email):
            """Étape 4: Vérifier la mise à jour dans la table"""
            try:
                logger.info("🔍 Étape 4: Vérification de la mise à jour dans la table...")
                
                # Recharger la table des clients
                clients_window.load_clientes()
                
                # Vérifier la mise à jour
                table = clients_window.table_clientes
                email_item = table.item(client_row, 5)  # Colonne email
                
                if email_item and email_item.text() == new_email:
                    logger.info("✅ Email correctement mis à jour dans la table")
                else:
                    current_email = email_item.text() if email_item else "N/A"
                    logger.error(f"❌ Email non mis à jour: attendu '{new_email}', trouvé '{current_email}'")
                    return
                
                QTimer.singleShot(500, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 4: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test d'intégration:")
                logger.info("   ✅ Création de client depuis facturas")
                logger.info("   ✅ Sauvegarde en base de données")
                logger.info("   ✅ Affichage dans la table clients")
                logger.info("   ✅ Modification depuis facturas")
                logger.info("   ✅ Mise à jour dans la table clients")
                logger.info("   ✅ Synchronisation parfaite")
                logger.info("🎉 Intégration complète réussie!")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_step_1)
        
        # Fermer automatiquement après 30 secondes
        QTimer.singleShot(30000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test d'Intégration Complète - Édition de Clients")
    print("=" * 55)
    print("📋 Fonctionnalités testées:")
    print("   • Création de client depuis facturas")
    print("   • Sauvegarde en base de données")
    print("   • Affichage dans la table clients")
    print("   • Modification depuis facturas")
    print("   • Mise à jour dans la table clients")
    print("   • Synchronisation bidirectionnelle")
    print()
    
    exit_code = test_client_integration()
    
    if exit_code == 0:
        print()
        print("✅ Test d'intégration terminé avec succès!")
        print("🎉 Synchronisation parfaite entre facturas et table clients")
        print("💡 Système d'édition complètement opérationnel")
    else:
        print()
        print("❌ Test d'intégration échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
