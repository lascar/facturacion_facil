# 🎨 Tests Interface Utilisateur

## 📋 **Description**
Tests des composants UI et interactions - validation de l'interface graphique et de l'expérience utilisateur.

## 📁 **Contenu du Répertoire**
```
ui/
├── README.md                           # Ce guide
├── test_productos.py                   # Tests interface produits
├── test_facturas_ui.py                 # Tests interface facturas
├── test_ui_components.py               # Tests composants UI
├── test_mini_images_facturas.py        # Tests mini images facturas
├── test_productos_buttons.py           # Tests boutons produits
├── test_scrollable_window.py           # Tests fenêtre scrollable
├── test_image_button_manual.py         # Tests bouton image manuel
├── test_stock_interface.py             # Tests interface stock
├── test_mousewheel_scroll.py           # Tests scroll molette
├── test_button_visibility.py           # Tests visibilité boutons
├── test_buttons_simple.py              # Tests boutons simples
├── test_window_management.py           # Tests gestion fenêtres
├── test_productos_window_simple.py     # Tests fenêtre produits simple
└── test_button_visibility_real.py      # Tests visibilité boutons réelle
```

## 🚀 **Exécution des Tests**

### **Tous les Tests UI**
```bash
# Depuis la racine du projet
./run_organized_tests.sh ui

# Avec pytest directement
pytest test/ui/

# Mode verbose (recommandé pour UI)
./run_organized_tests.sh ui -v

# Mode silencieux
./run_organized_tests.sh ui -q
```

### **Tests par Composant**
```bash
# Tests interface produits
./run_organized_tests.sh ui -k productos
pytest test/ui/test_productos.py
pytest test/ui/test_productos_buttons.py

# Tests interface facturas
./run_organized_tests.sh ui -k facturas
pytest test/ui/test_facturas_ui.py
pytest test/ui/test_mini_images_facturas.py

# Tests boutons et interactions
./run_organized_tests.sh ui -k button
pytest test/ui/test_button_visibility.py
pytest test/ui/test_buttons_simple.py

# Tests scroll et navigation
./run_organized_tests.sh ui -k scroll
pytest test/ui/test_scrollable_window.py
pytest test/ui/test_mousewheel_scroll.py

# Tests gestion fenêtres
pytest test/ui/test_window_management.py
```

### **Tests avec Interface Graphique**
```bash
# Tests avec affichage (nécessite DISPLAY)
DISPLAY=:0 ./run_organized_tests.sh ui -v

# Tests en mode headless (CI/CD)
xvfb-run ./run_organized_tests.sh ui

# Tests avec timeout (pour UI lente)
./run_organized_tests.sh ui --timeout=60
```

## 📊 **Statistiques**
- **Nombre de fichiers** : 14 fichiers de test
- **Tests estimés** : ~70 tests
- **Couverture** : Interfaces, composants, interactions
- **Temps d'exécution** : ~90-120 secondes

## 🎯 **Objectifs des Tests**

### **Tests de Composants**
- Création et initialisation des widgets
- Propriétés et configuration
- Événements et callbacks
- Destruction et nettoyage

### **Tests d'Interaction**
- Clics de boutons
- Saisie de texte
- Navigation entre fenêtres
- Scroll et défilement

### **Tests Visuels**
- Visibilité des éléments
- Positionnement et layout
- Images et icônes
- Responsive design

### **Tests de Workflow UI**
- Ouverture/fermeture de fenêtres
- Navigation entre écrans
- Validation de formulaires
- Messages d'erreur et confirmations

## 🔧 **Configuration**

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Interface graphique disponible
echo $DISPLAY

# Dépendances UI installées
pip install customtkinter pillow
```

### **Variables d'Environnement**
```bash
# Interface graphique
export DISPLAY=:0

# Mode test UI
export UI_TEST_MODE=1

# Timeout pour tests UI
export UI_TEST_TIMEOUT=60

# Mode headless pour CI
export HEADLESS_MODE=1
```

## 📋 **Types de Tests UI**

### **Tests de Création d'Interface**
```bash
# Tests de base des fenêtres
pytest test/ui/test_window_management.py

# Tests composants simples
pytest test/ui/test_buttons_simple.py

# Tests interface produits
pytest test/ui/test_productos_window_simple.py
```

### **Tests d'Interaction Avancée**
```bash
# Tests boutons avec logique
pytest test/ui/test_productos_buttons.py

# Tests images et sélection
pytest test/ui/test_image_button_manual.py
pytest test/ui/test_mini_images_facturas.py

# Tests scroll et navigation
pytest test/ui/test_mousewheel_scroll.py
```

### **Tests de Visibilité et Layout**
```bash
# Tests visibilité éléments
pytest test/ui/test_button_visibility.py
pytest test/ui/test_button_visibility_real.py

# Tests fenêtres scrollables
pytest test/ui/test_scrollable_window.py
```

## 🚀 **Exécution Spécialisée**

### **Tests avec Interface Graphique**
```bash
# Tests normaux (nécessite écran)
./run_organized_tests.sh ui -v -s

# Tests avec debug visuel
pytest test/ui/test_specific.py -s -vv

# Tests interactifs (attention: peuvent nécessiter interaction)
pytest test/ui/test_image_button_manual.py -s
```

### **Tests en Mode Headless**
```bash
# Pour CI/CD sans écran
xvfb-run -a ./run_organized_tests.sh ui

# Avec résolution spécifique
xvfb-run -s "-screen 0 1024x768x24" pytest test/ui/

# Tests headless uniquement
./run_organized_tests.sh ui -m "not interactive"
```

### **Tests de Performance UI**
```bash
# Temps de création des fenêtres
pytest test/ui/ --durations=10

# Tests lents uniquement
./run_organized_tests.sh ui -m slow

# Profiling UI si disponible
pytest test/ui/ --profile
```

## 🐛 **Dépannage**

### **Erreurs d'Interface Graphique**
```bash
# Pas d'affichage disponible
export DISPLAY=:0
# ou
xvfb-run pytest test/ui/

# Problèmes de permissions X11
xhost +local:

# Tkinter non disponible
sudo apt-get install python3-tk  # Ubuntu/Debian
```

### **Tests UI qui Échouent**
```bash
# Debug avec affichage des fenêtres
pytest test/ui/test_specific.py -s -vv

# Tests avec timeout étendu
pytest test/ui/ --timeout=120

# Skip tests interactifs
pytest test/ui/ -m "not manual"

# Logs détaillés UI
pytest test/ui/ --log-cli-level=DEBUG -s
```

### **Problèmes de Timing**
```bash
# Attentes explicites dans les tests
pytest test/ui/ --timeout=60

# Tests avec retry
pytest test/ui/ --reruns=2

# Mode lent pour debug
pytest test/ui/ --slow
```

## 📈 **Métriques de Qualité**

### **Couverture Attendue**
- **Composants UI** : >60%
- **Interactions** : >70%
- **Fenêtres principales** : >80%
- **Workflows UI** : >65%

### **Performance**
- **Temps total** : <180 secondes
- **Création fenêtre** : <2 secondes
- **Tests interactifs** : <10 secondes

## 🎯 **Scénarios de Test UI**

### **Workflow Produits**
1. Ouverture fenêtre produits
2. Création nouveau produit
3. Sélection image
4. Sauvegarde
5. Vérification affichage

### **Workflow Facturas**
1. Ouverture interface facturas
2. Création nouvelle factura
3. Ajout produits avec images
4. Calculs automatiques
5. Génération PDF

### **Tests de Navigation**
1. Menu principal
2. Navigation entre modules
3. Ouverture fenêtres modales
4. Fermeture et retour

## 🔄 **Maintenance**

### **Ajout de Nouveaux Tests UI**
```python
import pytest
import customtkinter as ctk
from ui.module_to_test import WindowToTest

class TestUIComponent:
    def setup_method(self):
        """Setup fenêtre de test"""
        self.root = ctk.CTk()
        self.root.withdraw()  # Cacher pendant les tests
    
    def test_window_creation(self):
        """Test création fenêtre"""
        window = WindowToTest(self.root)
        assert window is not None
    
    def teardown_method(self):
        """Nettoyage UI"""
        if hasattr(self, 'root'):
            self.root.destroy()
```

### **Bonnes Pratiques UI**
- Toujours nettoyer les fenêtres après tests
- Utiliser `withdraw()` pour cacher les fenêtres de test
- Tester en mode headless pour CI/CD
- Documenter les tests interactifs

### **Tests Interactifs**
```python
@pytest.mark.manual
def test_interactive_feature(self):
    """Test nécessitant interaction manuelle"""
    # Marquer comme manuel pour skip automatique
    pass
```

---

**⚠️ Note** : Les tests UI peuvent nécessiter un environnement graphique. Utilisez `xvfb-run` pour les tests automatisés.

**Pour plus d'informations, consultez le guide principal : `../README.md`**
