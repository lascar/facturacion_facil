# Propuesta de Implementación Verifactu - Facturación Fácil

## Resumen Ejecutivo

Este documento propone las soluciones para adaptar Facturación Fácil al Sistema Verifactu (Real Decreto 1007/2023).

---

## Opción 1: Integración Completa Verifactu (RECOMENDADA)

### Descripción
Implementación de la modalidad "VERIFACTU" con envío automático e inmediato de registros a la AEAT.

### Características
- ✅ Envío automático de facturas a la AEAT
- ✅ Firma electrónica de facturas
- ✅ Códigos QR verificables
- ✅ Registro de operaciones con ID único
- ✅ Consulta de estado de envío

### Arquitectura Propuesta

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Aplicación    │────▶│  VerifactuService │────▶│   AEAT API      │
│   (PyQt5)       │     │   (Nuevo módulo)  │     │   (SOAP/REST)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   SQLite     │
                        │  (colas de   │
                        │   envío)     │
                        └──────────────┘
```

### Componentes a Desarrollar

#### 1.1 Módulo `services/verifactu_service.py`
```python
class VerifactuService:
    """Servicio para la integración con Verifactu AEAT"""
    
    def enviar_factura(self, factura: Factura) -> ResultadoEnvio:
        """Envía una factura a la AEAT"""
        
    def consultar_estado(self, id_envio: str) -> EstadoEnvio:
        """Consulta el estado de un envío"""
        
    def generar_codigo_qr(self, factura: Factura) -> str:
        """Genera el código QR verificable"""
        
    def firmar_factura(self, factura: Factura) -> FacturaFirmada:
        """Firma electrónicamente la factura"""
```

#### 1.2 Modelo de Datos Extendido
```python
@dataclass
class RegistroVerifactu:
    factura_id: int
    id_envio_aeat: str
    estado: str  # PENDIENTE, ENVIADO, ACEPTADO, RECHAZADO
    fecha_envio: datetime
    respuesta_aeat: dict
    codigo_qr: str
    hash_registro: str  # Para garantizar integridad
    firma_electronica: str
```

#### 1.3 Tablas de Base de Datos (Nuevas)
```sql
-- Tabla para registros Verifactu
CREATE TABLE verifactu_registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER NOT NULL,
    id_envio_aeat TEXT UNIQUE,
    estado TEXT DEFAULT 'PENDIENTE',
    fecha_envio TIMESTAMP,
    fecha_respuesta TIMESTAMP,
    respuesta_aeat TEXT,
    codigo_qr TEXT,
    hash_registro TEXT NOT NULL,
    firma_electronica TEXT,
    reintentos INTEGER DEFAULT 0,
    FOREIGN KEY (factura_id) REFERENCES facturas(id)
);

-- Tabla para cola de envíos pendientes
CREATE TABLE verifactu_cola_envios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prioridad INTEGER DEFAULT 5,
    FOREIGN KEY (factura_id) REFERENCES facturas(id)
);

-- Tabla para configuración Verifactu
CREATE TABLE verifactu_config (
    id INTEGER PRIMARY KEY,
    certificado_digital_path TEXT,
    certificado_password TEXT,  -- Encriptado
    entorno TEXT DEFAULT 'PRUEBAS',  -- PRUEBAS o PRODUCCION
    modo_operacion TEXT DEFAULT 'VERIFACTU',  -- VERIFACTU o NO_VERIFACTU
    nif_emisor TEXT NOT NULL,
    nombre_emisor TEXT NOT NULL
);
```

### Flujo de Trabajo

```
1. Usuario crea factura
         │
         ▼
2. Sistema calcula hash de integridad
         │
         ▼
3. Se guarda en cola de envío Verifactu
         │
         ▼
4. Servicio envía a AEAT (asíncrono)
         │
         ▼
5. AEAT responde con ID de registro
         │
         ▼
6. Se genera código QR con ID de registro
         │
         ▼
7. PDF incluye QR y sello Verifactu
```

### Estimación de Esfuerzo
- **Desarrollo**: 80-100 horas
- **Testing**: 20-30 horas
- **Documentación**: 10 horas

---

## Opción 2: Modalidad "NO VERIFACTU" (Alternativa)

### Descripción
Implementación de un sistema homologado sin envío automático, garantizando integridad e inalterabilidad.

### Características
- ✅ Registros firmados digitalmente
- ✅ Hash de integridad por factura
- ✅ Cadena de bloques interna (blockchain ligero)
- ✅ Exportación de registros para AEAT
- ✅ Menor complejidad técnica

### Arquitectura Propuesta

```
┌─────────────────┐     ┌─────────────────────┐
│   Aplicación    │────▶│  IntegrityService   │
│   (PyQt5)       │     │  (Hash + Firma)     │
└─────────────────┘     └─────────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   SQLite     │
                        │  (registros  │
                        │  firmados)   │
                        └──────────────┘
```

### Componentes a Desarrollar

#### 2.1 Módulo `services/integrity_service.py`
```python
class IntegrityService:
    """Servicio para garantizar integridad e inalterabilidad"""
    
    def calcular_hash_factura(self, factura: Factura) -> str:
        """Calcula hash SHA-256 de la factura"""
        
    def firmar_registro(self, hash_registro: str) -> str:
        """Firma el registro con clave privada"""
        
    def verificar_integridad(self, factura_id: int) -> bool:
        """Verifica que la factura no ha sido alterada"""
        
    def exportar_registros(self, fecha_inicio, fecha_fin) -> str:
        """Exporta registros para AEAT (formato XML/JSON)"""
```

#### 2.2 Sistema de Cadena de Integridad
```python
@dataclass
class BloqueRegistro:
    """Bloque de la cadena de integridad"""
    indice: int
    timestamp: datetime
    hash_factura: str
    hash_anterior: str
    datos_factura: dict
    firma: str
```

### Ventajas
- Menor dependencia de servicios externos
- Funciona sin conexión a internet
- Más rápido (sin latencia de red)
- Costo operativo menor

### Desventajas
- Requiere exportación manual si AEAT solicita
- Menos "automatizado" para el usuario final

---

## Opción 3: Exportación para Software Homologado (Intermedia)

### Descripción
Generar archivos de exportación estándar que puedan ser importados por software homologado de terceros.

### Formatos de Exportación
- **XML**: Formato estándar de facturación español
- **CSV**: Para importación en software contable
- **JSON**: Para integraciones modernas

### Ejemplo de Exportación XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Factura xmlns="http://www.aeat.es/verifactu">
    <Cabecera>
        <IDEmisorFactura>NIF_EMISOR</IDEmisorFactura>
        <NumSerieFactura>FAC-2024-0001</NumSerieFactura>
        <FechaExpedicionFactura>2024-01-15</FechaExpedicionFactura>
    </Cabecera>
    <DatosFactura>
        <DescripcionOperacion>Venta de productos</DescripcionOperacion>
        <ImporteTotal>121.00</ImporteTotal>
        <ClaveRegimenEspecialOTrascendencia>01</ClaveRegimenEspecialOTrascendencia>
    </DatosFactura>
</Factura>
```

---

## Recomendación

### Para pequeños negocios (autónomos)
**Opción 2 (NO VERIFACTU)** es suficiente y más práctica.

### Para empresas con volumen medio/alto
**Opción 1 (VERIFACTU completo)** proporciona el mejor flujo de trabajo.

### Para negocios que usan gestoría externa
**Opción 3 (Exportación)** permite trabajar con la gestoría actual.

---

## Próximos Pasos

1. **Decisión de arquitectura** (necesita confirmación del usuario)
2. **Creación de base de datos de pruebas** (siguiendo normas de testing)
3. **Desarrollo incremental** con tests primero (BDD)
4. **Documentación de migración** de base de datos
5. **Testing de integración** con entorno de pruebas AEAT

---

## Referencias

- [Real Decreto 1007/2023](https://www.boe.es/buscar/doc.php?id=BOE-A-2023-18003)
- [Sede AEAT - Verifactu](https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu.html)
- [Especificaciones técnicas AEAT](https://www.agenciatributaria.gob.es/static_files/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Modelos_y_formularios/IVA/SII/especificaciones_mensajes_suministro_inmediato_informacion.pdf)
