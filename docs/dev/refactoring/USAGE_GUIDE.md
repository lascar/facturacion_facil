# 📖 Guide d'utilisation - Outils de refactorisation

## 🎯 Vue d'ensemble

Ce guide explique comment utiliser les nouveaux outils créés lors de la refactorisation Pythonique.

---

## 1. Décorateurs (`utils/decorators.py`)

### `@log_execution`

Enregistre automatiquement l'exécution d'une fonction.

```python
from utils.decorators import log_execution

@log_execution
def process_invoice(invoice_id):
    # Logs: "→ Ejecutando: module.process_invoice"
    # ... code ...
    # Logs: "✓ Completado: module.process_invoice"
    return result
```

**Quand l'utiliser :**
- Fonctions critiques
- Debugging
- Traçabilité des opérations

---

### `@log_performance`

Mesure et enregistre le temps d'exécution.

```python
from utils.decorators import log_performance

@log_performance(threshold_seconds=0.1)
def get_all_invoices():
    # Si l'exécution prend > 0.1s, un warning est enregistré
    return invoices
```

**Quand l'utiliser :**
- Requêtes de base de données
- Opérations I/O
- Calculs complexes

---

### `@retry_on_error`

Réessaie automatiquement en cas d'erreur.

```python
from utils.decorators import retry_on_error

@retry_on_error(max_attempts=3, delay_seconds=1.0)
def connect_to_database():
    # Réessaie jusqu'à 3 fois avec 1s de délai
    return connection
```

**Quand l'utiliser :**
- Connexions réseau/base de données
- Opérations qui peuvent échouer temporairement
- APIs externes

---

### `@handle_exceptions`

Capture les exceptions et retourne une valeur par défaut.

```python
from utils.decorators import handle_exceptions

@handle_exceptions(default_return=[], log_traceback=True)
def get_clients():
    # En cas d'erreur, retourne [] au lieu de lever une exception
    return clients
```

**Quand l'utiliser :**
- Code UI qui ne doit pas crasher
- Fonctions avec fallback
- Opérations non critiques

---

### `@validate_params`

Valide les paramètres d'une fonction.

```python
from utils.decorators import validate_params

@validate_params(
    price=lambda v: v > 0,
    quantity=lambda v: v >= 0
)
def add_product(name, price, quantity):
    # Lève ValueError si price <= 0 ou quantity < 0
    pass
```

**Quand l'utiliser :**
- Validation de données d'entrée
- Préconditions de fonctions
- Contrats de méthodes

---

## 2. Exceptions (`utils/exceptions.py`)

### Hiérarchie

```
FacturacionError (base)
├── DatabaseError
│   ├── DatabaseConnectionError
│   ├── DatabaseQueryError
│   └── DatabaseIntegrityError
├── ValidationError
│   ├── ClientValidationError
│   ├── ProductValidationError
│   └── InvoiceValidationError
├── BusinessLogicError
│   ├── InsufficientStockError
│   └── DuplicateInvoiceNumberError
├── DataNotFoundError
│   ├── ClientNotFoundError
│   ├── ProductNotFoundError
│   └── InvoiceNotFoundError
└── ... (autres)
```

### Utilisation

```python
from utils.exceptions import (
    ClientNotFoundError,
    InsufficientStockError,
    ValidationError
)

# Lever une exception
def get_client(client_id):
    client = db.query(...)
    if not client:
        raise ClientNotFoundError(client_id)
    return client

# Capturer une exception
try:
    client = get_client(999)
except ClientNotFoundError as e:
    print(f"Client {e.details['id']} non trouvé")
    # Afficher un message à l'utilisateur
```

### Exceptions avec détails

```python
from utils.exceptions import InsufficientStockError

# Créer une exception avec détails
raise InsufficientStockError(
    product_name="Producto A",
    requested=10,
    available=5
)

# Accéder aux détails
try:
    check_stock(...)
except InsufficientStockError as e:
    print(f"Produit: {e.details['producto']}")
    print(f"Demandé: {e.details['solicitado']}")
    print(f"Disponible: {e.details['disponible']}")
```

---

## 3. DatabaseEnhanced (`database/database_enhanced.py`)

### Utilisation

```python
from database.database_enhanced import DatabaseEnhanced

# Créer une instance
db = DatabaseEnhanced()

# Méthodes qui lèvent des exceptions typées
try:
    client = db.get_client_by_id(999)
except ClientNotFoundError:
    print("Client non trouvé")

try:
    product = db.get_product_by_id(123)
except ProductNotFoundError:
    print("Produit non trouvé")

# Vérifier le stock
try:
    db.check_stock_availability(product_id=1, quantity=10)
except InsufficientStockError as e:
    print(f"Stock insuffisant: {e}")

# Méthodes safe (ne lèvent pas d'exceptions)
clients = db.safe_get_all_clients()  # Retourne [] en cas d'erreur
products = db.safe_get_all_products()  # Retourne [] en cas d'erreur
```

---

## 4. Patterns recommandés

### Pattern 1 : Fonction critique avec retry et logging

```python
@log_execution
@retry_on_error(max_attempts=3, delay_seconds=0.5)
@log_performance(threshold_seconds=0.2)
def save_invoice(invoice_data):
    # Fonction critique avec:
    # - Logging automatique
    # - Retry en cas d'erreur
    # - Mesure de performance
    return db.add_invoice(invoice_data)
```

### Pattern 2 : Fonction UI safe

```python
@handle_exceptions(default_return=[], log_traceback=True)
@log_performance(threshold_seconds=0.1)
def load_clients_for_ui():
    # Fonction UI qui:
    # - Ne crashe jamais (retourne [])
    # - Log les erreurs
    # - Mesure la performance
    return db.get_all_clients()
```

### Pattern 3 : Validation avec exceptions typées

```python
@validate_params(
    client_data=lambda v: isinstance(v, dict),
    client_data=lambda v: 'nombre' in v
)
def create_client(client_data):
    # Valide les paramètres
    # Lève des exceptions typées
    if db.client_exists(client_data['nif']):
        raise ValidationError("Client déjà existant")
    
    return db.add_client(client_data)
```

---

## 5. Migration progressive

### Étape 1 : Ajouter le logging

```python
# Avant
def get_clients():
    return db.execute_query("SELECT * FROM clientes")

# Après
@log_performance(threshold_seconds=0.1)
def get_clients():
    return db.execute_query("SELECT * FROM clientes")
```

### Étape 2 : Ajouter les exceptions typées

```python
# Avant
def get_client(client_id):
    client = db.get_client_by_id(client_id)
    if not client:
        return None
    return client

# Après
def get_client(client_id):
    client = db.get_client_by_id(client_id)
    if not client:
        raise ClientNotFoundError(client_id)
    return client
```

### Étape 3 : Utiliser DatabaseEnhanced

```python
# Avant
from database.database import Database
db = Database()

# Après
from database.database_enhanced import DatabaseEnhanced
db = DatabaseEnhanced()
```

---

## ✅ Checklist de migration

- [ ] Identifier les fonctions critiques
- [ ] Ajouter `@log_performance` sur les requêtes DB
- [ ] Ajouter `@retry_on_error` sur les connexions
- [ ] Remplacer `return None` par des exceptions typées
- [ ] Utiliser `@handle_exceptions` pour le code UI
- [ ] Ajouter `@validate_params` sur les fonctions publiques
- [ ] Tester avec les nouveaux décorateurs
- [ ] Vérifier les logs
- [ ] Documenter les changements

