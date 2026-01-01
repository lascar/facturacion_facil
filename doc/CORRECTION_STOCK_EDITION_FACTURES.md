# 🔧 Correction: Calcul Stock lors Édition de Factures

## 🎯 Problème Résolu

**Problème initial**: Lors de l'édition d'une facture, l'interface vérifiait uniquement le stock actuel sans tenir compte du fait que les quantités de la facture en cours d'édition allaient être "libérées" lors de la modification.

**Conséquence**: Impossibilité d'augmenter les quantités dans une facture même après une augmentation de stock.

## ✅ Solution Implémentée

### 1. **Nouvelle Méthode de Calcul**

Ajout de la méthode `get_available_stock_for_product()` dans `EditarFacturaDialog`:

```python
def get_available_stock_for_product(self, producto_id):
    """Calcular el stock disponible para un producto considerando la factura actual"""
    # Stock actuel du produit
    stock_actual = producto.get('stock_actual', 0)
    
    # Quantité dans la facture originale (qui sera libérée)
    cantidad_original = sum(linea.get('cantidad', 0) 
                           for linea in self.factura_data.get('lineas', [])
                           if linea.get('producto_id') == producto_id)
    
    # Stock disponible = stock actuel + quantité à libérer
    return stock_actual + cantidad_original
```

### 2. **Modifications Interface**

#### **Ajout de Produits** (`agregar_producto`)
- ✅ Utilise `get_available_stock_for_product()` au lieu du stock actuel
- ✅ Message d'erreur adapté: "Stock disponible pour édition"

#### **Modification Quantités** (`on_table_item_changed`)
- ✅ Calcul du stock disponible pour la ligne spécifique
- ✅ Soustraction de la quantité actuelle de la ligne
- ✅ Vérification correcte des nouvelles quantités

## 📊 Exemple Concret

### Avant la Correction
```
Stock initial: 100 unités
Facture créée: 20 unités → Stock actuel: 80 unités
Augmentation stock: +30 unités → Stock actuel: 110 unités

❌ Édition facture: "Stock disponible: 110" 
❌ Impossible de mettre 25 unités (110 < 25 ??? FAUX!)
```

### Après la Correction
```
Stock initial: 100 unités  
Facture créée: 20 unités → Stock actuel: 80 unités
Augmentation stock: +30 unités → Stock actuel: 110 unités

✅ Édition facture: "Stock disponible pour édition: 130"
✅ Calcul: 110 (actuel) + 20 (libéré) = 130
✅ Possible de mettre jusqu'à 130 unités!
```

## 🔄 Flux de Calcul

### Pour Ajouter un Produit
1. Obtenir stock actuel du produit
2. Calculer quantité totale dans facture originale
3. **Stock disponible = stock actuel + quantité originale**
4. Vérifier: nouvelle quantité ≤ stock disponible

### Pour Modifier une Ligne
1. Obtenir stock actuel du produit
2. Calculer quantité totale dans facture originale
3. Soustraire quantité actuelle de cette ligne
4. **Stock disponible pour ligne = (stock actuel + quantité originale) - quantité ligne actuelle**
5. Vérifier: nouvelle quantité ≤ stock disponible pour ligne

## 🧪 Tests Réalisés

### Test 1: Calcul Stock Disponible
- ✅ Stock actuel: 1 unité
- ✅ Quantité facture: 1 unité  
- ✅ Stock disponible calculé: 2 unités
- ✅ Calcul correct: 1 + 1 = 2

### Test 2: Scénario Augmentation Stock
- ✅ Stock initial: 1 unité
- ✅ Augmentation: +10 unités → Stock: 11 unités
- ✅ Stock disponible édition: 12 unités (11 + 1)
- ✅ Modification possible: 1 → 6 unités

## 🎉 Bénéfices

### ✅ **Flexibilité Améliorée**
- Possibilité d'augmenter les quantités après augmentation de stock
- Calcul précis du stock réellement disponible

### ✅ **Logique Cohérente**  
- Le calcul reflète la réalité: stock + quantités libérées
- Plus de blocage artificiel

### ✅ **Expérience Utilisateur**
- Messages d'erreur plus clairs
- Fonctionnalité intuitive et prévisible

## 📝 Fichiers Modifiés

- **`ui/facturas_pyqt5.py`**
  - Ajout méthode `get_available_stock_for_product()`
  - Modification `agregar_producto()` 
  - Modification `on_table_item_changed()`

## 🔮 Impact

Cette correction permet maintenant aux utilisateurs de:
1. **Augmenter le stock** d'un produit
2. **Éditer immédiatement** les factures existantes
3. **Profiter pleinement** de l'augmentation de stock
4. **Modifier les quantités** selon le stock réellement disponible

---
*Correction implémentée et testée avec succès - PyQt5 Facturación Fácil*
