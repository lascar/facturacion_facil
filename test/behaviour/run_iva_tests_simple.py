#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour tester l'IVA modifiable sans pytest
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.facturas_pyqt5 import FacturasPyQt5Window
from database.database import Database
from services.producto_service import ProductoService
from services.cliente_service import ClienteService

def test_iva_column_exists():
    """Test que la colonne IVA % existe"""
    print("\n🧪 Test 1: Vérification colonne IVA %")
    print("=" * 70)
    
    app = QApplication(sys.argv)
    window = FacturasPyQt5Window()
    
    # Vérifier les en-têtes
    table = window.productos_table
    headers = []
    for col in range(table.columnCount()):
        header_item = table.horizontalHeaderItem(col)
        if header_item:
            headers.append(header_item.text())
    
    print(f"En-têtes trouvés: {headers}")
    
    expected_order = ["Producto", "Cantidad", "Precio Unit.", "IVA %", "Total", "Acciones"]
    
    if headers == expected_order:
        print("✅ Test réussi: Colonne IVA % présente et dans le bon ordre")
        return True
    else:
        print(f"❌ Test échoué: Ordre incorrect")
        print(f"   Attendu: {expected_order}")
        print(f"   Obtenu: {headers}")
        return False

def test_iva_recomendado_applied():
    """Test que l'IVA recommandé est appliqué par défaut"""
    print("\n🧪 Test 2: IVA recommandé appliqué par défaut")
    print("=" * 70)
    
    app = QApplication(sys.argv)
    window = FacturasPyQt5Window()
    
    # Obtenir un produit
    productos = window.producto_service.get_all_productos()
    if not productos:
        print("⚠️  Aucun produit disponible, test ignoré")
        return True
    
    # Trouver un produit avec IVA != 21%
    producto_test = None
    for p in productos:
        iva = p.get('iva_recomendado', 21.0)
        if iva != 21.0:
            producto_test = p
            break
    
    if not producto_test:
        producto_test = productos[0]
        print(f"⚠️  Aucun produit avec IVA != 21%, utilisation du premier")
    
    iva_expected = producto_test.get('iva_recomendado', 21.0)
    print(f"Produit: {producto_test['nombre']}")
    print(f"IVA recommandé: {iva_expected}%")
    
    # Ajouter le produit
    window.producto_autocomplete.set_product(producto_test)
    window.cantidad_spin.setValue(2)
    window.add_product_to_invoice()
    
    # Vérifier l'IVA dans la table
    table = window.productos_table
    if table.rowCount() == 0:
        print("❌ Test échoué: Produit non ajouté")
        return False
    
    iva_item = table.item(0, 3)
    if not iva_item:
        print("❌ Test échoué: Cellule IVA manquante")
        return False
    
    iva_text = iva_item.text()
    iva_value = float(iva_text.replace('%', '').strip())
    
    print(f"IVA dans la table: {iva_value}%")
    
    if abs(iva_value - iva_expected) < 0.1:
        print("✅ Test réussi: IVA recommandé appliqué correctement")
        return True
    else:
        print(f"❌ Test échoué: IVA incorrect")
        print(f"   Attendu: {iva_expected}%")
        print(f"   Obtenu: {iva_value}%")
        return False

def test_totals_calculated_correctly():
    """Test que les totaux sont calculés correctement"""
    print("\n🧪 Test 3: Calcul des totaux avec IVA individuel")
    print("=" * 70)
    
    app = QApplication(sys.argv)
    window = FacturasPyQt5Window()
    
    # Obtenir des produits
    productos = window.producto_service.get_all_productos()
    if len(productos) < 2:
        print("⚠️  Pas assez de produits, test ignoré")
        return True
    
    # Ajouter 2 produits
    for i, producto in enumerate(productos[:2]):
        print(f"Ajout produit {i+1}: {producto['nombre']} - IVA: {producto.get('iva_recomendado', 21)}%")
        window.producto_autocomplete.set_product(producto)
        window.cantidad_spin.setValue(1)
        window.add_product_to_invoice()
    
    # Calculer le total attendu
    table = window.productos_table
    subtotal_expected = 0.0
    iva_expected = 0.0
    
    for row in range(table.rowCount()):
        cantidad = int(table.item(row, 1).text())
        precio = float(table.item(row, 2).text().replace('€', '').strip())
        iva_percent = float(table.item(row, 3).text().replace('%', '').strip())
        
        linea_subtotal = cantidad * precio
        linea_iva = linea_subtotal * (iva_percent / 100)
        
        subtotal_expected += linea_subtotal
        iva_expected += linea_iva
        
        print(f"  Ligne {row+1}: {cantidad} × {precio}€ + {iva_percent}% = {linea_subtotal + linea_iva:.2f}€")
    
    total_expected = subtotal_expected + iva_expected
    
    # Vérifier les totaux affichés
    subtotal_text = window.subtotal_label.text()
    iva_text = window.iva_label.text()
    total_text = window.total_label.text()
    
    subtotal_actual = float(subtotal_text.replace('€', '').strip())
    iva_actual = float(iva_text.replace('€', '').strip())
    total_actual = float(total_text.replace('€', '').strip())
    
    print(f"\nTotaux:")
    print(f"  Subtotal: {subtotal_actual:.2f}€ (attendu: {subtotal_expected:.2f}€)")
    print(f"  IVA: {iva_actual:.2f}€ (attendu: {iva_expected:.2f}€)")
    print(f"  Total: {total_actual:.2f}€ (attendu: {total_expected:.2f}€)")
    
    if (abs(subtotal_actual - subtotal_expected) < 0.01 and
        abs(iva_actual - iva_expected) < 0.01 and
        abs(total_actual - total_expected) < 0.01):
        print("✅ Test réussi: Totaux calculés correctement")
        return True
    else:
        print("❌ Test échoué: Totaux incorrects")
        return False

def main():
    """Exécuter tous les tests"""
    print("\n" + "=" * 70)
    print("🧪 TESTS DE COMPORTEMENT - IVA MODIFIABLE")
    print("=" * 70)
    
    results = []
    
    results.append(("Colonne IVA % existe", test_iva_column_exists()))
    results.append(("IVA recommandé appliqué", test_iva_recomendado_applied()))
    results.append(("Totaux calculés correctement", test_totals_calculated_correctly()))
    
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status}: {test_name}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, result in results if result)
    
    print("\n" + "=" * 70)
    print(f"Total: {passed_tests}/{total_tests} tests réussis")
    print("=" * 70)
    
    return 0 if passed_tests == total_tests else 1

if __name__ == '__main__':
    sys.exit(main())

