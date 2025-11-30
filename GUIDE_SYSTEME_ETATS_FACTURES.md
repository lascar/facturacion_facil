# 📋 Guide du Système d'États de Factures PyQt5

## 🎯 Vue d'ensemble

Le système d'états de factures permet de **configurer et gérer les différents états** que peuvent avoir vos factures (Borrador, Enviada, Pagada, etc.) avec un **contrôle granulaire des permissions** d'édition.

## ✨ Fonctionnalités Principales

### 🔧 Configuration des États
- **Création d'états personnalisés** avec nom et description
- **Couleurs personnalisables** pour identification visuelle
- **Contrôle des permissions** : définir si un état permet la modification
- **Ordre d'affichage** configurable
- **Gestion CRUD complète** (Créer, Lire, Modifier, Supprimer)

### 🛡️ Contrôle des Permissions
- **Édition conditionnelle** : les factures ne peuvent être modifiées que si l'état le permet
- **Interface adaptative** : les champs se désactivent automatiquement selon l'état
- **Validation en temps réel** : vérification des permissions avant toute modification

## 🚀 Utilisation

### 1. Configuration des États

#### Accès à la Configuration
1. Ouvrez la **fenêtre d'organisation** (menu Configuration)
2. Naviguez vers la section **"Configuración de Estados de Facturas"**
3. Vous verrez la liste des états existants avec leurs propriétés

#### Créer un Nouvel État
1. Cliquez sur **"➕ Agregar Estado"**
2. Remplissez le formulaire :
   - **Nombre** : Nom de l'état (ex: "En Revisión")
   - **Descripción** : Description détaillée
   - **Permite Modificación** : ✅ Cocher si l'état permet l'édition
   - **Color** : Choisir une couleur d'identification
   - **Orden** : Position dans la liste (1 = premier)
3. Cliquez sur **"💾 Guardar"**

#### Modifier un État Existant
1. **Sélectionnez** l'état dans la table
2. Cliquez sur **"✏️ Editar Estado"**
3. Modifiez les propriétés souhaitées
4. Sauvegardez les changements

#### Supprimer un État
1. **Sélectionnez** l'état à supprimer
2. Cliquez sur **"🗑️ Eliminar Estado"**
3. **Confirmez** la suppression (action irréversible)

### 2. Utilisation dans l'Édition de Factures

#### Sélection de l'État
1. Ouvrez l'**éditeur de factures** (bouton "✏️ Editar")
2. Dans la section "Información de la Factura", vous verrez le **combo "Estado"**
3. Sélectionnez l'état approprié pour la facture

#### Contrôle Automatique des Permissions
- **État permettant modification** : Tous les champs sont éditables
- **État bloquant modification** : Les champs se grisent automatiquement
- **Changement d'état en temps réel** : Les permissions s'appliquent immédiatement

## 🏗️ Architecture Technique

### Composants Principaux

#### 1. Base de Données (`database/database.py`)
```sql
Table: factura_estados
- id (INTEGER PRIMARY KEY)
- nombre (TEXT UNIQUE)
- descripcion (TEXT)
- permite_modificacion (BOOLEAN)
- color (TEXT)
- orden (INTEGER)
- activo (BOOLEAN)
```

#### 2. Gestionnaire d'États (`utils/invoice_status_manager.py`)
- **InvoiceStatusManager** : Classe principale de gestion
- **Méthodes CRUD** : get_all_statuses(), save_status(), delete_status()
- **Validation des permissions** : can_modify_invoice()
- **Gestion des couleurs** : get_status_color()

#### 3. Interface de Configuration (`ui/organizacion_pyqt5.py`)
- **Section dédiée** dans la fenêtre d'organisation
- **Table interactive** avec colonnes : Estado, Descripción, Permite Modificación, Color, Orden
- **Boutons d'action** : Agregar, Editar, Eliminar

#### 4. Dialogue d'Édition (`ui/invoice_status_dialog_pyqt5.py`)
- **Formulaire complet** pour créer/modifier les états
- **Sélecteur de couleur** intégré
- **Validation des données** avant sauvegarde

#### 5. Intégration Éditeur (`ui/facturas_pyqt5.py`)
- **Combo d'état** dans l'interface d'édition
- **Méthode update_permissions()** pour contrôler l'accès
- **Sauvegarde de l'état** avec la facture

## 🎨 États par Défaut

Le système inclut **6 états prédéfinis** :

| État | Description | Modification | Couleur |
|------|-------------|--------------|---------|
| **Borrador** | Facture en cours de création | ✅ Oui | #6c757d |
| **Enviada** | Facture envoyée au client | ❌ Non | #007bff |
| **Pagada** | Facture payée | ❌ Non | #28a745 |
| **Vencida** | Facture échue | ✅ Oui | #ffc107 |
| **Cancelada** | Facture annulée | ❌ Non | #fd7e14 |
| **Anulada** | Facture annulée définitivement | ❌ Non | #dc3545 |

## 🔒 Logique des Permissions

### États Modifiables
- **Borrador** : Permet toutes les modifications (création en cours)
- **Vencida** : Permet modifications (pour corrections/relances)

### États Non-Modifiables
- **Enviada** : Facture officielle, pas de modification
- **Pagada** : Transaction terminée, intégrité comptable
- **Cancelada/Anulada** : États finaux, pas de retour en arrière

## 🛠️ Personnalisation Avancée

### Créer des États Métier Spécifiques
```
Exemples d'états personnalisés :
- "En Validation" (modifiable)
- "Attente Signature" (non-modifiable)
- "Partiellement Payée" (modifiable)
- "En Litige" (modifiable)
- "Archivée" (non-modifiable)
```

### Workflow Recommandé
```
Borrador → Enviada → Pagada
    ↓         ↓
 Cancelada  Vencida → Pagada
    ↓         ↓
 Anulada   Cancelada
```

## 🧪 Tests et Validation

### Fichiers de Test
- **`test_simple_states.py`** : Tests de base des composants
- **`test_invoice_states_system.py`** : Tests complets du système

### Validation Manuelle
1. **Créer un état** avec modification désactivée
2. **Éditer une facture** et changer vers cet état
3. **Vérifier** que les champs se désactivent
4. **Tenter de modifier** → doit être bloqué

## 🎉 Avantages du Système

### Pour l'Utilisateur
- **Interface intuitive** avec contrôles visuels clairs
- **Flexibilité totale** dans la définition des états
- **Sécurité renforcée** contre les modifications accidentelles
- **Workflow métier** respecté automatiquement

### Pour le Développement
- **Architecture modulaire** et extensible
- **Séparation des responsabilités** claire
- **Validation centralisée** des permissions
- **Base de données normalisée** et performante

---

## 📞 Support

Pour toute question ou problème avec le système d'états :
1. Consultez les **logs de l'application**
2. Vérifiez la **base de données** (table factura_estados)
3. Testez avec les **scripts de validation** fournis

**Le système d'états de factures est maintenant entièrement opérationnel ! 🚀**
