# 🪟 Facturación Fácil - Windows 11 Edition

## 🚀 Installation Rapide pour Windows 11

### Méthode 1: Script Automatisé (Recommandé)

```powershell
# Ouvrir Windows Terminal en tant qu'Administrateur
# Naviguer vers le dossier du projet
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\Install-Windows11.ps1 -CreateShortcut -DevTools
```

### Méthode 2: Installation Manuelle

```cmd
# 1. Installer Python depuis Microsoft Store
winget install Python.Python.3.12

# 2. Créer l'environnement
python -m venv venv
venv\Scripts\activate.bat

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Tester l'installation
python test_windows11_compatibility.py

# 5. Lancer l'application
python main.py
```

## ✨ Optimisations Windows 11

### 🎨 Interface Moderne
- **Fluent Design**: Interface adaptée au design moderne de Windows 11
- **Thème automatique**: Détection du mode sombre/clair du système
- **Snap Layouts**: Support natif pour l'organisation des fenêtres
- **Scaling DPI**: Adaptation automatique aux écrans haute résolution

### ⚡ Performance
- **PyQt6**: Framework GUI optimisé pour Windows 11
- **Multi-threading**: Interface réactive même avec de gros volumes de données
- **Mémoire optimisée**: Gestion efficace des ressources système
- **Démarrage rapide**: Temps de lancement réduit

### 🔒 Sécurité
- **Windows Defender**: Protection automatique des fichiers
- **SmartScreen**: Vérification des téléchargements
- **Sandboxing**: Exécution sécurisée de l'application
- **Chiffrement**: Protection des données sensibles

## 🛠️ Outils de Développement

### Scripts Disponibles

| Script | Description | Usage |
|--------|-------------|-------|
| `Install-Windows11.ps1` | Installation automatisée PowerShell | `.\Install-Windows11.ps1` |
| `install_windows11.bat` | Installation automatisée Batch | `install_windows11.bat` |
| `test_windows11_compatibility.py` | Test de compatibilité | `python test_windows11_compatibility.py` |
| `build_exe.py` | Construction d'exécutable | `python build_exe.py` |

### Commandes Utiles

```powershell
# Test complet de l'application
python -m pytest tests/ -v

# Construction d'exécutable optimisé
python build_exe.py

# Nettoyage des fichiers temporaires
Remove-Item -Recurse -Force __pycache__, *.pyc, build/, dist/

# Mise à jour des dépendances
pip install --upgrade -r requirements.txt
```

## 📋 Configuration Système Recommandée

### Matériel
- **CPU**: Intel Core i3 / AMD Ryzen 3 ou supérieur
- **RAM**: 8 GB (4 GB minimum)
- **Stockage**: 2 GB d'espace libre
- **Écran**: 1920x1080 (1366x768 minimum)

### Logiciels
- **Windows 11**: Version 21H2 ou supérieure
- **Python**: 3.12+ (3.10+ compatible)
- **Windows Terminal**: Recommandé pour l'installation
- **Microsoft Store**: Pour installation simplifiée de Python

## 🔧 Dépannage Windows 11

### Problèmes Courants

#### Python non reconnu
```powershell
# Vérifier l'installation
Get-Command python
# Si non trouvé, réinstaller depuis Microsoft Store
```

#### Erreur d'exécution de script PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Problème de permissions
```powershell
# Exécuter en tant qu'administrateur
Start-Process powershell -Verb runAs
```

#### PyQt6 ne s'installe pas
```cmd
# Mettre à jour pip et setuptools
python -m pip install --upgrade pip setuptools wheel
pip install PyQt6
```

### Optimisations Avancées

#### Pour écrans 4K/haute résolution
```cmd
set QT_SCALE_FACTOR=1.25
python main.py
```

#### Pour systèmes avec peu de RAM
```cmd
set PYTHONOPTIMIZE=1
python main.py
```

#### Mode haute performance
```powershell
# Configurer le plan d'alimentation
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

## 📦 Distribution

### Créer un Exécutable
```cmd
python build_exe.py
# Résultat dans dist/FacturacionFacil.exe
```

### Créer un Installateur
```powershell
# Utiliser Inno Setup ou NSIS pour créer un installateur professionnel
# Fichiers de configuration disponibles dans deploy/
```

## 🆘 Support

### Logs et Diagnostic
- **Logs application**: `logs/facturacion_facil.log`
- **Logs erreurs**: `logs/facturacion_facil_errors.log`
- **Test compatibilité**: `python test_windows11_compatibility.py`

### Ressources
- **Documentation complète**: `doc/manual_instalacion_windows.md`
- **Guide utilisateur**: `doc/tutorial_uso_interfaz.md`
- **Tests**: `python -m pytest tests/ -v`

---

## 🎯 Fonctionnalités Spécifiques Windows 11

### Intégration Système
- ✅ Notifications Windows natives
- ✅ Barre des tâches avec aperçu
- ✅ Menu contextuel moderne
- ✅ Support des raccourcis clavier Windows 11
- ✅ Intégration avec l'Explorateur de fichiers

### Accessibilité
- ✅ Support du narrateur Windows
- ✅ Contraste élevé automatique
- ✅ Navigation au clavier complète
- ✅ Zoom et mise à l'échelle adaptative

### Performance
- ✅ Démarrage optimisé avec Windows 11
- ✅ Gestion mémoire améliorée
- ✅ Support multi-moniteur natif
- ✅ Rendu graphique accéléré

---

**🎉 Profitez de Facturación Fácil optimisé pour Windows 11!**

Pour toute question ou problème, consultez la documentation complète ou créez un ticket de support.
