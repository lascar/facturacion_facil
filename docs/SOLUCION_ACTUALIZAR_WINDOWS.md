# Solución: "Rama master no disponible" en Windows

## 🔍 Problema

Al ejecutar `actualizar.bat` en Windows, aparece el mensaje:
```
⚠️  Rama master no disponible
```

---

## ✅ Soluciones

### Solución 1: Ejecutar Diagnóstico (RECOMENDADO)

1. **Ejecutar el script de diagnóstico**:
   ```
   Doble clic en: diagnostico_git.bat
   ```

2. **Revisar el informe** que muestra:
   - Estado de Git
   - Rama actual
   - Conexión al repositorio
   - Actualizaciones disponibles
   - Archivos críticos

3. **Seguir las recomendaciones** del diagnóstico

---

### Solución 2: Actualización Manual

Si `actualizar.bat` falla, actualizar manualmente:

1. **Abrir PowerShell o CMD** en la carpeta de la aplicación

2. **Verificar rama actual**:
   ```bash
   git branch
   ```

3. **Actualizar desde master**:
   ```bash
   git pull origin master
   ```

4. **Si hay cambios locales**, guardarlos primero:
   ```bash
   git stash
   git pull origin master
   git stash pop
   ```

5. **Actualizar dependencias**:
   ```bash
   python -m pip install -r requirements.txt --upgrade
   ```

---

### Solución 3: Cambios Locales

Si hay cambios locales que impiden la actualización:

**Opción A - Guardar cambios**:
```bash
git stash save "Mis cambios locales"
git pull origin master
git stash pop
```

**Opción B - Descartar cambios** (⚠️ CUIDADO: se pierden los cambios):
```bash
git reset --hard HEAD
git pull origin master
```

**Opción C - Ver qué cambios hay**:
```bash
git status
git diff
```

---

### Solución 4: Problemas de Conexión

Si no puede conectar al repositorio:

1. **Verificar conexión a internet**:
   ```bash
   ping github.com
   ```

2. **Verificar configuración del repositorio**:
   ```bash
   git remote -v
   ```

3. **Actualizar información del remoto**:
   ```bash
   git fetch origin
   ```

4. **Listar ramas disponibles**:
   ```bash
   git branch -r
   ```

---

### Solución 5: Reinstalar desde Cero

Si nada funciona, reinstalar:

1. **Hacer backup de la base de datos**:
   - Copiar `facturacion.db` a un lugar seguro
   - Copiar `config/config.json` si existe

2. **Descargar versión nueva**:
   ```bash
   git clone https://github.com/TU_USUARIO/facturacion_facil.git facturacion_facil_nuevo
   ```

3. **Restaurar datos**:
   - Copiar `facturacion.db` a la nueva carpeta
   - Copiar `config/config.json` a la nueva carpeta

4. **Instalar dependencias**:
   ```bash
   cd facturacion_facil_nuevo
   python -m pip install -r requirements.txt
   ```

---

## 🔧 Mejoras en actualizar.bat

El script `actualizar.bat` ha sido mejorado con:

### ✅ Detección de Cambios Locales

Ahora detecta automáticamente si hay cambios locales y ofrece opciones:
1. Guardar cambios (stash)
2. Descartar cambios
3. Cancelar actualización

### ✅ Mejor Manejo de Ramas

- Verifica que la rama master existe en el remoto
- Intenta primero con merge normal
- Si falla, intenta con rebase
- Muestra mensajes más claros

### ✅ Verificación de Conexión

- Verifica que la rama existe antes de intentar pull
- Muestra mensajes específicos según el problema

---

## 📋 Comandos Útiles

### Ver estado del repositorio
```bash
git status
```

### Ver rama actual
```bash
git branch
```

### Ver ramas remotas
```bash
git branch -r
```

### Ver últimos commits
```bash
git log --oneline -5
```

### Forzar actualización (⚠️ CUIDADO)
```bash
git fetch origin
git reset --hard origin/master
```

---

## 🆘 Soporte

Si ninguna solución funciona:

1. **Ejecutar diagnóstico completo**:
   ```
   diagnostico_git.bat
   ```

2. **Copiar el resultado** del diagnóstico

3. **Contactar soporte** con:
   - Resultado del diagnóstico
   - Mensaje de error exacto
   - Captura de pantalla si es posible

---

## 📝 Notas Importantes

- ✅ **Siempre se crea backup** antes de actualizar
- ✅ Backup en: `backup/facturacion_FECHA.db`
- ⚠️  **No borrar la carpeta backup**
- ⚠️  **Verificar que Git esté instalado**: https://git-scm.com/download/win

---

## 🎯 Prevención

Para evitar problemas futuros:

1. **No modificar archivos** del código fuente directamente
2. **Usar Git correctamente** (commit antes de actualizar)
3. **Mantener backup** de la base de datos regularmente
4. **Actualizar frecuentemente** para evitar conflictos grandes

---

## ✅ Verificación Post-Actualización

Después de actualizar, verificar:

```bash
# 1. Versión de Git
git --version

# 2. Rama actual
git branch

# 3. Estado del repositorio
git status

# 4. Último commit
git log -1

# 5. Archivos críticos
dir main.py
dir facturacion.db
```

---

**Última actualización**: 2025-01-19
**Versión del script**: actualizar.bat v2.0 (mejorado)

