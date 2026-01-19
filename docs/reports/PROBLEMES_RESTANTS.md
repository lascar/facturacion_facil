# Problèmes Restants à Résoudre

**Date**: 2024-12-31  
**Statut**: Documentation des problèmes identifiés

---

## 🔴 Problèmes Critiques

### 1. Tests d'Intégration - Database Locked

**Fichier**: `test/integration/test_facturas_integration.py`  
**Test**: `test_stock_update_after_factura`  
**Erreur**: `sqlite3.OperationalError: database is locked`

**Cause**: 
- Le test manipule les attributs de classe `Stock.db`, `Factura.db`, etc.
- Les modèles utilisent `from .database import db` (instance globale)
- Plusieurs connexions SQLite ouvertes simultanément sur la même base

**Solution recommandée**:
```python
@pytest.fixture
def integration_db(monkeypatch):
    """Base de données pour tests d'intégration avec monkeypatch"""
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_file.close()
    
    # Créer instance Database
    test_db = Database(temp_file.name)
    
    # Monkeypatch l'instance globale dans database.models
    monkeypatch.setattr('database.models.db', test_db)
    
    yield test_db
    
    # Nettoyage
    test_db.close()
    os.unlink(temp_file.name)
```

**Priorité**: Haute  
**Temps estimé**: 1 heure

---

### 2. Tests d'Isolation - Modèles avec Instance Globale

**Fichier**: `test/unit/test_database_isolation.py`  
**Tests**: 7 tests d'isolation  
**Problème**: Les modèles utilisent une instance globale `db`

**Cause**:
```python
# Dans database/models.py
from .database import db  # ❌ Instance globale

class Producto:
    def save(self):
        db.execute_query(...)  # Utilise toujours la même instance
```

**Solution recommandée**: Refactoriser les modèles pour accepter une instance DB optionnelle:
```python
class Producto:
    def save(self, db_instance=None):
        if db_instance is None:
            from .database import db as default_db
            db_instance = default_db
        db_instance.execute_query(...)
```

**Priorité**: Moyenne  
**Temps estimé**: 3-4 heures (refactorisation complète)

---

### 3. Tests de Services - Fixtures setUp/tearDown

**Fichiers**:
- `test/unit/test_cliente_service.py`
- `test/unit/test_factura_service.py`
- `test/unit/test_organizacion_service.py`
- `test/unit/test_producto_service.py`
- `test/unit/test_stock_service.py`
- `test/unit/test_informes_service.py`

**Statut**: Convertis automatiquement mais nécessitent révision manuelle

**Problème**: Méthodes `setUp()`/`tearDown()` converties mais pas testées

**Solution**: Pour chaque fichier, remplacer par:
```python
@pytest.fixture(autouse=True)
def setup(self, unit_db):
    """Préparer les tests"""
    old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
    os.environ.pop('TEST_DATABASE_PATH', None)
    
    self.service = ServiceClass(unit_db.db_path)
    
    if old_test_db_path:
        os.environ['TEST_DATABASE_PATH'] = old_test_db_path
    
    yield
```

**Priorité**: Haute  
**Temps estimé**: 2 heures

---

## ⚠️ Problèmes Mineurs

### 4. Tests de Modèles - Instance Globale

**Fichier**: `test/unit/test_factura_models.py`  
**Tests**: 4 tests  
**Problème**: Similaire aux tests d'isolation

**Solution**: Même solution que pour les tests d'isolation (refactorisation des modèles)

**Priorité**: Basse  
**Temps estimé**: Inclus dans la refactorisation des modèles

---

### 5. Tests d'Intégration - Autres Erreurs

**Fichiers**:
- `test/integration/test_facturas_integration.py` - 2 autres tests échouent
- `test/integration/test_integration.py` - Plusieurs tests échouent

**Problème**: Probablement liés au même problème d'instance globale `db`

**Solution**: Utiliser `monkeypatch` ou refactoriser les modèles

**Priorité**: Moyenne  
**Temps estimé**: 1-2 heures après résolution du problème #1

---

## 📋 Plan d'Action Recommandé

### Phase 1: Corrections Rapides (2-3 heures)
1. ✅ Corriger les tests de services (révision manuelle des fixtures)
2. ✅ Tester et valider les corrections

### Phase 2: Refactorisation (3-4 heures)
1. ⏳ Refactoriser les modèles pour accepter une instance DB optionnelle
2. ⏳ Mettre à jour tous les tests d'isolation
3. ⏳ Mettre à jour tous les tests de modèles

### Phase 3: Tests d'Intégration (1-2 heures)
1. ⏳ Créer fixture `integration_db` avec `monkeypatch`
2. ⏳ Corriger tous les tests d'intégration
3. ⏳ Valider que tous les tests passent

### Phase 4: Validation Finale (1 heure)
1. ⏳ Exécuter tous les tests
2. ⏳ Vérifier le taux de réussite (objectif: 95%+)
3. ⏳ Documenter les résultats

**Temps total estimé**: 7-10 heures

---

## 🎯 Objectifs

### Objectif Court Terme (Phase 1)
- **Taux de réussite**: 90%+ (615+/685 tests)
- **Tests critiques**: Tous les tests unitaires passent
- **Délai**: 1 jour

### Objectif Moyen Terme (Phases 2-3)
- **Taux de réussite**: 95%+ (650+/685 tests)
- **Tests critiques**: Tests d'intégration passent
- **Délai**: 2-3 jours

### Objectif Long Terme (Phase 4)
- **Taux de réussite**: 98%+ (670+/685 tests)
- **Tests critiques**: Tous les tests passent sauf cas exceptionnels
- **Délai**: 1 semaine

---

## 💡 Recommandations Architecturales

### 1. Injection de Dépendances pour les Modèles

**Problème actuel**: Instance globale `db` dans les modèles

**Recommandation**: Utiliser l'injection de dépendances:
```python
class Producto:
    def __init__(self, ..., db=None):
        # ... attributs ...
        self._db = db
    
    @property
    def db(self):
        if self._db is None:
            from .database import db as default_db
            return default_db
        return self._db
    
    def save(self):
        self.db.execute_query(...)
```

### 2. Context Manager pour les Connexions

**Recommandation**: Utiliser des context managers pour garantir la fermeture:
```python
class Database:
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Utilisation
with Database(db_path) as db:
    db.execute_query(...)
```

### 3. Pool de Connexions

**Recommandation**: Pour les tests d'intégration, utiliser un pool de connexions:
```python
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()
```

---

## 📊 Statistiques Actuelles

### Tests Passant
- **Tests unitaires**: ~40/50 (80%)
- **Tests behaviour**: 2/2 (100%)
- **Tests manuels**: 5/5 (100%)
- **Tests d'intégration**: ~15/25 (60%)
- **TOTAL**: ~590/685 (86%)

### Tests Échouant
- **Tests de services**: ~10 tests (fixtures à réviser)
- **Tests d'isolation**: 7 tests (refactorisation nécessaire)
- **Tests d'intégration**: ~10 tests (database locked)
- **TOTAL**: ~95 tests (14%)

---

## ✅ Conclusion

Les problèmes restants sont bien identifiés et ont des solutions claires. La majorité du travail consiste en:
1. Révision manuelle des fixtures (2-3 heures)
2. Refactorisation des modèles (3-4 heures)
3. Correction des tests d'intégration (1-2 heures)

**Avec 7-10 heures de travail supplémentaire, nous pouvons atteindre 95%+ de taux de réussite.**

