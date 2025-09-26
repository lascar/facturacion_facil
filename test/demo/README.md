# 🎯 Démonstrations

## 📋 **Description**
Scripts de démonstration des fonctionnalités - présentation interactive des capacités du système.

## 📁 **Contenu du Répertoire**
```
demo/
├── README.md                           # Ce guide
├── demo_pdf_download_feature.py        # Démo fonctionnalité PDF
├── demo_visor_pdf_personalizado.py     # Démo visor PDF personnalisé
├── demo_mini_images_facturas.py        # Démo mini images facturas
├── demo_mousewheel_scroll.py           # Démo scroll molette
└── demo_logo_persistence_fix.py        # Démo correction persistance logo
```

## 🚀 **Exécution des Démonstrations**

### **Toutes les Démonstrations**
```bash
# Depuis la racine du projet
./run_organized_tests.sh demo

# Exécution séquentielle de toutes les démos
for demo in test/demo/demo_*.py; do
    echo "=== $(basename $demo) ==="
    python3 "$demo"
    echo ""
done
```

### **Démonstrations Individuelles**
```bash
# Démo fonctionnalité PDF
python3 test/demo/demo_pdf_download_feature.py

# Démo visor PDF personnalisé
python3 test/demo/demo_visor_pdf_personalizado.py

# Démo mini images dans facturas
python3 test/demo/demo_mini_images_facturas.py

# Démo scroll molette
python3 test/demo/demo_mousewheel_scroll.py
```

### **Démonstrations avec Options**
```bash
# Mode verbose (si supporté)
python3 test/demo/demo_pdf_download_feature.py --verbose

# Mode interactif (si supporté)
python3 test/demo/demo_mini_images_facturas.py --interactive

# Mode debug
python3 test/demo/demo_visor_pdf_personalizado.py --debug
```

## 📊 **Statistiques**
- **Nombre de démos** : 4 démonstrations
- **Couverture** : PDF, images, interface, scroll
- **Type** : Démonstrations interactives et automatiques
- **Temps d'exécution** : ~30-60 secondes par démo

## 🎯 **Objectifs des Démonstrations**

### **Présentation des Fonctionnalités**
- Montrer les capacités du système
- Valider le fonctionnement en conditions réelles
- Documenter l'utilisation pratique
- Faciliter la compréhension

### **Validation Utilisateur**
- Tests d'acceptation
- Feedback utilisateur
- Validation ergonomique
- Démonstration client

## 🔧 **Description des Démonstrations**

### **demo_pdf_download_feature.py**
```bash
# Démonstration complète de la fonctionnalité PDF
python3 test/demo/demo_pdf_download_feature.py
```

**Fonctionnalités démontrées :**
- Configuration répertoire PDF par défaut
- Génération de PDFs avec ouverture automatique
- Système de fallback robuste
- Conservation des préférences utilisateur
- Interface d'organisation améliorée

**Scénario :**
1. Configuration organisation avec répertoire PDF
2. Création de données de démonstration
3. Génération PDF avec ouverture automatique
4. Test du système de fallback
5. Présentation de l'interface utilisateur

### **demo_visor_pdf_personalizado.py**
```bash
# Démonstration du visor PDF personnalisé
python3 test/demo/demo_visor_pdf_personalizado.py
```

**Fonctionnalités démontrées :**
- Détection automatique des visors PDF disponibles
- Configuration visor personnalisé
- Système de fallback vers visor système
- Conservation des préférences
- Compatibilité multi-plateforme

**Scénario :**
1. Détection des visors PDF sur le système
2. Configuration visor personnalisé
3. Génération PDF avec visor configuré
4. Test de différents visors
5. Validation du système de fallback

### **demo_mini_images_facturas.py**
```bash
# Démonstration des mini images dans facturas
python3 test/demo/demo_mini_images_facturas.py
```

**Fonctionnalités démontrées :**
- Affichage mini images dans lignes de facture
- Cache intelligent pour performance
- Placeholder pour produits sans image
- Interface moderne et visuelle
- Optimisation automatique des images

**Scénario :**
1. Création d'images de test
2. Création de produits avec/sans images
3. Test des utilitaires d'image
4. Création factura avec mini images
5. Simulation interface avec images
6. Test du cache de performance

### **demo_mousewheel_scroll.py**
```bash
# Démonstration du scroll molette
python3 test/demo/demo_mousewheel_scroll.py
```

**Fonctionnalités démontrées :**
- Scroll avec molette de souris
- Navigation fluide dans les interfaces
- Compatibilité avec différents widgets
- Amélioration ergonomique

**Scénario :**
1. Création interface avec scroll
2. Test navigation molette
3. Validation fluidité
4. Démonstration ergonomie

## 🚀 **Exécution Avancée**

### **Démonstrations en Mode Présentation**
```bash
# Mode présentation (plein écran si supporté)
python3 test/demo/demo_mini_images_facturas.py --presentation

# Mode silencieux (sans interaction)
python3 test/demo/demo_pdf_download_feature.py --silent

# Mode pas-à-pas
python3 test/demo/demo_visor_pdf_personalizado.py --step-by-step
```

### **Démonstrations avec Données Personnalisées**
```bash
# Avec données spécifiques
python3 test/demo/demo_mini_images_facturas.py --data-set=custom

# Avec configuration particulière
python3 test/demo/demo_pdf_download_feature.py --config=demo.conf

# Mode développeur
python3 test/demo/demo_visor_pdf_personalizado.py --dev-mode
```

### **Démonstrations pour Différents Publics**
```bash
# Mode utilisateur final
python3 test/demo/demo_mini_images_facturas.py --user-mode

# Mode technique
python3 test/demo/demo_pdf_download_feature.py --technical

# Mode commercial
python3 test/demo/demo_visor_pdf_personalizado.py --commercial
```

## 🔧 **Configuration des Démonstrations**

### **Variables d'Environnement**
```bash
# Mode démonstration
export DEMO_MODE=1

# Répertoires de démonstration
export DEMO_DATA_DIR="/tmp/demo_data"
export DEMO_OUTPUT_DIR="/tmp/demo_output"

# Configuration affichage
export DEMO_DISPLAY_MODE=interactive
export DEMO_SPEED=normal

# Logs de démonstration
export DEMO_LOG_LEVEL=INFO
```

### **Prérequis**
```bash
# Environnement virtuel activé
source ../bin/activate

# Interface graphique disponible (pour certaines démos)
echo $DISPLAY

# Répertoires temporaires
mkdir -p /tmp/demo_data /tmp/demo_output

# Permissions appropriées
chmod 755 /tmp/demo_*
```

## 🎯 **Utilisation des Démonstrations**

### **Pour Développeurs**
```bash
# Validation fonctionnalités
python3 test/demo/demo_mini_images_facturas.py

# Test intégration
python3 test/demo/demo_pdf_download_feature.py

# Debug interface
python3 test/demo/demo_mousewheel_scroll.py --debug
```

### **Pour Utilisateurs Finaux**
```bash
# Découverte fonctionnalités
./run_organized_tests.sh demo

# Apprentissage interface
python3 test/demo/demo_mini_images_facturas.py --tutorial

# Validation besoins
python3 test/demo/demo_pdf_download_feature.py --user-mode
```

### **Pour Présentations Client**
```bash
# Démonstration complète
./run_organized_tests.sh demo --presentation

# Fonctionnalités spécifiques
python3 test/demo/demo_visor_pdf_personalizado.py --commercial

# Mode interactif
python3 test/demo/demo_mini_images_facturas.py --interactive
```

## 🐛 **Dépannage**

### **Démonstrations qui Échouent**
```bash
# Mode debug
python3 test/demo/demo_specific.py --debug --verbose

# Vérifier prérequis
python3 test/demo/demo_specific.py --check-requirements

# Logs détaillés
python3 test/demo/demo_specific.py --log-level=DEBUG
```

### **Problèmes d'Interface**
```bash
# Vérifier affichage
echo $DISPLAY
xdpyinfo | head

# Mode headless si nécessaire
xvfb-run python3 test/demo/demo_mini_images_facturas.py

# Skip éléments graphiques
python3 test/demo/demo_specific.py --no-gui
```

### **Données de Démonstration**
```bash
# Nettoyer données précédentes
rm -rf /tmp/demo_*

# Recréer environnement
mkdir -p /tmp/demo_data /tmp/demo_output

# Vérifier permissions
ls -la /tmp/demo_*
```

## 📈 **Métriques des Démonstrations**

### **Indicateurs de Succès**
- **Exécution complète** : 100% des étapes
- **Temps d'exécution** : <60 secondes par démo
- **Stabilité** : Pas d'erreurs
- **Clarté** : Messages informatifs

### **Feedback Utilisateur**
- **Compréhension** : Fonctionnalités claires
- **Ergonomie** : Interface intuitive
- **Performance** : Réactivité acceptable
- **Utilité** : Valeur ajoutée évidente

## 🔄 **Maintenance des Démonstrations**

### **Mise à Jour des Démonstrations**
```python
#!/usr/bin/env python3
"""
Template pour nouvelle démonstration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def main():
    """Démonstration de nouvelle fonctionnalité"""
    print("🎯 === DÉMONSTRATION NOUVELLE FONCTIONNALITÉ ===")
    print()
    
    # Étapes de démonstration
    print("1️⃣ Étape 1: Description")
    # Code de démonstration
    
    print("✅ Démonstration terminée avec succès!")

if __name__ == "__main__":
    main()
```

### **Bonnes Pratiques**
- **Messages clairs** : Descriptions étape par étape
- **Émojis** : Rendre visuellement attrayant
- **Gestion d'erreurs** : Fallback gracieux
- **Nettoyage** : Suppression fichiers temporaires
- **Documentation** : Commentaires explicatifs

### **Évolution des Démonstrations**
- Adapter aux nouvelles fonctionnalités
- Maintenir la cohérence visuelle
- Optimiser les temps d'exécution
- Améliorer l'expérience utilisateur

## 📋 **Checklist Démonstrations**

### **Avant Présentation**
- [ ] Toutes les démos s'exécutent sans erreur
- [ ] Données de test préparées
- [ ] Environnement configuré
- [ ] Interface graphique disponible

### **Pendant Présentation**
- [ ] Messages clairs et informatifs
- [ ] Temps d'exécution raisonnable
- [ ] Pas d'erreurs visibles
- [ ] Résultats cohérents

### **Après Présentation**
- [ ] Nettoyage des fichiers temporaires
- [ ] Feedback collecté
- [ ] Améliorations identifiées
- [ ] Documentation mise à jour

---

**🎯 Note** : Les démonstrations sont des outils de communication. Elles doivent être claires, stables et impressionnantes.

**Pour plus d'informations, consultez le guide principal : `../README.md`**
