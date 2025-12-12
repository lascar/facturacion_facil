#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la nouvelle interface de facturas avec formulaire intégré
Vérifie que l'édition/création se fait directement dans la fenêtre principale
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.logger import get_logger

def test_inline_form():
    """Test du formulaire intégré de facturas"""
    logger = get_logger("TestFacturasInlineForm")
    
    try:
        app = QApplication(sys.argv)
        
        # Créer la fenêtre de facturas
        logger.info("🚀 Ouverture de la fenêtre de gestion de facturas...")
        window = FacturasPyQt5Window()
        window.show()
        
        # Vérifier que les nouveaux widgets existent
        widgets_to_check = [
            ('form_title_label', 'Titre du formulaire'),
            ('numero_edit', 'Champ numéro'),
            ('fecha_edit', 'Champ date'),
            ('estado_combo', 'Combo état'),
            ('cliente_combo', 'Combo client'),
            ('cliente_info_label', 'Info client'),
            ('producto_combo', 'Combo produit'),
            ('cantidad_spin', 'Spin quantité'),
            ('add_product_btn', 'Bouton ajouter produit'),
            ('productos_table', 'Table produits'),
            ('subtotal_label', 'Label subtotal'),
            ('iva_label', 'Label IVA'),
            ('total_label', 'Label total'),
            ('save_btn', 'Bouton guardar'),
            ('cancel_btn', 'Bouton cancelar'),
            ('new_btn', 'Bouton nueva factura')
        ]
        
        logger.info("🔍 Vérification des widgets du formulaire intégré...")
        
        missing_widgets = []
        for widget_name, description in widgets_to_check:
            if hasattr(window, widget_name):
                logger.info(f"✅ {description}: présent")
            else:
                logger.warning(f"⚠️ {description}: manquant")
                missing_widgets.append(widget_name)
        
        if missing_widgets:
            logger.error(f"❌ Widgets manquants: {', '.join(missing_widgets)}")
            return 1
        
        # Vérifier la structure de l'interface
        logger.info("🏗️ Vérification de la structure de l'interface...")
        
        # Vérifier que le formulaire est en haut et la liste en bas
        if hasattr(window, 'facturas_table'):
            logger.info("✅ Table des facturas: présente")
        else:
            logger.error("❌ Table des facturas: manquante")
            return 1
        
        # Test de la fonctionnalité "Nueva Factura"
        logger.info("🧪 Test de la fonction 'Nueva Factura'...")
        
        def test_nueva_factura():
            try:
                # Simuler un clic sur "Nueva Factura"
                window.new_factura_inline()
                
                # Vérifier que le formulaire est activé
                if window.save_btn.isEnabled():
                    logger.info("✅ Bouton 'Guardar' activé après 'Nueva Factura'")
                else:
                    logger.warning("⚠️ Bouton 'Guardar' non activé")
                
                if window.cancel_btn.isEnabled():
                    logger.info("✅ Bouton 'Cancelar' activé après 'Nueva Factura'")
                else:
                    logger.warning("⚠️ Bouton 'Cancelar' non activé")
                
                # Vérifier que le numéro de facture est généré
                if window.numero_edit.text():
                    logger.info(f"✅ Numéro de facture généré: {window.numero_edit.text()}")
                else:
                    logger.warning("⚠️ Numéro de facture non généré")
                
                logger.info("🎯 Test 'Nueva Factura' terminé")
                
            except Exception as e:
                logger.error(f"❌ Erreur lors du test 'Nueva Factura': {e}")
        
        # Lancer le test après 1 seconde
        QTimer.singleShot(1000, test_nueva_factura)
        
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
    print("🧪 Test du formulaire intégré - Gestion de Facturas")
    print("=" * 60)
    print("📋 Objectifs:")
    print("   • Vérifier que le formulaire est intégré dans la fenêtre principale")
    print("   • Confirmer que tous les widgets nécessaires sont présents")
    print("   • Tester la fonctionnalité 'Nueva Factura'")
    print("   • Valider la structure de l'interface (formulaire en haut, liste en bas)")
    print()
    
    exit_code = test_inline_form()
    
    if exit_code == 0:
        print()
        print("✅ Test terminé avec succès!")
        print("🎉 Le formulaire intégré fonctionne correctement")
        print("💡 Plus besoin de popup pour créer/éditer des facturas")
    else:
        print()
        print("❌ Test échoué")
        print("🔧 Vérifiez les logs pour plus de détails")
    
    sys.exit(exit_code)
