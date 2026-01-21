# 📖 Guide : Développement de Fenêtres Sans Glitch

## 🎯 Objectif

Ce guide explique comment créer des fenêtres PyQt5 qui s'affichent au premier plan **sans glitch visuel**, en évitant les pièges courants qui causent des repositionnements ou clignotements indésirables.

## ⚠️ Problèmes à Éviter

### 1. **Changements de Window Flags Après Ouverture**

❌ **À NE PAS FAIRE** :
```python
# PROBLÈME : Modifier les flags après show()
window.show()
window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
window.show()  # ← CAUSE UN GLITCH

# PROBLÈME : QTimer qui modifie les flags
QTimer.singleShot(500, lambda: self._change_flags(window))
```

✅ **BONNE PRATIQUE** :
```python
# SOLUTION : Définir les flags UNE SEULE FOIS
window.setWindowFlags(
    Qt.Window |
    Qt.WindowCloseButtonHint |
    Qt.WindowTitleHint
)
window.show()  # Une seule fois, avec les bons flags
```

### 2. **WindowStaysOnTopHint Temporaire**

❌ **À NE PAS FAIRE** :
```python
# PROBLÈME : Flag temporaire qui sera retiré
self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
self.show()

# Plus tard : retirer le flag → GLITCH
QTimer.singleShot(3000, self._remove_always_on_top)
```

✅ **BONNE PRATIQUE** :
```python
# SOLUTION : Pas de flag temporaire
self.setWindowFlags(
    Qt.Window |
    Qt.WindowCloseButtonHint |
    Qt.WindowTitleHint
    # Pas de WindowStaysOnTopHint temporaire
)
self.show()
```

### 3. **Appels Multiples à show()**

❌ **À NE PAS FAIRE** :
```python
# PROBLÈME : Multiples appels à show()
window.show()
window.setWindowFlags(new_flags)
window.show()  # ← REPOSITIONNEMENT VISUEL
```

✅ **BONNE PRATIQUE** :
```python
# SOLUTION : Un seul appel à show()
window.setWindowFlags(final_flags)
window.show()  # Une seule fois
```

## 🛠️ Mixin Recommandé

### Utilisation de NoGlitchDialogForegroundMixin

```python
from utils.dialog_no_glitch_foreground import NoGlitchDialogForegroundMixin

class MonDialog(QDialog, NoGlitchDialogForegroundMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mon Dialog")
        self.resize(800, 600)
        
        # Configuration de l'UI
        self.setup_ui()
        
        # Configuration sans glitch (à la fin)
        self.setup_no_glitch_foreground_display()
    
    def setup_ui(self):
        """Configurer l'interface utilisateur"""
        # ... widgets et layouts ...
        pass
```

### Avantages du Mixin

1. **Pas de glitch** : Flags définis une seule fois
2. **Forçage automatique** : Override de `show()` intégré
3. **Multi-plateforme** : Fonctionne sur Windows, Linux, macOS
4. **Simple** : Une seule ligne d'appel

## 📋 Checklist de Développement

### ✅ Avant de Créer une Nouvelle Fenêtre

- [ ] **Hériter** de `NoGlitchDialogForegroundMixin`
- [ ] **Appeler** `setup_no_glitch_foreground_display()` à la fin du constructeur
- [ ] **Éviter** `WindowStaysOnTopHint` temporaire
- [ ] **Éviter** les `QTimer` qui modifient les flags
- [ ] **Tester** l'ouverture pour vérifier l'absence de glitch

### ✅ Lors de la Migration d'une Fenêtre Existante

- [ ] **Remplacer** `SimpleDialogForegroundMixin` par `NoGlitchDialogForegroundMixin`
- [ ] **Changer** `setup_simple_foreground_display()` en `setup_no_glitch_foreground_display()`
- [ ] **Supprimer** les `QTimer` qui modifient les flags
- [ ] **Simplifier** les méthodes d'ouverture
- [ ] **Tester** pour confirmer l'élimination du glitch

## 🔧 Patterns de Forçage au Premier Plan

### Pattern Simple (Recommandé)

```python
def open_dialog(self):
    """Ouvrir un dialog au premier plan sans glitch"""
    dialog = MonDialog(self)
    
    # Affichage simple (le mixin gère le forçage)
    dialog.show()
    
    # Optionnel : forçage supplémentaire si nécessaire
    from utils.dialog_no_glitch_foreground import force_dialog_no_glitch_foreground
    force_dialog_no_glitch_foreground(dialog)
```

### Pattern pour Fenêtres Sans Mixin

```python
def open_simple_window(self):
    """Ouvrir une fenêtre simple au premier plan"""
    window = QDialog(self)
    window.setWindowTitle("Ma Fenêtre")
    window.resize(600, 400)
    
    # Configuration des flags (une seule fois)
    window.setWindowFlags(
        Qt.Window |
        Qt.WindowCloseButtonHint |
        Qt.WindowTitleHint
    )
    
    # Affichage et forçage
    window.show()
    window.raise_()
    window.activateWindow()
    window.setFocus()
```

## 🧪 Tests et Validation

### Test Visuel Manuel

```python
def test_no_glitch_visual():
    """Test visuel pour vérifier l'absence de glitch"""
    app = QApplication([])
    
    # Créer et ouvrir le dialog
    dialog = MonDialog()
    dialog.show()
    
    # Observer : pas de clignotement ou repositionnement
    # La fenêtre doit s'ouvrir de manière fluide
    
    app.exec_()
```

### Test Automatique des Flags

```python
def test_window_flags_stability():
    """Test que les flags ne changent pas après ouverture"""
    dialog = MonDialog()
    
    # Capturer les flags initiaux
    initial_flags = dialog.windowFlags()
    
    # Ouvrir la fenêtre
    dialog.show()
    
    # Vérifier que les flags n'ont pas changé
    final_flags = dialog.windowFlags()
    assert initial_flags == final_flags, "Les flags ne doivent pas changer"
    
    dialog.close()
```

## 📚 Références et Ressources

### Documentation Qt Pertinente

- **Window Flags** : [Qt::WindowFlags](https://doc.qt.io/qt-5/qt.html#WindowType-enum)
- **QWidget::show()** : [Documentation show()](https://doc.qt.io/qt-5/qwidget.html#show)
- **QWidget::setWindowFlags()** : [Documentation setWindowFlags()](https://doc.qt.io/qt-5/qwidget.html#setWindowFlags)

### Problèmes Courants

1. **"Window flickers on Linux"** → Utiliser le mixin sans glitch
2. **"Dialog opens behind main window"** → Forçage simple avec `raise_()` et `activateWindow()`
3. **"Window repositions after opening"** → Éviter les changements de flags

### Outils de Debug

```python
def debug_window_flags(window):
    """Afficher les flags d'une fenêtre pour debug"""
    flags = window.windowFlags()
    print(f"Window flags: {flags}")
    
    if flags & Qt.WindowStaysOnTopHint:
        print("  - WindowStaysOnTopHint: ACTIVÉ")
    if flags & Qt.Window:
        print("  - Window: ACTIVÉ")
    if flags & Qt.WindowCloseButtonHint:
        print("  - WindowCloseButtonHint: ACTIVÉ")
```

## 🎯 Bonnes Pratiques Résumées

### DO ✅

1. **Utiliser** `NoGlitchDialogForegroundMixin` pour les nouveaux dialogs
2. **Définir** les window flags une seule fois dans le constructeur
3. **Appeler** `show()` une seule fois avec les flags finaux
4. **Tester** visuellement l'ouverture des fenêtres
5. **Documenter** les choix de design pour les fenêtres complexes

### DON'T ❌

1. **Ne pas** utiliser `WindowStaysOnTopHint` temporaire
2. **Ne pas** modifier les flags après `show()`
3. **Ne pas** utiliser `QTimer` pour changer l'apparence
4. **Ne pas** appeler `show()` plusieurs fois
5. **Ne pas** ignorer les glitches visuels "mineurs"

---

**Version** : 1.0  
**Date** : 2025-01-21  
**Auteur** : Équipe de développement facturacion_facil  
**Status** : ✅ **VALIDÉ** et **TESTÉ**
