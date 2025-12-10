#!/bin/bash
# -*- coding: utf-8 -*-
# Script de sauvegarde pour Facturación Fácil - Version Linux

echo "========================================"
echo "💾 SAUVEGARDE - FACTURACIÓN FÁCIL"
echo "========================================"

# Générer un nom de backup avec timestamp
backup_name="backup_$(date +%Y%m%d_%H%M%S)"

# Créer le répertoire de backup s'il n'existe pas
mkdir -p "../base_de_datos/backups"

echo ""
echo "📅 Date: $(date)"
echo "📝 Nom du backup: $backup_name"
echo ""

# Sauvegarder la base de données
if [ -f "../base_de_datos/facturacion.db" ]; then
    echo "💾 Sauvegarde de la base de données..."
    cp "../base_de_datos/facturacion.db" "../base_de_datos/backups/${backup_name}_facturacion.db"
    if [ $? -eq 0 ]; then
        echo "   ✅ Base de données sauvegardée"
    else
        echo "   ❌ Erreur lors de la sauvegarde de la base"
        exit 1
    fi
else
    echo "   ⚠️  Base de données non trouvée: ../base_de_datos/facturacion.db"
fi

# Sauvegarder les fichiers de configuration
if [ -d "../config" ]; then
    echo "📋 Sauvegarde de la configuration..."
    cp -r "../config" "../base_de_datos/backups/${backup_name}_config"
    if [ $? -eq 0 ]; then
        echo "   ✅ Configuration sauvegardée"
    else
        echo "   ❌ Erreur lors de la sauvegarde de la config"
    fi
else
    echo "   ⚠️  Répertoire config non trouvé"
fi

echo ""
echo "✅ SAUVEGARDE TERMINÉE"
echo "📁 Fichiers créés dans: base_de_datos/backups/"
echo "   - ${backup_name}_facturacion.db"
echo "   - ${backup_name}_config/"
echo ""
echo "Appuyez sur Entrée pour continuer..."
read
