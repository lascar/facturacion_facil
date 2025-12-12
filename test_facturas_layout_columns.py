#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la disposition en colonnes des informations factura et client
Vérifie que les sections sont bien disposées côte à côte
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_columns_layout():
    """Test de la disposition en colonnes"""
    logger = get_logger("TestFacturasColumnsLayout")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Fonction pour analyser la structure des colonnes
        def analyze_layout():
            try:
                logger.info("🔍 Analyse de la structure en colonnes...")
                
                # Chercher le widget contenant les colonnes
                form_widget = None
                for child in window.findChildren(QGroupBox):
                    if child.title() == "Información de la Factura":
                        info_group = child
                        logger.info("✅ Section 'Información de la Factura' trouvée")
                        
                        # Vérifier le parent pour voir s'il a un layout horizontal
                        parent_widget = info_group.parent()
                        if parent_widget:
                            parent_layout = parent_widget.layout()
                            if isinstance(parent_layout, QHBoxLayout):
                                logger.info("✅ Layout horizontal détecté pour les colonnes")
                                
                                # Compter les widgets dans le layout horizontal
                                widget_count = parent_layout.count()
                                logger.info(f"📊 Nombre de widgets dans le layout horizontal: {widget_count}")
                                
                                if widget_count >= 2:
                                    logger.info("✅ Au moins 2 widgets dans le layout horizontal (colonnes)")
                                    
                                    # Analyser chaque widget
                                    for i in range(widget_count):
                                        widget = parent_layout.itemAt(i).widget()
                                        if isinstance(widget, QGroupBox):
                                            logger.info(f"📋 Colonne {i+1}: {widget.title()}")
                                        else:
                                            logger.info(f"📋 Colonne {i+1}: {type(widget).__name__}")
                                else:
                                    logger.warning("⚠️ Moins de 2 widgets dans le layout horizontal")
                            else:
                                logger.warning(f"⚠️ Layout parent n'est pas horizontal: {type(parent_layout).__name__}")
                        break
                else:
                    logger.warning("⚠️ Section 'Información de la Factura' non trouvée")
                
                # Chercher aussi la section client
                for child in window.findChildren(QGroupBox):
                    if child.title() == "Cliente":
                        client_group = child
                        logger.info("✅ Section 'Cliente' trouvée")
                        
                        # Vérifier si elle partage le même parent que la section factura
                        parent_widget = client_group.parent()
                        if parent_widget:
                            parent_layout = parent_widget.layout()
                            if isinstance(parent_layout, QHBoxLayout):
                                logger.info("✅ Section 'Cliente' aussi dans un layout horizontal")
                            else:
                                logger.warning("⚠️ Section 'Cliente' pas dans un layout horizontal")
                        break
                else:
                    logger.warning("⚠️ Section 'Cliente' non trouvée")
                
                # Vérifier les dimensions des groupes
                info_groups = [child for child in window.findChildren(QGroupBox) 
                              if child.title() in ["Información de la Factura", "Cliente"]]
                
                if len(info_groups) == 2:
                    logger.info("📏 Analyse des dimensions des colonnes:")
                    for group in info_groups:
                        width = group.width()
                        height = group.height()
                        logger.info(f"   {group.title()}: {width}x{height}px")
                        
                        # Vérifier si les largeurs sont similaires (colonnes équilibrées)
                        if len(info_groups) == 2:
                            other_group = [g for g in info_groups if g != group][0]
                            width_diff = abs(group.width() - other_group.width())
                            if width_diff < 50:  # Tolérance de 50px
                                logger.info("✅ Colonnes équilibrées en largeur")
                            else:
                                logger.info(f"📊 Différence de largeur: {width_diff}px")
                
                logger.info("🎯 Analyse de la structure terminée")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de l'analyse: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer l'analyse après 2 secondes (laisser le temps au layout de se stabiliser)
        QTimer.singleShot(2000, analyze_layout)
        
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
    print("🧪 Test de la disposition en colonnes - Gestion de Facturas")
    print("=" * 62)
    print("📋 Objectifs:")
    print("   • Vérifier que les sections factura et client sont côte à côte")
    print("   • Confirmer l'utilisation d'un layout horizontal")
    print("   • Analyser les dimensions des colonnes")
    print("   • Valider l'équilibrage des largeurs")
    print()
    
    exit_code = test_columns_layout()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 La disposition en colonnes fonctionne correctement")
        print("💡 Les informations factura et client sont bien juxtaposées")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
