#!/bin/bash
# Script pour activer l'environnement virtuel Python 3.13.7
# IMPORTANT: Ce script doit être sourcé, pas exécuté !
# Utilisation: source ./activate_env.sh

echo "🐍 Activation de l'environnement virtuel Python 3.13.7..."
echo "📁 Répertoire: $(pwd)"

# Vérifier si l'environnement virtuel existe
if [ ! -f "../bin/activate" ]; then
    echo "❌ Erreur: Environnement virtuel non trouvé dans ../bin/activate"
    echo "💡 Créez l'environnement avec: python -m venv ../venv"
    return 1 2>/dev/null || exit 1
fi

# Vérifier si le script est sourcé (pas exécuté)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "❌ Erreur: Ce script doit être sourcé, pas exécuté !"
    echo "💡 Utilisation correcte: source ./activate_env.sh"
    echo "💡 Ou: . ./activate_env.sh"
    exit 1
fi

echo "🔧 Activation en cours..."

# Activer l'environnement virtuel
source ../bin/activate

# Vérifier que l'activation a réussi
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Environnement activé avec succès !"
    echo "📁 Environnement virtuel: $VIRTUAL_ENV"
    echo "🐍 Python version: $(python --version)"
    echo "📦 pip version: $(pip --version)"
    echo "📍 Python path: $(which python)"
    echo ""
    echo "💡 Pour désactiver l'environnement, tapez: deactivate"
    echo "🚀 Pour lancer l'application: python main.py"
    echo "🧪 Pour lancer les tests: ./run_organized_tests.sh all"
    echo "🧪 Pour lancer les tests (pytest direct): pytest test/"
    echo "🎭 Pour lancer les tests de comportement: pytest test/behaviour/ -v -s"
else
    echo "❌ Erreur: L'activation de l'environnement virtuel a échoué"
    echo "💡 Vérifiez que l'environnement virtuel est correctement installé"
    return 1
fi
