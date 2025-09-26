#!/bin/bash
# Script pour organiser automatiquement la documentation
# Maintient la structure docs/ organisée

set -e

echo "🗂️ Organisation automatique de la documentation"
echo "================================================"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Répertoire racine du projet
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Répertoire de travail:${NC} $PROJECT_ROOT"

# Créer la structure docs/ si elle n'existe pas
echo -e "\n${BLUE}🏗️ Création de la structure docs/...${NC}"
mkdir -p docs/{architecture,features,fixes,implementation}

# Fonction pour déplacer des fichiers avec vérification
move_files() {
    local pattern="$1"
    local destination="$2"
    local description="$3"
    
    # Trouver les fichiers correspondant au pattern à la racine
    files=$(find . -maxdepth 1 -name "$pattern" -type f 2>/dev/null || true)
    
    if [ -n "$files" ]; then
        echo -e "\n${YELLOW}📝 Déplacement: $description${NC}"
        for file in $files; do
            filename=$(basename "$file")
            if [ "$filename" != "README.md" ]; then
                echo "   $filename -> docs/$destination/"
                mv "$file" "docs/$destination/"
            fi
        done
    fi
}

# Organiser les fichiers par catégorie
echo -e "\n${BLUE}📋 Organisation par catégories...${NC}"

# Architecture
move_files "*ARCHITECTURE*.md" "architecture" "Architecture et factorisation"
move_files "*FACTORIZATION*.md" "architecture" "Factorisation du code"

# Fonctionnalités
move_files "*FEATURE*.md" "features" "Nouvelles fonctionnalités"
move_files "*IMPLEMENTATION_SUMMARY.md" "features" "Résumés d'implémentation"
move_files "*NUMBERING*.md" "features" "Numérotation"
move_files "*PDF_AND_*.md" "features" "Fonctionnalités PDF"
move_files "*INTEGRATION*.md" "features" "Intégrations"
move_files "*COPYABLE*.md" "features" "Messages copiables"

# Corrections
move_files "*FIX*.md" "fixes" "Corrections de bugs"
move_files "*CORRECCION*.md" "fixes" "Corrections"
move_files "*CORRECION*.md" "fixes" "Corrections (variante)"
move_files "*ERROR*.md" "fixes" "Corrections d'erreurs"
move_files "*SCROLL*.md" "fixes" "Corrections de scroll"
move_files "*FOCUS*.md" "fixes" "Corrections de focus"
move_files "*TCLERROR*.md" "fixes" "Corrections TclError"
move_files "*DIALOG*.md" "fixes" "Corrections de dialogues"
move_files "*MOUSE*.md" "fixes" "Corrections souris"

# Implémentation
move_files "*IMPLEMENTATION.md" "implementation" "Détails d'implémentation"
move_files "*IMPLEMENTACION*.md" "implementation" "Implémentation (ES)"
move_files "*RESUMEN.md" "implementation" "Résumés d'implémentation"
move_files "*STOCK_IMPLEMENTATION*.md" "implementation" "Implémentation stock"
move_files "*FACTURAS_IMPLEMENTATION*.md" "implementation" "Implémentation factures"

# Vérifier les fichiers restants à la racine
echo -e "\n${BLUE}🔍 Vérification des fichiers MD à la racine...${NC}"
remaining_md=$(find . -maxdepth 1 -name "*.md" -type f | grep -v "./README.md" || true)

if [ -n "$remaining_md" ]; then
    echo -e "${YELLOW}⚠️ Fichiers MD restants à la racine:${NC}"
    for file in $remaining_md; do
        echo "   $(basename "$file")"
    done
    
    # Déplacer les fichiers généraux vers docs/
    for file in $remaining_md; do
        filename=$(basename "$file")
        echo "   $filename -> docs/"
        mv "$file" "docs/"
    done
else
    echo -e "${GREEN}✅ Seul README.md reste à la racine${NC}"
fi

# Statistiques finales
echo -e "\n${BLUE}📊 Statistiques de la documentation:${NC}"
echo "   📁 Architecture: $(find docs/architecture -name "*.md" 2>/dev/null | wc -l) fichiers"
echo "   ✨ Fonctionnalités: $(find docs/features -name "*.md" 2>/dev/null | wc -l) fichiers"
echo "   🔧 Corrections: $(find docs/fixes -name "*.md" 2>/dev/null | wc -l) fichiers"
echo "   🛠️ Implémentation: $(find docs/implementation -name "*.md" 2>/dev/null | wc -l) fichiers"
echo "   📚 Général: $(find docs -maxdepth 1 -name "*.md" 2>/dev/null | wc -l) fichiers"

total_docs=$(find docs -name "*.md" 2>/dev/null | wc -l)
echo -e "\n${GREEN}📈 Total: $total_docs documents organisés${NC}"

# Vérifier l'index de documentation
if [ ! -f "docs/README.md" ]; then
    echo -e "\n${YELLOW}⚠️ Création de l'index de documentation...${NC}"
    cat > docs/README.md << 'EOF'
# 📚 Documentation - Facturación Fácil

## 🗂️ Organisation de la Documentation

Cette documentation est organisée par catégories :

- **[architecture/](architecture/)** - Architecture et factorisation du code
- **[features/](features/)** - Nouvelles fonctionnalités implémentées  
- **[fixes/](fixes/)** - Corrections et résolutions de bugs
- **[implementation/](implementation/)** - Détails d'implémentation

Consultez les répertoires spécialisés selon vos besoins.
EOF
    echo -e "${GREEN}✅ Index créé: docs/README.md${NC}"
fi

echo -e "\n${GREEN}🎉 Organisation de la documentation terminée !${NC}"
echo -e "${BLUE}💡 Conseil:${NC} Consultez docs/README.md pour naviguer dans la documentation"
