> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# Guide de Migration - Suppression des Colonnes Stock de Productos

## Vue d'ensemble

Cette migration supprime les colonnes `stock_actual` et `stock_minimo` de la table `productos` pour ne conserver que la table `stock` dédiée. Cela élimine la duplication des données de stock et centralise la gestion dans une seule table.

## Avant la Migration

### Structure Actuelle
- **Table `productos`** : contient `stock_actual` et `stock_minimo`
- **Table `stock`** : contient également les données de stock
- **Problème** : Duplication des données, risque d'incohérence

### Structure Après Migration
- **Table `productos`** : sans colonnes de stock
- **Table `stock`** : seule source de vérité pour les stocks
- **Avantage** : Données centralisées, pas de duplication

## Processus de Migration

### 1. Sauvegarde Automatique
La migration crée automatiquement une sauvegarde dans `base_de_datos/backups/` avec timestamp.

### 2. Migration des Données
- Copie `productos.stock_actual` vers `stock.cantidad_disponible`
- Préserve toutes les données existantes
- Gère les cas où des produits n'ont pas d'entrée dans `stock`

### 3. Suppression des Colonnes
- Recrée la table `productos` sans les colonnes stock
- Préserve toutes les autres données (nom, prix, etc.)

## Exécution de la Migration

### Option 1: Script Interactif (Recommandé)
```bash
python migration_remove_stock_columns.py
```

### Option 2: Programmatique
```python
from database.migration_manager import MigrationManager

migration_manager = MigrationManager("base_de_datos/facturacion.db")
success = migration_manager.remove_stock_columns_from_productos()
```

## Tests de Validation

### Tests Automatisés
```bash
# Tester la migration
python test/unit/test_stock_migration.py

# Tester le système complet
python test/unit/test_complete_stock_system.py

# Ou avec pytest
pytest test/unit/test_stock_migration.py test/unit/test_complete_stock_system.py -v
```

### Tests Manuels Recommandés
1. **Vérifier l'affichage des stocks** dans l'interface
2. **Tester la mise à jour de stock** lors des ventes
3. **Contrôler la création de nouveaux produits**
4. **Valider les rapports de stock**

## Changements dans le Code

### Modèles Python
- `Producto.get_stock_actual()` : utilise maintenant `Stock.get_by_product()`
- `Stock.get_by_product()` : méthode principale pour récupérer le stock
- Support des tests avec paramètre `db_path` optionnel

### Base de Données
- Table `productos` : colonnes `stock_actual` et `stock_minimo` supprimées
- Table `stock` : reste inchangée, devient la seule source

## Rollback (Retour en Arrière)

En cas de problème, restaurer depuis la sauvegarde :

```bash
# Identifier la sauvegarde
ls -la base_de_datos/backups/backup_remove_stock_columns_*.db

# Restaurer (remplacer TIMESTAMP par la date/heure)
cp base_de_datos/backups/backup_remove_stock_columns_TIMESTAMP.db base_de_datos/facturacion.db
```

## Vérifications Post-Migration

### ✅ Checklist
- [ ] Application démarre sans erreur
- [ ] Stocks s'affichent correctement
- [ ] Création de produits fonctionne
- [ ] Mise à jour de stock fonctionne
- [ ] Rapports de stock corrects
- [ ] Aucune erreur dans les logs

### 🔍 Requêtes de Vérification
```sql
-- Vérifier que les colonnes stock ont été supprimées
PRAGMA table_info(productos);

-- Vérifier que les données stock sont dans la table stock
SELECT COUNT(*) FROM stock;

-- Vérifier l'intégrité des données
SELECT p.nombre, s.cantidad_disponible 
FROM productos p 
LEFT JOIN stock s ON p.id = s.producto_id 
LIMIT 10;
```

## Support et Dépannage

### Problèmes Courants
1. **Stock affiché à 0** : Vérifier que `Stock.get_by_product()` utilise la bonne base
2. **Erreur de connexion** : S'assurer que la base n'est pas verrouillée
3. **Données manquantes** : Vérifier la sauvegarde et restaurer si nécessaire

### Logs
Consulter les logs dans `logs/` pour plus de détails sur les erreurs.

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
