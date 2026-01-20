> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**

---

# 🐍 Configuration de l'Environnement Python

## 🎯 **Problème Identifié**

L'environnement virtuel ne s'active pas correctement avec le script `activate_env.sh`. Voici les solutions :

## ✅ **Solutions Disponibles**

### **Solution 1 : Activation Manuelle (Recommandée)**

```bash
# Activer l'environnement virtuel
source ../bin/activate

# Vérifier l'activation
which python
# Devrait afficher: /home/pascal/for_django/bin/python

# Vérifier la version
python --version
# Devrait afficher: Python 3.13.7
```

### **Solution 2 : Script d'Activation Amélioré**

```bash
# Utiliser le nouveau script (doit être sourcé)
source ./activate.sh

# Ou la version courte
. ./activate.sh
```

### **Solution 3 : Activation Directe avec Tests**

```bash
# Activer et lancer les tests en une commande
source ../bin/activate && ./run_organized_tests.sh all
```

## 🔧 **Vérification de l'Environnement**

### **Avant Activation**
```bash
which python
# Affiche: /home/pascal/anaconda3/bin/python (❌ Anaconda)
```

### **Après Activation Correcte**
```bash
which python
# Affiche: /home/pascal/for_django/bin/python (✅ Environnement virtuel)

echo $VIRTUAL_ENV
# Affiche: /home/pascal/for_django (✅ Variable définie)
```

## 🧪 **Exécuter Tous les Tests**

### **Méthode 1 : Avec Environnement Activé**
```bash
# 1. Activer l'environnement
source ../bin/activate

# 2. Exécuter tous les tests
./run_organized_tests.sh all

# Ou avec plus de détails
./run_organized_tests.sh all -v
```

### **Méthode 2 : En Une Commande**
```bash
# Activer et tester en une fois
source ../bin/activate && ./run_organized_tests.sh all
```

### **Méthode 3 : Tests Parallèles (Plus Rapide)**
```bash
source ../bin/activate && ./run_organized_tests.sh all -n auto
```

## 📊 **Types de Tests Disponibles**

```bash
# Tous les tests
./run_organized_tests.sh all

# Tests unitaires seulement
./run_organized_tests.sh unit

# Tests de régression
./run_organized_tests.sh regression

# Tests d'intégration
./run_organized_tests.sh integration

# Tests avec couverture de code
./run_organized_tests.sh all --cov
```

## 🔍 **Diagnostic des Problèmes**

### **Vérifier l'Environnement Virtuel**
```bash
# Vérifier que l'environnement existe
ls -la ../bin/activate
# Devrait afficher le fichier d'activation

# Vérifier la configuration
cat ../pyvenv.cfg
# Devrait montrer Python 3.13.7
```

### **Vérifier les Dépendances**
```bash
# Après activation de l'environnement
pip list
# Devrait afficher pytest, faker, etc.

# Vérifier une dépendance spécifique
pip show pytest
```

## 🛠️ **Résolution de Problèmes**

### **Si l'Environnement ne s'Active Pas**
```bash
# Recréer l'environnement virtuel
cd /home/pascal/for_django
rm -rf bin lib lib64 pyvenv.cfg
python3.13 -m venv .

# Réinstaller les dépendances
source bin/activate
pip install -r facturacion_facil/requirements.txt
```

### **Si Python Pointe Toujours vers Anaconda**
```bash
# Forcer l'utilisation du bon Python
/home/pascal/for_django/bin/python -m pytest test/

# Ou modifier temporairement le PATH
export PATH="/home/pascal/for_django/bin:$PATH"
python --version
```

### **Si les Tests ne Trouvent pas les Modules**
```bash
# Vérifier le PYTHONPATH
echo $PYTHONPATH

# Ajouter le répertoire du projet si nécessaire
export PYTHONPATH="/home/pascal/for_django/facturacion_facil:$PYTHONPATH"
```

## 🚀 **Workflow Recommandé**

### **Pour Développement Quotidien**
```bash
# 1. Aller dans le répertoire du projet
cd /home/pascal/for_django/facturacion_facil

# 2. Activer l'environnement
source ../bin/activate

# 3. Vérifier l'activation
which python  # Doit pointer vers l'environnement virtuel

# 4. Lancer les tests
./run_organized_tests.sh unit  # Tests rapides
# ou
./run_organized_tests.sh all   # Tous les tests
```

### **Pour Validation Complète**
```bash
# Tests complets avec couverture
source ../bin/activate && ./run_organized_tests.sh all --cov -v
```

### **Pour Debug**
```bash
# Tests avec debug détaillé
source ../bin/activate && ./run_organized_tests.sh all -vv -s --tb=long
```

## 📝 **Scripts Disponibles**

- **`activate.sh`** : Script d'activation amélioré (à sourcer)
- **`activate_env.sh`** : Script original (corrigé, à sourcer)
- **`run_organized_tests.sh`** : Script principal pour les tests

## 💡 **Conseils**

1. **Toujours sourcer** les scripts d'activation avec `source` ou `.`
2. **Vérifier l'activation** avec `which python` avant de lancer les tests
3. **Utiliser les tests organisés** avec `./run_organized_tests.sh` pour une meilleure expérience
4. **Activer l'environnement** à chaque nouvelle session de terminal

---

## 🎯 **Commande Rapide pour Exécuter Tous les Tests**

```bash
cd /home/pascal/for_django/facturacion_facil
source ../bin/activate && ./run_organized_tests.sh all
```

Cette commande active l'environnement et lance tous les tests avec le système de base de données isolée !

---

> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**
