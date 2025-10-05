# 🔧 INSTRUCCIONES: Debug Botón Copiar

## 📋 **Situación Actual**
- ✅ **Mensaje aparece:** "Por favor, selecciona un producto primero."
- ❌ **Falta botón copiar:** El mensaje no tiene botón "📋 Copiar"
- ⚠️  **Logs incompletos:** Se cortan después de "FORZANDO MENSAJE DE SELECCIÓN"

**Conclusión:** `show_copyable_warning` se ejecuta pero hay un error silencioso que impide crear el botón copiar.

---

## 🧪 **Pruebas a Realizar**

### **Prueba 1: Reiniciar y Probar Botón Stock**
1. **Reinicia la aplicación** para aplicar el nuevo debug
2. **Ve a Gestión de Stock**
3. **Presiona "Actualizar Stock" sin seleccionar producto**

**Resultado esperado:**
- **Primer mensaje:** "DEBUG - Advertencia (Copiable)" - DEBE tener botón "📋 Copiar"
- **Segundo mensaje:** "DEBUG - Advertencia (Estándar)" - NO tendrá botón copiar
- **En consola:** Líneas detalladas de debug mostrando cada paso

### **Prueba 2: Verificar Logs Detallados**
**En consola verás:**
```
🚨 DEBUG: BOTÓN ACTUALIZAR STOCK PRESIONADO
🚨 DEBUG: FORZANDO MENSAJE DE SELECCIÓN
🔍 DEBUG: Probando show_copyable_warning...
🔍 DEBUG: show_copyable_warning llamada - parent: <ventana>, title: DEBUG - Advertencia (Copiable)
🔍 DEBUG: CopyableMessageDialog.__init__ - type: warning, title: DEBUG - Advertencia (Copiable)
🔍 DEBUG: Iniciando creación de diálogo...
🔍 DEBUG: Creando CTkToplevel...
🔍 DEBUG: CTkToplevel creado exitosamente
🔍 DEBUG: Configuración básica del diálogo completada
🔍 DEBUG: Configurando apariencia del diálogo...
🔍 DEBUG: Apariencia configurada exitosamente
🔍 DEBUG: Creando widgets del diálogo...
🔍 DEBUG: Creando botón copiar...
✅ DEBUG: Botón copiar creado exitosamente
🔍 DEBUG: Widgets creados exitosamente
🔍 DEBUG: Configurando focus...
✅ DEBUG: Focus configurado exitosamente
✅ DEBUG: CopyableMessageDialog creado completamente
🔍 DEBUG: dialog.show() completado - resultado: True
✅ DEBUG: show_copyable_warning completado
```

### **Prueba 3: Test Independiente (Opcional)**
Si quieres probar CustomTkinter por separado:
```bash
python3 test_customtkinter_simple.py
```

---

## 🎯 **Interpretación de Resultados**

### **Caso A: Aparecen AMBOS mensajes, el primero CON botón copiar**
- ✅ **Sistema funcionando correctamente**
- **Acción:** Remover debug y usar versión normal
- **Conclusión:** El problema original estaba resuelto

### **Caso B: Aparecen AMBOS mensajes, NINGUNO con botón copiar**
- ❌ **Problema con CustomTkinter o configuración**
- **Acción:** Revisar instalación de CustomTkinter
- **Logs esperados:** Errores en creación de CTkToplevel o CTkButton

### **Caso C: Solo aparece el SEGUNDO mensaje (estándar)**
- ❌ **Error crítico en show_copyable_warning**
- **Acción:** Revisar logs para ver el error específico
- **Logs esperados:** Traceback detallado del error

### **Caso D: NO aparece ningún mensaje**
- ❌ **Error fundamental en el sistema de diálogos**
- **Acción:** Verificar que la aplicación se inició correctamente

---

## 🔍 **Información a Reportar**

Por favor, reporta:

1. **¿Cuántos mensajes aparecen?** (0, 1, o 2)
2. **¿Cuál(es) tienen botón "📋 Copiar"?**
3. **¿Qué aparece en la consola?** (copia las líneas que empiecen con 🔍 o ❌)
4. **¿Hay errores en los logs?**

### **Ejemplo de reporte:**
```
Mensajes que aparecen:
1. "DEBUG - Advertencia (Copiable)" - SIN botón copiar
2. "DEBUG - Advertencia (Estándar)" - SIN botón copiar (normal)

Consola:
🚨 DEBUG: BOTÓN ACTUALIZAR STOCK PRESIONADO
🚨 DEBUG: FORZANDO MENSAJE DE SELECCIÓN
🔍 DEBUG: Probando show_copyable_warning...
❌ DEBUG: Error creando CTkToplevel: [error específico]
```

---

## 🔧 **Posibles Soluciones Según Resultado**

### **Si hay errores de CustomTkinter:**
- Verificar instalación: `pip install customtkinter`
- Verificar versión: `pip show customtkinter`
- Reinstalar si es necesario

### **Si hay errores de parent window:**
- Problema con la ventana padre
- Solución: Usar `parent=None` temporalmente

### **Si hay errores de importación:**
- Problema con dependencias
- Solución: Verificar imports y paths

---

## 📝 **Próximos Pasos**

1. **Ejecutar Prueba 1** y reportar resultados
2. **Según el resultado**, aplicar la solución correspondiente
3. **Una vez identificado el problema**, limpiar el debug
4. **Verificar que la solución funciona** en condiciones normales

---

**Con este debug detallado, definitivamente identificaremos y solucionaremos el problema del botón copiar faltante.**
