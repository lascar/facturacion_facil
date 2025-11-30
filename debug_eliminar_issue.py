#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug du problème de double dialog eliminar
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from gui import set_gui_framework
from database.database import db
from ui.facturas_pyqt5 import FacturasPyQt5Window

def debug_eliminar_issue():
    """Debug du problème eliminar"""
    
    print("🐛 DEBUG PROBLÈME ELIMINAR")
    print("=" * 40)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre Facturas
        print("🧾 Création de la fenêtre Facturas...")
        facturas_window = FacturasPyQt5Window()
        
        # Patcher les méthodes pour ajouter des logs
        original_eliminar = facturas_window.eliminar_factura
        original_on_selected = facturas_window.on_factura_selected
        original_load_facturas = facturas_window.load_facturas
        original_show_warning = facturas_window.show_warning
        
        call_count = {'eliminar': 0, 'selected': 0, 'load': 0, 'warning': 0}
        
        def debug_eliminar():
            call_count['eliminar'] += 1
            print(f"🗑️ CALL #{call_count['eliminar']} - eliminar_factura()")
            print(f"   selected_factura_id: {facturas_window.selected_factura_id}")
            print(f"   current_row: {facturas_window.facturas_table.currentRow()}")
            print(f"   facturas count: {len(facturas_window.facturas)}")
            
            # Tracer la pile d'appels
            import traceback
            stack = traceback.format_stack()
            print(f"   Stack trace (last 3 calls):")
            for line in stack[-4:-1]:  # Exclure l'appel actuel
                print(f"     {line.strip()}")
            
            return original_eliminar()
        
        def debug_on_selected():
            call_count['selected'] += 1
            current_row = facturas_window.facturas_table.currentRow()
            print(f"📋 CALL #{call_count['selected']} - on_factura_selected()")
            print(f"   current_row: {current_row}")
            print(f"   facturas count: {len(facturas_window.facturas)}")
            
            result = original_on_selected()
            print(f"   selected_factura_id after: {facturas_window.selected_factura_id}")
            return result
        
        def debug_load_facturas():
            call_count['load'] += 1
            print(f"🔄 CALL #{call_count['load']} - load_facturas()")
            print(f"   selected_factura_id before: {facturas_window.selected_factura_id}")
            
            result = original_load_facturas()
            print(f"   facturas count after: {len(facturas_window.facturas)}")
            print(f"   selected_factura_id after: {facturas_window.selected_factura_id}")
            return result
        
        def debug_show_warning(title, message):
            call_count['warning'] += 1
            print(f"⚠️ CALL #{call_count['warning']} - show_warning()")
            print(f"   Title: {title}")
            print(f"   Message: {message}")
            
            # Tracer qui appelle show_warning
            import traceback
            stack = traceback.format_stack()
            print(f"   Called from:")
            for line in stack[-4:-1]:
                print(f"     {line.strip()}")
            
            return original_show_warning(title, message)
        
        # Appliquer les patches
        facturas_window.eliminar_factura = debug_eliminar
        facturas_window.on_factura_selected = debug_on_selected
        facturas_window.load_facturas = debug_load_facturas
        facturas_window.show_warning = debug_show_warning
        
        # Afficher la fenêtre
        facturas_window.show()
        
        print("\n📊 État initial:")
        print(f"   Facturas: {len(facturas_window.facturas)}")
        print(f"   Selected ID: {facturas_window.selected_factura_id}")
        
        if facturas_window.facturas:
            print("\n🎯 Simulation d'une suppression...")
            
            # Sélectionner la première facture
            facturas_window.facturas_table.selectRow(0)
            
            def simulate_delete():
                print("\n🗑️ Simulation du clic Eliminar...")
                
                # Intercepter les dialogs
                from PyQt5.QtWidgets import QMessageBox
                original_question = QMessageBox.question
                
                def mock_question(*args, **kwargs):
                    print("❓ Dialog de confirmation - Réponse: Yes")
                    return QMessageBox.Yes
                
                QMessageBox.question = mock_question
                
                try:
                    # Cliquer sur eliminar
                    facturas_window.eliminar_factura()
                    
                    # Attendre un peu puis vérifier l'état
                    def check_final_state():
                        print(f"\n📊 État final:")
                        print(f"   Facturas: {len(facturas_window.facturas)}")
                        print(f"   Selected ID: {facturas_window.selected_factura_id}")
                        print(f"   Current row: {facturas_window.facturas_table.currentRow()}")
                        
                        print(f"\n📈 Résumé des appels:")
                        print(f"   eliminar_factura: {call_count['eliminar']}")
                        print(f"   on_factura_selected: {call_count['selected']}")
                        print(f"   load_facturas: {call_count['load']}")
                        print(f"   show_warning: {call_count['warning']}")
                        
                        # Fermer après analyse
                        QTimer.singleShot(1000, app.quit)
                    
                    QTimer.singleShot(2000, check_final_state)
                    
                finally:
                    QMessageBox.question = original_question
            
            QTimer.singleShot(1000, simulate_delete)
        else:
            print("⚠️ Aucune facture pour le test")
            QTimer.singleShot(1000, app.quit)
        
        # Démarrer la boucle d'événements
        app.exec_()
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if app:
            app.quit()

if __name__ == "__main__":
    debug_eliminar_issue()
