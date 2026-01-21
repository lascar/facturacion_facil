# 🔧 Fix du Glitch des Fenêtres de Factures

## 📋 Problème Identifié

**Symptôme** : Glitch visuel bizarre lors de l'ouverture des fenêtres "Nueva Factura" et "Editar Factura"

**Cause racine** : 
- Utilisation de `WindowStaysOnTopHint` temporaire
- `QTimer.singleShot()` qui modifie les flags de fenêtre après ouverture
- Appel à `setWindowFlags()` + `show()` qui cause un repositionnement visuel

**Code problématique** :
```python
# Ancien code avec glitch
edit_window.setWindowFlags(edit_window.windowFlags() | Qt.WindowStaysOnTopHint)
edit_window.show()
# ...
QTimer.singleShot(500, lambda: self._remove_always_on_top(edit_window))

def _remove_always_on_top(self, window):
    flags = window.windowFlags()
    flags &= ~Qt.WindowStaysOnTopHint
    window.setWindowFlags(flags)  # ← CAUSE DU GLITCH
    window.show()  # ← REPOSITIONNEMENT VISUEL
```

## ✅ Solution Implémentée

### 1. **Nouveau Mixin Sans Glitch**

Créé `utils/dialog_no_glitch_foreground.py` avec `NoGlitchDialogForegroundMixin` :

**Caractéristiques** :
- ❌ **Pas de `WindowStaysOnTopHint`** temporaire
- ❌ **Pas de `QTimer`** qui modifie les flags
- ❌ **Pas de `setWindowFlags()`** après ouverture
- ✅ **Flags fixes** définis une seule fois
- ✅ **Forçage simple** avec `raise_()`, `activateWindow()`, `setFocus()`

```python
class NoGlitchDialogForegroundMixin:
    def setup_no_glitch_foreground_display(self):
        # Flags FIXES (pas de changement après ouverture)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowCloseButtonHint |
            Qt.WindowTitleHint
            # PAS de WindowStaysOnTopHint
        )
        
    def show(self):
        super().show()
        # Forçage simple SANS modification de flags
        self._no_glitch_force_foreground()
```

### 2. **Classes Modifiées**

**Avant** (avec glitch) :
```python
class CrearFacturaDialog(QDialog, SimpleDialogForegroundMixin):
    def __init__(self, ...):
        # ...
        self.setup_simple_foreground_display()  # ← Glitch
```

**Après** (sans glitch) :
```python
class CrearFacturaDialog(QDialog, NoGlitchDialogForegroundMixin):
    def __init__(self, ...):
        # ...
        self.setup_no_glitch_foreground_display()  # ← Sans glitch
```

### 3. **Fichiers Modifiés**

#### `utils/dialog_no_glitch_foreground.py` ✨ **NOUVEAU**
- Mixin `NoGlitchDialogForegroundMixin`
- Fonction `force_dialog_no_glitch_foreground()`

#### `ui/facturas_pyqt5.py`
- **Ligne 35** : Import du nouveau mixin
- **Ligne 1550** : `CrearFacturaDialog` utilise `NoGlitchDialogForegroundMixin`
- **Ligne 1577** : Appel à `setup_no_glitch_foreground_display()`
- **Ligne 2042** : `EditarFacturaDialog` utilise `NoGlitchDialogForegroundMixin`
- **Ligne 2072** : Appel à `setup_no_glitch_foreground_display()`
- **Ligne 2646** : `VerFacturaDialog` utilise `NoGlitchDialogForegroundMixin`
- **Ligne 2658** : Appel à `setup_no_glitch_foreground_display()`
- **Lignes 571-575** : Affichage simple de `FacturaEditWindow` (sans flags temporaires)
- **Lignes 612-616** : Affichage simple de `FacturaEditWindow` (sans flags temporaires)
- **Ligne 630-640** : Suppression de `_remove_always_on_top()` (plus utilisée)
- **Lignes 1282, 1353** : Utilisation de `force_dialog_no_glitch_foreground()`

#### `ui/factura_edit_window.py`
- **Ligne 18** : Import du nouveau mixin
- **Ligne 23** : `FacturaEditWindow` utilise `NoGlitchDialogForegroundMixin`

## 🧪 Tests de Validation

### Test Automatique
```bash
python3 -c "
from utils.dialog_no_glitch_foreground import NoGlitchDialogForegroundMixin
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog
from ui.factura_edit_window import FacturaEditWindow

# Vérifier les héritages
assert issubclass(CrearFacturaDialog, NoGlitchDialogForegroundMixin)
assert issubclass(EditarFacturaDialog, NoGlitchDialogForegroundMixin)
assert issubclass(FacturaEditWindow, NoGlitchDialogForegroundMixin)

print('✅ SUCCÈS: Toutes les classes utilisent le mixin sans glitch')
"
```

### Test de Régression
Fichier : `test/regression/test_glitch_factura_windows_fix.py`

## 🎯 Résultat

### ✅ **Avant le Fix**
- Glitch visuel lors de l'ouverture des fenêtres
- Fenêtre qui "clignote" ou se "repositionne" après 500ms
- Changements de flags visibles par l'utilisateur

### ✅ **Après le Fix**
- **Ouverture fluide** sans glitch visuel
- **Pas de repositionnement** après ouverture
- **Flags fixes** définis une seule fois
- **Fenêtres toujours au premier plan** sans effets indésirables

## 📚 Références Techniques

### Cause du Glitch
Le glitch était causé par cette séquence :
1. **Ouverture** avec `WindowStaysOnTopHint`
2. **500ms plus tard** : `setWindowFlags()` retire le flag
3. **Appel à `show()`** : La fenêtre se repositionne/redessine

### Solution
Élimination complète des changements de flags après ouverture :
- Flags définis **une seule fois** dans le constructeur
- **Pas de `QTimer`** qui modifie l'apparence
- **Forçage simple** sans modification de l'état de la fenêtre

---

## 🔄 Migration

Pour appliquer ce fix à d'autres fenêtres :

1. **Remplacer l'import** :
```python
# Ancien
from utils.dialog_simple_foreground import SimpleDialogForegroundMixin

# Nouveau
from utils.dialog_no_glitch_foreground import NoGlitchDialogForegroundMixin
```

2. **Changer l'héritage** :
```python
# Ancien
class MonDialog(QDialog, SimpleDialogForegroundMixin):

# Nouveau  
class MonDialog(QDialog, NoGlitchDialogForegroundMixin):
```

3. **Mettre à jour l'appel** :
```python
# Ancien
self.setup_simple_foreground_display()

# Nouveau
self.setup_no_glitch_foreground_display()
```

---

**Date** : 2025-01-21
**Status** : ✅ **RÉSOLU**
**Impact** : Amélioration de l'expérience utilisateur - Ouverture fluide des fenêtres

---

## 🔗 Documentation Complète

- **Problème détaillé** : [`docs/dev/problems/GLITCH_VISUAL_FENETRE_FACTURES.md`](../problems/GLITCH_VISUAL_FENETRE_FACTURES.md)
- **Solution technique** : [`docs/dev/solutions/GLITCH_VISUAL_SOLUTION.md`](../solutions/GLITCH_VISUAL_SOLUTION.md)
- **Guide de développement** : [`docs/dev/guides/GUIDE_FENETRE_SANS_GLITCH.md`](../guides/GUIDE_FENETRE_SANS_GLITCH.md)
- **Tests de régression** : [`test/regression/test_glitch_factura_windows_fix.py`](../../../test/regression/test_glitch_factura_windows_fix.py)
