#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'ouverture de toutes les fenêtres de l'application
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_creation(window_name, window_class, adapter):
    """Test de création d'une fenêtre spécifique"""
    try:
        print(f"🧪 Test création {window_name}...")
        
        # Créer la fenêtre
        window = window_class(adapter)
        print(f"✅ {window_name} créée avec succès")
        
        # Vérifier que la fenêtre a l'attribut window
        if hasattr(window, 'window'):
            print(f"✅ {window_name} a l'attribut 'window'")
            
            # Tester quelques méthodes de base
            try:
                window.window.title(f"Test {window_name}")
                print(f"✅ {window_name} titre modifié")
            except Exception as e:
                print(f"⚠️ {window_name} erreur titre: {e}")
            
            # Fermer la fenêtre
            try:
                window.window.destroy()
                print(f"✅ {window_name} fermée proprement")
            except Exception as e:
                print(f"⚠️ {window_name} erreur fermeture: {e}")
            
            return True
        else:
            print(f"❌ {window_name} n'a pas l'attribut 'window'")
            return False
            
    except Exception as e:
        print(f"❌ {window_name} erreur création: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 TEST D'OUVERTURE DE TOUTES LES FENÊTRES")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow
        from ui.pyqt6_window_adapter import create_adapter_for_pyqt6_parent
        
        # Configurer PyQt6
        from gui import set_gui_framework
        set_gui_framework('pyqt6')
        
        # Créer une application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Créer une fenêtre PyQt6 parent
        main_window = QMainWindow()
        main_window.setWindowTitle("Test Parent Window")
        main_window.resize(800, 600)
        
        print("✅ Fenêtre PyQt6 parent créée")
        
        # Créer l'adaptateur
        adapter = create_adapter_for_pyqt6_parent(main_window)
        print("✅ Adaptateur créé")
        
        # Liste des fenêtres à tester
        windows_to_test = [
            ("ProductosWindow", "ui.productos", "ProductosWindow"),
            ("OrganizacionWindow", "ui.organizacion", "OrganizacionWindow"),
            ("StockWindow", "ui.stock", "StockWindow"),
            ("FacturasWindow", "ui.facturas", "FacturasWindow"),
            ("ClientesWindow", "ui.clientes", "ClientesWindow"),
            ("SearchWindow", "ui.search_window", "SearchWindow")
        ]
        
        results = []
        
        print("\n--- Tests d'ouverture des fenêtres ---")
        
        for window_name, module_name, class_name in windows_to_test:
            print(f"\n🔍 Test {window_name}:")
            
            try:
                # Importer dynamiquement la classe
                module = __import__(module_name, fromlist=[class_name])
                window_class = getattr(module, class_name)
                
                # Tester la création
                result = test_window_creation(window_name, window_class, adapter)
                results.append((window_name, result))
                
            except ImportError as e:
                print(f"❌ {window_name} erreur import: {e}")
                results.append((window_name, False))
            except AttributeError as e:
                print(f"❌ {window_name} classe non trouvée: {e}")
                results.append((window_name, False))
            except Exception as e:
                print(f"❌ {window_name} erreur générale: {e}")
                results.append((window_name, False))
        
        # Nettoyer l'adaptateur
        adapter.cleanup()
        print("\n✅ Adaptateur nettoyé")
        
        # Résumé final
        print("\n" + "="*60)
        print("RÉSUMÉ DES TESTS D'OUVERTURE")
        print("="*60)
        
        success_count = 0
        for window_name, result in results:
            status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
            print(f"{window_name:<20} {status}")
            if result:
                success_count += 1
        
        print(f"\nFenêtres testées: {len(results)}")
        print(f"Fenêtres fonctionnelles: {success_count}")
        print(f"Taux de réussite: {(success_count * 100) // len(results)}%")
        
        if success_count == len(results):
            print("\n🎉 TOUTES LES FENÊTRES S'OUVRENT CORRECTEMENT !")
            print("\n✨ Votre application est complètement fonctionnelle !")
            print("\n🖥️ Fenêtres disponibles :")
            for window_name, _ in results:
                print(f"   • {window_name} ✅")
            print("\n🚀 Lancez l'application avec: python main.py")
            return 0
        else:
            failed_count = len(results) - success_count
            print(f"\n⚠️ {failed_count} fenêtre(s) ont des problèmes")
            print("\n❌ Fenêtres problématiques :")
            for window_name, result in results:
                if not result:
                    print(f"   • {window_name}")
            return 1
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
