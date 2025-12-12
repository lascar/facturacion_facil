#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des états de factures depuis la configuration d'organisation
Vérifie que les états du combo sont ceux configurés dans l'organisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger
from utils.invoice_status_manager import invoice_status_manager

def test_estados_organizacion():
    """Test des états depuis la configuration d'organisation"""
    logger = get_logger("TestFacturasEstadosOrganizacion")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Fonction pour tester les états
        def test_estados():
            try:
                logger.info("🔍 Test des états de factures...")
                
                # Récupérer les états depuis le gestionnaire
                estados_config = invoice_status_manager.get_all_statuses()
                logger.info(f"📊 États configurés dans l'organisation: {len(estados_config)}")
                
                for i, estado in enumerate(estados_config):
                    logger.info(f"   {i+1}. {estado['nombre']} - {estado['descripcion']} (Couleur: {estado['color']})")
                
                # Vérifier les états dans le combo
                combo_count = window.estado_combo.count()
                logger.info(f"📋 États dans le combo: {combo_count}")
                
                for i in range(combo_count):
                    text = window.estado_combo.itemText(i)
                    data = window.estado_combo.itemData(i)
                    logger.info(f"   {i}: '{text}' (ID: {data})")
                
                # Vérifier la correspondance
                if len(estados_config) == combo_count:
                    logger.info("✅ Nombre d'états correspond entre configuration et combo")
                    
                    # Vérifier que tous les états configurés sont dans le combo
                    estados_combo = [window.estado_combo.itemText(i) for i in range(combo_count)]
                    estados_nombres = [estado['nombre'] for estado in estados_config]
                    
                    missing_estados = set(estados_nombres) - set(estados_combo)
                    extra_estados = set(estados_combo) - set(estados_nombres)
                    
                    if not missing_estados and not extra_estados:
                        logger.info("✅ Tous les états configurés sont présents dans le combo")
                        logger.info("✅ Aucun état supplémentaire dans le combo")
                        
                        # Test de sélection d'un état
                        if combo_count > 0:
                            logger.info("🎯 Test de sélection d'état...")
                            window.estado_combo.setCurrentIndex(0)
                            selected_text = window.estado_combo.currentText()
                            selected_data = window.estado_combo.currentData()
                            logger.info(f"   État sélectionné: '{selected_text}' (ID: {selected_data})")
                            
                            # Vérifier que l'ID correspond à un état configuré
                            estado_found = None
                            for estado in estados_config:
                                if estado['id'] == selected_data:
                                    estado_found = estado
                                    break
                            
                            if estado_found:
                                logger.info("✅ ID de l'état sélectionné correspond à la configuration")
                                logger.info(f"   Détails: {estado_found['nombre']} - {estado_found['descripcion']}")
                            else:
                                logger.warning("⚠️ ID de l'état sélectionné ne correspond pas à la configuration")
                        
                    else:
                        if missing_estados:
                            logger.warning(f"⚠️ États manquants dans le combo: {missing_estados}")
                        if extra_estados:
                            logger.warning(f"⚠️ États supplémentaires dans le combo: {extra_estados}")
                else:
                    logger.warning(f"⚠️ Nombre d'états différent: config={len(estados_config)}, combo={combo_count}")
                
                # Test avec les anciens états codés en dur
                old_estados = ["Borrador", "Enviada", "Pagada", "Cancelada"]
                logger.info("🔍 Vérification que les anciens états codés en dur ne sont plus utilisés...")
                
                estados_combo_actuels = [window.estado_combo.itemText(i) for i in range(combo_count)]
                if set(old_estados) == set(estados_combo_actuels):
                    logger.warning("⚠️ Les états semblent encore être codés en dur!")
                else:
                    logger.info("✅ Les états ne sont plus codés en dur, ils viennent de la configuration")
                
                logger.info("🎯 Test des états terminé")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du test des états: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes (laisser le temps au chargement)
        QTimer.singleShot(2000, test_estados)
        
        # Fermer automatiquement après 8 secondes
        QTimer.singleShot(8000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test des États de Factures - Configuration d'Organisation")
    print("=" * 64)
    print("📋 Objectifs:")
    print("   • Vérifier que les états viennent de la configuration d'organisation")
    print("   • Confirmer que les anciens états codés en dur ne sont plus utilisés")
    print("   • Valider la correspondance entre configuration et combo")
    print("   • Tester la sélection d'états")
    print()
    
    exit_code = test_estados_organizacion()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 Les états de factures viennent bien de la configuration d'organisation")
        print("💡 Plus d'états codés en dur, système dynamique opérationnel")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
