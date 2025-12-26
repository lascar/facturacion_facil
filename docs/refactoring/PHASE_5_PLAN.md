# Phase 5 : Refactorisation UI - Plan détaillé

## 📋 Objectifs

Séparer la logique métier de la présentation dans les fichiers UI, en appliquant les décorateurs et exceptions de la Phase 4.

## État : 🚀 EN COURS

### ✅ Étape 1 : Services de Base - COMPLÈTE
- ✅ 4 services créés (ProductoService, ClienteService, OrganizacionService, FacturaService)
- ✅ 63 tests créés (17 + 15 + 13 + 11 + 18)
- ✅ Tous les tests passent (510 total)
- ✅ Coverage : 57-83% selon les services

### ✅ Étape 2 : Refactorisation `ui/productos_pyqt5.py` - COMPLÈTE
- ✅ Remplacé tous les appels `db_improved.*` par `ProductoService`
- ✅ Ajouté gestion d'erreurs typées (ProductValidationError, ProductNotFoundError, DatabaseError)
- ✅ 8 tests behaviour passent
- ✅ 510 tests total passent - aucune régression
- ✅ Coverage UI : 49% (était 0%)

---

## 🎯 Fichiers cibles (par priorité)

### 1. **facturas_pyqt5.py** (2511 lignes) - PRIORITÉ HAUTE
**Problèmes identifiés :**
- Logique métier mélangée avec la présentation
- Méthodes très longues (> 100 lignes)
- Pas de gestion d'erreurs typée
- Pas de logging de performance
- Duplication de code

**Actions à entreprendre :**
- Extraire la logique métier dans `services/factura_service.py`
- Appliquer `@log_performance` sur les méthodes lentes
- Utiliser les exceptions typées (`InvoiceNotFoundError`, etc.)
- Créer des méthodes helper pour réduire la duplication
- Séparer en plusieurs fichiers si nécessaire

### 2. **organizacion_pyqt5.py** (982 lignes) - PRIORITÉ MOYENNE
**Problèmes identifiés :**
- Logique de validation mélangée avec l'UI
- Pas de gestion d'erreurs robuste
- Méthodes longues

**Actions à entreprendre :**
- Extraire la logique dans `services/organizacion_service.py`
- Appliquer les décorateurs de validation
- Utiliser les exceptions typées

### 3. **client_autocomplete_widget.py** (726 lignes) - PRIORITÉ MOYENNE
**Problèmes identifiés :**
- Widget complexe avec logique métier
- Pas de séparation claire

**Actions à entreprendre :**
- Extraire la logique de recherche dans un service
- Appliquer `@log_performance` sur la recherche
- Simplifier le widget

### 4. **productos_pyqt5.py** (575 lignes) - PRIORITÉ BASSE
**Problèmes identifiés :**
- Similaire à facturas mais plus petit
- Logique métier mélangée

**Actions à entreprendre :**
- Extraire la logique dans `services/producto_service.py`
- Appliquer les décorateurs et exceptions

---

## 🏗️ Architecture proposée

### Nouvelle structure de dossiers

```
services/
├── __init__.py
├── base_service.py          # Classe de base avec décorateurs
├── factura_service.py       # Logique métier des factures
├── producto_service.py      # Logique métier des produits
├── cliente_service.py       # Logique métier des clients
└── organizacion_service.py  # Logique métier de l'organisation

ui/
├── facturas_pyqt5.py        # UI pure (réduit à ~800 lignes)
├── productos_pyqt5.py       # UI pure
├── clientes_pyqt5.py        # UI pure
└── organizacion_pyqt5.py    # UI pure
```

### Classe de base pour les services

```python
# services/base_service.py
from utils.decorators import log_execution, log_performance, retry_on_error
from utils.exceptions import *
from database.database import Database

class BaseService:
    """Classe de base pour tous les services métier"""
    
    def __init__(self):
        self.db = Database()
        self.logger = get_logger(self.__class__.__name__)
    
    @retry_on_error(max_attempts=3, delay_seconds=0.5)
    def get_connection(self):
        """Obtenir une connexion avec retry"""
        return self.db.get_connection()
```

---

## 📝 Exemple de refactorisation

### Avant (facturas_pyqt5.py)

```python
def save_factura(self):
    """Sauvegarder la facture"""
    try:
        # Validation
        if not self.numero_edit.text():
            QMessageBox.warning(self, "Error", "Número requerido")
            return
        
        # Logique métier
        factura_data = {
            'numero': self.numero_edit.text(),
            'cliente_id': self.cliente_id,
            # ... 50 lignes de code ...
        }
        
        # Sauvegarde
        conn = self.database.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO facturas ...")
        conn.commit()
        conn.close()
        
        QMessageBox.information(self, "Éxito", "Factura guardada")
        
    except Exception as e:
        QMessageBox.critical(self, "Error", str(e))
```

### Après (séparation UI / Service)

```python
# ui/facturas_pyqt5.py (UI pure)
def save_factura(self):
    """Sauvegarder la facture (UI)"""
    try:
        # Validation UI simple
        if not self.numero_edit.text():
            QMessageBox.warning(self, "Error", "Número requerido")
            return
        
        # Appel au service
        factura_data = self._collect_form_data()
        factura_id = self.factura_service.save_factura(factura_data)
        
        QMessageBox.information(self, "Éxito", f"Factura {factura_id} guardada")
        self.load_facturas()
        
    except InvoiceValidationError as e:
        QMessageBox.warning(self, "Validación", str(e))
    except DatabaseError as e:
        QMessageBox.critical(self, "Error de BD", str(e))

# services/factura_service.py (Logique métier)
class FacturaService(BaseService):
    
    @log_execution
    @log_performance(threshold_seconds=0.2)
    def save_factura(self, factura_data):
        """Sauvegarder une facture (logique métier)"""
        # Validation métier
        self._validate_factura_data(factura_data)
        
        # Sauvegarde
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO facturas ...", factura_data)
            factura_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return factura_id
            
        except Exception as e:
            raise DatabaseError(f"Error guardando factura: {e}")
    
    def _validate_factura_data(self, data):
        """Valider les données de facture"""
        if not data.get('numero'):
            raise InvoiceValidationError("Número requerido")
        # ... autres validations ...
```

---

## ✅ Avantages attendus

1. **Code plus maintenable** : Séparation claire UI / Logique
2. **Tests plus faciles** : Services testables indépendamment
3. **Réutilisabilité** : Services utilisables par plusieurs UIs
4. **Meilleure observabilité** : Logging automatique
5. **Gestion d'erreurs robuste** : Exceptions typées
6. **Performance** : Détection des requêtes lentes

---

## 📊 Métriques de succès

- Réduction de 50% de la taille des fichiers UI
- 100% des opérations DB avec logging
- 100% des erreurs avec exceptions typées
- Tous les tests passent (aucune régression)
- Couverture de code > 80% pour les services

