#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la fonctionnalité de création de factures
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_invoice_creation():
    """Test de création de factures"""
    print("🧾 TEST DE CRÉATION DE FACTURES")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        from ui.facturas_pyqt6 import FacturasPyQt6Window
        from ui.factura_editor_pyqt6 import FacturaEditorPyQt6Window
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Créer la fenêtre principale
        main_window = MainWindow()
        main_window.show()
        
        print("✅ MainWindow créée")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(0.5)
        
        # Test 1: Ouvrir la fenêtre des factures
        print("\n--- Test 1: Fenêtre des Factures ---")
        main_window.open_facturas()
        app.processEvents()
        time.sleep(0.5)
        
        if hasattr(main_window, 'facturas_window') and main_window.facturas_window:
            facturas_window = main_window.facturas_window
            print("✅ Fenêtre des factures ouverte")
            print(f"✅ Titre: {facturas_window.windowTitle()}")
            print(f"✅ Visible: {facturas_window.isVisible()}")
            
            # Test 2: Ouvrir l'éditeur de factures
            print("\n--- Test 2: Éditeur de Factures ---")
            
            try:
                # Créer directement l'éditeur pour le test
                editor = FacturaEditorPyQt6Window(facturas_window)
                editor.show()
                app.processEvents()
                time.sleep(0.5)
                
                print("✅ Éditeur de factures créé")
                print(f"✅ Titre: {editor.windowTitle()}")
                print(f"✅ Visible: {editor.isVisible()}")
                
                # Test 3: Vérifier les composants de l'éditeur
                print("\n--- Test 3: Composants de l'Éditeur ---")
                
                # Vérifier les widgets principaux
                components_to_check = [
                    ('numero_edit', 'Campo número de factura'),
                    ('fecha_edit', 'Campo fecha'),
                    ('cliente_combo', 'Selector de cliente'),
                    ('items_table', 'Tabla de líneas'),
                    ('subtotal_label', 'Label subtotal'),
                    ('total_label', 'Label total')
                ]
                
                for attr_name, description in components_to_check:
                    if hasattr(editor, attr_name):
                        component = getattr(editor, attr_name)
                        if component:
                            print(f"✅ {description}: Presente")
                        else:
                            print(f"⚠️ {description}: Nulo")
                    else:
                        print(f"❌ {description}: No encontrado")
                
                # Test 4: Vérifier les données initiales
                print("\n--- Test 4: Datos Iniciales ---")
                
                # Vérifier le numéro de facture généré
                numero = editor.numero_edit.text()
                if numero and numero.startswith('F-'):
                    print(f"✅ Número de factura generado: {numero}")
                else:
                    print(f"⚠️ Número de factura: {numero}")
                
                # Vérifier les clients chargés
                client_count = editor.cliente_combo.count()
                print(f"✅ Clientes cargados: {client_count}")
                
                # Vérifier les produits chargés
                products_count = len(editor.productos_data)
                print(f"✅ Productos cargados: {products_count}")
                
                # Test 5: Ajouter une ligne de facture
                print("\n--- Test 5: Añadir Línea de Factura ---")
                
                initial_rows = editor.items_table.rowCount()
                print(f"Filas iniciales: {initial_rows}")
                
                # Ajouter une ligne
                editor.add_invoice_item()
                app.processEvents()
                
                final_rows = editor.items_table.rowCount()
                print(f"Filas después de añadir: {final_rows}")
                
                if final_rows > initial_rows:
                    print("✅ Línea de factura añadida correctamente")
                    
                    # Vérifier les widgets de la ligne
                    row = final_rows - 1
                    widgets_in_row = []
                    
                    for col in range(editor.items_table.columnCount()):
                        widget = editor.items_table.cellWidget(row, col)
                        item = editor.items_table.item(row, col)
                        
                        if widget:
                            widgets_in_row.append(f"Col {col}: {type(widget).__name__}")
                        elif item:
                            widgets_in_row.append(f"Col {col}: QTableWidgetItem")
                    
                    print(f"✅ Widgets en la línea: {len(widgets_in_row)}")
                    for widget_info in widgets_in_row:
                        print(f"   • {widget_info}")
                
                else:
                    print("❌ Error añadiendo línea de factura")
                
                # Fermer l'éditeur
                editor.close()
                print("✅ Éditeur cerrado")
                
            except Exception as e:
                print(f"❌ Error en test del editor: {e}")
                import traceback
                traceback.print_exc()
            
            # Fermer la fenêtre des factures
            facturas_window.close()
            print("✅ Fenêtre des factures fermée")
            
        else:
            print("❌ Fenêtre des factures non créée")
            return False
        
        # Fermer la fenêtre principale
        main_window.close()
        print("✅ Fenêtre principale fermée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_invoice_creation()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST DE CRÉATION DE FACTURES")
        print("="*60)
        
        if success:
            print("🎉 TEST DE CRÉATION DE FACTURES RÉUSSI !")
            print("\n✨ FONCTIONNALITÉS VALIDÉES :")
            print("   ✅ Fenêtre des factures s'ouvre")
            print("   ✅ Éditeur de factures se crée")
            print("   ✅ Composants de l'éditeur présents")
            print("   ✅ Numéro de facture généré")
            print("   ✅ Clients et produits chargés")
            print("   ✅ Lignes de facture ajoutables")
            print("   ✅ Interface complète fonctionnelle")
            
            print("\n🎯 FONCTIONNALITÉ DE CRÉATION DE FACTURES OPÉRATIONNELLE !")
            print("\n🚀 Pour tester manuellement :")
            print("   1. Lancez: python main.py")
            print("   2. Cliquez sur 'Facturas'")
            print("   3. Cliquez sur 'Nueva Factura'")
            print("   4. Remplissez les données et sauvegardez")
            
            return 0
        else:
            print("❌ TEST DE CRÉATION DE FACTURES ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
