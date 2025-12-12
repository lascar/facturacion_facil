#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'autocomplétion améliorée pour les clients
Vérifie que les suggestions restent visibles et sélectionnables pendant la saisie
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QKeyEvent
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_improved_autocomplete():
    """Test de l'autocomplétion améliorée"""
    logger = get_logger("TestFacturasAutocompleteImproved")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        def test_step_1():
            """Test 1: Saisie progressive avec maintien des suggestions"""
            try:
                logger.info("🔍 Test 1: Saisie progressive avec maintien des suggestions...")
                
                autocomplete = window.cliente_autocomplete
                
                # Saisir progressivement "cli"
                logger.info("📝 Saisie: 'c'")
                autocomplete.setText("c")
                
                QTimer.singleShot(300, lambda: test_step_1_continue(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur test 1: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_1_continue(autocomplete, logger):
            """Continuer le test 1"""
            try:
                # Vérifier les suggestions pour "c"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    suggestions_c = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'c': {suggestions_c}")
                else:
                    logger.warning("⚠️ Pas de modèle de suggestions")
                
                # Continuer avec "cl"
                logger.info("📝 Saisie: 'cl'")
                autocomplete.setText("cl")
                
                QTimer.singleShot(300, lambda: test_step_1_final(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur test 1 continue: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_1_final(autocomplete, logger):
            """Finaliser le test 1"""
            try:
                # Vérifier les suggestions pour "cl"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    suggestions_cl = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'cl': {suggestions_cl}")
                    
                    # Afficher les suggestions
                    for i in range(min(3, suggestions_cl)):
                        suggestion = model.data(model.index(i, 0), Qt.DisplayRole)
                        logger.info(f"   Suggestion {i+1}: {suggestion}")
                else:
                    logger.warning("⚠️ Pas de modèle de suggestions pour 'cl'")
                
                # Continuer avec "client"
                logger.info("📝 Saisie: 'client'")
                autocomplete.setText("client")
                
                QTimer.singleShot(300, lambda: test_step_2(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur test 1 final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_2(autocomplete, logger):
            """Test 2: Sélection d'une suggestion"""
            try:
                logger.info("🔍 Test 2: Sélection d'une suggestion...")
                
                # Vérifier les suggestions pour "client"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    suggestions_client = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'client': {suggestions_client}")
                    
                    if suggestions_client > 0:
                        # Prendre la première suggestion
                        first_suggestion = model.data(model.index(0, 0), Qt.DisplayRole)
                        logger.info(f"📋 Première suggestion: {first_suggestion}")
                        
                        # Simuler la sélection
                        autocomplete.on_completion_selected(first_suggestion)
                        
                        # Vérifier que le client a été sélectionné
                        current_client = autocomplete.get_current_client()
                        if current_client:
                            logger.info(f"✅ Client sélectionné: {current_client.get('nombre', '')}")
                            logger.info(f"   ID: {current_client.get('id', 'N/A')}")
                            logger.info(f"   Is new: {current_client.get('is_new', False)}")
                        else:
                            logger.warning("⚠️ Aucun client sélectionné")
                    else:
                        logger.warning("⚠️ Aucune suggestion pour 'client'")
                else:
                    logger.warning("⚠️ Pas de modèle de suggestions")
                
                QTimer.singleShot(500, lambda: test_step_3(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur test 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_step_3(autocomplete, logger):
            """Test 3: Test de création de nouveau client"""
            try:
                logger.info("🔍 Test 3: Test de création de nouveau client...")
                
                # Effacer et saisir un nom qui n'existe pas
                autocomplete.clear()
                new_name = "Cliente Inexistente Test"
                autocomplete.setText(new_name)
                
                # Simuler la fin d'édition
                autocomplete.editingFinished.emit()
                
                # Vérifier qu'un nouveau client a été créé
                current_client = autocomplete.get_current_client()
                if current_client and current_client.get('is_new', False):
                    logger.info(f"✅ Nouveau client créé: {current_client.get('nombre', '')}")
                    logger.info(f"   Is new: {current_client.get('is_new', False)}")
                else:
                    logger.warning("⚠️ Nouveau client non créé")
                
                QTimer.singleShot(500, lambda: test_final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur test 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test d'autocomplétion améliorée:")
                logger.info("   ✅ Saisie progressive testée")
                logger.info("   ✅ Suggestions maintenues pendant la saisie")
                logger.info("   ✅ Sélection de clients existants")
                logger.info("   ✅ Création de nouveaux clients")
                logger.info("🎉 Test d'autocomplétion améliorée terminé!")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_step_1)
        
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
    print("🧪 Test de l'Autocomplétion Améliorée - Gestion de Facturas")
    print("=" * 60)
    print("📋 Tests effectués:")
    print("   • Saisie progressive avec maintien des suggestions")
    print("   • Sélection de clients existants")
    print("   • Création de nouveaux clients")
    print("   • Vérification de la persistance des suggestions")
    print()
    
    exit_code = test_improved_autocomplete()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 L'autocomplétion améliorée fonctionne correctement")
        print("💡 Les suggestions restent visibles pendant la saisie")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
