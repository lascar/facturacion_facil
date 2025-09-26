# 🔄 Tests de Régression

## 📋 **Description**
Tests pour éviter la réapparition de bugs - validation que les corrections restent effectives.

## 📁 **Contenu du Répertoire**
```
regression/
├── README.md                           # Ce guide
├── test_dialog_scroll_fix.py           # Tests correction scroll
├── test_image_selection.py             # Tests sélection images
├── test_ui_improvements.py             # Tests améliorations UI
├── test_stock_window_focus.py          # Tests focus fenêtre stock
├── test_filedialog_parent_fix.py       # Tests correction parent dialog
├── test_dialogo_logo_fix.py            # Tests correction dialog logo
├── test_image_fix.py                   # Tests correction images
├── test_filedialog_fix.py              # Tests correction filedialog
├── test_messageboxes_fix.py            # Tests correction messageboxes
├── test_image_display_selection.py     # Tests affichage sélection image
├── test_image_selection_fix.py         # Tests correction sélection image
├── test_logo_image_fix.py              # Tests correction logo image
├── test_producto_selection_fix.py      # Tests correction sélection produit
├── test_logo_persistence_fix.py        # Tests persistance logo (base)
├── test_logo_ui_persistence.py         # Tests persistance logo (UI)
└── test_logo_persistence_solution.py   # Tests solution LogoManager
```

## 🚀 **Exécution des Tests**

### **Tous les Tests de Régression**
```bash
# Depuis la racine du projet
./run_organized_tests.sh regression

# Avec pytest directement
pytest test/regression/

# Mode verbose
./run_organized_tests.sh regression -v

# Mode silencieux
./run_organized_tests.sh regression -q
```

### **Tests par Type de Correction**
```bash
# Tests corrections d'images
./run_organized_tests.sh regression -k image
pytest test/regression/test_image_fix.py
pytest test/regression/test_image_selection.py
pytest test/regression/test_logo_image_fix.py

# Tests corrections de dialogs
./run_organized_tests.sh regression -k dialog
pytest test/regression/test_filedialog_fix.py
pytest test/regression/test_dialogo_logo_fix.py
pytest test/regression/test_messageboxes_fix.py

# Tests corrections UI
./run_organized_tests.sh regression -k ui
pytest test/regression/test_ui_improvements.py
pytest test/regression/test_dialog_scroll_fix.py

# Tests corrections de focus
pytest test/regression/test_stock_window_focus.py
pytest test/regression/test_filedialog_parent_fix.py

# Tests corrections de sélection
./run_organized_tests.sh regression -k selection
pytest test/regression/test_image_selection_fix.py
pytest test/regression/test_producto_selection_fix.py
```

### **Tests avec Validation Stricte**
```bash
# Tests avec arrêt au premier échec
./run_organized_tests.sh regression -x

# Tests avec traceback détaillé
./run_organized_tests.sh regression --tb=long

# Tests avec couverture des corrections
pytest test/regression/ --cov=ui --cov-report=term-missing
```

## 📊 **Statistiques**
- **Nombre de fichiers** : 13 fichiers de test
- **Tests estimés** : ~60 tests
- **Couverture** : Corrections de bugs, améliorations UI
- **Temps d'exécution** : ~45-60 secondes

## 🎯 **Objectifs des Tests**

### **Prévention de Régression**
- Vérifier que les bugs corrigés ne reviennent pas
- Valider la stabilité des corrections
- Tester les cas limites qui causaient les bugs
- Maintenir la qualité du code

### **Types de Corrections Testées**
- **Images** : Sélection, affichage, chargement
- **Dialogs** : Parent, focus, comportement
- **UI** : Scroll, visibilité, interactions
- **Focus** : Gestion des fenêtres, navigation
- **Sélection** : Produits, images, éléments

## 🔧 **Configuration**

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Interface graphique pour tests UI
export DISPLAY=:0

# Mode test de régression
export REGRESSION_TEST=1
```

### **Variables d'Environnement**
```bash
# Mode strict pour régression
export STRICT_REGRESSION=1

# Timeout pour tests de régression
export REGRESSION_TIMEOUT=30

# Répertoires de test
export TEST_REGRESSION_DIR="/tmp/regression_test"
```

## 📋 **Catégories de Tests de Régression**

### **Corrections d'Images**
```bash
# Bug : Images ne se chargeaient pas
pytest test/regression/test_image_fix.py

# Bug : Sélection d'images défaillante
pytest test/regression/test_image_selection.py
pytest test/regression/test_image_selection_fix.py

# Bug : Logo ne s'affichait pas
pytest test/regression/test_logo_image_fix.py

# Bug : Affichage sélection image
pytest test/regression/test_image_display_selection.py
```

### **Corrections de Dialogs**
```bash
# Bug : Parent des dialogs incorrect
pytest test/regression/test_filedialog_parent_fix.py

# Bug : Dialog logo problématique
pytest test/regression/test_dialogo_logo_fix.py

# Bug : FileDialog ne fonctionnait pas
pytest test/regression/test_filedialog_fix.py

# Bug : MessageBoxes mal configurées
pytest test/regression/test_messageboxes_fix.py
```

### **Corrections UI et Focus**
```bash
# Bug : Scroll ne fonctionnait pas
pytest test/regression/test_dialog_scroll_fix.py

# Bug : Focus fenêtre stock
pytest test/regression/test_stock_window_focus.py

# Bug : Améliorations UI générales
pytest test/regression/test_ui_improvements.py

# Bug : Sélection produits
pytest test/regression/test_producto_selection_fix.py
```

## 🚀 **Exécution Spécialisée**

### **Tests de Régression Critique**
```bash
# Tests des bugs les plus critiques
./run_organized_tests.sh regression -m critical

# Tests avec validation stricte
pytest test/regression/ --strict-markers --strict-config

# Tests avec retry (pour bugs intermittents)
pytest test/regression/ --reruns=3
```

### **Tests de Régression par Priorité**
```bash
# Haute priorité (bugs critiques)
./run_organized_tests.sh regression -m "high_priority"

# Moyenne priorité
./run_organized_tests.sh regression -m "medium_priority"

# Tests de tous les niveaux
./run_organized_tests.sh regression -m "priority"
```

### **Validation de Corrections Spécifiques**
```bash
# Validation correction images
pytest test/regression/ -k "image" --tb=short

# Validation correction dialogs
pytest test/regression/ -k "dialog" --tb=short

# Validation correction UI
pytest test/regression/ -k "ui" --tb=short
```

## 🐛 **Dépannage**

### **Tests de Régression qui Échouent**
```bash
# Analyse détaillée des échecs
./run_organized_tests.sh regression --tb=long -v

# Tests avec debug
pytest test/regression/test_specific.py --pdb

# Comparaison avant/après
pytest test/regression/ --lf --tb=line
```

### **Bugs qui Reviennent**
```bash
# Identification des régressions
pytest test/regression/ --tb=short | grep FAILED

# Tests avec logs détaillés
pytest test/regression/ --log-cli-level=DEBUG

# Analyse des patterns d'échec
pytest test/regression/ --durations=0
```

## 📈 **Métriques de Qualité**

### **Indicateurs de Régression**
- **Taux de succès** : >95%
- **Stabilité** : Pas de fluctuation
- **Couverture corrections** : >90%
- **Temps d'exécution** : Stable

### **Suivi des Corrections**
- **Bugs corrigés** : Documentés et testés
- **Nouvelles régressions** : Détectées rapidement
- **Stabilité globale** : Maintenue

## 🎯 **Scénarios de Régression**

### **Workflow Images**
1. Sélection d'image (bug corrigé)
2. Affichage correct
3. Sauvegarde persistante
4. Rechargement sans erreur

### **Workflow Dialogs**
1. Ouverture dialog avec bon parent
2. Focus correct
3. Interaction normale
4. Fermeture propre

### **Workflow UI**
1. Navigation sans bugs
2. Scroll fonctionnel
3. Sélections correctes
4. Affichage stable

## 🔄 **Maintenance**

### **Ajout de Nouveaux Tests de Régression**
```python
import pytest
from regression_helpers import validate_fix

class TestNewRegression:
    def test_bug_fix_XXXX(self):
        """Test pour bug #XXXX - Description du bug"""
        # Reproduire les conditions du bug
        # Vérifier que la correction fonctionne
        # Valider que le bug ne revient pas
        assert validate_fix("bug_XXXX")
```

### **Documentation des Bugs**
- **ID du bug** : Référence unique
- **Description** : Symptômes et cause
- **Correction** : Solution implémentée
- **Test** : Validation de la correction

### **Suivi des Régressions**
```bash
# Historique des tests
pytest test/regression/ --tb=no -q

# Tendances de stabilité
pytest test/regression/ --durations=10

# Rapport de régression
pytest test/regression/ --html=regression_report.html
```

## 📋 **Checklist de Régression**

### **Avant Release**
- [ ] Tous les tests de régression passent
- [ ] Aucune nouvelle régression détectée
- [ ] Performance stable
- [ ] Couverture maintenue

### **Après Correction de Bug**
- [ ] Test de régression créé
- [ ] Bug documenté
- [ ] Correction validée
- [ ] Test ajouté à la suite

### **Maintenance Régulière**
- [ ] Tests de régression exécutés quotidiennement
- [ ] Nouveaux bugs ajoutés aux tests
- [ ] Documentation mise à jour
- [ ] Métriques surveillées

---

**⚠️ Important** : Les tests de régression sont critiques pour la stabilité. Ils doivent toujours passer.

**Pour plus d'informations, consultez le guide principal : `../README.md`**
