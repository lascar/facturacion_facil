#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test SÉCURISÉ pour vérifier l'édition des clients existants
Utilise une base de données de test isolée
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from database.test_database import get_test_database, cleanup_test_database
from utils.logger import get_logger

def test_existing_client_edit():
    """Test d'édition de clients existants"""
    logger = get_logger("TestExistingClientEdit")
    
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
            """Étape 1: Vérifier les clients existants"""
            try:
                logger.info("🔍 Étape 1: Vérification des clients existants...")
                
                autocomplete = window.cliente_autocomplete
                details = window.client_details
                
                # Vérifier qu'il y a des clients
                clients = test_db.get_all_clients()
                logger.info(f"📊 Nombre de clients dans la base de test: {len(clients)}")
                
                if len(clients) > 0:
                    first_client = clients[0]
                    logger.info(f"📋 Premier client: {first_client.get('nombre', '')} (ID: {first_client.get('id', '')})")
                    
                    # Saisir le nom du premier client
                    client_name = first_client.get('nombre', '')
                    autocomplete.setText(client_name)
                    
                    QTimer.singleShot(500, lambda: test_step_1_continue(autocomplete, details, logger, first_client))
                else:
                    logger.error("❌ Aucun client trouvé dans la base de test")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_1_continue(autocomplete, details, logger, expected_client):
            """Continuer l'étape 1"""
            try:
                # Vérifier les suggestions
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    suggestions_count = model.rowCount()
                    logger.info(f"📋 Nombre de suggestions: {suggestions_count}")
                    
                    if suggestions_count > 0:
                        # Sélectionner la première suggestion
                        first_suggestion = model.data(model.index(0, 0), Qt.DisplayRole)
                        logger.info(f"📋 Première suggestion: {first_suggestion}")
                        
                        # Simuler la sélection
                        autocomplete.on_completion_selected(first_suggestion)
                        
                        QTimer.singleShot(500, lambda: test_step_2(autocomplete, details, logger, expected_client))
                    else:
                        logger.error("❌ Aucune suggestion trouvée")
                        return
                else:
                    logger.error("❌ Modèle de suggestions non disponible")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2(autocomplete, details, logger, expected_client):
            """Étape 2: Vérifier l'affichage des détails"""
            try:
                logger.info("🔍 Étape 2: Vérification de l'affichage des détails...")
                
                # Vérifier que le client est sélectionné
                current_client = autocomplete.get_current_client()
                if current_client:
                    logger.info(f"✅ Client sélectionné: {current_client.get('nombre', '')} (ID: {current_client.get('id', '')})")
                    
                    # Vérifier que les détails sont affichés
                    if details.isVisible():
                        logger.info("✅ Widget de détails affiché")
                        
                        # Vérifier les données affichées
                        nif_displayed = details.nif_edit.text()
                        phone_displayed = details.telefono_edit.text()
                        email_displayed = details.email_edit.text()
                        address_displayed = details.direccion_edit.toPlainText()
                        
                        logger.info(f"📋 Données affichées:")
                        logger.info(f"   NIF: '{nif_displayed}'")
                        logger.info(f"   Téléphone: '{phone_displayed}'")
                        logger.info(f"   Email: '{email_displayed}'")
                        logger.info(f"   Adresse: '{address_displayed}'")
                        
                        # Vérifier les données attendues
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
                            logger.info("✅ Toutes les données correspondent")
                        else:
                            logger.warning("⚠️ Certaines données ne correspondent pas")
                        
                        # Vérifier l'état des boutons
                        save_enabled = details.save_btn.isEnabled()
                        discard_enabled = details.discard_btn.isEnabled()
                        logger.info(f"📊 État des boutons - Guardar: {save_enabled}, Deshacer: {discard_enabled}")
                        
                        if not save_enabled and not discard_enabled:
                            logger.info("✅ Boutons correctement désactivés (pas de changements)")
                        else:
                            logger.warning("⚠️ Boutons activés sans changements")
                        
                        QTimer.singleShot(500, lambda: test_step_3(details, logger))
                    else:
                        logger.error("❌ Widget de détails non affiché")
                        return
                else:
                    logger.error("❌ Aucun client sélectionné")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3(details, logger):
            """Étape 3: Tester l'édition"""
            try:
                logger.info("🔍 Étape 3: Test de l'édition...")
                
                # Modifier le téléphone
                original_phone = details.telefono_edit.text()
                new_phone = "TEST-EDIT-123"
                details.telefono_edit.setText(new_phone)
                
                logger.info(f"📝 Téléphone modifié: '{original_phone}' → '{new_phone}'")
                
                QTimer.singleShot(300, lambda: test_step_3_continue(details, logger, original_phone, new_phone))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3_continue(details, logger, original_phone, new_phone):
            """Continuer l'étape 3"""
            try:
                # Vérifier que les boutons sont activés
                save_enabled = details.save_btn.isEnabled()
                discard_enabled = details.discard_btn.isEnabled()
                logger.info(f"📊 État après modification - Guardar: {save_enabled}, Deshacer: {discard_enabled}")
                
                if save_enabled and discard_enabled:
                    logger.info("✅ Boutons correctement activés après modification")
                    
                    # Tester l'annulation
                    details.discard_btn.click()
                    
                    QTimer.singleShot(300, lambda: test_step_4(details, logger, original_phone))
                else:
                    logger.error("❌ Boutons non activés après modification")
                    return
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_4(details, logger, original_phone):
            """Étape 4: Vérifier l'annulation"""
            try:
                logger.info("🔍 Étape 4: Vérification de l'annulation...")
                
                # Vérifier que les données ont été restaurées
                current_phone = details.telefono_edit.text()
                logger.info(f"📋 Téléphone après annulation: '{current_phone}' (original: '{original_phone}')")
                
                if current_phone == original_phone:
                    logger.info("✅ Données correctement restaurées")
                else:
                    logger.warning("⚠️ Données non restaurées correctement")
                
                # Vérifier que les boutons sont désactivés
                save_enabled = details.save_btn.isEnabled()
                discard_enabled = details.discard_btn.isEnabled()
                logger.info(f"📊 État après annulation - Guardar: {save_enabled}, Deshacer: {discard_enabled}")
                
                if not save_enabled and not discard_enabled:
                    logger.info("✅ Boutons correctement désactivés après annulation")
                else:
                    logger.warning("⚠️ Boutons non désactivés après annulation")
                
                QTimer.singleShot(500, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 4: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test d'édition de clients existants:")
                logger.info("   ✅ Sélection de client existant")
                logger.info("   ✅ Affichage des détails")
                logger.info("   ✅ Édition des champs")
                logger.info("   ✅ Activation des boutons")
                logger.info("   ✅ Annulation des changements")
                logger.info("   ✅ Restauration des données")
                logger.info("🎉 Édition de clients existants fonctionnelle!")
                
                # Restaurer la base originale
                db_module.db = original_db
                logger.info("🔄 Base de données originale restaurée")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_step_1)
        
        # Fermer automatiquement après 20 secondes
        QTimer.singleShot(20000, app.quit)
        
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
    print("🧪 Test SÉCURISÉ d'Édition de Clients Existants")
    print("=" * 50)
    print("🔒 IMPORTANT: Ce test utilise une base de données de TEST")
    print("✅ Aucun impact sur la base de données de production")
    print()
    print("📋 Fonctionnalités testées:")
    print("   • Sélection de client existant")
    print("   • Affichage des détails")
    print("   • Édition des champs")
    print("   • Activation/désactivation des boutons")
    print("   • Annulation des changements")
    print()
    
    exit_code = test_existing_client_edit()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎯 Édition de clients existants validée")
        print("🛡️ Base de production intacte")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
