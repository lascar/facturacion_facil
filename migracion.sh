#!/bin/bash
# Script de migration pour Linux
# Importe les produits depuis 'Productos tienda.xls' vers la table 'products_shop'

echo ""
echo "========================================================================"
echo "MIGRATION DE PRODUCTOS TIENDA"
echo "========================================================================"
echo ""

# Détecter Python (pyenv ou système)
PYTHON_CMD=""
if [ -f "$HOME/.pyenv/shims/python" ]; then
    PYTHON_CMD="$HOME/.pyenv/shims/python"
    echo "✅ Python trouvé (pyenv): $($PYTHON_CMD --version)"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python trouvé (système): $($PYTHON_CMD --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ Python trouvé: $($PYTHON_CMD --version)"
else
    echo "❌ ERREUR: Python n'est pas installé"
    exit 1
fi

# Vérifier que xlrd est installé
if ! $PYTHON_CMD -c "import xlrd" &> /dev/null; then
    echo "📦 Installation du module xlrd..."
    $PYTHON_CMD -m pip install xlrd
    if [ $? -ne 0 ]; then
        echo "❌ ERREUR: Impossible d'installer xlrd"
        exit 1
    fi
    echo "✅ xlrd installé"
fi

# Exécuter le script de migration
echo "🚀 Exécution de la migration..."
echo ""
$PYTHON_CMD migracion_productos_shop.py

MIGRATION_EXIT_CODE=$?

if [ $MIGRATION_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Migration terminée avec succès!"
    exit 0
else
    echo ""
    echo "❌ ERREUR: La migration a échoué"
    exit 1
fi

