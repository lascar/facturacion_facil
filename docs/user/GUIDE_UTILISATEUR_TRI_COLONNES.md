# 🔄 Guide Utilisateur - Tri par Colonnes

## 📋 Description

Guide d'utilisation du système de tri par colonnes dans Facturación Fácil. Cette fonctionnalité permet d'ordonner facilement les données dans toutes les listes de l'application.

## 🎯 Objectif

Apprendre à utiliser le tri par colonnes pour organiser et trouver rapidement les informations dans les listes de produits, factures et stock.

## ✨ Fonctionnalités Disponibles

### 🔄 **Tri par Clic**
- **Un clic** sur un en-tête de colonne → Tri ascendant
- **Deux clics** sur la même colonne → Tri descendant
- **Indicateurs visuels** pour voir l'état du tri

### 📊 **Types de Données Supportés**
- **Texte** : Ordre alphabétique (A-Z ou Z-A)
- **Nombres** : Ordre numérique (1-100 ou 100-1)
- **Prix** : Ordre par valeur monétaire (€5.50 → €100.00)
- **Dates** : Ordre chronologique (plus ancien → plus récent)

## 🖥️ Utilisation dans les Fenêtres

### 📦 **Fenêtre Produits**

#### **Colonnes Disponibles**
- **Nom** : Tri alphabétique des noms de produits
- **Référence** : Tri par code de référence
- **Prix** : Tri par valeur monétaire
- **Catégorie** : Tri alphabétique des catégories

#### **Exemple d'Utilisation**
1. Ouvrir la fenêtre "Gestión de Productos"
2. Cliquer sur l'en-tête "Prix" → Les produits s'ordonnent du moins cher au plus cher
3. Cliquer à nouveau sur "Prix" → Ordre inverse (plus cher au moins cher)
4. Cliquer sur "Nom" → Tri alphabétique par nom de produit

### 📄 **Fenêtre Factures**

#### **Colonnes Disponibles**
- **Numéro** : Tri par numéro de facture
- **Date** : Tri chronologique
- **Client** : Tri alphabétique par nom de client
- **Total** : Tri par montant total

#### **Exemple d'Utilisation**
1. Ouvrir la fenêtre "Facturas"
2. Cliquer sur "Date" → Factures ordonnées de la plus ancienne à la plus récente
3. Cliquer sur "Total" → Factures ordonnées par montant croissant
4. Double-clic sur "Total" → Factures ordonnées par montant décroissant

### 📊 **Fenêtre Stock**

#### **Colonnes Disponibles**
- **Produit** : Tri alphabétique par nom de produit
- **Référence** : Tri par code de référence
- **Stock Actual** : Tri par quantité en stock
- **État** : Tri par état du stock (Disponible, Stock bas, Sin stock)
- **Última Actualización** : Tri par date de dernière mise à jour

#### **Exemple d'Utilisation**
1. Ouvrir la fenêtre "Gestión de Stock"
2. Cliquer sur "Stock Actual" → Produits ordonnés par quantité croissante
3. Identifier rapidement les produits en rupture de stock (en début de liste)
4. Cliquer sur "État" → Grouper par état de stock

## 🎨 Indicateurs Visuels

### **Symboles dans les En-têtes**
- **↕** : Colonne triable (état initial)
- **↑** : Tri ascendant actif (A-Z, 1-100, ancien→récent)
- **↓** : Tri descendant actif (Z-A, 100-1, récent→ancien)

### **Exemple Visuel**
```
Nom ↑ | Prix ↕ | Date ↕ | Stock ↕
```
*La colonne "Nom" est triée en ordre ascendant*

## 💡 Conseils d'Utilisation

### **🔍 Recherche Rapide**
1. **Trouver le produit le moins cher** :
   - Cliquer sur "Prix" → Le moins cher apparaît en premier
2. **Voir les factures récentes** :
   - Double-clic sur "Date" → Les plus récentes en premier
3. **Identifier les stocks faibles** :
   - Cliquer sur "Stock Actual" → Les quantités les plus faibles en premier

### **📊 Analyse de Données**
1. **Analyser les ventes par client** :
   - Trier par "Client" → Grouper les factures par client
2. **Surveiller les stocks** :
   - Trier par "État" → Voir rapidement les produits en rupture
3. **Gérer les prix** :
   - Trier par "Prix" → Analyser la gamme de prix

### **⚡ Raccourcis Efficaces**
- **Tri rapide** : Un seul clic sur l'en-tête
- **Inversion rapide** : Double-clic sur la même colonne
- **Retour à l'état initial** : Cliquer sur une autre colonne

## 🔧 Fonctionnalités Avancées

### **🎯 Tri Intelligent**
Le système détecte automatiquement le type de données :
- **€25.50, €100.00** → Tri par valeur numérique (pas alphabétique)
- **15/01/2024, 20/01/2024** → Tri chronologique
- **REF001, REF010, REF002** → Tri alphanumérique intelligent

### **🔄 Persistance du Tri**
- Le tri reste actif pendant toute la session
- Nouvelles données ajoutées respectent l'ordre de tri
- Chaque fenêtre maintient son propre état de tri

## ❓ Questions Fréquentes

### **Q: Pourquoi certaines colonnes ne se trient pas comme attendu ?**
**R:** Le système détecte automatiquement le type de données. Si une colonne contient des formats mixtes, elle sera triée comme du texte. Assurez-vous que les données sont dans un format cohérent.

### **Q: Comment revenir à l'ordre original ?**
**R:** Fermez et rouvrez la fenêtre, ou cliquez sur une colonne différente puis revenez à votre tri souhaité.

### **Q: Le tri fonctionne-t-il avec la recherche ?**
**R:** Oui ! Vous pouvez d'abord filtrer avec la recherche, puis trier les résultats filtrés.

### **Q: Puis-je trier par plusieurs colonnes ?**
**R:** Actuellement, le tri se fait par une colonne à la fois. Cliquer sur une nouvelle colonne remplace le tri précédent.

## 🚀 Avantages pour l'Utilisateur

### **⏱️ Gain de Temps**
- Trouver rapidement l'information recherchée
- Pas besoin de parcourir toute la liste
- Identification immédiate des valeurs extrêmes

### **📊 Meilleure Analyse**
- Visualiser les tendances dans les données
- Comparer facilement les valeurs
- Identifier les anomalies ou problèmes

### **🎯 Efficacité Améliorée**
- Workflow plus fluide
- Moins de clics pour trouver l'information
- Interface plus intuitive et professionnelle

## 🔧 Dépannage

### **Problème : Le tri ne fonctionne pas**
**Solutions :**
1. Vérifier que vous cliquez bien sur l'en-tête de colonne
2. Attendre que les données soient complètement chargées
3. Redémarrer l'application si nécessaire

### **Problème : L'ordre semble incorrect**
**Solutions :**
1. Vérifier le type de données dans la colonne
2. S'assurer que les formats sont cohérents
3. Essayer un double-clic pour inverser l'ordre

### **Problème : Les indicateurs ne s'affichent pas**
**Solutions :**
1. Vérifier que la fenêtre est complètement chargée
2. Redimensionner légèrement la fenêtre
3. Cliquer sur une autre colonne puis revenir

## 📞 Support

Si vous rencontrez des problèmes avec le système de tri :
1. Consultez d'abord cette documentation
2. Vérifiez que vos données sont dans un format cohérent
3. Testez avec la démonstration : `python test/demo/demo_treeview_sorting.py`
4. Contactez le support technique si le problème persiste

---

**Le tri par colonnes rend la navigation dans vos données plus rapide et plus intuitive !** 🎉
