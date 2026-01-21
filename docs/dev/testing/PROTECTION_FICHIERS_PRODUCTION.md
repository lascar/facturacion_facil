> **[⬆️ Volver al índice](../INDEX.md)** | **[🧪 Testing](README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🛡️ Protection des Fichiers de Production

> **CRITIQUE** : Ce document décrit le système de protection multi-niveaux qui empêche les tests de modifier ou supprimer les fichiers de production.

---

## 📋 Problème Résolu

### Symptômes
Lors de l'exécution de `./run_organized_tests.sh all`, les fichiers de production étaient modifiés ou perdus :
- ❌ **Base de données** (`base_de_datos/facturacion.db`) : Données effacées et remplacées par des données de test
- ❌ **Configuration** (`config/config.json`) : Paramètres modifiés
- ❌ **Logo** (`logo/`) : Fichiers perdus ou remplacés

### Cause Racine
Certains tests accédaient directement aux fichiers de production au lieu d'utiliser les fixtures de test isolées.

---

## ✅ Solution Implémentée

### Protection Multi-Niveaux

#### **Niveau 1 : Protection pytest** (`test/conftest.py`)
Variables d'environnement automatiques :
- `PYTEST_RUNNING=1` : Indique que les tests sont en cours
- `TEST_DATABASE_PATH` : Redirige vers une base de données temporaire

```python
# Dans conftest.py
def pytest_configure(config):
    os.environ['PYTEST_RUNNING'] = '1'
    test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db', prefix='pytest_default_')
    os.environ['TEST_DATABASE_PATH'] = test_db_path
```

#### **Niveau 2 : Fixtures de test**
Fixtures standardisées pour isolation :
- `temp_db` : Base de données temporaire pour tests généraux
- `unit_db` : Base isolée pour tests unitaires
- `integration_db` : Base isolée pour tests d'intégration
- `BaseTestWithFixtures` : Classe de base avec fixtures standardisées

```python
# Utilisation dans les tests
class TestMyFeature(BaseTestWithFixtures):
    def test_something(self):
        # self.db pointe vers une base de test isolée
        product_id = self.db.add_product({...})
```

#### **Niveau 3 : Backup/Restore Automatique** ⭐ NOUVEAU
Le script `run_organized_tests.sh` effectue automatiquement :

**AVANT les tests** :
1. Backup de `base_de_datos/facturacion.db` → `backups/facturacion_backup_before_tests_YYYYMMDD_HHMMSS.db`
2. Backup de `config/config.json` → `backups/config_backup_before_tests_YYYYMMDD_HHMMSS.json`
3. Backup de `logo/` → `backups/logo_backup_before_tests_YYYYMMDD_HHMMSS/`

**APRÈS les tests** :
1. Restauration automatique de la base de données
2. Restauration automatique de config.json
3. Restauration automatique du répertoire logo/

#### **Niveau 4 : Vérification Statique** ⭐ NOUVEAU
Script `test/scripts/verify_no_production_db_usage.py` qui détecte :
- ❌ `Database()` sans paramètre
- ❌ `Database("base_de_datos/facturacion.db")`
- ❌ Accès direct à `config/config.json`
- ❌ Ouverture/écriture de `config.json`

---

## 🚀 Utilisation

### Lancer les tests en toute sécurité
```bash
# Tous les tests (avec backup/restore automatique)
./run_organized_tests.sh all

# Tests unitaires uniquement
./run_organized_tests.sh unit

# Tests d'intégration
./run_organized_tests.sh integration
```

### Vérifier qu'aucun test n'utilise les fichiers de production
```bash
python3 test/scripts/verify_no_production_db_usage.py
```

### Restaurer manuellement depuis un backup
```bash
# Lister les backups disponibles
ls -lh base_de_datos/backups/

# Restaurer la base de données
cp base_de_datos/backups/facturacion_backup_before_tests_YYYYMMDD_HHMMSS.db base_de_datos/facturacion.db

# Restaurer config.json
cp base_de_datos/backups/config_backup_before_tests_YYYYMMDD_HHMMSS.json config/config.json

# Restaurer logo/
rm -rf logo/
cp -r base_de_datos/backups/logo_backup_before_tests_YYYYMMDD_HHMMSS logo/
```

---

## 📝 Bonnes Pratiques pour les Nouveaux Tests

### ✅ À FAIRE

**Utiliser les fixtures** :
```python
# Option 1 : Hériter de BaseTestWithFixtures
class TestMyFeature(BaseTestWithFixtures):
    def test_something(self):
        product_id = self.db.add_product({...})
        assert product_id is not None

# Option 2 : Utiliser les fixtures pytest
def test_my_feature(unit_db):
    product_id = unit_db.add_product({...})
    assert product_id is not None
```

### ❌ À NE PAS FAIRE

**NE JAMAIS accéder directement aux fichiers de production** :
```python
# ❌ INTERDIT - Utilise la production par défaut
from database.database import Database
db = Database()

# ❌ INTERDIT - Production explicite
db = Database("base_de_datos/facturacion.db")

# ❌ INTERDIT - Accès direct à config.json
with open("config/config.json", "r") as f:
    config = json.load(f)
```

---

## 🔒 Garanties de Sécurité

1. ✅ **Quadruple protection** : pytest + fixtures + backup/restore + vérification statique
2. ✅ **Protection complète** : base de données + config.json + logo/
3. ✅ **Aucune perte de données possible** : backup automatique avant chaque test
4. ✅ **Restauration automatique** : même en cas d'erreur pendant les tests
5. ✅ **Historique des backups** : tous les backups sont conservés dans `base_de_datos/backups/`

---

## 📁 Fichiers Modifiés

### `run_organized_tests.sh`
Ajout des fonctions :
- `backup_production_database()` : Backup de la base de données
- `backup_production_config()` : Backup de config.json et logo/
- `restore_production_database()` : Restauration de la base de données
- `restore_production_config()` : Restauration de config.json et logo/

### `test/scripts/verify_no_production_db_usage.py`
Extension des patterns détectés pour inclure :
- Accès à `config/config.json`
- Ouverture/écriture de `config.json`

### `docs/dev/testing/PROTECTION_FICHIERS_PRODUCTION.md` (ce document)
Documentation complète de la solution.

---

## 📅 Historique

- **2026-01-21** : Protection complète activée et testée avec succès
  - Base de données : ✅ Protégée
  - config.json : ✅ Protégé
  - logo/ : ✅ Protégé

---

## 🔗 Voir Aussi

- **[GUIDE_FIXTURES.md](GUIDE_FIXTURES.md)** - Système de fixtures (OBLIGATOIRE)
- **[REGLES_CRITIQUES_TESTS_BASE_DONNEES.md](REGLES_CRITIQUES_TESTS_BASE_DONNEES.md)** - Règles de sécurité
- **[run_organized_tests.sh](../../../run_organized_tests.sh)** - Script de tests avec protection automatique

---

**Dernière mise à jour** : 2026-01-21  
**Auteur** : Équipe de développement

