#!/bin/bash
# Script de redémarrage de l'application

echo "🔄 Redémarrage de l'application facturacion_facil"
echo "=" * 45

# Tuer les processus existants (optionnel)
echo "🛑 Arrêt des processus existants..."
pkill -f "python.*main.py" 2>/dev/null || true
pkill -f "python.*facturacion" 2>/dev/null || true

# Attendre un peu
sleep 2

# Relancer l'application
echo "🚀 Relancement de l'application..."
cd "$(dirname "$0")"
python3 main.py

echo "✅ Application relancée"
