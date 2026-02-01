#!/bin/bash

# 🧪 Script d'Exécution des Tests Organisés - Facturación Fácil
# Usage: ./run_organized_tests.sh [type] [options]

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="../bin"
TEST_DIR="test"
COVERAGE_DIR="htmlcov"
PRODUCTION_DB="base_de_datos/facturacion.db"
BACKUP_DIR="base_de_datos/backups"
BACKUP_FILE=""

# Configuration et logos
PRODUCTION_CONFIG="config/config.json"
PRODUCTION_LOGO_DIR="logo"
CONFIG_BACKUP_FILE=""
LOGO_BACKUP_DIR=""

# Fonction d'aide
show_help() {
    echo -e "${BLUE}🧪 Script d'Exécution des Tests Organisés${NC}"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./run_organized_tests.sh [type] [options]"
    echo ""
    echo -e "${YELLOW}Types de tests:${NC}"
    echo -e "  ${GREEN}all${NC}              Tous les tests"
    echo -e "  ${GREEN}pyqt5${NC}           🚀 Tests PyQt5 (recommandé)"
    echo -e "  ${GREEN}unit${NC}             Tests unitaires (test/unit/)"
    echo -e "  ${GREEN}integration${NC}      Tests d'intégration (test/integration/)"
    echo -e "  ${GREEN}ui${NC}               Tests interface utilisateur (test/ui/)"
    echo -e "  ${GREEN}regression${NC}       Tests de régression (test/regression/)"
    echo -e "  ${GREEN}performance${NC}      Tests de performance (test/performance/)"
    echo -e "  ${GREEN}property${NC}         Tests property-based (test/property_based/)"
    echo -e "  ${GREEN}specific${NC}         Tests fonctionnalités spécifiques (test/specific/)"
    echo -e "  ${GREEN}scripts${NC}          Scripts de test (test/scripts/)"
    echo -e "  ${GREEN}demo${NC}             Démonstrations (test/demo/)"
    echo -e "  ${GREEN}quick${NC}            Tests rapides (unit + integration)"
    echo -e "  ${GREEN}ci${NC}               Tests pour CI/CD (sans performance)"
    echo ""
    echo -e "${YELLOW}Options courantes:${NC}"
    echo "  -v, --verbose        Mode verbose"
    echo "  -x, --exitfirst      Arrêt au premier échec"
    echo "  -q, --quiet          Mode silencieux"
    echo "  --cov                Avec couverture de code"
    echo "  --cov-html           Avec rapport HTML de couverture"
    echo "  --lf                 Derniers tests échoués"
    echo "  --ff                 Tests échoués en premier"
    echo "  -k PATTERN           Filtrer par pattern"
    echo "  -m MARKER            Filtrer par marqueur"
    echo "  --tb=short           Format de traceback"
    echo "  -n auto              Parallélisation automatique"
    echo ""
    echo -e "${YELLOW}Exemples:${NC}"
    echo "  ./run_organized_tests.sh unit"
    echo "  ./run_organized_tests.sh integration --cov"
    echo "  ./run_organized_tests.sh ui -v -x"
    echo "  ./run_organized_tests.sh all --cov-html"
    echo "  ./run_organized_tests.sh quick -k pdf"
    echo "  ./run_organized_tests.sh specific -k copyable"
    echo "  ./run_organized_tests.sh regression --tb=short"
    echo ""
}

# Fonction de backup de la base de données de production
backup_production_database() {
    echo -e "${BLUE}💾 Sauvegarde de la base de données de production...${NC}"

    # Créer le répertoire de backup s'il n'existe pas
    mkdir -p "$BACKUP_DIR"

    # Vérifier si la base de production existe
    if [[ ! -f "$PRODUCTION_DB" ]]; then
        echo -e "${YELLOW}⚠️  Base de données de production non trouvée: $PRODUCTION_DB${NC}"
        echo -e "${YELLOW}   Aucun backup nécessaire${NC}"
        return 0
    fi

    # Créer le nom du fichier de backup avec timestamp
    local timestamp=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/facturacion_backup_before_tests_${timestamp}.db"

    # Copier la base de données
    cp "$PRODUCTION_DB" "$BACKUP_FILE"

    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ Backup DB créé: $(basename $BACKUP_FILE)${NC}"
        echo -e "${GREEN}   Taille: $(du -h $BACKUP_FILE | cut -f1)${NC}"
    else
        echo -e "${RED}❌ Erreur lors de la création du backup DB${NC}"
        exit 1
    fi
}

# Fonction de backup de la configuration et logos
backup_production_config() {
    echo -e "${BLUE}💾 Sauvegarde de la configuration et logos...${NC}"

    # Créer le répertoire de backup s'il n'existe pas
    mkdir -p "$BACKUP_DIR"

    local timestamp=$(date +%Y%m%d_%H%M%S)

    # Backup config.json
    if [[ -f "$PRODUCTION_CONFIG" ]]; then
        CONFIG_BACKUP_FILE="$BACKUP_DIR/config_backup_before_tests_${timestamp}.json"
        cp "$PRODUCTION_CONFIG" "$CONFIG_BACKUP_FILE"

        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ Backup config.json créé: $(basename $CONFIG_BACKUP_FILE)${NC}"
        else
            echo -e "${RED}❌ Erreur lors de la création du backup config.json${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️  config.json non trouvé, aucun backup nécessaire${NC}"
    fi

    # Backup répertoire logo/
    if [[ -d "$PRODUCTION_LOGO_DIR" ]]; then
        LOGO_BACKUP_DIR="$BACKUP_DIR/logo_backup_before_tests_${timestamp}"
        cp -r "$PRODUCTION_LOGO_DIR" "$LOGO_BACKUP_DIR"

        if [[ $? -eq 0 ]]; then
            local logo_count=$(find "$LOGO_BACKUP_DIR" -type f | wc -l)
            echo -e "${GREEN}✅ Backup logo/ créé: $(basename $LOGO_BACKUP_DIR) ($logo_count fichiers)${NC}"
        else
            echo -e "${RED}❌ Erreur lors de la création du backup logo/${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️  Répertoire logo/ non trouvé, aucun backup nécessaire${NC}"
    fi

    echo ""
}

# Fonction de restauration de la base de données de production
restore_production_database() {
    echo ""
    echo -e "${BLUE}🔄 Restauration de la base de données de production...${NC}"

    # Vérifier si un backup a été créé
    if [[ -z "$BACKUP_FILE" ]] || [[ ! -f "$BACKUP_FILE" ]]; then
        echo -e "${YELLOW}⚠️  Aucun backup DB à restaurer${NC}"
        return 0
    fi

    # Restaurer la base de données
    cp "$BACKUP_FILE" "$PRODUCTION_DB"

    if [[ $? -eq 0 ]]; then
        echo -e "${GREEN}✅ Base de données restaurée depuis: $(basename $BACKUP_FILE)${NC}"
    else
        echo -e "${RED}❌ Erreur lors de la restauration DB${NC}"
        echo -e "${RED}   Le backup est disponible ici: $BACKUP_FILE${NC}"
        exit 1
    fi
}

# Fonction de restauration de la configuration et logos
restore_production_config() {
    echo -e "${BLUE}🔄 Restauration de la configuration et logos...${NC}"

    local has_restore=false

    # Restaurer config.json
    if [[ -n "$CONFIG_BACKUP_FILE" ]] && [[ -f "$CONFIG_BACKUP_FILE" ]]; then
        cp "$CONFIG_BACKUP_FILE" "$PRODUCTION_CONFIG"

        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✅ config.json restauré depuis: $(basename $CONFIG_BACKUP_FILE)${NC}"
            has_restore=true
        else
            echo -e "${RED}❌ Erreur lors de la restauration config.json${NC}"
            echo -e "${RED}   Le backup est disponible ici: $CONFIG_BACKUP_FILE${NC}"
            exit 1
        fi
    fi

    # Restaurer répertoire logo/
    if [[ -n "$LOGO_BACKUP_DIR" ]] && [[ -d "$LOGO_BACKUP_DIR" ]]; then
        # Supprimer le répertoire logo/ actuel et restaurer le backup
        rm -rf "$PRODUCTION_LOGO_DIR"
        cp -r "$LOGO_BACKUP_DIR" "$PRODUCTION_LOGO_DIR"

        if [[ $? -eq 0 ]]; then
            local logo_count=$(find "$PRODUCTION_LOGO_DIR" -type f | wc -l)
            echo -e "${GREEN}✅ logo/ restauré depuis: $(basename $LOGO_BACKUP_DIR) ($logo_count fichiers)${NC}"
            has_restore=true
        else
            echo -e "${RED}❌ Erreur lors de la restauration logo/${NC}"
            echo -e "${RED}   Le backup est disponible ici: $LOGO_BACKUP_DIR${NC}"
            exit 1
        fi
    fi

    if [[ "$has_restore" == false ]]; then
        echo -e "${YELLOW}⚠️  Aucun backup config/logo à restaurer${NC}"
    fi

    echo ""
}

# Fonction de vérification de l'environnement
check_environment() {
    echo -e "${BLUE}🔧 Vérification de l'environnement...${NC}"

    # Vérifier le répertoire de travail
    if [[ ! -d "$TEST_DIR" ]]; then
        echo -e "${RED}❌ Répertoire de tests non trouvé: $TEST_DIR${NC}"
        exit 1
    fi

    # Activer l'environnement virtuel
    if [[ -f "$VENV_DIR/activate" ]]; then
        echo -e "${GREEN}📁 Activation de l'environnement virtuel...${NC}"
        source "$VENV_DIR/activate"
    else
        echo -e "${YELLOW}⚠️  Environnement virtuel non trouvé, utilisation de l'environnement système${NC}"
    fi

    # Vérifier pytest
    if ! command -v pytest &> /dev/null; then
        echo -e "${RED}❌ pytest non installé${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ Environnement prêt${NC}"
    echo ""
}

# Fonction d'exécution des tests
run_tests() {
    local test_type="$1"
    shift
    local pytest_args="$@"
    
    case "$test_type" in
        "all")
            echo -e "${PURPLE}🧪 Exécution de TOUS les tests${NC}"
            pytest "$TEST_DIR/" $pytest_args
            ;;
        "unit")
            echo -e "${GREEN}🔧 Tests unitaires${NC}"
            pytest "$TEST_DIR/unit/" $pytest_args
            ;;
        "integration")
            echo -e "${BLUE}🔗 Tests d'intégration${NC}"
            pytest "$TEST_DIR/integration/" $pytest_args
            ;;
        "ui")
            echo -e "${CYAN}🎨 Tests interface utilisateur${NC}"
            pytest "$TEST_DIR/ui/" $pytest_args
            ;;
        "regression")
            echo -e "${YELLOW}🔄 Tests de régression${NC}"
            pytest "$TEST_DIR/regression/" $pytest_args
            ;;
        "performance")
            echo -e "${RED}⚡ Tests de performance${NC}"
            pytest "$TEST_DIR/performance/" $pytest_args
            ;;
        "property")
            echo -e "${PURPLE}🎲 Tests property-based${NC}"
            pytest "$TEST_DIR/property_based/" $pytest_args
            ;;
        "specific")
            echo -e "${CYAN}🎯 Tests fonctionnalités spécifiques${NC}"
            pytest "$TEST_DIR/specific/" $pytest_args
            ;;
        "scripts")
            echo -e "${BLUE}📜 Scripts de test${NC}"
            echo "Scripts disponibles dans $TEST_DIR/scripts/:"
            ls -la "$TEST_DIR/scripts/"
            echo ""
            echo "Pour exécuter un script: python3 $TEST_DIR/scripts/[nom_script]"
            return 0
            ;;
        "demo")
            echo -e "${GREEN}🎯 Exécution des démonstrations${NC}"
            for demo in "$TEST_DIR/demo"/*.py; do
                if [[ -f "$demo" ]]; then
                    echo -e "${BLUE}▶️  $(basename "$demo")${NC}"
                    python3 "$demo"
                    echo ""
                fi
            done
            return 0
            ;;
        "quick")
            echo -e "${GREEN}⚡ Tests rapides (unit + integration)${NC}"
            pytest "$TEST_DIR/unit/" "$TEST_DIR/integration/" $pytest_args
            ;;
        "ci")
            echo -e "${BLUE}🔄 Tests CI/CD (sans performance)${NC}"
            pytest "$TEST_DIR/" --ignore="$TEST_DIR/performance/" --ignore="$TEST_DIR/demo/" --ignore="$TEST_DIR/scripts/" $pytest_args
            ;;
        "pyqt5")
            echo -e "${GREEN}🚀 Tests PyQt5 (Suite spécialisée)${NC}"
            echo -e "${YELLOW}💡 Redirection vers la suite PyQt5 spécialisée...${NC}"
            exec ./run_pyqt5_tests_simple.sh quick
            ;;
        *)
            echo -e "${RED}❌ Type de test inconnu: $test_type${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Fonction de rapport post-exécution
show_report() {
    local exit_code=$1
    local test_type="$2"
    local duration="$3"

    echo ""
    echo -e "${BLUE}📊 RÉSUMÉ DÉTAILLÉ DES TESTS${NC}"
    echo "=" $(printf '=%.0s' {1..50})
    echo ""

    # Informations générales
    echo -e "${CYAN}📋 INFORMATIONS GÉNÉRALES${NC}"
    echo "Type de tests: $test_type"
    echo "Durée d'exécution: ${duration}s"
    echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "Répertoire: $PROJECT_DIR"
    echo ""

    # Résultat principal
    echo -e "${CYAN}🎯 RÉSULTAT PRINCIPAL${NC}"
    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}✅ TOUS LES TESTS ONT RÉUSSI${NC}"
        echo -e "${GREEN}🎉 Suite de tests '$test_type' validée !${NC}"
        echo ""

        # Messages spécifiques selon le type de test
        case "$test_type" in
            "all")
                echo -e "${YELLOW}🚀 Toute la suite de tests a été validée !${NC}"
                echo "   Votre application est prête pour la production."
                ;;
            "pyqt5")
                echo -e "${YELLOW}🎨 Interface PyQt5 validée !${NC}"
                echo "   Votre interface PyQt5 est fonctionnelle."
                ;;
            "unit")
                echo -e "${YELLOW}🔧 Tests unitaires validés !${NC}"
                echo "   Les composants individuels fonctionnent correctement."
                ;;
            "integration")
                echo -e "${YELLOW}🔗 Tests d'intégration validés !${NC}"
                echo "   Les interactions entre composants sont correctes."
                ;;
            "ui")
                echo -e "${YELLOW}🎨 Tests UI validés !${NC}"
                echo "   L'interface utilisateur fonctionne correctement."
                ;;
            "performance")
                echo -e "${YELLOW}⚡ Tests de performance validés !${NC}"
                echo "   Les performances de l'application sont acceptables."
                ;;
            "quick")
                echo -e "${YELLOW}⚡ Tests rapides validés !${NC}"
                echo "   Les fonctionnalités essentielles sont opérationnelles."
                ;;
        esac

    else
        echo -e "${RED}❌ CERTAINS TESTS ONT ÉCHOUÉ${NC}"
        echo -e "${RED}⚠️  Code de sortie: $exit_code${NC}"
        echo ""

        echo -e "${YELLOW}💡 ACTIONS RECOMMANDÉES:${NC}"
        echo "   1. Examinez les erreurs détaillées ci-dessus"
        echo "   2. Corrigez les problèmes identifiés"
        echo "   3. Relancez les tests: ./run_organized_tests.sh $test_type"
        echo ""

        echo -e "${CYAN}🔧 COMMANDES UTILES POUR LE DEBUG:${NC}"
        echo "   ./run_organized_tests.sh $test_type -v     # Mode verbose"
        echo "   ./run_organized_tests.sh $test_type -s     # Afficher les prints"
        echo "   ./run_organized_tests.sh $test_type -x     # Arrêt au premier échec"
        echo "   ./run_organized_tests.sh $test_type --lf   # Derniers tests échoués"
    fi
    echo ""

    # Informations de couverture
    if [[ -d "$COVERAGE_DIR" ]]; then
        echo -e "${CYAN}📈 COUVERTURE DE CODE${NC}"
        echo -e "${BLUE}Rapport HTML disponible:${NC}"
        echo "   file://$PROJECT_DIR/$COVERAGE_DIR/index.html"
        echo ""
    fi

    # Conseils généraux
    echo -e "${CYAN}💡 CONSEILS GÉNÉRAUX${NC}"
    echo "   • Pour aide complète: ./run_organized_tests.sh --help"
    echo "   • Tests PyQt5 spécialisés: ./run_organized_tests.sh pyqt5"
    echo "   • Tests rapides: ./run_organized_tests.sh quick"
    echo "   • Tous les tests: ./run_organized_tests.sh all --cov-html"
    echo ""
}

# Fonction principale
main() {
    # Gestion des arguments
    if [[ $# -eq 0 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
        show_help
        exit 0
    fi

    local test_type="$1"
    shift

    # 🛡️ VÉRIFICATION CRITIQUE: Protection contre la pollution de la base de production
    echo -e "${BLUE}🛡️  Vérification de la protection des données de production...${NC}"
    if ! python3 "${TEST_DIR}/verifier_protection_tests.py"; then
        echo ""
        echo -e "${RED}❌ ERREUR CRITIQUE: La protection de la base de données n'est pas correctement configurée!${NC}"
        echo -e "${RED}   Les tests risquent de polluer la base de données de production.${NC}"
        echo ""
        echo -e "${YELLOW}🔧 Solutions possibles:${NC}"
        echo -e "   1. Vérifier que database/database.py utilise PYTEST_RUNNING et TEST_DATABASE_PATH"
        echo -e "   2. Vérifier que test/conftest.py définit correctement les fixtures isolées"
        echo -e "   3. Vérifier que test/unit/conftest.py utilise tempfile pour unit_db"
        echo ""
        exit 1
    fi
    echo ""

    # 🛡️ PROTECTION CRITIQUE: Backup de la base de données de production
    backup_production_database

    # 🛡️ PROTECTION CRITIQUE: Backup de la configuration et logos
    backup_production_config

    # Vérification de l'environnement
    check_environment

    # Affichage des informations
    echo -e "${BLUE}🧪 === TESTS ORGANISÉS - FACTURACIÓN FÁCIL ===${NC}"
    echo -e "${YELLOW}📁 Répertoire de travail:${NC} $PROJECT_DIR"
    echo -e "${YELLOW}🎯 Type de tests:${NC} $test_type"
    echo -e "${YELLOW}⚙️  Options:${NC} $@"
    echo ""

    # Exécution des tests
    local start_time=$(date +%s)

    run_tests "$test_type" "$@"
    local exit_code=$?

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    # 🛡️ PROTECTION CRITIQUE: Restauration de la base de données de production
    restore_production_database

    # 🛡️ PROTECTION CRITIQUE: Restauration de la configuration et logos
    restore_production_config

    # Rapport final
    show_report $exit_code "$test_type" $duration

    exit $exit_code
}

# Point d'entrée
main "$@"
