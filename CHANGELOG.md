# 📝 Changelog - Facturación Fácil

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

## [1.2.0] - 2024-09-26

### ✨ Ajouté
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
