> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🖱️ Fonctionnalité de Scroll avec la Molette de Souris

## 📋 Vue d'ensemble

Cette documentation décrit la nouvelle fonctionnalité de scroll avec la molette de souris ajoutée aux fenêtres PyQt5 de l'application Facturación Fácil.

## ✨ Fonctionnalités

### 🎯 **Scroll automatique**
- **Scroll vertical** avec la molette de souris dans toutes les fenêtres
- **Détection automatique** du contenu qui dépasse la taille de l'écran
- **Scroll fluide** et réactif
- **Support multi-plateforme** (Windows, Linux, macOS)

### 🔧 **Fenêtres avec scroll activé**
- ✅ **Productos** - Gestion des produits
- ✅ **Organización** - Configuration de l'organisation
- ✅ **Facturas (Gestión)** - Gestion des factures (liste scrollable)
- ✅ **Facturas (Nueva/Editar)** - Création/édition de factures (contenu scrollable, boutons fixes)
- ⚪ **Clientes** - Gestion des clients (peut être activé si nécessaire)
- ⚪ **Stock** - Gestion du stock (peut être activé si nécessaire)

## 🏗️ Architecture technique

### **Composants principaux**

1. **`ScrollableMixin`** (`ui/scroll_mixin_pyqt5.py`)
   - Mixin qui ajoute le support du scroll
   - Gestion des événements de molette
   - Configuration flexible du scroll horizontal/vertical

2. **`BasePyQt5Window`** (`ui/base_pyqt5_window.py`)
   - Classe de base modifiée pour intégrer le scroll
   - Méthodes utilitaires pour activer/désactiver le scroll
   - Support automatique du scroll pour les fenêtres filles

### **Utilisation dans le code**

#### **Méthode 1 : Utiliser BasePyQt5Window (Recommandé)**

```python
# Dans une fenêtre PyQt5 héritant de BasePyQt5Window
class MaFenetre(BasePyQt5Window):
    def setup_ui(self):
        # Activer le scroll pour cette fenêtre
        self.setup_scrollable_content(enable_horizontal=False, enable_vertical=True)

        # Obtenir le layout de contenu (scrollable)
        main_layout = self.get_content_layout()

        # Ajouter le contenu normalement
        main_layout.addWidget(mon_widget)
```

#### **Méthode 2 : Utiliser QScrollArea directement (Pour QDialog)**

```python
# Dans un QDialog personnalisé (ex: FacturaEditWindow)
class MonDialog(QDialog):
    def setup_ui(self):
        # Layout principal du dialog
        main_layout = QVBoxLayout(self)

        # Créer un widget conteneur pour le contenu scrollable
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Ajouter le contenu au layout scrollable
        content_layout.addWidget(mon_widget)

        # Créer une zone de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)

        # Ajouter la zone de scroll au layout principal
        main_layout.addWidget(scroll_area)

        # Boutons en dehors du scroll (toujours visibles)
        buttons_layout = self.create_buttons()
        main_layout.addLayout(buttons_layout)
```

## 🧪 Tests

### **Tests unitaires**
```bash
# Exécuter les tests de scroll
python3 test/unit/test_scroll_functionality.py
```

### **Test interactif**
```bash
# Lancer le test interactif
python3 test_scroll_functionality.py
```

## 🎮 Utilisation

### **Pour l'utilisateur final**
1. **Ouvrir une fenêtre** (Productos, Organización, ou Facturas)
2. **Utiliser la molette de souris** pour faire défiler le contenu
3. **Scroll fluide** vers le haut et vers le bas
4. **Fonctionne partout** dans la fenêtre (pas seulement sur les barres de scroll)

### **Raccourcis disponibles**
- **Molette vers le haut** : Scroll vers le haut
- **Molette vers le bas** : Scroll vers le bas
- **Scroll fluide** : Pas de saccades, mouvement naturel

## 🔧 Configuration

### **Activer le scroll dans une nouvelle fenêtre**

```python
class NouvelleFenetre(BasePyQt5Window):
    def __init__(self, parent=None):
        # Activer le scroll par défaut
        super().__init__(parent, title="Ma Fenêtre", enable_scroll=True)

    def setup_ui(self):
        # Configurer le scroll
        self.setup_scrollable_content(
            enable_horizontal=False,  # Pas de scroll horizontal
            enable_vertical=True      # Scroll vertical activé
        )

        # Utiliser le layout scrollable
        layout = self.get_content_layout()
        # ... ajouter le contenu
```

### **Désactiver le scroll**

```python
class FenetreSimple(BasePyQt5Window):
    def __init__(self, parent=None):
        # Désactiver le scroll
        super().__init__(parent, title="Simple", enable_scroll=False)
```

## 📚 Exemples Concrets

### **Exemple 1 : FacturasPyQt5Window (Gestión de Facturas)**

```python
class FacturasPyQt5Window(BasePyQt5Window):
    def setup_ui(self):
        # Activer le scroll pour la liste de factures
        self.setup_scrollable_content(enable_horizontal=False, enable_vertical=True)
        main_layout = self.get_content_layout()

        # Ajouter le contenu (titre, boutons, table)
        main_layout.addWidget(title_label)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(facturas_table)
```

### **Exemple 2 : FacturaEditWindow (Nueva/Editar Factura)**

```python
class FacturaEditWindow(QDialog):
    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Widget conteneur scrollable
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.addWidget(info_section)
        content_layout.addWidget(client_section)
        content_layout.addWidget(products_section)
        content_layout.addWidget(totals_section)

        # Zone de scroll
        scroll_area = QScrollArea()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Boutons HORS du scroll (toujours visibles)
        main_layout.addLayout(buttons_layout)
```

## 🧪 Tests

### **Tests de comportement créés**

Fichier : `test/behaviour/test_scrollable_windows_behaviour.py`

**3 tests BDD** :
1. ✅ `test_factura_edit_window_is_scrollable` - Vérifie la présence de QScrollArea
2. ✅ `test_facturas_pyqt5_window_is_scrollable` - Vérifie l'activation du scroll
3. ✅ `test_factura_edit_window_buttons_outside_scroll` - Vérifie que les boutons sont toujours visibles

**Exécution** :
```bash
pytest test/behaviour/test_scrollable_windows_behaviour.py -v
```

## 🐛 Dépannage

### **Problèmes courants**

1. **Le scroll ne fonctionne pas**
   - Vérifier que `enable_scroll=True` dans le constructeur
   - S'assurer que `setup_scrollable_content()` est appelé dans `setup_ui()`
   - Pour QDialog, vérifier que QScrollArea est bien créé

2. **Scroll trop rapide/lent**
   - Modifier `scroll_step` dans `handle_wheel_event()` du mixin

3. **Conflits avec d'autres widgets**
   - Le filtre d'événements gère automatiquement la propagation
   - Les widgets natifs avec scroll (QTextEdit, etc.) gardent leur comportement

4. **Boutons non visibles**
   - S'assurer que les boutons sont ajoutés APRÈS le QScrollArea dans le layout principal
   - Ne pas les ajouter dans le `content_widget` scrollable

## 📈 Performance

- **Impact minimal** sur les performances
- **Filtrage d'événements optimisé**
- **Pas de polling** - événements uniquement
- **Compatible** avec les widgets PyQt5 existants

## 🔮 Améliorations futures

- Support du scroll horizontal pour les tableaux larges
- Configuration de la vitesse de scroll par utilisateur
- Animations de scroll plus avancées
- Support du scroll tactile sur tablettes

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
