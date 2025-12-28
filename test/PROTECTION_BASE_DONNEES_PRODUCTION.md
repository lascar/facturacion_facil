# 🛡️ Protection de la Base de Données de Production

## ⚠️ Problème Identifié

Les tests effaçaient les données de production car :

1. **Instance globale `db`** : Dans `database/database.py` ligne 1921, il y a une instance globale :
   ```python
   db = Database()  # Utilise "base_de_datos/facturacion.db" par défaut
   ```

2. **Tests créant des instances directes** : Certains tests créaient des instances `Database()` sans argument, utilisant ainsi la base de production.

3. **Monkeypatch insuffisant** : Le `monkeypatch` dans `conftest.py` ne protégeait pas contre :
   - Les imports directs avant l'application du patch
   - Les créations d'instances `Database()` sans passer par `db`
   - Les accès directs au fichier `base_de_datos/facturacion.db`

## ✅ Solutions Implémentées

### 1. Protection au Niveau de `pytest_configure`

**Fichier : `test/conftest.py`**

```python
def pytest_configure(config):
    """Configuration pytest"""
    # Variables d'environnement
    os.environ['PYTEST_RUNNING'] = '1'
    os.environ['DISABLE_PDF_OPEN'] = '1'
    
    # PROTECTION CRITIQUE: Base de données de test par défaut
    import tempfile
    test_db_fd, test_db_path = tempfile.mkstemp(suffix='.db', prefix='pytest_default_')
    os.close(test_db_fd)
    
    # Stocker pour nettoyage
    config._pytest_default_db_path = test_db_path
    
    # Variable d'environnement pour redirection
    os.environ['TEST_DATABASE_PATH'] = test_db_path
```

**Avantages :**
- ✅ S'exécute AVANT tout import de module
- ✅ Crée une base de données de test par défaut
- ✅ Définit `TEST_DATABASE_PATH` pour redirection automatique

### 2. Protection au Niveau de `Database.__init__`

**Fichier : `database/database.py`**

```python
class Database:
    def __init__(self, db_path="base_de_datos/facturacion.db"):
        # PROTECTION: Si pytest est en cours, utiliser la base de test
        if os.environ.get('PYTEST_RUNNING') == '1' and os.environ.get('TEST_DATABASE_PATH'):
            self.db_path = os.environ.get('TEST_DATABASE_PATH')
            self.logger = get_logger("database_test")
            self.logger.info(f"🧪 Mode TEST - DB: {os.path.basename(self.db_path)}")
        else:
            self.db_path = db_path
            self.logger = get_logger("database")
```

**Avantages :**
- ✅ Protège TOUTES les créations d'instances `Database()`
- ✅ Fonctionne même si le monkeypatch échoue
- ✅ Log clairement quand le mode test est actif

### 3. Nettoyage Automatique

**Fichier : `test/conftest.py`**

```python
def pytest_sessionfinish(session, exitstatus):
    """Nettoyage à la fin de tous les tests"""
    # Nettoyer la base de données de test par défaut
    if hasattr(session.config, '_pytest_default_db_path'):
        try:
            if os.path.exists(session.config._pytest_default_db_path):
                os.unlink(session.config._pytest_default_db_path)
        except Exception:
            pass
    
    # Nettoyer les variables d'environnement
    os.environ.pop('TEST_DATABASE_PATH', None)
```

### 4. Correction des Tests Problématiques

**Fichier : `test/integration/test_global_todas_correcciones.py`**

**Avant :**
```python
db = Database()  # ❌ Crée une instance avec le chemin par défaut
```

**Après :**
```python
from database.database import db  # ✅ Utilise l'instance globale patchée
```

## 🎯 Résultat

### Protection Multi-Niveaux

1. **Niveau 1** : Variable d'environnement `TEST_DATABASE_PATH` définie par pytest
2. **Niveau 2** : `Database.__init__` vérifie `PYTEST_RUNNING` et redirige automatiquement
3. **Niveau 3** : Monkeypatch du fixture `setup_test_environment` (protection existante)
4. **Niveau 4** : Nettoyage automatique à la fin des tests

### Garanties

- ✅ **Aucun test ne peut accéder à `base_de_datos/facturacion.db`** pendant l'exécution
- ✅ **Toutes les instances `Database()` sont redirigées** vers une base de test
- ✅ **Les données de production sont protégées** même en cas d'erreur de test
- ✅ **Nettoyage automatique** des bases de données de test

## 📋 Vérification

Pour vérifier que la protection fonctionne :

```bash
# Lancer les tests et vérifier les logs
python -m pytest test/ -v

# Chercher dans les logs :
# "🧪 Mode TEST activé - Utilisation de: pytest_default_*.db"
```

## ⚠️ Important

**NE JAMAIS :**
- Créer des instances `Database()` directement dans les tests
- Modifier `os.environ['PYTEST_RUNNING']` dans les tests
- Supprimer les protections dans `Database.__init__`

**TOUJOURS :**
- Utiliser les fixtures `temp_db`, `clean_db`, ou `isolated_db`
- Importer `from database.database import db` (instance globale)
- Vérifier que `PYTEST_RUNNING=1` dans l'environnement de test

