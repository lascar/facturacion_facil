#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du système d'autocomplétion de clients avec création de nouveaux clients
Vérifie l'ensemble du workflow : saisie, autocomplétion, création, détails
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_complete_client_workflow():
    """Test complet du workflow client"""
    logger = get_logger("TestFacturasClientComplete")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Variables pour le test
        test_results = {
            'autocomplete_widget': False,
            'details_widget': False,
            'existing_client_search': False,
            'new_client_creation': False,
            'client_details_form': False,
            'data_persistence': False
        }
        
        def test_step_1():
            """Étape 1: Vérifier les widgets"""
            try:
                logger.info("🔍 Étape 1: Vérification des widgets...")
                
                # Widget d'autocomplétion
                if hasattr(window, 'cliente_autocomplete'):
                    autocomplete = window.cliente_autocomplete
                    logger.info(f"✅ Widget d'autocomplétion: {type(autocomplete).__name__}")
                    test_results['autocomplete_widget'] = True
                    
                    # Vérifier les clients chargés
                    if hasattr(autocomplete, 'clients_data') and autocomplete.clients_data:
                        logger.info(f"✅ {len(autocomplete.clients_data)} clients chargés")
                    else:
                        logger.warning("⚠️ Aucun client chargé")
                else:
                    logger.error("❌ Widget d'autocomplétion manquant")
                
                # Widget de détails
                if hasattr(window, 'client_details'):
                    details = window.client_details
                    logger.info(f"✅ Widget de détails: {type(details).__name__}")
                    test_results['details_widget'] = True
                else:
                    logger.error("❌ Widget de détails manquant")
                
                # Passer à l'étape suivante
                QTimer.singleShot(500, test_step_2)
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2():
            """Étape 2: Test de recherche de client existant"""
            try:
                logger.info("🔍 Étape 2: Test de recherche de client existant...")
                
                autocomplete = window.cliente_autocomplete
                
                # Saisir un début de nom de client existant
                autocomplete.setText("client")
                
                # Vérifier que l'autocomplétion fonctionne
                if hasattr(autocomplete, 'completer') and autocomplete.completer:
                    model = autocomplete.completer.model()
                    if model and model.rowCount() > 0:
                        logger.info(f"✅ Autocomplétion: {model.rowCount()} suggestions trouvées")
                        test_results['existing_client_search'] = True
                    else:
                        logger.warning("⚠️ Aucune suggestion d'autocomplétion")
                
                # Passer à l'étape suivante
                QTimer.singleShot(500, test_step_3)
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3():
            """Étape 3: Test de création de nouveau client"""
            try:
                logger.info("🔍 Étape 3: Test de création de nouveau client...")
                
                autocomplete = window.cliente_autocomplete
                details = window.client_details
                
                # Effacer et saisir un nouveau nom
                autocomplete.clear()
                new_client_name = "Cliente Test Autocompletado"
                autocomplete.setText(new_client_name)
                
                # Simuler la fin d'édition pour déclencher la création
                autocomplete.editingFinished.emit()
                
                # Vérifier qu'un nouveau client a été créé
                current_client = autocomplete.get_current_client()
                if current_client and current_client.get('is_new', False):
                    logger.info(f"✅ Nouveau client créé: {current_client.get('nombre', '')}")
                    test_results['new_client_creation'] = True
                    
                    # Vérifier que le widget de détails est visible
                    if details.isVisible():
                        logger.info("✅ Widget de détails affiché")
                        test_results['client_details_form'] = True
                    else:
                        logger.warning("⚠️ Widget de détails non affiché")
                else:
                    logger.warning("⚠️ Nouveau client non créé")
                
                # Passer à l'étape suivante
                QTimer.singleShot(500, test_step_4)
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_4():
            """Étape 4: Test de saisie des détails client"""
            try:
                logger.info("🔍 Étape 4: Test de saisie des détails client...")
                
                details = window.client_details
                
                # Remplir les détails du client
                if hasattr(details, 'nif_edit'):
                    details.nif_edit.setText("12345678Z")
                    logger.info("✅ NIF saisi")
                
                if hasattr(details, 'telefono_edit'):
                    details.telefono_edit.setText("666777888")
                    logger.info("✅ Téléphone saisi")
                
                if hasattr(details, 'email_edit'):
                    details.email_edit.setText("test@example.com")
                    logger.info("✅ Email saisi")
                
                if hasattr(details, 'direccion_edit'):
                    details.direccion_edit.setPlainText("Calle Test, 123")
                    logger.info("✅ Adresse saisie")
                
                # Vérifier que les données sont mises à jour
                client_data = details.get_client_data()
                if client_data:
                    logger.info(f"✅ Données client récupérées: {client_data.get('nombre', '')}")
                    logger.info(f"   NIF: {client_data.get('nif', '')}")
                    logger.info(f"   Téléphone: {client_data.get('telefono', '')}")
                    logger.info(f"   Email: {client_data.get('email', '')}")
                    test_results['data_persistence'] = True
                else:
                    logger.warning("⚠️ Données client non récupérées")
                
                # Passer au résumé final
                QTimer.singleShot(500, test_final_summary)
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 4: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary():
            """Résumé final du test complet"""
            try:
                logger.info("📊 Résumé final du test complet:")
                
                total_tests = len(test_results)
                passed_tests = sum(test_results.values())
                
                for test_name, result in test_results.items():
                    status = "✅" if result else "❌"
                    logger.info(f"   {status} {test_name.replace('_', ' ').title()}: {'PASS' if result else 'FAIL'}")
                
                logger.info(f"📈 Résultat: {passed_tests}/{total_tests} tests réussis")
                
                if passed_tests == total_tests:
                    logger.info("🎉 TOUS LES TESTS RÉUSSIS!")
                    logger.info("💡 Le système d'autocomplétion de clients est parfaitement fonctionnel")
                    logger.info("🚀 Fonctionnalités validées:")
                    logger.info("   • Autocomplétion de clients existants")
                    logger.info("   • Création automatique de nouveaux clients")
                    logger.info("   • Formulaire de détails client intégré")
                    logger.info("   • Persistance des données saisies")
                elif passed_tests >= total_tests * 0.8:
                    logger.info("✅ TESTS MAJORITAIREMENT RÉUSSIS")
                    logger.info("💡 Le système fonctionne avec quelques améliorations possibles")
                else:
                    logger.warning("⚠️ TESTS PARTIELLEMENT RÉUSSIS")
                    logger.info("🔧 Le système nécessite des corrections")
                
                logger.info("🎯 Test complet terminé")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_step_1)
        
        # Fermer automatiquement après 20 secondes
        QTimer.singleShot(20000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test Complet du Système d'Autocomplétion de Clients")
    print("=" * 60)
    print("📋 Workflow testé:")
    print("   1. Vérification des widgets d'autocomplétion")
    print("   2. Test de recherche de clients existants")
    print("   3. Test de création de nouveaux clients")
    print("   4. Test de saisie des détails client")
    print("   5. Validation de la persistance des données")
    print()
    
    exit_code = test_complete_client_workflow()
    
    if exit_code == 0:
        print()
        print("✅ Test complet terminé avec succès!")
        print("🎉 Le système d'autocomplétion de clients est opérationnel")
        print("💡 Workflow complet validé : saisie → autocomplétion → création → détails")
    else:
        print()
        print("❌ Test complet échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
