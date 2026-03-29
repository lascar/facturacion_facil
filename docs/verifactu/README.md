# Documentación Verifactu - Facturación Fácil

## 📋 ¿Qué es Verifactu?

Verifactu es el sistema de verificación de facturas de la Agencia Estatal de Administración Tributaria (AEAT) de España, establecido por el **Real Decreto 1007/2023**.

### Fechas de Entrada en Vigor

| Tipo de Entidad | Fecha Obligatoria |
|-----------------|-------------------|
| Personas Jurídicas (SL, SA, etc.) | 1 de enero 2026 |
| Autónomos y Comunidades de Bienes | 1 de julio 2026 |

---

## 📁 Estructura de Documentación

```
docs/verifactu/
├── README.md                          # Este archivo
├── PROPUESTA_IMPLEMENTACION.md        # Propuesta técnica detallada
├── EJEMPLO_IMPLEMENTACION.py          # Código de ejemplo
├── MIGRACION_BASE_DATOS.sql           # Script SQL de migración
└── CHECKLIST_IMPLEMENTACION.md        # Checklist de tareas
```

---

## 🚀 Opciones de Implementación

### Opción 1: Integración Completa Verifactu (Recomendada)
- **Envío automático** a AEAT
- **Códigos QR** verificables
- **Firma electrónica** de registros
- **Mayor automatización**

**Ideal para:** Empresas con volumen medio/alto de facturación

### Opción 2: Modalidad "NO Verifactu"
- **Sin envío automático** a AEAT
- **Hash de integridad** garantizado
- **Exportación manual** para AEAT
- **Menor complejidad técnica**

**Ideal para:** Pequeños negocios, autónomos

### Opción 3: Exportación para Gestoría
- **Exportación estándar** (XML/JSON)
- **Compatible** con software homologado
- **Delegación** en gestoría

**Ideal para:** Negocios que trabajan con gestoría externa

---

## 🛠️ Requisitos Técnicos

### Dependencias Python
```
# Core
hashlib>=3.9
pycryptodome>=3.15.0

# QR Codes
qrcode[pil]>=7.3

# API AEAT (opcional para VERIFACTU)
zeep>=4.0.0
requests>=2.28.0
cryptography>=37.0.0
```

### Infraestructura
- Certificado digital de representante
- Acceso a entornos de pruebas AEAT
- Base de datos SQLite con extensión para migraciones

---

## 📊 Resumen de Cambios en Base de Datos

### Nuevas Tablas
1. **`verifactu_config`** - Configuración del sistema
2. **`verifactu_registros`** - Registros de facturas
3. **`verifactu_cola_envios`** - Cola de envíos pendientes
4. **`verifactu_historial_cambios`** - Auditoría de modificaciones
5. **`verifactu_registro_anulaciones`** - Registro de anulaciones

### Campos Añadidos a Facturas
- Hash de integridad (SHA-256)
- ID de envío AEAT
- Estado de verificación
- Código QR

---

## 🔒 Aspectos de Seguridad

### Obligatorios
- ✅ Encriptación de contraseñas de certificados
- ✅ Hash SHA-256 para integridad
- ✅ Cadena de hash para inalterabilidad
- ✅ Logs sin datos sensibles
- ✅ Auditoría completa de cambios

### Recomendados
- Rotación periódica de certificados
- Backup encriptado de registros
- Acceso restringido a configuración

---

## 📅 Plan de Implementación Sugerido

| Fase | Duración | Descripción |
|------|----------|-------------|
| 1 | 1 semana | Preparación y análisis |
| 2 | 1 semana | Base de datos y migraciones |
| 3 | 2 semanas | Servicios core |
| 4 | 1 semana | Integración UI |
| 5 | 1 semana | Generación de PDF |
| 6 | 2 semanas | Integración AEAT real |
| 7 | 1 semana | Testing y validación |
| 8 | 1 semana | Documentación y despliegue |

**Total estimado:** 10 semanas (2.5 meses)

---

## ⚡ Quick Start (Desarrollo)

```bash
# 1. Crear base de datos de pruebas
cd database
python test_database.py

# 2. Aplicar migración Verifactu
sqlite3 test_facturacion.db < docs/verifactu/MIGRACION_BASE_DATOS.sql

# 3. Ejecutar ejemplo
python docs/verifactu/EJEMPLO_IMPLEMENTACION.py

# 4. Ejecutar tests
pytest test/unit/test_verifactu.py -v
```

---

## ❓ Preguntas Frecuentes

### ¿Es obligatorio implementar Verifactu?
Sí, si utilizas un sistema informático de facturación y:
- Eres persona jurídica (desde 01/01/2026)
- Eres autónomo (desde 01/07/2026)
- Emites facturas a otros empresarios/profesionales

### ¿Qué pasa si no cumplo?
Sanciones administrativas, multas económicas y posible cancelación del registro como contribuyente.

### ¿Puedo usar Facturación Fácil sin Verifactu?
Sí, si:
- Facturas solo en papel (sin sistema informático)
- Estás en régimen de recargo de equivalencia y no emites facturas
- Realizas operaciones no empresariales

### ¿Necesito certificado digital?
Solo si implementas la modalidad VERIFACTU (envío automático). Para NO_VERIFACTU no es necesario.

---

## 📚 Referencias Oficiales

- [Real Decreto 1007/2023 - BOE](https://www.boe.es/buscar/doc.php?id=BOE-A-2023-18003)
- [Portal Verifactu - AEAT](https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu.html)
- [Especificaciones Técnicas SII](https://www.agenciatributaria.gob.es/static_files/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Modelos_y_formularios/IVA/SII/especificaciones_mensajes_suministro_inmediato_informacion.pdf)

---

## 🤝 Contribución

Para reportar problemas o sugerir mejoras en la implementación de Verifactu:

1. Crear un issue con etiqueta `verifactu`
2. Incluir logs y pasos para reproducir
3. Especificar modalidad (VERIFACTU/NO_VERIFACTU)

---

## ⚠️ Disclaimer Legal

Esta documentación tiene fines técnicos. Consulta con un asesor fiscal antes de implementar Verifactu en producción para asegurar el cumplimiento completo de la normativa vigente.

---

**Última actualización:** Marzo 2026  
**Versión documentación:** 1.0
