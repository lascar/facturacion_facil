# 🔧 Tests Unitaires

## 📋 **Description**
Tests de composants individuels isolés - validation des fonctions, classes et méthodes de base.

## 📁 **Contenu du Répertoire**
```
unit/
├── README.md                           # Ce guide
├── test_database.py                    # Tests base de données
├── test_models.py                      # Tests modèles de données
├── test_factura_models.py              # Tests modèles factures
├── test_validators.py                  # Tests validateurs
├── test_translations.py                # Tests traductions
├── test_parametrized.py                # Tests paramétrés
├── test_security.py                    # Tests sécurité
├── test_validate_form.py               # Tests validation formulaires
├── test_validacion_facturas_opcional.py # Tests validation facturas
├── test_ejemplos_validacion_facturas.py # Exemples validation
├── test_stock_models.py                # Tests modèles stock
├── test_logging_system.py              # Tests système de logs
├── test_pytest_markers.py              # Tests marqueurs pytest
└── test_file_manager.py                # Tests architecture factorée
```

## 🚀 **Exécution des Tests**

### **Tous les Tests Unitaires**
```bash
# Depuis la racine du projet
./run_organized_tests.sh unit

# Avec pytest directement
pytest test/unit/

# Mode verbose
./run_organized_tests.sh unit -v

# Mode silencieux
./run_organized_tests.sh unit -q
```

### **Tests Spécifiques**
```bash
# Tests de base de données
./run_organized_tests.sh unit -k database
pytest test/unit/test_database.py

# Tests de modèles
./run_organized_tests.sh unit -k models
pytest test/unit/test_models.py test/unit/test_factura_models.py

# Tests de validation
./run_organized_tests.sh unit -k valid
pytest test/unit/test_validators.py test/unit/test_validate_form.py

# Tests de sécurité
pytest test/unit/test_security.py

# Tests de logging
pytest test/unit/test_logging_system.py

# Tests architecture factorée
./run_organized_tests.sh unit -k file_manager
pytest test/unit/test_file_manager.py
```

### **Avec Couverture de Code**
```bash
# Couverture pour les modules principaux
./run_organized_tests.sh unit --cov=database --cov=utils --cov=common

# Rapport HTML de couverture
./run_organized_tests.sh unit --cov=database --cov-report=html

# Couverture détaillée
pytest test/unit/ --cov=database --cov=utils --cov-report=term-missing
```

## 📊 **Statistiques**
- **Nombre de fichiers** : 14 fichiers de test
- **Tests estimés** : ~55 tests
- **Couverture** : Base de données, modèles, validateurs, utilitaires
- **Temps d'exécution** : ~30-45 secondes

## 🎯 **Objectifs des Tests**

### **Tests de Base de Données**
- Connexion et configuration
- Opérations CRUD de base
- Intégrité des données
- Gestion des erreurs

### **Tests de Modèles**
- Création et validation d'objets
- Relations entre modèles
- Méthodes de calcul
- Sérialisation/désérialisation

### **Tests de Validation**
- Validation des formulaires
- Règles métier
- Gestion des erreurs de saisie
- Formats de données

### **Tests de Sécurité**
- Validation des entrées
- Protection contre injections
- Gestion des permissions
- Chiffrement des données sensibles

## 🔧 **Configuration**

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Dépendances installées
pip install pytest pytest-cov hypothesis
```

### **Variables d'Environnement**
```bash
# Base de données de test
export TEST_DATABASE=":memory:"

# Niveau de log pour les tests
export LOG_LEVEL=WARNING

# Mode debug
export PYTEST_DEBUG=1
```

## 📋 **Bonnes Pratiques**

### **Exécution Pendant le Développement**
```bash
# Tests rapides avec arrêt au premier échec
./run_organized_tests.sh unit -x

# Tests avec output détaillé
./run_organized_tests.sh unit -v -s

# Tests d'un module spécifique
pytest test/unit/test_models.py -v
```

### **Avant Commit**
```bash
# Tests complets avec couverture
./run_organized_tests.sh unit --cov=database --cov=utils

# Vérification de la qualité
./run_organized_tests.sh unit --tb=short
```

### **Debug de Tests**
```bash
# Mode debug avec prints
pytest test/unit/test_specific.py -s -vv

# Avec pdb pour debugging
pytest test/unit/test_specific.py --pdb

# Tests les plus lents
pytest test/unit/ --durations=10
```

## 🐛 **Dépannage**

### **Erreurs Courantes**
```bash
# Import errors
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Base de données locked
rm -f test_database.db

# Permissions
chmod +x run_organized_tests.sh
```

### **Tests Qui Échouent**
```bash
# Voir les détails des échecs
./run_organized_tests.sh unit --tb=long

# Relancer seulement les tests échoués
./run_organized_tests.sh unit --lf

# Tests échoués en premier
./run_organized_tests.sh unit --ff
```

## 📈 **Métriques de Qualité**

### **Couverture Attendue**
- **Base de données** : >80%
- **Modèles** : >90%
- **Validateurs** : >95%
- **Utilitaires** : >70%

### **Performance**
- **Temps total** : <60 secondes
- **Tests individuels** : <1 seconde
- **Setup/teardown** : <5 secondes

## 🎯 **Ajout de Nouveaux Tests**

### **Structure de Test**
```python
import pytest
from module_to_test import ClassToTest

class TestClassName:
    def setup_method(self):
        """Setup avant chaque test"""
        pass
    
    def test_specific_functionality(self):
        """Test d'une fonctionnalité spécifique"""
        # Arrange
        # Act
        # Assert
        pass
    
    def teardown_method(self):
        """Nettoyage après chaque test"""
        pass
```

### **Conventions de Nommage**
- **Fichiers** : `test_[module].py`
- **Classes** : `TestClassName`
- **Méthodes** : `test_specific_functionality`
- **Fixtures** : `@pytest.fixture`

---

**Pour plus d'informations, consultez le guide principal : `../README.md`**
