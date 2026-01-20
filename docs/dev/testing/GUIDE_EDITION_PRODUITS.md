> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 📝 Guide d'Édition des Produits

## 🎯 Fonctionnalités d'Édition Disponibles

### 1️⃣ Créer un Nouveau Produit
- **Bouton** : "Nuevo"
- **Action** : Vide le formulaire et active le mode création
- **Indicateur** : Champs avec bordure bleue
- **Sauvegarde** : "Guardar" → Crée un nouveau produit

### 2️⃣ Éditer un Produit Existant

#### Méthode 1 : Bouton Editar
1. **Sélectionner** un produit dans la liste
2. **Cliquer** sur "Editar"
3. **Modifier** les données dans le formulaire
4. **Cliquer** sur "Guardar"

#### Méthode 2 : Double-clic (⭐ Rapide)
1. **Double-cliquer** sur un produit dans la liste
2. **Modifier** les données dans le formulaire
3. **Cliquer** sur "Guardar"

### 3️⃣ Supprimer un Produit
- **Sélectionner** un produit dans la liste
- **Cliquer** sur "Eliminar"
- **Confirmer** la suppression

## 🎨 Indicateurs Visuels

### Mode Normal (Consultation)
- ✅ **Champs** : Bordure grise, fond blanc
- ✅ **Boutons actifs** : Nuevo, Editar (si sélection), Eliminar (si sélection)
- ✅ **Boutons inactifs** : Guardar

### Mode Édition/Création
- 🔵 **Champs** : Bordure bleue, fond gris clair
- ✅ **Boutons actifs** : Guardar, Cerrar
- ✅ **Boutons inactifs** : Editar, Eliminar

## 🔄 États des Boutons

| Situation | Nuevo | Editar | Guardar | Eliminar |
|-----------|-------|--------|---------|----------|
| Aucune sélection | ✅ | ❌ | ❌ | ❌ |
| Produit sélectionné | ✅ | ✅ | ❌ | ✅ |
| Mode création | ✅ | ❌ | ✅ | ❌ |
| Mode édition | ✅ | ❌ | ✅ | ❌ |

## 📋 Champs du Formulaire

### Obligatoires
- **Referencia** : Code unique du produit
- **Nombre** : Nom du produit

### Optionnels
- **Categoría** : Catégorie (créée automatiquement si nouvelle)
- **Precio Compra** : Prix d'achat
- **Precio Venta** : Prix de vente
- **Descripción** : Description détaillée

## 🎯 Catégories Dynamiques

### Création de Nouvelle Catégorie
1. **Cliquer** dans le champ "Categoría"
2. **Taper** le nom de la nouvelle catégorie
3. **Sauvegarder** le produit
4. **Résultat** : La catégorie apparaît dans la liste pour les prochains produits

### Utilisation de Catégorie Existante
1. **Cliquer** sur la flèche du champ "Categoría"
2. **Sélectionner** une catégorie dans la liste
3. **Continuer** la saisie

## ⚡ Raccourcis et Astuces

### Raccourcis Clavier
- **Tab** : Naviguer entre les champs
- **Enter** : Valider la saisie (dans certains champs)
- **Escape** : Annuler l'édition (fermer la fenêtre)

### Astuces d'Utilisation
- 🖱️ **Double-clic** sur un produit = édition rapide
- 🔍 **Sélection** d'un produit = affichage dans le formulaire
- 💾 **Sauvegarde automatique** des nouvelles catégories
- 🔄 **Rechargement automatique** de la liste après modification

## ⚠️ Validations

### Erreurs Communes
- **Referencia vacía** : La référence est obligatoire
- **Nombre vacío** : Le nom est obligatoire
- **Referencia duplicada** : Chaque référence doit être unique

### Messages d'Information
- ✅ **"Producto creado correctamente"** : Nouveau produit créé
- ✅ **"Producto actualizado correctamente"** : Produit modifié
- ✅ **"Editando producto: [nom]"** : Mode édition activé

## 🚀 Workflow Recommandé

### Pour Créer un Produit
1. Cliquer "Nuevo"
2. Remplir Referencia et Nombre (obligatoires)
3. Ajouter Categoría (nouvelle ou existante)
4. Définir les prix
5. Ajouter une description
6. Cliquer "Guardar"

### Pour Modifier un Produit
1. Double-cliquer sur le produit dans la liste
2. Modifier les champs nécessaires
3. Cliquer "Guardar"

### Pour Supprimer un Produit
1. Sélectionner le produit
2. Cliquer "Eliminar"
3. Confirmer la suppression

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
