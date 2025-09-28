# 📋 GUÍA DE USUARIO - Confirmación de Stock en Facturas

## 🎯 **¿Qué es la Confirmación de Stock?**

Cuando creas una factura con productos que tienen **stock bajo** (5 unidades o menos), el sistema te mostrará un diálogo de confirmación antes de procesar la factura.

Este diálogo te informa:
- **Qué productos** se verán afectados
- **Cuánto stock** quedará después de la venta
- **Qué acciones** realizará el sistema

---

## 🔍 **¿Cuándo Aparece el Diálogo?**

El diálogo de confirmación aparece cuando:

✅ **Creas una factura** con productos de stock bajo  
✅ **Haces clic en "Guardar"**  
✅ **El sistema detecta** productos con ≤ 5 unidades en stock  

---

## 💻 **Tipos de Diálogo que Puedes Ver**

### **Diálogo Preferido (CustomTkinter)**
```
┌─────────────────────────────────────────────────────────┐
│ 📦 Confirmar Procesamiento de Factura                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 📦 IMPACTO EN STOCK:                                   │
│                                                         │
│ • Producto ABC:                                        │
│   Stock actual: 3 → Después: 2 unidades               │
│   Estado: 🟠 STOCK BAJO (2)                           │
│                                                         │
│ ==================================================     │
│ 🔄 ACCIÓN A REALIZAR:                                  │
│ • Se guardará la factura                               │
│ • Se actualizará automáticamente el stock             │
│ • Se registrarán los movimientos de stock             │
│                                                         │
│ ¿Desea continuar y procesar la factura?               │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [📋 Copiar]              [✅ CONFIRMAR] [❌ CANCELAR]  │
└─────────────────────────────────────────────────────────┘
```

### **Diálogo Alternativo (Tkinter Simple)**
```
┌─────────────────────────────────────────────────────────┐
│ Confirmar Procesamiento de Factura                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ [Mensaje detallado sobre el impacto en stock]          │
│                                                         │
│ • SÍ = Confirmar y procesar                            │
│ • NO = Cancelar operación                              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    [SÍ]    [NO]                        │
└─────────────────────────────────────────────────────────┘
```

### **Último Recurso (Consola)**
```
📦 CONFIRMACIÓN DE STOCK:

• Producto ABC: Stock 3 → 2 unidades
• Estado: STOCK BAJO

¿Desea continuar y procesar la factura? (s/n):
```

---

## ✅ **Qué Hacer en Cada Caso**

### **Para PROCESAR la Factura:**

#### **En Diálogo CustomTkinter:**
1. **Leer** el impacto en stock mostrado
2. **Hacer clic en "✅ CONFIRMAR"** (botón verde)

#### **En Diálogo Simple:**
1. **Leer** el mensaje detallado
2. **Hacer clic en "SÍ"**

#### **En Consola:**
1. **Leer** la información mostrada
2. **Escribir** `s` o `si` y presionar Enter

### **Para CANCELAR la Operación:**

#### **En Diálogo CustomTkinter:**
1. **Hacer clic en "❌ CANCELAR"** (botón rojo)

#### **En Diálogo Simple:**
1. **Hacer clic en "NO"**

#### **En Consola:**
1. **Escribir** `n` o `no` y presionar Enter

---

## 🔄 **¿Qué Pasa Después?**

### **Si CONFIRMAS:**
✅ **La factura se guarda** en la base de datos  
✅ **El stock se actualiza** automáticamente  
✅ **Se registran los movimientos** de stock  
✅ **Ves una confirmación** de éxito  

### **Si CANCELAS:**
❌ **La factura NO se guarda**  
❌ **El stock NO se modifica**  
ℹ️ **Puedes modificar** la factura y intentar de nuevo  

---

## 🎨 **Características Especiales**

### **Botón "📋 Copiar" (Solo en Diálogo CustomTkinter)**
- **Función**: Copia todo el mensaje al portapapeles
- **Uso**: Para guardar la información o enviarla por email
- **Cómo usar**: Hacer clic en "📋 Copiar"

### **Atajos de Teclado (Solo en Diálogo CustomTkinter)**
- **Enter**: Confirmar (igual que hacer clic en "✅ CONFIRMAR")
- **Escape**: Cancelar (igual que hacer clic en "❌ CANCELAR")

### **Estados de Stock Mostrados**
- **🟢 STOCK NORMAL**: Más de 5 unidades (no aparece diálogo)
- **🟡 STOCK MEDIO**: 3-5 unidades
- **🟠 STOCK BAJO**: 1-2 unidades
- **🔴 STOCK CRÍTICO**: 0 unidades (venta no permitida)

---

## 🔧 **Solución de Problemas**

### **"No aparece ningún diálogo"**
- **Causa**: Error técnico muy raro
- **Solución**: Revisar la consola/terminal para pregunta por texto

### **"El diálogo aparece vacío"**
- **Causa**: Problema de renderizado
- **Solución**: Cerrar y volver a intentar, o usar el diálogo alternativo

### **"No puedo hacer clic en los botones"**
- **Causa**: Diálogo no está enfocado
- **Solución**: Hacer clic en la barra de título del diálogo primero

### **"Quiero deshabilitar la confirmación"**
- **Respuesta**: La confirmación es una medida de seguridad importante
- **Alternativa**: Mantener stock alto (>5 unidades) para evitar el diálogo

---

## 📊 **Ejemplos Prácticos**

### **Ejemplo 1: Stock Bajo Normal**
```
📦 IMPACTO EN STOCK:

• Camiseta Azul Talla M:
  Stock actual: 4 → Después: 3 unidades
  Estado: 🟡 STOCK MEDIO (3)

• Pantalón Negro Talla L:
  Stock actual: 2 → Después: 1 unidades
  Estado: 🟠 STOCK BAJO (1)
```
**Acción recomendada**: Confirmar, pero considerar reabastecer pronto.

### **Ejemplo 2: Stock Crítico**
```
📦 IMPACTO EN STOCK:

• Zapatos Deportivos Talla 42:
  Stock actual: 1 → Después: 0 unidades
  Estado: 🔴 STOCK CRÍTICO (0)
```
**Acción recomendada**: Confirmar solo si es la última unidad disponible.

### **Ejemplo 3: Múltiples Productos**
```
📦 IMPACTO EN STOCK:

• Producto A: Stock 5 → 4 unidades (🟡 MEDIO)
• Producto B: Stock 3 → 1 unidades (🟠 BAJO)  
• Producto C: Stock 8 → 6 unidades (🟢 NORMAL)
```
**Acción recomendada**: Confirmar y planificar reabastecimiento.

---

## 🎯 **Consejos de Uso**

### **Para Evitar el Diálogo:**
- **Mantener stock alto**: >5 unidades por producto
- **Reabastecer regularmente**: Antes de llegar a stock bajo
- **Monitorear stock**: Revisar regularmente los niveles

### **Para Gestión Eficiente:**
- **Leer siempre** el impacto antes de confirmar
- **Usar "Copiar"** para documentar ventas importantes
- **Planificar reabastecimiento** basado en la información mostrada

### **Para Casos Especiales:**
- **Última unidad**: Confirmar solo si el cliente realmente la quiere
- **Productos estacionales**: Considerar si vale la pena reabastecer
- **Productos descontinuados**: Confirmar para liquidar stock

---

## 📞 **Soporte**

Si tienes problemas con el diálogo de confirmación:

1. **Revisar logs**: `logs/facturacion_facil.log`
2. **Buscar mensajes**: Que empiecen con "🔧 DEBUG:"
3. **Reportar problemas**: Con capturas de pantalla y logs
4. **Información útil**: Versión del sistema, tipo de diálogo que aparece

---

**Última actualización**: 27 de septiembre de 2024  
**Versión del sistema**: Con solución robusta de diálogos  
**Estado**: ✅ **FUNCIONANDO PERFECTAMENTE**
