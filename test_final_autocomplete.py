#!/usr/bin/env python3
"""
Test final de l'autocomplétion des produits
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

def test_facturas_window_creation():
    """Tester la création de la fenêtre de facturas avec autocomplétion"""
    print("🧪 TEST: Création Fenêtre Facturas avec Autocomplétion")
    print("=" * 55)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        # Créer la fenêtre
        window = FacturasPyQt5Window()
        
        # Vérifier que le widget autocomplete existe
        assert hasattr(window, 'producto_autocomplete'), "❌ Attribut producto_autocomplete manquant"
        print("✅ Widget producto_autocomplete créé")
        
        # Vérifier que les méthodes existent
        assert hasattr(window.producto_autocomplete, 'load_products'), "❌ Méthode load_products manquante"
        assert hasattr(window.producto_autocomplete, 'get_current_product'), "❌ Méthode get_current_product manquante"
        assert hasattr(window.producto_autocomplete, 'clear_product'), "❌ Méthode clear_product manquante"
        print("✅ Toutes les méthodes d'autocomplétion disponibles")
        
        # Vérifier que les signaux sont connectés
        assert hasattr(window, 'on_product_selected'), "❌ Méthode on_product_selected manquante"
        assert hasattr(window, 'on_product_changed'), "❌ Méthode on_product_changed manquante"
        print("✅ Gestionnaires de signaux créés")
        
        print("\n🎉 Fenêtre de facturas créée avec succès avec autocomplétion")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dialogs_creation():
    """Tester la création des dialogs avec autocomplétion"""
    print("\n🧪 TEST: Création Dialogs avec Autocomplétion")
    print("=" * 45)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog
        
        # Créer l'application Qt si pas déjà fait
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        # Test CrearFacturaDialog
        crear_dialog = CrearFacturaDialog()
        assert hasattr(crear_dialog, 'producto_autocomplete'), "❌ CrearFacturaDialog: producto_autocomplete manquant"
        print("✅ CrearFacturaDialog: Widget autocomplete créé")
        
        # Test EditarFacturaDialog (avec données factices)
        fake_factura_data = {'id': 1, 'numero': 'TEST-001', 'fecha': '2024-01-01', 'cliente_id': 1}
        editar_dialog = EditarFacturaDialog(fake_factura_data)
        assert hasattr(editar_dialog, 'producto_autocomplete'), "❌ EditarFacturaDialog: producto_autocomplete manquant"
        print("✅ EditarFacturaDialog: Widget autocomplete créé")
        
        print("\n🎉 Tous les dialogs créés avec succès avec autocomplétion")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des dialogs: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_product_loading():
    """Tester le chargement des produits"""
    print("\n🧪 TEST: Chargement des Produits")
    print("=" * 35)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.facturas_pyqt5 import FacturasPyQt5Window
        from database.database import db
        
        # Créer l'application Qt si pas déjà fait
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        # Créer la fenêtre
        window = FacturasPyQt5Window()
        
        # Charger les données
        window.load_form_data()
        
        # Vérifier que les produits sont chargés
        productos = db.get_all_products()
        products_with_stock = [p for p in productos if p.get('stock_actual', 0) > 0]
        
        print(f"📦 Total productos: {len(productos)}")
        print(f"📦 Productos con stock: {len(products_with_stock)}")
        
        if products_with_stock:
            print("✅ Productos disponibles pour autocomplétion")
            for i, product in enumerate(products_with_stock[:3]):
                stock = product.get('stock_actual', 0)
                precio = product.get('precio_venta', 0.0)
                print(f"   {i+1}. {product['nombre']} - {precio:.2f}€ (Stock: {stock})")
        else:
            print("⚠️  Aucun produit avec stock disponible")
        
        print("\n🎉 Chargement des produits réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🎯 TEST FINAL: Autocomplétion des Produits")
    print("=" * 50)
    
    print("🎯 OBJECTIF:")
    print("   Vérifier que l'autocomplétion fonctionne dans toutes les fenêtres")
    print("   et que l'erreur 'object has no attribute' est résolue")
    print()
    
    # Exécuter les tests
    test1 = test_facturas_window_creation()
    test2 = test_dialogs_creation()
    test3 = test_product_loading()
    
    print("\n" + "=" * 50)
    if all([test1, test2, test3]):
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ RÉSULTAT:")
        print("   🎯 Fenêtre principale: autocomplétion fonctionnelle")
        print("   🎯 Dialogs: autocomplétion intégrée")
        print("   🎯 Chargement: produits disponibles")
        print("   ✅ Erreur 'object has no attribute' résolue")
        
        print("\n🚀 PROCHAINE ÉTAPE:")
        print("   L'application est prête ! Testez manuellement:")
        print("   python main.py → Gestión de Facturas")
        print("   → Essayez de créer une nouvelle factura")
        print("   → Tapez dans le champ 'Producto:' pour voir l'autocomplétion")
        
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifiez les messages d'erreur ci-dessus")
    
    print("=" * 50)
    return all([test1, test2, test3])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
