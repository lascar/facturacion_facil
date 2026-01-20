> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🪟 Installation sur Windows 11 - Facturación Fácil

## 📋 Prérequis

### 1. **Python 3.8+**
Télécharge et installe Python depuis [python.org](https://www.python.org/downloads/windows/)
- ✅ Coche "Add Python to PATH" pendant l'installation
- ✅ Choisis "Install for all users" si possible

### 2. **Git** (si pas déjà fait)
Télécharge depuis [git-scm.com](https://git-scm.com/download/win)

## 🚀 Installation étape par étape

### **Étape 1 : Cloner le projet**
```bash
git clone https://github.com/ton-username/facturacion_facil.git
cd facturacion_facil
```

### **Étape 2 : Créer un environnement virtuel**
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
venv\Scripts\activate
```

### **Étape 3 : Installer les dépendances**
```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt
```

### **Étape 4 : Vérifier l'installation**
```bash
# Tester l'application
python main.py
```

## 📦 Dépendances principales

Le fichier `requirements.txt` contient :
```
PyQt5>=5.15.0
reportlab>=3.6.0
Pillow>=8.0.0
```

## 🔧 Résolution des problèmes courants

### **Problème 1 : Python non trouvé**
```bash
# Vérifier que Python est installé
python --version
# ou
py --version
```

**Solution :** Réinstaller Python en cochant "Add to PATH"

### **Problème 2 : pip non trouvé**
```bash
# Utiliser le module pip directement
python -m pip --version
```

### **Problème 3 : Erreur PyQt5**
```bash
# Installer PyQt5 manuellement
pip install PyQt5
```

**Si ça ne marche pas :**
```bash
# Essayer avec conda (si Anaconda installé)
conda install pyqt
```

### **Problème 4 : Erreur de permissions**
```bash
# Exécuter PowerShell en tant qu'administrateur
# Puis réessayer l'installation
```

## 🎯 Scripts de lancement

### **Script batch pour Windows** (`start.bat`)
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python main.py
pause
```

### **Script PowerShell** (`start.ps1`)
```powershell
Set-Location $PSScriptRoot
.\venv\Scripts\Activate.ps1
python main.py
```

## 📁 Structure après installation

```
facturacion_facil/
├── venv/                    # Environnement virtuel
├── ui/                      # Interface utilisateur
├── database/                # Base de données
├── utils/                   # Utilitaires
├── logs/                    # Fichiers de log
├── main.py                  # Point d'entrée
├── requirements.txt         # Dépendances
└── README.md               # Documentation
```

## 🧪 Tests

### **Test rapide**
```bash
# Activer l'environnement
venv\Scripts\activate

# Lancer l'application
python main.py
```

### **Test des fonctionnalités**
1. **Fenêtre principale** doit s'ouvrir
2. **Boutons** doivent être cliquables
3. **Scroll avec molette** dans les fenêtres Productos/Organización/Facturas

## 🔄 Mise à jour

### **Mettre à jour le code**
```bash
git pull origin main
```

### **Mettre à jour les dépendances**
```bash
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

## 🎮 Utilisation quotidienne

### **Démarrage rapide**
1. Double-clic sur `start.bat` (si créé)
2. Ou ouvrir PowerShell/CMD dans le dossier :
   ```bash
   venv\Scripts\activate
   python main.py
   ```

## 🆘 Support

### **Logs d'erreur**
Les logs sont dans le dossier `logs/` :
- `app.log` - Log principal
- `error.log` - Erreurs uniquement

### **Problèmes fréquents**
1. **Antivirus** - Ajouter le dossier aux exceptions
2. **Firewall** - Autoriser Python si demandé
3. **Permissions** - Exécuter en tant qu'administrateur si nécessaire

## 🔧 Configuration avancée

### **Variables d'environnement** (optionnel)
```bash
# Dans PowerShell
$env:PYTHONPATH = "."
```

### **Raccourci bureau**
Créer un raccourci vers `start.bat` sur le bureau pour un accès rapide.

## 🚀 Installation automatique

### **Option 1 : Installation complète automatique**
```bash
# Double-clic sur le fichier ou dans PowerShell/CMD :
install.bat
```

### **Option 2 : Lancement rapide**
```bash
# Double-clic sur le fichier ou dans PowerShell/CMD :
start.bat
```

### **Option 3 : PowerShell (recommandé)**
```powershell
# Clic droit sur start.ps1 > "Exécuter avec PowerShell"
# Ou dans PowerShell :
.\start.ps1
```

## 🔧 Dépannage Windows spécifique

### **Erreur "Execution Policy"** (PowerShell)
```powershell
# Exécuter en tant qu'administrateur :
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Erreur "Module not found"**
```bash
# Réinstaller les dépendances
venv\Scripts\activate
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### **Problème d'antivirus**
1. Ajouter le dossier `facturacion_facil` aux exceptions
2. Ajouter `python.exe` aux exceptions
3. Désactiver temporairement la protection en temps réel

### **Erreur de permissions**
1. Clic droit sur `install.bat` > "Exécuter en tant qu'administrateur"
2. Ou déplacer le projet vers `C:\facturacion_facil`

## ✅ Checklist d'installation

- [ ] Python 3.8+ installé avec PATH
- [ ] Git installé
- [ ] Projet cloné
- [ ] `install.bat` exécuté avec succès
- [ ] Application testée avec `start.bat`
- [ ] Scroll testé dans les fenêtres Productos/Organización

## 🎯 Fonctionnalités à tester

### **Test du scroll** 🖱️
1. Ouvrir **Productos** → Utiliser la molette de souris
2. Ouvrir **Organización** → Scroller dans les formulaires
3. Ouvrir **Facturas** → Tester le scroll vertical

### **Test général**
- [ ] Fenêtre principale s'ouvre
- [ ] Tous les boutons fonctionnent
- [ ] Base de données se crée automatiquement
- [ ] Logs générés dans `logs/`

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
