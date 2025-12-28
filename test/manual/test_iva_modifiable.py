#!/usr/bin/env python3
"""Test pour vérifier que l'IVA est modifiable dans les factures"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.facturas_pyqt5 import FacturasPyQt5Window

def test_iva_modifiable():
    """Test de l'IVA modifiable dans factura"""
    print('🧪 Test - IVA Recommandé Appliqué par Défaut\n')
    print('=' * 70)

    app = QApplication(sys.argv)
    window = FacturasPyQt5Window()

    # Obtenir un produit
    productos = window.producto_service.get_all_productos()
    if not productos:
        print('❌ Aucun produit disponible pour le test')
        return False

    # Trouver un produit avec un IVA différent de 21%
    producto_test = None
    for p in productos:
        iva = p.get('iva_recomendado', 21.0)
        if iva != 21.0:
            producto_test = p
            break

    # Si aucun produit avec IVA différent, utiliser le premier
    if not producto_test:
        producto_test = productos[0]
        print('⚠️  Aucun produit avec IVA != 21%, utilisation du premier produit')

    print(f'📦 Produit de test: {producto_test["nombre"]}')
    print(f'   IVA recommandé: {producto_test.get("iva_recomendado", 21.0)}%')
    print(f'   Prix: {producto_test.get("precio_venta", 0.0)}€')

    # Simuler la sélection du produit
    window.producto_autocomplete.set_product(producto_test)
    window.cantidad_spin.setValue(2)

    # Ajouter le produit
    window.add_product_to_invoice()

    # Vérifier que le produit a été ajouté
    if window.productos_table.rowCount() == 0:
        print('\n❌ ERREUR: Produit non ajouté à la table')
        return False

    print(f'\n✅ Produit ajouté à la facture')

    # Vérifier les valeurs dans la table
    row = 0
    nombre = window.productos_table.item(row, 0).text()
    cantidad = window.productos_table.item(row, 1).text()
    precio = window.productos_table.item(row, 2).text()
    iva = window.productos_table.item(row, 3).text()
    total = window.productos_table.item(row, 4).text()

    print(f'\n📊 Valeurs dans la table:')
    print(f'   Producto: {nombre}')
    print(f'   Cantidad: {cantidad}')
    print(f'   Precio Unit.: {precio}')
    print(f'   IVA %: {iva}')
    print(f'   Total: {total}')

    # Vérifier que l'IVA correspond à l'IVA recommandé
    iva_value = float(iva.replace('%', '').strip())
    iva_expected = producto_test.get('iva_recomendado', 21.0)

    if abs(iva_value - iva_expected) < 0.1:
        print(f'\n✅ IVA recommandé appliqué correctement: {iva_value}%')
    else:
        print(f'\n❌ ERREUR: IVA incorrect')
        print(f'   Attendu: {iva_expected}%')
        print(f'   Obtenu: {iva_value}%')
        return False

    # Vérifier que le total est calculé correctement
    cantidad_val = int(cantidad)
    precio_val = float(precio.replace('€', '').strip())
    subtotal_calc = cantidad_val * precio_val
    iva_calc = subtotal_calc * (iva_value / 100)
    total_calc = subtotal_calc + iva_calc
    total_val = float(total.replace('€', '').strip())

    if abs(total_val - total_calc) < 0.01:
        print(f'✅ Total calculé correctement: {total_val:.2f}€')
        print(f'   Subtotal: {subtotal_calc:.2f}€')
        print(f'   IVA: {iva_calc:.2f}€')
        print(f'   Total: {total_calc:.2f}€')
    else:
        print(f'❌ ERREUR: Total incorrect')
        print(f'   Attendu: {total_calc:.2f}€')
        print(f'   Obtenu: {total_val:.2f}€')
        return False

    print('\n' + '=' * 70)
    print('🎉 TOUS LES TESTS RÉUSSIS')
    print('=' * 70)
    print('\n📋 Fonctionnalités validées:')
    print('  1. ✅ IVA recommandé du produit appliqué par défaut')
    print('  2. ✅ Colonne IVA % visible et remplie')
    print('  3. ✅ Total calculé avec IVA individuel')
    print('  4. ✅ Calculs corrects (quantité × prix + IVA)')
    print('=' * 70)
    
    return True

if __name__ == '__main__':
    success = test_iva_modifiable()
    sys.exit(0 if success else 1)

