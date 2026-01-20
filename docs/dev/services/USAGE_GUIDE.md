> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# Guide d'Utilisation des Services

## Introduction

Ce guide explique comment utiliser les services dans l'application Facturacion Facil.

## Installation

Les services sont déjà intégrés dans l'application. Aucune installation supplémentaire n'est nécessaire.

## Utilisation de Base

### 1. Importer un Service

```python
from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from services.factura_service import FacturaService
```

### 2. Créer une Instance

```python
# Utiliser la base de données par défaut
producto_service = ProductoService()

# Utiliser une base de données spécifique (pour les tests)
producto_service = ProductoService('/path/to/test.db')
```

### 3. Utiliser les Méthodes

```python
# Créer un produit
producto_id = producto_service.create_producto({
    'nombre': 'Camiseta Roja',
    'precio_venta': 19.99,
    'iva_recomendado': 21.0,
    'stock': 50
})

# Lire tous les produits
productos = producto_service.get_all_productos()

# Lire un produit spécifique
producto = producto_service.get_producto_by_id(producto_id)

# Mettre à jour un produit
producto_service.update_producto({
    'id': producto_id,
    'nombre': 'Camiseta Roja XL',
    'precio_venta': 24.99
})

# Supprimer un produit
producto_service.delete_producto(producto_id)
```

## Exemples Pratiques

### Exemple 1: Créer une Facture Complète

```python
from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from services.factura_service import FacturaService
from datetime import datetime

# Initialiser les services
producto_service = ProductoService()
cliente_service = ClienteService()
factura_service = FacturaService()

# 1. Créer un produit
producto_id = producto_service.create_producto({
    'nombre': 'Camiseta',
    'precio_venta': 19.99,
    'iva_recomendado': 21.0,
    'stock': 100
})

# 2. Créer un client
cliente_id = cliente_service.create_cliente({
    'nombre': 'Juan Pérez',
    'email': 'juan@example.com',
    'nif': '12345678A',
    'direccion': 'Calle Mayor 123',
    'telefono': '666777888'
})

# 3. Récupérer les données du client
cliente = cliente_service.get_cliente_by_id(cliente_id)

# 4. Créer la facture
factura_data = {
    'numero': factura_service.generate_factura_number(),
    'fecha': datetime.now().strftime('%Y-%m-%d'),
    'cliente': {
        'id': cliente['id'],
        'nombre': cliente['nombre'],
        'nif': cliente['nif'],
        'direccion': cliente['direccion']
    },
    'lineas': [{
        'producto_id': producto_id,
        'cantidad': 2,
        'precio_unitario': 19.99,
        'iva': 21.0
    }]
}

# Calculer les totaux
totales = factura_service.calculate_totals(factura_data['lineas'])
factura_data.update(totales)

# Créer la facture
factura_id = factura_service.create_factura(factura_data)
print(f"Factura créée avec ID: {factura_id}")
```

### Exemple 2: Gestion d'Erreurs

```python
from services.producto_service import ProductoService
from utils.exceptions import (
    ProductValidationError,
    ProductNotFoundError,
    DatabaseError
)

service = ProductoService()

try:
    # Tentative de création avec données invalides
    producto_id = service.create_producto({
        'nombre': '',  # Nom vide!
        'precio_venta': -10  # Prix négatif!
    })
except ProductValidationError as e:
    print(f"Erreur de validation: {e}")
    print(f"Détails: {e.details}")

try:
    # Tentative de lecture d'un produit inexistant
    producto = service.get_producto_by_id(99999)
    if producto is None:
        print("Produit non trouvé")
except DatabaseError as e:
    print(f"Erreur de base de données: {e}")
```

### Exemple 3: Utilisation dans une UI PyQt5

```python
from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox
from services.producto_service import ProductoService
from utils.exceptions import ProductValidationError, DatabaseError

class ProductosWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        
        # Initialiser le service avec le même db_path que la fenêtre
        db_path = db.db_path if hasattr(db, 'db_path') else None
        self.producto_service = ProductoService(db_path)
        
        # Créer l'UI
        self.init_ui()
    
    def init_ui(self):
        # ... créer les widgets ...
        
        btn_guardar = QPushButton('Guardar')
        btn_guardar.clicked.connect(self.guardar_producto)
    
    def guardar_producto(self):
        try:
            # Récupérer les données du formulaire
            producto_data = {
                'nombre': self.txt_nombre.text(),
                'precio_venta': float(self.txt_precio.text()),
                'iva_recomendado': float(self.txt_iva.text()),
                'stock': int(self.txt_stock.text())
            }
            
            # Créer le produit via le service
            producto_id = self.producto_service.create_producto(producto_data)
            
            # Afficher un message de succès
            QMessageBox.information(
                self,
                'Éxito',
                f'Producto creado con ID: {producto_id}'
            )
            
            # Rafraîchir la liste
            self.cargar_productos()
            
        except ProductValidationError as e:
            QMessageBox.warning(
                self,
                'Error de Validación',
                str(e)
            )
        except DatabaseError as e:
            QMessageBox.critical(
                self,
                'Error de Base de Datos',
                str(e)
            )
    
    def cargar_productos(self):
        try:
            productos = self.producto_service.get_all_productos()
            # ... afficher les produits dans la table ...
        except DatabaseError as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Error cargando productos: {e}'
            )
```

## Bonnes Pratiques

### 1. Toujours Gérer les Exceptions

```python
# ❌ Mauvais
producto = service.create_producto(data)

# ✅ Bon
try:
    producto = service.create_producto(data)
except ProductValidationError as e:
    # Gérer l'erreur de validation
    pass
except DatabaseError as e:
    # Gérer l'erreur de base de données
    pass
```

### 2. Utiliser le Même db_path dans les Tests

```python
# ❌ Mauvais (utilise des DB différentes)
service1 = ProductoService()
service2 = ClienteService('/tmp/test.db')

# ✅ Bon (utilise la même DB)
db_path = '/tmp/test.db'
service1 = ProductoService(db_path)
service2 = ClienteService(db_path)
```

### 3. Valider les Données Avant l'Envoi

```python
# ✅ Bon
if not nombre or not precio_venta:
    QMessageBox.warning(self, 'Error', 'Campos requeridos vacíos')
    return

try:
    service.create_producto({'nombre': nombre, 'precio_venta': precio_venta})
except ProductValidationError as e:
    QMessageBox.warning(self, 'Error', str(e))
```

### 4. Utiliser calculate_totals pour les Factures

```python
# ✅ Bon
lineas = [...]
totales = factura_service.calculate_totals(lineas)
factura_data.update(totales)
factura_service.create_factura(factura_data)
```

## Tests

Pour tester les services, utiliser `BaseTestWithFixtures`:

```python
from test.base_test_with_fixtures import BaseTestWithFixtures
from services.producto_service import ProductoService

class TestProductoService(BaseTestWithFixtures):
    def setUp(self):
        super().setUp()
        self.service = ProductoService(self.db_path)
    
    def test_create_producto(self):
        producto_id = self.service.create_producto({
            'nombre': 'Test',
            'precio_venta': 10.0
        })
        self.assertIsNotNone(producto_id)
```

---

**Version**: 1.0  
**Date**: 2025-12-25


---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
