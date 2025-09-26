# 🎯 Tests de Fonctionnalités Spécifiques

## 📋 **Description**
Tests de fonctionnalités particulières et corrections spécialisées - validation de features spécifiques.

## 📁 **Contenu du Répertoire**
```
specific/
├── README.md                           # Ce guide
├── test_pdf_copyable_messages.py       # Tests messages PDF copiables
├── test_copyable_dialogs.py            # Tests dialogs copiables
├── test_nueva_numeracion.py            # Tests nouvelle numérotation
├── test_pdf_and_search_features.py     # Tests PDF et recherche
├── test_stock_with_copyable_messages.py # Tests stock avec messages
├── test_pdf_message_flow.py            # Tests flux messages PDF
├── test_edicion_automatica_facturas.py # Tests édition auto facturas
└── test_improvements.py                # Tests améliorations générales
```

## 🚀 **Exécution des Tests**

### **Tous les Tests Spécifiques**
```bash
# Depuis la racine du projet
./run_organized_tests.sh specific

# Avec pytest directement
pytest test/specific/

# Mode verbose
./run_organized_tests.sh specific -v

# Mode silencieux
./run_organized_tests.sh specific -q
```

### **Tests par Fonctionnalité**
```bash
# Tests messages copiables
./run_organized_tests.sh specific -k copyable
pytest test/specific/test_pdf_copyable_messages.py
pytest test/specific/test_copyable_dialogs.py
pytest test/specific/test_stock_with_copyable_messages.py

# Tests PDF avancés
./run_organized_tests.sh specific -k pdf
pytest test/specific/test_pdf_and_search_features.py
pytest test/specific/test_pdf_message_flow.py

# Tests numérotation
pytest test/specific/test_nueva_numeracion.py

# Tests édition automatique
pytest test/specific/test_edicion_automatica_facturas.py

# Tests améliorations
pytest test/specific/test_improvements.py
```

### **Tests avec Validation Approfondie**
```bash
# Tests avec couverture spécifique
./run_organized_tests.sh specific --cov=ui --cov=utils

# Tests avec traceback détaillé
./run_organized_tests.sh specific --tb=long

# Tests avec arrêt au premier échec
./run_organized_tests.sh specific -x
```

## 📊 **Statistiques**
- **Nombre de fichiers** : 8 fichiers de test
- **Tests estimés** : ~25 tests
- **Couverture** : Fonctionnalités avancées, améliorations
- **Temps d'exécution** : ~60-75 secondes

## 🎯 **Objectifs des Tests**

### **Fonctionnalités Avancées**
- Messages copiables dans les dialogs
- Système de numérotation avancé
- Édition automatique de facturas
- Intégration PDF et recherche

### **Améliorations Spécialisées**
- Workflow optimisés
- Interface utilisateur améliorée
- Performance et ergonomie
- Fonctionnalités métier spécifiques

## 🔧 **Configuration**

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Fonctionnalités spécifiques activées
export SPECIFIC_FEATURES=1

# Mode test avancé
export ADVANCED_TEST_MODE=1
```

### **Variables d'Environnement**
```bash
# Tests de fonctionnalités spécifiques
export SPECIFIC_TEST=1

# Timeout pour tests complexes
export SPECIFIC_TIMEOUT=120

# Répertoires de test spécialisés
export SPECIFIC_TEST_DIR="/tmp/specific_test"
```

## 📋 **Catégories de Tests Spécifiques**

### **Messages Copiables**
```bash
# Tests dialogs copiables
pytest test/specific/test_copyable_dialogs.py

# Tests messages PDF copiables
pytest test/specific/test_pdf_copyable_messages.py

# Tests stock avec messages copiables
pytest test/specific/test_stock_with_copyable_messages.py
```

**Fonctionnalités testées :**
- Dialogs avec contenu copiable
- Messages d'erreur copiables
- Informations de succès copiables
- Intégration avec le presse-papiers

### **Système de Numérotation Avancé**
```bash
# Tests nouvelle numérotation
pytest test/specific/test_nueva_numeracion.py -v
```

**Fonctionnalités testées :**
- Séries de numérotation personnalisées
- Incrémentation automatique
- Gestion des préfixes/suffixes
- Validation des formats

### **PDF et Recherche**
```bash
# Tests PDF et recherche
pytest test/specific/test_pdf_and_search_features.py

# Tests flux messages PDF
pytest test/specific/test_pdf_message_flow.py
```

**Fonctionnalités testées :**
- Génération PDF avec métadonnées
- Recherche dans les PDFs
- Workflow PDF complet
- Messages et notifications PDF

### **Édition Automatique**
```bash
# Tests édition automatique facturas
pytest test/specific/test_edicion_automatica_facturas.py -v
```

**Fonctionnalités testées :**
- Édition automatique de champs
- Calculs automatiques
- Validation en temps réel
- Sauvegarde automatique

### **Améliorations Générales**
```bash
# Tests améliorations
pytest test/specific/test_improvements.py -v
```

**Fonctionnalités testées :**
- Optimisations d'interface
- Améliorations ergonomiques
- Nouvelles fonctionnalités
- Corrections et ajustements

## 🚀 **Exécution Spécialisée**

### **Tests par Complexité**
```bash
# Tests simples
./run_organized_tests.sh specific -m "not complex"

# Tests complexes
./run_organized_tests.sh specific -m complex

# Tests interactifs
./run_organized_tests.sh specific -m interactive
```

### **Tests par Priorité**
```bash
# Haute priorité
./run_organized_tests.sh specific -m high_priority

# Fonctionnalités critiques
./run_organized_tests.sh specific -m critical

# Nouvelles fonctionnalités
./run_organized_tests.sh specific -m new_feature
```

### **Tests avec Configuration Spéciale**
```bash
# Tests avec interface graphique
DISPLAY=:0 ./run_organized_tests.sh specific -k copyable

# Tests avec timeout étendu
./run_organized_tests.sh specific --timeout=180

# Tests avec retry pour stabilité
pytest test/specific/ --reruns=2
```

## 🐛 **Dépannage**

### **Tests Spécifiques qui Échouent**
```bash
# Debug détaillé
./run_organized_tests.sh specific --tb=long -v

# Tests avec logs
pytest test/specific/ --log-cli-level=DEBUG -s

# Tests individuels
pytest test/specific/test_specific_feature.py --pdb
```

### **Fonctionnalités Non Disponibles**
```bash
# Vérifier les prérequis
pytest test/specific/ --collect-only

# Skip fonctionnalités manquantes
pytest test/specific/ -k "not requires_feature_x"

# Tests avec fallback
pytest test/specific/ --ignore-missing-features
```

## 📈 **Métriques de Qualité**

### **Couverture Fonctionnelle**
- **Messages copiables** : >90%
- **Numérotation** : >85%
- **PDF avancé** : >80%
- **Édition auto** : >75%

### **Stabilité**
- **Taux de succès** : >95%
- **Reproductibilité** : >98%
- **Performance** : Stable

## 🎯 **Scénarios de Test Spécifiques**

### **Workflow Messages Copiables**
1. Génération d'un message d'erreur
2. Affichage dans dialog copiable
3. Copie du contenu
4. Validation du presse-papiers
5. Utilisation dans autre application

### **Workflow Numérotation Avancée**
1. Configuration série personnalisée
2. Génération numéros séquentiels
3. Gestion des préfixes
4. Validation format
5. Persistance configuration

### **Workflow PDF Avancé**
1. Génération PDF avec métadonnées
2. Ajout de fonctionnalités recherche
3. Intégration avec messages
4. Workflow complet
5. Validation résultat

## 🔄 **Maintenance**

### **Ajout de Nouveaux Tests Spécifiques**
```python
import pytest
from specific_helpers import setup_specific_feature

class TestNewSpecificFeature:
    def setup_method(self):
        """Setup pour fonctionnalité spécifique"""
        self.feature = setup_specific_feature()
    
    def test_specific_functionality(self):
        """Test d'une fonctionnalité spécifique"""
        # Test de la fonctionnalité particulière
        result = self.feature.execute_specific_action()
        assert result.is_valid()
    
    def teardown_method(self):
        """Nettoyage spécifique"""
        self.feature.cleanup()
```

### **Documentation des Fonctionnalités**
- **Description** : Objectif de la fonctionnalité
- **Prérequis** : Dépendances et configuration
- **Tests** : Scénarios de validation
- **Limitations** : Contraintes connues

### **Évolution des Tests**
- Adapter aux nouvelles fonctionnalités
- Maintenir la compatibilité
- Optimiser les performances
- Documenter les changements

## 📋 **Checklist Fonctionnalités Spécifiques**

### **Avant Ajout de Fonctionnalité**
- [ ] Tests de la fonctionnalité créés
- [ ] Documentation mise à jour
- [ ] Prérequis identifiés
- [ ] Scénarios de test définis

### **Après Implémentation**
- [ ] Tests passent
- [ ] Couverture suffisante
- [ ] Performance acceptable
- [ ] Documentation complète

### **Maintenance Continue**
- [ ] Tests exécutés régulièrement
- [ ] Fonctionnalités surveillées
- [ ] Améliorations documentées
- [ ] Évolutions planifiées

---

**🎯 Note** : Ces tests valident des fonctionnalités avancées. Ils peuvent nécessiter une configuration spéciale.

**Pour plus d'informations, consultez le guide principal : `../README.md`**
