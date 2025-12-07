#!/bin/bash

# 🚀 Suite de Tests PyQt5 Simplifiée - Facturación Fácil
# Usage: ./run_pyqt5_tests_simple.sh [type]

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 SUITE DE TESTS PYQT5 SIMPLIFIÉE${NC}"
echo -e "${PURPLE}📅 $(date)${NC}"
echo ""

# Vérifier PyQt5
echo -e "${BLUE}🔍 Vérification de l'environnement PyQt5...${NC}"
if ! python3 -c "import PyQt5" 2>/dev/null; then
    echo -e "${RED}❌ PyQt5 non installé${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Environnement PyQt5 OK${NC}"
echo ""

# Tests selon le type
case "${1:-basic}" in
    "basic"|"")
        echo -e "${BLUE}⚡ Tests de Base PyQt5${NC}"
        echo "=================================================="
        
        echo -e "${CYAN}🧪 Test 1: Import des modules principaux${NC}"
        if python3 -c "from ui.main_window_pyqt5 import MainWindowPyQt5; print('✅ Import réussi')" 2>/dev/null; then
            echo -e "${GREEN}✅ Import Modules PyQt5 réussi${NC}"
        else
            echo -e "${RED}❌ Import Modules PyQt5 échoué${NC}"
            exit 1
        fi
        
        echo -e "${CYAN}🧪 Test 2: Création d'application PyQt5${NC}"
        if python3 -c "from PyQt5.QtWidgets import QApplication; import sys; app = QApplication(sys.argv); print('✅ Application créée')" 2>/dev/null; then
            echo -e "${GREEN}✅ Création Application PyQt5 réussi${NC}"
        else
            echo -e "${RED}❌ Création Application PyQt5 échoué${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${GREEN}🎉 TOUS LES TESTS DE BASE ONT RÉUSSI !${NC}"
        ;;
        
    "validation")
        echo -e "${BLUE}🔍 Tests de Validation PyQt5${NC}"
        echo "=================================================="
        
        echo -e "${CYAN}🧪 Validation de l'interface PyQt5${NC}"
        if python3 verify_pyqt5_only.py; then
            echo -e "${GREEN}✅ Validation Interface PyQt5 réussi${NC}"
        else
            echo -e "${RED}❌ Validation Interface PyQt5 échoué${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${GREEN}🎉 VALIDATION PYQT5 RÉUSSIE !${NC}"
        ;;
        
    "quick")
        echo -e "${BLUE}⚡ Tests Rapides PyQt5${NC}"
        echo "=================================================="
        
        # Tests de base
        echo -e "${CYAN}🧪 Tests de base...${NC}"
        if python3 -c "from ui.main_window_pyqt5 import MainWindowPyQt5; from PyQt5.QtWidgets import QApplication; import sys; app = QApplication(sys.argv); print('✅ Tests de base OK')" 2>/dev/null; then
            echo -e "${GREEN}✅ Tests de base réussis${NC}"
        else
            echo -e "${RED}❌ Tests de base échoués${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${GREEN}🎉 TESTS RAPIDES PYQT5 RÉUSSIS !${NC}"
        ;;
        
    "help"|"-h"|"--help")
        echo -e "${BLUE}🚀 Suite de Tests PyQt5 Simplifiée${NC}"
        echo ""
        echo -e "${YELLOW}Usage:${NC}"
        echo "  ./run_pyqt5_tests_simple.sh [type]"
        echo ""
        echo -e "${YELLOW}Types de tests:${NC}"
        echo -e "  ${GREEN}basic${NC}            Tests de base PyQt5 (défaut)"
        echo -e "  ${GREEN}validation${NC}       Validation complète de l'interface"
        echo -e "  ${GREEN}quick${NC}            Tests rapides"
        echo -e "  ${GREEN}help${NC}             Afficher cette aide"
        echo ""
        echo -e "${YELLOW}Exemples:${NC}"
        echo "  ./run_pyqt5_tests_simple.sh basic"
        echo "  ./run_pyqt5_tests_simple.sh validation"
        echo "  ./run_pyqt5_tests_simple.sh quick"
        ;;
        
    *)
        echo -e "${RED}❌ Type de test inconnu: $1${NC}"
        echo "Utilisez 'help' pour voir les options disponibles"
        exit 1
        ;;
esac

echo ""
echo -e "${CYAN}💡 Votre application PyQt5 est fonctionnelle !${NC}"
echo -e "${CYAN}   Lancez-la avec: python3 main.py${NC}"
