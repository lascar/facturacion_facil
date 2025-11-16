# Guide d'Installation - Facturación Fácil

## Vue d'ensemble

Facturación Fácil utilise maintenant **PyQt6** comme framework GUI principal pour de meilleures performances et une compatibilité Windows optimale.

## Prérequis

- **Python 3.13+** (recommandé)
- **Système d'exploitation**: Windows 10/11, Linux (Ubuntu 20.04+)
- **Mémoire**: 4GB RAM minimum
- **Espace disque**: 500MB libres

## Installation Rapide

### Option 1: Installation Automatique (Recommandée)

```bash
# 1. Cloner le repository
git clone <url-du-repository>
cd facturacion_facil

# 2. Exécuter le script de déploiement
python deploy/deploy_solution.py
```

### Option 2: Installation Manuelle

```bash
# 1. Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Initialiser la base de données
python -c "from database.database import db; db.init_database()"

# 4. Lancer l'application
python main.py
```

## Installation par Composants

### 1. PyQt6 (Framework GUI Principal)

```bash
# Installation PyQt6
pip install PyQt6==6.6.1

# Vérification
python -c "import PyQt6; print('PyQt6 installé avec succès')"
```

### 2. Dépendances Complémentaires

```bash
# CustomTkinter (compatibilité legacy)
pip install customtkinter==5.2.2

# Traitement d'images
pip install Pillow==10.4.0

# Génération PDF
pip install reportlab==4.2.2
```

### 3. Validation de l'Installation

```bash
# Test complet PyQt6
python validate_pyqt6_migration.py

# Tests de performance
python compare_frameworks.py

# Test de l'application
python main.py
```

## Installation par Plateforme

### Windows 10/11

```powershell
# PowerShell en tant qu'administrateur
# 1. Installer Python 3.13
winget install Python.Python.3.13

# 2. Cloner et installer
git clone <url-du-repository>
cd facturacion_facil
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Lancer
python main.py
```

### Ubuntu/Debian Linux

```bash
# 1. Installer les prérequis système
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip git

# 2. Installer PyQt6 (optionnel, via apt)
sudo apt install python3-pyqt6

# 3. Cloner et installer
git clone <url-du-repository>
cd facturacion_facil
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Lancer
python main.py
```

### macOS

```bash
# 1. Installer Homebrew (si pas déjà fait)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Installer Python
brew install python@3.13

# 3. Cloner et installer
git clone <url-du-repository>
cd facturacion_facil
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Lancer
python main.py
```

## Résolution de Problèmes

### PyQt6 ne s'installe pas

```bash
# Option 1: Mise à jour pip
python -m pip install --upgrade pip setuptools wheel

# Option 2: Installation avec cache clear
pip install --no-cache-dir PyQt6

# Option 3: Installation via conda
conda install pyqt

# Option 4: Installation système (Linux)
sudo apt install python3-pyqt6
```

### Erreurs d'Import

```python
# Vérifier l'installation
python -c "
import sys
print('Python:', sys.version)
try:
    import PyQt6
    print('✅ PyQt6 disponible')
except ImportError:
    print('❌ PyQt6 non disponible')
"
```

### Application ne se lance pas

```bash
# 1. Vérifier les dépendances
pip check

# 2. Réinstaller les dépendances
pip install --force-reinstall -r requirements.txt

# 3. Validation complète
python validate_pyqt6_migration.py

# 4. Mode debug
python main.py --debug
```

### Problèmes de Performance

```bash
# Comparer les frameworks
python compare_frameworks.py

# Si PyQt6 est lent, utiliser CustomTkinter
# Dans main.py, changer:
set_gui_framework('customtkinter')
```

## Configuration Avancée

### Variables d'Environnement

```bash
# Framework GUI par défaut
export GUI_FRAMEWORK=pyqt6

# Mode debug
export DEBUG=1

# Répertoire de logs
export LOG_DIR=/path/to/logs
```

### Configuration PyQt6

```python
# Dans main.py, après set_gui_framework('pyqt6')
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Configuration globale PyQt6
QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
```

## Mise à Jour

### Mise à jour des Dépendances

```bash
# Mise à jour complète
pip install --upgrade -r requirements.txt

# Mise à jour PyQt6 uniquement
pip install --upgrade PyQt6
```

### Migration depuis CustomTkinter

Si vous avez une version antérieure avec CustomTkinter :

```bash
# 1. Sauvegarder la configuration actuelle
cp main.py main.py.backup

# 2. Exécuter la migration
python migrate_to_pyqt6.py

# 3. Valider la migration
python validate_pyqt6_migration.py
```

## Support

### Logs et Debugging

```bash
# Logs détaillés
tail -f logs/app.log

# Tests de diagnostic
python test/scripts/run_pyqt6_tests.py
```

### Rollback

```bash
# Revenir à CustomTkinter
# Dans main.py:
set_gui_framework('customtkinter')

# Ou restaurer les fichiers de sauvegarde
cp main.py.backup_* main.py
```

### Aide

- **Documentation**: `docs/PYQT6_MIGRATION.md`
- **Tests**: `test/integration/test_pyqt6_integration.py`
- **Exemples**: `test_pyqt6.py`
