# Tests de Comportement (Behaviour Tests) - PyQt5

## 🎯 Objectif

Les tests de comportement simulent l'interaction utilisateur réelle avec l'interface graphique PyQt5 de Facturación Fácil. Ils utilisent **QTest** et **pytest-qt** pour automatiser les actions utilisateur et vérifier que l'application fonctionne correctement du point de vue de l'utilisateur final.

## 🛠️ Technologies Utilisées

- **QTest** : Framework de test officiel de Qt pour l'automatisation GUI
- **pytest-qt** : Plugin pytest pour les applications Qt
- **PyQt5** : Framework GUI de l'application
- **pytest** : Framework de test
- **Base de données de test isolée** : Respect des préférences de sécurité

## ✅ **SUITE COMPLÈTE DE TESTS IMPLÉMENTÉE**

### 🎯 **Remplacement de Selenium par QTest**

**Problème résolu** : Selenium ne peut pas tester les applications PyQt5 car il est conçu pour les applications web.

**Solution adoptée** : **QTest** - le framework de test officiel de Qt pour l'automatisation GUI.

### 📁 **TESTS COMPLETS SELON FACTURACION_FACIL.TXT**

**Mission accomplie** : Suite complète de tests de comportement basée sur les spécifications exactes de `facturacion_facil.txt`.

#### **Tests Complets Ajoutés**
- `test_complete_application_behaviour.py` - **Tests fenêtres principales selon spécifications**
- `test_autocomplete_widgets_behaviour.py` - **Tests widgets autocomplétion**
- `test_dialogs_behaviour.py` - **Tests dialogues modaux**
- `test_stock_window_behaviour.py` - **Tests gestion stock**

### 🛠️ **Architecture de Test Mise en Place**

1. **Tests de Base** (`test_qtest_basic.py`) ✅
   - Tests de clic de bouton avec `QTest.mouseClick()`
   - Tests de saisie de texte avec `QTest.keyClicks()`
   - Tests de séquences de touches avec modificateurs
   - Tests de propriétés de widgets
   - Tests de timing et traitement d'événements

2. **Tests de Base de Données** (`test_database_behaviour.py`) ✅
   - Tests CRUD pour clients, produits, factures
   - Tests de recherche et filtrage
   - Tests de workflow de création de factures
   - Isolation complète avec bases de test

3. **Tests d'Interface Avancés** (`test_clientes_behaviour.py`, `test_facturas_behaviour.py`) ✅
   - Tests de workflow complets avec QTest
   - Tests d'autocomplétion clients/produits
   - Tests de formulaires et validation
   - Tests de génération PDF

4. **Utilitaires d'Automatisation** (`utils/pyqt5_automation.py`) ✅
   - Classe `PyQt5Automation` avec méthodes spécialisées
   - Méthodes pour ouvrir des dialogues
   - Méthodes pour remplir des formulaires
   - Méthodes pour vérifier des tableaux

### 🚀 **Scripts d'Exécution**

- `run_pyqt5_behaviour_tests.sh` : Script principal avec rapports détaillés
- Support des modes : simple, database, gui, all
- Génération de rapports HTML/XML
- Captures d'écran automatiques en cas d'erreur

## 📋 Scénarios de Test Couverts

### 🏠 Fenêtre Principale (MainWindow)
- ✅ Lancement de l'application
- ✅ Vérification des boutons principaux
- ✅ Navigation vers les différentes fenêtres

### 🧾 Gestion des Facturas
- ✅ Création d'une nouvelle facture
- ✅ Sélection de client avec autocomplétion
- ✅ Ajout de produits à la facture
- ✅ Calcul automatique des totaux
- ✅ Sauvegarde de la facture
- ✅ Génération de PDF

### 👥 Gestion des Clients
- ✅ Création d'un nouveau client
- ✅ Modification des données client
- ✅ Suppression d'un client
- ✅ Recherche et filtrage

### 📦 Gestion des Produits
- ✅ Création d'un nouveau produit
- ✅ Modification des prix et stock
- ✅ Gestion des catégories
- ✅ Synchronisation avec les factures

### 🏢 Configuration Organización
- ✅ Configuration des données d'entreprise
- ✅ Gestion du logo
- ✅ Configuration des répertoires
- ✅ États de factures personnalisés

### 📊 Gestion du Stock
- ✅ Visualisation du stock
- ✅ Ajustement des quantités
- ✅ Alertes de stock bas

## 🚀 Exécution des Tests

```bash
# Activer l'environnement
source ./activate_env.sh

# Lancer tous les tests de comportement
python -m pytest test/behaviour/ -v

# Lancer un test spécifique
python -m pytest test/behaviour/test_facturas_behaviour.py -v

# Lancer avec mode headless (sans interface graphique)
python -m pytest test/behaviour/ -v --headless

# Lancer avec capture d'écran en cas d'échec
python -m pytest test/behaviour/ -v --screenshots
```

## 🔒 Sécurité et Isolation

- **Base de données de test isolée** : Chaque test utilise une base temporaire
- **Nettoyage automatique** : Suppression des données de test après exécution
- **Aucun impact sur la production** : Tests complètement isolés
- **Respect des préférences utilisateur** : Conformité avec pref_auggie.txt

## 📁 Structure des Fichiers

```
test/behaviour/
├── __init__.py                    # Module principal
├── README.md                      # Documentation
├── conftest.py                    # Configuration pytest et fixtures
├── base_behaviour_test.py         # Classe de base pour tous les tests
├── test_main_window_behaviour.py  # Tests de la fenêtre principale
├── test_facturas_behaviour.py     # Tests de gestion des factures
├── test_clientes_behaviour.py     # Tests de gestion des clients
├── test_productos_behaviour.py    # Tests de gestion des produits
├── test_organizacion_behaviour.py # Tests de configuration
├── test_stock_behaviour.py        # Tests de gestion du stock
└── utils/
    ├── selenium_helpers.py        # Utilitaires Selenium
    ├── pyqt5_automation.py        # Automatisation PyQt5
    └── test_data_factory.py       # Génération de données de test
```

## 🎨 Exemple de Test

```python
def test_crear_factura_completa(self):
    """Test complet de création d'une facture"""
    
    # 1. Ouvrir la fenêtre facturas
    self.main_window.click_facturas_button()
    
    # 2. Créer une nouvelle facture
    self.facturas_window.click_nueva_factura()
    
    # 3. Sélectionner un client
    self.facturas_window.select_client("Cliente Test")
    
    # 4. Ajouter des produits
    self.facturas_window.add_product("Producto Test", cantidad=2)
    
    # 5. Vérifier les totaux
    assert self.facturas_window.get_total() > 0
    
    # 6. Sauvegarder
    self.facturas_window.save_factura()
    
    # 7. Vérifier la sauvegarde
    assert self.facturas_window.is_factura_saved()
```

## 🐛 Débogage

- **Logs détaillés** : Chaque action est loggée
- **Captures d'écran** : Sauvegarde automatique en cas d'erreur
- **Mode pas-à-pas** : Possibilité de ralentir l'exécution
- **Inspection des éléments** : Outils pour identifier les composants PyQt5
