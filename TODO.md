# TODO - Facturación Fácil

<!-- ==================== SECTION NON EDITABLE ==================== -->
<!-- NE PAS MODIFIER CETTE SECTION - Préférences de développement -->

# Préférences de développement pour facturacion_facil
## Communication et workflow
- **Langue** : Communiquer exclusivement en français avec tutoiement
- **Validation obligatoire** : Aucune modification de code ou système sans confirmation préalable explicite de l'utilisateur. Toujours expliquer en détail le code. Présenter les modifications sous la forme d'un git diff

## Localisation
- **Textes en dur** : ne jamais harcoder des textes en dur dans le code
- **Langues obligatoires** : ES pour chaque nouveau texte

## Tests - RÈGLES STRICTES ⚠️
- **Intégration** : les tests doivent être intégrés comme test de régression ou d'integration dans la suite de test et non supprimés
- **Base de données de test - RÈGLES CRITIQUES** :
  - ❌ **INTERDIT ABSOLU** : Créer des bases de données temporaires ou de test
  - ❌ **INTERDIT ABSOLU** : Modifier le chemin de la base de données dans les tests
  - ❌ **INTERDIT ABSOLU** : Utiliser `tempfile`, `mkdtemp()` ou bases temporaires pour les tests
  - ❌ **INTERDIT ABSOLU** : Créer/supprimer/modifier des données dans les tests
  - ❌ **INTERDIT ABSOLU** : Modifier la structure de base même temporairement
  - ✅ **OBLIGATOIRE** : Utiliser UNIQUEMENT la base de données de production existante
  - ✅ **OBLIGATOIRE** : Tests en lecture seule ou avec données existantes
  - ✅ **AUTORISÉ** : Lire les données existantes pour validation d'interface
  - ✅ **AUTORISÉ** : Tester l'interface avec les données réelles (lecture seule)
- **Données de test** :
  - ✅ **AUTORISÉ** : Validation de l'affichage des données existantes
  - ✅ **AUTORISÉ** : Tests de structure d'interface (colonnes, champs, etc.)
  - ✅ **AUTORISÉ** : Tests de logique métier sans modification de données
- **Suite de tests** : lorsque tu fais un nouveau test dans le développement intègre-le à la suite de test
- **Respect des migrations** : TOUJOURS utiliser le système de migration officiel (database/migration_manager.py)
- **Aucune exception** : Ces règles s'appliquent même pour les tests "temporaires" ou "de développement"
- **Violation = INCIDENT GRAVE** : Toute violation de ces règles est considérée comme un incident grave
- **Documentation critique** : CONSULTER obligatoirement `REGLES_CRITIQUES_TESTS_BASE_DONNEES.md` avant tout développement de test

## Structure de données - CRITIQUE ⚠️
- **JAMAIS** modifier la structure de base de données sans sauvegarde préalable obligatoire
- **JAMAIS** supprimer ou perdre des données de production - INCIDENT GRAVE
- **Compatibilité** : quand la structure de la base de donnée change, il faut maintenir la compatibilité avec la structure antérieure
- **Migration** : si la structure de la base de donnée change, il faut migrer les données existantes de la base de production
- **Migrations progressives** : TOUJOURS utiliser des migrations progressives (ADD COLUMN) au lieu de DROP/CREATE
- **Tests de migration** : TOUJOURS tester les migrations sur une copie avant application en production
- **Vérification** : TOUJOURS vérifier que les données sont préservées après migration
- **Confirmation** : En cas de doute sur une modification de structure : DEMANDER CONFIRMATION EXPLICITE
- **Système de migration** : UTILISER OBLIGATOIREMENT le système de migration : database/migration_manager.py
- **Documentation** : CONSULTER la documentation : GUIDE_MIGRATIONS_BASE_DONNEES.md
- **Tests préalables** : TESTER avec le script : test_migration_system.py avant toute modification
- **Récupération** : En cas de perte de données : utiliser restore_and_migrate.py pour récupération

## Standards de code
- **Langue des commentaires** : Français pour la documentation, Espagnol pour l'interface utilisateur
- **Format des logs** : `YYYY-MM-DD HH:MM:SS - LEVEL - Message`
- **Encodage** : UTF-8 partout
- **Style de code** : PEP 8 pour Python, avec des exceptions pour la lisibilité

## Structure des fichiers
- **Base de données** : SQLite dans `facturacion.db`
- **Logs** : Répertoire `logs/` avec rotation automatique
- **PDF** : Répertoire configurable par l'utilisateur (fallback: `pdfs/`)
- **Images** : `assets/` pour les ressources, `data/logos/` pour les logos utilisateur
- **Tests** : Fichiers `test_*.py` à la racine pour les tests rapides

## Conventions de nommage
- **Variables** : `snake_case` en français/espagnol selon le contexte
- **Classes** : `PascalCase`
- **Méthodes** : `snake_case`
- **Constantes** : `UPPER_SNAKE_CASE`
- **Fichiers** : `snake_case.py`

## Workflow de développement
1. **Analyse** : Comprendre le problème avec `codebase-retrieval`
2. **Planification** : Utiliser les task management tools pour les tâches complexes
3. **Implémentation** : Modifications incrémentales avec tests
4. **Validation** : Tests automatisés + tests manuels
5. **Documentation** : Mise à jour des guides utilisateur

## Standards de test
- **Activation de l'environnement** : source activate_env.sh
- **Tests unitaires** : Un test par fonctionnalité
- **Tests d'intégration** : Validation end-to-end
- **Environnement de test** : `TESTING=1` pour désactiver l'ouverture de fichiers
- **Nettoyage** : Toujours nettoyer les fichiers temporaires

## Documentation
- **README** : Instructions d'installation et utilisation de base
- **Guides utilisateur** : Fichiers `GUIDE_*.md` détaillés
- **Documentation technique** : Fichiers `*_RESUME.md` pour les développeurs
- **Changelog** : Suivi des modifications importantes
- **TODO** : Fichier `TODO.md` pour les tâches à accomplir ne le modifie pas. il sert seulement pour que je communique avec toi

## Sécurité et bonnes pratiques
- **Validation des entrées** : Toujours valider les données utilisateur
- **Gestion d'erreurs** : Try-catch avec logs détaillés
- **Sauvegarde** : Backup automatique avant modifications critiques
- **Permissions** : Vérifier l'existence des répertoires avant écriture

<!-- ==================== FIN SECTION NON EDITABLE ==================== -->

---

# ✅ PROBLEMAS
