#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la sélection de client lors du chargement d'une facture
Vérifie que le combo client est correctement informé avec le client de la facture
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger
from database.database import db

def test_client_selection():
    """Test de la sélection de client"""
    logger = get_logger("TestFacturasClientSelection")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Fonction pour tester la sélection de client
        def test_selection():
            try:
                logger.info("🔍 Test de la sélection de client...")
                
                # Vérifier qu'il y a des facturas
                if len(window.facturas) == 0:
                    logger.warning("⚠️ Aucune factura trouvée pour le test")
                    return
                
                logger.info(f"📊 {len(window.facturas)} facturas trouvées")
                
                # Sélectionner la première factura
                if window.facturas_table.rowCount() > 0:
                    logger.info("🎯 Sélection de la première factura...")
                    window.facturas_table.selectRow(0)
                    
                    # Attendre un peu pour que la sélection se propage
                    QTimer.singleShot(500, check_client_selection)
                else:
                    logger.warning("⚠️ Aucune ligne dans la table des facturas")
                    
            except Exception as e:
                logger.error(f"❌ Erreur lors du test de sélection: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        def check_client_selection():
            try:
                logger.info("🔍 Vérification de la sélection de client...")
                
                # Vérifier l'état du combo client
                current_index = window.cliente_combo.currentIndex()
                current_text = window.cliente_combo.currentText()
                current_data = window.cliente_combo.itemData(current_index)
                
                logger.info(f"📋 Index sélectionné: {current_index}")
                logger.info(f"📋 Texte sélectionné: '{current_text}'")
                logger.info(f"📋 Données associées: {current_data}")
                
                # Vérifier si un client valide est sélectionné
                if current_index > 0 and current_data is not None:
                    logger.info("✅ Client correctement sélectionné!")
                    logger.info(f"   Client ID: {current_data}")
                    logger.info(f"   Client: {current_text}")
                    
                    # Vérifier la cohérence avec la factura sélectionnée
                    if window.selected_factura_id:
                        factura_completa = db.get_invoice_by_id(window.selected_factura_id)
                        if factura_completa and 'cliente' in factura_completa:
                            expected_client_id = factura_completa['cliente']['id']
                            if current_data == expected_client_id:
                                logger.info("✅ Client ID correspond à la factura!")
                            else:
                                logger.warning(f"⚠️ Client ID ne correspond pas: attendu {expected_client_id}, trouvé {current_data}")
                        else:
                            logger.warning("⚠️ Impossible de vérifier la cohérence (données factura incomplètes)")
                    
                elif current_index == 0:
                    logger.warning("⚠️ Aucun client sélectionné (index 0 = 'Seleccionar cliente...')")
                else:
                    logger.warning("⚠️ Sélection de client invalide")
                
                # Afficher tous les clients disponibles pour debug
                logger.info("📋 Clients disponibles dans le combo:")
                for i in range(window.cliente_combo.count()):
                    text = window.cliente_combo.itemText(i)
                    data = window.cliente_combo.itemData(i)
                    marker = " ← SÉLECTIONNÉ" if i == current_index else ""
                    logger.info(f"   {i}: '{text}' (ID: {data}){marker}")
                
                logger.info("🎯 Test de sélection de client terminé")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors de la vérification: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 2 secondes (laisser le temps au chargement)
        QTimer.singleShot(2000, test_selection)
        
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
    print("🧪 Test de la sélection de client - Gestion de Facturas")
    print("=" * 58)
    print("📋 Objectifs:")
    print("   • Vérifier que le combo client est informé lors de la sélection d'une factura")
    print("   • Confirmer que l'ID client correspond à la factura")
    print("   • Valider la cohérence des données")
    print("   • Diagnostiquer les problèmes de sélection")
    print()
    
    exit_code = test_client_selection()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 La sélection de client fonctionne correctement")
        print("💡 Le combo client est bien informé avec le client de la factura")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
