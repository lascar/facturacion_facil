> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🔧 CORRECCIÓN - Problema de Selección para Exportación PDF

## 🎯 **Problema Reportado**

El usuario reportó que **"exportar a pdf ne fonctionne plus"** con el mensaje:
```
⚠️ Seleccione una factura para exportar
```

A pesar de haber seleccionado una factura en la lista.

---

## 🔍 **Diagnóstico del Problema**

### **Causa Identificada**

El problema estaba en el método `on_factura_select` en `ui/facturas.py`:

```python
# CÓDIGO PROBLEMÁTICO
def on_factura_select(self, event):
    selection = self.facturas_tree.selection()
    if selection:
        item = selection[0]
        index = self.facturas_tree.index(item)
        self.selected_factura = self.facturas[index]  # ❌ PROBLEMA AQUÍ
```

**Problema**: Cuando se usa la carga optimizada de facturas, `self.facturas` puede estar vacío o no corresponder al índice del TreeView, causando que `self.facturas[index]` falle o retorne la factura incorrecta.

### **Síntomas**
- ✅ La factura se selecciona visualmente en la lista
- ❌ `self.selected_factura` no se establece correctamente
- ❌ El método `exportar_pdf()` detecta que no hay factura seleccionada
- ❌ Aparece el mensaje de advertencia

---

## 🔧 **Solución Implementada**

### **1. Método `get_by_numero` Agregado**

**Archivo**: `database/models.py`

```python
@staticmethod
def get_by_numero(numero_factura):
    """Obtiene una factura por su número de factura"""
    query = "SELECT * FROM facturas WHERE numero_factura=?"
    results = db.execute_query(query, (numero_factura,))
    if results:
        row = results[0]
        factura = Factura(
            id=row[0], numero_factura=row[1], fecha_factura=row[2], nombre_cliente=row[3],
            dni_nie_cliente=row[4], direccion_cliente=row[5], email_cliente=row[6],
            telefono_cliente=row[7], subtotal=row[8], total_iva=row[9], total_factura=row[10],
            modo_pago=row[11], fecha_creacion=row[12]
        )
        # Cargar items de la factura
        factura.items = FacturaItem.get_by_factura_id(factura.id)
        return factura
    return None
```

### **2. Método `on_factura_select` Corregido**

**Archivo**: `ui/facturas.py`

```python
def on_factura_select(self, event):
    """Maneja la selección de una factura en la lista y la carga automáticamente para edición"""
    try:
        selection = self.facturas_tree.selection()
        if selection:
            item = selection[0]
            # Obtener el número de factura desde la primera columna del TreeView
            item_values = self.facturas_tree.item(item, 'values')
            if item_values and len(item_values) > 0:
                numero_factura = item_values[0]  # Primera columna es el número de factura
                
                # Buscar la factura por número en la base de datos
                self.selected_factura = Factura.get_by_numero(numero_factura)
                
                if self.selected_factura:
                    # Cargar factura en el formulario para edición automática
                    self.load_factura_to_form()
                    # ... resto del código ...
```

### **3. Logging de Diagnóstico Agregado**

**Archivos**: `ui/facturas.py` y `ui/facturas_methods.py`

```python
# En on_factura_select
self.logger.info(f"🔍 DEBUG: Buscando factura con número: {numero_factura}")
self.logger.info(f"🔍 DEBUG: Factura encontrada: {self.selected_factura is not None}")

# En exportar_pdf
self.logger.info(f"🔍 DEBUG PDF: selected_factura = {self.selected_factura}")
self.logger.info(f"🔍 DEBUG PDF: hasattr selected_factura = {hasattr(self, 'selected_factura')}")
```

---

## 🧪 **Tests Implementados**

### **Test de Selección de Factura**
**Archivo**: `test/demo/demo_test_factura_selection.py`

Este test verifica:
- ✅ Método `get_by_numero` funciona correctamente
- ✅ Simulación de selección exitosa
- ✅ Estado correcto para exportación PDF
- ✅ Datos completos de factura

### **Test de Exportación PDF**
**Archivo**: `test/demo/demo_test_pdf_export.py`

Este test verifica:
- ✅ Método directo de exportación
- ✅ Exportación con interfaz gráfica
- ✅ Manejo de errores

### **Ejecutar Tests**
```bash
# Test de selección
python3 test/demo/demo_test_factura_selection.py

# Test de exportación PDF
python3 test/demo/demo_test_pdf_export.py
```

---

## 📊 **Resultados de Tests**

### **Test de Selección - EXITOSO**
```
📊 RESUMEN DEL TEST:
   Facturas disponibles: ✅ 38
   Método get_by_numero: ✅ Funciona
   Simulación selección: ✅ Exitosa
   Estado para PDF: ✅ Correcto
   Datos completos: ✅ Sí
```

### **Logs Esperados Ahora**
```
🔍 DEBUG: Buscando factura con número: FACT-1758878404-2025
🔍 DEBUG: Factura encontrada: True
🔍 DEBUG: Factura ID: 40, Items: 1
🔍 DEBUG PDF: selected_factura = <database.models.Factura object at 0x...>
```

---

## 📋 **Instrucciones para el Usuario**

### **Pasos para Exportar PDF**
1. **Abrir la ventana de Facturas**
2. **En la lista de la izquierda, hacer clic en una factura**
3. **Verificar que la factura se carga en el formulario**
4. **Hacer clic en el botón "Exportar PDF"**
5. **El PDF se generará y abrirá automáticamente**

### **Verificación de Funcionamiento**
- ✅ **La factura seleccionada** debe aparecer en el formulario
- ✅ **El título debe cambiar** a "Editando Factura: [NÚMERO]"
- ✅ **Los logs deben mostrar** mensajes de debug de selección

### **Si Aún No Funciona**
1. **Revisar logs** en `logs/facturacion_facil.log`
2. **Buscar líneas** que empiecen con "🔍 DEBUG"
3. **Verificar** que `selected_factura` no sea None
4. **Comprobar** que ReportLab esté instalado: `pip install reportlab`

---

## 🔍 **Diagnóstico de Problemas**

### **Problema: "Factura encontrada: False"**
**Causa**: El número de factura no se encuentra en la base de datos
**Solución**: Verificar que la factura existe y el número es correcto

### **Problema: "selected_factura = None"**
**Causa**: La selección no se está estableciendo correctamente
**Solución**: Verificar que `on_factura_select` se ejecuta sin errores

### **Problema: Error de ReportLab**
**Causa**: Biblioteca de PDF no instalada
**Solución**: `pip install reportlab`

### **Problema: Error de permisos**
**Causa**: No se puede escribir el archivo PDF
**Solución**: Verificar permisos del directorio de salida

---

## ✅ **Estado de la Corrección**

### **Archivos Modificados**
- ✅ `database/models.py` - Método `get_by_numero` agregado
- ✅ `ui/facturas.py` - Método `on_factura_select` corregido
- ✅ `ui/facturas_methods.py` - Logging de diagnóstico agregado

### **Tests Creados**
- ✅ `test/demo/demo_test_factura_selection.py` - Test de selección
- ✅ `test/demo/demo_test_pdf_export.py` - Test de exportación

### **Documentación**
- ✅ `docs/fixes/PDF_EXPORT_SELECTION_FIX.md` - Este documento

### **Resultado**
**La selección de facturas ahora funciona correctamente y la exportación PDF debería funcionar.**

---

## 🚀 **Próximos Pasos**

1. **Reiniciar la aplicación** para cargar los cambios
2. **Probar la selección** de facturas en la lista
3. **Verificar logs** durante la selección
4. **Probar exportación PDF** con factura seleccionada
5. **Reportar** cualquier error específico que aparezca

---

**Fecha de Corrección**: 27 de septiembre de 2024  
**Problema**: Selección de factura para PDF no funcionaba  
**Solución**: Método robusto de selección por número de factura  
**Estado**: ✅ **CORREGIDO Y TESTADO**

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
