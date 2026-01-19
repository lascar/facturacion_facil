# 🏗️ Architecture de Facturación Fácil

## 📋 Vue d'ensemble

**Facturación Fácil** est une application de facturation développée en Python avec PyQt5, suivant une architecture modulaire et maintenable.

## 🎯 Stack Technique

### Framework GUI
- **PyQt5** : Framework GUI principal
- Interface native du système d'exploitation
- Widgets modernes et performants

### Base de données
- **SQLite** : Base de données embarquée
- Migrations automatiques
- Modèles optimisés

### Dépendances principales
- **Pillow** : Traitement d'images (logos, produits)
- **ReportLab** : Génération de PDFs professionnels
- **Matplotlib** : Génération de graphiques pour rapports
- **Pytest** : Framework de testing

## 📁 Structure du Projet

```
facturacion_facil/
├── main.py                      # Point d'entrée principal
├── requirements.txt             # Dépendances Python
├── pref_auggie.txt             # Préférences de développement
│
├── database/                    # Couche de données
│   ├── database.py             # Connexion et migrations
│   ├── models.py               # Modèles de données
│   ├── fixtures.py             # Données de test
│   ├── migration_manager.py    # Gestionnaire de migrations
│   └── test_database.py        # Base de test isolée
│
├── gui/                         # Abstraction GUI
│   ├── abstract_gui.py         # Interfaces abstraites
│   ├── gui_manager.py          # Gestionnaire de frameworks
│   └── abstract_components.py  # Composants réutilisables
│
├── ui/                          # Interfaces utilisateur (PyQt5)
│   ├── main_window_pyqt5.py    # Fenêtre principale
│   ├── productos_pyqt5.py      # Gestion des produits
│   ├── clientes_pyqt5.py       # Gestion des clients
│   ├── facturas_pyqt5.py       # Gestion des factures
│   ├── stock_pyqt5.py          # Gestion du stock
│   ├── organizacion_pyqt5.py   # Configuration entreprise
│   └── widgets/                # Widgets personnalisés
│
├── services/                    # Logique métier
│   ├── producto_service.py     # Service produits
│   ├── cliente_service.py      # Service clients
│   ├── factura_service.py      # Service factures
│   ├── stock_service.py        # Service stock
│   └── organizacion_service.py # Service organisation
│
├── utils/                       # Utilitaires
│   ├── pdf_generator.py        # Génération de PDFs
│   ├── excel_generator.py      # Génération Excel
│   ├── logger.py               # Système de logging
│   ├── translations.py         # Traductions (ES)
│   └── image_manager.py        # Gestion d'images
│
├── config/                      # Configuration
│   ├── config.py               # Gestionnaire de config
│   ├── config.json             # Configuration utilisateur
│   └── constants.py            # Constantes de l'app
│
├── test/                        # Tests automatisés
│   ├── base_test_with_fixtures.py  # Classe de base pour tests
│   ├── unit/                   # Tests unitaires
│   ├── integration/            # Tests d'intégration
│   ├── behaviour/              # Tests de comportement
│   └── conftest.py             # Configuration pytest
│
├── doc/                         # Documentation technique
├── docs/                        # Documentation utilisateur
├── data/                        # Données de configuration
├── logs/                        # Fichiers de log
├── facturas/                    # PDFs de factures générés
└── assets/                      # Ressources (images, icônes)
```

## 🔄 Flux de Données

### 1. Interface Utilisateur (UI)
- Fenêtres PyQt5 (`ui/*_pyqt5.py`)
- Widgets personnalisés (`ui/widgets/`)
- Gestion des événements et signaux PyQt5

### 2. Services (Logique Métier)
- Validation des données
- Règles métier
- Orchestration des opérations

### 3. Modèles (Database)
- Accès aux données
- ORM simplifié
- Migrations automatiques

### 4. Utilitaires
- Génération de documents (PDF, Excel)
- Logging et traçabilité
- Gestion des ressources

## 🧪 Système de Tests

### Principes
- **BDD** : Behaviour-Driven Development (tests first)
- **Fixtures** : Système de fixtures standardisées obligatoire
- **Isolation** : Base de test séparée de la production

### Classes de base
- `BaseTestWithFixtures` : Tests avec données standardisées
- `BaseBehaviourTest` : Tests de comportement PyQt5

### Données de test
- 3 produits standardisés
- 3 clients standardisés
- 3 factures standardisées
- Reset automatique entre chaque test

## 🔒 Sécurité et Bonnes Pratiques

### Protection de la Production
- ❌ **INTERDICTION ABSOLUE** : Utiliser la base de production pour les tests
- ✅ **OBLIGATOIRE** : Utiliser `database/test_database.py`
- ✅ **OBLIGATOIRE** : Vérifier que le chemin contient "test" ou "temp"

### Migrations de Base de Données
- ✅ Utiliser `migration_manager.py`
- ✅ Toujours créer un backup avant migration
- ✅ Tester sur copie avant production

### Code Pythonic
- ✅ Préférer les fonctions aux classes
- ✅ Context managers (`with`) obligatoires
- ✅ Annotations de type complètes
- ✅ EAFP (try/except) plutôt que LBYL
- ✅ Dataclasses pour structures de données
- ✅ Logging au lieu de print()

## 🌍 Internationalisation

- **Langue principale** : Espagnol (ES)
- **Fichier** : `utils/translations.py`
- **Règle** : Jamais de textes hardcodés dans le code

## 📊 Modèles de Données

### Tables principales
- **productos** : Produits avec images, prix, IVA
- **clientes** : Clients avec validations optionnelles
- **facturas** : En-têtes de factures
- **factura_items** : Lignes de détail des factures
- **stock** : Inventaire par produit
- **organizacion** : Configuration de l'entreprise

## 🚀 Démarrage Rapide

```bash
# 1. Activer l'environnement
source activate_env.sh

# 2. Lancer l'application
python main.py

# 3. Lancer les tests
pytest test/ -v
```

---

**Dernière mise à jour** : 2025-01-19  
**Version** : PyQt5 (stable)

