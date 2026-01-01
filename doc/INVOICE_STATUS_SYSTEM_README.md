# 📋 Système de Gestion des Statuts de Factures

## 🎯 Objectif

Implémentation d'un système complet de gestion des statuts de factures permettant :
- Configuration des statuts possibles dans la fenêtre organisation
- Contrôle des permissions de modification selon le statut
- Interface utilisateur adaptative selon les permissions

## 🏗️ Architecture

### 1. Base de Données

#### Nouvelle table `factura_estados`
```sql
CREATE TABLE factura_estados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT,
    permite_modificacion BOOLEAN DEFAULT 1,
    color TEXT DEFAULT '#007bff',
    orden INTEGER DEFAULT 0,
    activo BOOLEAN DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Colonne ajoutée à `facturas`
```sql
ALTER TABLE facturas ADD COLUMN estado TEXT DEFAULT 'Borrador'
```

### 2. Gestionnaire de Statuts

**Fichier:** `utils/invoice_status_manager.py`

**Fonctionnalités:**
- Gestion CRUD des statuts
- Vérification des permissions de modification
- Validation des transitions de statuts
- Gestion des couleurs et ordres

### 3. Interface Utilisateur

#### A. Fenêtre Organisation (`ui/organizacion_pyqt6.py`)
- **Nouvelle section:** "Configuración de Estados de Facturas"
- **Table interactive** avec colonnes :
  - Estado
  - Descripción  
  - Permite Modificación
  - Color
  - Orden
- **Boutons d'action:**
  - ➕ Agregar Estado
  - ✏️ Editar Estado
  - 🗑️ Eliminar Estado

#### B. Dialogue de Configuration (`ui/invoice_status_dialog.py`)
- Formulaire complet pour créer/éditer des statuts
- Sélecteur de couleur
- Checkbox pour permissions de modification
- Validation des données

#### C. Éditeur de Factures (`ui/factura_editor_pyqt6.py`)
- **Nouveau champ:** Combo "Estado"
- **Logique adaptative:** Champs désactivés selon le statut
- **Champs contrôlés:**
  - Número (lecture seule)
  - Fecha
  - Vencimiento
  - Productos (table entière)
  - Cliente (référence non modifiable)

#### D. Liste des Factures (`ui/facturas_pyqt6.py`)
- **Filtre dynamique** des statuts
- Chargement automatique des statuts depuis la base

## 🔧 Statuts par Défaut

| Statut | Description | Modifiable | Couleur |
|--------|-------------|------------|---------|
| Borrador | Facture en création | ✅ Oui | Gris |
| Pendiente | Envoyée, en attente | ❌ Non | Jaune |
| Pagada | Payée complètement | ❌ Non | Vert |
| Vencida | Échue sans paiement | ❌ Non | Rouge |
| Cancelada | Annulée | ❌ Non | Violet |
| Anulada | Annulée définitivement | ❌ Non | Orange |

## 🎮 Utilisation

### 1. Configuration des Statuts
1. Ouvrir la fenêtre "🏢 Organización"
2. Aller à la section "Configuración de Estados de Facturas"
3. Utiliser les boutons pour ajouter/éditer/supprimer des statuts

### 2. Création de Factures
1. Ouvrir l'éditeur de factures
2. Le statut par défaut est "Borrador" (modifiable)
3. Tous les champs sont éditables

### 3. Modification selon le Statut
- **Statut modifiable** (ex: Borrador) → Tous les champs éditables
- **Statut non-modifiable** (ex: Pagada) → Champs en lecture seule

### 4. Filtrage des Factures
1. Dans la liste des factures
2. Utiliser le filtre "Estado" pour voir les factures par statut

## 🔒 Règles de Sécurité

### Champs Contrôlés (Non-modifiables si statut ne le permet pas)
- ✅ **Número de factura** (toujours lecture seule)
- 🔒 **Fecha** 
- 🔒 **Vencimiento**
- 🔒 **Productos** (table entière)
- 🔒 **Totaux** (toujours calculés automatiquement)

### Champ Spécial
- 👁️ **Cliente** : Reste visible comme référence mais non modifiable

## 📁 Fichiers Modifiés

### Base de Données
- `database/database.py` - Tables et méthodes CRUD

### Utilitaires
- `utils/invoice_status_manager.py` - Gestionnaire principal

### Interface Utilisateur
- `ui/organizacion_pyqt6.py` - Configuration des statuts
- `ui/invoice_status_dialog.py` - Dialogue de configuration
- `ui/factura_editor_pyqt6.py` - Éditeur avec contrôle des statuts
- `ui/facturas_pyqt6.py` - Liste avec filtre dynamique

### Tests
- `test_invoice_status_system.py` - Test complet du système
- `test_simple_status.py` - Test simple des imports
- `test_ui_status_integration.py` - Test d'intégration UI

## 🚀 Déploiement

Le système est entièrement intégré et prêt à l'utilisation. 
Toutes les fonctionnalités demandées sont implémentées :

✅ Configuration des statuts dans la fenêtre organisation
✅ Contrôle des permissions de modification
✅ Interface adaptative selon le statut
✅ Champs spécifiques contrôlés (produit, prix, fecha, número, total, vencimiento)
✅ Client comme référence non-modifiable
✅ Persistance en base de données
✅ Filtrage dynamique dans la liste des factures
