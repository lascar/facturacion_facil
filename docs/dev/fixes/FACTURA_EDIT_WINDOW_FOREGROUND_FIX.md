# Correction : Fenêtre d'Édition de Facture en Arrière-Plan

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

## 📋 Contexte

Lors de la refactorisation de la gestion des facturas pour séparer la liste et le formulaire d'édition en deux fenêtres distinctes, deux problèmes majeurs sont apparus :

1. **Blocage de l'application** : L'utilisation de `exec_()` (dialogue modal) bloquait complètement l'interface
2. **Fenêtre en arrière-plan** : Après résolution du blocage, la fenêtre d'édition s'ouvrait derrière la fenêtre principale

## 🔍 Problème 1 : Blocage de l'Application

### Symptômes
- Dès l'ouverture d'une fenêtre de factura (nouvelle ou édition), l'application se bloquait
- L'utilisateur devait fermer l'application avec `Ctrl+Z`
- Impossible d'interagir avec l'application

### Cause Racine
L'utilisation de `exec_()` pour afficher la fenêtre d'édition :

```python
# ❌ Code problématique
edit_window = FacturaEditWindow(...)
edit_window.exec_()  # Bloque l'exécution jusqu'à fermeture
```

`exec_()` est une méthode **bloquante** (modale) qui :
- Suspend l'exécution du code appelant
- Empêche toute interaction avec les autres fenêtres
- Attend que la fenêtre soit fermée pour continuer

### Solution
Remplacer `exec_()` par `show()` pour un affichage **non-modal** :

```python
# ✅ Solution
edit_window = FacturaEditWindow(...)
self.current_edit_window = edit_window  # Garder référence
edit_window.show()  # Non-bloquant
```

**Fichiers modifiés** :
- `ui/facturas_pyqt5.py` : Lignes 569, 612
- `ui/factura_edit_window.py` : Lignes 639, 650 (`accept()` → `close()`)

## 🔍 Problème 2 : Fenêtre en Arrière-Plan

### Symptômes
- Après résolution du blocage, la fenêtre d'édition s'ouvrait derrière la fenêtre principale
- L'utilisateur devait manuellement cliquer sur la fenêtre pour la voir
- Mauvaise expérience utilisateur

### Tentatives Infructueuses

#### Tentative 1 : Utilisation du Mixin Existant
```python
# ❌ Ne fonctionne pas
edit_window.setup_simple_foreground_display()
```
Le mixin `SimpleDialogForegroundMixin` était déjà hérité mais appelé trop tôt dans le cycle de vie.

#### Tentative 2 : Séquence Standard PyQt5
```python
# ❌ Insuffisant
edit_window.show()
edit_window.raise_()
edit_window.activateWindow()
```
Cette séquence standard ne suffit pas sur certains gestionnaires de fenêtres Linux.

### Solution Finale : Flag WindowStaysOnTopHint Temporaire

La solution consiste à forcer temporairement la fenêtre au premier plan avec le flag `WindowStaysOnTopHint`, puis le retirer après 500ms :

```python
# ✅ Solution agressive et efficace
from PyQt5.QtCore import Qt, QTimer

# 1. Ajouter le flag "always on top"
edit_window.setWindowFlags(edit_window.windowFlags() | Qt.WindowStaysOnTopHint)

# 2. Séquence d'affichage complète
edit_window.show()
edit_window.raise_()
edit_window.activateWindow()
edit_window.setFocus()

# 3. Retirer le flag après 500ms
QTimer.singleShot(500, lambda: self._remove_always_on_top(edit_window))
```

**Méthode helper** :
```python
def _remove_always_on_top(self, window):
    """Retirer le flag WindowStaysOnTopHint d'une fenêtre"""
    try:
        if window and window.isVisible():
            from PyQt5.QtCore import Qt
            flags = window.windowFlags()
            flags &= ~Qt.WindowStaysOnTopHint
            window.setWindowFlags(flags)
            window.show()
    except:
        pass
```

## 📦 Fichiers Modifiés

### `ui/facturas_pyqt5.py`
- **Lignes 565-581** : `open_new_factura_window()` - Affichage avec flag temporaire
- **Lignes 612-628** : `open_edit_factura_window()` - Affichage avec flag temporaire  
- **Lignes 634-644** : `_remove_always_on_top()` - Nouvelle méthode helper

### `ui/factura_edit_window.py`
- **Lignes 71-76** : Suppression de l'appel à `setup_simple_foreground_display()` dans `__init__`
- **Lignes 639, 650** : Remplacement de `self.accept()` par `self.close()`

## ✅ Résultat

### Comportement Final
1. ✅ L'application ne se bloque plus lors de l'ouverture d'une fenêtre d'édition
2. ✅ La fenêtre d'édition s'ouvre **au premier plan**
3. ✅ Après 500ms, la fenêtre redevient normale (peut passer en arrière-plan si l'utilisateur clique ailleurs)
4. ✅ L'utilisateur peut interagir avec les deux fenêtres simultanément

### Avantages
- **Non-bloquant** : L'utilisateur peut consulter la liste pendant l'édition
- **Premier plan garanti** : Le flag `WindowStaysOnTopHint` force l'affichage
- **Comportement naturel** : Après 500ms, la fenêtre se comporte normalement
- **Multiplateforme** : Fonctionne sur Windows, Linux, macOS

## 🔧 Technique Utilisée

### Pourquoi WindowStaysOnTopHint ?
- Force la fenêtre à rester au-dessus de **toutes** les autres fenêtres
- Garanti par Qt sur toutes les plateformes
- Temporaire (500ms) pour éviter de gêner l'utilisateur

### Pourquoi QTimer.singleShot ?
- Permet de retirer le flag après un délai
- Non-bloquant (asynchrone)
- Évite que la fenêtre reste "always on top" indéfiniment

## 📚 Références

- [Documentation Qt - Window Flags](https://doc.qt.io/qt-5/qt.html#WindowType-enum)
- [Documentation Qt - QTimer](https://doc.qt.io/qt-5/qtimer.html)
- Fichier : [`utils/dialog_simple_foreground.py`](../../utils/dialog_simple_foreground.py)
- Refactorisation : [Séparation Liste/Formulaire Facturas](../features/FACTURA_EDIT_WINDOW.md)

---

**Date** : 2026-01-20  
**Auteur** : Augment Agent  
**Statut** : ✅ Résolu et testé

