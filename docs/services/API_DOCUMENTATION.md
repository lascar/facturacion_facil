# Documentation API - Services

## Vue d'ensemble

Les services fournissent une couche d'abstraction entre l'interface utilisateur et la base de données. Ils encapsulent la logique métier, la validation des données et la gestion des erreurs.

## Architecture

```
UI Layer (PyQt5)
    ↓
Service Layer (Business Logic)
    ↓
Database Layer (SQLite)
```

### Avantages

- **Séparation des responsabilités**: UI ≠ Logique métier ≠ Accès données
- **Réutilisabilité**: Les services peuvent être utilisés par différentes UIs
- **Testabilité**: Tests unitaires sans dépendance à l'UI
- **Maintenabilité**: Modifications centralisées

---

## BaseService

Classe de base pour tous les services. Fournit des fonctionnalités communes.

### Méthodes

#### `__init__(db_path: Optional[str] = None)`

Initialise le service avec une base de données.

**Paramètres:**
- `db_path` (str, optionnel): Chemin vers la base de données. Si None, utilise la DB par défaut.

**Exemple:**
```python
from services.producto_service import ProductoService

# Utiliser la DB par défaut
service = ProductoService()

# Utiliser une DB spécifique (pour les tests)
service = ProductoService('/tmp/test.db')
```

#### `validate_required_fields(data, required_fields, error_class)`

Valide que tous les champs requis sont présents.

**Lève:** Exception de type `error_class` si un champ manque.

#### `validate_id(id_value, entity_name, error_class)`

Valide qu'un ID est un entier positif.

**Lève:** Exception de type `error_class` si l'ID est invalide.

#### `validate_positive_number(value, field_name, error_class)`

Valide qu'un nombre est positif ou zéro.

**Lève:** Exception de type `error_class` si le nombre est négatif.

---

## ProductoService

Gestion des produits.

### Méthodes

#### `get_all_productos() -> List[Dict[str, Any]]`

Récupère tous les produits.

**Retourne:** Liste de dictionnaires représentant les produits.

**Lève:** `DatabaseError` en cas d'erreur.

**Exemple:**
```python
service = ProductoService()
productos = service.get_all_productos()
for producto in productos:
    print(f"{producto['nombre']}: {producto['precio_venta']}€")
```

#### `get_producto_by_id(producto_id: int) -> Optional[Dict[str, Any]]`

Récupère un produit par son ID.

**Paramètres:**
- `producto_id` (int): ID du produit

**Retourne:** Dictionnaire du produit ou None si non trouvé.

**Lève:** 
- `ProductValidationError` si l'ID est invalide
- `DatabaseError` en cas d'erreur

#### `create_producto(producto_data: Dict[str, Any]) -> int`

Crée un nouveau produit.

**Paramètres:**
- `producto_data` (dict): Données du produit
  - `nombre` (str, requis): Nom du produit
  - `precio_venta` (float, optionnel): Prix de vente (≥ 0)
  - `iva_recomendado` (float, optionnel): IVA (0-100)
  - `stock` (int, optionnel): Stock initial (≥ 0)
  - `referencia` (str, optionnel): Référence unique
  - `categoria` (str, optionnel): Catégorie
  - `descripcion` (str, optionnel): Description

**Retourne:** ID du produit créé.

**Lève:**
- `ProductValidationError` si les données sont invalides
- `DatabaseError` en cas d'erreur

**Exemple:**
```python
producto_id = service.create_producto({
    'nombre': 'Camiseta',
    'precio_venta': 19.99,
    'iva_recomendado': 21.0,
    'stock': 50
})
```

#### `update_producto(producto_data: Dict[str, Any]) -> bool`

Met à jour un produit existant.

**Paramètres:**
- `producto_data` (dict): Données du produit (doit contenir 'id')

**Retourne:** True si la mise à jour a réussi.

**Lève:**
- `ProductValidationError` si les données sont invalides
- `DatabaseError` en cas d'erreur

#### `delete_producto(producto_id: int) -> bool`

Supprime un produit.

**Paramètres:**
- `producto_id` (int): ID du produit à supprimer

**Retourne:** True si la suppression a réussi.

**Lève:**
- `ProductValidationError` si l'ID est invalide
- `DatabaseError` en cas d'erreur

---

## ClienteService

Gestion des clients.

### Méthodes

#### `get_all_clientes() -> List[Dict[str, Any]]`

Récupère tous les clients.

#### `get_cliente_by_id(cliente_id: int) -> Optional[Dict[str, Any]]`

Récupère un client par son ID.

#### `create_cliente(cliente_data: Dict[str, Any]) -> int`

Crée un nouveau client.

**Champs requis:**
- `nombre` (str): Nom du client
- `email` (str): Email (doit contenir @)

**Champs optionnels:**
- `nif` (str): NIF/CIF
- `direccion` (str): Adresse
- `telefono` (str): Téléphone

#### `update_cliente(cliente_data: Dict[str, Any]) -> bool`

Met à jour un client existant.

#### `delete_cliente(cliente_id: int) -> bool`

Supprime un client.

---

## OrganizacionService

Gestion de l'organisation (paramètres de l'entreprise).

### Méthodes

#### `get_organizacion() -> Optional[Dict[str, Any]]`

Récupère les données de l'organisation.

#### `create_organizacion(org_data: Dict[str, Any]) -> int`

Crée l'organisation.

**Champs requis:**
- `nombre` (str): Nom de l'entreprise

**Champs optionnels:**
- `cif` (str): CIF (≥ 9 caractères)
- `email` (str): Email (doit contenir @)
- `numero_factura_inicial` (int): Numéro de facture initial (> 0)

#### `update_organizacion(org_data: Dict[str, Any]) -> bool`

Met à jour l'organisation.

---

## FacturaService

Gestion des factures (le plus complexe).

### Méthodes

#### `get_all_facturas() -> List[Dict[str, Any]]`

Récupère toutes les factures.

#### `get_factura_by_id(factura_id: int) -> Optional[Dict[str, Any]]`

Récupère une facture par son ID (avec lignes incluses).

#### `create_factura(factura_data: Dict[str, Any]) -> int`

Crée une nouvelle facture.

**Format des données:**
```python
factura_data = {
    'numero': 'FAC-0001',
    'fecha': '2025-12-25',
    'cliente': {
        'id': 1,
        'nombre': 'Cliente Test',
        'nif': '12345678A',
        'direccion': 'Calle Test 123'
    },
    'subtotal': 10.0,
    'iva_total': 2.1,
    'total': 12.1,
    'lineas': [{
        'producto_id': 1,
        'cantidad': 2,
        'precio_unitario': 5.0,
        'iva': 21.0
    }]
}
```

**Validation automatique:**
- Vérification du stock disponible
- Validation des prix (≥ 0)
- Validation des quantités (> 0)

#### `update_factura(factura_data: Dict[str, Any]) -> bool`

Met à jour une facture existante.

#### `delete_factura(factura_id: int) -> bool`

Supprime une facture.

#### `calculate_totals(lineas: List[Dict[str, Any]]) -> Dict[str, float]`

Calcule les totaux d'une facture.

**Retourne:**
```python
{
    'subtotal': 10.0,
    'iva_total': 2.1,
    'total': 12.1
}
```

#### `generate_factura_number() -> str`

Génère un nouveau numéro de facture (format: FAC-XXXX).

---

## Gestion des Erreurs

Toutes les méthodes peuvent lever les exceptions suivantes:

### Exceptions de Validation

- `ProductValidationError`: Données produit invalides
- `ClientValidationError`: Données client invalides
- `OrganizationValidationError`: Données organisation invalides
- `InvoiceValidationError`: Données facture invalides

### Exceptions Not Found

- `ProductNotFoundError`: Produit non trouvé
- `ClientNotFoundError`: Client non trouvé
- `OrganizationNotFoundError`: Organisation non trouvée
- `InvoiceNotFoundError`: Facture non trouvée

### Exceptions Métier

- `InsufficientStockError`: Stock insuffisant pour une facture

### Exceptions Techniques

- `DatabaseError`: Erreur de base de données
- `DatabaseConnectionError`: Erreur de connexion

**Exemple de gestion d'erreurs:**
```python
from services.producto_service import ProductoService
from utils.exceptions import ProductValidationError, DatabaseError

service = ProductoService()

try:
    producto_id = service.create_producto({
        'nombre': 'Test',
        'precio_venta': -10  # Prix négatif!
    })
except ProductValidationError as e:
    print(f"Erreur de validation: {e}")
except DatabaseError as e:
    print(f"Erreur de base de données: {e}")
```

---

**Version**: 1.0  
**Date**: 2025-12-25

