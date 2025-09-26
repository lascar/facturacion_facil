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

# Fonction d'aide
show_help() {
    echo -e "${BLUE}🧪 Script d'Exécution des Tests Organisés${NC}"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./run_organized_tests.sh [type] [options]"
    echo ""
    echo -e "${YELLOW}Types de tests:${NC}"
    echo -e "  ${GREEN}all${NC}              Tous les tests"
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
    
    echo ""
    echo -e "${BLUE}📊 Rapport d'exécution${NC}"
    echo "=================================="
    
    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}✅ Tests réussis${NC}"
    else
        echo -e "${RED}❌ Tests échoués (code: $exit_code)${NC}"
    fi
    
    # Afficher les informations de couverture si disponible
    if [[ -d "$COVERAGE_DIR" ]]; then
        echo -e "${BLUE}📈 Rapport de couverture disponible:${NC}"
        echo "   file://$PROJECT_DIR/$COVERAGE_DIR/index.html"
    fi
    
    echo ""
    echo -e "${YELLOW}💡 Conseils:${NC}"
    echo "   - Pour plus de détails: ajoutez -v"
    echo "   - Pour debug: ajoutez -s"
    echo "   - Pour couverture: ajoutez --cov-html"
    echo "   - Pour aide: ./run_organized_tests.sh --help"
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
    
    # Rapport final
    echo ""
    echo -e "${BLUE}⏱️  Durée d'exécution: ${duration}s${NC}"
    show_report $exit_code
    
    exit $exit_code
}

# Point d'entrée
main "$@"
