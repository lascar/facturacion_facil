#!/bin/bash
# Script pour activer l'environnement virtuel Python 3.13.7

echo "🐍 Activation de l'environnement virtuel Python 3.13.7..."
echo "📁 Répertoire: $(pwd)"
echo ""

# Activer l'environnement virtuel
source ../bin/activate

echo "✅ Environnement activé !"
echo "🐍 Python version: $(python --version)"
echo "📦 pip version: $(pip --version)"
echo ""
echo "💡 Pour désactiver l'environnement, tapez: deactivate"
echo "🚀 Pour lancer l'application: python main.py"
echo "🧪 Pour lancer les tests: pytest"
echo ""
