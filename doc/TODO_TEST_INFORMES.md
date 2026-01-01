# TODO: Correction de test_informes_service.py

**Fichier**: `test/unit/test_informes_service.py`  
**Tests**: 9 tests  
**Statut**: Nécessite révision manuelle approfondie

---

## Problème

Le setup actuel utilise des méthodes de `Database` qui n'existent pas :
- `self.db.create_organization()`
- `self.db.add_client()`
- `self.db.add_product()`
- `self.db.update_product_stock()`
- `self.db.add_invoice()`

Ces méthodes n'existent pas dans la classe `Database`. Le setup doit être réécrit pour utiliser les services appropriés.

---

## Solution Recommandée

### 1. Utiliser les Services

```python
@pytest.fixture(autouse=True)
def setup(self, unit_db):
    """Configuration avant chaque test"""
    # Désactiver temporairement TEST_DATABASE_PATH
    old_test_db_path = os.environ.get('TEST_DATABASE_PATH')
    os.environ.pop('TEST_DATABASE_PATH', None)
    
    # Créer les services
    from services.organizacion_service import OrganizacionService
    from services.cliente_service import ClienteService
    from services.producto_service import ProductoService
    from services.factura_service import FacturaService
    
    org_service = OrganizacionService(unit_db.db_path)
    cliente_service = ClienteService(unit_db.db_path)
    producto_service = ProductoService(unit_db.db_path)
    factura_service = FacturaService(unit_db.db_path)
    self.informes_service = InformesService(unit_db.db_path)
    
    # Créer une organisation
    org_service.create_organizacion({
        'nombre': 'Test Org',
        'cif': '12345678A',
        'direccion': 'Test Address',
        'telefono': '123456789',
        'email': 'test@test.com'
    })
    
    # Créer un client
    self.cliente_id = cliente_service.create_cliente({
        'nombre': 'Cliente Test',
        'nif': 'B87654321',
        'direccion': 'Calle Test 123',
        'telefono': '987654321',
        'email': 'cliente@test.com'
    })
    
    # Créer des produits
    self.producto1_id = producto_service.create_producto({
        'nombre': 'Producto Test 1',
        'referencia': 'REF-001',
        'precio_venta': 100.0,
        'iva_recomendado': 21.0,
        'categoria': 'Categoría A',
        'stock': 100
    })
    
    self.producto2_id = producto_service.create_producto({
        'nombre': 'Producto Test 2',
        'referencia': 'REF-002',
        'precio_venta': 50.0,
        'iva_recomendado': 21.0,
        'categoria': 'Categoría B',
        'stock': 50
    })
    
    # Créer des factures
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Factura 1
    factura1_data = {
        'numero': 'F-001',
        'fecha': today,
        'cliente': {
            'id': self.cliente_id,
            'nombre': 'Cliente Test',
            'nif': 'B87654321',
            'direccion': 'Calle Test 123'
        },
        'lineas': [
            {
                'producto_id': self.producto1_id,
                'cantidad': 2,
                'precio_unitario': 100.0,
                'iva_aplicado': 21.0,
                'descuento': 0.0
            }
        ]
    }
    self.factura1_id = factura_service.create_factura(factura1_data)
    
    # Factura 2
    factura2_data = {
        'numero': 'F-002',
        'fecha': yesterday,
        'cliente': {
            'id': self.cliente_id,
            'nombre': 'Cliente Test',
            'nif': 'B87654321',
            'direccion': 'Calle Test 123'
        },
        'lineas': [
            {
                'producto_id': self.producto2_id,
                'cantidad': 3,
                'precio_unitario': 50.0,
                'iva_aplicado': 21.0,
                'descuento': 0.0
            }
        ]
    }
    self.factura2_id = factura_service.create_factura(factura2_data)
    
    # Restaurer TEST_DATABASE_PATH
    if old_test_db_path:
        os.environ['TEST_DATABASE_PATH'] = old_test_db_path
    
    yield
```

### 2. Convertir les Assertions unittest

Remplacer toutes les assertions unittest par des assertions pytest :

```python
# Avant
self.assertIn('periodo', informe)
self.assertEqual(informe['resumen']['num_facturas'], 2)

# Après
assert 'periodo' in informe
assert informe['resumen']['num_facturas'] == 2
```

### 3. Vérifier les Méthodes du Service

S'assurer que les méthodes appelées existent dans `InformesService` :
- `get_informe_facturacion(fecha_inicio, fecha_fin)`
- `get_informe_stock(productos_ids=None)`
- etc.

---

## Temps Estimé

**1-2 heures** pour :
1. Réécrire le setup (30 min)
2. Convertir les assertions (30 min)
3. Tester et corriger les erreurs (30-60 min)

---

## Priorité

**Moyenne** - Ces tests sont importants mais pas critiques pour le fonctionnement de base.

---

## Alternative

Si le temps manque, on peut :
1. Marquer ces tests comme `@pytest.mark.skip(reason="Nécessite refactorisation")`
2. Les corriger plus tard quand on a plus de temps
3. Se concentrer sur les tests d'intégration qui sont plus critiques

