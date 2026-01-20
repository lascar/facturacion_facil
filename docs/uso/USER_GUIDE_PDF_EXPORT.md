> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**

---

# 📄 GUÍA DE USUARIO - Exportación de Facturas a PDF

## 🎯 **¿Qué es la Exportación a PDF?**

La funcionalidad de exportación a PDF te permite generar documentos PDF profesionales de tus facturas para:
- **Enviar por email** a clientes
- **Imprimir** copias físicas
- **Archivar** documentos digitalmente
- **Cumplir** con requisitos legales

---

## 📋 **Pasos para Exportar una Factura a PDF**

### **1. Abrir la Ventana de Facturas**
- Desde el menú principal, hacer clic en **"Facturas"**
- Se abrirá la ventana con la lista de facturas y el formulario

### **2. Seleccionar una Factura**
- En la **lista de la izquierda**, buscar la factura que deseas exportar
- **Hacer clic** en la fila de la factura
- La factura se cargará automáticamente en el formulario de la derecha

### **3. Verificar la Selección**
- El **título del formulario** cambiará a: `"Editando Factura: [NÚMERO]"`
- Los **datos de la factura** aparecerán en el formulario
- La **lista de productos** se mostrará en la parte inferior

### **4. Exportar a PDF**
- Hacer clic en el botón **"Exportar PDF"**
- El sistema generará el PDF automáticamente
- El archivo se abrirá en tu visor de PDF predeterminado

---

## 🔍 **Verificación Visual**

### **Factura Correctamente Seleccionada:**
```
┌─────────────────────────────────────────────────────────┐
│ ✅ Editando Factura: FACT-1758878404-2025             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Número: FACT-1758878404-2025                           │
│ Cliente: Juan Pérez                                     │
│ Fecha: 27/09/2024                                       │
│ Total: €125.50                                          │
│                                                         │
│ Productos:                                              │
│ • Producto A - Cantidad: 2 - €50.00                   │
│ • Producto B - Cantidad: 1 - €25.50                   │
│                                                         │
│              [Exportar PDF]                             │
└─────────────────────────────────────────────────────────┘
```

### **Factura NO Seleccionada:**
```
┌─────────────────────────────────────────────────────────┐
│ ❌ Datos de la Factura                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Número: [vacío]                                         │
│ Cliente: [vacío]                                        │
│ Fecha: [vacío]                                          │
│ Total: [vacío]                                          │
│                                                         │
│ Productos: [lista vacía]                                │
│                                                         │
│              [Exportar PDF]                             │
└─────────────────────────────────────────────────────────┘
```

---

## ⚠️ **Mensajes de Error y Soluciones**

### **Error: "Seleccione una factura para exportar"**

#### **Causa:**
No hay ninguna factura seleccionada en la lista.

#### **Solución:**
1. **Ir a la lista de facturas** (lado izquierdo)
2. **Hacer clic en una fila** de la lista
3. **Verificar** que el título cambie a "Editando Factura: [NÚMERO]"
4. **Intentar exportar** nuevamente

#### **Si el problema persiste:**
- **Reiniciar la aplicación**
- **Verificar** que la factura existe en la base de datos
- **Revisar logs** en `logs/facturacion_facil.log`

### **Error: "ReportLab no está instalado"**

#### **Causa:**
La biblioteca necesaria para generar PDFs no está instalada.

#### **Solución:**
```bash
pip install reportlab
```

### **Error: "No se puede escribir el archivo PDF"**

#### **Causa:**
Problemas de permisos en el directorio de salida.

#### **Solución:**
- **Verificar permisos** del directorio donde se guarda el PDF
- **Ejecutar como administrador** si es necesario
- **Cambiar directorio** de salida en configuración

### **Error: "Datos de factura incompletos"**

#### **Causa:**
La factura seleccionada no tiene todos los datos necesarios.

#### **Solución:**
1. **Editar la factura** para completar datos faltantes
2. **Guardar los cambios**
3. **Intentar exportar** nuevamente

---

## 📊 **Contenido del PDF Generado**

### **Información de la Empresa:**
- Nombre de la empresa
- Dirección
- Teléfono y email
- Número de identificación fiscal

### **Información del Cliente:**
- Nombre completo
- DNI/NIE
- Dirección
- Email y teléfono

### **Detalles de la Factura:**
- Número de factura
- Fecha de emisión
- Modo de pago
- Fecha de vencimiento (si aplica)

### **Productos/Servicios:**
- Descripción detallada
- Cantidad
- Precio unitario
- IVA aplicado
- Subtotal por línea

### **Totales:**
- Subtotal sin IVA
- Total IVA
- **Total factura**

### **Información Legal:**
- Condiciones de pago
- Información fiscal requerida
- Notas adicionales

---

## 🔧 **Solución de Problemas Avanzados**

### **Problema: La factura no se selecciona**

#### **Diagnóstico:**
1. **Abrir logs** en `logs/facturacion_facil.log`
2. **Buscar líneas** que contengan "🔍 DEBUG"
3. **Verificar** si aparecen estos mensajes:

```
🔍 DEBUG: Buscando factura con número: FACT-XXXXX
🔍 DEBUG: Factura encontrada: True
🔍 DEBUG: Factura ID: XX, Items: X
```

#### **Si NO aparecen estos logs:**
- **Problema:** El evento de selección no se está ejecutando
- **Solución:** Reiniciar la aplicación, verificar que se hace clic en la fila correcta

#### **Si aparece "Factura encontrada: False":**
- **Problema:** La factura no existe en la base de datos
- **Solución:** Verificar que la factura no fue eliminada, recrear si es necesario

### **Problema: PDF se genera pero está vacío**

#### **Diagnóstico:**
1. **Verificar** que la factura tiene productos asociados
2. **Revisar** que los totales no son cero
3. **Comprobar** que los datos del cliente están completos

#### **Solución:**
1. **Editar la factura** para agregar productos si faltan
2. **Completar datos** del cliente
3. **Recalcular totales** guardando la factura
4. **Intentar exportar** nuevamente

### **Problema: PDF se abre pero no se ve bien**

#### **Posibles causas:**
- **Fuentes** no disponibles en el sistema
- **Caracteres especiales** no soportados
- **Tamaño de página** incorrecto

#### **Solución:**
- **Actualizar ReportLab**: `pip install --upgrade reportlab`
- **Verificar configuración** de fuentes en el sistema
- **Reportar** el problema con captura de pantalla

---

## 📚 **Consejos y Mejores Prácticas**

### **Para Mejores Resultados:**
- ✅ **Completar todos los datos** del cliente antes de exportar
- ✅ **Verificar totales** antes de generar el PDF
- ✅ **Usar descripciones claras** en los productos
- ✅ **Revisar el PDF** antes de enviarlo al cliente

### **Para Organización:**
- 📁 **Crear carpetas** por mes o cliente para organizar PDFs
- 📝 **Usar nombres descriptivos** para los archivos
- 💾 **Hacer copias de seguridad** de los PDFs importantes
- 📧 **Enviar por email** directamente desde la aplicación (si disponible)

### **Para Cumplimiento Legal:**
- 📋 **Verificar** que todos los datos fiscales están completos
- 🔢 **Asegurar** que la numeración de facturas es consecutiva
- 📅 **Mantener** las fechas correctas
- 💼 **Archivar** los PDFs según requisitos legales locales

---

## 🆘 **Soporte Técnico**

### **Si Necesitas Ayuda:**

#### **Información a Proporcionar:**
1. **Número de factura** que intentas exportar
2. **Mensaje de error** exacto que aparece
3. **Captura de pantalla** de la ventana de facturas
4. **Logs relevantes** de `logs/facturacion_facil.log`

#### **Logs Importantes a Buscar:**
```bash
# Ver logs de selección
grep "🔍 DEBUG" logs/facturacion_facil.log

# Ver errores de PDF
grep "PDF" logs/facturacion_facil.log

# Ver errores generales
grep "ERROR" logs/facturacion_facil.log
```

#### **Tests de Diagnóstico:**
```bash
# Test de selección de facturas
python3 test/demo/demo_test_factura_selection.py

# Test de exportación PDF
python3 test/demo/demo_test_pdf_export.py
```

---

## 📞 **Contacto**

Para soporte técnico adicional:
- **Revisar documentación** en `docs/fixes/PDF_EXPORT_SELECTION_FIX.md`
- **Ejecutar tests** de diagnóstico
- **Proporcionar logs** detallados del problema

---

**Última Actualización**: 27 de septiembre de 2024
**Versión**: Con corrección de selección de facturas
**Estado**: ✅ **FUNCIONANDO CORRECTAMENTE**

---

> **[⬆️ Volver al índice](INDEX.md)** | **[📖 README](README.md)** | **[🏠 Inicio](../README.md)**
