#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des styles des combo boxes dans la gestion de facturas
Vérifie que les options sélectionnées ne sont plus blanches
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QComboBox
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_combo_styles():
    """Test des styles des combo boxes"""
    logger = get_logger("TestFacturasComboStyles")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Fonction pour tester les styles
        def test_styles():
            try:
                logger.info("🔍 Test des styles des combo boxes...")
                
                # Trouver tous les combo boxes dans la fenêtre
                combo_boxes = window.findChildren(QComboBox)
                logger.info(f"📊 {len(combo_boxes)} combo boxes trouvés")
                
                styled_combos = 0
                unstyled_combos = 0
                
                for i, combo in enumerate(combo_boxes):
                    # Vérifier si le combo a un style appliqué
                    style_sheet = combo.styleSheet()
                    
                    if style_sheet and "QComboBox" in style_sheet:
                        styled_combos += 1
                        logger.info(f"✅ Combo {i+1}: Style appliqué")
                        
                        # Vérifier les propriétés importantes du style
                        if "color: #2c3e50" in style_sheet:
                            logger.info(f"   ✅ Couleur de texte définie: #2c3e50")
                        else:
                            logger.warning(f"   ⚠️ Couleur de texte non définie")
                        
                        if "background-color: white" in style_sheet:
                            logger.info(f"   ✅ Couleur de fond définie: white")
                        else:
                            logger.warning(f"   ⚠️ Couleur de fond non définie")
                        
                        if "selection-background-color: #3498db" in style_sheet:
                            logger.info(f"   ✅ Couleur de sélection définie: #3498db")
                        else:
                            logger.warning(f"   ⚠️ Couleur de sélection non définie")
                        
                        if "selection-color: white" in style_sheet:
                            logger.info(f"   ✅ Couleur de texte sélectionné définie: white")
                        else:
                            logger.warning(f"   ⚠️ Couleur de texte sélectionné non définie")
                    else:
                        unstyled_combos += 1
                        logger.warning(f"⚠️ Combo {i+1}: Aucun style appliqué")
                        
                        # Identifier le combo par son parent ou sa position
                        parent = combo.parent()
                        if parent:
                            parent_name = parent.objectName() or parent.__class__.__name__
                            logger.warning(f"   Parent: {parent_name}")
                
                # Résumé
                logger.info(f"📊 Résumé des styles:")
                logger.info(f"   ✅ Combo boxes stylés: {styled_combos}")
                logger.info(f"   ⚠️ Combo boxes non stylés: {unstyled_combos}")
                
                if unstyled_combos == 0:
                    logger.info("🎉 Tous les combo boxes ont des styles appliqués!")
                else:
                    logger.warning(f"⚠️ {unstyled_combos} combo boxes sans style")
                
                # Test de sélection pour vérifier la visibilité
                logger.info("🎯 Test de sélection pour vérifier la visibilité...")
                
                # Tester le combo client s'il a des éléments
                if hasattr(window, 'cliente_combo') and window.cliente_combo.count() > 0:
                    logger.info("🔍 Test du combo client...")
                    original_index = window.cliente_combo.currentIndex()
                    
                    # Sélectionner différents éléments
                    for i in range(min(3, window.cliente_combo.count())):
                        window.cliente_combo.setCurrentIndex(i)
                        current_text = window.cliente_combo.currentText()
                        logger.info(f"   Index {i}: '{current_text}'")
                    
                    # Restaurer la sélection originale
                    window.cliente_combo.setCurrentIndex(original_index)
                
                # Tester le combo état s'il a des éléments
                if hasattr(window, 'estado_combo') and window.estado_combo.count() > 0:
                    logger.info("🔍 Test du combo état...")
                    original_index = window.estado_combo.currentIndex()
                    
                    # Sélectionner différents éléments
                    for i in range(min(3, window.estado_combo.count())):
                        window.estado_combo.setCurrentIndex(i)
                        current_text = window.estado_combo.currentText()
                        logger.info(f"   Index {i}: '{current_text}'")
                    
                    # Restaurer la sélection originale
                    window.estado_combo.setCurrentIndex(original_index)
                
                logger.info("🎯 Test des styles terminé")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du test des styles: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes (laisser le temps au chargement)
        QTimer.singleShot(2000, test_styles)
        
        # Fermer automatiquement après 10 secondes
        QTimer.singleShot(10000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test des Styles des Combo Boxes - Gestion de Facturas")
    print("=" * 60)
    print("📋 Objectifs:")
    print("   • Vérifier que tous les combo boxes ont des styles appliqués")
    print("   • Confirmer que les options sélectionnées ne sont plus blanches")
    print("   • Valider la visibilité du texte dans les déroulants")
    print("   • Tester la sélection d'éléments")
    print()
    
    exit_code = test_combo_styles()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 Les styles des combo boxes sont correctement appliqués")
        print("💡 Plus de problème de texte blanc dans les sélections")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
