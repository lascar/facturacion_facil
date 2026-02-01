> **[⬆️ Volver al índice](../INDEX.md)** | **[📦 Features](README.md)** | **[🏠 Inicio](../../README.md)**

---

# 📄 Contrôles de Visibilité PDF - Conditions de Paiement, Forma de Pago et Informations Légales

> **Date** : 2026-02-01  
> **Statut** : ✅ Implémenté et testé  
> **Version** : 2.0

---

## 📋 Vue d'ensemble

Cette fonctionnalité permet de contrôler la visibilité des sections "Condiciones de Pago", "Forma de Pago" et "Información Legal" dans les PDFs de factures générés par l'application.

### Architecture

Toute la configuration de l'organisation est stockée dans **`config/config.json`** avec un système de cache en mémoire. La base de données n'est plus utilisée pour ces données.

```
┌─────────────────────────────────────────────┐
│         CONFIGURATION ORGANISATION          │
│                                             │
│  config.json (SOURCE UNIQUE)                │
│  ├── organizacion_defaults                  │
│  │   ├── nombre, direccion, telefono       │
│  │   ├── email, cif, logo_path             │
│  │   ├── numero_factura_inicial            │
│  │   ├── condiciones_pago / _visible       │
│  │   ├── forma_pago / _visible             │
│  │   └── informacion_legal / _visible      │
│  │                                          │
│  └── Cache (functools.lru_cache)            │
│      ├── get_config() → lecture avec cache  │
│      ├── save_config() → écriture + invalide│
│      └── invalidate_config_cache()          │
│                                             │
└─────────────────────────────────────────────┘
```

### Compatibilité Rétroactive

L'API `Organizacion.get()` et `Organizacion.save()` reste inchangée pour maintenir la compatibilité avec le code existant. Si `config.json` est vide, une **migration automatique** depuis la base de données est effectuée.

---

## ✨ Fonctionnalités

### Interface Utilisateur

**Localisation** : Fenêtre "Configuración de la Organización"

Trois nouvelles cases à cocher ont été ajoutées :
- ✅ **"Visible en los PDF"** sous le champ "Condiciones de Pago"
- ✅ **"Visible en los PDF"** sous le champ "Forma de Pago"
- ✅ **"Visible en los PDF"** sous le champ "Información Legal"

**Comportement par défaut** : Les trois cases sont cochées (sections visibles)

### Configuration

**Fichier** : `config/config.json`

Structure complète :
```json
{
  "organizacion_defaults": {
    "nombre": "Mi Empresa",
    "direccion": "Calle Principal, 123",
    "telefono": "+34 123 456 789",
    "email": "contacto@miempresa.com",
    "cif": "B12345678",
    "logo_path": "logo/logo.png",
    "numero_factura_inicial": "1",
    "condiciones_pago": "...",
    "forma_pago": "...",
    "informacion_legal": "...",
    "condiciones_pago_visible": 1,
    "forma_pago_visible": 1,
    "informacion_legal_visible": 1
  }
}
```

**Valeurs des flags de visibilité** :
- `1` = Section visible dans les PDFs
- `0` = Section masquée dans les PDFs

### Génération PDF

Le générateur PDF vérifie les flags de visibilité avant d'inclure les sections dans le footer.

**Logique** :
- Si `condiciones_pago_visible == 0` → Section "CONDICIONES DE PAGO" non affichée
- Si `forma_pago_visible == 0` → Section "FORMA DE PAGO" non affichée
- Si `informacion_legal_visible == 0` → Section "INFORMACIÓN LEGAL" non affichée

---

## 🔧 Implémentation Technique

### Fichiers Modifiés

#### 1. **Configuration** (`config/config.py`)

**Nouveau système de cache** :
```python
# Cache global
_config_cache = {}

def get_config(config_file=None):
    """Obtient la configuration avec cache"""
    
def save_config(config_data, config_file=None):
    """Sauvegarde et invalide le cache automatiquement"""
    
def invalidate_config_cache(config_file=None):
    """Invalide le cache pour forcer le rechargement"""
```

**Classe Config** (compatible legacy) :
```python
class Config:
    def reload(self):
        """Recharge depuis le fichier (invalide le cache)"""
        
    def get_organizacion_defaults(self):
        """Obtient les valeurs depuis config.json"""
        
    def set_organizacion_defaults(self, data):
        """Définit les valeurs et sauvegarde"""
```

#### 2. **Modèle** (`database/models.py`)

**Classe Organizacion** (API inchangée, implémentation modifiée) :

```python
class Organizacion:
    """
    Modelo de Organizacion - AHORA USA config.json (no base de datos)
    
    Mantiene compatibilidad: Organizacion.get() y Organizacion.save()
    """
    
    def save(self):
        """Guarda en config.json (no en DB)"""
        from config.config import get_config, save_config
        # ...
    
    @staticmethod
    def get():
        """Obtiene desde config.json (con fallback a DB para migración)"""
        from config.config import get_config
        # Si config.json vacío → migra desde DB → guarda en config.json
```

**Compatibilité** : Le code existant utilisant `Organizacion.get()` et `Organizacion.save()` continue de fonctionner sans modification.

#### 3. **Interface** (`ui/organizacion_pyqt5.py`)

**Modifications** :
- Utilise `get_config()` pour le chargement (avec cache)
- Appelle `invalidate_config_cache()` après sauvegarde
- Plus de sauvegarde dans la base de données

```python
def save_organizacion(self):
    # Sauvegarder dans config.json
    config_saved = self.save_all_to_config_json(organizacion_data)
    
    if config_saved:
        # Invalider le cache pour forcer le rechargement
        from config.config import invalidate_config_cache
        invalidate_config_cache(self.config_file)
```

#### 4. **Générateur PDF** (`utils/pdf_generator.py`)

Lecture depuis config.json via le cache :
```python
def load_config_data(self):
    from config.config import get_config
    config = get_config(self.config_file)
    return config.get('organizacion_defaults', {})
```

---

## 🔄 Migration depuis la Base de Données

### Processus Automatique

Lors du premier accès après la mise à jour :

1. `Organizacion.get()` vérifie config.json
2. Si vide → lit la base de données (table `organizacion`)
3. Migre les données vers config.json
4. Sauvegarde dans config.json
5. Affiche : "🔄 Migración automática: Datos de organización migrados de DB a config.json"

### Données Migrées

| Champ | Source → Destination |
|-------|---------------------|
| `nombre` | DB.organizacion → config.json |
| `direccion` | DB.organizacion → config.json |
| `telefono` | DB.organizacion → config.json |
| `email` | DB.organizacion → config.json |
| `cif` | DB.organizacion → config.json |
| `logo_path` | DB.organizacion → config.json |
| `numero_factura_inicial` | DB.organizacion → config.json |

**Note** : La table `organizacion` dans la DB est préservée mais ignorée après migration.

---

## 🧪 Tests

### Structure des Tests

**Fichiers de Tests** :
- `test/unit/test_models.py::TestOrganizacion` (6 tests unitaires)
- `test/behaviour/test_organizacion_visibility_checkboxes_behaviour.py` (4 tests)
- `test/behaviour/test_organizacion_forma_pago_behaviour.py` (5 tests)
- `test/behaviour/test_forma_pago_pdf_visibility_behaviour.py` (5 tests)

### Tests Unitaires - Organizacion

| Test | Description |
|------|-------------|
| `test_organizacion_creation` | Création d'une organisation |
| `test_organizacion_creation_with_defaults` | Valeurs par défaut |
| `test_organizacion_save_new` | Sauvegarde dans config.json |
| `test_organizacion_save_update` | Mise à jour config.json |
| `test_organizacion_get` | Récupération depuis config.json |
| `test_organizacion_get_empty` | Comportement si vide |

### Tests de Comportement

**14 tests de comportement** :
- 4 tests : Condiciones de Pago / Información Legal
- 5 tests : Forma de Pago (UI)
- 5 tests : Visibilité PDF Forma de Pago

### Exécution

```bash
# Tests unitaires
pytest test/unit/test_models.py::TestOrganizacion -v

# Tests de comportement
pytest test/behaviour/test_organizacion_forma_pago_behaviour.py -v
pytest test/behaviour/test_forma_pago_pdf_visibility_behaviour.py -v

# Tous les tests
pytest test/ -v
```

**Résultat** : ✅ 401+ tests passent

---

## 📝 Utilisation

### Pour l'Utilisateur Final

1. Ouvrir **"Configuración de la Organización"**
2. Remplir tous les champs
3. Cocher/décocher les cases **"✓ Visible en los PDF"**
4. Cliquer sur **"💾 Guardar Configuración"**
5. Les PDFs générés respecteront les choix de visibilité

### Pour les Développeurs

**Lecture de la configuration** :
```python
from database.models import Organizacion

# Lecture avec cache automatique
org = Organizacion.get()
print(org.nombre, org.cif)
```

**Sauvegarde (invalide le cache automatiquement)** :
```python
org = Organizacion()
org.nombre = "Nueva Empresa"
org.save()  # Sauvegarde dans config.json + invalide cache
```

**Forcer le rechargement** :
```python
from config.config import invalidate_config_cache
invalidate_config_cache()
```

---

## 🔒 Protection des Données de Production

Le script `test/verifier_protection_tests.py` est exécuté automatiquement par `run_organized_tests.sh` avant tout test. Il bloque l'exécution si des données de test sont détectées dans :

| Source | Critère de détection | Action |
|--------|---------------------|--------|
| **Base de données** | Produits/factures/clients avec "Test" | ❌ Bloque |
| **config.json** | Nom/email contenant "test" ou "empresa" | ❌ Bloque |
| **Organisation DB** | Nom contenant "test" | ❌ Bloque |
| **Protection PYTEST_RUNNING** | Absent de database.py | ❌ Bloque |

**Commande de vérification manuelle :**
```bash
python3 test/verifier_protection_tests.py
```

---

## 🔗 Voir Aussi

- **[PDF_FEATURES_SUMMARY.md](PDF_FEATURES_SUMMARY.md)** - Vue d'ensemble des fonctionnalités PDF
- **[PROTECTION_FICHIERS_PRODUCTION.md](../testing/PROTECTION_FICHIERS_PRODUCTION.md)** - Protection des fichiers de production

---

**Dernière mise à jour** : 2026-02-01  
**Auteur** : Équipe de développement
