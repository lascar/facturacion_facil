# 🔧 GUÍA DE ADMINISTRACIÓN - Facturación Fácil

## 📋 **Resumen para Administradores**

Esta guía está dirigida a administradores del sistema que necesitan:
- **Monitorear** el funcionamiento de la aplicación
- **Diagnosticar** problemas reportados por usuarios
- **Optimizar** el rendimiento del sistema
- **Mantener** la integridad de los datos

---

## 🔍 **Herramientas de Diagnóstico**

### **1. Monitor en Tiempo Real**
```bash
python3 test/demo/demo_real_time_monitor.py
```

**Qué monitorea:**
- ✅ Creación de facturas en tiempo real
- ✅ Actualizaciones de stock automáticas
- ✅ Exportaciones PDF
- ✅ Errores del sistema
- ✅ Estadísticas de uso

**Cuándo usar:**
- Cuando los usuarios reportan problemas
- Para verificar que las funcionalidades funcionan
- Durante períodos de alta actividad

### **2. Validación Completa del Sistema**
```bash
python3 test/validate_solution.py
```

**Qué verifica:**
- ✅ Archivos clave del sistema
- ✅ Métodos principales disponibles
- ✅ Integridad de la base de datos
- ✅ Tests de integración
- ✅ Estado general del sistema

**Resultado esperado:**
```
📊 RESULTADO GENERAL: 15/16 (93.8%)
🎉 EXCELENTE - Solución completamente validada
```

### **3. Benchmark de Performance**
```bash
python3 test/performance/benchmark_solution.py
```

**Qué mide:**
- ⚡ Velocidad de operaciones de base de datos
- ⚡ Performance de creación de facturas
- ⚡ Eficiencia de actualización de stock
- ⚡ Tiempo de selección para PDF

**Cuándo usar:**
- Sistema lento reportado por usuarios
- Después de actualizaciones importantes
- Planificación de capacidad

### **4. Stress Test**
```bash
python3 test/stress/stress_test_solution.py
```

**Qué simula:**
- 💥 Múltiples usuarios creando facturas simultáneamente
- 💥 Carga alta en la base de datos
- 💥 Operaciones concurrentes de stock

**Cuándo usar:**
- Antes de poner en producción
- Después de cambios importantes
- Para verificar estabilidad bajo carga

---

## 📊 **Interpretación de Logs**

### **Ubicación de Logs**
```bash
tail -f logs/facturacion_facil.log
```

### **Tipos de Logs Importantes**

#### **✅ Logs de Funcionamiento Normal**
```
INFO - Factura seleccionada y cargada para edición: FACT-123
INFO - Stock actualizado: Producto 5, nuevo stock: 15
INFO - PDF generado exitosamente: /path/to/pdf
```

#### **🔍 Logs de Debug (Selección PDF)**
```
INFO - 🔍 DEBUG: Buscando factura con número: FACT-123
INFO - 🔍 DEBUG: Factura encontrada: True
INFO - 🔍 DEBUG PDF: selected_factura = <Factura object>
```

#### **⚠️ Logs de Advertencia**
```
WARNING - Diálogo CustomTkinter falló, usando fallback
WARNING - Stock bajo detectado: Producto 3, stock: 2
```

#### **❌ Logs de Error**
```
ERROR - Error en selección de factura: [detalle del error]
ERROR - No se pudo actualizar stock: [detalle del error]
ERROR - ReportLab no instalado para PDF
```

### **Comandos Útiles para Logs**
```bash
# Ver errores recientes
grep "ERROR" logs/facturacion_facil.log | tail -10

# Ver actividad de PDF
grep "PDF\|pdf" logs/facturacion_facil.log | tail -10

# Ver actualizaciones de stock
grep "stock" logs/facturacion_facil.log | tail -10

# Ver logs de debug
grep "🔍 DEBUG" logs/facturacion_facil.log | tail -10
```

---

## 🚨 **Problemas Comunes y Soluciones**

### **Problema: "Exportar PDF no funciona"**

#### **Diagnóstico:**
```bash
# 1. Verificar selección de facturas
python3 test/demo/demo_test_factura_selection.py

# 2. Verificar logs de selección
grep "🔍 DEBUG" logs/facturacion_facil.log
```

#### **Posibles Causas:**
- **Factura no se selecciona**: Logs muestran "Factura encontrada: False"
- **ReportLab no instalado**: Error "ModuleNotFoundError: reportlab"
- **Permisos de escritura**: Error al crear archivo PDF

#### **Soluciones:**
```bash
# Instalar ReportLab
pip install reportlab

# Verificar permisos
ls -la pdfs/

# Test específico de PDF
python3 test/demo/demo_test_pdf_export.py
```

### **Problema: "Stock no se actualiza"**

#### **Diagnóstico:**
```bash
# Test completo de stock
python3 test/demo/demo_complete_stock_solution_test.py

# Verificar logs de stock
grep "stock" logs/facturacion_facil.log | tail -20
```

#### **Posibles Causas:**
- **Usuario cancela diálogo**: Logs muestran "Usuario canceló"
- **Diálogos no aparecen**: Error en sistema de ventanas
- **Error en cálculos**: Problema en actualización de base de datos

#### **Soluciones:**
```bash
# Test de diálogos
python3 test/demo/demo_test_direct_dialog.py

# Verificar herencia de clases
python3 test/demo/demo_quick_inheritance_check.py
```

### **Problema: "Sistema lento"**

#### **Diagnóstico:**
```bash
# Benchmark de performance
python3 test/performance/benchmark_solution.py
```

#### **Métricas a Revisar:**
- **Lectura de facturas > 0.5s**: Base de datos lenta
- **Búsqueda por número > 0.1s**: Falta índice
- **Actualización stock > 0.2s**: Transacciones lentas

#### **Soluciones:**
- Optimizar consultas de base de datos
- Agregar índices
- Implementar paginación para listas grandes

---

## 🔧 **Mantenimiento Preventivo**

### **Verificaciones Semanales**
```bash
# 1. Validación general
python3 test/validate_solution.py

# 2. Verificar logs de errores
grep "ERROR" logs/facturacion_facil.log | wc -l

# 3. Verificar espacio en disco
df -h

# 4. Backup de base de datos
cp database/facturacion.db backups/facturacion_$(date +%Y%m%d).db
```

### **Verificaciones Mensuales**
```bash
# 1. Benchmark de performance
python3 test/performance/benchmark_solution.py

# 2. Stress test
python3 test/stress/stress_test_solution.py

# 3. Limpiar logs antiguos
find logs/ -name "*.log" -mtime +30 -delete

# 4. Verificar integridad de base de datos
sqlite3 database/facturacion.db "PRAGMA integrity_check;"
```

---

## 📈 **Optimización del Sistema**

### **Base de Datos**
```sql
-- Crear índices para mejorar performance
CREATE INDEX IF NOT EXISTS idx_facturas_numero ON facturas(numero_factura);
CREATE INDEX IF NOT EXISTS idx_stock_producto ON stock(producto_id);
CREATE INDEX IF NOT EXISTS idx_factura_items_factura ON factura_items(factura_id);
```

### **Configuración de Logs**
```python
# En utils/logger.py - Ajustar nivel de logging
# Para producción: logging.INFO
# Para debug: logging.DEBUG
```

### **Limpieza de Datos**
```bash
# Eliminar facturas de test antiguas
sqlite3 database/facturacion.db "DELETE FROM facturas WHERE numero_factura LIKE 'TEST-%' AND fecha_factura < date('now', '-30 days');"

# Limpiar movimientos de stock antiguos
sqlite3 database/facturacion.db "DELETE FROM stock_movements WHERE fecha < date('now', '-90 days');"
```

---

## 🚀 **Despliegue y Actualizaciones**

### **Antes de Actualizar**
```bash
# 1. Backup completo
cp -r database/ backups/database_$(date +%Y%m%d)/
cp -r logs/ backups/logs_$(date +%Y%m%d)/

# 2. Test completo
python3 test/demo/demo_complete_solution_test.py

# 3. Verificar que no hay usuarios activos
python3 test/demo/demo_real_time_monitor.py
```

### **Después de Actualizar**
```bash
# 1. Validación completa
python3 test/validate_solution.py

# 2. Test de funcionalidades críticas
python3 test/demo/demo_complete_solution_test.py

# 3. Benchmark de performance
python3 test/performance/benchmark_solution.py

# 4. Monitor en tiempo real por 10 minutos
python3 test/demo/demo_real_time_monitor.py
```

---

## 📞 **Escalación de Problemas**

### **Nivel 1: Problemas Menores**
- Usuario no puede exportar PDF específico
- Factura individual no actualiza stock
- **Solución**: Tests específicos y corrección manual

### **Nivel 2: Problemas Moderados**
- Múltiples usuarios reportan el mismo problema
- Performance degradada
- **Solución**: Benchmark, optimización, reinicio si necesario

### **Nivel 3: Problemas Críticos**
- Sistema no responde
- Corrupción de datos
- Pérdida de funcionalidad principal
- **Solución**: Restaurar backup, análisis completo

### **Información para Soporte**
```bash
# Recopilar información completa
echo "=== INFORMACIÓN DEL SISTEMA ===" > support_info.txt
date >> support_info.txt
python3 --version >> support_info.txt
echo "=== VALIDACIÓN ===" >> support_info.txt
python3 test/validate_solution.py >> support_info.txt 2>&1
echo "=== LOGS RECIENTES ===" >> support_info.txt
tail -50 logs/facturacion_facil.log >> support_info.txt
echo "=== ERRORES ===" >> support_info.txt
grep "ERROR" logs/facturacion_facil.log | tail -20 >> support_info.txt
```

---

**Última Actualización**: 27 de septiembre de 2024  
**Versión**: Guía completa de administración  
**Estado**: ✅ **HERRAMIENTAS COMPLETAS DISPONIBLES**
