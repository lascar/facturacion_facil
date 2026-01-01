# 📦 Guide du Système de Fixtures

## 🎯 Vue d'ensemble

Le système de fixtures fournit un **état initial standardisé** pour tous les tests, avec :
- **3 produits** avec stocks définis
- **3 clients** avec données complètes  
- **3 factures** avec différents états et items

## 🏗️ Architecture

```
database/
├── fixtures.py          # Gestionnaire de fixtures
├── test_database.py     # Base de données de test
└── models.py           # Modèles (Stock, etc.)

test/
├── base_test_with_fixtures.py  # Classe de base pour tests
└── test_stock_with_fixtures.py # Exemple d'utilisation
```

## 📋 Données des Fixtures

### 🛍️ Produits
1. **Laptop Dell Inspiron** - Stock: 25 - Catégorie: Informatique
2. **Souris Logitech MX** - Stock: 150 - Catégorie: Accessoires  
3. **Clavier Mécanique RGB** - Stock: 75 - Catégorie: Accessoires

### 👥 Clients
1. **Empresa Tech Solutions** - Paris
2. **Boutique Informatique Plus** - Lyon
3. **StartUp Innovation Lab** - Paris

### 📄 Factures
1. **FAC-2024-001** - État: Enviada - 2 Laptops
2. **FAC-2024-002** - État: Pagada - 5 Souris + 3 Claviers
3. **FAC-2024-003** - État: Borrador - 1 Laptop + 2 Souris + 1 Clavier

## 🚀 Utilisation

### Classe de Test Simple

```python
from test.base_test_with_fixtures import BaseTestWithFixtures

class MonTest(BaseTestWithFixtures):
    def test_mon_fonctionnement(self):
        # Les fixtures sont automatiquement chargées
        products = self.get_test_products()
        clients = self.get_test_clients()
        invoices = self.get_test_invoices()
        
        # Faire des modifications
        # ...
        
        # setUp() remet automatiquement à l'état initial
```

### Test Manuel

```python
from database.test_database import TestDatabase

# Créer base de test avec fixtures
test_db = TestDatabase(with_fixtures=True)

# Obtenir les données
summary = test_db.get_fixtures_summary()
print(f"Produits: {summary['products_count']}")

# Faire des modifications
# ...

# Remettre à l'état initial
test_db.reset_to_fixtures()

# Nettoyage
test_db.cleanup()
```

## 🔄 Cycle de Vie des Tests

1. **setUpClass()** : Crée la base de test avec fixtures (une fois par classe)
2. **setUp()** : Remet à l'état initial avant chaque test
3. **test_xxx()** : Exécute le test avec données propres
4. **tearDown()** : Pas de nettoyage nécessaire
5. **tearDownClass()** : Nettoie la base de test

## 🛠️ Méthodes Utilitaires

### BaseTestWithFixtures

```python
# Accès aux données
self.get_test_products()    # Liste des produits
self.get_test_clients()     # Liste des clients  
self.get_test_invoices()    # Liste des factures

# Accès rapide
self.get_first_product()    # Premier produit
self.get_first_client()     # Premier client
self.get_first_invoice()    # Première facture

# Vérifications
self.assert_fixtures_loaded()  # Vérifie que tout est chargé
self.print_fixtures_summary()  # Affiche un résumé pour debug
```

### TestDatabase

```python
test_db = TestDatabase(with_fixtures=True)

# Gestion des fixtures
test_db.create_fixtures()        # Crée les fixtures
test_db.reset_to_fixtures()      # Remet à l'état initial
test_db.get_fixtures_summary()   # Résumé des données

# Nettoyage
test_db.cleanup()               # Supprime la base temporaire
```

## 📊 Exemple Complet

```python
class TestStockAvecFixtures(BaseTestWithFixtures):
    
    def test_modification_stock(self):
        """Test de modification de stock avec reset automatique"""
        
        # 1. Obtenir les données initiales
        first_product = self.get_first_product()
        original_stock = first_product['stock_actual']
        
        # 2. Modifier le stock
        new_stock = 999
        Stock.update_stock_direct(
            first_product['id'], 
            new_stock, 
            self.test_db.db_path
        )
        
        # 3. Vérifier la modification
        updated_products = self.test_db.fixtures.db_improved.get_all_products()
        updated_product = next(p for p in updated_products if p['id'] == first_product['id'])
        self.assertEqual(updated_product['stock_actual'], new_stock)
        
        # 4. setUp() du test suivant remettra automatiquement à l'état initial
```

## ✅ Avantages

- **🔄 Reset automatique** : Chaque test commence avec des données propres
- **📊 Données réalistes** : Produits, clients, factures avec relations
- **🚀 Rapidité** : Base temporaire en mémoire
- **🧹 Nettoyage automatique** : Pas de pollution entre tests
- **🎯 Consistance** : Même état initial pour tous les tests
- **🔧 Flexibilité** : Peut être étendu facilement

## 🎮 Démonstration

Lancer la démonstration complète :

```bash
python test_fixtures_demo.py
```

Cette démonstration montre :
- Création des fixtures
- Modifications de données
- Reset automatique
- Nettoyage final

## 🔧 Configuration

Les fixtures sont définies dans `database/fixtures.py` :

```python
def get_products_fixtures(self):
    return [
        {
            'nombre': 'Laptop Dell Inspiron',
            'referencia': 'DELL001',
            'precio': 899.99,
            'stock_actual': 25
        },
        # ...
    ]
```

Modifier ces données pour adapter les fixtures à tes besoins spécifiques.
