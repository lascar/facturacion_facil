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
- ✅ **Facturas** - Gestion des factures
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

```python
# Dans une fenêtre PyQt5
class MaFenetre(BasePyQt5Window):
    def setup_ui(self):
        # Activer le scroll pour cette fenêtre
        self.enable_window_scroll(enable_horizontal=False, enable_vertical=True)
        
        # Obtenir le layout de contenu (scrollable)
        main_layout = self.get_content_layout()
        
        # Ajouter le contenu normalement
        main_layout.addWidget(mon_widget)
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
        self.enable_window_scroll(
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

## 🐛 Dépannage

### **Problèmes courants**

1. **Le scroll ne fonctionne pas**
   - Vérifier que `enable_scroll=True` dans le constructeur
   - S'assurer que `enable_window_scroll()` est appelé dans `setup_ui()`

2. **Scroll trop rapide/lent**
   - Modifier `scroll_step` dans `handle_wheel_event()` du mixin

3. **Conflits avec d'autres widgets**
   - Le filtre d'événements gère automatiquement la propagation
   - Les widgets natifs avec scroll (QTextEdit, etc.) gardent leur comportement

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
