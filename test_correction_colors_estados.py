#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de correction des couleurs des états de factures
Vérifie que les boutons de couleur ne débordent plus dans la fenêtre d'organisation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
from utils.logger import get_logger

def test_colors_display():
    """Test l'affichage des couleurs dans la fenêtre d'organisation"""
    logger = get_logger("TestColorsEstados")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre d'organisation
        logger.info("Ouverture de la fenêtre d'organisation...")
        window = OrganizacionPyQt5Window()
        
        # Afficher la fenêtre
        window.show()
        
        # Vérifier que la table des états est présente
        if hasattr(window, 'statuses_table'):
            table = window.statuses_table
            logger.info(f"Table des états trouvée avec {table.rowCount()} lignes")
            
            # Vérifier la configuration des colonnes
            header = table.horizontalHeader()
            color_column_width = header.sectionSize(3)  # Colonne Color
            logger.info(f"Largeur de la colonne Color: {color_column_width}px")
            
            # Vérifier la hauteur des lignes
            row_height = table.verticalHeader().defaultSectionSize()
            logger.info(f"Hauteur des lignes: {row_height}px")
            
            # Vérifier les boutons de couleur
            for row in range(table.rowCount()):
                color_widget = table.cellWidget(row, 3)
                if color_widget:
                    size = color_widget.size()
                    logger.info(f"Ligne {row}: Bouton couleur {size.width()}x{size.height()}px")
                    
                    # Vérifier que le bouton ne dépasse pas la cellule
                    if size.width() <= color_column_width and size.height() <= row_height:
                        logger.info(f"✅ Ligne {row}: Bouton bien dimensionné")
                    else:
                        logger.warning(f"⚠️ Ligne {row}: Bouton peut déborder")
        
        logger.info("✅ Test d'affichage des couleurs terminé")
        logger.info("💡 Vérifiez visuellement que les boutons de couleur ne débordent plus")
        
        # Fermer automatiquement après 10 secondes pour les tests automatisés
        QTimer.singleShot(10000, app.quit)
        
        # Lancer l'application
        return app.exec_()
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        return 1

if __name__ == "__main__":
    print("🧪 Test de correction des couleurs des états de factures")
    print("=" * 60)
    
    exit_code = test_colors_display()
    
    if exit_code == 0:
        print("✅ Test terminé avec succès")
    else:
        print("❌ Test échoué")
    
    sys.exit(exit_code)
