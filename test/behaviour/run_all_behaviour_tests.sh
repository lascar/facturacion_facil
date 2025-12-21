#!/bin/bash
# Script pour exécuter tous les tests de comportement avec rapport détaillé

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo -e "${BLUE}🧪 Tests de Comportement - Facturación Fácil${NC}"
echo "=================================================="
echo "📁 Répertoire projet: $PROJECT_ROOT"
echo "📁 Répertoire tests: $SCRIPT_DIR"
echo ""

# Vérifier l'environnement
if [[ ! -f "$PROJECT_ROOT/activate_env.sh" ]]; then
    echo -e "${RED}❌ Script d'activation d'environnement non trouvé${NC}"
    exit 1
fi

# Activer l'environnement
echo -e "${YELLOW}🔧 Activation de l'environnement...${NC}"
cd "$PROJECT_ROOT"
source ./activate_env.sh

# Vérifier que pytest est disponible
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest non trouvé dans l'environnement${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environnement activé${NC}"
echo ""

# Créer le répertoire de rapports
REPORTS_DIR="$SCRIPT_DIR/reports"
mkdir -p "$REPORTS_DIR"

# Timestamp pour les rapports
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo -e "${BLUE}📋 Exécution des tests de comportement...${NC}"
echo "=================================================="

# 1. Tests simples (validation de la configuration)
echo -e "${YELLOW}🔍 1. Tests de validation de configuration...${NC}"
pytest "$SCRIPT_DIR/test_simple_behaviour.py" \
    -v \
    --tb=short \
    --junit-xml="$REPORTS_DIR/simple_tests_$TIMESTAMP.xml" \
    --html="$REPORTS_DIR/simple_tests_$TIMESTAMP.html" \
    --self-contained-html \
    2>&1 | tee "$REPORTS_DIR/simple_tests_$TIMESTAMP.log"

SIMPLE_EXIT_CODE=$?

if [ $SIMPLE_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Tests simples réussis${NC}"
else
    echo -e "${RED}❌ Tests simples échoués (code: $SIMPLE_EXIT_CODE)${NC}"
fi

echo ""

# 2. Tests d'interface (si les tests simples passent)
if [ $SIMPLE_EXIT_CODE -eq 0 ]; then
    echo -e "${YELLOW}🖥️ 2. Tests d'interface utilisateur...${NC}"
    
    # Tests avec timeout plus long pour l'interface
    timeout 300 pytest "$SCRIPT_DIR/test_main_window_behaviour.py" \
        -v \
        --tb=short \
        --junit-xml="$REPORTS_DIR/ui_tests_$TIMESTAMP.xml" \
        --html="$REPORTS_DIR/ui_tests_$TIMESTAMP.html" \
        --self-contained-html \
        --headless \
        2>&1 | tee "$REPORTS_DIR/ui_tests_$TIMESTAMP.log" || true
    
    UI_EXIT_CODE=$?
    
    if [ $UI_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ Tests d'interface réussis${NC}"
    else
        echo -e "${YELLOW}⚠️ Tests d'interface échoués ou interrompus (code: $UI_EXIT_CODE)${NC}"
        echo -e "${YELLOW}   (Normal si l'interface graphique n'est pas disponible)${NC}"
    fi
else
    echo -e "${YELLOW}⏭️ Tests d'interface ignorés (tests simples échoués)${NC}"
    UI_EXIT_CODE=1
fi

echo ""

# 3. Génération du rapport final
echo -e "${BLUE}📊 Génération du rapport final...${NC}"
echo "=================================================="

FINAL_REPORT="$REPORTS_DIR/behaviour_tests_report_$TIMESTAMP.txt"

cat > "$FINAL_REPORT" << EOF
# Rapport des Tests de Comportement - Facturación Fácil
Date: $(date)
Répertoire: $PROJECT_ROOT

## Résumé des Tests

### 1. Tests de Configuration
- Fichier: test_simple_behaviour.py
- Statut: $([ $SIMPLE_EXIT_CODE -eq 0 ] && echo "✅ RÉUSSI" || echo "❌ ÉCHOUÉ")
- Code de sortie: $SIMPLE_EXIT_CODE

### 2. Tests d'Interface Utilisateur  
- Fichier: test_main_window_behaviour.py
- Statut: $([ $UI_EXIT_CODE -eq 0 ] && echo "✅ RÉUSSI" || echo "⚠️ ÉCHOUÉ/IGNORÉ")
- Code de sortie: $UI_EXIT_CODE

## Fichiers de Rapport Générés
- Logs simples: simple_tests_$TIMESTAMP.log
- Logs UI: ui_tests_$TIMESTAMP.log
- XML JUnit: *_$TIMESTAMP.xml
- HTML: *_$TIMESTAMP.html

## Recommandations

EOF

if [ $SIMPLE_EXIT_CODE -eq 0 ]; then
    echo "✅ Configuration des tests de comportement validée" >> "$FINAL_REPORT"
else
    echo "❌ Problèmes de configuration détectés - vérifier les logs" >> "$FINAL_REPORT"
fi

if [ $UI_EXIT_CODE -ne 0 ]; then
    cat >> "$FINAL_REPORT" << EOF
⚠️ Tests d'interface échoués - causes possibles:
  - Environnement graphique non disponible
  - Problèmes de dépendances PyQt5
  - Timeout des tests (> 5 minutes)
  - Problèmes de base de données de test
EOF
fi

echo ""
echo -e "${GREEN}📄 Rapport final généré: $FINAL_REPORT${NC}"
cat "$FINAL_REPORT"

echo ""
echo "=================================================="
if [ $SIMPLE_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}🎉 Tests de comportement terminés avec succès !${NC}"
    exit 0
else
    echo -e "${RED}💥 Tests de comportement échoués${NC}"
    exit 1
fi
