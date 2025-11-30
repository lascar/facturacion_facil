#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de debug pour le problème du bouton Eliminar
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from gui import set_gui_framework
from database.database import db
from ui.facturas_pyqt5 import FacturasPyQt5Window
import logging

def test_eliminar_debug():
    """Test de debug pour le bouton Eliminar"""
    
    print("🐛 TEST DEBUG BOUTON ELIMINAR")
    print("=" * 40)
    
    # Configurer le logging pour voir les détails
    logging.basicConfig(level=logging.DEBUG)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre Facturas
        print("🧾 Création de la fenêtre Facturas...")
        facturas_window = FacturasPyQt5Window()
        facturas_window.show()
        
        # Charger les factures
        facturas_window.load_facturas()
        
        # Vérifier s'il y a des factures
        if not facturas_window.facturas:
            print("⚠️  Aucune facture trouvée pour le test")
            return
        
        print(f"📊 {len(facturas_window.facturas)} factures trouvées")
        
        # Simuler la sélection de la première facture
        print("🎯 Sélection de la première facture...")
        facturas_window.facturas_table.selectRow(0)
        
        # Vérifier que la sélection fonctionne
        if facturas_window.selected_factura_id:
            print(f"✅ Facture sélectionnée: ID {facturas_window.selected_factura_id}")
            
            # Simuler un clic sur le bouton Eliminar après un délai
            def simulate_eliminar():
                print("🗑️ Simulation du clic sur Eliminar...")
                
                # Intercepter les QMessageBox pour automatiser la réponse
                original_question = QMessageBox.question
                def mock_question(*args, **kwargs):
                    print("❓ Dialog de confirmation intercepté - Réponse: Yes")
                    return QMessageBox.Yes
                
                QMessageBox.question = mock_question
                
                try:
                    # Cliquer sur le bouton
                    facturas_window.eliminar_factura()
                    print("✅ Méthode eliminar_factura exécutée")
                except Exception as e:
                    print(f"❌ Erreur lors de l'exécution: {e}")
                    import traceback
                    traceback.print_exc()
                finally:
                    # Restaurer la méthode originale
                    QMessageBox.question = original_question
                
                # Fermer l'application après le test
                QTimer.singleShot(1000, app.quit)
            
            # Programmer l'exécution du test
            QTimer.singleShot(500, simulate_eliminar)
            
        else:
            print("❌ Aucune facture sélectionnée")
            app.quit()
            return
        
        # Démarrer la boucle d'événements
        print("🚀 Démarrage du test...")
        app.exec_()
        
        print("🏁 Test terminé")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if app:
            app.quit()

if __name__ == "__main__":
    test_eliminar_debug()
