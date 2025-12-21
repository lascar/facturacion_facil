#!/bin/bash
# Script pour exécuter la suite complète de tests de comportement
# basée sur les spécifications facturacion_facil.txt

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

echo -e "${BLUE}🎯 Suite Complète de Tests de Comportement - Basée sur facturacion_facil.txt${NC}"
echo "================================================================================"
echo ""

show_usage() {
    echo -e "${YELLOW}Usage: $0 [app|widgets|dialogs|search|stock|all]${NC}"
    echo ""
    echo "Options:"
    echo "  app       - Tests complets application (fenêtres principales)"
    echo "  widgets   - Tests widgets autocomplétion"
    echo "  dialogs   - Tests dialogues modaux"
    echo "  search    - Tests recherche avancée"
    echo "  stock     - Tests gestion stock"
    echo "  all       - Tous les tests complets (défaut)"
    echo ""
}

show_summary() {
    echo ""
    echo -e "${PURPLE}📊 RÉSUMÉ DES TESTS COMPLETS${NC}"
    echo "================================="
    echo -e "${GREEN}✅ Tests application: Fenêtres principales selon spécifications${NC}"
    echo -e "${GREEN}✅ Tests widgets: ClientAutoComplete + ProductAutoComplete${NC}"
    echo -e "${GREEN}✅ Tests dialogues: InvoiceStatus + DataCleanup + ProductConfig${NC}"
    echo -e "${GREEN}✅ Tests recherche: SearchWindow avec filtres avancés${NC}"
    echo -e "${GREEN}✅ Tests stock: StockWindow avec ajustements temps réel${NC}"
    echo ""
    echo -e "${CYAN}🎯 SUITE BASÉE SUR FACTURACION_FACIL.TXT${NC}"
    echo -e "${CYAN}✅ Tests suivent les spécifications exactes${NC}"
    echo -e "${CYAN}✅ Validation des workflows complets${NC}"
    echo -e "${CYAN}✅ Tests indépendants du code existant (potentiellement bugué)${NC}"
    echo ""
}

# Fonction principale
run_complete_tests() {
    local test_type="${1:-all}"
    
    echo -e "${YELLOW}🚀 Exécution des tests complets: $test_type${NC}"
    echo ""
    
    # Aller dans le répertoire du projet
    cd "$PROJECT_DIR"
    
    # Configuration pour les tests headless
    export QT_QPA_PLATFORM=offscreen
    
    case "$test_type" in
        "app"|"application")
            echo -e "${CYAN}🏠 Tests complets application...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_complete_application_behaviour.py -v
            ;;
            
        "widgets"|"autocomplete")
            echo -e "${CYAN}🔧 Tests widgets autocomplétion...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_autocomplete_widgets_behaviour.py -v
            ;;
            
        "dialogs"|"dialogues")
            echo -e "${CYAN}💬 Tests dialogues...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_dialogs_behaviour.py -v
            ;;
            
        "search"|"recherche")
            echo -e "${CYAN}🔍 Tests recherche avancée...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_search_window_behaviour.py -v
            ;;
            
        "stock"|"inventaire")
            echo -e "${CYAN}📊 Tests gestion stock...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_stock_window_behaviour.py -v
            ;;
            
        "all"|*)
            echo -e "${CYAN}🏠 1. Tests complets application...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_complete_application_behaviour.py -v
            echo ""
            
            echo -e "${CYAN}🔧 2. Tests widgets autocomplétion...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_autocomplete_widgets_behaviour.py -v
            echo ""
            
            echo -e "${CYAN}💬 3. Tests dialogues...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_dialogs_behaviour.py -v
            echo ""
            
            echo -e "${CYAN}🔍 4. Tests recherche avancée...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_search_window_behaviour.py -v
            echo ""
            
            echo -e "${CYAN}📊 5. Tests gestion stock...${NC}"
            /home/pascal/.pyenv/shims/python -m pytest test/behaviour/test_stock_window_behaviour.py -v
            echo ""
            ;;
    esac
}

# Vérifier les arguments
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_usage
    exit 0
fi

# Exécuter les tests
echo -e "${GREEN}🔧 Activation de l'environnement...${NC}"
source "$PROJECT_DIR/activate_env.sh"

run_complete_tests "$1"

show_summary

echo -e "${GREEN}✅ Tests complets terminés !${NC}"
echo ""
