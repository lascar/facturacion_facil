> **[⬆️ Volver al índice](../INDEX.md)** | **[🔧 Refactoring](README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🔧 Refactorisation : Organisation - config.json comme Source Unique de Vérité

> **Date** : 2026-01-21  
> **Type** : Refactorisation majeure  
> **Impact** : Architecture, Persistance des données

---

## 📋 Problème Initial

### Symptômes
- La fenêtre **Organización** affichait un formulaire vide malgré des données présentes dans `config/config.json`
- Confusion entre deux sources de données : base de données SQLite et fichier JSON
- Perte de données de configuration lors des tests

### Cause Racine
Le code chargeait les données depuis **deux sources** :
1. **Base de données** (`organizacion` table) via `OrganizacionService`
2. **Fichier JSON** (`config/config.json`)

La base de données était **vide**, donc le formulaire restait vide même si `config.json` contenait des données valides.

---

## ✅ Solution Implémentée

### Décision Architecturale
**`config/config.json` est maintenant la SEULE source de vérité pour les données d'organisation.**

### Raisons
1. ✅ **Simplicité** : Une seule source de données, pas de synchronisation nécessaire
2. ✅ **Portabilité** : Fichier JSON facile à sauvegarder/restaurer
3. ✅ **Lisibilité** : Format texte lisible par l'humain
4. ✅ **Versionnable** : Peut être versionné dans Git si nécessaire
5. ✅ **Pas de migration** : Pas besoin de migrer la structure de la table

---

## 🔧 Modifications Effectuées

### 1. Fichier `ui/organizacion_pyqt5.py`

#### Imports Supprimés
```python
# SUPPRIMÉ :
# from database import database
# from services.organizacion_service import OrganizacionService
# from utils.exceptions import (
#     OrganizationValidationError, OrganizationNotFoundError, DatabaseError
# )
```

#### Initialisation Modifiée
```python
# AVANT :
def __init__(self, parent=None):
    # ...
    db_path = database.db.db_path if hasattr(database.db, 'db_path') else None
    self.organizacion_service = OrganizacionService(db_path)

# APRÈS :
def __init__(self, parent=None):
    # ...
    self.config_file = "config/config.json"
    # Plus de OrganizacionService !
```

#### Méthode `load_organizacion()` Refactorisée
```python
# AVANT : Chargeait depuis la base de données
def load_organizacion(self):
    organizacion = self.organizacion_service.get_organizacion()
    if organizacion:
        self.load_organization_data(organizacion)

# APRÈS : Charge UNIQUEMENT depuis config.json
def load_organizacion(self):
    config_data = self.load_config_json()
    if config_data:
        self.load_organization_data(config_data)
    else:
        self.clear_form()
```

#### Méthode `save_organizacion()` Refactorisée
```python
# AVANT : Sauvegardait dans la base de données + config.json partiel
def save_organizacion(self):
    # Validation
    organizacion_data = {...}
    # Sauvegarder dans la base de données
    self.organizacion_service.save_organizacion(organizacion_data)
    # Sauvegarder partiellement dans config.json
    self.save_to_config_json(partial_data)

# APRÈS : Sauvegarde TOUT dans config.json uniquement
def save_organizacion(self):
    # Validation
    organizacion_data = {...}
    # Sauvegarder TOUT dans config.json
    if self.save_all_to_config_json(organizacion_data):
        self.show_info("Éxito", "Configuración actualizada correctamente")
        self.load_organizacion()
```

#### Nouvelle Méthode `save_all_to_config_json()`
```python
def save_all_to_config_json(self, organizacion_data):
    """Sauvegarder TOUTES les données de l'organisation dans config.json"""
    try:
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        config = {}
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        # Mettre à jour toutes les valeurs
        config['organizacion_defaults'] = organizacion_data
        
        # Sauvegarder
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        self.logger.error(f"Erreur sauvegarde config.json: {e}")
        return False
```

### 2. Fichier `ui/main_window_pyqt5.py`

#### Problème de Rechargement
La fenêtre était **réutilisée** sans recharger les données :

```python
# AVANT : Pas de rechargement !
def open_organizacion(self):
    if self.organizacion_window is None:
        self.organizacion_window = OrganizacionPyQt5Window()
    self.organizacion_window.show()  # ❌ Données pas rechargées !
```

#### Solution : Rechargement Forcé
```python
# APRÈS : Rechargement à chaque ouverture
def open_organizacion(self):
    if self.organizacion_window is None:
        self.organizacion_window = OrganizacionPyQt5Window()
    else:
        # ✅ Forcer le rechargement depuis config.json
        self.organizacion_window.load_organizacion()
    self.organizacion_window.show()
```

---

## 🧪 Tests BDD Créés

### Fichier `test/behaviour/test_organizacion_config_json_only_behaviour.py`

**6 tests comportementaux** pour garantir que `config.json` est la seule source de vérité :

1. **`test_01_organizacion_window_no_database_imports`**
   - Vérifie qu'il n'y a AUCUN import de `database` ou `OrganizacionService`

2. **`test_02_organizacion_loads_from_config_json_only`**
   - Vérifie que les données sont chargées depuis `config.json` UNIQUEMENT

3. **`test_03_organizacion_saves_to_config_json_only`**
   - Vérifie que les données sont sauvegardées dans `config.json` UNIQUEMENT

4. **`test_04_organizacion_window_has_no_organizacion_service`**
   - Vérifie qu'il n'y a PAS d'attribut `organizacion_service`

5. **`test_05_organizacion_uses_save_all_to_config_json`**
   - Vérifie que la méthode `save_all_to_config_json` existe

6. **`test_06_organizacion_persistence_across_reopens`**
   - Vérifie que les données persistent entre les ouvertures de fenêtre

### Exécution des Tests
```bash
# Tous les tests
pytest test/behaviour/test_organizacion_config_json_only_behaviour.py -v

# Un test spécifique
pytest test/behaviour/test_organizacion_config_json_only_behaviour.py::TestOrganizacionConfigJsonOnlyBehaviour::test_06_organizacion_persistence_across_reopens -v
```

---

## 📊 Impact et Bénéfices

### Avant la Refactorisation
- ❌ Deux sources de données (base de données + config.json)
- ❌ Synchronisation manuelle nécessaire
- ❌ Risque de désynchronisation
- ❌ Formulaire vide si la base de données est vide
- ❌ Complexité accrue (OrganizacionService, exceptions, etc.)

### Après la Refactorisation
- ✅ Une seule source de vérité : `config/config.json`
- ✅ Pas de synchronisation nécessaire
- ✅ Données toujours disponibles
- ✅ Code simplifié (moins de dépendances)
- ✅ Tests BDD garantissent le comportement
- ✅ Rechargement automatique à chaque ouverture

---

## 🔒 Protection des Données

### Backup Automatique dans `actualizar.bat`
Le script de mise à jour crée automatiquement un backup de `config/config.json` :

```batch
:: Respaldo de configuración
if exist "config\config.json" (
    copy "config\config.json" "backup\config_%FECHA%.json" >nul
    if %errorlevel%==0 (
        echo ✅ Configuración respaldada: backup\config_%FECHA%.json
    )
)
```

### Backup Automatique dans `run_organized_tests.sh`
Le script de tests crée et restaure automatiquement `config/config.json` :

```bash
# Backup avant les tests
backup_config_json

# Exécution des tests
pytest ...

# Restauration après les tests
restore_config_json
```

---

## 📁 Fichiers Modifiés

### Code Source
- **`ui/organizacion_pyqt5.py`** - Refactorisation complète (suppression dépendances DB)
- **`ui/main_window_pyqt5.py`** - Ajout rechargement forcé

### Tests
- **`test/behaviour/test_organizacion_config_json_only_behaviour.py`** - Nouveau fichier (6 tests BDD)

### Documentation
- **`docs/dev/refactoring/ORGANIZACION_CONFIG_JSON_REFACTORING.md`** - Ce document

---

## 🔗 Voir Aussi

- **[PROTECTION_FICHIERS_PRODUCTION.md](../testing/PROTECTION_FICHIERS_PRODUCTION.md)** - Protection de config.json pendant les tests
- **[ARCHITECTURE.md](../ARCHITECTURE.md)** - Architecture générale du projet
- **[actualizar.bat](../../../actualizar.bat)** - Script de mise à jour avec backup

---

## 📅 Historique

| Date | Action | Auteur |
|------|--------|--------|
| 2026-01-21 | Refactorisation complète : config.json comme source unique | Équipe dev |
| 2026-01-21 | Ajout rechargement forcé dans main_window_pyqt5.py | Équipe dev |
| 2026-01-21 | Création tests BDD (6 tests) | Équipe dev |
| 2026-01-21 | Documentation créée | Équipe dev |

---

**Dernière mise à jour** : 2026-01-21
**Auteur** : Équipe de développement
**Statut** : ✅ Complété et testé

