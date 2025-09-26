# 🧪 Guide Complet des Tests - Facturación Fácil

## 📁 **Structure des Tests**

```
test/
├── README.md                    # Ce guide
├── conftest.py                  # Configuration pytest globale
├── pytest.ini                  # Configuration pytest
├── __init__.py                  # Module Python
├── unit/                        # Tests unitaires
│   ├── test_database.py         # Tests base de données
│   ├── test_models.py           # Tests modèles de données
│   ├── test_factura_models.py   # Tests modèles factures
│   ├── test_validators.py       # Tests validateurs
│   ├── test_translations.py     # Tests traductions
│   ├── test_parametrized.py     # Tests paramétrés
│   ├── test_security.py         # Tests sécurité
│   ├── test_validate_form.py    # Tests validation formulaires
│   ├── test_validacion_facturas_opcional.py # Tests validation facturas
│   ├── test_ejemplos_validacion_facturas.py # Exemples validation
│   ├── test_stock_models.py     # Tests modèles stock
│   ├── test_logging_system.py   # Tests système de logs
│   └── test_pytest_markers.py   # Tests marqueurs pytest
├── integration/                 # Tests d'intégration
│   ├── test_integration.py      # Tests intégration générale
│   ├── test_facturas_integration.py # Tests intégration facturas
│   ├── test_pdf_download_feature.py # Tests fonctionnalité PDF
│   ├── test_visor_pdf_personalizado.py # Tests visor PDF
│   ├── test_facturas_validacion_integracion.py # Tests validation intégration
│   ├── test_stock_facturacion_integration.py # Tests stock-factura
│   ├── test_facturas_implementation.py # Tests implémentation facturas
│   ├── test_complete_functionality.py # Tests fonctionnalité complète
│   ├── test_organizacion_completo.py # Tests organisation complète
│   └── test_global_todas_correcciones.py # Tests corrections globales
├── ui/                          # Tests interface utilisateur
│   ├── test_productos.py        # Tests interface produits
│   ├── test_facturas_ui.py      # Tests interface facturas
│   ├── test_ui_components.py    # Tests composants UI
│   ├── test_mini_images_facturas.py # Tests mini images facturas
│   ├── test_productos_buttons.py # Tests boutons produits
│   ├── test_scrollable_window.py # Tests fenêtre scrollable
│   ├── test_image_button_manual.py # Tests bouton image manuel
│   ├── test_stock_interface.py  # Tests interface stock
│   ├── test_mousewheel_scroll.py # Tests scroll molette
│   ├── test_button_visibility.py # Tests visibilité boutons
│   ├── test_buttons_simple.py   # Tests boutons simples
│   ├── test_window_management.py # Tests gestion fenêtres
│   ├── test_productos_window_simple.py # Tests fenêtre produits simple
│   └── test_button_visibility_real.py # Tests visibilité boutons réelle
├── regression/                  # Tests de régression
│   ├── test_dialog_scroll_fix.py # Tests correction scroll
│   ├── test_image_selection.py  # Tests sélection images
│   ├── test_ui_improvements.py  # Tests améliorations UI
│   ├── test_stock_window_focus.py # Tests focus fenêtre stock
│   ├── test_filedialog_parent_fix.py # Tests correction parent dialog
│   ├── test_dialogo_logo_fix.py # Tests correction dialog logo
│   ├── test_image_fix.py        # Tests correction images
│   ├── test_filedialog_fix.py   # Tests correction filedialog
│   ├── test_messageboxes_fix.py # Tests correction messageboxes
│   ├── test_image_display_selection.py # Tests affichage sélection image
│   ├── test_image_selection_fix.py # Tests correction sélection image
│   ├── test_logo_image_fix.py   # Tests correction logo image
│   └── test_producto_selection_fix.py # Tests correction sélection produit
├── performance/                 # Tests de performance
│   └── test_performance.py      # Benchmarks et performance
├── property_based/              # Tests basés sur propriétés
│   └── test_property_based.py   # Tests avec Hypothesis
├── specific/                    # Tests de fonctionnalités spécifiques
│   ├── test_pdf_copyable_messages.py # Tests messages PDF copiables
│   ├── test_copyable_dialogs.py # Tests dialogs copiables
│   ├── test_nueva_numeracion.py # Tests nouvelle numérotation
│   ├── test_pdf_and_search_features.py # Tests PDF et recherche
│   ├── test_stock_with_copyable_messages.py # Tests stock messages
│   ├── test_pdf_message_flow.py # Tests flux messages PDF
│   ├── test_edicion_automatica_facturas.py # Tests édition auto facturas
│   └── test_improvements.py     # Tests améliorations
├── scripts/                     # Scripts de test
│   ├── run_tests_fixed.py       # Script tests corrigé
│   ├── run_working_tests.py     # Script tests fonctionnels
│   ├── run_tests.py             # Script tests principal
│   ├── run_productos_tests.py   # Script tests produits
│   ├── run_facturas_tests.py    # Script tests facturas
│   └── run_with_correct_python.sh # Script avec bon Python
└── demo/                        # Démonstrations
    ├── demo_pdf_download_feature.py # Démo fonctionnalité PDF
    ├── demo_visor_pdf_personalizado.py # Démo visor PDF
    ├── demo_mini_images_facturas.py # Démo mini images facturas
    └── demo_mousewheel_scroll.py # Démo scroll molette
```

## 🚀 **Exécution des Tests**

### **Prérequis**
```bash
# Activer l'environnement virtuel
source ../bin/activate

# Vérifier les dépendances
pip list | grep -E "(pytest|hypothesis|customtkinter)"
```

### **Scripts d'Exécution**
Utilisez les scripts fournis à la racine du projet :
```bash
# Script bash (recommandé)
./run_tests.sh [options]

# Script Python (cross-platform)
python3 run_tests_fixed.py [options]
```

## 📊 **Types de Tests et Commandes**

### **1. Tests Unitaires** 🔧
**Description** : Tests de composants individuels isolés
**Localisation** : `test/unit/`
**Nombre** : ~55 tests

```bash
# Tous les tests unitaires
./run_tests.sh test/unit/

# Tests spécifiques
./run_tests.sh test/unit/test_models.py
./run_tests.sh test/unit/test_database.py
./run_tests.sh test/unit/test_validators.py
./run_organized_tests.sh test/unit/test_validate_form.py

# Avec couverture
./run_tests.sh test/unit/ --cov=database --cov=utils
```

### **2. Tests d'Intégration** 🔗
**Description** : Tests d'interaction entre composants
**Localisation** : `test/integration/`
**Nombre** : ~35 tests

```bash
# Tous les tests d'intégration
./run_tests.sh test/integration/

# Tests fonctionnalité PDF
./run_tests.sh test/integration/test_pdf_download_feature.py
./run_tests.sh test/integration/test_visor_pdf_personalizado.py

# Tests intégration facturas
./run_tests.sh test/integration/test_facturas_integration.py
./run_organized_tests.sh test/integration/test_complete_functionality.py
```

### **3. Tests Interface Utilisateur** 🎨
**Description** : Tests des composants UI et interactions
**Localisation** : `test/ui/`
**Nombre** : ~70 tests

```bash
# Tous les tests UI
./run_tests.sh test/ui/

# Tests interface facturas
./run_tests.sh test/ui/test_facturas_ui.py
./run_tests.sh test/ui/test_ui_components.py
./run_organized_tests.sh test/ui/test_mini_images_facturas.py

# Tests interface produits
./run_tests.sh test/ui/test_productos.py
./run_organized_tests.sh test/ui/test_productos_buttons.py

# Tests boutons et interactions
./run_organized_tests.sh test/ui/test_button_visibility.py

# Mode verbose pour debug UI
./run_tests.sh test/ui/ -v -s
```

### **4. Tests de Régression** 🔄
**Description** : Tests pour éviter la réapparition de bugs
**Localisation** : `test/regression/`
**Nombre** : ~60 tests

```bash
# Tous les tests de régression
./run_tests.sh test/regression/

# Tests corrections spécifiques
./run_tests.sh test/regression/test_dialog_scroll_fix.py
./run_tests.sh test/regression/test_image_selection.py
./run_organized_tests.sh test/regression/test_filedialog_parent_fix.py
./run_organized_tests.sh test/regression/test_image_fix.py
```

### **5. Tests de Performance** ⚡
**Description** : Benchmarks et tests de performance
**Localisation** : `test/performance/`
**Nombre** : ~13 tests

```bash
# Tests de performance
./run_tests.sh test/performance/

# Avec rapport détaillé
./run_tests.sh test/performance/ -v --benchmark-only

# Sauvegarde des benchmarks
./run_tests.sh test/performance/ --benchmark-save=baseline
```

### **6. Tests Basés sur Propriétés** 🎲
**Description** : Tests avec génération automatique de données (Hypothesis)
**Localisation** : `test/property_based/`
**Nombre** : ~13 tests

```bash
# Tests property-based
./run_tests.sh test/property_based/

# Avec plus d'exemples
./run_tests.sh test/property_based/ --hypothesis-show-statistics

# Mode verbose pour voir les exemples générés
./run_tests.sh test/property_based/ -v -s
```

### **7. Tests de Fonctionnalités Spécifiques** 🎯
**Description** : Tests de fonctionnalités particulières et corrections
**Localisation** : `test/specific/`
**Nombre** : ~25 tests

```bash
# Tous les tests spécifiques
./run_organized_tests.sh test/specific/

# Tests PDF et messages
./run_organized_tests.sh test/specific/test_pdf_copyable_messages.py
./run_organized_tests.sh test/specific/test_copyable_dialogs.py

# Tests nouvelles fonctionnalités
./run_organized_tests.sh test/specific/test_nueva_numeracion.py
./run_organized_tests.sh test/specific/test_edicion_automatica_facturas.py
```

### **8. Scripts de Test** 📜
**Description** : Scripts d'exécution et utilitaires de test
**Localisation** : `test/scripts/`

```bash
# Scripts disponibles
ls test/scripts/

# Exécuter un script spécifique
python3 test/scripts/run_tests_fixed.py
python3 test/scripts/run_productos_tests.py
```

### **9. Démonstrations** 🎯
**Description** : Scripts de démonstration des fonctionnalités
**Localisation** : `test/demo/`

```bash
# Démonstration fonctionnalité PDF
python3 test/demo/demo_pdf_download_feature.py

# Démonstration visor PDF personnalisé
python3 test/demo/demo_visor_pdf_personalizado.py

# Démonstration mini images facturas
python3 test/demo/demo_mini_images_facturas.py

# Démonstration scroll molette
python3 test/demo/demo_mousewheel_scroll.py
```

## 🎯 **Commandes Courantes**

### **Exécution Globale**
```bash
# Tous les tests
./run_tests.sh test/

# Tests rapides (sans performance)
./run_tests.sh test/ --ignore=test/performance/

# Tests avec couverture complète
./run_tests.sh test/ --cov=. --cov-report=html
```

### **Exécution Sélective**
```bash
# Tests par marqueur
./run_tests.sh test/ -m "unit"
./run_tests.sh test/ -m "integration"
./run_tests.sh test/ -m "ui"

# Tests par pattern
./run_tests.sh test/ -k "pdf"
./run_tests.sh test/ -k "factura"
./run_tests.sh test/ -k "ui"

# Tests modifiés récemment
./run_tests.sh test/ --lf  # last failed
./run_tests.sh test/ --ff  # failed first
```

### **Options Utiles**
```bash
# Mode verbose
./run_tests.sh test/ -v

# Arrêt au premier échec
./run_tests.sh test/ -x

# Parallélisation
./run_tests.sh test/ -n auto

# Sortie détaillée
./run_tests.sh test/ --tb=long

# Mode silencieux
./run_tests.sh test/ -q
```

## 📈 **Rapports et Couverture**

### **Rapport de Couverture**
```bash
# Générer rapport HTML
./run_tests.sh test/ --cov=. --cov-report=html

# Ouvrir le rapport
xdg-open htmlcov/index.html  # Linux
open htmlcov/index.html      # macOS
start htmlcov/index.html     # Windows
```

### **Rapport de Performance**
```bash
# Benchmarks avec comparaison
./run_tests.sh test/performance/ --benchmark-compare

# Graphiques de performance
./run_tests.sh test/performance/ --benchmark-histogram
```

## 🔧 **Configuration et Personnalisation**

### **Variables d'Environnement**
```bash
# Mode debug
export PYTEST_DEBUG=1

# Niveau de log
export LOG_LEVEL=DEBUG

# Base de données de test
export TEST_DATABASE=":memory:"
```

### **Configuration pytest.ini**
Le fichier `pytest.ini` à la racine configure :
- Marqueurs de tests
- Options par défaut
- Chemins de recherche
- Plugins activés

### **Fixtures Personnalisées**
Le fichier `conftest.py` fournit :
- Fixtures de base de données
- Fixtures d'interface utilisateur
- Configuration des tests
- Utilitaires de test

## 🐛 **Dépannage**

### **Erreurs Courantes**
```bash
# Import errors
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Problèmes d'affichage UI
export DISPLAY=:0  # Linux
xvfb-run ./run_tests.sh test/ui/  # Mode headless

# Permissions
chmod +x run_tests.sh
```

### **Tests Lents**
```bash
# Identifier les tests lents
./run_tests.sh test/ --durations=10

# Exclure les tests lents
./run_tests.sh test/ -m "not slow"
```

## 📊 **Statistiques Actuelles**

- **Total** : ~400+ tests
- **Unitaires** : ~55 tests
- **Intégration** : ~35 tests
- **UI** : ~70 tests
- **Régression** : ~60 tests
- **Performance** : ~13 tests
- **Property-based** : ~13 tests
- **Spécifiques** : ~25 tests
- **Scripts** : 6 scripts
- **Démonstrations** : 4 démos
- **Couverture** : ~26%
- **Temps d'exécution** : ~3-4 minutes

## 🎯 **Bonnes Pratiques**

1. **Avant commit** : `./run_tests.sh test/ --lf`
2. **Développement** : `./run_tests.sh test/unit/ -x`
3. **CI/CD** : `./run_tests.sh test/ --cov=. --tb=short`
4. **Debug** : `./run_tests.sh test/specific_test.py -v -s`
5. **Performance** : `./run_tests.sh test/performance/ --benchmark-only`

## 📚 **Documentation Détaillée**

Chaque catégorie de tests dispose de sa propre documentation complète dans son répertoire.

### **📖 Documentation par Répertoire**
- **`unit/README.md`** : Tests unitaires (300 lignes)
- **`integration/README.md`** : Tests d'intégration (300 lignes)
- **`ui/README.md`** : Tests interface utilisateur (300 lignes)
- **`regression/README.md`** : Tests de régression (300 lignes)
- **`performance/README.md`** : Tests de performance (300 lignes)
- **`property_based/README.md`** : Tests property-based (300 lignes)
- **`specific/README.md`** : Tests spécifiques (300 lignes)
- **`scripts/README.md`** : Scripts de test (300 lignes)
- **`demo/README.md`** : Démonstrations (300 lignes)

### **📋 Guides Spécialisés**
- **`MIGRATION_GUIDE.md`** : Guide de migration complète
- **`DOCUMENTATION_COMPLETE.md`** : Résumé de toute la documentation

**Total : ~2700 lignes de documentation détaillée !**

---

**🧪 Cette structure de tests organisée facilite le développement, la maintenance et l'évolution du projet !**

**Pour plus d'aide** : Consultez la documentation dans `doc/technical/TESTING_GUIDE.md`
