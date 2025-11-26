# Manual de Instalación - Facturación Fácil para Windows

## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación de Python](#instalación-de-python)
3. [Descarga del Proyecto](#descarga-del-proyecto)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Instalación de Dependencias](#instalación-de-dependencias)
6. [Primera Ejecución](#primera-ejecución)
7. [Configuración Inicial](#configuración-inicial)
8. [Solución de Problemas](#solución-de-problemas)
9. [Creación de Ejecutable](#creación-de-ejecutable)
10. [Desinstalación](#desinstalación)

---

## 🖥️ Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**:
  - Windows 7 SP1 o superior (32-bit o 64-bit) - **Soporte limitado**
  - Windows 8/8.1 (32-bit o 64-bit) - **Soporte limitado**
  - Windows 10 (64-bit recomendado) - **Soporte completo**
  - **Windows 11 (64-bit) - Soporte completo y recomendado**
- **RAM**:
  - Windows 7/8: 2 GB mínimo, 4 GB recomendado
  - Windows 10: 4 GB mínimo, 8 GB recomendado
  - **Windows 11: 4 GB mínimo, 8 GB recomendado**
- **Espacio en Disco**: 1 GB libres (500 MB para la aplicación + 500 MB para Python y dependencias)
- **Resolución**: 1024x768 mínimo, **1920x1080 recomendado para Windows 11**

### Software Requerido
- **Python**:
  - Windows 7/8: Python 3.8 a 3.11 (Python 3.12+ no soporta Windows 7/8)
  - Windows 10: Python 3.9 a 3.13 (recomendado Python 3.11+)
  - **Windows 11: Python 3.10 a 3.13 (recomendado Python 3.12+)**
- **Conexión a Internet** (para descarga de dependencias)
- **Microsoft Visual C++ Redistributable** (se instala automáticamente con Python)
- **Para Windows 11**: Microsoft Store opcional para instalación simplificada de Python

---

## 🐍 Instalación de Python

### Opción 1: Instalación desde python.org (Recomendada)

#### Para Windows 10/11:
1. **Descargar Python**:
   - Visita [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - **Windows 10**: Haz clic en "Download Python 3.11.x" o "Download Python 3.12.x"
   - **Windows 11**: Haz clic en "Download Python 3.12.x" o "Download Python 3.13.x" (versión más reciente)
   - Descarga el instalador para Windows (64-bit recomendado)

2. **Ejecutar el Instalador**:
   - Ejecuta el archivo descargado (`python-3.12.x-amd64.exe` o `python-3.13.x-amd64.exe`)
   - ⚠️ **IMPORTANTE**: Marca la casilla "Add Python to PATH"
   - Selecciona "Install Now" para instalación estándar
   - O selecciona "Customize installation" para opciones avanzadas
   - **Windows 11**: El instalador detectará automáticamente la compatibilidad

#### Para Windows 7/8/8.1:
1. **Descargar Python Compatible**:
   - Visita [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
   - Busca "Python 3.8.10" o "Python 3.11.x" (última versión compatible)
   - ⚠️ **IMPORTANTE**: Python 3.12+ NO funciona en Windows 7/8
   - Descarga el instalador apropiado:
     - 32-bit: `python-3.8.10.exe` o `python-3.11.x.exe`
     - 64-bit: `python-3.8.10-amd64.exe` o `python-3.11.x-amd64.exe`

2. **Ejecutar el Instalador**:
   - Ejecuta el archivo descargado
   - ⚠️ **IMPORTANTE**: Marca la casilla "Add Python to PATH"
   - Si aparece error de "api-ms-win-crt", instala primero:
     - [Microsoft Visual C++ Redistributable](https://www.microsoft.com/es-es/download/details.aspx?id=48145)
     - [Windows Update KB2999226](https://support.microsoft.com/es-es/help/2999226)

3. **Verificar la Instalación**:
   ```cmd
   # Abrir Command Prompt (cmd) y ejecutar:
   python --version
   pip --version
   ```

   Deberías ver algo como:
   ```
   Python 3.8.10  (o Python 3.11.x)
   pip 21.1.1 from ...
   ```

### Opción 2: Instalación desde Microsoft Store (Solo Windows 10/11)

1. Abre Microsoft Store
2. **Windows 10**: Busca "Python 3.11" o "Python 3.12"
3. **Windows 11**: Busca "Python 3.12" o "Python 3.13" (recomendado)
4. Instala la versión más reciente disponible
5. Python se agregará automáticamente al PATH
6. **Ventaja en Windows 11**: Actualizaciones automáticas y gestión simplificada

**Nota**: Microsoft Store NO está disponible en Windows 7/8/8.1

### Opción 3: Instalación con Winget (Windows 10/11 con Package Manager)

**Solo para Windows 10 versión 1809+ y Windows 11**:
```cmd
# Abrir PowerShell como Administrador
winget install Python.Python.3.12
# O para la versión más reciente:
winget install Python.Python.3.13
```

**Ventajas**:
- Instalación rápida desde línea de comandos
- Actualizaciones fáciles con `winget upgrade Python.Python.3.12`
- Configuración automática del PATH

### Verificación de pip

Si pip no está disponible, instálalo manualmente:
```cmd
python -m ensurepip --upgrade
```

### Problemas Específicos de Windows 7/8

#### Error "api-ms-win-crt-runtime" en Windows 7:
1. Instala las actualizaciones de Windows Update
2. Descarga e instala [Microsoft Visual C++ Redistributable 2015-2019](https://aka.ms/vs/16/release/vc_redist.x64.exe)
3. Reinicia el sistema

#### Error "MSVCP140.dll missing":
1. Descarga [Microsoft Visual C++ Redistributable](https://www.microsoft.com/es-es/download/details.aspx?id=48145)
2. Instala la versión correspondiente a tu sistema (x86 o x64)

#### Python no se reconoce en Windows 7/8:
```cmd
# Agregar manualmente al PATH (reemplaza con tu ruta de instalación):
set PATH=%PATH%;C:\Python38;C:\Python38\Scripts
# O para Python 3.11:
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts
```

---

## 📥 Descarga del Proyecto

### Opción 1: Descarga Directa (Más Fácil)

1. **Descargar ZIP**:
   - Ve al repositorio del proyecto
   - Haz clic en "Code" → "Download ZIP"
   - Guarda el archivo en tu carpeta deseada (ej: `C:\Proyectos\`)

2. **Extraer Archivos**:
   - Haz clic derecho en el archivo ZIP
   - Selecciona "Extraer todo..."
   - Elige la ubicación (ej: `C:\Proyectos\facturacion_facil\`)

### Opción 2: Usando Git (Para Desarrolladores)

1. **Instalar Git** (si no lo tienes):
   - Descarga desde [https://git-scm.com/download/win](https://git-scm.com/download/win)
   - Instala con configuración por defecto

2. **Clonar el Repositorio**:
   ```cmd
   cd C:\Proyectos
   git clone [URL_DEL_REPOSITORIO] facturacion_facil
   cd facturacion_facil
   ```

---

## ⚙️ Configuración del Entorno

### 1. Abrir Command Prompt

#### Windows 10/11:
- Presiona `Win + R`
- Escribe `cmd` y presiona Enter
- O busca "Command Prompt" en el menú Inicio
- O haz clic derecho en el botón Inicio → "Windows PowerShell" o "Terminal"

#### Windows 7/8/8.1:
- Presiona `Win + R`
- Escribe `cmd` y presiona Enter
- O ve a Inicio → Todos los programas → Accesorios → Símbolo del sistema
- **Para Windows 8**: Presiona `Win + X` → "Símbolo del sistema"

### 2. Navegar al Proyecto

```cmd
cd C:\Proyectos\facturacion_facil
```

### 3. Crear Entorno Virtual (Recomendado)

```cmd
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Verificar activación (deberías ver (venv) al inicio de la línea)
```

**Nota para Windows 7/8**: Si el comando `venv` no funciona, usa:
```cmd
# Alternativa para versiones antiguas de Python
python -m pip install virtualenv
python -m virtualenv venv
venv\Scripts\activate
```

**Nota**: Para desactivar el entorno virtual más tarde, usa:
```cmd
deactivate
```

---

## 📦 Instalación de Dependencias

### 1. Actualizar pip

```cmd
python -m pip install --upgrade pip
```

### 2. Instalar Dependencias del Proyecto

```cmd
# Instalar dependencias principales
pip install -r requirements.txt

# Para desarrollo (opcional)
pip install -r requirements-dev.txt
```

### 3. Verificar Instalación

```cmd
pip list
```

Deberías ver las siguientes librerías instaladas:
- `PyQt6==6.6.1` (Framework GUI principal)
- `customtkinter==5.2.2` (Framework GUI de compatibilidad)
- `Pillow==10.4.0` (Procesamiento de imágenes)
- `reportlab==4.2.2` (Generación de PDFs)

**Nota importante**: La aplicación ahora usa **PyQt6** como framework GUI principal, con CustomTkinter como respaldo para compatibilidad.

---

## 🚀 Primera Ejecución

### 1. Ejecutar la Aplicación

```cmd
# Asegúrate de estar en el directorio del proyecto
cd C:\Proyectos\facturacion_facil

# Activar entorno virtual (si lo usas)
venv\Scripts\activate

# Ejecutar la aplicación
python main.py
```

### 2. Verificar Funcionamiento

- La aplicación debería abrirse en una ventana gráfica
- Verás la interfaz principal con menús: Productos, Organización, Stock, Facturas
- La base de datos SQLite se creará automáticamente

---

## 🔧 Configuración Inicial

### 1. Configurar Datos de la Empresa

1. **Abrir Configuración de Organización**:
   - Haz clic en "Organización" en el menú principal

2. **Completar Información**:
   - Nombre de la empresa
   - Dirección completa
   - Teléfono y email
   - Número de identificación fiscal
   - Subir logo (opcional)

3. **Guardar Configuración**:
   - Haz clic en "Guardar"

### 2. Agregar Productos Iniciales

1. **Ir a Gestión de Productos**:
   - Haz clic en "Productos" → "Nuevo Producto"

2. **Completar Información del Producto**:
   - Nombre del producto
   - Referencia/código
   - Precio unitario
   - Porcentaje de IVA
   - Categoría
   - Descripción
   - Imagen (opcional)

3. **Configurar Stock Inicial**:
   - Ve a "Stock"
   - Establece cantidades iniciales para cada producto

---

## 🔍 Solución de Problemas

### Error: "python no se reconoce como comando"

**Solución General**:
1. Reinstala Python marcando "Add Python to PATH"
2. O agrega Python manualmente al PATH

**Para Windows 10/11**:
- Ve a "Configuración" → "Sistema" → "Acerca de" → "Configuración avanzada del sistema"
- Haz clic en "Variables de entorno"
- En "Variables del sistema", busca "Path" y haz clic en "Editar"
- Haz clic en "Nuevo" y agrega las rutas:
  - `C:\Python311\` (o tu versión de Python)
  - `C:\Python311\Scripts\`

**Para Windows 7/8/8.1**:
- Ve a "Panel de Control" → "Sistema" → "Configuración avanzada del sistema"
- Haz clic en "Variables de entorno"
- En "Variables del sistema", busca "Path" y haz clic en "Editar"
- Al final del valor existente, agrega (sin borrar lo anterior):
  - `;C:\Python38\;C:\Python38\Scripts\` (para Python 3.8)
  - `;C:\Python311\;C:\Python311\Scripts\` (para Python 3.11)

**Solución Temporal** (para la sesión actual):
```cmd
set PATH=%PATH%;C:\Python38;C:\Python38\Scripts
# O para Python 3.11:
set PATH=%PATH%;C:\Python311;C:\Python311\Scripts
```

### Error: "No module named 'PyQt6'" o "No module named 'customtkinter'"

**Solución para PyQt6** (framework principal):
```cmd
pip install PyQt6==6.6.1
```

**Solución para CustomTkinter** (compatibilidad):
```cmd
pip install customtkinter==5.2.2
```

**Instalar ambos** (recomendado):
```cmd
pip install PyQt6==6.6.1 customtkinter==5.2.2
```

### Error: "Permission denied" al instalar

**Solución**:
```cmd
# Ejecutar como administrador o usar:
pip install --user -r requirements.txt
```

### La aplicación no se abre o se cierra inmediatamente

**Solución**:
1. Ejecuta desde Command Prompt para ver errores:
   ```cmd
   python main.py
   ```
2. Verifica que todas las dependencias estén instaladas
3. Revisa el archivo de log en `logs/facturacion_facil.log`

### Problemas con imágenes o PDFs

**Solución**:
1. Verifica que Pillow esté instalado correctamente:
   ```cmd
   pip install --upgrade Pillow
   ```
2. Para PDFs, verifica ReportLab:
   ```cmd
   pip install --upgrade reportlab
   ```

### Error de base de datos

**Solución**:
1. Elimina el archivo `facturacion.db` (se recreará automáticamente)
2. O restaura desde backup en la carpeta `database/`

### Problemas Específicos de Windows 7/8

#### Error "SSL Certificate" al instalar paquetes:
```cmd
# Usar versión específica de pip
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### Error "Microsoft Visual C++ 14.0 is required":
1. Descarga e instala [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. O instala [Microsoft Visual Studio Community](https://visualstudio.microsoft.com/es/vs/community/)
3. Reinicia el sistema

#### Rendimiento lento en Windows 7:
- Cierra programas innecesarios
- Aumenta la memoria virtual si es posible
- Considera usar Python 3.8 en lugar de versiones más nuevas

---

## 📦 Creación de Ejecutable

Para crear un archivo `.exe` que no requiera Python instalado:

### 1. Instalar PyInstaller

```cmd
pip install pyinstaller
```

### 2. Crear Ejecutable

```cmd
# Ejecutable simple
pyinstaller --onefile main.py

# Ejecutable con ventana (sin consola)
pyinstaller --onefile --windowed main.py

# Con icono personalizado (opcional)
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
```

### 3. Ubicar el Ejecutable

- El archivo `.exe` se creará en la carpeta `dist/`
- Puedes distribuir este archivo sin necesidad de Python

### 4. Consideraciones por Versión de Windows

#### Para Windows 7/8:
- El ejecutable creado funcionará en la misma versión de Windows o superior
- Si creas el ejecutable en Windows 10, puede no funcionar en Windows 7
- **Recomendación**: Crear el ejecutable en la versión más antigua que quieras soportar

#### Para distribución universal:
```cmd
# Crear ejecutable compatible con Windows 7+
pyinstaller --onefile --windowed --target-architecture=universal main.py
```

### 5. Crear Instalador (Opcional)

Para crear un instalador profesional, puedes usar:
- **Inno Setup** (gratuito): [https://jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)
  - Compatible con Windows 7/8/10/11
- **NSIS** (gratuito): [https://nsis.sourceforge.io/](https://nsis.sourceforge.io/)
  - Compatible con todas las versiones de Windows

---

## 🗑️ Desinstalación

### 1. Eliminar Entorno Virtual

```cmd
# Desactivar entorno virtual
deactivate

# Eliminar carpeta del entorno
rmdir /s venv
```

### 2. Eliminar Proyecto

- Simplemente elimina la carpeta del proyecto
- Los datos se guardan en `facturacion.db` - haz backup si es necesario

### 3. Desinstalar Python (Opcional)

#### Windows 10/11:
- Ve a "Configuración" → "Aplicaciones"
- Busca "Python" y desinstala

#### Windows 7/8/8.1:
- Ve a "Panel de Control" → "Programas y características"
- Busca "Python" y haz clic en "Desinstalar"

---

## 📞 Soporte y Ayuda

### Archivos de Log

Los errores se registran en:
- `logs/facturacion_facil.log` - Log general
- `logs/facturacion_facil_errors.log` - Solo errores

### Backup de Datos

La base de datos se guarda en:
- `database/facturacion.db` - Base de datos principal
- `database/facturacion_backup_*.db` - Backups automáticos

### Recursos Adicionales

- **Documentación completa**: Carpeta `docs/`
- **Tests**: Ejecuta `python run_tests.py` para verificar funcionamiento
- **Configuración**: Archivo `config.json` para ajustes avanzados

---

## ✅ Lista de Verificación Post-Instalación

- [ ] Python instalado y funcionando
- [ ] Proyecto descargado y extraído
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas sin errores
- [ ] Aplicación se ejecuta correctamente
- [ ] Datos de empresa configurados
- [ ] Primer producto creado
- [ ] Stock inicial configurado
- [ ] Primera factura de prueba generada

---

## 🔧 Guía Específica para Windows 7/8/8.1

### Limitaciones Conocidas

#### Windows 7:
- **Python máximo**: 3.8.10 (oficialmente soportado hasta enero 2020)
- **Soporte extendido**: Hasta enero 2023 para Python 3.8
- **Recomendación**: Usar Python 3.8.10 para máxima compatibilidad

#### Windows 8/8.1:
- **Python máximo**: 3.11.x (última versión compatible)
- **Python 3.12+**: NO compatible
- **Recomendación**: Usar Python 3.11.x

### Instalación Paso a Paso para Windows 7

1. **Preparar el Sistema**:
   ```cmd
   # Verificar versión de Windows
   ver

   # Debe mostrar: Microsoft Windows [Version 6.1.xxxx] (Windows 7)
   ```

2. **Instalar Prerrequisitos**:
   - Instalar todas las actualizaciones de Windows Update
   - Descargar [Microsoft Visual C++ Redistributable 2015-2019](https://aka.ms/vs/16/release/vc_redist.x64.exe)
   - Descargar [.NET Framework 4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48)

3. **Descargar Python 3.8.10**:
   - Ve a [https://www.python.org/downloads/release/python-3810/](https://www.python.org/downloads/release/python-3810/)
   - Descarga "Windows x86-64 executable installer" (64-bit)
   - O "Windows x86 executable installer" (32-bit)

4. **Instalar Python**:
   - Ejecuta el instalador como Administrador
   - Marca "Add Python 3.8 to PATH"
   - Selecciona "Install Now"

5. **Verificar Instalación**:
   ```cmd
   python --version
   # Debe mostrar: Python 3.8.10
   ```

### Comandos Específicos para Windows 7/8

#### Configurar PATH manualmente:
```cmd
# Temporal (solo para la sesión actual)
set PATH=%PATH%;C:\Python38;C:\Python38\Scripts

# Permanente (requiere reinicio)
setx PATH "%PATH%;C:\Python38;C:\Python38\Scripts"
```

#### Instalar dependencias con certificados:
```cmd
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip

pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

#### Crear entorno virtual alternativo:
```cmd
# Si venv no funciona, usar virtualenv
python -m pip install virtualenv
python -m virtualenv venv
venv\Scripts\activate
```

### Solución de Problemas Específicos

#### Error "api-ms-win-crt-runtime-l1-1-0.dll":
1. Instala [KB2999226](https://support.microsoft.com/es-es/help/2999226)
2. Instala [Visual C++ Redistributable 2015](https://www.microsoft.com/es-es/download/details.aspx?id=48145)
3. Reinicia el sistema

#### Error "VCRUNTIME140.dll":
1. Descarga [Microsoft Visual C++ Redistributable](https://aka.ms/vs/16/release/vc_redist.x64.exe)
2. Instala como Administrador
3. Reinicia el sistema

#### Python se instala pero no funciona:
```cmd
# Verificar instalación
where python
# Debe mostrar la ruta de instalación

# Si no aparece, agregar manualmente:
set PATH=C:\Python38;C:\Python38\Scripts;%PATH%
```

### Rendimiento en Sistemas Antiguos

#### Optimizaciones para Windows 7:
- Cerrar programas innecesarios antes de ejecutar la aplicación
- Aumentar memoria virtual: Panel de Control → Sistema → Configuración avanzada → Rendimiento → Configuración → Avanzado → Memoria virtual
- Usar tema básico de Windows para liberar recursos

#### Configuración recomendada:
```cmd
# Ejecutar con prioridad normal
python main.py

# O con prioridad baja si el sistema es lento
start /low python main.py
```

---

**¡Felicitaciones! Facturación Fácil está listo para usar en Windows.**

Para cualquier problema adicional, revisa la documentación en la carpeta `docs/` o consulta los archivos de log para más detalles sobre errores específicos.

### 📞 Soporte por Versión de Windows

- **Windows 7**: Soporte limitado, usar Python 3.8.10
- **Windows 8/8.1**: Soporte limitado, usar Python 3.11.x
- **Windows 10**: Soporte completo, usar Python 3.11+ o 3.12+
- **Windows 11**: Soporte completo y optimizado, usar Python 3.12+ o 3.13

---

## 🪟 Guía Específica para Windows 11

### Características Optimizadas para Windows 11

#### Ventajas de Windows 11 para Facturación Fácil:
- **Rendimiento mejorado**: PyQt6 aprovecha las optimizaciones gráficas de Windows 11
- **Interfaz moderna**: Mejor integración con el diseño Fluent Design
- **Gestión de ventanas**: Soporte nativo para Snap Layouts y ventanas múltiples
- **Escalado DPI**: Mejor soporte para pantallas de alta resolución
- **Seguridad**: Windows Defender integrado protege la aplicación y datos

### Instalación Recomendada para Windows 11

#### Método 1: Microsoft Store (Más Fácil)
```cmd
# 1. Abrir Microsoft Store
# 2. Buscar "Python 3.12" o "Python 3.13"
# 3. Instalar directamente
# 4. Python se configura automáticamente
```

#### Método 2: Winget (Recomendado para Desarrolladores)
```powershell
# Abrir Windows Terminal como Administrador
winget install Python.Python.3.12

# Verificar instalación
python --version
pip --version
```

#### Método 3: Instalador Oficial
1. Descargar desde [python.org](https://www.python.org/downloads/)
2. Ejecutar `python-3.12.x-amd64.exe`
3. ✅ Marcar "Add Python to PATH"
4. ✅ Marcar "Install for all users" (recomendado)
5. Seleccionar "Install Now"

### Configuración Específica para Windows 11

#### 1. Configurar Windows Terminal (Recomendado)
```powershell
# Instalar Windows Terminal si no está disponible
winget install Microsoft.WindowsTerminal

# Configurar como terminal por defecto
# Configuración → Sistema → Para desarrolladores → Terminal
```

#### 2. Configurar Variables de Entorno
Windows 11 facilita la configuración:
1. `Win + X` → "Configuración"
2. "Sistema" → "Acerca de" → "Configuración avanzada del sistema"
3. "Variables de entorno"
4. Verificar que Python esté en PATH

#### 3. Optimizar para Pantallas de Alta Resolución
```cmd
# La aplicación detecta automáticamente el escalado DPI
# Para forzar un escalado específico:
set QT_SCALE_FACTOR=1.25  # Para pantallas 4K
python main.py
```

### Características Específicas de Windows 11

#### Integración con el Sistema
- **Notificaciones**: La aplicación puede usar las notificaciones nativas de Windows 11
- **Temas**: Soporte automático para modo claro/oscuro del sistema
- **Widgets**: Posible integración futura con Windows Widgets
- **Microsoft Store**: Distribución simplificada para usuarios finales

#### Rendimiento Optimizado
```cmd
# Configurar prioridad alta para mejor rendimiento
start /high python main.py

# O configurar afinidad de CPU (para sistemas multi-core)
start /affinity 3 python main.py
```

#### Seguridad Mejorada
- **Windows Defender**: Protección automática contra malware
- **SmartScreen**: Verificación de archivos descargados
- **Sandboxing**: Ejecución segura de la aplicación
- **Backup automático**: OneDrive puede respaldar automáticamente los datos

### Solución de Problemas Específicos de Windows 11

#### Error: "Esta aplicación no puede ejecutarse en tu PC"
```cmd
# Verificar arquitectura del sistema
systeminfo | findstr "Tipo de sistema"

# Descargar la versión correcta de Python (64-bit recomendado)
```

#### Problemas con Microsoft Store
```powershell
# Reiniciar Microsoft Store
Get-AppxPackage Microsoft.WindowsStore | Reset-AppxPackage

# O usar instalación alternativa
winget install Python.Python.3.12
```

#### Problemas de Permisos
```powershell
# Ejecutar como Administrador si es necesario
Start-Process powershell -Verb runAs

# O configurar permisos de usuario
icacls "C:\Proyectos\facturacion_facil" /grant %USERNAME%:F /T
```

#### Optimización de Rendimiento
```cmd
# Deshabilitar efectos visuales para mejor rendimiento
systempropertiesperformance.exe
# Seleccionar "Ajustar para obtener el mejor rendimiento"

# O mantener efectos pero optimizar
# Seleccionar "Personalizar" y mantener solo efectos esenciales
```

### Creación de Ejecutable para Windows 11

#### Configuración Optimizada
```cmd
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable optimizado para Windows 11
pyinstaller --onefile --windowed --optimize=2 main.py

# Con configuraciones específicas de Windows 11
pyinstaller --onefile --windowed --target-architecture=universal --optimize=2 --strip main.py
```

#### Distribución en Microsoft Store (Avanzado)
Para distribución profesional:
1. Crear paquete MSIX
2. Registrarse como desarrollador en Microsoft Partner Center
3. Subir la aplicación para certificación
4. Distribución automática a usuarios de Windows 11

### Lista de Verificación para Windows 11

- [ ] Windows 11 versión 21H2 o superior
- [ ] Python 3.12+ instalado y en PATH
- [ ] Windows Terminal configurado
- [ ] PyQt6 y dependencias instaladas
- [ ] Aplicación ejecutándose sin errores
- [ ] Escalado DPI configurado correctamente
- [ ] Windows Defender configurado (excluir carpeta si es necesario)
- [ ] Backup automático configurado (OneDrive recomendado)

### Ventajas Adicionales en Windows 11

#### Para Usuarios Finales:
- Instalación más simple desde Microsoft Store
- Actualizaciones automáticas
- Mejor integración con el sistema
- Rendimiento optimizado

#### Para Desarrolladores:
- Windows Subsystem for Linux (WSL) para desarrollo multiplataforma
- Windows Terminal mejorado
- Package Manager (winget) integrado
- Mejor soporte para contenedores y virtualización

---

**🎉 ¡Facturación Fácil está completamente optimizada para Windows 11!**

La aplicación aprovecha todas las características modernas de Windows 11 para ofrecer la mejor experiencia de usuario posible.
