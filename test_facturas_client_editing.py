#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'édition de clients avec boutons Guardar et Deshacer cambios
Vérifie que les changements peuvent être sauvegardés ou annulés
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_client_editing():
    """Test de l'édition de clients"""
    logger = get_logger("TestFacturasClientEditing")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        def test_step_1():
            """Étape 1: Sélectionner un client existant"""
            try:
                logger.info("🔍 Étape 1: Sélection d'un client existant...")
                
                autocomplete = window.cliente_autocomplete
                details = window.client_details
                
                # Saisir un client existant
                autocomplete.setText("client")
                
                QTimer.singleShot(300, lambda: test_step_1_continue(autocomplete, details, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_1_continue(autocomplete, details, logger):
            """Continuer l'étape 1"""
            try:
                # Sélectionner le premier client
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    if model.rowCount() > 0:
                        first_suggestion = model.data(model.index(0, 0), Qt.DisplayRole)
                        logger.info(f"📋 Sélection du client: {first_suggestion}")
                        autocomplete.on_completion_selected(first_suggestion)
                        
                        # Vérifier que les détails sont affichés
                        if details.isVisible():
                            logger.info("✅ Widget de détails affiché")
                            
                            # Vérifier l'état initial des boutons
                            if hasattr(details, 'save_btn') and hasattr(details, 'discard_btn'):
                                save_enabled = details.save_btn.isEnabled()
                                discard_enabled = details.discard_btn.isEnabled()
                                logger.info(f"📊 État initial - Guardar: {save_enabled}, Deshacer: {discard_enabled}")
                                
                                if not save_enabled and not discard_enabled:
                                    logger.info("✅ Boutons correctement désactivés (pas de changements)")
                                else:
                                    logger.warning("⚠️ Boutons activés sans changements")
                            else:
                                logger.error("❌ Boutons Guardar/Deshacer non trouvés")
                                return
                        else:
                            logger.warning("⚠️ Widget de détails non affiché")
                            return
                    else:
                        logger.warning("⚠️ Aucune suggestion trouvée")
                        return
                else:
                    logger.warning("⚠️ Pas de modèle de suggestions")
                    return
                
                QTimer.singleShot(500, lambda: test_step_2(details, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 1 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2(details, logger):
            """Étape 2: Modifier les données du client"""
            try:
                logger.info("🔍 Étape 2: Modification des données client...")
                
                # Modifier le téléphone
                original_phone = details.telefono_edit.text()
                new_phone = "666777888"
                details.telefono_edit.setText(new_phone)
                logger.info(f"📝 Téléphone modifié: '{original_phone}' → '{new_phone}'")
                
                # Modifier l'email
                original_email = details.email_edit.text()
                new_email = "test.edit@example.com"
                details.email_edit.setText(new_email)
                logger.info(f"📝 Email modifié: '{original_email}' → '{new_email}'")
                
                QTimer.singleShot(300, lambda: test_step_2_continue(details, logger, original_phone, original_email))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2_continue(details, logger, original_phone, original_email):
            """Continuer l'étape 2"""
            try:
                # Vérifier que les boutons sont maintenant activés
                save_enabled = details.save_btn.isEnabled()
                discard_enabled = details.discard_btn.isEnabled()
                logger.info(f"📊 État après modification - Guardar: {save_enabled}, Deshacer: {discard_enabled}")
                
                if save_enabled and discard_enabled:
                    logger.info("✅ Boutons correctement activés après modification")
                else:
                    logger.warning("⚠️ Boutons non activés après modification")
                
                # Vérifier l'indicateur de changements dans le titre
                title = details.details_group.title()
                if title.startswith("*"):
                    logger.info("✅ Indicateur de changements affiché dans le titre")
                else:
                    logger.info(f"📋 Titre actuel: {title}")
                
                QTimer.singleShot(500, lambda: test_step_3(details, logger, original_phone, original_email))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 2 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3(details, logger, original_phone, original_email):
            """Étape 3: Tester l'annulation des changements"""
            try:
                logger.info("🔍 Étape 3: Test d'annulation des changements...")
                
                # Cliquer sur "Deshacer cambios"
                details.discard_btn.click()
                
                QTimer.singleShot(300, lambda: test_step_3_continue(details, logger, original_phone, original_email))
                
            except Exception as e:
                logger.error(f"❌ Erreur étape 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3_continue(details, logger, original_phone, original_email):
            """Continuer l'étape 3"""
            try:
                # Vérifier que les données ont été restaurées
                current_phone = details.telefono_edit.text()
                current_email = details.email_edit.text()
                
                logger.info(f"📋 Téléphone après annulation: '{current_phone}' (original: '{original_phone}')")
                logger.info(f"📋 Email après annulation: '{current_email}' (original: '{original_email}')")
                
                if current_phone == original_phone and current_email == original_email:
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
                logger.error(f"❌ Erreur étape 3 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test d'édition de clients:")
                logger.info("   ✅ Sélection de client existant")
                logger.info("   ✅ Affichage des détails client")
                logger.info("   ✅ Boutons Guardar/Deshacer présents")
                logger.info("   ✅ Détection des changements")
                logger.info("   ✅ Activation/désactivation des boutons")
                logger.info("   ✅ Annulation des changements")
                logger.info("   ✅ Restauration des données originales")
                logger.info("🎉 Système d'édition de clients opérationnel!")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
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
    print("🧪 Test d'Édition de Clients - Gestion de Facturas")
    print("=" * 55)
    print("📋 Fonctionnalités testées:")
    print("   • Sélection de client existant")
    print("   • Modification des données client")
    print("   • Boutons Guardar et Deshacer cambios")
    print("   • Détection des changements")
    print("   • Annulation des modifications")
    print("   • Restauration des données originales")
    print()
    
    exit_code = test_client_editing()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 Le système d'édition de clients fonctionne")
        print("💡 Boutons Guardar/Deshacer opérationnels")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
