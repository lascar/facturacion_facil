# Facturación Fácil

Aplicación de facturación simple con gestión de productos, stock y clientes desarrollada en Python con CustomTkinter.

## Características

- ✅ **Gestión de Productos**: CRUD completo con imágenes, categorías, precios e IVA
- 🏢 **Datos de Organización**: Configuración de empresa con logo
- 📦 **Gestión de Stock**: Control de inventario automático
- 🧾 **Facturación**: Creación de facturas con cálculos automáticos
- 🌍 **Multiidioma**: Interfaz en español (fácilmente extensible)
- 💾 **Base de datos SQLite**: Sin configuración adicional
- 🖥️ **Multiplataforma**: Funciona en Linux y Windows

## Requisitos

- Python 3.13+ (recomendado usar pyenv)
- CustomTkinter 5.2.2+
- Pillow 10.4.0+
- ReportLab 4.2.2+

## Instalación

### 1. Clonar o descargar el proyecto
```bash
cd facturacion_facil
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
python main.py
```

## Estructura del Proyecto

```
facturacion_facil/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
├── database/
│   ├── __init__.py
│   ├── database.py        # Conexión SQLite
│   └── models.py          # Modelos de datos
├── ui/
│   ├── __init__.py
│   ├── main_window.py     # Ventana principal
│   ├── productos.py       # Gestión de productos
│   ├── organizacion.py    # Configuración empresa
│   ├── stock.py           # Gestión de stock
│   └── facturas.py        # Creación de facturas
├── utils/
│   ├── __init__.py
│   └── translations.py    # Textos en español
└── assets/
    ├── images/            # Imágenes de productos
    └── logos/             # Logos de empresa
```

## Base de Datos

La aplicación utiliza SQLite con las siguientes tablas:

- **productos**: Información de productos (nombre, referencia, precio, IVA, etc.)
- **organizacion**: Datos de la empresa
- **stock**: Cantidades disponibles por producto
- **facturas**: Cabeceras de facturas
- **factura_items**: Líneas de detalle de facturas

## Uso

### 1. Configurar Organización
- Ir a "Organización" y completar los datos de tu empresa
- Subir logo (opcional)

### 2. Agregar Productos
- Ir a "Productos" → "Nuevo Producto"
- Completar información: nombre, referencia, precio, IVA, etc.
- Subir imagen del producto (opcional)

### 3. Gestionar Stock
- Ir a "Stock" para ver y actualizar cantidades disponibles
- El stock se actualiza automáticamente con cada factura

### 4. Crear Facturas
- Ir a "Nueva Factura"
- Completar datos del cliente
- Agregar productos y cantidades
- La aplicación calcula automáticamente totales e IVA

## Estado del Desarrollo

### ✅ Completado
- Estructura base del proyecto
- Configuración de base de datos
- Modelos de datos
- Ventana principal con navegación
- Gestión completa de productos
- Sistema de traducciones

### 🚧 En Desarrollo
- Ventana de organización (formulario completo)
- Ventana de stock (lista y edición)
- Ventana de facturas (formulario y generación PDF)
- Generador de PDF para facturas
- Validaciones adicionales

### 📋 Por Hacer
- Búsqueda y filtros en listas
- Backup y restauración de datos
- Reportes de ventas
- Configuración de impuestos personalizados
- Exportación a Excel

## Personalización

### Cambiar Idioma
Editar `utils/translations.py` para modificar textos o agregar nuevos idiomas.

### Modificar Colores
Los colores se pueden cambiar en cada ventana modificando los parámetros `fg_color` y `hover_color` de los botones.

### Agregar Campos
Para agregar nuevos campos a productos o facturas:
1. Modificar la tabla en `database/database.py`
2. Actualizar el modelo en `database/models.py`
3. Agregar campos en la interfaz correspondiente

## Distribución

Para crear un ejecutable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Soporte

Esta aplicación está diseñada para ser simple y fácil de modificar. El código está bien comentado y estructurado para facilitar el mantenimiento y las extensiones.

## Tests

### Instalación de dependencias de test
```bash
pip install -r requirements-dev.txt
```

### Ejecutar tests
```bash
# Todos los tests
python run_tests.py
# o
make test

# Tests específicos
python run_tests.py unit      # Tests de base de datos
python run_tests.py ui        # Tests de interfaz
python run_tests.py utils     # Tests de utilidades
python run_tests.py coverage  # Con reporte de cobertura

# Usando make
make test-unit
make test-coverage
make lint
make format
```

### Estructura de tests
```
tests/
├── conftest.py              # Fixtures communes
├── test_database/
│   ├── test_database.py     # Tests de connexion DB
│   └── test_models.py       # Tests des modèles
├── test_ui/
│   └── test_productos.py    # Tests interface produits
└── test_utils/
    └── test_translations.py # Tests traductions
```

### Couverture de tests
- **Base de données**: Tests complets avec SQLite temporaire
- **Modèles**: CRUD, validations, relations
- **Interface**: Mocking des widgets CustomTkinter
- **Traductions**: Vérification complétude et cohérence
- **Données fake**: Génération avec Faker en espagnol

### Commandes utiles
```bash
# Vérification complète avant commit
make dev-check

# Nettoyage
make clean

# Information du projet
make info
```

## Licencia

Proyecto de código abierto para uso educativo y comercial.
