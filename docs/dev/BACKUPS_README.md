# 💾 Sistema de Backups - Facturación Fácil

## 📋 Descripción

Sistema completo de gestión de backups para la base de datos de Facturación Fácil.

## 🚀 Scripts Disponibles

### 1. `crear_backup.bat` 💾
Crea un backup manual de la base de datos actual.

**Uso:**
- Doble clic en el archivo
- El backup se guardará en `backups/backup_YYYYMMDD_HHMMSS.db`

**Características:**
- Crea automáticamente la carpeta `backups` si no existe
- Nombra los archivos con fecha y hora
- Muestra el tamaño del backup
- Lista todos los backups disponibles

---

### 2. `restablecer.bat` 🔄
Restaura la base de datos desde un backup existente.

**Uso:**
1. Doble clic en el archivo
2. Selecciona el backup que deseas restaurar de la lista
3. Confirma la operación

**Características:**
- Lista todos los backups disponibles con fecha y tamaño
- Crea un backup de seguridad antes de restaurar
- Permite cancelar la operación
- Muestra información detallada de cada backup

**⚠️ IMPORTANTE:** Antes de restaurar, se crea automáticamente un backup de la base actual con el nombre `antes_restaurar_YYYYMMDD_HHMMSS.db`

---

### 3. `crear_todos_accesos.bat` 🔗
Crea accesos directos para todos los scripts principales.

**Uso:**
- Doble clic en el archivo
- Se crearán 4 accesos directos en la carpeta actual

**Accesos directos creados:**
- 🚀 **Iniciar Facturación.lnk** - Inicia la aplicación
- 💾 **Crear Backup.lnk** - Crea un backup manual
- 🔄 **Restaurar Backup.lnk** - Restaura desde un backup
- 📁 **Ver Backups.lnk** - Abre la carpeta de backups

**💡 Tip:** Puedes copiar estos accesos directos a tu escritorio o cualquier otra carpeta.

---

## 📁 Estructura de Carpetas

```
facturacion_facil/
├── base_de_datos/
│   └── facturacion.db          ← Base de datos actual
├── backups/
│   ├── backup_20231215_1430.db
│   ├── backup_20231216_0900.db
│   └── antes_restaurar_20231216_1000.db
├── crear_backup.bat
├── restablecer.bat
└── crear_todos_accesos.bat
```

---

## 🔄 Flujo de Trabajo Recomendado

### Crear Backups Regulares

1. **Antes de cambios importantes:**
   ```
   Ejecutar: crear_backup.bat
   ```

2. **Backups automáticos:**
   - La aplicación puede crear backups automáticamente
   - Configurable en la ventana de Organización

3. **Frecuencia recomendada:**
   - Diario: Si usas la aplicación frecuentemente
   - Semanal: Para uso ocasional
   - Antes de actualizaciones o cambios importantes

### Restaurar un Backup

1. **Ejecutar:** `restablecer.bat`
2. **Seleccionar** el backup deseado de la lista
3. **Confirmar** la restauración
4. **Verificar** que los datos se restauraron correctamente

---

## ⚠️ Advertencias Importantes

1. **Backup de Seguridad:**
   - Antes de restaurar, se crea automáticamente un backup de la base actual
   - Este backup se guarda como `antes_restaurar_YYYYMMDD_HHMMSS.db`

2. **Espacio en Disco:**
   - Los backups ocupan espacio
   - Elimina backups antiguos periódicamente
   - Cada backup tiene aproximadamente el mismo tamaño que la base de datos

3. **Cierra la Aplicación:**
   - Cierra Facturación Fácil antes de restaurar un backup
   - No restaures mientras la aplicación está en uso

---

## 🛠️ Solución de Problemas

### No se pueden crear backups

**Problema:** Error al crear backup
**Solución:**
- Verifica que existe `base_de_datos/facturacion.db`
- Verifica permisos de escritura en la carpeta
- Asegúrate de tener espacio en disco

### No aparecen backups en la lista

**Problema:** `restablecer.bat` no muestra backups
**Solución:**
- Verifica que exista la carpeta `backups`
- Verifica que haya archivos `.db` en la carpeta
- Crea un backup manual con `crear_backup.bat`

### Error de permisos

**Problema:** "Access Denied" o "Acceso Denegado"
**Solución:**
- Ejecuta como Administrador (clic derecho → Ejecutar como administrador)
- Verifica que no tengas la aplicación abierta
- Verifica permisos de la carpeta

---

## 📊 Gestión de Backups

### Limpieza de Backups Antiguos

Si tienes muchos backups (>10), considera eliminar los más antiguos:

1. Abre la carpeta `backups`
2. Ordena por fecha
3. Elimina los backups más antiguos que ya no necesites
4. **Mantén al menos 3-5 backups recientes**

### Backup Externo

Para mayor seguridad, copia periódicamente la carpeta `backups` a:
- USB externa
- Nube (Google Drive, Dropbox, OneDrive)
- Otro disco duro
- Servidor de red

---

## 💡 Consejos

1. **Nombra tus backups importantes:**
   - Renombra backups importantes: `backup_antes_migracion.db`
   - Añade notas descriptivas al nombre

2. **Verifica los backups:**
   - Ocasionalmente, restaura un backup en una copia de prueba
   - Verifica que los datos se restauran correctamente

3. **Automatiza:**
   - Crea una tarea programada de Windows para backups automáticos
   - Usa el Programador de Tareas de Windows

---

## 📞 Soporte

Si tienes problemas con el sistema de backups:
1. Verifica este README
2. Revisa la sección de Solución de Problemas
3. Contacta al soporte técnico

---

**Última actualización:** 2024-12-27

