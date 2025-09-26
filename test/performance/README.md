# ⚡ Tests de Performance

## 📋 **Description**
Benchmarks et tests de performance - validation des temps de réponse et optimisations.

## 📁 **Contenu du Répertoire**
```
performance/
├── README.md                    # Ce guide
└── test_performance.py          # Benchmarks et tests de performance
```

## 🚀 **Exécution des Tests**

### **Tous les Tests de Performance**
```bash
# Depuis la racine du projet
./run_organized_tests.sh performance

# Avec pytest directement
pytest test/performance/

# Mode benchmark uniquement
./run_organized_tests.sh performance --benchmark-only

# Mode verbose avec métriques
./run_organized_tests.sh performance -v
```

### **Tests avec Benchmarks**
```bash
# Benchmarks complets
pytest test/performance/ --benchmark-only

# Benchmarks avec comparaison
pytest test/performance/ --benchmark-compare

# Benchmarks avec sauvegarde
pytest test/performance/ --benchmark-save=baseline

# Benchmarks avec graphiques
pytest test/performance/ --benchmark-histogram
```

### **Tests de Performance Spécifiques**
```bash
# Performance base de données
pytest test/performance/test_performance.py -k database

# Performance UI
pytest test/performance/test_performance.py -k ui

# Performance calculs
pytest test/performance/test_performance.py -k calculation

# Performance I/O
pytest test/performance/test_performance.py -k io
```

## 📊 **Statistiques**
- **Nombre de fichiers** : 1 fichier principal
- **Tests estimés** : ~13 tests
- **Couverture** : Base de données, UI, calculs, I/O
- **Temps d'exécution** : ~60-90 secondes

## 🎯 **Objectifs des Tests**

### **Benchmarks de Performance**
- Temps de réponse des opérations critiques
- Utilisation mémoire
- Débit des opérations
- Scalabilité

### **Métriques Surveillées**
- **Base de données** : Temps de requête, connexions
- **Interface** : Temps de chargement, réactivité
- **Calculs** : Temps de traitement, précision
- **I/O** : Lecture/écriture fichiers, images

## 🔧 **Configuration**

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Plugin benchmark installé
pip install pytest-benchmark

# Ressources système disponibles
free -h
df -h
```

### **Variables d'Environnement**
```bash
# Mode performance
export PERFORMANCE_TEST=1

# Nombre d'itérations
export BENCHMARK_ITERATIONS=100

# Timeout pour tests longs
export PERFORMANCE_TIMEOUT=300

# Répertoire de résultats
export BENCHMARK_DIR="./benchmarks"
```

## 📋 **Types de Tests de Performance**

### **Performance Base de Données**
```bash
# Tests CRUD
pytest test/performance/ -k "database" --benchmark-only

# Tests requêtes complexes
pytest test/performance/ -k "query" --benchmark-only

# Tests transactions
pytest test/performance/ -k "transaction" --benchmark-only
```

### **Performance Interface Utilisateur**
```bash
# Temps de chargement fenêtres
pytest test/performance/ -k "ui_load" --benchmark-only

# Réactivité interactions
pytest test/performance/ -k "ui_response" --benchmark-only

# Performance scroll et navigation
pytest test/performance/ -k "ui_navigation" --benchmark-only
```

### **Performance Calculs**
```bash
# Calculs facturas
pytest test/performance/ -k "calculation" --benchmark-only

# Calculs stock
pytest test/performance/ -k "stock_calc" --benchmark-only

# Calculs IVA et totaux
pytest test/performance/ -k "tax_calc" --benchmark-only
```

### **Performance I/O**
```bash
# Lecture/écriture fichiers
pytest test/performance/ -k "file_io" --benchmark-only

# Traitement images
pytest test/performance/ -k "image_io" --benchmark-only

# Génération PDF
pytest test/performance/ -k "pdf_gen" --benchmark-only
```

## 🚀 **Exécution Avancée**

### **Benchmarks avec Comparaison**
```bash
# Créer baseline
pytest test/performance/ --benchmark-save=baseline

# Comparer avec baseline
pytest test/performance/ --benchmark-compare=baseline

# Comparer plusieurs runs
pytest test/performance/ --benchmark-compare-fail=min:5%
```

### **Benchmarks avec Visualisation**
```bash
# Générer histogrammes
pytest test/performance/ --benchmark-histogram

# Graphiques de tendance
pytest test/performance/ --benchmark-sort=mean

# Rapport HTML
pytest test/performance/ --benchmark-json=results.json
```

### **Tests de Charge**
```bash
# Tests avec charge élevée
pytest test/performance/ -k "load" --benchmark-only

# Tests de stress
pytest test/performance/ -k "stress" --benchmark-only

# Tests de scalabilité
pytest test/performance/ -k "scale" --benchmark-only
```

## 📈 **Métriques de Performance**

### **Seuils Acceptables**
```
Base de données:
- Requête simple: <10ms
- Requête complexe: <100ms
- Transaction: <50ms

Interface utilisateur:
- Chargement fenêtre: <500ms
- Réponse clic: <100ms
- Scroll: <16ms (60fps)

Calculs:
- Calcul factura: <50ms
- Calcul stock: <20ms
- Totaux: <10ms

I/O:
- Lecture fichier: <100ms
- Traitement image: <200ms
- Génération PDF: <1000ms
```

### **Métriques Collectées**
- **Temps moyen** : Moyenne des exécutions
- **Médiane** : Valeur médiane
- **Min/Max** : Valeurs extrêmes
- **Écart-type** : Variabilité
- **Ops/sec** : Débit d'opérations

## 🐛 **Dépannage**

### **Tests de Performance Lents**
```bash
# Identifier les goulots d'étranglement
pytest test/performance/ --durations=0

# Profiling détaillé
pytest test/performance/ --profile

# Tests avec timeout étendu
pytest test/performance/ --timeout=600
```

### **Résultats Incohérents**
```bash
# Augmenter le nombre d'itérations
pytest test/performance/ --benchmark-min-rounds=10

# Stabiliser l'environnement
sudo cpufreq-set -g performance

# Tests avec warmup
pytest test/performance/ --benchmark-warmup=on
```

### **Dégradation de Performance**
```bash
# Comparer avec baseline
pytest test/performance/ --benchmark-compare=baseline

# Analyser les régressions
pytest test/performance/ --benchmark-compare-fail=mean:10%

# Identifier les causes
pytest test/performance/ --benchmark-sort=mean -v
```

## 📊 **Analyse des Résultats**

### **Interprétation des Métriques**
```bash
# Résultats détaillés
pytest test/performance/ --benchmark-columns=min,max,mean,stddev

# Tri par performance
pytest test/performance/ --benchmark-sort=mean

# Groupement par catégorie
pytest test/performance/ --benchmark-group-by=group
```

### **Rapports de Performance**
```bash
# Rapport JSON
pytest test/performance/ --benchmark-json=perf_report.json

# Rapport HTML (si plugin disponible)
pytest test/performance/ --benchmark-html=perf_report.html

# Export CSV
pytest test/performance/ --benchmark-csv=perf_data.csv
```

## 🎯 **Optimisation**

### **Identification des Goulots**
1. **Profiling** : Identifier les fonctions lentes
2. **Benchmarking** : Mesurer avant/après optimisation
3. **Monitoring** : Surveiller en continu
4. **Validation** : Vérifier les améliorations

### **Stratégies d'Optimisation**
- **Cache** : Mise en cache des résultats
- **Indexation** : Optimisation base de données
- **Lazy loading** : Chargement à la demande
- **Parallélisation** : Traitement concurrent

## 🔄 **Maintenance**

### **Ajout de Nouveaux Benchmarks**
```python
import pytest
from performance_helpers import benchmark_function

class TestNewPerformance:
    def test_new_operation_performance(self, benchmark):
        """Benchmark d'une nouvelle opération"""
        result = benchmark(operation_to_test, *args)
        assert result is not None
    
    def test_performance_regression(self, benchmark):
        """Test de régression de performance"""
        # Benchmark avec seuil acceptable
        result = benchmark.pedantic(
            operation_to_test,
            iterations=100,
            rounds=10
        )
        assert benchmark.stats.stats.mean < 0.1  # <100ms
```

### **Surveillance Continue**
```bash
# Tests de performance quotidiens
./run_organized_tests.sh performance --benchmark-save=daily_$(date +%Y%m%d)

# Comparaison avec la veille
pytest test/performance/ --benchmark-compare=daily_$(date -d yesterday +%Y%m%d)

# Alertes de régression
pytest test/performance/ --benchmark-compare-fail=mean:20%
```

### **Optimisation Continue**
- Surveiller les tendances de performance
- Identifier les régressions rapidement
- Optimiser les opérations critiques
- Maintenir les seuils de performance

---

**📊 Note** : Les tests de performance peuvent varier selon le matériel. Établissez des baselines sur votre environnement.

**Pour plus d'informations, consultez le guide principal : `../README.md`**
