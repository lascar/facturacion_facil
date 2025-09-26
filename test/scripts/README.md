# 📜 Scripts de Test

## 📋 **Description**
Scripts d'exécution et utilitaires de test - outils pour automatiser et faciliter les tests.

## 📁 **Contenu du Répertoire**
```
scripts/
├── README.md                    # Ce guide
├── run_tests_fixed.py           # Script tests corrigé
├── run_working_tests.py         # Script tests fonctionnels
├── run_tests.py                 # Script tests principal
├── run_productos_tests.py       # Script tests produits
├── run_facturas_tests.py        # Script tests facturas
└── run_with_correct_python.sh   # Script avec bon Python
```

## 🚀 **Utilisation des Scripts**

### **Lister les Scripts Disponibles**
```bash
# Depuis la racine du projet
./run_organized_tests.sh scripts

# Voir le contenu du répertoire
ls -la test/scripts/

# Permissions d'exécution
ls -la test/scripts/ | grep rwx
```

### **Exécution des Scripts**
```bash
# Script principal de tests
python3 test/scripts/run_tests.py

# Script tests corrigé
python3 test/scripts/run_tests_fixed.py

# Script tests fonctionnels
python3 test/scripts/run_working_tests.py

# Script tests produits
python3 test/scripts/run_productos_tests.py

# Script tests facturas
python3 test/scripts/run_facturas_tests.py

# Script avec Python correct
bash test/scripts/run_with_correct_python.sh
```

## 📊 **Statistiques**
- **Nombre de scripts** : 6 scripts
- **Types** : Python et Bash
- **Fonctions** : Tests spécialisés, corrections, utilitaires
- **Maintenance** : Scripts legacy organisés

## 🎯 **Objectifs des Scripts**

### **Automatisation**
- Exécution de tests spécialisés
- Configuration d'environnement
- Gestion des dépendances
- Rapports automatisés

### **Utilitaires**
- Scripts de correction de bugs
- Tests de modules spécifiques
- Validation d'environnement
- Outils de développement

## 🔧 **Description des Scripts**

### **run_tests.py**
```bash
# Script principal de tests
python3 test/scripts/run_tests.py

# Options disponibles
python3 test/scripts/run_tests.py --help
```

**Fonctionnalités :**
- Exécution de tests généraux
- Configuration automatique
- Rapports de résultats
- Gestion d'erreurs

### **run_tests_fixed.py**
```bash
# Script avec corrections appliquées
python3 test/scripts/run_tests_fixed.py
```

**Fonctionnalités :**
- Tests avec corrections de bugs
- Validation des fixes
- Environnement stabilisé
- Rapports de régression

### **run_working_tests.py**
```bash
# Script tests fonctionnels uniquement
python3 test/scripts/run_working_tests.py
```

**Fonctionnalités :**
- Tests qui passent garantis
- Validation de stabilité
- CI/CD friendly
- Rapports de succès

### **run_productos_tests.py**
```bash
# Tests spécifiques aux produits
python3 test/scripts/run_productos_tests.py
```

**Fonctionnalités :**
- Tests module produits
- Interface produits
- Validation métier produits
- Rapports spécialisés

### **run_facturas_tests.py**
```bash
# Tests spécifiques aux facturas
python3 test/scripts/run_facturas_tests.py
```

**Fonctionnalités :**
- Tests module facturas
- Interface facturas
- Calculs et validation
- Workflow complet

### **run_with_correct_python.sh**
```bash
# Script avec environnement Python correct
bash test/scripts/run_with_correct_python.sh
```

**Fonctionnalités :**
- Détection version Python
- Activation environnement virtuel
- Configuration PATH
- Exécution sécurisée

## 🚀 **Exécution Avancée**

### **Scripts avec Options**
```bash
# Mode verbose
python3 test/scripts/run_tests.py --verbose

# Mode debug
python3 test/scripts/run_tests.py --debug

# Tests spécifiques
python3 test/scripts/run_productos_tests.py --module=ui

# Avec couverture
python3 test/scripts/run_tests.py --coverage
```

### **Scripts en Parallèle**
```bash
# Exécution simultanée (attention aux conflits)
python3 test/scripts/run_productos_tests.py &
python3 test/scripts/run_facturas_tests.py &
wait

# Séquentiel recommandé
python3 test/scripts/run_productos_tests.py
python3 test/scripts/run_facturas_tests.py
```

### **Scripts avec Redirection**
```bash
# Logs dans fichier
python3 test/scripts/run_tests.py > test_results.log 2>&1

# Logs séparés
python3 test/scripts/run_tests.py 1>success.log 2>errors.log

# Avec timestamp
python3 test/scripts/run_tests.py | ts '[%Y-%m-%d %H:%M:%S]'
```

## 🔧 **Configuration des Scripts**

### **Variables d'Environnement**
```bash
# Configuration pour scripts
export SCRIPT_MODE=1
export TEST_SCRIPT_DIR="test/scripts"
export SCRIPT_TIMEOUT=300

# Environnement Python
export PYTHON_VERSION=3.13
export VIRTUAL_ENV_PATH="../bin/activate"

# Rapports
export SCRIPT_REPORT_DIR="./script_reports"
```

### **Prérequis**
```bash
# Permissions d'exécution
chmod +x test/scripts/*.py
chmod +x test/scripts/*.sh

# Environnement virtuel
source ../bin/activate

# Dépendances
pip install -r requirements.txt
```

## 🐛 **Dépannage**

### **Scripts qui ne s'exécutent pas**
```bash
# Vérifier permissions
ls -la test/scripts/

# Donner permissions
chmod +x test/scripts/run_with_correct_python.sh

# Vérifier shebang
head -1 test/scripts/run_tests.py

# Vérifier Python
which python3
python3 --version
```

### **Erreurs d'Environnement**
```bash
# Activer environnement virtuel
source ../bin/activate

# Vérifier PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Vérifier dépendances
pip list | grep pytest
```

### **Scripts qui Échouent**
```bash
# Mode debug
python3 -u test/scripts/run_tests.py --debug

# Avec traceback complet
python3 test/scripts/run_tests.py --tb=long

# Logs détaillés
python3 test/scripts/run_tests.py --log-level=DEBUG
```

## 📈 **Utilisation Recommandée**

### **Développement**
```bash
# Tests rapides pendant développement
python3 test/scripts/run_working_tests.py

# Tests module spécifique
python3 test/scripts/run_productos_tests.py

# Validation après correction
python3 test/scripts/run_tests_fixed.py
```

### **Intégration Continue**
```bash
# Tests stables pour CI
python3 test/scripts/run_working_tests.py

# Avec environnement correct
bash test/scripts/run_with_correct_python.sh

# Tests complets
python3 test/scripts/run_tests.py --ci-mode
```

### **Debug et Maintenance**
```bash
# Tests avec debug
python3 test/scripts/run_tests.py --debug --verbose

# Tests spécifiques
python3 test/scripts/run_facturas_tests.py --module=specific

# Validation environnement
bash test/scripts/run_with_correct_python.sh --check-only
```

## 🔄 **Maintenance des Scripts**

### **Mise à Jour des Scripts**
```bash
# Vérifier compatibilité
python3 test/scripts/run_tests.py --check

# Mettre à jour dépendances
pip install --upgrade -r requirements.txt

# Tester après mise à jour
python3 test/scripts/run_tests_fixed.py
```

### **Ajout de Nouveaux Scripts**
```python
#!/usr/bin/env python3
"""
Script de test personnalisé
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def main():
    """Fonction principale du script"""
    # Logique du script
    pass

if __name__ == "__main__":
    main()
```

### **Bonnes Pratiques**
- **Shebang** : Toujours inclure `#!/usr/bin/env python3`
- **Path** : Ajouter le répertoire racine au PYTHONPATH
- **Erreurs** : Gestion appropriée des exceptions
- **Logs** : Messages informatifs et debug
- **Exit codes** : Codes de retour appropriés

## 📋 **Checklist Scripts**

### **Avant Exécution**
- [ ] Permissions d'exécution
- [ ] Environnement virtuel activé
- [ ] Dépendances installées
- [ ] Variables d'environnement configurées

### **Pendant Exécution**
- [ ] Surveiller les logs
- [ ] Vérifier les performances
- [ ] Gérer les interruptions
- [ ] Sauvegarder les rapports

### **Après Exécution**
- [ ] Analyser les résultats
- [ ] Archiver les logs
- [ ] Nettoyer les fichiers temporaires
- [ ] Documenter les problèmes

## 🎯 **Migration vers Scripts Organisés**

### **Ancien Workflow**
```bash
# Avant : Scripts dans la racine
python3 run_tests.py
python3 run_productos_tests.py
```

### **Nouveau Workflow**
```bash
# Après : Scripts organisés
./run_organized_tests.sh scripts  # Lister
python3 test/scripts/run_tests.py  # Exécuter

# Ou utiliser le script principal
./run_organized_tests.sh unit      # Plus moderne
./run_organized_tests.sh integration
```

---

**📜 Note** : Ces scripts sont des outils legacy organisés. Préférez `./run_organized_tests.sh` pour les nouveaux workflows.

**Pour plus d'informations, consultez le guide principal : `../README.md`**
