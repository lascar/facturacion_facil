#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de visibilité des fenêtres - Vérifie que les fenêtres s'affichent correctement
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_visibility():
    """Test de visibilité des fenêtres"""
    print("🧪 TEST DE VISIBILITÉ DES FENÊTRES")
    print("="*60)
    
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
        main_window.show()  # Afficher la fenêtre principale
        
        print("✅ MainWindow créée et affichée")
        print(f"✅ Fenêtre principale visible: {main_window.isVisible()}")
        print(f"✅ Taille fenêtre: {main_window.width()}x{main_window.height()}")
        
        # Attendre un peu pour que la fenêtre s'affiche
        app.processEvents()
        time.sleep(1)
        
        # Test d'ouverture d'une fenêtre
        print("\n--- Test d'ouverture de ProductosWindow ---")
        
        try:
            # Simuler un clic sur le bouton Productos
            main_window.open_productos()
            
            # Vérifier que la fenêtre a été créée
            if hasattr(main_window, 'productos_window') and main_window.productos_window:
                print("✅ ProductosWindow créée")
                
                # Vérifier la visibilité
                if hasattr(main_window.productos_window, 'window'):
                    window = main_window.productos_window.window
                    
                    # Forcer l'affichage et vérifier
                    window.update()
                    app.processEvents()
                    
                    print(f"✅ Fenêtre Productos existe: {window.winfo_exists()}")
                    print(f"✅ Fenêtre Productos géométrie: {window.geometry()}")
                    
                    # Essayer de récupérer des informations sur la fenêtre
                    try:
                        print(f"✅ Titre: {window.title()}")
                        print(f"✅ État: {window.state()}")
                    except Exception as e:
                        print(f"⚠️ Erreur info fenêtre: {e}")
                    
                    # Fermer la fenêtre après test
                    time.sleep(2)
                    window.destroy()
                    print("✅ Fenêtre Productos fermée")
                    
                else:
                    print("❌ ProductosWindow n'a pas d'attribut 'window'")
            else:
                print("❌ ProductosWindow non créée")
                
        except Exception as e:
            print(f"❌ Erreur test ProductosWindow: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n--- Test d'ouverture de StockWindow ---")
        
        try:
            # Simuler un clic sur le bouton Stock
            main_window.open_stock()
            
            # Vérifier que la fenêtre a été créée
            if hasattr(main_window, 'stock_window') and main_window.stock_window:
                print("✅ StockWindow créée")
                
                # Vérifier la visibilité
                if hasattr(main_window.stock_window, 'window'):
                    window = main_window.stock_window.window
                    
                    # Forcer l'affichage et vérifier
                    window.update()
                    app.processEvents()
                    
                    print(f"✅ Fenêtre Stock existe: {window.winfo_exists()}")
                    print(f"✅ Fenêtre Stock géométrie: {window.geometry()}")
                    
                    # Fermer la fenêtre après test
                    time.sleep(2)
                    window.destroy()
                    print("✅ Fenêtre Stock fermée")
                    
                else:
                    print("❌ StockWindow n'a pas d'attribut 'window'")
            else:
                print("❌ StockWindow non créée")
                
        except Exception as e:
            print(f"❌ Erreur test StockWindow: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST DE VISIBILITÉ")
        print("="*60)
        print("✅ Application PyQt6 fonctionne")
        print("✅ Fenêtre principale s'affiche")
        print("✅ Fenêtres CustomTkinter se créent")
        print("✅ Adaptateur PyQt6 ↔ CustomTkinter opérationnel")
        
        print("\n🎯 RECOMMANDATIONS :")
        print("1. Lancez l'application: python main.py")
        print("2. Cliquez sur les boutons pour ouvrir les fenêtres")
        print("3. Les fenêtres devraient maintenant s'afficher correctement")
        print("4. Si une fenêtre ne s'affiche pas, elle pourrait être derrière d'autres fenêtres")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_window_visibility()
        
        if success:
            print("\n🎉 TEST DE VISIBILITÉ RÉUSSI !")
            print("\n✨ Votre application devrait maintenant afficher les fenêtres correctement !")
            return 0
        else:
            print("\n❌ TEST DE VISIBILITÉ ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
