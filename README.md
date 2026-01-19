# Facturación Fácil

Aplicación de facturación completa desarrollada en Python con **PyQt5**. Sistema robusto de gestión comercial con todas las funcionalidades esenciales implementadas y probadas.

## 🎯 Estado Actual - **COMPLETAMENTE FUNCIONAL** ✅

- ✅ **Sistema de Productos**: CRUD completo con imágenes, categorías, precios e IVA
- ✅ **Gestión de Organización**: Configuración completa de empresa con logo
- ✅ **Control de Stock**: Inventario automático con actualizaciones en tiempo real
- ✅ **Sistema de Facturación**: Creación, edición y gestión completa de facturas
- ✅ **Exportación PDF**: Generación profesional de facturas con diseño empresarial
- ✅ **Gestión de Clientes**: Base de datos completa de clientes
- ✅ **Relación Stock-Facturas**: Sistema 100% operacional con confirmaciones automáticas
- ✅ **Interfaz Moderna**: PyQt6 con look nativo del sistema operativo
- ✅ **Base de Datos**: SQLite con modelos optimizados y migraciones automáticas
- ✅ **Sistema de Tests**: 243+ tests automatizados con cobertura completa
- ✅ **Arquitectura Modular**: Código bien estructurado y mantenible
- ✅ **Documentación Completa**: Guías de usuario y desarrollador

## 🚀 Características Principales

### **Funcionalidades Comerciales**
- 🏢 **Gestión Empresarial**: Configuración completa con logo y datos fiscales
- 📦 **Control de Inventario**: Stock automático con alertas y movimientos
- 🧾 **Facturación Profesional**: Numeración automática, cálculos de IVA, descuentos
- 👥 **Base de Clientes**: Gestión completa con validaciones opcionales
- 📄 **Exportación PDF**: Facturas profesionales con logo empresarial

### **Características Técnicas**
- ⚡ **Alto Rendimiento**: PyQt5 con optimizaciones de base de datos
- 🛡️ **Sistema Robusto**: Manejo robusto de errores
- 🌍 **Multiidioma**: Interfaz en español (extensible a otros idiomas)
- 🖥️ **Multiplataforma**: Compatible con Linux y Windows
- 🔧 **Arquitectura Modular**: Fácil mantenimiento y extensión

## 📋 Requisitos del Sistema

### **Requisitos Mínimos**
- **Python 3.10+** (recomendado usar pyenv para gestión de versiones)
- **PyQt5** (framework GUI principal)
- **SQLite 3.x** (incluido con Python)
- **4 GB RAM** mínimo
- **100 MB** espacio en disco

### **Dependencias Python**
```bash
PyQt5                  # Framework GUI principal
Pillow>=10.4.0         # Procesamiento de imágenes
reportlab>=4.2.2       # Generación de PDFs
matplotlib>=3.7.0      # Generación de gráficos
pytest>=7.4.3          # Framework de testing
```

### **Framework GUI**

La aplicación utiliza **PyQt5** como framework GUI principal, ofreciendo:

- 🖥️ **Interfaz nativa** del sistema operativo
- ⚡ **Alto rendimiento** y estabilidad
- 🎨 **Widgets modernos** y personalizables

## 🚀 Instalación y Configuración

### **Método 1: Instalación Rápida (Recomendada)**
```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd facturacion_facil

# 2. Activar entorno virtual
source activate.sh

# 3. Ejecutar aplicación
python main.py
```

### **Método 2: Instalación Manual**
```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Inicializar base de datos
python3 -c "from database.database import db; db.init_database()"

# 4. Ejecutar aplicación
python3 main.py
```

### **🔍 Verificación de Instalación**
```bash
# Test completo del sistema (recomendado)
python test/demo/demo_complete_solution_test.py

# Validación de funcionalidades principales
python validation_complete_2024.py

# Suite completa de tests
./run_organized_tests.sh all
```

### **🛠️ Herramientas de Diagnóstico**
```bash
# Limpiar base de datos
./clean_databases.sh

# Monitor en tiempo real
python test/demo/demo_real_time_monitor.py

# Benchmark de rendimiento
python test/performance/benchmark_solution.py
```

## 🎯 **Funcionalidades Implementadas**

### **📊 Gestión Comercial Completa**
- **Productos**: CRUD completo con imágenes, categorías, precios, IVA
- **Clientes**: Base de datos con validaciones opcionales (NIF, email, teléfono)
- **Organización**: Configuración empresarial completa con logo
- **Stock**: Control automático de inventario con movimientos detallados
- **Facturación**: Sistema completo con numeración automática y cálculos

### **🔄 Sistema de Stock Inteligente**
- **Actualización automática**: Stock se actualiza al guardar facturas
- **Confirmación inteligente**: Diálogos de confirmación robustos
- **Validación de disponibilidad**: Verificación antes de venta
- **Historial de movimientos**: Seguimiento completo de cambios
- **Alertas de stock bajo**: Notificaciones automáticas

### **📄 Exportación PDF Profesional**
- **Diseño empresarial**: Facturas con logo y datos completos
- **Generación automática**: PDF se crea y abre automáticamente
- **Selección intuitiva**: Clic en factura para seleccionar y exportar
- **Formato profesional**: Layout optimizado para impresión
- **Datos completos**: Cliente, productos, totales, IVA, descuentos

### **🧪 Sistema de Testing Robusto**
- **243+ tests automatizados**: Cobertura completa de funcionalidades
- **Tests de integración**: Verificación de flujos completos
- **Tests de rendimiento**: Benchmark y stress testing
- **Validación continua**: Tests ejecutables en cualquier momento
- **Herramientas de diagnóstico**: Monitor en tiempo real y análisis

---

## 📁 Estructura del Proyecto

```
facturacion_facil/
├── 🚀 main.py                    # Punto de entrada principal (PyQt6)
├── 📋 requirements.txt           # Dependencias del proyecto
├── 🔧 activate.sh               # Script de activación del entorno
├── 🧹 clean_databases.sh        # Herramienta de limpieza de datos
├── 📚 README.md                 # Documentación principal
│
├── 💾 database/                 # Sistema de base de datos
│   ├── database.py              # Conexión SQLite y migraciones
│   ├── models.py                # Modelos: Producto, Cliente, Factura, Stock
│   └── optimized_models.py      # Modelos optimizados para rendimiento
│
├── 🖥️ gui/                      # Gestión de GUI
│   ├── abstract_gui.py          # Interfaces abstractas
│   ├── gui_manager.py           # Gestor de frameworks
│   └── abstract_components.py   # Componentes reutilizables
│
├── 🎨 ui/                       # Interfaces de usuario
│   ├── main_window_pyqt5.py     # Ventana principal (PyQt5)
│   ├── productos_pyqt5.py       # Gestión completa de productos
│   ├── organizacion_pyqt5.py    # Configuración empresarial
│   ├── stock_pyqt5.py           # Control de inventario
│   ├── facturas_pyqt5.py        # Sistema de facturación
│   ├── clientes_pyqt5.py        # Gestión de clientes
│   └── widgets/                 # Widgets personalizados
│
├── 🛠️ utils/                    # Utilidades del sistema
│   ├── translations.py          # Sistema de traducciones
│   ├── logger.py                # Sistema de logging
│   ├── pdf_generator.py         # Generador de PDFs
│   ├── config.py                # Configuración de la aplicación
│   └── file_manager.py          # Gestión de archivos
│
├── 🧪 test/                     # Suite completa de tests
│   ├── demo/                    # Tests de demostración
│   ├── unit/                    # Tests unitarios
│   ├── integration/             # Tests de integración
│   ├── performance/             # Tests de rendimiento
│   └── validate_solution.py     # Validación completa del sistema
│
├── 📚 docs/                     # Documentación completa
│   ├── README.md                # Índice de documentación
│   ├── architecture/            # Documentación de arquitectura
│   ├── features/                # Documentación de funcionalidades
│   └── implementation/          # Detalles de implementación
│
├── 📄 assets/                   # Recursos del proyecto
│   ├── images/                  # Imágenes de productos
│   ├── logos/                   # Logos empresariales
│   └── icons/                   # Iconos de la aplicación
│
├── 📊 data/                     # Datos de configuración
├── 📝 logs/                     # Archivos de log
├── 📋 facturas_pdf/             # PDFs generados
└── 🔧 scripts/                  # Scripts de utilidad
```

---

## 🚀 **PyQt5: Interfaz Moderna y Estable**

### **¿Por qué PyQt5?**

La aplicación utiliza **PyQt5** como framework GUI principal:

- ⚡ **Alto rendimiento** y estabilidad probada
- 🖥️ **Interfaz nativa** con look and feel del sistema operativo
- 🎨 **Widgets modernos** y personalizables
- 🔧 **Excelente compatibilidad** con Linux y Windows
- 🎯 **Soporte completo** de funcionalidades avanzadas

### **Arquitectura GUI**

```python
# La aplicación utiliza PyQt5 como framework principal
from gui import set_gui_framework

set_gui_framework('pyqt5')  # Framework principal
```

### **Ventajas de PyQt5**

| Característica | Beneficio |
|----------------|-----------|
| **Rendimiento** | Interfaz rápida y fluida |
| **Estabilidad** | Framework maduro y probado |
| **Widgets** | Componentes ricos y nativos |
| **Comunidad** | Amplio soporte y documentación |

---

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

## 📊 Estado del Desarrollo - **COMPLETADO** ✅

### ✅ **Funcionalidades Principales Implementadas**
- ✅ **Sistema de Productos**: CRUD completo con imágenes y categorías
- ✅ **Gestión de Organización**: Configuración empresarial completa con logo
- ✅ **Control de Stock**: Inventario automático con movimientos y alertas
- ✅ **Sistema de Facturación**: Creación, edición, numeración automática
- ✅ **Gestión de Clientes**: Base de datos completa con validaciones
- ✅ **Exportación PDF**: Generación profesional de facturas
- ✅ **Base de Datos**: SQLite con modelos optimizados y migraciones
- ✅ **Interfaz PyQt5**: Moderna, nativa y de alto rendimiento
- ✅ **Sistema de Tests**: 243+ tests automatizados con cobertura completa
- ✅ **Documentación**: Guías completas de usuario y desarrollador

### 🎯 **Funcionalidades Avanzadas Disponibles**
- ✅ **Numeración Inteligente**: Sistema FACT-XXX-2025 automático
- ✅ **Validaciones Opcionales**: NIF, email, teléfono configurables
- ✅ **Mensajes Copiables**: Todos los diálogos con botón copiar
- ✅ **Arquitectura Modular**: Código bien estructurado y mantenible
- ✅ **Sistema de Logging**: Seguimiento completo de operaciones
- ✅ **Herramientas de Diagnóstico**: Monitor, benchmark, validación

### 🚀 **Próximas Mejoras Posibles**
- 📊 **Reportes Avanzados**: Estadísticas de ventas y análisis
- 💾 **Backup Automático**: Respaldo programado de datos
- 🌐 **API REST**: Backend para aplicaciones móviles
- 📱 **Aplicación Móvil**: Versión para tablets y smartphones
- 🎨 **Temas Personalizados**: Modo oscuro y colores empresariales

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

## Tests - Version 2024 ✅

### **🎯 Tests Stocks-Factures (NOUVEAUX)**
```bash
# Validation complète du système 2024
python validation_complete_2024.py

# Test complet relation stocks-factures
python test_relation_stocks_factures_complet.py

# Test bouton Actualizar corrigé
python test_bouton_actualizar.py

# Test boutons +/- avec symboles
python test_symboles_boutons.py

# Démonstration fonctionnelle
python demo_relation_stocks_factures.py
```

### **📚 Documentation Mise à Jour**
```bash
# Guide complet 2024
GUIDE_COMPLET_STOCKS_FACTURES_2024.md

# Documentation technique
DOCUMENTATION_TECHNIQUE_STOCKS.md

# Index complet
INDEX_TESTS_ET_DOCUMENTATION.md
```

### Ejecutar tests legacy
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
- **Interface**: Tests de widgets PyQt5
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
- **Funcionalidades**: PDF, stock, numeración
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
