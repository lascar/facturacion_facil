#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour vérifier que le problème du double dialog est résolu
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from gui import set_gui_framework
from database.database import db
from ui.facturas_pyqt5 import FacturasPyQt5Window

def test_eliminar_no_double_dialog():
    """Test pour s'assurer qu'il n'y a pas de double dialog"""
    
    print("🧪 TEST ELIMINAR - PAS DE DOUBLE DIALOG")
    print("=" * 50)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre Facturas
        print("🧾 Création de la fenêtre Facturas...")
        facturas_window = FacturasPyQt5Window()
        
        # Compter les appels aux dialogs
        dialog_calls = {'warning': 0, 'info': 0, 'question': 0}
        
        # Patcher les méthodes de dialog
        original_show_warning = facturas_window.show_warning
        original_show_info = facturas_window.show_info
        original_question = QMessageBox.question
        
        def count_warning(title, message):
            dialog_calls['warning'] += 1
            print(f"⚠️ WARNING DIALOG #{dialog_calls['warning']}: {title} - {message}")
            return original_show_warning(title, message)
        
        def count_info(title, message):
            dialog_calls['info'] += 1
            print(f"ℹ️ INFO DIALOG #{dialog_calls['info']}: {title} - {message}")
            return original_show_info(title, message)
        
        def count_question(*args, **kwargs):
            dialog_calls['question'] += 1
            print(f"❓ QUESTION DIALOG #{dialog_calls['question']}")
            return QMessageBox.Yes  # Toujours confirmer
        
        # Appliquer les patches
        facturas_window.show_warning = count_warning
        facturas_window.show_info = count_info
        QMessageBox.question = count_question
        
        # Afficher la fenêtre
        facturas_window.show()
        
        print(f"\n📊 État initial:")
        print(f"   Facturas: {len(facturas_window.facturas)}")
        print(f"   Selected ID: {facturas_window.selected_factura_id}")
        
        if facturas_window.facturas:
            print("\n🎯 Test de suppression avec protection...")
            
            # Sélectionner la première facture
            facturas_window.facturas_table.selectRow(0)
            
            def test_sequence():
                print("\n🗑️ ÉTAPE 1: Premier clic Eliminar...")
                
                # Premier clic
                facturas_window.eliminar_factura()
                
                def test_rapid_clicks():
                    print("\n🗑️ ÉTAPE 2: Clics rapides multiples (doivent être ignorés)...")
                    
                    # Essayer plusieurs clics rapides
                    for i in range(5):
                        print(f"   Clic #{i+1}...")
                        facturas_window.eliminar_factura()
                    
                    def final_check():
                        print(f"\n📊 RÉSULTATS FINAUX:")
                        print(f"   Dialogs WARNING: {dialog_calls['warning']}")
                        print(f"   Dialogs INFO: {dialog_calls['info']}")
                        print(f"   Dialogs QUESTION: {dialog_calls['question']}")
                        
                        # Vérifications
                        if dialog_calls['warning'] == 0:
                            print("✅ SUCCÈS: Aucun dialog 'Seleccione una factura'")
                        else:
                            print("❌ ÉCHEC: Dialog 'Seleccione una factura' apparu")
                        
                        if dialog_calls['question'] == 1:
                            print("✅ SUCCÈS: Un seul dialog de confirmation")
                        else:
                            print(f"❌ ÉCHEC: {dialog_calls['question']} dialogs de confirmation")
                        
                        if dialog_calls['info'] == 1:
                            print("✅ SUCCÈS: Un seul dialog de succès")
                        else:
                            print(f"❌ ÉCHEC: {dialog_calls['info']} dialogs de succès")
                        
                        # Test final: essayer de cliquer quand aucune facture n'est sélectionnée
                        print(f"\n🎯 ÉTAPE 3: Test sans sélection...")
                        facturas_window.selected_factura_id = None
                        facturas_window.eliminar_factura()
                        
                        def final_final_check():
                            print(f"\n📊 RÉSULTATS APRÈS TEST SANS SÉLECTION:")
                            print(f"   Dialogs WARNING: {dialog_calls['warning']}")
                            
                            if dialog_calls['warning'] == 1:
                                print("✅ SUCCÈS: Un seul warning pour sélection manquante")
                            else:
                                print(f"❌ ÉCHEC: {dialog_calls['warning']} warnings")
                            
                            print("\n🎉 TEST TERMINÉ")
                            QTimer.singleShot(500, app.quit)
                        
                        QTimer.singleShot(1000, final_final_check)
                    
                    QTimer.singleShot(2000, final_check)
                
                QTimer.singleShot(500, test_rapid_clicks)
            
            QTimer.singleShot(1000, test_sequence)
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
    test_eliminar_no_double_dialog()
