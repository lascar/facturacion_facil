# Isolation de la Base de Données pour les Tests de Comportement

## ⚠️ IMPORTANT : Protection de la Base de Données de Production

**Les tests de comportement utilisent TOUJOURS une base de données de test isolée.**

**La base de données de production (`base_de_datos/facturacion.db`) n'est JAMAIS touchée par les tests.**

## 🔒 Comment fonctionne l'isolation ?

### 1. Fixtures Automatiques (conftest.py)

Le fichier `test/conftest.py` contient des fixtures pytest qui sont **automatiquement appliquées** à tous les tests :

```python
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch, temp_db, request):
    """Configurar entorno de test automáticamente"""
    # Remplacer la base de données globale par une base de test
    monkeypatch.setattr('database.database.db', temp_db)
    monkeypatch.setattr('database.models.db', temp_db)
```

**`autouse=True`** signifie que cette fixture est appliquée automatiquement à **TOUS** les tests, sans avoir besoin de l'injecter explicitement.

### 2. Base de Données Temporaire

Chaque test utilise une base de données temporaire créée dans `/tmp/` :

```python
@pytest.fixture
def temp_db(request):
    """Base de datos temporal para tests"""
    test_db, db_path = test_db_manager.create_test_database(test_name)
    yield test_db
    # Nettoyage automatique à la fin du test
```

### 3. Nettoyage Automatique

À la fin de chaque test, la base de données temporaire est **automatiquement supprimée** :

```
10:22:34 - INFO - Toutes les ressources de test nettoyées
```

## 📋 Exemple : Tests de Tri des Tables

Le fichier `test/behaviour/test_table_sorting_behaviour.py` utilise cette isolation automatique :

```python
class TestTableSortingBehaviour:
    """Tests de comportement pour le tri des colonnes dans les tables
    
    IMPORTANT: Ces tests utilisent les fixtures automatiques du conftest.py
    qui remplacent la base de données de production par une base de test isolée.
    Aucune donnée de production n'est modifiée.
    """
    
    def setup_method(self):
        """Configuration avant chaque test"""
        self.logger = get_logger(self.__class__.__name__)
        # Pas besoin de créer manuellement une base de test
        # La fixture 'temp_db' est automatiquement injectée
```

## ✅ Vérification

Pour vérifier que les tests utilisent bien une base de test isolée, regardez les logs :

```
INFO - Base de données de test créée: test_test_01_facturas_table_sorting_enabled_72yk744c.db
```

Le nom du fichier contient :
- `test_` : préfixe indiquant qu'il s'agit d'un test
- Nom du test : `test_01_facturas_table_sorting_enabled`
- Hash aléatoire : `72yk744c` (pour éviter les conflits)

## 🚀 Exécution des Tests

```bash
# Exécuter tous les tests de tri
pytest test/behaviour/test_table_sorting_behaviour.py -v

# Tous les tests passent et utilisent une base de test isolée
# ✅ 9 passed in 2.51s
```

## 📊 Résumé

| Aspect | Détail |
|--------|--------|
| **Base de production** | `base_de_datos/facturacion.db` |
| **Base de test** | `/tmp/test_<nom_test>_<hash>.db` |
| **Protection** | Automatique via fixtures pytest |
| **Nettoyage** | Automatique à la fin de chaque test |
| **Isolation** | Complète - aucune interaction avec la production |

## 🔍 Fichiers Importants

1. **`test/conftest.py`** : Configuration globale des fixtures
2. **`test/utils/test_database_manager.py`** : Gestionnaire de bases de test
3. **`database/test_database.py`** : Classe TestDatabase
4. **`database/fixtures.py`** : Données de test standardisées

## ⚠️ Note pour les Développeurs

**Vous n'avez PAS besoin de gérer manuellement l'isolation de la base de données dans vos tests.**

Les fixtures pytest s'en occupent automatiquement. Il suffit d'écrire vos tests normalement :

```python
def test_my_feature(self):
    # La base de test est déjà configurée
    window = MyWindow()
    # Vos assertions ici
```

**La base de production est protégée automatiquement.** ✅

