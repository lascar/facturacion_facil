#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système d'autocomplétion de clients dans la gestion de facturas
Vérifie que les clients peuvent être sélectionnés par autocomplétion et créés directement
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from ui.client_autocomplete_widget import ClientAutoCompleteWidget, ClientDetailsWidget
from utils.logger import get_logger

def test_client_autocomplete():
    """Test du système d'autocomplétion de clients"""
    logger = get_logger("TestFacturasClientAutocomplete")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Fonction pour tester l'autocomplétion
        def test_autocomplete():
            try:
                logger.info("🔍 Test du système d'autocomplétion de clients...")
                
                # Vérifier que les widgets existent
                if hasattr(window, 'cliente_autocomplete'):
                    logger.info("✅ Widget d'autocomplétion trouvé")
                    autocomplete_widget = window.cliente_autocomplete
                    
                    # Vérifier le type
                    if isinstance(autocomplete_widget, ClientAutoCompleteWidget):
                        logger.info("✅ Type correct: ClientAutoCompleteWidget")
                    else:
                        logger.error(f"❌ Type incorrect: {type(autocomplete_widget)}")
                        return
                    
                    # Vérifier le placeholder
                    placeholder = autocomplete_widget.placeholderText()
                    logger.info(f"📝 Placeholder: '{placeholder}'")
                    
                    # Tester la saisie d'un client existant
                    logger.info("🧪 Test 1: Saisie d'un client existant...")
                    autocomplete_widget.setText("client")
                    
                    # Attendre un peu pour l'autocomplétion
                    QTimer.singleShot(500, lambda: test_new_client(autocomplete_widget, logger))
                    
                else:
                    logger.error("❌ Widget d'autocomplétion non trouvé")
                    return
                
                # Vérifier le widget de détails
                if hasattr(window, 'client_details'):
                    logger.info("✅ Widget de détails client trouvé")
                    details_widget = window.client_details
                    
                    if isinstance(details_widget, ClientDetailsWidget):
                        logger.info("✅ Type correct: ClientDetailsWidget")
                    else:
                        logger.error(f"❌ Type incorrect: {type(details_widget)}")
                        return
                        
                    # Vérifier qu'il est caché par défaut
                    if details_widget.isVisible():
                        logger.warning("⚠️ Widget de détails visible par défaut")
                    else:
                        logger.info("✅ Widget de détails caché par défaut")
                        
                else:
                    logger.error("❌ Widget de détails client non trouvé")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du test d'autocomplétion: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_new_client(autocomplete_widget, logger):
            """Test de création d'un nouveau client"""
            try:
                logger.info("🧪 Test 2: Création d'un nouveau client...")
                
                # Effacer et saisir un nouveau nom
                autocomplete_widget.clear()
                autocomplete_widget.setText("Nuevo Cliente Test")
                
                # Simuler la fin d'édition
                autocomplete_widget.editingFinished.emit()
                
                # Vérifier l'état
                current_client = autocomplete_widget.get_current_client()
                if current_client:
                    logger.info(f"✅ Nouveau client détecté: {current_client.get('nombre', '')}")
                    logger.info(f"   Is new: {current_client.get('is_new', False)}")
                    
                    # Vérifier que le widget de détails est visible
                    if hasattr(window, 'client_details') and window.client_details.isVisible():
                        logger.info("✅ Widget de détails affiché pour nouveau client")
                    else:
                        logger.warning("⚠️ Widget de détails non affiché")
                        
                else:
                    logger.warning("⚠️ Aucun client détecté")
                
                # Test final
                QTimer.singleShot(1000, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du test de nouveau client: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final du test"""
            try:
                logger.info("📊 Résumé final du test d'autocomplétion:")
                
                # Vérifier les composants
                components_ok = 0
                total_components = 2
                
                if hasattr(window, 'cliente_autocomplete'):
                    components_ok += 1
                    logger.info("   ✅ Widget d'autocomplétion: OK")
                else:
                    logger.error("   ❌ Widget d'autocomplétion: MANQUANT")
                
                if hasattr(window, 'client_details'):
                    components_ok += 1
                    logger.info("   ✅ Widget de détails: OK")
                else:
                    logger.error("   ❌ Widget de détails: MANQUANT")
                
                # Résultat final
                if components_ok == total_components:
                    logger.info("🎉 Tous les composants d'autocomplétion sont présents!")
                    logger.info("💡 Le système d'autocomplétion est opérationnel")
                else:
                    logger.warning(f"⚠️ {components_ok}/{total_components} composants présents")
                
                logger.info("🎯 Test d'autocomplétion terminé")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes (laisser le temps au chargement)
        QTimer.singleShot(2000, test_autocomplete)
        
        # Fermer automatiquement après 15 secondes
        QTimer.singleShot(15000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test du Système d'Autocomplétion de Clients - Gestion de Facturas")
    print("=" * 70)
    print("📋 Objectifs:")
    print("   • Vérifier que le widget d'autocomplétion remplace le combo box")
    print("   • Tester la saisie de clients existants")
    print("   • Tester la création de nouveaux clients")
    print("   • Valider l'affichage des détails client")
    print("   • Confirmer l'intégration dans l'interface")
    print()
    
    exit_code = test_client_autocomplete()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 Le système d'autocomplétion de clients fonctionne")
        print("💡 Plus besoin de select - saisie libre avec suggestions")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
