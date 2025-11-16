# Migration vers PyQt6

## Vue d'ensemble

Facturación Fácil a été migré de CustomTkinter vers **PyQt6** pour offrir de meilleures performances et une meilleure compatibilité Windows.

## Avantages de PyQt6

### 🚀 Performances
- **25% plus rapide** que CustomTkinter
- Création de widgets optimisée
- Rendu graphique accéléré
- Gestion mémoire améliorée

### 🖥️ Interface Native
- Look and feel natif Windows
- Support des thèmes système
- Widgets riches et modernes
- Meilleure intégration OS

### 🔧 Compatibilité
- Support Windows 10/11 optimal
- Moins de dépendances problématiques
- Stabilité améliorée
- Meilleur support multi-écrans

## Architecture

### Couche d'Abstraction GUI

```
gui/
├── abstract_gui.py          # Interfaces abstraites
├── gui_manager.py           # Gestionnaire de frameworks
├── pyqt6_impl.py           # Implémentation PyQt6
├── customtkinter_impl.py   # Implémentation CustomTkinter (legacy)
└── tkinter_impl.py         # Implémentation Tkinter (fallback)
```

### Changement de Framework

```python
from gui import set_gui_framework

# PyQt6 (par défaut)
set_gui_framework('pyqt6')

# CustomTkinter (legacy)
set_gui_framework('customtkinter')

# Tkinter (fallback)
set_gui_framework('tkinter')
```

## Migration Automatique

### Scripts de Migration

1. **Migration complète**
   ```bash
   python migrate_to_pyqt6.py
   ```

2. **Patch des imports**
   ```bash
   python patch_customtkinter_imports.py
   ```

3. **Validation**
   ```bash
   python validate_pyqt6_migration.py
   ```

### Fichiers Modifiés

- `main.py` → Configuré pour PyQt6
- `ui/main_window.py` → Version PyQt6 native
- Toutes les fenêtres UI → Patchées avec adaptateur
- `requirements.txt` → PyQt6 ajouté

### Sauvegardes

Tous les fichiers originaux sont sauvegardés :
- Format: `fichier.py.backup_YYYYMMDD_HHMMSS`
- Restauration possible à tout moment

## Tests

### Tests PyQt6 Spécifiques

```bash
# Tests d'intégration PyQt6
python test/integration/test_pyqt6_integration.py

# Tests UI PyQt6
python test/ui/test_pyqt6_ui.py

# Suite complète de tests
python test/scripts/run_pyqt6_tests.py
```

### Comparaison de Performance

```bash
python compare_frameworks.py
```

Résultats typiques :
```
Framework       Setup    Factory  Window   Widgets  Total   
-----------------------------------------------------------------
pyqt6           0.073    0.000    0.001    0.005    0.079   
customtkinter   0.046    0.000    0.012    0.047    0.105   
tkinter         0.008    0.000    0.113    0.010    0.131   

🏆 Framework le plus rapide: PYQT6 (0.079s)
```

## Compatibilité

### Adaptateur CustomTkinter

Pour les fenêtres existantes, un adaptateur transparent permet la compatibilité :

```python
# L'ancien code CustomTkinter fonctionne automatiquement
import customtkinter as ctk

window = ctk.CTkToplevel()  # → Utilise PyQt6 en arrière-plan
frame = ctk.CTkFrame(window)
label = ctk.CTkLabel(frame, text="Test")
```

### Widgets Supportés

| Widget | PyQt6 | CustomTkinter | Tkinter |
|--------|-------|---------------|---------|
| Window | ✅ | ✅ | ✅ |
| Frame | ✅ | ✅ | ✅ |
| Label | ✅ | ✅ | ✅ |
| Button | ✅ | ✅ | ✅ |
| Entry | ✅ | ✅ | ✅ |
| TreeView | ✅ | ✅ | ✅ |
| Combobox | ✅ | ✅ | ✅ |
| ScrollableFrame | ✅ | ✅ | ❌ |

## Rollback

### Option 1: Changement de Framework

```python
# Dans main.py
from gui import set_gui_framework
set_gui_framework('customtkinter')  # Au lieu de 'pyqt6'
```

### Option 2: Restauration des Fichiers

```bash
# Restaurer main.py
cp main.py.backup_YYYYMMDD_HHMMSS main.py

# Restaurer main_window.py
cp ui/main_window.py.backup_YYYYMMDD_HHMMSS ui/main_window.py

# Restaurer autres fichiers si nécessaire
```

## Dépannage

### PyQt6 Non Installé

```bash
pip install PyQt6
```

### Erreurs d'Import

```python
# Vérifier que le framework est défini
from gui import set_gui_framework
set_gui_framework('pyqt6')
```

### Tests qui Échouent

```bash
# Validation complète
python validate_pyqt6_migration.py

# Tests spécifiques
python test_pyqt6.py
```

## Support

- **Documentation**: `docs/`
- **Tests**: `test/integration/test_pyqt6_integration.py`
- **Exemples**: `test_pyqt6.py`, `main_pyqt6_demo.py`
- **Comparaisons**: `compare_frameworks.py`
