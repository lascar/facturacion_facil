> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# Prochaines Étapes de la Refactorisation

## 📋 Vue d'ensemble

Ce document décrit les prochaines étapes de la refactorisation du projet Facturacion Facil.

---

## 🎯 Objectifs Prioritaires

### 1. Compléter la Refactorisation des Services ⏳

#### 1.1 Ajouter stock_minimo à la table stock
**Priorité** : Haute  
**Effort** : Faible

**Actions** :
1. Créer une migration pour ajouter la colonne `stock_minimo` à la table `stock`
2. Implémenter `StockService.update_stock_minimo()`
3. Ajouter les tests correspondants
4. Mettre à jour `ui/stock_pyqt5.py` pour utiliser la nouvelle méthode

**Fichiers à modifier** :
- `database/migrations/` - Nouvelle migration
- `services/stock_service.py` - Ajouter la méthode
- `test/unit/test_stock_service.py` - Ajouter les tests
- `ui/stock_pyqt5.py` - Utiliser la méthode

---

### 2. Appliquer les Principes Arjan Codes Restants ⏳

#### 2.1 Principe 1 : Préférer les fonctions aux classes
**Priorité** : Moyenne  
**Effort** : Moyen

**Actions** :
1. Identifier les classes qui pourraient être des fonctions
2. Refactoriser les classes simples en fonctions
3. Utiliser des fonctions pures quand c'est possible

**Exemples de candidats** :
- Certaines méthodes statiques dans les services
- Utilitaires de validation
- Formatage de données

#### 2.2 Principe 6 : Utiliser les comprehensions
**Priorité** : Basse  
**Effort** : Faible

**Actions** :
1. Rechercher les boucles `for` qui construisent des listes/dicts
2. Remplacer par des list/dict comprehensions
3. Améliorer la lisibilité et les performances

**Exemples** :
```python
# Avant
result = []
for item in items:
    if item.is_valid():
        result.append(item.name)

# Après
result = [item.name for item in items if item.is_valid()]
```

#### 2.3 Principe 9 : Ajouter des fonctions main()
**Priorité** : Basse  
**Effort** : Faible

**Actions** :
1. Ajouter des fonctions `main()` aux scripts exécutables
2. Utiliser le pattern `if __name__ == "__main__":`
3. Améliorer la testabilité

**Fichiers candidats** :
- Scripts de migration
- Scripts de validation
- Scripts de profiling

---

### 3. Augmenter le Coverage ⏳

#### 3.1 Coverage des Services
**Priorité** : Haute  
**Effort** : Moyen

**Objectif** : **80%+** sur tous les services

**Actions** :
1. Analyser le coverage actuel avec `pytest-cov`
2. Identifier les branches non testées
3. Ajouter des tests pour les cas limites
4. Tester les chemins d'erreur

**Commande** :
```bash
pytest test/unit/test_*_service.py --cov=services --cov-report=html
```

#### 3.2 Coverage de la Base de Données
**Priorité** : Moyenne  
**Effort** : Élevé

**Objectif** : **60%+** sur `database/database.py`

**Actions** :
1. Identifier les méthodes non testées
2. Créer des tests d'intégration
3. Tester les transactions et rollbacks
4. Tester les cas d'erreur

---

### 4. Optimisations et Améliorations 🔄

#### 4.1 Optimisation des Requêtes SQL
**Priorité** : Basse  
**Effort** : Moyen

**Actions** :
1. Analyser les requêtes lentes avec `EXPLAIN QUERY PLAN`
2. Ajouter des index si nécessaire
3. Optimiser les JOINs
4. Utiliser des requêtes préparées

#### 4.2 Amélioration de la Gestion des Erreurs
**Priorité** : Moyenne  
**Effort** : Faible

**Actions** :
1. Ajouter plus de contexte aux exceptions
2. Améliorer les messages d'erreur pour l'utilisateur
3. Logger les erreurs de manière plus détaillée
4. Ajouter des suggestions de résolution

#### 4.3 Amélioration de la Documentation
**Priorité** : Basse  
**Effort** : Faible

**Actions** :
1. Ajouter des docstrings manquants
2. Créer des diagrammes d'architecture
3. Documenter les patterns utilisés
4. Créer un guide de contribution

---

## 📅 Planning Suggéré

### Sprint 1 (1-2 jours)
- ✅ Compléter stock_minimo
- ✅ Augmenter coverage des services à 80%+

### Sprint 2 (2-3 jours)
- ⏳ Appliquer les comprehensions
- ⏳ Ajouter les fonctions main()
- ⏳ Augmenter coverage de la base de données

### Sprint 3 (1-2 jours)
- ⏳ Optimiser les requêtes SQL
- ⏳ Améliorer la gestion des erreurs
- ⏳ Compléter la documentation

---

## 🎯 Critères de Succès

### Coverage
- ✅ Services : **80%+**
- ⏳ Base de données : **60%+**
- ⏳ UI : **40%+**
- ⏳ Global : **50%+**

### Tests
- ✅ **536+ tests passent**
- ✅ **0 régression**
- ✅ **Temps d'exécution < 3 minutes**

### Code Quality
- ✅ Tous les principes Arjan Codes appliqués
- ✅ Gestion d'erreurs robuste
- ✅ Documentation complète
- ✅ Performances optimales

---

## 📝 Notes

### Priorités
1. **Haute** : À faire en priorité
2. **Moyenne** : Important mais pas urgent
3. **Basse** : Nice to have

### Effort
1. **Faible** : < 1 jour
2. **Moyen** : 1-2 jours
3. **Élevé** : > 2 jours

---

**Dernière mise à jour** : 2025-12-25  
**Statut global** : 🚀 En cours


---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
