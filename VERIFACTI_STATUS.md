# Estado de Implementación Verifacti

> **Documento creado:** 2026-04-07  
> **Última actualización:** Interrupción de sesión  
> **Autor:** Kimi

---

## ✅ COMPLETADO - QR en PDF

### 1. Base de Datos
**Archivo:** `database/migration_manager.py`
- ✅ Columna `qr_verifacti` (TEXT) - Almacena QR en base64
- ✅ Columna `uuid_verifacti` (TEXT) - Almacena UUID de Verifacti
- ✅ Migración automática en `run_all_migrations()`

### 2. Modelo de Datos
**Archivo:** `database/models.py`
- ✅ Clase `Factura` actualizada con atributos:
  - `estado_verifacti`
  - `qr_verifacti`
  - `uuid_verifacti`
- ✅ Método `_get_column_value()` para lectura segura
- ✅ Métodos `get_all()`, `get_by_id()`, `get_by_numero()` actualizados

### 3. Handler de Envío
**Archivo:** `ui/verifacti_factura_handler.py`
- ✅ Función `actualizar_estado_factura_db()` acepta QR y UUID
- ✅ Al enviar factura exitosamente, se guarda QR en BD

### 4. Generador PDF
**Archivo:** `utils/pdf_generator.py`
- ✅ Método `create_verifacti_section()` - Muestra QR en factura
- ✅ Sección con borde verde (#28a745) indicando validación
- ✅ Muestra: QR + Estado + UUID truncado
- ✅ Integrado en `generar_factura_pdf()`

---

## ❌ PENDIENTE - Por hacer

### Prioridad ALTA

| # | Tarea | Descripción | Archivos a modificar |
|---|-------|-------------|---------------------|
| 1 | **Test con API real** | Verificar que el JSON enviado es válido para Verifacti | `services/verifacti_service.py` |
| 2 | **Validar URL API** | Confirmar `https://api.verifacti.com` es correcta | `services/verifacti_service.py` |
| 3 | **Reenvío automático** | Procesar facturas pendientes al iniciar app | `main.py` o servicio background |
| 4 | **Consulta estado** | Verificar periódicamente estado en AEAT | Nuevo servicio/método |

### Prioridad MEDIA (Compliance Verifactu)

| # | Tarea | Descripción | Notas |
|---|-------|-------------|-------|
| 5 | **Declaración responsable** | Crear plantilla accesible para usuarios | Documento legal obligatorio |
| 6 | **Modelos de representación** | Formularios pre-rellenados para firma | BOE diciembre 2024 |
| 7 | **Webhooks** | Endpoint para recibir respuestas AEAT | Si Verifacti soporta |
| 8 | **Validación NIF** | Validar letra/NIF españoles | `verifacti_service.py` |

### Prioridad BAJA (Mejoras)

| # | Tarea | Descripción |
|---|-------|-------------|
| 9 | Dashboard estadísticas | Enviadas, pendientes, errores |
| 10 | Cola background | Procesar envíos asíncronos |
| 11 | Notificaciones UI | Alertar si hay facturas pendientes |
| 12 | Tests unitarios | Cobertura de tests para Verifacti |

---

## 🧪 Cómo Probar lo Implementado

### 1. Aplicar migración
```bash
python -c "from database.migration_manager import MigrationManager; m = MigrationManager(); m.migrate_facturas_verifacti()"
```

### 2. Configurar Verifacti
1. Abrir aplicación → "Organización"
2. Click "📋 Preparar por Verifacti"
3. Rellenar NIF, nombre empresa, API Key
4. Guardar

### 3. Enviar factura de prueba
1. Ir a "Facturas" → crear factura
2. Click "👁️ Ver Detalles"
3. Click "📤 Enviar a Verifacti"
4. Si éxito: estado cambia a "Enviado"

### 4. Verificar QR en PDF
1. Desde detalle de factura, generar PDF
2. Verificar que aparece sección "Verifacti (AEAT)" con QR

---

## ⚠️ Problemas Conocidos / Limitaciones

1. **URL API no verificada** - `https://api.verifacti.com` es placeholder, confirmar URL real
2. **Sin tests automatizados** - No hay tests para Verifacti
3. **Envío síncrono** - La UI se congela si la API es lenta
4. **Sin reintentos automáticos** - Facturas en error quedan en `errores/`

---

## 📁 Estructura de Archivos Verifacti

```
verifacti/
├── enviadas/           # Facturas enviadas (JSON + respuesta)
├── pendientes/         # Sin internet (reenviar manual/auto)
└── errores/            # Errores API (JSON + log)

services/
├── verifacti_service.py          # API client
├── verifacti_config_dialog.py    # UI configuración
└── verifacti_factura_handler.py  # Lógica envío

utils/
└── pdf_generator.py              # QR en PDF (NUEVO)

database/
├── migration_manager.py          # Migraciones BD (NUEVO)
└── models.py                     # Modelo Factura (NUEVO)
```

---

## 🎯 Próxima Acción Recomendada

**Test con API real de Verifacti:**
1. Obtener API Key real del portal Verifacti/AEAT
2. Probar envío de factura de prueba
3. Verificar que el QR recibido es válido
4. Validar formato JSON del payload

---

*Documento generado automáticamente. Actualizar tras cada sesión de desarrollo.*
