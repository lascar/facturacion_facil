-- =============================================================================
-- MIGRACIÓN BASE DE DATOS PARA VERIFACTU
-- Real Decreto 1007/2023
-- =============================================================================
-- Ejecutar este script para añadir las tablas necesarias para Verifactu
-- Fecha: 2024-01-15
-- =============================================================================

-- =============================================================================
-- TABLA: verifactu_config
-- Configuración del sistema Verifactu
-- =============================================================================
CREATE TABLE IF NOT EXISTS verifactu_config (
    id INTEGER PRIMARY KEY CHECK (id = 1),  -- Solo un registro permitido
    
    -- Datos del emisor (obligatorios)
    nif_emisor TEXT NOT NULL,
    nombre_emisor TEXT NOT NULL,
    
    -- Modalidad de operación
    modo_operacion TEXT DEFAULT 'NO_VERIFACTU' 
        CHECK (modo_operacion IN ('VERIFACTU', 'NO_VERIFACTU')),
    
    -- Entorno de trabajo
    entorno TEXT DEFAULT 'PRUEBAS' 
        CHECK (entorno IN ('PRUEBAS', 'PRODUCCION')),
    
    -- Certificado digital para envío a AEAT
    certificado_digital_path TEXT,
    certificado_password TEXT,  -- Encriptado con Fernet
    
    -- URLs de servicios AEAT
    url_api_pruebas TEXT DEFAULT 'https://prewww2.aeat.es/wlpl/SSII-FACT/ws/',
    url_api_produccion TEXT DEFAULT 'https://www2.agenciatributaria.gob.es/wlpl/SSII-FACT/ws/',
    
    -- Configuración de cola de envíos
    reintentos_maximos INTEGER DEFAULT 3,
    intervalo_reintento_minutos INTEGER DEFAULT 30,
    
    -- Timestamp
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar configuración por defecto
INSERT OR IGNORE INTO verifactu_config (id, nif_emisor, nombre_emisor, modo_operacion, entorno)
VALUES (1, '', '', 'NO_VERIFACTU', 'PRUEBAS');

-- =============================================================================
-- TABLA: verifactu_registros
-- Registros de facturas en el sistema Verifactu
-- =============================================================================
CREATE TABLE IF NOT EXISTS verifactu_registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Referencia a la factura
    factura_id INTEGER NOT NULL,
    
    -- Identificadores
    numero_factura TEXT NOT NULL,
    serie_factura TEXT DEFAULT '',
    
    -- Estado del registro
    estado TEXT DEFAULT 'PENDIENTE' 
        CHECK (estado IN ('PENDIENTE', 'ENVIADO', 'ACEPTADO', 'RECHAZADO', 'ERROR', 'ANULADO')),
    
    -- Respuesta de AEAT
    id_envio_aeat TEXT UNIQUE,
    codigo_respuesta_aeat TEXT,
    descripcion_respuesta_aeat TEXT,
    
    -- Datos de envío
    fecha_envio TIMESTAMP,
    fecha_respuesta TIMESTAMP,
    respuesta_completa TEXT,  -- JSON con respuesta completa
    
    -- Hash y firma para integridad
    hash_registro TEXT NOT NULL,  -- SHA-256 de los datos de la factura
    hash_cadena_anterior TEXT,     -- Hash del registro anterior (cadena de integridad)
    firma_electronica TEXT,        -- Firma del registro
    
    -- Código QR
    codigo_qr_data TEXT,           -- Datos del código QR en base64
    url_verificacion TEXT,         -- URL pública de verificación
    
    -- Contador de reintentos
    reintentos INTEGER DEFAULT 0,
    
    -- Datos técnicos
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE RESTRICT
);

-- Índices para verifactu_registros
CREATE INDEX IF NOT EXISTS idx_verifactu_factura_id ON verifactu_registros(factura_id);
CREATE INDEX IF NOT EXISTS idx_verifactu_estado ON verifactu_registros(estado);
CREATE INDEX IF NOT EXISTS idx_verifactu_id_envio ON verifactu_registros(id_envio_aeat);
CREATE INDEX IF NOT EXISTS idx_verifactu_fecha ON verifactu_registros(fecha_envio);

-- =============================================================================
-- TABLA: verifactu_cola_envios
-- Cola de envíos pendientes (para procesamiento asíncrono)
-- =============================================================================
CREATE TABLE IF NOT EXISTS verifactu_cola_envios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Referencia a la factura
    factura_id INTEGER NOT NULL,
    
    -- Prioridad (1 = máxima, 10 = mínima)
    prioridad INTEGER DEFAULT 5 CHECK (prioridad BETWEEN 1 AND 10),
    
    -- Estado en la cola
    estado_cola TEXT DEFAULT 'PENDIENTE' 
        CHECK (estado_cola IN ('PENDIENTE', 'PROCESANDO', 'COMPLETADO', 'ERROR')),
    
    -- Contador de intentos
    intentos INTEGER DEFAULT 0,
    max_intentos INTEGER DEFAULT 3,
    
    -- Mensaje de error si falló
    mensaje_error TEXT,
    
    -- Timestamps
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_procesamiento TIMESTAMP,
    fecha_ultimo_intento TIMESTAMP,
    
    -- Foreign key
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
);

-- Índices para cola de envíos
CREATE INDEX IF NOT EXISTS idx_cola_estado ON verifactu_cola_envios(estado_cola);
CREATE INDEX IF NOT EXISTS idx_cola_prioridad ON verifactu_cola_envios(prioridad);

-- =============================================================================
-- TABLA: verifactu_historial_cambios
-- Auditoría de cambios en facturas (para inalterabilidad)
-- =============================================================================
CREATE TABLE IF NOT EXISTS verifactu_historial_cambios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Referencia
    factura_id INTEGER NOT NULL,
    tipo_cambio TEXT NOT NULL 
        CHECK (tipo_cambio IN ('CREACION', 'MODIFICACION', 'ANULACION', 'ENVIO')),
    
    -- Datos del cambio
    datos_anteriores TEXT,  -- JSON con datos anteriores
    datos_nuevos TEXT,      -- JSON con datos nuevos
    
    -- Hash de verificación
    hash_cambio TEXT NOT NULL,
    
    -- Usuario que realizó el cambio (si aplica)
    usuario TEXT,
    
    -- Timestamp
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
);

-- Índice para historial
CREATE INDEX IF NOT EXISTS idx_historial_factura ON verifactu_historial_cambios(factura_id);

-- =============================================================================
-- TABLA: verifactu_registro_anulaciones
-- Registro específico para facturas anuladas
-- =============================================================================
CREATE TABLE IF NOT EXISTS verifactu_registro_anulaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Referencias
    factura_id INTEGER NOT NULL,
    registro_verifactu_id INTEGER NOT NULL,
    
    -- Datos de la anulación
    fecha_anulacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo_anulacion TEXT,
    
    -- Envío a AEAT de la anulación
    id_envio_anulacion_aeat TEXT,
    estado_anulacion TEXT DEFAULT 'PENDIENTE'
        CHECK (estado_anulacion IN ('PENDIENTE', 'ENVIADA', 'ACEPTADA', 'RECHAZADA')),
    
    -- Foreign keys
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE RESTRICT,
    FOREIGN KEY (registro_verifactu_id) REFERENCES verifactu_registros(id) ON DELETE RESTRICT
);

-- =============================================================================
-- TRIGGER: Actualizar fecha de modificación automáticamente
-- =============================================================================
CREATE TRIGGER IF NOT EXISTS trigger_verifactu_config_update
AFTER UPDATE ON verifactu_config
BEGIN
    UPDATE verifactu_config SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trigger_verifactu_registros_update
AFTER UPDATE ON verifactu_registros
BEGIN
    UPDATE verifactu_registros SET fecha_actualizacion = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- =============================================================================
-- VISTAS ÚTILES
-- =============================================================================

-- Vista de facturas pendientes de envío
CREATE VIEW IF NOT EXISTS vista_facturas_pendientes_envio AS
SELECT 
    f.id AS factura_id,
    f.numero_factura,
    f.fecha_factura,
    f.total_factura,
    vr.estado AS estado_verifactu,
    vr.reintentos,
    c.nombre AS nombre_cliente
FROM facturas f
LEFT JOIN verifactu_registros vr ON f.id = vr.factura_id
LEFT JOIN clientes c ON f.cliente_id = c.id
WHERE vr.estado IN ('PENDIENTE', 'ERROR') 
   OR vr.estado IS NULL;

-- Vista de estadísticas de envío
CREATE VIEW IF NOT EXISTS vista_estadisticas_verifactu AS
SELECT 
    estado,
    COUNT(*) AS cantidad,
    MIN(fecha_envio) AS primer_envio,
    MAX(fecha_envio) AS ultimo_envio
FROM verifactu_registros
GROUP BY estado;

-- =============================================================================
-- DATOS INICIALES
-- =============================================================================

-- Asegurar que existe la configuración por defecto
INSERT OR IGNORE INTO verifactu_config (id, nif_emisor, nombre_emisor) 
VALUES (1, 'PENDIENTE_CONFIGURAR', 'PENDIENTE_CONFIGURAR');

-- =============================================================================
-- FIN DEL SCRIPT
-- =============================================================================
