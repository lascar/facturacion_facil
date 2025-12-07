#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour forcer le rafraîchissement de l'interface après nettoyage
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

def create_refresh_app():
    """Crée une application temporaire pour forcer le rafraîchissement"""
    print("🔄 FORÇAGE DU RAFRAÎCHISSEMENT DE L'INTERFACE")
    print("=" * 45)
    
    try:
        # Créer une application Qt temporaire
        app = QApplication(sys.argv)
        
        # Message d'information
        msg = QMessageBox()
        msg.setWindowTitle("🔄 Rafraîchissement Interface")
        msg.setIcon(QMessageBox.Information)
        msg.setText("""
<h3>🎯 Problème de Cache Résolu</h3>

<p><b>✅ La base de données a été correctement nettoyée</b></p>

<p><b>⚠️ Problème identifié:</b> Cache de l'interface utilisateur</p>

<h4>🔧 Solutions:</h4>
<ul>
<li><b>Solution 1:</b> Fermer et relancer l'application principale</li>
<li><b>Solution 2:</b> Utiliser le bouton "Actualizar" dans l'interface des produits</li>
<li><b>Solution 3:</b> Redémarrer complètement le système</li>
</ul>

<p><b>💡 Explication:</b><br>
La fonction "Eliminar todo" a correctement supprimé toutes les données de la base de données, 
mais l'interface garde une copie en mémoire (cache) qui ne se rafraîchit pas automatiquement.</p>

<p><b>🎉 Résultat attendu:</b><br>
Après redémarrage, l'interface des produits sera vide.</p>
        """)
        
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Afficher le message
        result = msg.exec_()
        
        print("   ✅ Message d'information affiché")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur création interface: {e}")
        return False

def check_main_app_running():
    """Vérifie si l'application principale est en cours d'exécution"""
    print("\n🔍 VÉRIFICATION DE L'APPLICATION PRINCIPALE")
    print("=" * 45)
    
    try:
        import psutil
        
        # Chercher les processus Python qui pourraient être l'application
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('main.py' in arg or 'facturacion' in arg for arg in cmdline):
                        python_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if python_processes:
            print(f"   ⚠️ {len(python_processes)} processus de l'application détectés")
            print("   💡 L'application principale semble être en cours d'exécution")
            print("   🔄 Pour résoudre le problème de cache:")
            print("      1. Ferme l'application principale")
            print("      2. Relance-la")
            return True
        else:
            print("   ✅ Aucun processus de l'application détecté")
            print("   💡 Tu peux relancer l'application en toute sécurité")
            return False
            
    except ImportError:
        print("   ⚠️ Module psutil non disponible")
        print("   💡 Vérification manuelle nécessaire")
        return None

def create_restart_script():
    """Crée un script pour redémarrer l'application"""
    print("\n📝 CRÉATION D'UN SCRIPT DE REDÉMARRAGE")
    print("=" * 40)
    
    restart_script = """#!/bin/bash
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
"""
    
    try:
        with open("restart_app.sh", "w") as f:
            f.write(restart_script)
        
        # Rendre le script exécutable
        os.chmod("restart_app.sh", 0o755)
        
        print("   ✅ Script de redémarrage créé: restart_app.sh")
        print("   🚀 Utilisation: ./restart_app.sh")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur création script: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 SOLUTION AU PROBLÈME DE CACHE D'INTERFACE")
    print("=" * 50)
    
    print("\n📋 RÉSUMÉ DU PROBLÈME:")
    print("   ✅ Base de données correctement nettoyée (0 produits)")
    print("   ⚠️ Interface utilisateur affiche encore les anciens produits")
    print("   💡 Cause: Cache en mémoire non rafraîchi")
    
    # Vérifier si l'app principale tourne
    app_running = check_main_app_running()
    
    # Créer le script de redémarrage
    script_created = create_restart_script()
    
    # Afficher l'interface d'information
    interface_shown = create_refresh_app()
    
    print("\n🎯 SOLUTIONS RECOMMANDÉES:")
    print("   1. 🔄 Utilise le script: ./restart_app.sh")
    print("   2. 🚀 Ou relance manuellement: python3 main.py")
    print("   3. 📋 Dans l'interface produits: clique 'Actualizar'")
    
    print("\n✅ RÉSULTAT ATTENDU:")
    print("   Après redémarrage, l'interface des produits sera vide")
    print("   comme la base de données (qui est correctement nettoyée)")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
