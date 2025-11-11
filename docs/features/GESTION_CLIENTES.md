# 👥 GESTIÓN DE CLIENTES

## 📋 **Vue d'ensemble**

Implémentation complète d'un système de gestion des clients avec deux approches :

1. **Interface dédiée** : Fenêtre complète pour gérer les clients (créer, modifier, supprimer)
2. **Ajout automatique** : Création automatique de clients lors de la facturation

---

## 🎯 **Fonctionnalités Implémentées**

### **1. Interface de Gestion des Clients**
- ✅ **Fenêtre dédiée** accessible depuis le menu principal
- ✅ **Liste des clients** avec recherche en temps réel
- ✅ **Formulaire complet** : nom, DNI/NIE, email, téléphone, adresse
- ✅ **Opérations CRUD** : Créer, Lire, Modifier, Supprimer
- ✅ **Validation des données** avec messages d'erreur clairs
- ✅ **Tri et recherche** dans la liste des clients

### **2. Intégration avec les Factures**
- ✅ **Sélection de clients** via dropdown dans l'interface de facturation
- ✅ **Ajout automatique** de nouveaux clients lors de la création de factures
- ✅ **Relation base de données** entre clients et factures
- ✅ **Compatibilité** avec les factures existantes

### **3. Base de Données**
- ✅ **Table `clientes`** avec tous les champs nécessaires
- ✅ **Relation `cliente_id`** dans la table `facturas`
- ✅ **Migration automatique** des bases de données existantes
- ✅ **Compatibilité** avec les anciennes structures

---

## 🏗️ **Architecture Technique**

### **Modèle de Données**

#### **Table `clientes`**
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    dni_nie TEXT,
    direccion TEXT,
    email TEXT,
    telefono TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Table `facturas` (modifiée)**
```sql
-- Nouvelle colonne ajoutée
ALTER TABLE facturas ADD COLUMN cliente_id INTEGER;
-- Relation avec clientes
FOREIGN KEY (cliente_id) REFERENCES clientes (id)
```

### **Modèles Python**

#### **Classe `Cliente`**
```python
class Cliente:
    def __init__(self, id=None, nombre="", dni_nie="", direccion="", email="", telefono=""):
        # Propriétés du client
    
    def save(self):           # Créer/Modifier
    def delete(self):         # Supprimer
    
    @staticmethod
    def get_all():           # Lister tous
    def get_by_id(id):       # Obtenir par ID
    def get_by_nombre(nom):  # Obtenir par nom
    def search(terme):       # Rechercher
```

#### **Classe `Factura` (modifiée)**
```python
class Factura:
    def __init__(self, ..., cliente_id=None, ...):
        self.cliente_id = cliente_id  # Nouvelle propriété
        # ... autres propriétés
```

---

## 🖥️ **Interface Utilisateur**

### **1. Menu Principal**
- **Nouveau bouton** : "👥 Clientes"
- **Position** : À côté des autres modules (Productos, Stock, Facturas)

### **2. Fenêtre de Gestion des Clientes**
- **Taille** : 1000x700 pixels
- **Layout** : Vertical (liste en haut, formulaire en bas)
- **Fonctionnalités** :
  - Liste avec tri par colonnes
  - Barre de recherche en temps réel
  - Formulaire avec validation
  - Boutons : Nouveau, Guardar, Eliminar, Limpiar

### **3. Interface de Facturation (modifiée)**
- **Dropdown de sélection** : Liste des clients existants
- **Bouton de gestion** : Accès rapide à la fenêtre de clients
- **Auto-remplissage** : Sélection d'un client remplit automatiquement les champs
- **Ajout automatique** : Nouveaux clients créés automatiquement

---

## 🔄 **Flux de Travail**

### **Scénario 1 : Gestion via Interface Dédiée**
1. **Accès** : Menu Principal → "👥 Clientes"
2. **Création** : Bouton "Nuevo Cliente" → Remplir formulaire → "Guardar"
3. **Modification** : Sélectionner client → Modifier → "Guardar"
4. **Suppression** : Sélectionner client → "Eliminar" → Confirmer

### **Scénario 2 : Ajout Automatique via Facturation**
1. **Facturation** : Menu Principal → "Facturas" → "Nueva Factura"
2. **Client existant** : Dropdown → Sélectionner client → Auto-remplissage
3. **Nouveau client** : Saisir nom → Remplir données → "Guardar Factura"
4. **Résultat** : Client créé automatiquement et associé à la facture

---

## 🧪 **Tests Intégrés**

### **Tests d'Intégration**
**Fichier :** `test/integration/test_clientes_integration.py`

#### **Tests Couverts :**
1. **CRUD Operations** : Créer, Lire, Modifier, Supprimer clients
2. **Intégration Factura-Cliente** : Relation entre clients et factures
3. **Simulation Interface** : Test de l'interface utilisateur

#### **Résultats :**
```bash
pytest test/integration/test_clientes_integration.py -v
# ✅ test_cliente_crud_operations PASSED
# ✅ test_cliente_factura_integration PASSED
# ✅ test_cliente_interface_simulation PASSED
```

---

## 📊 **Avantages**

### **Pour l'Utilisateur**
- ✅ **Gestion centralisée** des clients
- ✅ **Évite la duplication** de données
- ✅ **Recherche rapide** de clients existants
- ✅ **Auto-remplissage** des données dans les factures
- ✅ **Historique** des relations client-facture

### **Pour le Système**
- ✅ **Normalisation** de la base de données
- ✅ **Intégrité référentielle** entre clients et factures
- ✅ **Performance** améliorée (pas de duplication)
- ✅ **Évolutivité** pour futures fonctionnalités

### **Pour la Maintenance**
- ✅ **Code modulaire** et réutilisable
- ✅ **Tests automatisés** complets
- ✅ **Migration automatique** des données existantes
- ✅ **Compatibilité** avec les versions antérieures

---

## 🔧 **Migration et Compatibilité**

### **Migration Automatique**
- ✅ **Création de table** `clientes` si elle n'existe pas
- ✅ **Ajout de colonne** `cliente_id` dans `facturas`
- ✅ **Préservation** de toutes les données existantes
- ✅ **Détection automatique** de la structure de base de données

### **Compatibilité**
- ✅ **Anciennes factures** : Fonctionnent sans modification
- ✅ **Nouvelles factures** : Utilisent automatiquement les clients
- ✅ **Données existantes** : Préservées intégralement
- ✅ **Interface** : Rétrocompatible avec les workflows existants

**État :** ✅ **IMPLÉMENTÉ ET TESTÉ**
