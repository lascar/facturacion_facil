# 🔒 Protection du Fichier config.json en Tests

## 🎯 Objectif

**Garantir que les tests n'utilisent JAMAIS le fichier `config/config.json` de production**, mais un fichier de test isolé `config_test.json` qui est automatiquement créé et nettoyé.

## ⚠️ Problème Résolu

### Avant
Les tests modifiaient directement `config/config.json` :
- ❌ Risque de corruption des données de production
- ❌ Pollution entre tests
- ❌ Nécessité de backup/restore manuel
- ❌ Données de test mélangées avec données réelles

### Après
Les tests utilisent un fichier isolé `config_test.json` :
- ✅ Isolation complète de la production
- ✅ Nettoyage automatique après chaque test
- ✅ Pas de backup/restore nécessaire
- ✅ Données de test séparées

## 🏗️ Architecture

### Composants Modifiés

#### 1. **OrganizacionPyQt5Window** (`ui/organizacion_pyqt5.py`)
```python
def __init__(self, parent=None, config_file=None):
    # Utiliser config_test.json en mode test, sinon config.json
    if config_file is not None:
        self.config_file = config_file
    else:
        import os
        self.config_file = os.environ.get('CONFIG_FILE', 'config/config.json')
```

#### 2. **Config** (`config/config.py`)
```python
def __init__(self, config_file=None):
    # Utiliser config_test.json en mode test, sinon config.json
    if config_file is not None:
        self.config_file = config_file
    else:
        self.config_file = os.environ.get('CONFIG_FILE', 'config/config.json')
```

#### 3. **Fixture pytest** (`test/behaviour/conftest.py`)
```python
@pytest.fixture(scope="function")
def isolated_test_config():
    """Créer un fichier config_test.json isolé pour chaque test"""
    # Créer un fichier config temporaire
    temp_dir = tempfile.mkdtemp(prefix="config_test_")
    config_path = os.path.join(temp_dir, "config_test.json")
    
    # Créer un config vide avec structure par défaut
    default_config = {
        "organizacion_defaults": { ... }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    yield config_path
    
    # Nettoyage automatique
    shutil.rmtree(temp_dir)
```

## 🚀 Utilisation

### Pour les Tests de Comportement

Les tests de comportement utilisent **automatiquement** le fichier config de test via la fixture `app_instance` :

```python
class TestOrganizacionConfigJsonOnlyBehaviour(BaseBehaviourTest):
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, mock_messagebox, mock_filedialog):
        """Configuration du test avec l'application"""
        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        
        # Le fichier config de test est automatiquement configuré
        self.config_file = os.environ.get('CONFIG_FILE', 'config/config.json')
        
        yield
        
        # Nettoyage automatique - pas besoin de restaurer
```

### Pour les Tests Unitaires

Pour les tests unitaires qui utilisent directement `Config` ou `OrganizacionPyQt5Window` :

```python
def test_config_isolation(isolated_test_config):
    """Test avec config isolé"""
    # Créer une instance avec le config de test
    config = Config(config_file=isolated_test_config)
    
    # Modifier le config sans affecter la production
    config.set('test_key', 'test_value')
    config.save_config()
    
    # Le fichier sera automatiquement nettoyé après le test
```

## 📋 Checklist de Conformité

Avant de créer un test qui utilise config.json, vérifier :

- [ ] ✅ Le test utilise la fixture `isolated_test_config` ou `app_instance`
- [ ] ✅ Le test ne référence PAS directement `config/config.json`
- [ ] ✅ Le test utilise `os.environ.get('CONFIG_FILE')` pour obtenir le chemin
- [ ] ❌ Le test ne crée PAS de backup manuel de config.json
- [ ] ❌ Le test ne restaure PAS manuellement config.json
- [ ] ✅ Le test laisse le nettoyage à la fixture

## 🔍 Vérification

### Vérifier qu'un Test Utilise le Config Isolé

```python
def test_verification(isolated_test_config):
    """Vérifier que le config de test est utilisé"""
    config_path = os.environ.get('CONFIG_FILE')
    assert 'config_test' in config_path
    assert config_path != 'config/config.json'
```

### Lancer les Tests

```bash
# Les tests utilisent automatiquement config_test.json
python -m pytest test/behaviour/test_organizacion_config_json_only_behaviour.py -v
```

## 📊 Avantages

- 🔒 **Sécurité** : config.json de production jamais touché
- 🧹 **Propreté** : Nettoyage automatique après chaque test
- ⚡ **Performance** : Pas de backup/restore manuel
- 🔧 **Simplicité** : Utilisation transparente via fixtures
- 🧪 **Fiabilité** : Tests vraiment isolés

---

**Date de création** : 2026-01-22  
**Statut** : **ACTIF ET OBLIGATOIRE**  
**Révision** : Annuelle ou après incident

