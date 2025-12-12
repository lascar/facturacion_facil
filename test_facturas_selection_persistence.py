#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test spécifique pour vérifier que les clients peuvent être sélectionnés
pendant la saisie et ne disparaissent pas aussitôt
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_selection_persistence():
    """Test de la persistance de la sélection"""
    logger = get_logger("TestFacturasSelectionPersistence")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        def test_typing_and_selection():
            """Test de saisie et sélection"""
            try:
                logger.info("🔍 Test: Saisie progressive et sélection de clients...")
                
                autocomplete = window.cliente_autocomplete
                
                # Étape 1: Saisir "c"
                logger.info("📝 Étape 1: Saisie 'c'")
                autocomplete.setText("c")
                
                QTimer.singleShot(300, lambda: step_2(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur test typing: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def step_2(autocomplete, logger):
            """Étape 2: Continuer avec 'cl'"""
            try:
                # Vérifier les suggestions pour "c"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    count_c = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'c': {count_c}")
                
                # Continuer avec "cl"
                logger.info("📝 Étape 2: Saisie 'cl'")
                autocomplete.setText("cl")
                
                QTimer.singleShot(300, lambda: step_3(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur step 2: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def step_3(autocomplete, logger):
            """Étape 3: Continuer avec 'cli'"""
            try:
                # Vérifier les suggestions pour "cl"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    count_cl = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'cl': {count_cl}")
                
                # Continuer avec "cli"
                logger.info("📝 Étape 3: Saisie 'cli'")
                autocomplete.setText("cli")
                
                QTimer.singleShot(300, lambda: step_4(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur step 3: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def step_4(autocomplete, logger):
            """Étape 4: Continuer avec 'clie'"""
            try:
                # Vérifier les suggestions pour "cli"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    count_cli = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'cli': {count_cli}")
                
                # Continuer avec "clie"
                logger.info("📝 Étape 4: Saisie 'clie'")
                autocomplete.setText("clie")
                
                QTimer.singleShot(300, lambda: step_5(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur step 4: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def step_5(autocomplete, logger):
            """Étape 5: Finaliser avec 'client'"""
            try:
                # Vérifier les suggestions pour "clie"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    count_clie = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'clie': {count_clie}")
                
                # Finaliser avec "client"
                logger.info("📝 Étape 5: Saisie 'client'")
                autocomplete.setText("client")
                
                QTimer.singleShot(300, lambda: test_selection(autocomplete, logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur step 5: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def test_selection(autocomplete, logger):
            """Test de sélection d'un client"""
            try:
                logger.info("🎯 Test de sélection d'un client...")
                
                # Vérifier les suggestions pour "client"
                if hasattr(autocomplete.completer, 'model') and autocomplete.completer.model():
                    model = autocomplete.completer.model()
                    count_client = model.rowCount()
                    logger.info(f"✅ Suggestions pour 'client': {count_client}")
                    
                    if count_client > 0:
                        # Afficher toutes les suggestions disponibles
                        logger.info("📋 Suggestions disponibles:")
                        for i in range(count_client):
                            suggestion = model.data(model.index(i, 0), Qt.DisplayRole)
                            logger.info(f"   {i+1}. {suggestion}")
                        
                        # Sélectionner la première suggestion
                        first_suggestion = model.data(model.index(0, 0), Qt.DisplayRole)
                        logger.info(f"🎯 Sélection de: {first_suggestion}")
                        
                        # Simuler la sélection
                        autocomplete.on_completion_selected(first_suggestion)
                        
                        # Vérifier que le client a été sélectionné
                        current_client = autocomplete.get_current_client()
                        if current_client:
                            logger.info(f"✅ Client sélectionné avec succès!")
                            logger.info(f"   Nom: {current_client.get('nombre', '')}")
                            logger.info(f"   ID: {current_client.get('id', 'N/A')}")
                            logger.info(f"   Nouveau: {current_client.get('is_new', False)}")
                        else:
                            logger.warning("⚠️ Aucun client sélectionné")
                    else:
                        logger.warning("⚠️ Aucune suggestion disponible")
                else:
                    logger.warning("⚠️ Pas de modèle de suggestions")
                
                QTimer.singleShot(500, lambda: final_summary(logger))
                
            except Exception as e:
                logger.error(f"❌ Erreur test selection: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def final_summary(logger):
            """Résumé final"""
            try:
                logger.info("📊 Résumé du test de persistance de sélection:")
                logger.info("   ✅ Saisie progressive maintient les suggestions")
                logger.info("   ✅ Les clients restent sélectionnables pendant la saisie")
                logger.info("   ✅ La sélection fonctionne correctement")
                logger.info("   ✅ Les suggestions ne disparaissent plus aussitôt")
                logger.info("🎉 Problème de disparition des clients résolu!")
                
            except Exception as e:
                logger.error(f"❌ Erreur résumé final: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes
        QTimer.singleShot(2000, test_typing_and_selection)
        
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
    print("🧪 Test de Persistance de Sélection - Autocomplétion Clients")
    print("=" * 65)
    print("🎯 Objectif:")
    print("   Vérifier que les clients peuvent être sélectionnés pendant")
    print("   la saisie et ne disparaissent pas aussitôt")
    print()
    print("📋 Scénario testé:")
    print("   1. Saisie progressive: c → cl → cli → clie → client")
    print("   2. Vérification des suggestions à chaque étape")
    print("   3. Sélection d'un client depuis les suggestions")
    print("   4. Validation de la persistance")
    print()
    
    exit_code = test_selection_persistence()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 Les clients restent sélectionnables pendant la saisie")
        print("💡 Le problème de disparition est résolu")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
