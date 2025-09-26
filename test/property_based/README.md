# 🎲 Tests Property-Based

## 📋 **Description**
Tests avec génération automatique de données - validation des propriétés avec Hypothesis.

## 📁 **Contenu du Répertoire**
```
property_based/
├── README.md                    # Ce guide
└── test_property_based.py       # Tests avec Hypothesis
```

## 🚀 **Exécution des Tests**

### **Tous les Tests Property-Based**
```bash
# Depuis la racine du projet
./run_organized_tests.sh property

# Avec pytest directement
pytest test/property_based/

# Mode verbose avec exemples
./run_organized_tests.sh property -v

# Avec statistiques Hypothesis
./run_organized_tests.sh property --hypothesis-show-statistics
```

### **Tests avec Configuration Hypothesis**
```bash
# Plus d'exemples générés
pytest test/property_based/ --hypothesis-max-examples=1000

# Mode debug Hypothesis
pytest test/property_based/ --hypothesis-verbosity=verbose

# Seed fixe pour reproductibilité
pytest test/property_based/ --hypothesis-seed=12345

# Profile spécifique
pytest test/property_based/ --hypothesis-profile=dev
```

### **Tests Property-Based Spécifiques**
```bash
# Tests de calculs
pytest test/property_based/test_property_based.py -k calculation

# Tests de validation
pytest test/property_based/test_property_based.py -k validation

# Tests de modèles
pytest test/property_based/test_property_based.py -k model

# Tests de formats
pytest test/property_based/test_property_based.py -k format
```

## 📊 **Statistiques**
- **Nombre de fichiers** : 1 fichier principal
- **Tests estimés** : ~13 tests
- **Couverture** : Calculs, validation, modèles, formats
- **Temps d'exécution** : ~45-60 secondes

## 🎯 **Objectifs des Tests**

### **Validation de Propriétés**
- Invariants mathématiques
- Propriétés de symétrie
- Comportements limites
- Robustesse des fonctions

### **Génération Automatique**
- **Données aléatoires** : Hypothesis génère les cas de test
- **Cas limites** : Détection automatique des edge cases
- **Réduction** : Simplification des cas d'échec
- **Reproductibilité** : Seeds pour reproduire les échecs

## 🔧 **Configuration**

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Hypothesis installé
pip install hypothesis

# Configuration Hypothesis
export HYPOTHESIS_PROFILE=dev
```

### **Variables d'Environnement**
```bash
# Profil Hypothesis
export HYPOTHESIS_PROFILE=dev  # ou ci, debug

# Nombre d'exemples
export HYPOTHESIS_MAX_EXAMPLES=100

# Verbosité
export HYPOTHESIS_VERBOSITY=normal

# Répertoire de base de données
export HYPOTHESIS_DATABASE_FILE=.hypothesis/examples
```

## 📋 **Types de Tests Property-Based**

### **Tests de Calculs Mathématiques**
```bash
# Propriétés arithmétiques
pytest test/property_based/ -k "arithmetic" --hypothesis-show-statistics

# Calculs de pourcentages
pytest test/property_based/ -k "percentage" -v

# Calculs de totaux
pytest test/property_based/ -k "total" -v
```

### **Tests de Validation de Données**
```bash
# Validation formats
pytest test/property_based/ -k "format" --hypothesis-verbosity=verbose

# Validation contraintes
pytest test/property_based/ -k "constraint" -v

# Validation types
pytest test/property_based/ -k "type" -v
```

### **Tests de Modèles de Données**
```bash
# Propriétés des modèles
pytest test/property_based/ -k "model" --hypothesis-show-statistics

# Sérialisation/désérialisation
pytest test/property_based/ -k "serialize" -v

# Invariants d'objets
pytest test/property_based/ -k "invariant" -v
```

## 🚀 **Exécution Avancée**

### **Tests avec Profils Hypothesis**
```bash
# Profil développement (rapide)
pytest test/property_based/ --hypothesis-profile=dev

# Profil CI (plus d'exemples)
pytest test/property_based/ --hypothesis-profile=ci

# Profil debug (très verbeux)
pytest test/property_based/ --hypothesis-profile=debug
```

### **Tests avec Contrôle de Génération**
```bash
# Beaucoup d'exemples
pytest test/property_based/ --hypothesis-max-examples=1000

# Exemples minimaux
pytest test/property_based/ --hypothesis-max-examples=10

# Avec seed fixe
pytest test/property_based/ --hypothesis-seed=42

# Deadline étendue
pytest test/property_based/ --hypothesis-deadline=1000
```

### **Debug et Analyse**
```bash
# Mode très verbeux
pytest test/property_based/ --hypothesis-verbosity=debug

# Statistiques détaillées
pytest test/property_based/ --hypothesis-show-statistics

# Exemples qui échouent
pytest test/property_based/ -v --tb=short
```

## 📈 **Concepts Hypothesis**

### **Stratégies de Génération**
```python
from hypothesis import strategies as st

# Entiers dans une plage
st.integers(min_value=0, max_value=100)

# Texte avec contraintes
st.text(min_size=1, max_size=50)

# Listes de données
st.lists(st.integers(), min_size=1, max_size=10)

# Objets complexes
st.builds(MyClass, field1=st.text(), field2=st.integers())
```

### **Propriétés Testées**
```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Addition est commutative"""
    assert a + b == b + a

@given(st.floats(min_value=0, max_value=100))
def test_percentage_calculation(value):
    """Calcul de pourcentage cohérent"""
    result = calculate_percentage(value, 21.0)
    assert 0 <= result <= value * 1.21
```

## 🐛 **Dépannage**

### **Tests Property-Based qui Échouent**
```bash
# Voir l'exemple qui échoue
pytest test/property_based/ -v --tb=long

# Reproduire avec le même seed
pytest test/property_based/ --hypothesis-seed=SEED_FROM_FAILURE

# Mode debug pour comprendre
pytest test/property_based/ --hypothesis-verbosity=debug
```

### **Génération Trop Lente**
```bash
# Réduire le nombre d'exemples
pytest test/property_based/ --hypothesis-max-examples=50

# Profil plus rapide
pytest test/property_based/ --hypothesis-profile=dev

# Deadline plus courte
pytest test/property_based/ --hypothesis-deadline=200
```

### **Cas Limites Non Trouvés**
```bash
# Plus d'exemples
pytest test/property_based/ --hypothesis-max-examples=1000

# Profil exhaustif
pytest test/property_based/ --hypothesis-profile=ci

# Stratégies plus larges
# Modifier les stratégies dans le code de test
```

## 📊 **Analyse des Résultats**

### **Statistiques Hypothesis**
```bash
# Voir les statistiques de génération
pytest test/property_based/ --hypothesis-show-statistics

# Analyser la couverture des cas
pytest test/property_based/ --hypothesis-verbosity=verbose

# Distribution des exemples générés
pytest test/property_based/ -v
```

### **Exemples Intéressants**
```bash
# Hypothesis sauvegarde les exemples intéressants
ls .hypothesis/examples/

# Rejouer des exemples spécifiques
pytest test/property_based/ --hypothesis-seed=SPECIFIC_SEED
```

## 🎯 **Avantages des Tests Property-Based**

### **Détection Automatique**
- **Edge cases** : Cas limites trouvés automatiquement
- **Invariants** : Propriétés qui doivent toujours être vraies
- **Robustesse** : Test avec données inattendues
- **Réduction** : Simplification automatique des cas d'échec

### **Couverture Étendue**
- **Espace d'entrée large** : Plus de cas testés
- **Cas non prévus** : Découverte de bugs cachés
- **Validation continue** : Propriétés vérifiées en permanence
- **Documentation vivante** : Les propriétés documentent le comportement

## 🔄 **Maintenance**

### **Ajout de Nouveaux Tests Property-Based**
```python
from hypothesis import given, strategies as st, assume

class TestNewProperties:
    @given(st.floats(min_value=0.0, max_value=1000000.0))
    def test_price_calculation_property(self, price):
        """Les calculs de prix respectent les propriétés mathématiques"""
        assume(price >= 0)  # Précondition
        
        # Test de la propriété
        result = calculate_total_with_tax(price, 21.0)
        
        # Assertions sur les propriétés
        assert result >= price  # Le total est toujours >= au prix de base
        assert result <= price * 1.25  # Borne supérieure raisonnable
    
    @given(st.text(min_size=1, max_size=100))
    def test_validation_property(self, text_input):
        """La validation est cohérente"""
        result = validate_input(text_input)
        
        # Propriété : la validation est déterministe
        assert validate_input(text_input) == result
```

### **Optimisation des Stratégies**
```python
# Stratégies personnalisées pour le domaine métier
@st.composite
def valid_product_data(draw):
    """Génère des données de produit valides"""
    return {
        'name': draw(st.text(min_size=1, max_size=50)),
        'price': draw(st.floats(min_value=0.01, max_value=10000.0)),
        'tax_rate': draw(st.floats(min_value=0.0, max_value=50.0))
    }
```

### **Configuration Avancée**
```python
# Configuration dans conftest.py ou settings
from hypothesis import settings, Verbosity

# Profil personnalisé
settings.register_profile("custom", 
    max_examples=500,
    verbosity=Verbosity.verbose,
    deadline=1000
)
```

---

**🎲 Note** : Les tests property-based peuvent révéler des bugs subtils. Analysez attentivement les échecs.

**Pour plus d'informations, consultez le guide principal : `../README.md`**
