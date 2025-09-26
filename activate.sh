#!/bin/bash
# Script simple pour activer l'environnement virtuel
# Utilisation: source ./activate.sh

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐍 Activation de l'environnement virtuel...${NC}"

# Vérifier si l'environnement virtuel existe
if [ ! -f "../bin/activate" ]; then
    echo -e "${RED}❌ Erreur: Environnement virtuel non trouvé${NC}"
    echo -e "${YELLOW}💡 Créez l'environnement avec: python -m venv ../${NC}"
    return 1 2>/dev/null || exit 1
fi

# Activer l'environnement virtuel
source ../bin/activate

# Vérifier que l'activation a réussi
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✅ Environnement activé !${NC}"
    echo -e "${BLUE}🐍 Python: $(which python)${NC}"
    echo -e "${BLUE}📦 Version: $(python --version)${NC}"
    echo ""
    echo -e "${YELLOW}💡 Commandes utiles:${NC}"
    echo "   🚀 Lancer l'app: python main.py"
    echo "   🧪 Tous les tests: ./run_organized_tests.sh all"
    echo "   🔧 Tests unitaires: ./run_organized_tests.sh unit"
    echo "   ❌ Désactiver: deactivate"
else
    echo -e "${RED}❌ Erreur: L'activation a échoué${NC}"
    return 1
fi
