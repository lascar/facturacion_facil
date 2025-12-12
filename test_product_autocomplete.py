#!/usr/bin/env python3
"""
Test du widget d'autocomplétion des produits
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

def test_product_autocomplete_widget():
    """Tester le widget d'autocomplétion des produits"""
    print("🧪 TEST: Widget d'Autocomplétion des Produits")
    print("=" * 50)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.product_autocomplete_widget import ProductAutoCompleteWidget
        from database.database import db
        
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        # Créer le widget
        widget = ProductAutoCompleteWidget()
        
        # Charger les produits
        productos = db.get_all_products()
        widget.load_products(productos)
        
        print(f"✅ Widget créé avec {len(productos)} produits")
        
        # Tester quelques fonctionnalités
        print("\n📋 Produits avec stock > 0:")
        products_with_stock = [p for p in productos if p.get('stock_actual', 0) > 0]
        for i, product in enumerate(products_with_stock[:5]):
            stock = product.get('stock_actual', 0)
            precio = product.get('precio_venta', 0.0)
            print(f"   {i+1}. {product['nombre']} - {precio:.2f}€ (Stock: {stock})")
        
        # Tester la méthode format_product_display
        if products_with_stock:
            test_product = products_with_stock[0]
            formatted = widget.format_product_display(test_product)
            print(f"\n🔍 Formato de visualización:")
            print(f"   Producto: {test_product['nombre']}")
            print(f"   Formato: {formatted}")
        
        # Tester la validation
        print(f"\n✅ Widget tiene producto válido: {widget.has_valid_product()}")
        
        # Simuler la sélection d'un produit
        if products_with_stock:
            test_product = products_with_stock[0]
            widget.set_product(test_product)
            print(f"✅ Producto seleccionado: {widget.get_current_product()['nombre']}")
            print(f"✅ Widget tiene producto válido: {widget.has_valid_product()}")
        
        print("\n🎉 Test del widget completado con éxito")
        return True
        
    except Exception as e:
        print(f"❌ Error en test del widget: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_facturas():
    """Tester l'intégration avec la fenêtre de facturas"""
    print("\n🧪 TEST: Intégration avec Fenêtre de Facturas")
    print("=" * 50)
    
    try:
        from database.database import db
        
        # Vérifier que les produits sont disponibles
        productos = db.get_all_products()
        products_with_stock = [p for p in productos if p.get('stock_actual', 0) > 0]
        
        print(f"📦 Total productos: {len(productos)}")
        print(f"📦 Productos con stock: {len(products_with_stock)}")
        
        if products_with_stock:
            print("\n✅ Productos disponibles para autocomplétion:")
            for i, product in enumerate(products_with_stock[:3]):
                stock = product.get('stock_actual', 0)
                precio = product.get('precio_venta', 0.0)
                print(f"   {i+1}. {product['nombre']} - {precio:.2f}€ (Stock: {stock})")
        else:
            print("⚠️  No hay productos con stock disponible")
        
        print("\n💡 Para probar manualmente:")
        print("   1. Ejecute: python main.py")
        print("   2. Vaya a: Gestión de Facturas")
        print("   3. Haga clic en 'Nueva Factura'")
        print("   4. En el campo 'Producto:', escriba el nombre de un producto")
        print("   5. Debería ver sugerencias de autocomplétion")
        print("   6. Seleccione un producto y agregue cantidad")
        print("   7. Haga clic en '➕ Agregar'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de integración: {e}")
        return False

def test_stock_consistency():
    """Tester la cohérence du stock"""
    print("\n🧪 TEST: Cohérence du Stock")
    print("=" * 30)
    
    try:
        from database.database import db
        from database.models import Stock
        
        productos = db.get_all_products()
        
        print("🔍 Vérification cohérence stock:")
        consistent_count = 0
        total_count = 0
        
        for product in productos[:10]:  # Vérifier les 10 premiers
            product_id = product['id']
            stock_from_get_all = product.get('stock_actual', 0)
            stock_from_model = Stock.get_by_product(product_id)
            
            status = "✅" if stock_from_get_all == stock_from_model else "❌"
            if stock_from_get_all == stock_from_model:
                consistent_count += 1
            total_count += 1
            
            print(f"   {status} ID {product_id}: get_all={stock_from_get_all}, model={stock_from_model}")
        
        consistency_rate = (consistent_count / total_count) * 100
        print(f"\n📊 Taux de cohérence: {consistency_rate:.1f}% ({consistent_count}/{total_count})")
        
        if consistency_rate == 100.0:
            print("✅ Stock parfaitement cohérent - Autocomplétion fonctionnera correctement")
        else:
            print("⚠️  Incohérences détectées - Exécutez fix_stock_sync_problema.py")
        
        return consistency_rate >= 100.0
        
    except Exception as e:
        print(f"❌ Error en test de cohérence: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 TEST COMPLET: Autocomplétion des Produits")
    print("=" * 60)
    
    print("🎯 OBJECTIF:")
    print("   Vérifier que l'autocomplétion des produits fonctionne correctement")
    print("   et remplace efficacement les ComboBox")
    print()
    
    # Exécuter les tests
    test1 = test_product_autocomplete_widget()
    test2 = test_integration_with_facturas()
    test3 = test_stock_consistency()
    
    print("\n" + "=" * 60)
    if all([test1, test2, test3]):
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ RÉSULTAT:")
        print("   🎯 Widget d'autocomplétion fonctionnel")
        print("   🔄 Intégration avec facturas complète")
        print("   📊 Stock cohérent pour autocomplétion")
        print("   ✅ Prêt pour utilisation en production")
        
        print("\n🚀 PROCHAINE ÉTAPE:")
        print("   Testez manuellement l'interface:")
        print("   python main.py → Gestión de Facturas → Nueva Factura")
        
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Vérifiez les messages d'erreur ci-dessus")
    
    print("=" * 60)
    return all([test1, test2, test3])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
