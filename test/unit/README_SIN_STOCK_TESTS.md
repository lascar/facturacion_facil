# Tests Unitaires - Système "Sin Stock"

## 📋 Description

Tests unitaires pour vérifier le bon fonctionnement du système "sin stock" qui permet de désactiver la gestion de stock pour certains produits (services, produits digitaux, etc.).

## 🎯 Objectif

Vérifier que les produits marqués "sin stock" :
- ✅ **N'ont PAS d'entrée dans la table `stock`** lors de la création
- ✅ **Voient leur entrée supprimée** quand on les marque "sin stock"
- ✅ **Voient leur entrée créée** quand on les démarque "sin stock"

## 📁 Fichiers de Test

### `test_sin_stock.py`
Tests unitaires pytest pour le système sin stock.

**Prérequis**: pytest installé

**Exécution**:
```bash
python -m pytest test/unit/test_sin_stock.py -v
```

### `run_sin_stock_test.py`
Script de test standalone qui ne nécessite pas pytest.

**Prérequis**: Aucun (utilise uniquement la bibliothèque standard)

**Exécution**:
```bash
python3 test/unit/run_sin_stock_test.py
```

## 🧪 Tests Inclus

### 1. `test_create_product_with_stock`
Vérifie qu'un produit créé avec `sin_stock=False` a une entrée dans la table `stock`.

**Comportement attendu**:
- Produit créé avec `sin_stock=False`
- Entrée créée dans table `stock` avec la quantité spécifiée

### 2. `test_create_product_without_stock`
Vérifie qu'un produit créé avec `sin_stock=True` n'a PAS d'entrée dans la table `stock`.

**Comportement attendu**:
- Produit créé avec `sin_stock=True`
- **Aucune** entrée dans table `stock`

### 3. `test_change_from_stock_to_sin_stock`
Vérifie que marquer un produit existant comme "sin stock" supprime son entrée dans la table `stock`.

**Comportement attendu**:
1. Produit créé avec `sin_stock=False` → entrée dans `stock`
2. Produit mis à jour avec `sin_stock=True`
3. Entrée dans `stock` **supprimée**

### 4. `test_change_from_sin_stock_to_stock`
Vérifie que démarquer un produit "sin stock" crée une entrée dans la table `stock`.

**Comportement attendu**:
1. Produit créé avec `sin_stock=True` → pas d'entrée dans `stock`
2. Produit mis à jour avec `sin_stock=False`
3. Entrée dans `stock` **créée** avec la quantité spécifiée

## 📊 Résultats Attendus

```
======================================================================
🧪 TESTS UNITAIRES - Système 'Sin Stock'
======================================================================

✅ test_create_product_with_stock
✅ test_create_product_without_stock
✅ test_change_from_stock_to_sin_stock
✅ test_change_from_sin_stock_to_stock

======================================================================
Résultats: 4 passés, 0 échoués sur 4 tests
======================================================================
```

## 🔍 Vérifications

Les tests vérifient :

1. **Création de produits**
   - Produits avec stock → entrée dans table `stock`
   - Produits sans stock → pas d'entrée dans table `stock`

2. **Mise à jour de produits**
   - Passage à "sin stock" → suppression de l'entrée
   - Passage à "con stock" → création de l'entrée

3. **Intégrité de la table stock**
   - La table `stock` contient uniquement les produits qui gèrent le stock
   - Les quantités sont correctement enregistrées

## 🛠️ Maintenance

Pour ajouter de nouveaux tests :

1. Ajouter la fonction de test dans `test_sin_stock.py` (pour pytest)
2. Ajouter la fonction de test dans `run_sin_stock_test.py` (pour standalone)
3. Mettre à jour la liste des tests dans la fonction `main()` de `run_sin_stock_test.py`
4. Mettre à jour ce README

## 📚 Références

- **Documentation système**: `RESUMEN_SIN_STOCK.md` (racine du projet)
- **Code source**: `database/database.py` (méthodes `add_product`, `update_product`)
- **Interface**: `ui/productos_pyqt5.py` (checkbox "Sin stock")

