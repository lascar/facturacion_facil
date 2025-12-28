# IVA Modifiable dans les Factures

## 📋 Résumé

L'IVA (TVA) est maintenant **modifiable** pour chaque produit dans les factures, avec l'**IVA recommandé du produit appliqué par défaut**.

---

## ✅ Fonctionnalités Implémentées

### 1. Colonne IVA % dans la Table de Produits

La table des produits dans les factures contient maintenant une colonne **"IVA %"** :

```
| Producto | Cantidad | Precio Unit. | IVA % | Total | Acciones |
```

### 2. IVA Recommandé Appliqué par Défaut

Lorsqu'un produit est ajouté à une facture :
- L'IVA recommandé du produit (`iva_recomendado`) est automatiquement appliqué
- Exemple : Si un produit a un IVA recommandé de 4%, la colonne IVA % affichera "4.0%"

### 3. IVA Modifiable

L'utilisateur peut **modifier l'IVA** directement dans la table :
- Cliquer sur la cellule IVA %
- Entrer une nouvelle valeur (ex: 10, 21, 4)
- Le total est recalculé automatiquement

### 4. Calcul Automatique des Totaux

Les totaux sont calculés en fonction de l'IVA individuel de chaque produit :

```
Subtotal ligne = Quantité × Prix unitaire
IVA ligne = Subtotal ligne × (IVA % / 100)
Total ligne = Subtotal ligne + IVA ligne

Subtotal facture = Somme des subtotals de toutes les lignes
IVA total = Somme des IVA de toutes les lignes
Total facture = Subtotal facture + IVA total
```

---

## 🔧 Modifications Techniques

### Fichier : `ui/facturas_pyqt5.py`

#### 1. Ajout de la colonne IVA % (lignes 329-344)

```python
productos_headers = ["Producto", "Cantidad", "Precio Unit.", "IVA %", "Total", "Acciones"]
self.productos_table.setColumnCount(len(productos_headers))
self.productos_table.setHorizontalHeaderLabels(productos_headers)
```

#### 2. Calcul des totaux avec IVA individuel (lignes 428-471)

```python
def update_totals(self):
    """Actualizar los totales de la factura"""
    subtotal = 0.0
    total_iva = 0.0

    for row in range(self.productos_table.rowCount()):
        cantidad = float(cantidad_item.text())
        precio_unit = float(precio_item.text().replace('€', '').strip())
        iva_percent = float(iva_item.text().replace('%', '').strip())
        
        linea_subtotal = cantidad * precio_unit
        subtotal += linea_subtotal
        
        linea_iva = linea_subtotal * (iva_percent / 100)
        total_iva += linea_iva
```

#### 3. Gestion des modifications dans la table (lignes 473-528)

```python
def on_product_table_item_changed(self, item):
    """Gérer les changements dans la table de produits"""
    # Si on modifie la quantité, le prix ou l'IVA
    if col in [1, 2, 3]:
        # Recalculer les totaux
        self.update_totals()
```

#### 4. Ajout de produit avec IVA recommandé (lignes 788-833)

```python
iva_recomendado = producto.get('iva_recomendado', 21.0)
iva_item = QTableWidgetItem(f"{iva_recomendado:.1f}%")
self.productos_table.setItem(row, 3, iva_item)
```

#### 5. Sauvegarde avec IVA (lignes 1113-1136)

```python
iva_percent = float(self.productos_table.item(row, 3).text().replace('%', '').strip())
lineas.append({
    'producto_id': producto_id,
    'cantidad': cantidad,
    'precio_unitario': precio_unit,
    'iva_aplicado': iva_percent,
    'subtotal': subtotal,
    'iva_amount': iva_amount,
    'total': total
})
```

---

## 🧪 Tests

### Test : `test/manual/test_iva_modifiable.py`

```bash
$ PYTHONPATH=/home/pascal/development/for_django/facturacion_facil python3 test/manual/test_iva_modifiable.py

✅ Produit ajouté à la factura
✅ IVA recommandé appliqué correctement: 4.0%
✅ Total calculé correctement: 50.00€
   Subtotal: 48.08€
   IVA: 1.92€
   Total: 50.00€
```

---

## 📊 Exemple d'Utilisation

### Scénario : Facture avec produits à IVA différents

| Producto | Cantidad | Precio Unit. | IVA % | Total |
|----------|----------|--------------|-------|-------|
| Livre    | 2        | 10.00€       | 4.0%  | 20.80€ |
| Vêtement | 1        | 50.00€       | 21.0% | 60.50€ |

**Totaux** :
- Subtotal : 70.00€
- IVA : 11.30€ (0.80€ + 10.50€)
- **Total : 81.30€**

---

## ✅ Résultat Final

- ✅ IVA modifiable pour chaque produit
- ✅ IVA recommandé appliqué par défaut
- ✅ Calculs automatiques corrects
- ✅ Sauvegarde en base de données
- ✅ Chargement depuis base de données

**Date** : 2025-12-28

