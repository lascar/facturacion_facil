# 🐛 Problème : Glitch Visuel des Fenêtres de Factures

## 📋 Description du Problème

### Symptômes Observés
- **Glitch visuel bizarre** lors de l'ouverture des fenêtres "Nueva Factura" et "Editar Factura"
- La fenêtre s'ouvre normalement puis **"clignote"** ou se **repositionne** après ~500ms
- Effet visuel désagréable qui perturbe l'expérience utilisateur
- Le problème se produit **systématiquement** à chaque ouverture

### Contexte Technique
- **Environnement** : PyQt5 sur Linux
- **Fenêtres concernées** :
  - `CrearFacturaDialog` (Nueva Factura)
  - `EditarFacturaDialog` (Editar Factura) 
  - `VerFacturaDialog` (Ver Factura)
  - `FacturaEditWindow` (Fenêtre unifiée d'édition)

### Impact Utilisateur
- **Expérience dégradée** : L'interface semble "instable"
- **Confusion visuelle** : L'utilisateur peut penser que l'application a un bug
- **Perte de confiance** dans la stabilité de l'application

## 🔍 Analyse Technique Approfondie

### Code Problématique Identifié

**Dans `ui/facturas_pyqt5.py`** :
```python
# Ligne 573-581 (open_new_factura_window)
edit_window.setWindowFlags(edit_window.windowFlags() | Qt.WindowStaysOnTopHint)
edit_window.show()
edit_window.raise_()
edit_window.activateWindow()
edit_window.setFocus()

# ⚠️ PROBLÈME : QTimer qui modifie les flags après ouverture
QTimer.singleShot(500, lambda: self._remove_always_on_top(edit_window))

def _remove_always_on_top(self, window):
    """Retirer le flag WindowStaysOnTopHint d'une fenêtre"""
    try:
        if window and window.isVisible():
            flags = window.windowFlags()
            flags &= ~Qt.WindowStaysOnTopHint
            window.setWindowFlags(flags)  # ← CAUSE DU GLITCH
            window.show()                 # ← REPOSITIONNEMENT VISUEL
    except:
        pass
```

**Dans `utils/dialog_simple_foreground.py`** :
```python
def setup_simple_foreground_display(self):
    # Configuration avec WindowStaysOnTopHint temporaire
    self.setWindowFlags(
        Qt.Window |
        Qt.WindowCloseButtonHint |
        Qt.WindowTitleHint |
        Qt.WindowStaysOnTopHint  # ← FLAG TEMPORAIRE
    )
    
    # ⚠️ PROBLÈME : QTimer qui retire le flag après 3 secondes
    QTimer.singleShot(3000, self._remove_always_on_top)

def _remove_always_on_top(self):
    """Retire le flag WindowStaysOnTopHint après affichage"""
    try:
        if self.isVisible():
            self.setWindowFlags(
                Qt.Window |
                Qt.WindowCloseButtonHint |
                Qt.WindowTitleHint
            )
            self.show()  # ← REPOSITIONNEMENT VISUEL
            self.raise_()
            self.activateWindow()
    except:
        pass
```

### Séquence du Glitch

1. **T=0ms** : Ouverture de la fenêtre
   - `setWindowFlags()` avec `WindowStaysOnTopHint`
   - `show()` affiche la fenêtre au premier plan

2. **T=500ms** (ou 3000ms) : QTimer déclenché
   - `setWindowFlags()` retire `WindowStaysOnTopHint`
   - **`show()` force un redessin/repositionnement**
   - **GLITCH VISUEL** : La fenêtre "clignote" ou se repositionne

3. **Résultat** : L'utilisateur voit un effet visuel indésirable

### Pourquoi ce Glitch se Produit

#### 1. **Changement de Window Flags**
```python
# État initial
flags = Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint

# Après QTimer (changement de flags)
flags = Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowTitleHint
# WindowStaysOnTopHint retiré → Changement d'état de la fenêtre
```

#### 2. **Appel à show() Après Changement**
- `setWindowFlags()` modifie les propriétés de la fenêtre
- `show()` force Qt à **recalculer** la position et l'apparence
- **Effet visuel** : La fenêtre se "redessine" ou se "repositionne"

#### 3. **Timing Visible**
- Le délai (500ms ou 3000ms) est **suffisamment long** pour que l'utilisateur voie le changement
- **Trop court** pour être imperceptible
- **Trop long** pour être considéré comme normal

## 🎯 Objectifs de la Solution

### Critères de Réussite
1. **Élimination complète** du glitch visuel
2. **Maintien** de l'affichage au premier plan
3. **Compatibilité** avec toutes les plateformes (Windows, Linux, macOS)
4. **Performance** : Pas de délais ou timers inutiles
5. **Simplicité** : Code plus maintenable

### Contraintes Techniques
- **PyQt5** : Respecter les limitations du framework
- **Multi-plateforme** : Solution qui fonctionne partout
- **Rétrocompatibilité** : Ne pas casser les fonctionnalités existantes
- **Performance** : Pas d'impact sur la vitesse d'ouverture

## 📊 Impact du Problème

### Fréquence
- **100%** des ouvertures de fenêtres de factures
- **Reproductible** sur tous les environnements
- **Systématique** : Pas de conditions particulières

### Gravité
- **Cosmétique** mais **très visible**
- **Perception de qualité** dégradée
- **Expérience utilisateur** impactée négativement

### Urgence
- **Moyenne** : N'empêche pas l'utilisation
- **Importante** pour la perception de qualité
- **Facile à corriger** une fois la cause identifiée

## 🔬 Méthodes d'Investigation Utilisées

### 1. **Analyse du Code Source**
- Recherche des utilisations de `WindowStaysOnTopHint`
- Identification des `QTimer.singleShot()` suspects
- Traçage des appels à `setWindowFlags()` et `show()`

### 2. **Tests de Reproduction**
- Ouverture répétée des fenêtres concernées
- Observation du timing du glitch
- Corrélation avec les logs de debug

### 3. **Analyse des Mixins**
- Examen de `SimpleDialogForegroundMixin`
- Identification de la logique de forçage au premier plan
- Compréhension de la séquence temporelle

## 📚 Références Techniques

### Documentation Qt
- [Qt Window Flags](https://doc.qt.io/qt-5/qt.html#WindowType-enum)
- [QTimer Single Shot](https://doc.qt.io/qt-5/qtimer.html#singleShot)
- [QWidget setWindowFlags](https://doc.qt.io/qt-5/qwidget.html#setWindowFlags)

### Problèmes Similaires
- **Stack Overflow** : "Qt window flickers when changing flags"
- **Qt Forums** : "WindowStaysOnTopHint causing visual glitches"
- **PyQt5 Issues** : "Window repositioning after flag changes"

---

**Date d'identification** : 2025-01-21  
**Priorité** : Moyenne-Haute  
**Complexité** : Moyenne  
**Status** : ✅ **RÉSOLU** (voir solution dans `GLITCH_VISUAL_SOLUTION.md`)

---

## 🔗 Fichiers Liés

- **Solution** : [`docs/dev/solutions/GLITCH_VISUAL_SOLUTION.md`](../solutions/GLITCH_VISUAL_SOLUTION.md)
- **Fix appliqué** : [`docs/dev/fixes/GLITCH_FACTURA_WINDOWS_FIX.md`](../fixes/GLITCH_FACTURA_WINDOWS_FIX.md)
- **Tests** : [`test/regression/test_glitch_factura_windows_fix.py`](../../../test/regression/test_glitch_factura_windows_fix.py)
- **Nouveau mixin** : [`utils/dialog_no_glitch_foreground.py`](../../../utils/dialog_no_glitch_foreground.py)
