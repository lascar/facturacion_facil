# Checklist de Implementación Verifactu

## Fase 1: Preparación (Semana 1)

### Análisis y Planificación
- [ ] Revisar especificaciones técnicas AEAT actualizadas
- [ ] Decidir modalidad: VERIFACTU / NO_VERIFACTU
- [ ] Definir alcance (MVP vs. Completo)
- [ ] Estimar recursos y tiempo

### Infraestructura
- [ ] Solicitar certificado digital de representante
- [ ] Configurar acceso a entorno de pruebas AEAT
- [ ] Preparar base de datos de testing
- [ ] Documentar arquitectura elegida

---

## Fase 2: Base de Datos (Semana 2)

### Migraciones
- [ ] Crear migración `migration_verifactu_v1.sql`
- [ ] Tabla `verifactu_config`
- [ ] Tabla `verifactu_registros`
- [ ] Tabla `verifactu_cola_envios`
- [ ] Tabla `verifactu_historial_cambios`
- [ ] Índices optimizados
- [ ] Vistas de utilidad

### Testing
- [ ] Crear fixtures de prueba para Verifactu
- [ ] Tests de migración
- [ ] Tests de integridad referencial

---

## Fase 3: Servicios Core (Semana 3-4)

### Módulo IntegrityService (`services/integrity_service.py`)
- [ ] Método `calcular_hash_factura()`
- [ ] Método `verificar_integridad()`
- [ ] Método `exportar_registros_json()`
- [ ] Método `exportar_registros_xml()`
- [ ] Tests unitarios
- [ ] Tests de integridad

### Módulo VerifactuService (`services/verifactu_service.py`)
- [ ] Método `registrar_factura()`
- [ ] Método `enviar_a_aeat()` (simulado inicialmente)
- [ ] Método `consultar_estado()`
- [ ] Método `generar_codigo_qr()`
- [ ] Método `anular_factura()`
- [ ] Tests unitarios
- [ ] Tests con mocks de AEAT

---

## Fase 4: Integración UI (Semana 5)

### Configuración
- [ ] Pantalla de configuración Verifactu
- [ ] Formulario de datos del emisor
- [ ] Selector de modalidad
- [ ] Upload de certificado digital
- [ ] Validaciones de campos

### Facturación
- [ ] Indicador de estado Verifactu en lista de facturas
- [ ] Badge de "Verificado" en facturas enviadas
- [ ] Botón de "Enviar a Verifactu" manual
- [ ] Visualización del código QR
- [ ] Opción de descargar justificante

### Alertas y Notificaciones
- [ ] Alerta de errores de envío
- [ ] Notificación de facturas pendientes
- [ ] Resumen diario de estado

---

## Fase 5: Generación de PDF (Semana 6)

### Modificaciones al PDF Generator
- [ ] Incluir código QR en factura
- [ ] Añadir sello "Verifactu Compliant"
- [ ] Mostrar hash de integridad
- [ ] URL de verificación
- [ ] Leyenda legal obligatoria

### Testing
- [ ] Tests de generación de QR
- [ ] Tests de integridad del PDF

---

## Fase 6: Integración AEAT Real (Semana 7-8)

### Conexión API
- [ ] Implementar cliente SOAP/REST
- [ ] Configurar certificado digital
- [ ] Manejo de errores de red
- [ ] Sistema de reintentos
- [ ] Cola de envíos asíncrona

### Seguridad
- [ ] Encriptar contraseña de certificado
- [ ] Validar certificados
- [ ] Logs seguros (sin datos sensibles)
- [ ] Protección contra replay attacks

---

## Fase 7: Testing y Validación (Semana 9)

### Tests Funcionales
- [ ] Tests end-to-end de flujo completo
- [ ] Tests de concurrencia
- [ ] Tests de recuperación de errores
- [ ] Tests de rendimiento

### Validación AEAT
- [ ] Pruebas en entorno de pruebas AEAT
- [ ] Validación de esquemas XML
- [ ] Verificación de códigos de respuesta
- [ ] Prueba de anulaciones

---

## Fase 8: Documentación y Despliegue (Semana 10)

### Documentación
- [ ] Manual de usuario Verifactu
- [ ] Guía de configuración
- [ ] FAQ de problemas comunes
- [ ] Documentación técnica para desarrolladores

### Despliegue
- [ ] Script de migración de producción
- [ ] Backup de base de datos
- [ ] Checklist de verificación post-deploy
- [ ] Plan de rollback

---

## Criterios de Aceptación

### Funcionales
- [ ] Las facturas se registran con hash único
- [ ] Se genera código QR verificable
- [ ] El envío a AEAT funciona correctamente
- [ ] Las anulaciones se procesan adecuadamente
- [ ] Los PDF incluyen todos los elementos Verifactu

### No Funcionales
- [ ] Tiempo de respuesta < 2s para registro local
- [ ] Cola de envíos procesa en < 5 minutos
- [ ] Sin pérdida de datos en caso de error
- [ ] 99.9% de disponibilidad del servicio de registro

### Seguridad
- [ ] Certificados almacenados encriptados
- [ ] Logs sin datos sensibles
- [ ] Acceso restringido a configuración
- [ ] Auditoría de cambios completa

---

## Post-Implementación

### Monitorización
- [ ] Dashboard de estado de envíos
- [ ] Alertas de errores
- [ ] Métricas de rendimiento
- [ ] Informes periódicos

### Mejoras Futuras
- [ ] Integración con más gestorías
- [ ] Soporte para facturas rectificativas
- [ ] Informes avanzados para AEAT
- [ ] API pública para consultas

---

## Notas Importantes

### Seguridad de Datos (CRÍTICO)
- NUNCA almacenar contraseñas de certificados en texto plano
- Usar Fernet o similar para encriptación
- Rotar contraseñas periódicamente
- Auditar accesos a configuración

### Compatibilidad
- Mantener compatibilidad con versiones anteriores
- Migración transparente de datos existentes
- Opción de desactivar Verifactu si es necesario

### Legal
- Consultar con asesor fiscal antes del despliegue
- Verificar cumplimiento de normativa local
- Mantener registros según plazos legales
