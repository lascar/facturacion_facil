# Tutorial de Uso - Interfaz de Usuario Facturación Fácil

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Ventana Principal](#ventana-principal)
3. [Gestión de Productos](#gestión-de-productos)
4. [Configuración de Organización](#configuración-de-organización)
5. [Gestión de Stock](#gestión-de-stock)
6. [Creación de Facturas](#creación-de-facturas)
7. [Consejos y Trucos](#consejos-y-trucos)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🚀 Introducción

**Facturación Fácil** es una aplicación de gestión empresarial diseñada para pequeñas y medianas empresas. Su interfaz intuitiva permite gestionar productos, stock, clientes y facturas de manera eficiente.

### Características Principales
- ✅ **Interfaz moderna** con CustomTkinter
- 🖱️ **Navegación intuitiva** con botones grandes y claros
- 📱 **Diseño responsivo** que se adapta al tamaño de ventana
- 🎨 **Colores diferenciados** para cada función
- 🔄 **Tri par colonnes** avec indicateurs visuels dans toutes les listes

---

## 🏠 Ventana Principal

### Descripción General
La ventana principal es el centro de control de la aplicación. Desde aquí puedes acceder a todas las funcionalidades.

### Elementos de la Interfaz

#### 🎯 Botones Principales
1. **Productos** (Azul) - Gestión del catálogo de productos
2. **Organización** (Azul) - Configuración de datos de empresa
3. **Stock** (Azul) - Control de inventario
4. **Facturas** (Azul) - Gestión de facturas existentes
5. **Nueva Factura** (Verde) - Crear factura rápidamente
6. **Salir** (Rojo) - Cerrar la aplicación

#### 📐 Diseño de la Ventana
- **Tamaño inicial**: 800x600 píxeles
- **Redimensionable**: Sí, se adapta al contenido
- **Centrado automático**: La ventana aparece centrada en pantalla
- **Tema**: Claro con acentos azules

### Navegación
- **Un clic** en cualquier botón abre la ventana correspondiente
- **Ventanas múltiples**: Puedes tener varias ventanas abiertas simultáneamente
- **Foco automático**: Las ventanas nuevas aparecen al frente

---

## 📦 Gestión de Productos

### Acceso
Haz clic en el botón **"Productos"** en la ventana principal.

### Interfaz de Productos

#### 📋 Panel Izquierdo - Lista de Productos
- **Lista scrollable** con todos los productos
- **Formato**: `Nombre - Referencia - €Precio`
- **Selección**: Un clic selecciona el producto
- **Actualización automática** al guardar cambios

#### 📝 Panel Derecho - Formulario de Producto

##### Campos Obligatorios (*)
1. **Nombre*** - Nombre del producto
2. **Referencia*** - Código único del producto
3. **Precio*** - Precio unitario en euros

##### Campos Opcionales
4. **Categoría** - Clasificación del producto
5. **IVA Recomendado** - Porcentaje de IVA (por defecto 21%)
6. **Descripción** - Texto libre descriptivo

##### Gestión de Imágenes
- **Botón "Seleccionar Imagen"** - Abre explorador de archivos
- **Formatos soportados**: PNG, JPG, JPEG, GIF, BMP
- **Vista previa** - Muestra la imagen seleccionada
- **Botón "Quitar Imagen"** - Elimina la imagen actual
- **Configuración** (⚙️) - Establece directorio por defecto

#### 🔘 Botones de Acción

##### Primera Fila
- **Nuevo Producto** (Azul Oscuro) - Limpia el formulario para crear producto

##### Segunda Fila
- **Guardar** (Verde) - Guarda el producto actual
- **Eliminar** (Rojo) - Elimina el producto seleccionado

### Flujo de Trabajo

#### ➕ Crear Nuevo Producto
1. Haz clic en **"Nuevo Producto"**
2. Completa los campos obligatorios (*)
3. Agrega imagen si es necesario
4. Haz clic en **"Guardar"**
5. El producto aparece en la lista

#### ✏️ Editar Producto Existente
1. Selecciona el producto en la lista
2. Los datos se cargan automáticamente
3. Modifica los campos necesarios
4. Haz clic en **"Guardar"**

#### 🗑️ Eliminar Producto
1. Selecciona el producto en la lista
2. Haz clic en **"Eliminar"**
3. Confirma la eliminación
4. El producto se elimina permanentemente

#### 🔄 Ordenar Lista de Productos
1. **Clic simple** en cualquier en-tête de colonne (Nom, Référence, Prix, Catégorie)
2. **Tri ascendant** : Les données s'ordonnent de A-Z, 1-100, etc.
3. **Clic double** sur la même colonne pour **tri descendant** (Z-A, 100-1)
4. **Indicateurs visuels** :
   - ↕ : Colonne triable
   - ↑ : Tri ascendant actif
   - ↓ : Tri descendant actif

**Exemples d'utilisation** :
- Cliquer sur "Prix" → Voir les produits du moins cher au plus cher
- Double-clic sur "Nom" → Ordre alphabétique inverse
- Cliquer sur "Catégorie" → Grouper par catégorie

### Validaciones
- **Nombre y Referencia**: No pueden estar vacíos
- **Precio**: Debe ser un número válido ≥ 0
- **IVA**: Debe estar entre 0 y 100%
- **Referencia única**: No se permiten duplicados

---

## 🏢 Configuración de Organización

### Acceso
Haz clic en el botón **"Organización"** en la ventana principal.

### Secciones de Configuración

#### 📋 Datos Básicos de la Empresa
- **Nombre*** (obligatorio) - Razón social
- **CIF/NIF** - Número de identificación fiscal
- **Dirección** - Dirección completa
- **Teléfono** - Número de contacto
- **Email** - Correo electrónico

#### 🖼️ Gestión del Logo
- **Seleccionar Logo** - Abre explorador de archivos
- **Vista previa** - Muestra el logo actual
- **Quitar Logo** - Elimina el logo actual
- **Formatos soportados**: PNG, JPG, JPEG, GIF, BMP
- **Uso**: El logo aparece en las facturas PDF

#### ⚙️ Configuración Avanzada
- **Directorio de Imágenes** - Carpeta por defecto para imágenes de productos
- **Directorio PDF** - Carpeta donde se guardan las facturas PDF
- **Visor PDF** - Programa para abrir PDFs (opcional)
- **Número Inicial de Factura** - Primer número de la secuencia

### Botones de Acción
- **Guardar** (Verde) - Guarda toda la configuración
- **Cancelar** (Gris) - Cierra sin guardar

### Validaciones
- **Nombre**: Obligatorio
- **CIF**: Mínimo 8 caracteres si se proporciona
- **Email**: Formato válido si se proporciona
- **Número inicial**: Debe ser > 0

---

## 📊 Gestión de Stock

### Acceso
Haz clic en el botón **"Stock"** en la ventana principal.

### Interfaz de Stock

#### 🔍 Panel Superior - Búsqueda y Filtros
- **Campo de búsqueda** - Busca por nombre o referencia
- **Filtro "Stock Bajo"** - Muestra solo productos con stock ≤ 5
- **Botón "Actualizar"** - Recarga los datos
- **Contador de resultados** - Muestra productos encontrados

#### 📋 Tabla de Stock
Columnas mostradas:
1. **Producto** - Nombre del producto
2. **Referencia** - Código del producto
3. **Stock Actual** - Cantidad disponible
4. **Estado** - Indicador visual del nivel de stock
5. **Última Actualización** - Fecha del último cambio
6. **Acciones** - Botones de operación

#### 🎨 Códigos de Color del Estado
- 🔴 **Rojo**: Sin Stock (0 unidades)
- 🟠 **Naranja**: Stock Bajo (1-5 unidades)
- 🟡 **Amarillo**: Stock Medio (6-10 unidades)
- 🟢 **Verde**: Stock OK (>10 unidades)

#### 🔘 Botones de Acción por Producto
- **✏️ Modificar** - Establece nueva cantidad directamente
- **➕ Agregar** - Suma unidades al stock actual
- **➖ Quitar** - Resta unidades del stock actual
- **📋 Historial** - Muestra movimientos del producto

### Operaciones de Stock

#### ✏️ Modificar Stock Directamente
1. Haz clic en el botón **✏️** del producto
2. Ingresa la nueva cantidad total
3. Confirma la operación
4. El stock se actualiza inmediatamente

#### ➕ Agregar Stock (Entrada de Mercancía)
1. Haz clic en el botón **➕** del producto
2. Ingresa la cantidad a agregar
3. Confirma la operación
4. Se suma al stock actual

#### ➖ Quitar Stock (Salida Manual)
1. Haz clic en el botón **➖** del producto
2. Ingresa la cantidad a quitar
3. Confirma la operación
4. Se resta del stock actual

#### 📋 Ver Historial de Movimientos
1. Haz clic en el botón **📋** del producto
2. Se abre ventana con historial completo
3. Muestra: fecha, tipo, cantidad, descripción
4. Tipos de movimiento:
   - **ENTRADA** (Verde) - Mercancía recibida
   - **SALIDA** (Rojo) - Mercancía enviada
   - **VENTA** (Naranja) - Venta automática
   - **AJUSTE_POSITIVO** (Azul) - Corrección al alza
   - **AJUSTE_NEGATIVO** (Morado) - Corrección a la baja
   - **INICIAL** (Gris) - Stock inicial

### Búsqueda y Filtros
- **Búsqueda en tiempo real** mientras escribes
- **Busca en**: nombre y referencia del producto
- **Filtro stock bajo**: Muestra solo productos críticos
- **Actualización**: Recarga datos desde la base de datos

---

## 🧾 Creación de Facturas

### Acceso
- **Opción 1**: Botón **"Nueva Factura"** (verde) en ventana principal
- **Opción 2**: Botón **"Facturas"** → **"Nueva Factura"**

### Interfaz de Facturas

#### 📋 Panel Izquierdo - Lista de Facturas
- **Tabla con columnas**:
  - Número de Factura
  - Fecha
  - Cliente
  - Total
- **Selección**: Un clic carga la factura en el formulario
- **Ordenación**: Por fecha (más recientes primero)

#### 📝 Panel Derecho - Formulario de Factura

##### 📊 Datos de la Factura
- **Número de Factura** - Generado automáticamente
- **Fecha** - Fecha actual por defecto
- **Estado** - Borrador/Finalizada

##### 👤 Datos del Cliente
- **Nombre del Cliente*** (obligatorio)
- **CIF/NIF del Cliente**
- **Dirección del Cliente**
- **Teléfono del Cliente**
- **Email del Cliente**

##### 📦 Productos de la Factura
- **Lista de productos agregados**
- **Botón "Agregar Producto"** - Abre diálogo de selección
- **Cada línea muestra**:
  - Imagen del producto (miniatura)
  - Nombre y referencia
  - Cantidad
  - Precio unitario
  - IVA aplicado
  - Total línea
- **Botones por línea**:
  - **✏️ Editar** - Modifica cantidad/precio
  - **🗑️ Eliminar** - Quita producto de factura

##### 💰 Totales de la Factura
- **Subtotal** - Suma sin IVA
- **Total IVA** - Impuestos calculados
- **Total Factura** - Importe final

#### 🔘 Botones de Acción
- **Guardar Borrador** (Azul) - Guarda sin finalizar
- **Finalizar Factura** (Verde) - Completa y actualiza stock
- **Generar PDF** (Naranja) - Crea archivo PDF
- **Limpiar** (Gris) - Limpia el formulario
- **Eliminar** (Rojo) - Elimina factura seleccionada

### Flujo de Trabajo

#### ➕ Crear Nueva Factura
1. Haz clic en **"Nueva Factura"**
2. Completa datos del cliente
3. Agrega productos:
   - Clic en **"Agregar Producto"**
   - Selecciona producto del catálogo
   - Especifica cantidad
   - Confirma
4. Revisa totales calculados
5. **Guardar Borrador** o **Finalizar Factura**

#### 📄 Generar PDF
1. Selecciona factura finalizada
2. Haz clic en **"Generar PDF"**
3. El PDF se guarda automáticamente
4. Se abre con el visor por defecto

#### ✏️ Editar Factura Existente
1. Selecciona factura en la lista
2. Modifica los campos necesarios
3. Guarda los cambios

### Validaciones
- **Cliente**: Nombre obligatorio
- **Productos**: Mínimo un producto
- **Stock**: Verifica disponibilidad
- **Cantidades**: Deben ser > 0
- **Precios**: Deben ser válidos

---

## 💡 Consejos y Trucos

### 🚀 Productividad
- **Atajos de teclado**: Enter para guardar, Escape para cancelar
- **Ventanas múltiples**: Mantén abiertas las ventanas que uses frecuentemente

### 🎨 Personalización
- **Directorio de imágenes**: Configura una carpeta específica para organizar mejor
- **Numeración de facturas**: Establece el número inicial según tu sistema
- **Logo empresarial**: Agrega tu logo para facturas profesionales

### 💾 Gestión de Datos
- **Backups automáticos**: La aplicación crea copias de seguridad automáticamente
- **Imágenes organizadas**: Las imágenes se copian a la carpeta de la aplicación
- **PDFs centralizados**: Todas las facturas PDF se guardan en un directorio específico

### 🔧 Mantenimiento
- **Limpieza regular**: Elimina productos no utilizados
- **Revisión de stock**: Usa el filtro de stock bajo regularmente
- **Actualización de precios**: Revisa y actualiza precios periódicamente

---

## 🆘 Solución de Problemas

### Problemas Comunes

#### ❌ "No se puede guardar el producto"
**Causas posibles**:
- Campos obligatorios vacíos
- Referencia duplicada
- Precio inválido

**Solución**:
1. Verifica que nombre y referencia no estén vacíos
2. Asegúrate de que la referencia sea única
3. Ingresa un precio numérico válido

#### 🖼️ "No se muestra la imagen del producto"
**Causas posibles**:
- Archivo de imagen corrupto
- Formato no soportado
- Archivo movido o eliminado

**Solución**:
1. Verifica que el archivo existe
2. Usa formatos soportados (PNG, JPG, GIF, BMP)
3. Vuelve a seleccionar la imagen

#### 📊 "El stock no se actualiza"
**Causas posibles**:
- Error en la base de datos
- Factura no finalizada
- Problema de permisos

**Solución**:
1. Haz clic en "Actualizar" en la ventana de stock
2. Verifica que la factura esté finalizada
3. Reinicia la aplicación si persiste

#### 📄 "No se genera el PDF"
**Causas posibles**:
- Factura incompleta
- Problema con ReportLab
- Permisos de escritura

**Solución**:
1. Verifica que la factura tenga cliente y productos
2. Comprueba permisos en la carpeta de PDFs
3. Revisa los logs de error

### 📞 Obtener Ayuda
- **Logs de aplicación**: Revisa `logs/facturacion_facil.log`
- **Archivos de configuración**: `config.json`
- **Base de datos**: `database/facturacion.db`

---

**¡Felicidades! Ya conoces todas las funcionalidades de Facturación Fácil.**

Para más información técnica, consulta la documentación en la carpeta `docs/`.
