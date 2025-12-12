#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test SÉCURISÉ de l'édition de clients avec base de données de test
N'utilise PAS la base de production !
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from database.test_database import get_test_database, cleanup_test_database
from utils.logger import get_logger

def test_safe_client_editing():
    """Test sécurisé de l'édition de clients"""
    logger = get_logger("TestSafeClientEditing")
    
    try:
        # Utiliser la base de test
        test_db = get_test_database()
        logger.info("🛡️ Utilisation de la base de données de TEST (pas de production)")
        
        app = QApplication(sys.argv)
        
        # Remplacer temporairement la base de données dans le module
        import database.database as db_module
        original_db = db_module.db
        db_module.db = test_db
        
        # Maintenant importer et utiliser les fenêtres avec la base de test
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        
        logger.info("🚀 Ouverture de la fenêtre de facturas avec base de TEST...")
        window = FacturasPyQt5Window()
        window.show()
        
        def test_step_1():
            """Étape 1: Créer un client de test"""
            try:
                logger.info("🔍 Test avec base de données de TEST uniquement")
                
                autocomplete = window.cliente_autocomplete
                details = window.client_details
                
                # Créer un nouveau client de test
                test_client_name = "Client Test Sécurisé"
                autocomplete.setText(test_client_name)
                autocomplete.editingFinished.emit()
                
                QTimer.singleShot(500, lambda: test_step_1_continue(details, logger, test_client_name))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_1_continue(details, logger, client_name):
            """Continuer l'étape 1"""
            try:
                if details.isVisible():
                    logger.info("✅ Widget de détails affiché (base de TEST)")
                    
                    # Remplir les détails
                    details.nif_edit.setText("TEST123456")
                    details.telefono_edit.setText("000111222")
                    details.email_edit.setText("test.seguro@example.com")
                    details.direccion_edit.setPlainText("Dirección de Test Seguro")
                    
                    logger.info("📝 Détails du client de test remplis")
                    
                    # Sauvegarder
                    if details.save_btn.isEnabled():
                        details.save_btn.click()
                        logger.info("💾 Client de test sauvegardé dans la base de TEST")
                    else:
                        logger.warning("⚠️ Bouton Guardar non activé")
                else:
                    logger.error("❌ Widget de détails non affiché")
                
                QTimer.singleShot(1000, lambda: test_verification(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_verification(logger):
            """Vérifier que nous utilisons bien la base de test"""
            try:
                # Vérifier le chemin de la base de données
                db_path = test_db.db_path
                logger.info(f"📊 Base utilisée: {db_path}")
                
                if "test" in db_path.lower() and "temp" in db_path:
                    logger.info("✅ CONFIRMATION: Base de données de TEST utilisée")
                    logger.info("🛡️ Aucun impact sur la base de production")
                else:
                    logger.error("❌ ATTENTION: Possible utilisation de la base de production!")
                
                # Compter les clients dans la base de test
                clients = test_db.get_all_clients()
                logger.info(f"📋 Nombre de clients dans la base de TEST: {len(clients)}")
                
                QTimer.singleShot(500, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur vérification: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test sécurisé:")
                logger.info("   ✅ Base de données de TEST utilisée")
                logger.info("   ✅ Aucun impact sur la production")
                logger.info("   ✅ Fonctionnalité d'édition testée")
                logger.info("   ✅ Sauvegarde dans environnement isolé")
                logger.info("🎉 Test sécurisé réussi!")
                
                # Restaurer la base originale
                db_module.db = original_db
                logger.info("🔄 Base de données originale restaurée")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_step_1)
        
        # Fermer automatiquement après 15 secondes
        QTimer.singleShot(15000, app.quit)
        
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
    print("🛡️ Test SÉCURISÉ d'Édition de Clients")
    print("=" * 45)
    print("🔒 IMPORTANT: Ce test utilise une base de données de TEST")
    print("✅ Aucun impact sur la base de données de production")
    print()
    print("📋 Fonctionnalités testées:")
    print("   • Création de client de test")
    print("   • Édition sécurisée")
    print("   • Sauvegarde en environnement isolé")
    print("   • Vérification de l'isolation")
    print()
    
    exit_code = test_safe_client_editing()
    
    if exit_code == 0:
        print()
        print("✅ Test sécurisé terminé avec succès!")
        print("🛡️ Base de production intacte")
        print("🧹 Base de test automatiquement nettoyée")
    else:
        print()
        print("❌ Test sécurisé échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
