# 🔧 DEBUG: Problema de Selección de Stock

## 📋 **Problema Reportado**
**Síntoma:** No aparece ventana de error cuando se intenta actualizar stock sin seleccionar producto  
**Esperado:** Debería aparecer mensaje "Por favor, selecciona un producto primero." con botón copiar

---

## 🔍 **Diagnóstico Implementado**

### **1. Logging Agresivo Agregado**
**Archivo:** `ui/stock.py`

**Modificaciones realizadas:**

#### **A. Wrapper de Debug en Botón**
```python
def _debug_actualizar_stock_wrapper(self):
    """Wrapper de debug para actualizar stock"""
    print("🚨 DEBUG: BOTÓN ACTUALIZAR STOCK PRESIONADO")
    
    # FORZAR MENSAJE SIEMPRE (para debug)
    show_copyable_warning(self.window, "DEBUG - Advertencia", 
        "Por favor, selecciona un producto primero.\n\n(Este es un mensaje de debug forzado)")
    
    # Luego ejecutar la función original
    self.actualizar_stock_selected()
```

#### **B. Logging Detallado en Función Principal**
```python
def actualizar_stock_selected(self):
    # LOGGING AGRESIVO PARA DEBUG
    print("🚨 DEBUG: actualizar_stock_selected EJECUTADA")
    
    print(f"🚨 DEBUG: hasattr(self, 'selected_producto_id') = {hasattr(self, 'selected_producto_id')}")
    
    if not hasattr(self, 'selected_producto_id'):
        print("🚨 DEBUG: CONDICIÓN CUMPLIDA - MOSTRANDO MENSAJE")
        print("🚨 DEBUG: EJECUTANDO show_copyable_warning AHORA")
        
        show_copyable_warning(self.window, "Advertencia", "Por favor, selecciona un producto primero.")
```

### **2. Doble Verificación**
- **Mensaje forzado:** Aparece SIEMPRE al presionar el botón (para confirmar que funciona)
- **Mensaje condicional:** Aparece solo si no hay producto seleccionado (lógica original)

---

## 🧪 **Cómo Probar el Debug**

### **Paso 1: Reiniciar Aplicación**
```bash
python3 main.py
```

### **Paso 2: Ir a Gestión de Stock**
- Abrir ventana de stock
- NO seleccionar ningún producto

### **Paso 3: Presionar "Actualizar Stock"**
**Resultado esperado:**
1. **Primer mensaje (forzado):** "DEBUG - Advertencia" con texto de debug
2. **Segundo mensaje (condicional):** "Advertencia" con mensaje original

### **Paso 4: Verificar Logs**
**En consola verás:**
```
🚨 DEBUG: BOTÓN ACTUALIZAR STOCK PRESIONADO
🚨 DEBUG: FORZANDO MENSAJE DE SELECCIÓN
✅ DEBUG: Mensaje forzado mostrado exitosamente
🚨 DEBUG: actualizar_stock_selected EJECUTADA
🚨 DEBUG: hasattr(self, 'selected_producto_id') = False
🚨 DEBUG: CONDICIÓN CUMPLIDA - MOSTRANDO MENSAJE
🚨 DEBUG: EJECUTANDO show_copyable_warning AHORA
✅ DEBUG: show_copyable_warning ejecutado exitosamente
```

**En logs (`logs/facturacion_facil.log`):**
```
🚨 DEBUG: BOTÓN ACTUALIZAR STOCK PRESIONADO
🚨 DEBUG: FORZANDO MENSAJE DE SELECCIÓN
✅ DEBUG: Mensaje forzado mostrado exitosamente
🚨 DEBUG: actualizar_stock_selected EJECUTADA
```

---

## 🎯 **Interpretación de Resultados**

### **Caso 1: Aparecen AMBOS mensajes**
- ✅ **Sistema funcionando correctamente**
- ✅ **Botón conectado correctamente**
- ✅ **show_copyable_warning funciona**
- **Conclusión:** El problema original estaba resuelto

### **Caso 2: Solo aparece el PRIMER mensaje (forzado)**
- ✅ **Botón conectado correctamente**
- ✅ **show_copyable_warning funciona**
- ❌ **Problema en la lógica condicional**
- **Acción:** Revisar lógica de `hasattr` y selección

### **Caso 3: NO aparece NINGÚN mensaje**
- ❌ **Problema fundamental con show_copyable_warning**
- ❌ **Posible problema con CustomTkinter o parent window**
- **Acción:** Verificar instalación y configuración

### **Caso 4: Solo aparece messagebox estándar (fallback)**
- ⚠️  **show_copyable_warning falla pero fallback funciona**
- **Acción:** Revisar logs para ver el error específico

---

## 🔧 **Acciones Según Resultado**

### **Si NO aparece ningún mensaje:**
1. **Verificar que CustomTkinter está instalado**
2. **Verificar que la aplicación se inició correctamente**
3. **Revisar logs para errores de importación**

### **Si aparece solo el forzado:**
1. **Revisar lógica de selección de productos**
2. **Verificar que `selected_producto_id` se maneja correctamente**
3. **Comprobar el evento de selección en TreeView**

### **Si aparecen ambos mensajes:**
1. **El sistema funciona correctamente**
2. **Remover el debug y usar versión normal**
3. **El problema original estaba resuelto**

---

## 🧹 **Limpieza Después del Debug**

Una vez identificado el problema, remover el debug:

1. **Restaurar botón original:**
```python
command=self.actualizar_stock_selected,  # En lugar del wrapper
```

2. **Remover logging agresivo:**
- Quitar prints de debug
- Mantener solo logging normal

3. **Remover función wrapper:**
- Eliminar `_debug_actualizar_stock_wrapper`

---

## 📊 **Estado Actual**

**Modificaciones activas:**
- ✅ Wrapper de debug en botón "Actualizar Stock"
- ✅ Logging agresivo en `actualizar_stock_selected`
- ✅ Mensaje forzado para verificar funcionalidad
- ✅ Doble verificación de condiciones

**Objetivo:**
Identificar exactamente por qué no aparece el mensaje de selección y corregir el problema de raíz.

---

**Fecha de implementación:** 2025-10-05  
**Estado:** 🔍 Debug activo - Esperando resultados de prueba
