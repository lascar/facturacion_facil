> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 📜 Fenêtres de Facturation Scrollables

## 📋 Vue d'ensemble

**Date** : 2026-01-21  
**Fonctionnalité** : Ajout du scroll vertical aux fenêtres de gestion et création de factures  
**Impact** : Amélioration de l'expérience utilisateur sur petits écrans

## ✨ Fonctionnalités Implémentées

### 1. **Gestión de Facturas (FacturasPyQt5Window)**

#### Avant
- Liste de factures sans scroll
- Contenu coupé sur petits écrans

#### Après
- ✅ Scroll vertical activé via `BasePyQt5Window`
- ✅ Liste complète accessible quelle que soit la taille de l'écran
- ✅ Utilise `ScrollableMixin` pour gestion automatique

#### Implémentation
```python
def setup_ui(self):
    # Activer le scroll pour la fenêtre
    self.setup_scrollable_content(enable_horizontal=False, enable_vertical=True)
    main_layout = self.get_content_layout()
    # ... reste du code
```

### 2. **Nueva/Editar Factura (FacturaEditWindow)**

#### Avant
- Formulaire sans scroll
- Boutons parfois hors de l'écran
- Sections coupées sur petits écrans

#### Après
- ✅ Contenu scrollable (info, client, produits, totaux)
- ✅ **Boutons toujours visibles** en bas (Guardar, Cancelar)
- ✅ QScrollArea personnalisé pour contrôle total

#### Implémentation
```python
def setup_ui(self):
    main_layout = QVBoxLayout(self)
    
    # Widget conteneur scrollable
    content_widget = QWidget()
    content_layout = QVBoxLayout(content_widget)
    content_layout.addWidget(info_group)
    content_layout.addWidget(client_group)
    content_layout.addWidget(products_group)
    content_layout.addWidget(totals_group)
    
    # Zone de scroll
    scroll_area = QScrollArea()
    scroll_area.setWidget(content_widget)
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(QScrollArea.NoFrame)
    main_layout.addWidget(scroll_area)
    
    # Boutons HORS du scroll (toujours visibles)
    buttons_layout = self.create_buttons_section()
    main_layout.addLayout(buttons_layout)
```

## 📁 Fichiers Modifiés

### 1. `ui/factura_edit_window.py`
- **Ligne 10** : Ajout import `QScrollArea`
- **Lignes 79-115** : Restructuration complète de `setup_ui()`
  - Création widget conteneur scrollable
  - Ajout QScrollArea
  - Boutons en dehors du scroll

### 2. `ui/facturas_pyqt5.py`
- **Ligne 77** : Appel `setup_scrollable_content()`
- **Ligne 75** : Commentaire mis à jour

## 🧪 Tests Créés

### Fichier : `test/behaviour/test_scrollable_windows_behaviour.py`

**3 tests BDD** :

1. **`test_factura_edit_window_is_scrollable`**
   - GIVEN: Une fenêtre FacturaEditWindow
   - WHEN: La fenêtre est créée
   - THEN: Elle doit contenir un QScrollArea

2. **`test_facturas_pyqt5_window_is_scrollable`**
   - GIVEN: Une fenêtre FacturasPyQt5Window
   - WHEN: La fenêtre est créée
   - THEN: Elle doit avoir le scroll activé via BasePyQt5Window

3. **`test_factura_edit_window_buttons_outside_scroll`**
   - GIVEN: Une fenêtre FacturaEditWindow
   - WHEN: La fenêtre est créée
   - THEN: Les boutons doivent être en dehors du QScrollArea

**Résultat** : ✅ 3/3 tests passent

**Exécution** :
```bash
pytest test/behaviour/test_scrollable_windows_behaviour.py -v
```

## 🎯 Avantages

### Pour l'Utilisateur
- ✅ **Accessibilité** : Tout le contenu accessible sur petits écrans
- ✅ **Boutons visibles** : Actions toujours disponibles
- ✅ **Expérience fluide** : Scroll naturel avec molette
- ✅ **Pas de contenu coupé** : Toutes les sections visibles

### Pour le Développement
- ✅ **Code réutilisable** : Deux approches (BasePyQt5Window et QScrollArea)
- ✅ **Tests complets** : Vérification automatique du scroll
- ✅ **Maintenable** : Structure claire et documentée
- ✅ **Extensible** : Facile d'ajouter le scroll à d'autres fenêtres

## 📊 Comparaison des Approches

| Aspect | BasePyQt5Window | QScrollArea Direct |
|--------|-----------------|-------------------|
| **Utilisation** | Fenêtres héritant de BasePyQt5Window | QDialog personnalisés |
| **Complexité** | Simple (1 ligne) | Moyenne (structure manuelle) |
| **Contrôle** | Automatique | Total |
| **Boutons fixes** | Non supporté | Oui (hors scroll) |
| **Exemple** | FacturasPyQt5Window | FacturaEditWindow |

## 🔮 Améliorations Futures

- [ ] Ajouter scroll aux autres fenêtres (Clientes, Stock)
- [ ] Configuration de la vitesse de scroll
- [ ] Scroll horizontal pour tableaux larges
- [ ] Animations de scroll plus fluides

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

