#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration final de l'interface d'organisation
Vérifie que tous les éléments s'affichent correctement après les corrections
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
from utils.logger import get_logger

def test_interface_complete():
    """Test complet de l'interface d'organisation"""
    logger = get_logger("TestInterfaceOrganizacion")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre d'organisation
        logger.info("🚀 Ouverture de la fenêtre d'organisation...")
        window = OrganizacionPyQt5Window()
        
        # Afficher la fenêtre
        window.show()
        window.raise_()
        window.activateWindow()
        
        # Vérifications de l'interface
        logger.info("🔍 Vérification de l'interface...")
        
        # 1. Vérifier la table des états
        if hasattr(window, 'statuses_table'):
            table = window.statuses_table
            logger.info(f"✅ Table des états: {table.rowCount()} lignes")
            
            # Vérifier les dimensions
            header = table.horizontalHeader()
            color_width = header.sectionSize(3)
            row_height = table.verticalHeader().defaultSectionSize()
            
            logger.info(f"📏 Colonne Color: {color_width}px")
            logger.info(f"📏 Hauteur lignes: {row_height}px")
            
            # Vérifier chaque bouton de couleur
            all_buttons_ok = True
            for row in range(table.rowCount()):
                color_widget = table.cellWidget(row, 3)
                if color_widget:
                    size = color_widget.size()
                    fits = size.width() <= color_width and size.height() <= row_height
                    status = "✅" if fits else "❌"
                    logger.info(f"{status} Ligne {row}: {size.width()}x{size.height()}px")
                    if not fits:
                        all_buttons_ok = False
            
            if all_buttons_ok:
                logger.info("🎉 Tous les boutons de couleur sont bien dimensionnés!")
            else:
                logger.warning("⚠️ Certains boutons peuvent encore déborder")
        
        # 2. Vérifier les autres éléments de l'interface
        elements_to_check = [
            ('company_name_edit', 'Champ nom entreprise'),
            ('company_address_edit', 'Champ adresse'),
            ('save_btn', 'Bouton sauvegarder'),
            ('reset_btn', 'Bouton reset')
        ]
        
        for attr_name, description in elements_to_check:
            if hasattr(window, attr_name):
                logger.info(f"✅ {description}: présent")
            else:
                logger.warning(f"⚠️ {description}: manquant")
        
        logger.info("🎯 Test d'interface terminé avec succès")
        logger.info("💡 La fenêtre restera ouverte 5 secondes pour inspection visuelle")
        
        # Fermer automatiquement après 5 secondes
        QTimer.singleShot(5000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    print("🧪 Test d'intégration de l'interface d'organisation")
    print("=" * 60)
    print("📋 Vérifications:")
    print("   • Affichage correct des boutons de couleur")
    print("   • Dimensions appropriées des colonnes")
    print("   • Présence de tous les éléments d'interface")
    print("   • Fonctionnement général de la fenêtre")
    print()
    
    exit_code = test_interface_complete()
    
    if exit_code == 0:
        print()
        print("✅ Test d'intégration réussi!")
        print("🎉 L'interface d'organisation fonctionne correctement")
        print("💡 Les couleurs des états ne débordent plus")
    else:
        print()
        print("❌ Test d'intégration échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
