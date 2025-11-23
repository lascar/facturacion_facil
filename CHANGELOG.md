# 📝 Changelog - Facturación Fácil

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

## [2.0.0] - 2024-11-23

### ✨ Ajouté
- **🧪 Suite de tests complète** : 243+ tests automatizados avec coberture complète
- **🔧 Herramientas de maintenance** : Scripts de nettoyage et diagnostic
- **📊 Documentation mise à jour** : État actuel et guides utilisateur
- **🛠️ Outils de développement** : Scripts d'activation et validation
- **🎯 Tests de régression** : Validation continue des fonctionnalités

### 🔧 Amélioré
- **📚 README complet** : Documentation restructurée et mise à jour
- **🚀 Guide de démarrage rapide** : Instructions simplifiées pour nouveaux utilisateurs
- **📋 État du projet** : Documentation claire du statut actuel
- **🔍 Système de validation** : Tests automatisés pour toutes les fonctionnalités
- **🧹 Nettoyage de données** : Outils pour réinitialiser la base de données

### 🐛 Corrigé
- **✅ Tests ProductoFacturaDialog** : Tous les tests passent maintenant (9/9)
- **🔧 Signature des constructeurs** : Compatibilité avec les tests
- **📝 Validation des formulaires** : Logique de validation corrigée
- **🎨 Widgets simulés** : Mocks appropriés pour les tests
- **💾 Gestion de base de données** : Nettoyage et réinitialisation fiables

### 📚 Documentation
- **📊 ESTADO_ACTUAL_2024.md** : État complet du projet
- **🚀 GUIA_INICIO_RAPIDO.md** : Guide de démarrage rapide
- **📋 README.md mis à jour** : Documentation principale restructurée
- **🔧 Scripts documentés** : Guides d'utilisation des outils

## [1.2.0] - 2024-09-26

### ✨ Ajouté
- **🚀 Optimisation de performance majeure** : Amélioration spectaculaire des performances
  - Modèles optimisés (OptimizedFactura, OptimizedStock, OptimizedProducto)
  - Interfaces virtualisées avec pagination et chargement paresseux
  - Système de cache intelligent avec TTL configurable
  - Index de base de données automatiques
  - Monitor de performance intégré
  - Résultats: 25-120x plus rapide, 99% moins de requêtes
  - Script d'application automatique (utils/apply_performance_optimizations.py)

- **🧹 Solution PDFs en tests** : Les PDFs ne s'ouvrent plus automatiquement pendant les tests
  - Détection automatique du mode test (variables PYTEST_RUNNING, DISABLE_PDF_OPEN)
  - Génération PDF normale mais sans ouverture en mode test
  - Script de nettoyage des PDFs de test (utils/cleanup_test_pdfs.py)
  - Tests 20% plus rapides (pas d'attente d'ouverture PDF)
  - 71 PDFs de test nettoyés (11.6 MB libérés)
  - Configuration automatique dans conftest.py

- **🖼️ Logo dans les PDFs** : Affichage automatique du logo de l'entreprise en haut à gauche des factures PDF
  - Redimensionnement automatique proportionnel (max 3cm x 3cm)
  - Support de tous les formats d'image PIL (PNG, JPG, GIF, BMP)
  - Gestion d'erreurs robuste (fonctionne avec ou sans logo)
  - Configuration simple via les paramètres d'organisation
  - Tests complets (8 tests unitaires, intégration et bout en bout)
  - Documentation complète avec exemples

### 🔧 Amélioré
- **Générateur PDF** : Méthode `add_header()` améliorée pour inclure le logo
- **Gestion d'images** : Nouvelle méthode `create_logo_image()` avec redimensionnement intelligent
- **Tests** : Suite de tests étendue pour la fonctionnalité logo
- **Documentation** : Ajout de `docs/features/PDF_LOGO_FEATURE_SUMMARY.md`

### 🐛 Corrigé
- **Tests bloquants** : Résolution du deadlock dans `TestDatabaseManager.cleanup_all_test_resources()`
- **Warnings pytest** : Suppression des warnings de collection sur `TestDatabaseManager`
- **Warnings CustomTkinter** : Filtrage des warnings d'images non-CTkImage
- **Tests d'isolation** : Correction des tests d'isolation de base de données concurrents

### 📚 Documentation
- Ajout de documentation complète pour la fonctionnalité logo
- Mise à jour du README principal
- Mise à jour de MEJORAS_IMPLEMENTADAS.md
- Création de ce CHANGELOG.md

## [1.1.0] - 2024-09-XX

### ✨ Ajouté
- **Messages copiables** : Possibilité de copier les messages d'erreur et d'information
- **Numérotation automatique** : Système de numérotation intelligent des factures
- **Intégration stock-facturation** : Gestion complète du stock avec la facturation
- **Recherche avancée** : Recherche dans les produits et factures

### 🔧 Amélioré
- **Interface utilisateur** : Amélioration de l'interface des produits
- **Gestion d'images** : Display amélioré des images de produits
- **Configuration** : Système de configuration de répertoires

### 🐛 Corrigé
- **Gestion des fenêtres** : Corrections diverses de l'interface
- **Sélection d'images** : Amélioration de la sélection d'images
- **Tests** : Stabilisation de la suite de tests

## [1.0.0] - 2024-09-XX

### ✨ Ajouté
- **Version initiale** : Application de facturation complète
- **Gestion des produits** : CRUD complet des produits
- **Gestion des factures** : Création et gestion des factures
- **Gestion du stock** : Suivi des stocks
- **Génération PDF** : Export des factures en PDF
- **Base de données** : Système de base de données SQLite
- **Interface graphique** : Interface utilisateur avec CustomTkinter

---

## 📋 Types de changements

- **✨ Ajouté** pour les nouvelles fonctionnalités
- **🔧 Amélioré** pour les changements dans les fonctionnalités existantes
- **🐛 Corrigé** pour les corrections de bugs
- **🗑️ Supprimé** pour les fonctionnalités supprimées
- **🔒 Sécurité** pour les corrections de vulnérabilités
- **📚 Documentation** pour les changements de documentation uniquement

## 🔗 Liens

- [Documentation complète](docs/README.md)
- [Guide d'installation](docs/ENVIRONMENT_SETUP.md)
- [Architecture du projet](docs/ORGANISATION_PROJET.md)
