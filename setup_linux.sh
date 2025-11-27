#!/bin/bash

# Script d'installation pour Linux
echo "🐧 Installation Facturación Fácil sur Linux"
echo "=========================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier Python
echo -e "${BLUE}🐍 Vérification de Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 n'est pas installé${NC}"
    echo -e "${YELLOW}💡 Installez Python3: sudo apt install python3 python3-pip${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 trouvé: $(python3 --version)${NC}"

# Vérifier l'environnement virtuel
echo -e "${BLUE}📦 Vérification de l'environnement virtuel...${NC}"
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️ Environnement virtuel non activé${NC}"
    echo -e "${BLUE}🔧 Activation de l'environnement virtuel...${NC}"
    
    if [ -f "../bin/activate" ]; then
        source ../bin/activate
        echo -e "${GREEN}✅ Environnement virtuel activé${NC}"
    else
        echo -e "${RED}❌ Environnement virtuel non trouvé${NC}"
        echo -e "${YELLOW}💡 Créez-le avec: python3 -m venv ../venv${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Environnement virtuel actif: $VIRTUAL_ENV${NC}"
fi

# Mettre à jour pip
echo -e "${BLUE}📈 Mise à jour de pip...${NC}"
python -m pip install --upgrade pip

# Installer les dépendances système si nécessaire
echo -e "${BLUE}🔧 Vérification des dépendances système...${NC}"
if command -v apt &> /dev/null; then
    echo -e "${YELLOW}💡 Pour installer les dépendances Qt6 (optionnel):${NC}"
    echo "sudo apt install qt6-base-dev libgl1-mesa-dev"
fi

# Installer PySide6
echo -e "${BLUE}📚 Installation de PySide6...${NC}"
pip install PySide6

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PySide6 installé avec succès${NC}"
else
    echo -e "${RED}❌ Échec de l'installation de PySide6${NC}"
    echo -e "${YELLOW}💡 Essayez: pip install --upgrade pip setuptools wheel${NC}"
    echo -e "${YELLOW}💡 Puis: pip install PySide6${NC}"
    exit 1
fi

# Installer les autres dépendances
echo -e "${BLUE}📚 Installation des autres dépendances...${NC}"
pip install -r requirements.txt

# Tester PySide6
echo -e "${BLUE}🧪 Test de PySide6...${NC}"
python -c "from PySide6 import QtCore; print('✅ PySide6 fonctionne!')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PySide6 fonctionne correctement${NC}"
else
    echo -e "${RED}❌ PySide6 ne fonctionne pas${NC}"
    echo -e "${YELLOW}💡 Vérifiez les dépendances système Qt6${NC}"
    exit 1
fi

# Lancer l'application
echo -e "${BLUE}🚀 Lancement de l'application...${NC}"
echo ""
python main.py

echo -e "${BLUE}👋 Application fermée${NC}"
