> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 📦 Guide Complet du Système de Stock

## 🎯 Vue d'Ensemble

Le système de stock de **Facturación Fácil** est complètement intégré et automatisé :

- ✅ **Création automatique** d'entrées de stock pour chaque nouveau produit
- ✅ **Diminution automatique** du stock lors de facturation
- ✅ **Interface de gestion** pour ajuster manuellement les stocks
- ✅ **Historique des mouvements** avec traçabilité complète

## 🔄 Fonctionnement Automatique

### 1️⃣ Création de Produit → Stock Automatique
```
Nouveau Produit → Stock Initial = 0
```
- **Quand** : Création d'un nouveau produit
- **Action** : Entrée automatique avec stock = 0
- **Localisation** : `database/models.py` ligne 123

### 2️⃣ Facturation → Diminution de Stock
```
Facture Sauvegardée → Stock Diminué Automatiquement
```
- **Quand** : Sauvegarde d'une facture
- **Action** : Stock réduit selon les quantités facturées
- **Localisation** : `database/database.py` ligne 905

## 🖥️ Interface de Gestion de Stock

### Accès
1. **Lancer l'application** : `python main.py`
2. **Cliquer** sur "📋 Stock" dans la fenêtre principale

### Fonctionnalités Disponibles

#### 📊 Vue d'Ensemble
- **Liste complète** de tous les produits
- **Stock actuel** affiché en temps réel
- **Indicateurs visuels** selon le niveau de stock
- **Recherche et filtrage** par nom, référence ou catégorie

#### ⚡ Ajustements Rapides
- **Boutons +/-** pour chaque produit
- **Ajustement immédiat** sans dialogue
- **Feedback visuel** dans la barre de statut
- **Historique automatique** des mouvements

#### 🔧 Gestion Avancée
- **Édition manuelle** du stock
- **Définition de stock minimum**
- **Exportation** des données
- **Historique détaillé** des mouvements

## 🎮 Utilisation Pratique

### Augmenter le Stock
1. **Localiser** le produit dans la liste
2. **Cliquer** sur le bouton **"+"**
3. **Résultat** : Stock augmenté de 1 unité

### Diminuer le Stock
1. **Localiser** le produit dans la liste
2. **Cliquer** sur le bouton **"-"**
3. **Résultat** : Stock diminué de 1 unité (minimum 0)

### Édition Manuelle
1. **Sélectionner** un produit
2. **Cliquer** sur "📝 Editar Stock"
3. **Saisir** la nouvelle quantité
4. **Confirmer** la modification

## 🔗 Intégration Facture-Stock

### Workflow Automatique
```
1. Créer une facture avec produits
2. Sauvegarder la facture
3. Stock automatiquement diminué
4. Mouvement enregistré dans l'historique
```

### Exemple Concret
```
Produit: Laptop Dell
Stock initial: 20 unités

Facture créée:
- 5 x Laptop Dell

Résultat automatique:
- Stock final: 15 unités
- Mouvement: -5 (VENTE)
```

## 📈 Indicateurs Visuels

### États du Stock
- 🔴 **Rouge** : Stock épuisé (0)
- 🟠 **Orange** : Stock bas (≤ stock minimum)
- 🟡 **Jaune** : Stock moyen (≤ 10)
- 🟢 **Vert** : Stock OK (> 10)

### Feedback en Temps Réel
- 📈 **Flèche montante** : Stock augmenté
- 📉 **Flèche descendante** : Stock diminué
- ✅ **Message de confirmation** dans la barre de statut

## 🗃️ Structure de Données

### Table `productos`
```sql
stock_actual INTEGER    -- Stock actuel du produit
stock_minimo INTEGER    -- Seuil d'alerte de stock bas
```

### Table `stock_movements`
```sql
producto_id INTEGER     -- Référence du produit
cantidad INTEGER        -- Quantité du mouvement (+/-)
tipo TEXT              -- Type: VENTA, AJUSTE, MANUAL
descripcion TEXT       -- Description du mouvement
fecha_movimiento TIMESTAMP -- Date/heure du mouvement
```

## 🔧 Maintenance et Diagnostic

### Vérification de Cohérence
```bash
# Vérifier que tous les produits ont une entrée de stock
python -c "from database.models import Producto, Stock; 
productos = Producto.get_all(); 
print(f'Produits: {len(productos)}');
stock_entries = Stock.get_all();
print(f'Entrées stock: {len(stock_entries)}')"
```

### Test de Relation Facture-Stock
1. **Noter** le stock initial d'un produit
2. **Créer** une facture avec ce produit
3. **Vérifier** que le stock a diminué
4. **Consulter** l'historique des mouvements

## ⚠️ Points Importants

### Sécurités Intégrées
- ✅ **Stock minimum 0** : Impossible d'avoir un stock négatif
- ✅ **Validation des quantités** : Contrôle des saisies
- ✅ **Traçabilité complète** : Tous les mouvements enregistrés
- ✅ **Transactions atomiques** : Cohérence garantie

### Bonnes Pratiques
- 📊 **Surveiller régulièrement** les stocks bas
- 📝 **Utiliser les descriptions** pour les ajustements manuels
- 🔄 **Vérifier périodiquement** la cohérence des données
- 💾 **Exporter régulièrement** pour sauvegarde

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
