# Facturación Fácil

Aplicación de facturación simple con gestión de productos, stock y clientes desarrollada en Python con CustomTkinter.

## Características

- ✅ **Gestión de Productos**: CRUD completo con imágenes, categorías, precios e IVA
- 🏢 **Datos de Organización**: Configuración de empresa con logo
- 📦 **Gestión de Stock**: Control de inventario automático con confirmación
- 🧾 **Facturación**: Creación de facturas con cálculos automáticos
- 📄 **Exportación PDF**: Generación profesional de facturas en PDF
- 🔄 **Actualización Automática**: Stock se actualiza al guardar facturas
- 🛡️ **Sistema Robusto**: Múltiples fallbacks para máxima compatibilidad
- 🌍 **Multiidioma**: Interfaz en español (fácilmente extensible)
- 💾 **Base de datos SQLite**: Sin configuración adicional
- 🖥️ **Multiplataforma**: Funciona en Linux y Windows

## Requisitos

- Python 3.13+ (recomendado usar pyenv)
- CustomTkinter 5.2.2+
- Pillow 10.4.0+
- ReportLab 4.2.2+

## Instalación

### **Instalación Automática (Recomendada)**
```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd facturacion_facil

# Ejecutar script de despliegue
python3 deploy/deploy_solution.py
```

### **Instalación Manual**
```bash
# 1. Instalar dependencias
pip install customtkinter reportlab pillow

# 2. Inicializar base de datos
python3 -c "from database.database import db; db.init_database()"

# 3. Ejecutar aplicación
python3 main.py
```

### **Verificación de Instalación**
```bash
# Test completo del sistema
python3 test/demo/demo_complete_solution_test.py

# Validación del sistema
python3 test/validate_solution.py
```

## 🎯 **Funcionalidades Principales**

### **🔄 Actualización Automática de Stock**
- **Confirmación inteligente**: Diálogo aparece al guardar facturas
- **Sistema robusto**: Múltiples fallbacks (CustomTkinter → tkinter → consola)
- **Logging detallado**: Seguimiento completo de operaciones
- **Validación**: Verificación de stock disponible antes de venta

### **📄 Exportación PDF Profesional**
- **Selección fácil**: Clic en factura de la lista para seleccionar
- **Generación automática**: PDF se crea y abre automáticamente
- **Diseño profesional**: Formato empresarial completo
- **Datos completos**: Empresa, cliente, productos, totales, IVA

### **🛠️ Herramientas de Diagnóstico**
- **Monitor en tiempo real**: Seguimiento de actividad del sistema
- **Tests automatizados**: Validación completa de funcionalidades
- **Benchmark de performance**: Medición de velocidad del sistema
- **Stress testing**: Pruebas bajo carga alta

---

## Estructura del Proyecto

```
facturacion_facil/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
├── docs/                  # 📚 Documentación organizada
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

## 📚 Documentación

La documentación completa del proyecto está organizada en el directorio `docs/`:

- **[docs/README.md](docs/README.md)** - Índice de toda la documentación
- **[docs/architecture/](docs/architecture/)** - Arquitectura y factorización del código
- **[docs/features/](docs/features/)** - Nuevas funcionalidades implementadas
- **[docs/fixes/](docs/fixes/)** - Correcciones y resoluciones de bugs
- **[docs/implementation/](docs/implementation/)** - Detalles de implementación

### Documentación Destacada

- **Arquitectura factorizada**: Código simplificado y reutilizable
- **Gestión de archivos**: FileManager, ImageManager, LogoManager
- **Tests organizados**: Suite completa de tests automatizados
- **Funcionalidades**: PDF, stock, numeración, búsqueda
- **Soluciones robustas**: Stock automático y exportación PDF

---

## 🧪 **Herramientas de Testing y Diagnóstico**

### **Tests Rápidos**
```bash
# Test completo del sistema (Stock + PDF)
python3 test/demo/demo_complete_solution_test.py

# Validación completa del sistema
python3 test/validate_solution.py

# Test específico de selección de facturas
python3 test/demo/demo_test_factura_selection.py
```

### **Herramientas de Monitoreo**
```bash
# Monitor en tiempo real
python3 test/demo/demo_real_time_monitor.py

# Benchmark de performance
python3 test/performance/benchmark_solution.py

# Stress test del sistema
python3 test/stress/stress_test_solution.py
```

### **Accesos Directos (después del despliegue)**
```bash
# Ejecutar aplicación
python3 run_app.py

# Test del sistema
python3 test_system.py

# Monitor del sistema
python3 monitor_system.py

# Validar sistema
python3 validate_system.py
```

### **Documentación de Soporte**
- **`docs/USER_GUIDE_STOCK_CONFIRMATION.md`** - Guía de confirmación de stock
- **`docs/USER_GUIDE_PDF_EXPORT.md`** - Guía de exportación PDF
- **`docs/ADMIN_GUIDE.md`** - Guía de administración del sistema
- **`docs/TESTING_GUIDE.md`** - Guía completa de testing

## Licencia

Proyecto de código abierto para uso educativo y comercial.
