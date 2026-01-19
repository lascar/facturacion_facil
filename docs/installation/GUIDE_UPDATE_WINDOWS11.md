# 🔄 Guide de Mise à Jour - Windows 11

## 🎯 Vue d'ensemble

Ce guide explique comment mettre à jour ton application **Facturación Fácil** sur Windows 11 après avoir fait des modifications ou reçu des mises à jour.

## 📋 Prérequis

- ✅ Application déjà installée (voir `INSTALLATION_WINDOWS11.md`)
- ✅ Git installé sur ton système
- ✅ Connexion Internet active
- ✅ Droits d'administrateur (si nécessaire)

## 🚀 Méthodes de mise à jour

### **Méthode 1 : Mise à jour automatique (Recommandée)**

#### **Étape 1 : Script de mise à jour automatique**
```batch
# Double-cliquer sur le fichier
update.bat
```

#### **Étape 2 : Vérification**
Le script va :
- 🔄 Télécharger les dernières modifications
- 📦 Mettre à jour les dépendances si nécessaire
- 🧪 Tester que tout fonctionne
- ✅ Confirmer la mise à jour

### **Méthode 2 : Mise à jour manuelle**

#### **Étape 1 : Ouvrir le terminal**
```batch
# Appuyer sur Win + R, taper "cmd", puis Entrée
cd C:\chemin\vers\facturacion_facil
```

#### **Étape 2 : Sauvegarder les données (optionnel)**
```batch
# Copier la base de données
copy facturacion.db facturacion_backup_%date%.db
```

#### **Étape 3 : Télécharger les mises à jour**
```batch
# Récupérer les dernières modifications
git pull origin main
```

#### **Étape 4 : Mettre à jour les dépendances**
```batch
# Activer l'environnement virtuel
env\Scripts\activate

# Mettre à jour les packages
pip install -r requirements.txt --upgrade
```

#### **Étape 5 : Tester l'application**
```batch
# Lancer l'application
python main.py
```

## 🔧 Scripts automatiques créés

### **Script de mise à jour : `update.bat`**
Créé automatiquement pour simplifier les mises à jour.

### **Script de diagnostic : `diagnostic_update.bat`**
Vérifie l'état avant et après mise à jour.

### **Script de sauvegarde : `backup.bat`**
Sauvegarde automatique des données importantes.

## 📊 Types de mises à jour

### **🔹 Mise à jour mineure (Corrections de bugs)**
- Corrections de petits problèmes
- Améliorations de l'interface
- Optimisations de performance

**Procédure** : Méthode automatique recommandée

### **🔸 Mise à jour majeure (Nouvelles fonctionnalités)**
- Nouvelles fonctionnalités importantes
- Modifications de la base de données
- Changements d'interface significatifs

**Procédure** : Sauvegarde + Méthode automatique

### **🔺 Mise à jour critique (Sécurité)**
- Corrections de sécurité importantes
- Mise à jour urgente recommandée

**Procédure** : Mise à jour immédiate

## ⚠️ Précautions importantes

### **Avant la mise à jour**
1. **💾 Sauvegarde** : Toujours sauvegarder tes données
2. **🔒 Fermer l'application** : S'assurer qu'elle n'est pas en cours d'exécution
3. **📋 Noter les modifications** : Lire les notes de version

### **Pendant la mise à jour**
1. **🌐 Connexion stable** : Maintenir la connexion Internet
2. **⏳ Patience** : Ne pas interrompre le processus
3. **👀 Surveillance** : Vérifier les messages d'erreur

### **Après la mise à jour**
1. **🧪 Test** : Vérifier que tout fonctionne
2. **📊 Données** : Contrôler l'intégrité des données
3. **🔄 Redémarrage** : Redémarrer si nécessaire

## 🛠️ Résolution de problèmes

### **Problème : Git pull échoue**
```batch
# Solution 1 : Forcer la mise à jour
git reset --hard origin/main
git pull origin main
```

### **Problème : Dépendances manquantes**
```batch
# Solution : Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### **Problème : Base de données corrompue**
```batch
# Solution : Restaurer la sauvegarde
copy facturacion_backup_YYYYMMDD.db facturacion.db
```

### **Problème : Application ne démarre pas**
```batch
# Solution : Diagnostic complet
diagnostic_update.bat
```

## 📱 Notifications de mise à jour

### **Vérification automatique**
L'application peut vérifier automatiquement les mises à jour disponibles.

### **Notifications**
- 🔔 Popup de notification
- 📧 Email (si configuré)
- 📱 Message dans l'application

## 🎯 Bonnes pratiques

### **Fréquence de mise à jour**
- **Quotidienne** : Vérifier les mises à jour critiques
- **Hebdomadaire** : Appliquer les mises à jour mineures
- **Mensuelle** : Planifier les mises à jour majeures

### **Planification**
- **🕐 Heures creuses** : Faire les mises à jour quand l'application n'est pas utilisée
- **📅 Jour fixe** : Définir un jour de la semaine pour les mises à jour
- **🔄 Automatisation** : Utiliser les scripts automatiques

### **Documentation**
- **📝 Journal** : Tenir un journal des mises à jour
- **📋 Checklist** : Utiliser une checklist de vérification
- **📊 Suivi** : Suivre les performances après mise à jour

## 🎉 Avantages des mises à jour régulières

### **Sécurité**
- 🛡️ Corrections de vulnérabilités
- 🔒 Améliorations de sécurité
- 🚫 Protection contre les menaces

### **Performance**
- ⚡ Optimisations de vitesse
- 💾 Gestion mémoire améliorée
- 🔧 Corrections de bugs

### **Fonctionnalités**
- ✨ Nouvelles fonctionnalités
- 🎨 Améliorations d'interface
- 🔧 Outils supplémentaires

## 📞 Support

### **En cas de problème**
1. **📖 Consulter** ce guide
2. **🔍 Vérifier** les logs d'erreur
3. **🛠️ Utiliser** les scripts de diagnostic
4. **📧 Contacter** le support si nécessaire

### **Ressources utiles**
- `INSTALLATION_WINDOWS11.md` - Guide d'installation
- `README_WINDOWS.md` - Documentation principale
- `diagnostic_python.bat` - Diagnostic système
- `DEMARRAGE_RAPIDE_WINDOWS.md` - Démarrage rapide

**Mise à jour réussie = Application plus stable et sécurisée !** 🚀
