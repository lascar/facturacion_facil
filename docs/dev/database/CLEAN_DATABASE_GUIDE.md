> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🗑️ Guide d'Utilisation du Script de Nettoyage

## Script Disponible
- ✅ **`./clean_databases.sh`** - Script complet et fonctionnel
- ❌ **`cleaning_base.sh`** - Supprimé (ne fonctionnait pas)

## 🚀 Utilisation

```bash
./clean_databases.sh
```

## 📋 Options Disponibles

### 1️⃣ Eliminar TODAS las bases de datos (⚠️ PELIGROSO)
- **Action** : Supprime toutes les bases de données (.db)
- **Confirmation** : Tape "SI" pour confirmer
- **Usage** : Nettoyage complet du projet

### 2️⃣ Limpiar solo el CONTENIDO de la base principal
- **Action** : Vide les tables mais garde la structure
- **Confirmation** : Tape "SI" pour confirmer  
- **Usage** : Reset des données sans recréer les tables

### 3️⃣ Eliminar TODOS los datos (⚠️ MUY PELIGROSO)
- **Action** : Supprime bases, logs, PDFs, cache
- **Confirmation** : Tape "ELIMINAR_TODO" pour confirmer
- **Usage** : Nettoyage complet du projet

### 4️⃣ Eliminar solo las bases de datos de TEST
- **Action** : Supprime uniquement les bases de test
- **Confirmation** : Aucune
- **Usage** : Nettoyage après tests

### 5️⃣ Eliminar solo las bases de datos de BACKUP
- **Action** : Supprime les fichiers *old*.db et *backup*.db
- **Confirmation** : Aucune
- **Usage** : Nettoyage des anciens backups

### 6️⃣ Crear base de datos LIMPIA (⭐ RECOMENDADO)
- **Action** : Crée une nouvelle base propre avec structure
- **Confirmation** : Tape "SI" pour confirmer
- **Usage** : Démarrage propre pour développement

### 7️⃣ Mostrar estado actual y salir
- **Action** : Affiche l'état sans modification
- **Confirmation** : Aucune
- **Usage** : Diagnostic

### 8️⃣ Cancelar
- **Action** : Quitte sans modification
- **Confirmation** : Aucune
- **Usage** : Sortie sécurisée

## 🎯 Recommandations

### Pour Développement
```bash
./clean_databases.sh
# Choisir option 6 (Crear base de datos LIMPIA)
```

### Pour Nettoyage Complet
```bash
./clean_databases.sh  
# Choisir option 3 (Eliminar TODOS los datos)
```

### Pour Diagnostic
```bash
./clean_databases.sh
# Choisir option 7 (Mostrar estado actual)
```

## ✅ Fonctionnalités

- 📊 **Affichage du contenu** des bases de données
- 📋 **Liste des fichiers** avec tailles
- 🔒 **Confirmations** pour actions dangereuses
- 🆕 **Création automatique** de base propre
- 🧹 **Nettoyage sélectif** par type de fichier
- 📈 **État avant/après** chaque opération

## 🛡️ Sécurité

- ⚠️ **Confirmations obligatoires** pour actions destructives
- 📋 **Affichage préalable** du contenu
- 🔄 **État final** affiché après chaque action
- 💾 **Backup automatique** non supprimé par défaut

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
