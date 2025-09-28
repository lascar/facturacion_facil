# 🧪 GUÍA DE TESTING - Solución de Stock

## 📋 **Tests Disponibles**

### **Tests Unitarios**
- `test/demo/demo_simple_stock_test.py` - Test básico del problema
- `test/demo/demo_quick_inheritance_check.py` - Verificación de herencia
- `test/demo/demo_test_direct_dialog.py` - Test diálogo CustomTkinter
- `test/demo/demo_test_simple_dialog.py` - Test diálogo tkinter simple
- `test/demo/demo_test_factura_selection.py` - Test selección de facturas
- `test/demo/demo_test_pdf_export.py` - Test exportación PDF

### **Tests de Integración**
- `test/integration/test_stock_update_integration.py` - Suite completa de tests
- `test/demo/demo_complete_stock_solution_test.py` - Test completo con interfaz

### **Tests de Interfaz**
- `test/demo/demo_interface_debug_test.py` - Test con interfaz gráfica
- `test/demo/demo_real_time_stock_test.py` - Monitor en tiempo real

---

## 🚀 **Cómo Ejecutar los Tests**

### **Test Rápido (Recomendado)**
```bash
# Test completo de toda la solución (Stock + PDF)
python3 test/demo/demo_complete_solution_test.py

# Test completo solo de stock
python3 test/demo/demo_complete_stock_solution_test.py
```

### **Tests Individuales**
```bash
# Test básico del problema
python3 test/demo/demo_simple_stock_test.py

# Test de herencia
python3 test/demo/demo_quick_inheritance_check.py

# Test diálogo CustomTkinter
python3 test/demo/demo_test_direct_dialog.py

# Test diálogo simple
python3 test/demo/demo_test_simple_dialog.py

# Test selección de facturas
python3 test/demo/demo_test_factura_selection.py

# Test exportación PDF
python3 test/demo/demo_test_pdf_export.py
```

### **Tests de Integración**
```bash
# Suite completa de tests de stock
python3 test/integration/test_stock_update_integration.py

# Suite completa de tests de PDF
python3 test/integration/test_pdf_export_integration.py
```

### **Tests con Interfaz Gráfica**
```bash
# Test con interfaz completa
python3 test/demo/demo_interface_debug_test.py

# Monitor en tiempo real
python3 test/demo/demo_real_time_monitor.py
```

### **Tests de Performance**
```bash
# Benchmark de performance
python3 test/performance/benchmark_solution.py

# Stress test del sistema
python3 test/stress/stress_test_solution.py
```

---

## 📊 **Interpretación de Resultados**

### **✅ Resultados Exitosos**

#### **Test Básico**:
```
✅ Método Stock.update_stock funciona: 30 → 22
❌ PROBLEMA CONFIRMADO: Stock NO actualizado automáticamente
✅ Actualización manual exitosa: 50 → 35
```
**Significado**: El método base funciona, el problema está en el flujo.

#### **Test Completo**:
```
📊 RESUMEN DE TESTS:
   Diálogo CustomTkinter: ✅ FUNCIONA
   Diálogo simple: ✅ FUNCIONA  
   Flujo completo: ✅ FUNCIONA
   Procesamiento: ✅ ÉXITO
```
**Significado**: La solución robusta funciona perfectamente.

#### **Test de Integración**:
```
Ran 6 tests in 2.345s
OK
✅ TODOS LOS TESTS D'INTÉGRATION RÉUSSIS
```
**Significado**: Todos los componentes funcionan correctamente juntos.

### **⚠️ Resultados con Advertencias**

#### **Diálogo CustomTkinter Falla**:
```
   Diálogo CustomTkinter: ⚠️ FALLA (normal)
   Diálogo simple: ✅ FUNCIONA
   Flujo completo: ✅ FUNCIONA
```
**Significado**: El fallback funciona correctamente. Es normal en algunos sistemas.

### **❌ Resultados con Errores**

#### **Todos los Diálogos Fallan**:
```
   Diálogo CustomTkinter: ❌ FALLA
   Diálogo simple: ❌ FALLA
   Flujo completo: ❌ FALLA
```
**Significado**: Problema serio. Revisar logs y configuración del sistema.

---

## 🔍 **Diagnóstico de Problemas**

### **Error: "ModuleNotFoundError"**
```bash
# Verificar que estás en el directorio correcto
cd /ruta/al/proyecto/facturacion_facil

# Verificar estructura de directorios
ls -la test/demo/
```

### **Error: "Database not found"**
```bash
# Verificar que la base de datos existe
ls -la database/facturacion.db

# Si no existe, ejecutar la aplicación principal una vez
python3 main.py
```

### **Error: "grab failed: window not viewable"**
**Significado**: Error esperado en algunos sistemas. El fallback debería funcionar.
**Solución**: Verificar que el diálogo simple funciona.

### **Error: "No display"**
**Causa**: Ejecutando en servidor sin interfaz gráfica.
**Solución**: Usar tests que no requieren GUI o configurar X11 forwarding.

---

## 📋 **Checklist de Testing**

### **Antes de Reportar un Problema**:
- [ ] Ejecuté `demo_complete_stock_solution_test.py`
- [ ] Al menos 1 de 3 métodos de diálogo funciona
- [ ] Revisé los logs en `logs/facturacion_facil.log`
- [ ] Probé con la aplicación real
- [ ] Documenté el error específico

### **Para Desarrollo**:
- [ ] Todos los tests unitarios pasan
- [ ] Tests de integración exitosos
- [ ] Probado en interfaz gráfica
- [ ] Logs detallados funcionan
- [ ] Documentación actualizada

### **Para Producción**:
- [ ] Test completo exitoso
- [ ] Al menos 2 métodos de diálogo funcionan
- [ ] Probado con datos reales
- [ ] Usuarios pueden confirmar/cancelar
- [ ] Stock se actualiza correctamente

---

## 🎯 **Tests por Escenario**

### **Escenario 1: Primera Instalación**
```bash
# Test básico para verificar funcionamiento
python3 test/demo/demo_simple_stock_test.py
```

### **Escenario 2: Problema Reportado**
```bash
# Test completo para diagnóstico
python3 test/demo/demo_complete_stock_solution_test.py
```

### **Escenario 3: Desarrollo/Debugging**
```bash
# Suite completa de tests
python3 test/integration/test_stock_update_integration.py
```

### **Escenario 4: Test de Usuario Final**
```bash
# Test con interfaz gráfica
python3 test/demo/demo_interface_debug_test.py
```

---

## 📚 **Documentación Relacionada**

### **Para Usuarios**:
- `docs/USER_GUIDE_STOCK_CONFIRMATION.md` - Guía de uso del diálogo
- `docs/fixes/STOCK_UPDATE_PROBLEM_SOLVED.md` - Problema original resuelto

### **Para Desarrolladores**:
- `docs/fixes/ROBUST_DIALOG_SOLUTION.md` - Solución técnica completa
- `docs/fixes/DIRECT_DIALOG_IMPLEMENTATION.md` - Implementación directa

### **Para Soporte**:
- `logs/facturacion_facil.log` - Logs detallados de la aplicación
- Tests individuales para diagnóstico específico

---

## 🔧 **Comandos Útiles**

### **Limpiar Logs**:
```bash
> logs/facturacion_facil.log
```

### **Ver Logs en Tiempo Real**:
```bash
tail -f logs/facturacion_facil.log
```

### **Buscar Errores Específicos**:
```bash
grep "ERROR" logs/facturacion_facil.log
grep "🔧 DEBUG" logs/facturacion_facil.log
```

### **Verificar Base de Datos**:
```bash
sqlite3 database/facturacion.db ".tables"
sqlite3 database/facturacion.db "SELECT * FROM stock LIMIT 5;"
```

---

**Última Actualización**: 27 de septiembre de 2024  
**Versión**: Solución robusta con múltiples fallbacks  
**Estado**: ✅ **COMPLETAMENTE TESTADO Y DOCUMENTADO**
