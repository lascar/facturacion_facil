#!/bin/bash
# Script pour exécuter les tests de comportement PyQt5 avec QTest

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORTS_DIR="$SCRIPT_DIR/reports"

# Créer le répertoire de rapports
mkdir -p "$REPORTS_DIR"
mkdir -p "$SCRIPT_DIR/screenshots"

echo -e "${BLUE}🧪 Tests de Comportement PyQt5 - Facturación Fácil${NC}"
echo "=================================================="
echo -e "📁 Répertoire projet: ${PROJECT_DIR}"
echo -e "📁 Répertoire tests: ${SCRIPT_DIR}"
echo ""

# Fonction pour vérifier l'environnement
check_environment() {
    echo -e "${YELLOW}🔧 Vérification de l'environnement...${NC}"
    
    # Activer l'environnement
    cd "$PROJECT_DIR"
    source ./activate_env.sh
    
    # Vérifier pytest avec le chemin complet
    if ! /home/pascal/.pyenv/shims/python -m pytest --version &> /dev/null; then
        echo -e "${RED}❌ pytest non trouvé dans l'environnement${NC}"
        exit 1
    fi
    
    # Vérifier PyQt5
    if ! python -c "import PyQt5.QtWidgets, PyQt5.QtTest" 2>/dev/null; then
        echo -e "${RED}❌ PyQt5 ou QTest non disponible${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Environnement PyQt5 prêt${NC}"
}

# Fonction pour exécuter les tests simples
run_simple_tests() {
    echo -e "${CYAN}🚀 1. Tests simples de validation...${NC}"

    # Utiliser seulement les options de base de pytest
    /home/pascal/.pyenv/shims/python -m pytest "$SCRIPT_DIR/test_simple_behaviour.py" \
        -v \
        --tb=short \
        2>&1 | tee "$REPORTS_DIR/simple_tests_$TIMESTAMP.log"

    return $?
}

# Fonction pour exécuter les tests de base de données
run_database_tests() {
    echo -e "${CYAN}🗄️ 2. Tests de base de données...${NC}"

    /home/pascal/.pyenv/shims/python -m pytest "$SCRIPT_DIR/test_database_behaviour.py" \
        -v \
        --tb=short \
        2>&1 | tee "$REPORTS_DIR/database_tests_$TIMESTAMP.log"

    return $?
}

# Fonction pour exécuter les tests GUI avec QTest
run_gui_tests() {
    echo -e "${CYAN}🖥️ 3. Tests GUI avec QTest...${NC}"
    
    # Configurer l'environnement pour les tests GUI
    export QT_QPA_PLATFORM=offscreen
    export DISPLAY=:99
    
    # Tests clients
    echo -e "${YELLOW}   👥 Tests Clients...${NC}"
    timeout 300 /home/pascal/.pyenv/shims/python -m pytest "$SCRIPT_DIR/test_clientes_behaviour.py" \
        -v \
        --tb=short \
        --headless \
        --screenshots \
        2>&1 | tee "$REPORTS_DIR/clientes_tests_$TIMESTAMP.log" || true
    
    CLIENTES_EXIT=$?
    
    # Tests facturas
    echo -e "${YELLOW}   📄 Tests Facturas...${NC}"
    timeout 300 /home/pascal/.pyenv/shims/python -m pytest "$SCRIPT_DIR/test_facturas_behaviour.py" \
        -v \
        --tb=short \
        --headless \
        --screenshots \
        2>&1 | tee "$REPORTS_DIR/facturas_tests_$TIMESTAMP.log" || true
    
    FACTURAS_EXIT=$?
    
    # Tests fenêtre principale
    echo -e "${YELLOW}   🏠 Tests Fenêtre Principale...${NC}"
    timeout 180 /home/pascal/.pyenv/shims/python -m pytest "$SCRIPT_DIR/test_main_window_behaviour.py" \
        -v \
        --tb=short \
        --headless \
        2>&1 | tee "$REPORTS_DIR/main_window_tests_$TIMESTAMP.log" || true
    
    MAIN_EXIT=$?
    
    # Retourner le pire code de sortie
    if [ $CLIENTES_EXIT -ne 0 ] || [ $FACTURAS_EXIT -ne 0 ] || [ $MAIN_EXIT -ne 0 ]; then
        return 1
    fi
    return 0
}

# Fonction principale
main() {
    local test_type="${1:-all}"
    
    echo -e "${BLUE}🚀 SUITE DE TESTS PYQT5 BEHAVIOUR${NC}"
    echo -e "${PURPLE}📅 $(date)${NC}"
    echo ""
    
    # Vérifier l'environnement
    check_environment
    echo ""
    
    case $test_type in
        "simple")
            run_simple_tests
            ;;
        "database") 
            run_database_tests
            ;;
        "gui")
            run_gui_tests
            ;;
        "all"|*)
            echo -e "${BLUE}🎯 Exécution de tous les tests de comportement${NC}"
            echo ""
            
            # 1. Tests simples
            run_simple_tests
            SIMPLE_EXIT=$?
            echo ""
            
            # 2. Tests base de données
            run_database_tests  
            DB_EXIT=$?
            echo ""
            
            # 3. Tests GUI (seulement si les précédents passent)
            if [ $SIMPLE_EXIT -eq 0 ] && [ $DB_EXIT -eq 0 ]; then
                run_gui_tests
                GUI_EXIT=$?
            else
                echo -e "${YELLOW}⚠️ Tests GUI ignorés (échecs précédents)${NC}"
                GUI_EXIT=1
            fi
            
            # Résumé final
            echo ""
            echo -e "${BLUE}📊 RÉSUMÉ FINAL${NC}"
            echo "=================================="
            [ $SIMPLE_EXIT -eq 0 ] && echo -e "${GREEN}✅ Tests simples: RÉUSSIS${NC}" || echo -e "${RED}❌ Tests simples: ÉCHOUÉS${NC}"
            [ $DB_EXIT -eq 0 ] && echo -e "${GREEN}✅ Tests base de données: RÉUSSIS${NC}" || echo -e "${RED}❌ Tests base de données: ÉCHOUÉS${NC}"
            [ $GUI_EXIT -eq 0 ] && echo -e "${GREEN}✅ Tests GUI: RÉUSSIS${NC}" || echo -e "${RED}❌ Tests GUI: ÉCHOUÉS${NC}"
            
            echo ""
            echo -e "${PURPLE}📁 Rapports générés dans: $REPORTS_DIR${NC}"
            echo -e "${PURPLE}📸 Captures d'écran dans: $SCRIPT_DIR/screenshots${NC}"
            
            # Code de sortie global
            if [ $SIMPLE_EXIT -eq 0 ] && [ $DB_EXIT -eq 0 ] && [ $GUI_EXIT -eq 0 ]; then
                echo -e "${GREEN}🎉 TOUS LES TESTS RÉUSSIS !${NC}"
                exit 0
            else
                echo -e "${RED}💥 CERTAINS TESTS ONT ÉCHOUÉ${NC}"
                exit 1
            fi
            ;;
    esac
}

# Aide
show_help() {
    echo "Usage: $0 [TYPE]"
    echo ""
    echo "Types de tests disponibles:"
    echo "  simple     - Tests simples de validation"
    echo "  database   - Tests de base de données"
    echo "  gui        - Tests GUI avec QTest"
    echo "  all        - Tous les tests (défaut)"
    echo ""
    echo "Exemples:"
    echo "  $0              # Tous les tests"
    echo "  $0 simple       # Tests simples seulement"
    echo "  $0 gui          # Tests GUI seulement"
}

# Point d'entrée
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

main "$@"
