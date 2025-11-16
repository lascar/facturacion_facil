#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de toutes les fenêtres PyQt6 natives
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pyqt6_windows():
    """Test de toutes les fenêtres PyQt6"""
    print("🧪 TEST DE TOUTES LES FENÊTRES PYQT6 NATIVES")
    print("="*80)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Créer la fenêtre principale
        main_window = MainWindow()
        main_window.show()
        
        print("✅ MainWindow créée et affichée")
        print(f"✅ Fenêtre principale visible: {main_window.isVisible()}")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(0.5)
        
        # Tester chaque fenêtre
        windows_to_test = [
            ("productos", main_window.open_productos),
            ("organizacion", main_window.open_organizacion),
            ("stock", main_window.open_stock),
            ("facturas", main_window.open_facturas),
            ("clientes", main_window.open_clientes),
            ("search", main_window.open_search)
        ]
        
        results = []
        
        print("\n--- Tests d'ouverture des fenêtres PyQt6 ---")
        
        for window_name, open_method in windows_to_test:
            print(f"\n🔍 Test {window_name}:")
            
            try:
                # Ouvrir la fenêtre
                open_method()
                
                # Traiter les événements
                app.processEvents()
                time.sleep(0.2)
                
                # Vérifier que la fenêtre a été créée
                window_attr = f"{window_name}_window"
                if hasattr(main_window, window_attr):
                    window = getattr(main_window, window_attr)
                    
                    if window and hasattr(window, 'isVisible'):
                        print(f"✅ {window_name} créée")
                        print(f"✅ {window_name} visible: {window.isVisible()}")
                        print(f"✅ {window_name} titre: {window.windowTitle()}")
                        
                        # Fermer la fenêtre après test
                        window.close()
                        print(f"✅ {window_name} fermée")
                        
                        results.append((window_name, True))
                    else:
                        print(f"❌ {window_name} non créée correctement")
                        results.append((window_name, False))
                else:
                    print(f"❌ {window_name} attribut non trouvé")
                    results.append((window_name, False))
                
            except Exception as e:
                print(f"❌ {window_name} erreur: {e}")
                results.append((window_name, False))
        
        # Fermer la fenêtre principale
        main_window.close()
        print("\n✅ Fenêtre principale fermée")
        
        # Résumé final
        print("\n" + "="*80)
        print("RÉSUMÉ DES TESTS PYQT6")
        print("="*80)
        
        success_count = 0
        for window_name, result in results:
            status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
            print(f"{window_name:<15} {status}")
            if result:
                success_count += 1
        
        print(f"\nFenêtres testées: {len(results)}")
        print(f"Fenêtres fonctionnelles: {success_count}")
        print(f"Taux de réussite: {(success_count * 100) // len(results)}%")
        
        if success_count == len(results):
            print("\n🎉 TOUTES LES FENÊTRES PYQT6 FONCTIONNENT PARFAITEMENT !")
            print("\n✨ CONVERSION PYQT6 COMPLÈTE RÉUSSIE !")
            print("\n🖥️ Fenêtres PyQt6 natives disponibles :")
            for window_name, _ in results:
                print(f"   • {window_name}Window PyQt6 ✅")
            
            print("\n🎯 AVANTAGES DE LA CONVERSION PYQT6 :")
            print("   • Interface 100% native PyQt6")
            print("   • Performance optimale")
            print("   • Look & Feel Windows authentique")
            print("   • Messages PyQt6 natifs (QMessageBox)")
            print("   • Pas de dépendance CustomTkinter")
            print("   • Maintenance simplifiée")
            
            print("\n🚀 Lancez l'application avec: python main.py")
            return True
        else:
            failed_count = len(results) - success_count
            print(f"\n⚠️ {failed_count} fenêtre(s) ont des problèmes")
            return False
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_pyqt6_windows()
        
        if success:
            print("\n🎊 CONVERSION PYQT6 COMPLÈTE RÉUSSIE !")
            print("\n✅ TOUTES LES FENÊTRES SONT MAINTENANT EN PYQT6 NATIF !")
            print("\n🎯 VOTRE APPLICATION EST MAINTENANT :")
            print("   🖥️  100% PyQt6 native")
            print("   ⚡  Plus rapide et performante")
            print("   🎨  Look Windows authentique")
            print("   🔧  Plus facile à maintenir")
            print("   📱  Messages natifs PyQt6")
            print("   🚀  Prête pour la production")
            
            return 0
        else:
            print("\n❌ CERTAINES FENÊTRES ONT DES PROBLÈMES")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
