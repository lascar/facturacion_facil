> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**

---

# 🔍 Instructions de Debug - Problème de Stock

## 🎯 Objectif
Identifier pourquoi les fenêtres gauche et droite affichent des stocks différents (2 vs 3).

## 📋 Découvertes Importantes

### ✅ **Base de Données Cohérente**
- Tests de cohérence : **4/4 réussis**
- Pas de problème d'accès concurrent
- Données stables entre appels
- **Problème** : Base de données **vide** (0 produits)

### 🚨 **Cause Probable**
La base de données de test est vide, mais l'application utilise probablement :
- **Données de démonstration** hardcodées
- **Cache local** avec des valeurs différentes
- **Fichiers de configuration** avec des stocks prédéfinis

## 🛠️ Étapes de Debug

### **Étape 1 : Lancer l'Application avec Logs**
```bash
cd /home/pascal/development/for_django/facturacion_facil
python3 main.py
```

### **Étape 2 : Reproduire le Problème**
1. **Ouvrir fenêtre de création** (bouton "Nueva Factura")
2. **Noter le stock affiché** dans le combo produit
3. **Fermer la fenêtre de création**
4. **Sélectionner une facture existante**
5. **Ouvrir fenêtre d'édition** (bouton "✏️ Editar")
6. **Noter le stock affiché** dans le combo produit
7. **Comparer les valeurs**

### **Étape 3 : Analyser les Logs**
Recherchez dans les logs (ou dans la console) :

```
[HH:MM:SS.mmm] CrearFacturaDialog - Llamando db.get_all_products()
[HH:MM:SS.mmm] CrearFacturaDialog - Recibidos X productos
[HH:MM:SS.mmm] CrearFacturaDialog - Producto: NOM_PRODUIT, Stock: 2, ID: Y

[HH:MM:SS.mmm] EditarFacturaDialog - Llamando db.get_all_products()
[HH:MM:SS.mmm] EditarFacturaDialog - Recibidos X productos
[HH:MM:SS.mmm] EditarFacturaDialog - Producto: NOM_PRODUIT, Stock: 3, ID: Y
```

### **Étape 4 : Identifier la Différence**

#### **Si même ID, stocks différents** :
- **Problème** : Modification entre les appels
- **Solution** : Forcer rechargement des données

#### **Si IDs différents** :
- **Problème** : Sources de données différentes
- **Solution** : Vérifier les requêtes SQL

#### **Si timing différent** :
- **Problème** : Cache ou transaction
- **Solution** : Synchroniser les accès

## 🔧 Solutions Potentielles

### **Solution A : Forcer le Rechargement**
```python
def load_data(self):
    # Forcer rechargement à chaque ouverture
    self.productos = None  # Vider le cache
    self.productos = db.get_all_products()
```

### **Solution B : Synchroniser les Données**
```python
def __init__(self, parent=None):
    # Partager les données entre fenêtres
    if hasattr(parent, 'productos_cache'):
        self.productos = parent.productos_cache
    else:
        self.productos = db.get_all_products()
        if parent:
            parent.productos_cache = self.productos
```

### **Solution C : Logs Plus Détaillés**
```python
# Ajouter dans load_data()
self.logger.debug(f"Requête SQL: {cursor.lastrowid}")
self.logger.debug(f"Timestamp: {datetime.now()}")
for producto in self.productos:
    self.logger.debug(f"Produit complet: {producto}")
```

## 📊 Informations à Collecter

### **Données Essentielles**
- **Timestamp exact** de chaque appel
- **Nombre de produits** retournés
- **ID des produits** pour vérifier l'identité
- **Valeurs de stock complètes** pour chaque produit
- **Source des données** (base, cache, fichier)

### **Contexte d'Exécution**
- **Ordre d'ouverture** des fenêtres
- **État de la base** avant/après
- **Modifications concurrentes** éventuelles
- **Transactions en cours**

## 🎯 Résultat Attendu

Après debug, vous devriez avoir :

### **Logs Clairs**
```
[14:50:01.123] CrearFacturaDialog - Producto: Produit A, Stock: 2, ID: 1
[14:50:05.456] EditarFacturaDialog - Producto: Produit A, Stock: 3, ID: 1
```

### **Cause Identifiée**
- **Modification de stock** entre les appels
- **Cache invalide** dans une fenêtre
- **Sources différentes** de données
- **Calcul incorrect** du stock disponible

### **Solution Appliquée**
- **Rechargement forcé** des données
- **Synchronisation** entre fenêtres
- **Correction** du calcul de stock
- **Invalidation** du cache

## 💡 Notes Importantes

### **Stock Normal vs Stock Disponible**
- **Création** : Stock réel en base
- **Édition** : Stock disponible (réel + libéré)
- **Différence attendue** si facture contient le produit

### **Vérification Rapide**
Si le produit est dans la facture en cours d'édition :
- **Stock création** : X
- **Stock édition** : X + quantité_dans_facture
- **C'est normal !**

---

## 🚀 Action Immédiate

**Lancez l'application et suivez les étapes 1-3 pour obtenir les logs détaillés !**

Les logs avec timestamp vous diront exactement ce qui se passe. 🔍

---

> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**
