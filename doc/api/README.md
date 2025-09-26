# 🔌 Documentation API

## 📋 **Description**
Documentation des interfaces de programmation - APIs, modules et interfaces pour développeurs.

## 📁 **Contenu du Répertoire**
```
api/
├── README.md                    # Ce guide
├── [futurs documents API]
└── [références modules]
```

## 🎯 **Objectifs de la Documentation API**

### **Pour les Développeurs**
- Interfaces de programmation disponibles
- Modules et classes principales
- Méthodes et paramètres détaillés
- Exemples d'utilisation et intégration

### **Pour l'Intégration**
- APIs publiques et privées
- Formats de données et protocoles
- Authentification et sécurité
- Gestion d'erreurs et codes de retour

## 📖 **Structure API du Projet**

### **🏗️ Modules Principaux**

#### **Database (`database/`)**
```python
# Modèles de données
from database.models import Organizacion, Producto, Factura, FacturaItem

# Gestionnaire de base de données
from database.database import DatabaseManager

# Exemples d'utilisation
db = DatabaseManager()
productos = db.get_all_productos()
```

#### **Interface Utilisateur (`ui/`)**
```python
# Fenêtres principales
from ui.main_window import MainWindow
from ui.productos import ProductosWindow
from ui.facturas import FacturasWindow

# Composants spécialisés
from ui.producto_list_widget import ProductoListWidget
from ui.configuracion_facturas import ConfiguracionFacturas
```

#### **Utilitaires (`utils/`)**
```python
# Génération PDF
from utils.pdf_generator import PDFGenerator

# Gestion d'images
from utils.image_utils import ImageUtils

# Configuration
from utils.config import ConfigManager

# Logging
from utils.logger import get_logger
```

#### **Composants Communs (`common/`)**
```python
# Dialogs personnalisés
from common.custom_dialogs import CustomDialog

# Composants UI réutilisables
from common.ui_components import UIComponents

# Validateurs
from common.validators import Validators
```

## 🔧 **APIs Principales**

### **📊 API Base de Données**

#### **Gestion des Produits**
```python
from database.models import Producto

# Création
producto = Producto(
    nombre="Producto Test",
    precio=99.99,
    iva_porcentaje=21.0,
    imagen_path="/path/to/image.jpg"
)

# Sauvegarde
producto.save()

# Recherche
productos = Producto.get_all()
producto = Producto.get_by_id(1)
```

#### **Gestion des Facturas**
```python
from database.models import Factura, FacturaItem

# Création factura
factura = Factura(
    numero="FAC-001",
    organizacion_id=1,
    fecha=datetime.now()
)

# Ajout d'items
item = FacturaItem(
    factura=factura,
    producto_id=1,
    cantidad=2,
    precio_unitario=99.99
)
```

### **🖼️ API Gestion d'Images**

#### **Utilitaires d'Images**
```python
from utils.image_utils import ImageUtils

# Création mini image
image_utils = ImageUtils()
mini_image = image_utils.create_mini_image(
    image_path="/path/to/image.jpg",
    size=(32, 32)
)

# Cache d'images
cached_image = image_utils.get_cached_mini_image(
    image_path="/path/to/image.jpg",
    size=(32, 32)
)

# Image placeholder
placeholder = image_utils.create_placeholder_image(size=(32, 32))
```

### **📄 API Génération PDF**

#### **Générateur PDF**
```python
from utils.pdf_generator import PDFGenerator

# Configuration
pdf_gen = PDFGenerator()

# Génération factura
pdf_path = pdf_gen.generar_factura_pdf(
    factura=factura,
    output_dir="/path/to/output",
    open_after_generation=True
)
```

### **⚙️ API Configuration**

#### **Gestionnaire de Configuration**
```python
from utils.config import ConfigManager

# Lecture configuration
config = ConfigManager()
pdf_dir = config.get_pdf_directory()
visor_pdf = config.get_pdf_viewer()

# Écriture configuration
config.set_pdf_directory("/new/path")
config.set_pdf_viewer("/path/to/viewer")
config.save()
```

## 🚀 **Utilisation des APIs**

### **Développement de Nouvelles Fonctionnalités**
```python
# 1. Importer les modules nécessaires
from database.models import Producto
from utils.image_utils import ImageUtils
from utils.logger import get_logger

# 2. Initialiser les composants
logger = get_logger("nouvelle_fonctionnalite")
image_utils = ImageUtils()

# 3. Implémenter la logique
def nouvelle_fonctionnalite():
    try:
        # Logique métier
        productos = Producto.get_all()
        for producto in productos:
            if producto.imagen_path:
                mini_image = image_utils.create_mini_image(
                    producto.imagen_path
                )
        logger.info("Fonctionnalité exécutée avec succès")
    except Exception as e:
        logger.error(f"Erreur: {e}")
```

### **Intégration Interface Utilisateur**
```python
# 1. Hériter des classes de base
import customtkinter as ctk
from ui.base_window import BaseWindow

class NouvelleWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Configuration interface
        pass
```

### **Extension du Système**
```python
# 1. Créer nouveaux modèles
from database.models import BaseModel

class NouveauModel(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Propriétés spécifiques
    
    def save(self):
        # Logique de sauvegarde
        pass
```

## 📊 **Formats de Données**

### **Modèles de Base de Données**

#### **Producto**
```json
{
    "id": 1,
    "nombre": "Producto Test",
    "precio": 99.99,
    "iva_porcentaje": 21.0,
    "imagen_path": "/path/to/image.jpg",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}
```

#### **Factura**
```json
{
    "id": 1,
    "numero": "FAC-001",
    "organizacion_id": 1,
    "fecha": "2024-01-01",
    "subtotal": 199.98,
    "iva_total": 41.99,
    "total": 241.97,
    "items": [
        {
            "producto_id": 1,
            "cantidad": 2,
            "precio_unitario": 99.99
        }
    ]
}
```

### **Configuration**
```json
{
    "pdf": {
        "default_directory": "/path/to/pdfs",
        "viewer_path": "/path/to/viewer",
        "auto_open": true
    },
    "images": {
        "cache_enabled": true,
        "max_cache_size": 100,
        "default_size": [32, 32]
    }
}
```

## 🔒 **Sécurité et Bonnes Pratiques**

### **Validation des Données**
```python
from common.validators import Validators

# Validation prix
if not Validators.validate_price(precio):
    raise ValueError("Prix invalide")

# Validation email
if not Validators.validate_email(email):
    raise ValueError("Email invalide")
```

### **Gestion d'Erreurs**
```python
from utils.logger import get_logger

logger = get_logger("api_module")

try:
    # Opération API
    result = api_operation()
except ValidationError as e:
    logger.warning(f"Erreur de validation: {e}")
    raise
except DatabaseError as e:
    logger.error(f"Erreur base de données: {e}")
    raise
except Exception as e:
    logger.error(f"Erreur inattendue: {e}")
    raise
```

### **Logging et Monitoring**
```python
from utils.logger import get_logger

# Logger spécialisé
logger = get_logger("api_component")

# Niveaux de log
logger.debug("Information de debug")
logger.info("Information générale")
logger.warning("Avertissement")
logger.error("Erreur")
logger.critical("Erreur critique")
```

## 🧪 **Tests des APIs**

### **Tests Unitaires**
```bash
# Tests des modèles
./run_organized_tests.sh unit -k models

# Tests des utilitaires
./run_organized_tests.sh unit -k utils

# Tests de validation
./run_organized_tests.sh unit -k validators
```

### **Tests d'Intégration**
```bash
# Tests d'intégration API
./run_organized_tests.sh integration -k api

# Tests de workflow complet
./run_organized_tests.sh integration -k workflow
```

### **Tests de Performance**
```bash
# Performance des APIs
./run_organized_tests.sh performance --benchmark-only
```

## 📋 **Checklist Développement API**

### **Nouvelle API**
- [ ] Interface clairement définie
- [ ] Documentation complète
- [ ] Validation des paramètres
- [ ] Gestion d'erreurs appropriée
- [ ] Tests unitaires créés
- [ ] Tests d'intégration validés
- [ ] Logging implémenté
- [ ] Performance validée

### **Maintenance API**
- [ ] Rétrocompatibilité préservée
- [ ] Documentation mise à jour
- [ ] Tests de régression passent
- [ ] Performance maintenue
- [ ] Sécurité validée

## 🔄 **Évolution des APIs**

### **Versioning**
- **Compatibilité** : Maintenir rétrocompatibilité
- **Dépréciation** : Processus de dépréciation graduelle
- **Migration** : Guides de migration pour changements majeurs

### **Extension**
- **Nouveaux modules** : Suivre patterns existants
- **Nouvelles méthodes** : Cohérence avec APIs existantes
- **Documentation** : Maintenir documentation à jour

---

**🔌 Cette documentation API facilite le développement et l'intégration !**

**Pour plus d'informations, consultez :**
- **Technique** : `../technical/README.md`
- **Tests** : `../../test/README.md`
- **Utilisateur** : `../user/README.md`
