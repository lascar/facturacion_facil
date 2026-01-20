> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**

---

# TODO - Facturación Fácil

<!-- ==================== SECTION NON EDITABLE ==================== -->
<!-- NE PAS MODIFIER CETTE SECTION - Préférences de développement -->

# Instructions de développement pour facturacion_facil

## 🗣️ Communication
- Communique TOUJOURS en français avec tutoiement
- Explique en détail chaque modification de code
- Présente les changements sous forme de git diff
- Demande TOUJOURS une confirmation explicite avant toute modification de code ou système

## 🌍 Localisation et Internationalisation
- INTERDICTION : Ne jamais hardcoder de textes en dur dans le code
- OBLIGATOIRE : Tous les nouveaux textes doivent être en espagnol (ES)

## 🧪 Tests - PROTECTION PRODUCTION CRITIQUE ⚠️

### Règles de sécurité absolues
- ❌ INTERDICTION ABSOLUE : Utiliser la base de données de production pour les tests (INCIDENT GRAVE)
- ❌ INTERDICTION ABSOLUE : Modifier, créer ou supprimer des données en production via les tests
- ✅ OBLIGATOIRE : Utiliser `database/test_database.py` pour créer une base de test isolée
- ✅ OBLIGATOIRE : Vérifier que le chemin de la base contient "test" ou "temp" avant tout test
- ✅ OBLIGATOIRE : Nettoyer automatiquement les bases de test après utilisation
- ✅ OBLIGATOIRE : Préfixer tous les noms de test par "Test" ou "TEST"
- ⚠️ CRITIQUE : Si des données de test apparaissent en production, les supprimer IMMÉDIATEMENT
- ✅ OBLIGATOIRE : Intégrer chaque nouveau test dans la suite de test existante
- ✅ OBLIGATOIRE : Travailler en BDD (Behaviour-Driven Development) - tests first

### Système de Fixtures - OBLIGATOIRE ⚠️
- ✅ UTILISATION OBLIGATOIRE : Tous les tests DOIVENT utiliser le système de fixtures standardisées
- ✅ CLASSE DE BASE OBLIGATOIRE : Hériter de `BaseTestWithFixtures` pour tous les nouveaux tests
- ✅ DONNÉES STANDARDISÉES : Utiliser les 3 produits, 3 clients, 3 factures des fixtures
- ✅ RESET AUTOMATIQUE : `setUp()` remet automatiquement à l'état initial entre chaque test
- ❌ INTERDICTION : Créer des données de test manuellement - utiliser les fixtures
- 📖 GUIDE OBLIGATOIRE : Consulter `GUIDE_FIXTURES.md` avant de créer des tests
- 🎯 DÉMONSTRATION : Lancer `test_fixtures_demo.py` pour comprendre le fonctionnement
- 📁 STRUCTURE OBLIGATOIRE : `test/base_test_with_fixtures.py` comme classe parent
- 🛠️ MÉTHODES UTILITAIRES : Utiliser `get_test_products()`, `get_test_clients()`, `get_test_invoices()`
- ✨ ÉTAT INITIAL GARANTI : Chaque test commence avec des données propres et prévisibles

### Workflow de Développement avec Fixtures - OBLIGATOIRE ⚠️
1. **ÉTAPE 1** : Créer d'abord les tests de comportement avec `BaseTestWithFixtures`
2. **ÉTAPE 2** : Utiliser les fixtures standardisées (3 produits, 3 clients, 3 factures)
3. **ÉTAPE 3** : Vérifier que `setUp()` remet bien à l'état initial
4. **ÉTAPE 4** : Tester les modifications sur les données des fixtures
5. **ÉTAPE 5** : Valider que le reset fonctionne entre les tests
6. **EXEMPLE** : Suivre le modèle de `test/test_stock_with_fixtures.py`
7. **DÉMONSTRATION** : Lancer `test_fixtures_demo.py` avant tout nouveau développement
8. **INTÉGRATION** : Ajouter tous les nouveaux tests à la suite de test existante
9. **DOCUMENTATION** : Mettre à jour `GUIDE_FIXTURES.md` si nouvelles fonctionnalités

### Tests de Comportement PyQt5 - FERMETURE AUTOMATIQUE ⚠️
- ✅ PROBLÈME RÉSOLU : Les boîtes de dialogue "Êtes-vous sûr de fermer?" ne bloquent plus les tests
- ✅ MODE TEST AUTOMATIQUE : Variable `PYTEST_RUNNING=1` activée automatiquement pendant les tests
- ✅ FERMETURE SANS CONFIRMATION : `closeEvent()` détecte le mode test et ferme sans demander
- ✅ PATCH QMESSAGEBOX : `QMessageBox.question()` retourne automatiquement Yes en mode test
- ✅ CLASSE DE BASE OBLIGATOIRE : Hériter de `BaseBehaviourTest` pour fermeture automatique
- ✅ TEARDOWN AUTOMATIQUE : `teardown_method()` ferme toutes les fenêtres après chaque test
- 🚀 COMMANDE TESTS : `pytest test/behaviour/ -v -s` (sans blocage garanti)
- ✅ VALIDATION OBLIGATOIRE : Lancer `test_no_confirmation_dialogs.py` pour vérifier
- 📖 GUIDE OBLIGATOIRE : Consulter `INSTRUCTIONS_TESTS_BEHAVIOUR_SANS_BLOCAGE.md`
- ❌ INTERDICTION : Ne jamais appeler manuellement `window.close()` dans les tests

### Protocole de sécurité des données - CRITIQUE ⚠️
- ✅ AVANT tout test : Vérifier que `database.db_path` contient "test" ou "temp"
- ✅ AVANT toute modification : Confirmer explicitement avec l'utilisateur
- ✅ APRÈS tout test : Vérifier qu'aucune donnée de test n'est restée en production
- ⚠️ EN CAS D'ERREUR : Nettoyer immédiatement et informer l'utilisateur
- ✅ UTILISER EXCLUSIVEMENT : `get_test_database()` pour tous les tests
- ❌ INTERDICTION : Importer directement `database.db` dans les tests

## 🗄️ Structure de données - CRITIQUE ⚠️

### Règles de sécurité des données
- ❌ JAMAIS modifier la structure de base de données sans sauvegarde préalable obligatoire
- ❌ JAMAIS supprimer ou perdre des données de production (INCIDENT GRAVE)
- ❌ JAMAIS utiliser la base de production pour tester des modifications
- ✅ UTILISER : `database/test_database.py` pour les tests de modifications

### Migrations de base de données
- ✅ OBLIGATOIRE : Si la structure change, créer/modifier `migration.bat` (Windows) et `migration.sh` (Linux)
- ✅ PRIVILÉGIER : Migrations progressives (`ADD COLUMN`) au lieu de `DROP/CREATE`
- ✅ TOUJOURS : Tester les migrations sur une copie avant application en production
- ✅ TOUJOURS : Vérifier que les données sont préservées après migration
- ⚠️ EN CAS DE DOUTE : DEMANDER CONFIRMATION EXPLICITE
- ✅ UTILISER OBLIGATOIREMENT : Le système de migration `database/migration_manager.py`
- 📖 CONSULTER : La documentation `GUIDE_MIGRATIONS_BASE_DONNEES.md`
- 🧪 TESTER : Avec le script `test_migration_system.py` avant toute modification
- 🔄 RÉCUPÉRATION : Utiliser `restore_and_migrate.py` en cas de perte de données

## 🛠️ Environnement de développement

### Configuration Python
- **Activation environnement** : `source ./activate_env.sh`
- **Python** : `/home/pascal/.pyenv/shims/python`
- **Pytest** : Installé dans l'environnement

### Rappel méthodologie
- Travailler en BDD (Behaviour-Driven Development)
- Utiliser UNIQUEMENT la base de test
- Intégrer tous les tests dans la suite de test existante
<!-- ==================== FIN SECTION NON EDITABLE ==================== -->

---

# ✅ PROBLEMAS
le fichier 'Productos Tienda.xlsx' a 6 colonnes, je voudrais que tu fasses un migracion.bat (pour windows) et un migracion.sh (pour linux) qui mette dans la table 'products_shop' avec les 6 colonnes du fichier 'Productos Tienda.xlsx' dans la base de données 'database.db'
tu dois adapter les données de 'Productos Tienda.xlsx' à la table, le nom c'est la categorie et la reférencia c'est le nom du produit, la 2eme colonne c'est la talla

---

> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**

