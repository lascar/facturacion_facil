# 🚀 Guía de Inicio Rápido - Facturación Fácil

## ⚡ **Instalación en 3 Pasos**

### **Paso 1: Descargar y Preparar**
```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd facturacion_facil

# Activar entorno (automático)
source activate.sh
```

### **Paso 2: Verificar Instalación**
```bash
# Test rápido del sistema
python test/demo/demo_complete_solution_test.py
```

### **Paso 3: Ejecutar Aplicación**
```bash
# Iniciar Facturación Fácil
python main.py
```

---

## 🎯 **Primer Uso - Configuración Inicial**

### **1. Configurar tu Empresa** 🏢
1. Abrir la aplicación
2. Ir a **"Organización"**
3. Completar datos de tu empresa:
   - Nombre y razón social
   - NIF/CIF
   - Dirección completa
   - Teléfono y email
4. **Subir logo** (opcional pero recomendado)
5. Guardar configuración

### **2. Agregar tus Primeros Productos** 📦
1. Ir a **"Productos"**
2. Clic en **"Nuevo Producto"**
3. Completar información:
   - Nombre del producto
   - Referencia/código
   - Precio de venta
   - IVA aplicable
   - Categoría
4. **Subir imagen** del producto (opcional)
5. Guardar producto

### **3. Configurar Stock Inicial** 📊
1. Ir a **"Stock"**
2. Localizar tus productos
3. Establecer **cantidad inicial** disponible
4. Configurar **stock mínimo** para alertas
5. Guardar cambios

### **4. Crear tu Primera Factura** 🧾
1. Ir a **"Nueva Factura"**
2. Completar **datos del cliente**:
   - Nombre/empresa
   - NIF (opcional)
   - Dirección
   - Contacto
3. **Agregar productos**:
   - Seleccionar producto
   - Indicar cantidad
   - Verificar precio y descuentos
4. **Revisar totales** (automáticos)
5. **Guardar factura**
6. **Confirmar actualización de stock**

### **5. Generar PDF de Factura** 📄
1. En la lista de facturas
2. **Clic en la factura** deseada
3. Clic en **"Exportar PDF"**
4. El PDF se genera y abre automáticamente
5. Guardar o imprimir según necesites

---

## 🔧 **Comandos Útiles**

### **Mantenimiento**
```bash
# Limpiar base de datos (CUIDADO: elimina todos los datos)
./clean_databases.sh

# Ejecutar todos los tests
./run_organized_tests.sh all

# Validar sistema completo
python validation_complete_2024.py
```

### **Diagnóstico**
```bash
# Monitor en tiempo real
python test/demo/demo_real_time_monitor.py

# Test de rendimiento
python test/performance/benchmark_solution.py

# Verificar logs
tail -f logs/facturacion_facil.log
```

---

## 💡 **Consejos Importantes**

### **✅ Buenas Prácticas**
- **Configura tu empresa PRIMERO** antes de crear facturas
- **Establece stock inicial** para todos tus productos
- **Confirma siempre** las actualizaciones de stock
- **Haz backup** de tu base de datos regularmente
- **Revisa los PDFs** antes de enviarlos a clientes

### **⚠️ Puntos de Atención**
- El **stock se actualiza automáticamente** al guardar facturas
- Las **validaciones son opcionales** pero recomendadas
- Los **PDFs se guardan** en la carpeta `facturas_pdf/`
- Los **logs están** en la carpeta `logs/` para diagnóstico

### **🛡️ Seguridad de Datos**
- La base de datos está en `facturacion.db`
- **Haz copias de seguridad** regularmente
- Usa `./clean_databases.sh` solo para **limpiar datos de prueba**

---

## 🆘 **Solución de Problemas**

### **Problema: La aplicación no inicia**
```bash
# Verificar entorno
source activate.sh
python --version  # Debe ser 3.13+

# Reinstalar dependencias
pip install -r requirements.txt

# Test de diagnóstico
python test_structure.py
```

### **Problema: Error en base de datos**
```bash
# Reinicializar base de datos
python -c "from database.database import db; db.init_database()"

# Verificar integridad
python test/demo/demo_complete_solution_test.py
```

### **Problema: PDFs no se generan**
```bash
# Verificar ReportLab
pip install reportlab

# Test específico de PDF
python test/demo/demo_test_pdf_export.py
```

---

## 📞 **Obtener Ayuda**

1. **Documentación completa**: `docs/README.md`
2. **Guías específicas**: `docs/features/`
3. **Logs del sistema**: `logs/facturacion_facil.log`
4. **Tests de validación**: `test/validate_solution.py`

---

## 🎉 **¡Listo para Facturar!**

Con estos pasos ya tienes **Facturación Fácil** completamente configurado y listo para gestionar tu negocio.

**¡Disfruta de la aplicación!** 🚀
