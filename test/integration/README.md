# 🔗 Tests d'Intégration

## 📋 **Description**
Tests d'interaction entre composants - validation du fonctionnement des modules ensemble.

## 📁 **Contenu du Répertoire**
```
integration/
├── README.md                               # Ce guide
├── test_integration.py                     # Tests intégration générale
├── test_facturas_integration.py            # Tests intégration facturas
├── test_pdf_download_feature.py            # Tests fonctionnalité PDF
├── test_visor_pdf_personalizado.py         # Tests visor PDF
├── test_facturas_validacion_integracion.py # Tests validation intégration
├── test_stock_facturacion_integration.py   # Tests stock-factura
├── test_facturas_implementation.py         # Tests implémentation facturas
├── test_complete_functionality.py          # Tests fonctionnalité complète
├── test_organizacion_completo.py           # Tests organisation complète
└── test_global_todas_correcciones.py       # Tests corrections globales
```

## 🚀 **Exécution des Tests**

### **Tous les Tests d'Intégration**
```bash
# Depuis la racine du projet
./run_organized_tests.sh integration

# Avec pytest directement
pytest test/integration/

# Mode verbose
./run_organized_tests.sh integration -v

# Mode silencieux
./run_organized_tests.sh integration -q
```

### **Tests par Fonctionnalité**
```bash
# Tests PDF
./run_organized_tests.sh integration -k pdf
pytest test/integration/test_pdf_download_feature.py
pytest test/integration/test_visor_pdf_personalizado.py

# Tests Facturas
./run_organized_tests.sh integration -k factura
pytest test/integration/test_facturas_integration.py
pytest test/integration/test_facturas_implementation.py

# Tests Stock
./run_organized_tests.sh integration -k stock
pytest test/integration/test_stock_facturacion_integration.py

# Tests Organisation
pytest test/integration/test_organizacion_completo.py

# Tests complets
pytest test/integration/test_complete_functionality.py
```

### **Tests avec Couverture**
```bash
# Couverture des modules d'intégration
./run_organized_tests.sh integration --cov=ui --cov=database --cov=utils

# Rapport HTML
./run_organized_tests.sh integration --cov=ui --cov-report=html

# Couverture détaillée
pytest test/integration/ --cov=ui --cov=database --cov-report=term-missing
```

## 📊 **Statistiques**
- **Nombre de fichiers** : 10 fichiers de test
- **Tests estimés** : ~35 tests
- **Couverture** : UI, base de données, intégrations
- **Temps d'exécution** : ~60-90 secondes

## 🎯 **Objectifs des Tests**

### **Intégration Base de Données ↔ UI**
- Sauvegarde et récupération de données
- Synchronisation des interfaces
- Gestion des transactions
- Cohérence des données

### **Intégration Modules Métier**
- Facturas ↔ Produits ↔ Stock
- Calculs et totaux
- Workflow complet
- Règles métier

### **Fonctionnalités Complètes**
- PDF : Génération, visor, téléchargement
- Organisation : Configuration, persistance
- Stock : Gestion, intégration facturas
- Validation : Formulaires, données

## 🔧 **Configuration**

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Base de données de test
export TEST_DATABASE="test_integration.db"

# Répertoires temporaires
mkdir -p /tmp/test_images /tmp/test_pdfs
```

### **Variables d'Environnement**
```bash
# Mode test d'intégration
export INTEGRATION_TEST=1

# Timeout pour tests longs
export PYTEST_TIMEOUT=300

# Répertoires de test
export TEST_IMAGE_DIR="/tmp/test_images"
export TEST_PDF_DIR="/tmp/test_pdfs"
```

## 📋 **Types de Tests d'Intégration**

### **Tests de Workflow Complet**
```bash
# Test complet facturation
pytest test/integration/test_complete_functionality.py

# Test organisation complète
pytest test/integration/test_organizacion_completo.py

# Test toutes corrections
pytest test/integration/test_global_todas_correcciones.py
```

### **Tests de Fonctionnalités Spécifiques**
```bash
# Fonctionnalité PDF complète
pytest test/integration/test_pdf_download_feature.py -v

# Visor PDF personnalisé
pytest test/integration/test_visor_pdf_personalizado.py -v

# Intégration stock-facturas
pytest test/integration/test_stock_facturacion_integration.py -v
```

### **Tests de Validation d'Intégration**
```bash
# Validation intégrée
pytest test/integration/test_facturas_validacion_integracion.py

# Implémentation facturas
pytest test/integration/test_facturas_implementation.py
```

## 🚀 **Exécution Avancée**

### **Tests Parallèles**
```bash
# Exécution en parallèle (si supporté)
./run_organized_tests.sh integration -n auto

# Avec nombre de workers spécifique
pytest test/integration/ -n 2
```

### **Tests avec Timeout**
```bash
# Timeout global
pytest test/integration/ --timeout=300

# Tests longs uniquement
./run_organized_tests.sh integration -m slow
```

### **Tests de Performance d'Intégration**
```bash
# Avec mesure de temps
pytest test/integration/ --durations=10

# Benchmark si disponible
pytest test/integration/ --benchmark-only
```

## 🐛 **Dépannage**

### **Erreurs Communes**
```bash
# Base de données en conflit
rm -f test_integration.db

# Fichiers temporaires
rm -rf /tmp/test_*

# Permissions de fichiers
chmod -R 755 /tmp/test_images /tmp/test_pdfs

# Interface graphique non disponible
export DISPLAY=:0
# ou
xvfb-run pytest test/integration/
```

### **Tests Qui Échouent**
```bash
# Debug détaillé
./run_organized_tests.sh integration --tb=long -v

# Tests spécifiques en échec
pytest test/integration/test_specific.py --pdb

# Logs détaillés
pytest test/integration/ -s --log-cli-level=DEBUG
```

## 📈 **Métriques de Qualité**

### **Couverture Attendue**
- **Intégration UI-DB** : >70%
- **Workflows complets** : >80%
- **Fonctionnalités PDF** : >85%
- **Gestion stock** : >75%

### **Performance**
- **Temps total** : <120 secondes
- **Tests individuels** : <10 secondes
- **Setup complexe** : <30 secondes

## 🎯 **Scénarios de Test**

### **Workflow Factura Complet**
1. Création organisation
2. Ajout produits avec images
3. Création factura
4. Ajout items à la factura
5. Calculs automatiques
6. Génération PDF
7. Ouverture avec visor

### **Intégration Stock-Facturas**
1. Configuration stock initial
2. Création factura avec produits
3. Vérification déduction stock
4. Gestion stock insuffisant
5. Mise à jour automatique

### **Fonctionnalité PDF Complète**
1. Configuration répertoire PDF
2. Configuration visor personnalisé
3. Génération PDF avec images
4. Ouverture automatique
5. Fallback en cas d'erreur

## 🔄 **Maintenance**

### **Ajout de Nouveaux Tests**
```python
import pytest
from integration_helpers import setup_test_environment

class TestNewIntegration:
    def setup_method(self):
        """Setup environnement d'intégration"""
        self.test_env = setup_test_environment()
    
    def test_complete_workflow(self):
        """Test d'un workflow complet"""
        # Test d'intégration bout en bout
        pass
    
    def teardown_method(self):
        """Nettoyage environnement"""
        self.test_env.cleanup()
```

### **Mise à Jour des Tests**
- Adapter aux nouvelles fonctionnalités
- Maintenir la cohérence des données de test
- Optimiser les temps d'exécution
- Documenter les nouveaux scénarios

---

**Pour plus d'informations, consultez le guide principal : `../README.md`**
