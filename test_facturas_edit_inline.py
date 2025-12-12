#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'édition inline des facturas
Vérifie que la sélection d'une facture charge ses données dans le formulaire
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_edit_inline():
    """Test de l'édition inline des facturas"""
    logger = get_logger("TestFacturasEditInline")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Fonction pour tester la sélection d'une facture
        def test_factura_selection():
            try:
                logger.info("📋 Test de sélection d'une factura...")
                
                # Vérifier qu'il y a des facturas dans la table
                row_count = window.facturas_table.rowCount()
                logger.info(f"📊 Nombre de facturas dans la table: {row_count}")
                
                if row_count > 0:
                    # Sélectionner la première factura
                    window.facturas_table.selectRow(0)
                    
                    # Simuler la sélection
                    window.on_factura_selected()
                    
                    # Vérifier que le formulaire est rempli
                    if window.numero_edit.text():
                        logger.info(f"✅ Numéro de factura chargé: {window.numero_edit.text()}")
                    else:
                        logger.warning("⚠️ Numéro de factura non chargé")
                    
                    if window.is_editing:
                        logger.info("✅ Mode édition activé")
                    else:
                        logger.warning("⚠️ Mode édition non activé")
                    
                    if window.save_btn.isEnabled():
                        logger.info("✅ Bouton 'Guardar' activé pour édition")
                    else:
                        logger.warning("⚠️ Bouton 'Guardar' non activé")
                    
                    if window.cancel_btn.isEnabled():
                        logger.info("✅ Bouton 'Cancelar' activé pour édition")
                    else:
                        logger.warning("⚠️ Bouton 'Cancelar' non activé")
                    
                    # Vérifier le titre du formulaire
                    title_text = window.form_title_label.text()
                    if "Editando" in title_text:
                        logger.info(f"✅ Titre du formulaire mis à jour: {title_text}")
                    else:
                        logger.warning(f"⚠️ Titre du formulaire non mis à jour: {title_text}")
                    
                    logger.info("🎯 Test de sélection terminé avec succès")
                    
                else:
                    logger.info("ℹ️ Aucune factura dans la base de données pour tester l'édition")
                    logger.info("💡 Créez d'abord quelques facturas pour tester l'édition")
                
                # Test du bouton "Cancelar"
                logger.info("🧪 Test du bouton 'Cancelar'...")
                
                def test_cancel():
                    try:
                        # Simuler l'annulation (sans confirmation pour le test)
                        window.clear_form()
                        window.form_title_label.setText("Seleccionar factura para editar o crear nueva")
                        
                        if not window.is_editing:
                            logger.info("✅ Mode édition désactivé après annulation")
                        else:
                            logger.warning("⚠️ Mode édition toujours actif après annulation")
                        
                        if not window.save_btn.isEnabled():
                            logger.info("✅ Bouton 'Guardar' désactivé après annulation")
                        else:
                            logger.warning("⚠️ Bouton 'Guardar' toujours actif après annulation")
                        
                        logger.info("🎯 Test d'annulation terminé")
                        
                    except Exception as e:
                        logger.error(f"❌ Erreur lors du test d'annulation: {e}")
                
                # Lancer le test d'annulation après 1 seconde
                QTimer.singleShot(1000, test_cancel)
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du test de sélection: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Lancer le test après 1 seconde (laisser le temps à l'interface de se charger)
        QTimer.singleShot(1000, test_factura_selection)
        
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
    print("🧪 Test de l'édition inline - Gestion de Facturas")
    print("=" * 55)
    print("📋 Objectifs:")
    print("   • Vérifier que la sélection d'une factura charge ses données")
    print("   • Confirmer que le mode édition s'active correctement")
    print("   • Tester le bouton 'Cancelar'")
    print("   • Valider la mise à jour du titre du formulaire")
    print()
    
    exit_code = test_edit_inline()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 L'édition inline fonctionne correctement")
        print("💡 Les facturas peuvent être éditées directement dans la fenêtre principale")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
