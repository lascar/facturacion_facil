# 📝 Guía de Edición de Facturas - PyQt5

## 🎯 Funcionalidad Implementada

Se ha añadido la capacidad de **editar facturas existentes** en la aplicación PyQt5 de Facturación Fácil.

## 🚀 Cómo Usar la Edición de Facturas

### 1. Acceder a la Edición
1. Abra la ventana de **Gestión de Facturas**
2. Seleccione una factura de la lista haciendo clic en ella
3. Haga clic en el botón **"✏️ Editar"**

### 2. Modificar la Factura
En el diálogo de edición puede modificar:

#### ✅ Campos Editables:
- **Fecha de la factura** (selector de calendario)
- **Cliente** (lista desplegable)
- **Productos y cantidades** (tabla editable)
- **IVA por producto** (editable en la tabla)

#### 🔒 Campos No Editables:
- **Número de factura** (solo lectura)

### 3. Gestión de Productos
- **Agregar productos**: Use el selector de productos y haga clic en "➕ Agregar"
- **Modificar cantidades**: Haga clic directamente en la celda de cantidad en la tabla
- **Cambiar IVA**: Edite el porcentaje de IVA en la tabla
- **Eliminar productos**: Use el botón "🗑️" en cada fila

### 4. Guardar Cambios
1. Revise que todos los datos sean correctos
2. Verifique los totales calculados automáticamente
3. Haga clic en **"OK"** para guardar los cambios
4. La factura se actualizará en la base de datos

## 🔧 Características Técnicas

### Validaciones Implementadas
- ✅ **Cliente obligatorio**: Debe seleccionar un cliente
- ✅ **Productos obligatorios**: Debe tener al menos un producto
- ✅ **Control de stock**: Verifica disponibilidad antes de agregar/modificar
- ✅ **Cálculos automáticos**: Subtotales, IVA y total se calculan automáticamente

### Gestión de Stock
- El sistema maneja automáticamente los movimientos de stock
- Al modificar cantidades, se verifica la disponibilidad
- Los cambios se reflejan correctamente en el inventario

### Base de Datos
- Utiliza la función `update_invoice()` existente
- Mantiene la integridad referencial
- Preserva el historial de la factura

## 🎨 Interfaz de Usuario

### Botones Principales
- **➕ Nueva Factura**: Crear nueva factura
- **👁️ Ver Detalles**: Ver factura en modo solo lectura
- **✏️ Editar**: Editar factura seleccionada ⭐ **NUEVO**
- **🗑️ Eliminar**: Eliminar factura
- **🔄 Actualizar**: Refrescar lista

### Diálogo de Edición
- **Información de la Factura**: Número, fecha, cliente
- **Gestión de Productos**: Agregar, modificar, eliminar productos
- **Totales**: Subtotal, IVA, total (calculados automáticamente)
- **Botones**: OK (guardar), Cancelar

## 📋 Flujo de Trabajo

```
1. Seleccionar Factura → 2. Clic "Editar" → 3. Modificar Datos → 4. Guardar
```

## ⚠️ Consideraciones Importantes

1. **Backup**: Siempre haga backup de la base de datos antes de modificaciones importantes
2. **Stock**: Las modificaciones afectan el inventario inmediatamente
3. **Validación**: El sistema valida todos los datos antes de guardar
4. **Cancelación**: Use "Cancelar" para descartar cambios sin guardar

## 🐛 Resolución de Problemas

### Error: "No se pudo cargar la factura"
- Verifique que la factura existe en la base de datos
- Compruebe la conexión a la base de datos

### Error: "Stock insuficiente"
- Verifique la disponibilidad del producto
- Ajuste las cantidades según el stock disponible

### Error: "Seleccione un cliente"
- Asegúrese de seleccionar un cliente de la lista desplegable

## 🎉 ¡Listo para Usar!

La funcionalidad de edición de facturas está completamente implementada y probada. 
Puede comenzar a editar sus facturas de inmediato siguiendo esta guía.

---
*Implementado con PyQt5 - Facturación Fácil*
