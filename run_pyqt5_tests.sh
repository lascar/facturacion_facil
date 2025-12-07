#!/bin/bash

# 🚀 Suite de Tests PyQt5 - Facturación Fácil
# Usage: ./run_pyqt5_tests.sh [type] [options]

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
TEST_DIR="test"
COVERAGE_DIR="htmlcov"

# Fonction d'aide
show_help() {
    echo -e "${BLUE}🚀 Suite de Tests PyQt5${NC}"
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  ./run_pyqt5_tests.sh [type] [options]"
    echo ""
    echo -e "${YELLOW}Types de tests PyQt5:${NC}"
    echo -e "  ${GREEN}all${NC}              Tous les tests PyQt5"
    echo -e "  ${GREEN}validation${NC}       Validation de l'interface PyQt5"
    echo -e "  ${GREEN}integration${NC}      Tests d'intégration PyQt5"
    echo -e "  ${GREEN}ui${NC}               Tests UI PyQt5"
    echo -e "  ${GREEN}performance${NC}      Tests de performance UI"
    echo -e "  ${GREEN}basic${NC}            Tests de base PyQt5"
    echo -e "  ${GREEN}compatibility${NC}    Tests de compatibilité"
    echo -e "  ${GREEN}quick${NC}            Tests rapides (validation + basic)"
    echo ""
    echo -e "${YELLOW}Options:${NC}"
    echo "  -v, --verbose        Mode verbose"
    echo "  -q, --quiet          Mode silencieux"
    echo "  --cov                Avec couverture de code"
    echo "  --cov-html           Avec rapport HTML de couverture"
    echo "  -h, --help           Afficher cette aide"
    echo ""
    echo -e "${YELLOW}Exemples:${NC}"
    echo "  ./run_pyqt5_tests.sh all --cov-html"
    echo "  ./run_pyqt5_tests.sh quick -v"
    echo "  ./run_pyqt5_tests.sh validation"
}

# Fonction pour vérifier l'environnement
check_environment() {
    echo -e "${BLUE}🔍 Vérification de l'environnement PyQt5...${NC}"
    
    # Vérifier Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 non trouvé${NC}"
        exit 1
    fi
    
    # Vérifier PyQt5
    if ! python3 -c "import PyQt5" 2>/dev/null; then
        echo -e "${RED}❌ PyQt5 non installé${NC}"
        echo -e "${YELLOW}💡 Installez PyQt5 avec: pip install PyQt5${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Environnement PyQt5 OK${NC}"
}

# Fonction pour exécuter les tests avec gestion d'erreurs
run_test_command() {
    local test_name="$1"
    local command="$2"
    local start_time=$(date +%s)
    
    echo -e "${CYAN}🧪 Exécution: ${test_name}${NC}"
    echo -e "${PURPLE}📝 Commande: ${command}${NC}"
    
    if eval "$command"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo -e "${GREEN}✅ ${test_name} réussi (${duration}s)${NC}"
        return 0
    else
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        echo -e "${RED}❌ ${test_name} échoué (${duration}s)${NC}"
        return 1
    fi
}

# Tests de validation PyQt5
run_validation_tests() {
    echo -e "${BLUE}🔍 Tests de Validation PyQt5${NC}"
    echo "=================================================="
    
    local success=0
    local total=0
    
    # Test de validation principal
    ((total++))
    if run_test_command "Validation Interface PyQt5" "python3 verify_pyqt5_only.py"; then
        ((success++))
    fi
    
    echo -e "${BLUE}📊 Résultats Validation: ${success}/${total}${NC}"
    return $((total - success))
}

# Tests d'intégration PyQt5
run_integration_tests() {
    echo -e "${BLUE}🔗 Tests d'Intégration PyQt5${NC}"
    echo "=================================================="
    
    local success=0
    local total=0
    local pytest_args="$1"
    
    # Tests d'intégration existants
    if [ -d "$TEST_DIR/integration" ]; then
        ((total++))
        if run_test_command "Tests Intégration Généraux" "python3 -m pytest $TEST_DIR/integration/ ${pytest_args}"; then
            ((success++))
        fi
    fi
    
    echo -e "${BLUE}📊 Résultats Intégration: ${success}/${total}${NC}"
    return $((total - success))
}

# Tests UI PyQt5
run_ui_tests() {
    echo -e "${BLUE}🖥️ Tests UI PyQt5${NC}"
    echo "=================================================="

    local success=0
    local total=0
    local pytest_args="$1"

    # Tests UI existants
    if [ -d "$TEST_DIR/ui" ]; then
        ((total++))
        if run_test_command "Tests UI PyQt5" "python3 -m pytest $TEST_DIR/ui/ ${pytest_args}"; then
            ((success++))
        fi
    fi

    echo -e "${BLUE}📊 Résultats UI: ${success}/${total}${NC}"
    return $((total - success))
}

# Tests de base PyQt5
run_basic_tests() {
    echo -e "${BLUE}⚡ Tests de Base PyQt5${NC}"
    echo "=================================================="

    local success=0
    local total=0

    # Test d'import des modules principaux
    ((total++))
    if run_test_command "Import Modules PyQt5" "python3 -c 'from ui.main_window_pyqt5 import MainWindowPyQt5; print(\"✅ Import réussi\")'"; then
        ((success++))
    fi

    # Test de création d'application
    ((total++))
    if run_test_command "Création Application PyQt5" "python3 -c 'from PyQt5.QtWidgets import QApplication; import sys; app = QApplication(sys.argv); print(\"✅ Application créée\")'"; then
        ((success++))
    fi

    echo -e "${BLUE}📊 Résultats Base: ${success}/${total}${NC}"
    return $((total - success))
}

# Tests de performance
run_performance_tests() {
    echo -e "${BLUE}⚡ Tests de Performance${NC}"
    echo "=================================================="

    local success=0
    local total=0

    # Tests de performance si disponibles
    if [ -d "$TEST_DIR/performance" ]; then
        ((total++))
        if run_test_command "Tests Performance UI" "python3 -m pytest $TEST_DIR/performance/ -v"; then
            ((success++))
        fi
    else
        echo -e "${YELLOW}⚠️ Aucun test de performance trouvé${NC}"
    fi

    echo -e "${BLUE}📊 Résultats Performance: ${success}/${total}${NC}"
    return $((total - success))
}

# Suite complète PyQt5
run_complete_suite() {
    echo -e "${BLUE}🚀 Suite Complète PyQt5${NC}"
    echo "============================================================"

    local pytest_args="$1"
    local total_failures=0

    # Arrays pour stocker les résultats détaillés
    declare -a test_results=()
    declare -a test_names=()

    # Exécuter tous les types de tests avec capture des résultats
    echo -e "${CYAN}🔍 Tests de Validation PyQt5${NC}"
    if run_validation_tests; then
        test_results+=("✅ RÉUSSI")
        test_names+=("Tests de Validation")
    else
        test_results+=("❌ ÉCHOUÉ")
        test_names+=("Tests de Validation")
        ((total_failures++))
    fi
    echo ""

    echo -e "${CYAN}⚡ Tests de Base PyQt5${NC}"
    if run_basic_tests; then
        test_results+=("✅ RÉUSSI")
        test_names+=("Tests de Base")
    else
        test_results+=("❌ ÉCHOUÉ")
        test_names+=("Tests de Base")
        ((total_failures++))
    fi
    echo ""

    echo -e "${CYAN}🔗 Tests d'Intégration PyQt5${NC}"
    if run_integration_tests "$pytest_args"; then
        test_results+=("✅ RÉUSSI")
        test_names+=("Tests d'Intégration")
    else
        test_results+=("❌ ÉCHOUÉ")
        test_names+=("Tests d'Intégration")
        ((total_failures++))
    fi
    echo ""

    echo -e "${CYAN}🖥️ Tests UI PyQt5${NC}"
    if run_ui_tests "$pytest_args"; then
        test_results+=("✅ RÉUSSI")
        test_names+=("Tests UI")
    else
        test_results+=("❌ ÉCHOUÉ")
        test_names+=("Tests UI")
        ((total_failures++))
    fi
    echo ""

    echo -e "${CYAN}⚡ Tests de Performance${NC}"
    if run_performance_tests; then
        test_results+=("✅ RÉUSSI")
        test_names+=("Tests de Performance")
    else
        test_results+=("❌ ÉCHOUÉ")
        test_names+=("Tests de Performance")
        ((total_failures++))
    fi
    echo ""

    # Résumé final détaillé
    show_detailed_summary "${test_names[@]}" "${test_results[@]}" $total_failures

    return $total_failures
}

# Fonction principale
main() {
    # Vérifier d'abord les options d'aide
    if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        show_help
        exit 0
    fi

    local test_type="${1:-all}"
    local pytest_args=""

    # Parser les arguments
    shift || true
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--verbose)
                pytest_args="$pytest_args -v"
                shift
                ;;
            -q|--quiet)
                pytest_args="$pytest_args -q"
                shift
                ;;
            --cov)
                pytest_args="$pytest_args --cov=ui"
                shift
                ;;
            --cov-html)
                pytest_args="$pytest_args --cov=ui --cov-report=html"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                pytest_args="$pytest_args $1"
                shift
                ;;
        esac
    done

    echo -e "${BLUE}🚀 SUITE DE TESTS PYQT5${NC}"
    echo -e "${PURPLE}📅 $(date)${NC}"
    echo -e "${PURPLE}📁 Répertoire: $(pwd)${NC}"
    echo ""

    # Vérifier l'environnement
    check_environment
    echo ""

    # Exécuter les tests selon le type
    case $test_type in
        all)
            run_complete_suite "$pytest_args"
            ;;
        validation)
            run_validation_tests
            ;;
        integration)
            run_integration_tests "$pytest_args"
            ;;
        ui)
            run_ui_tests "$pytest_args"
            ;;
        basic)
            run_basic_tests
            ;;
        performance)
            run_performance_tests
            ;;
        quick)
            echo -e "${BLUE}⚡ Tests Rapides PyQt5${NC}"
            run_validation_tests || exit 1
            echo ""
            run_basic_tests || exit 1
            ;;
        *)
            echo -e "${RED}❌ Type de test inconnu: $test_type${NC}"
            show_help
            exit 1
            ;;
    esac
}

# Fonction pour afficher un résumé détaillé
show_detailed_summary() {
    local test_names=("${@:1:5}")  # Les 5 premiers arguments sont les noms
    local test_results=("${@:6:5}")  # Les 5 suivants sont les résultats
    local total_failures=${@: -1}  # Le dernier argument est le nombre d'échecs

    local total_tests=${#test_names[@]}
    local passed_tests=$((total_tests - total_failures))

    echo -e "${BLUE}📋 RÉSUMÉ DÉTAILLÉ DES TESTS PYQT5${NC}"
    echo "============================================================"
    echo ""

    # Statistiques globales
    echo -e "${CYAN}📊 STATISTIQUES GLOBALES${NC}"
    echo "Total des suites de tests: $total_tests"
    echo "Suites réussies: $passed_tests"
    echo "Suites échouées: $total_failures"
    if [ $total_tests -gt 0 ]; then
        local success_rate=$(( (passed_tests * 100) / total_tests ))
        echo "Taux de réussite: ${success_rate}%"
    fi
    echo ""

    # Détail par test
    echo -e "${CYAN}📋 DÉTAIL PAR SUITE DE TESTS${NC}"
    echo "----------------------------------------"
    for i in "${!test_names[@]}"; do
        local name="${test_names[$i]}"
        local result="${test_results[$i]}"
        printf "%-25s %s\n" "$name" "$result"
    done
    echo ""

    # Tests réussis
    if [ $passed_tests -gt 0 ]; then
        echo -e "${GREEN}✅ TESTS RÉUSSIS ($passed_tests/${total_tests})${NC}"
        for i in "${!test_names[@]}"; do
            if [[ "${test_results[$i]}" == *"✅"* ]]; then
                echo "  🎯 ${test_names[$i]}"
            fi
        done
        echo ""
    fi

    # Tests échoués
    if [ $total_failures -gt 0 ]; then
        echo -e "${RED}❌ TESTS ÉCHOUÉS ($total_failures/${total_tests})${NC}"
        for i in "${!test_names[@]}"; do
            if [[ "${test_results[$i]}" == *"❌"* ]]; then
                echo "  ⚠️  ${test_names[$i]}"
            fi
        done
        echo ""
    fi

    # Message final
    echo -e "${BLUE}🎯 CONCLUSION${NC}"
    echo "----------------------------------------"
    if [ $total_failures -eq 0 ]; then
        echo -e "${GREEN}🎉 TOUS LES TESTS PYQT5 ONT RÉUSSI !${NC}"
        echo -e "${GREEN}✨ Votre interface PyQt5 est validée !${NC}"
        echo ""
        echo -e "${YELLOW}🚀 Votre application est prête à utiliser PyQt5 !${NC}"
        echo -e "${CYAN}💡 Lancez votre application avec: python3 main.py${NC}"
    else
        echo -e "${RED}⚠️ $total_failures suite(s) de tests ont échoué${NC}"
        echo -e "${YELLOW}💡 Actions recommandées:${NC}"
        echo "   1. Vérifiez les erreurs détaillées ci-dessus"
        echo "   2. Corrigez les problèmes identifiés"
        echo "   3. Relancez les tests: ./run_pyqt5_tests.sh all"
        echo ""
        echo -e "${CYAN}🔧 Pour des tests spécifiques:${NC}"
        echo "   ./run_pyqt5_tests.sh validation  # Tests de validation"
        echo "   ./run_pyqt5_tests.sh integration # Tests d'intégration"
        echo "   ./run_pyqt5_tests.sh ui          # Tests UI"
    fi
    echo ""
}

# Exécuter le script
main "$@"
