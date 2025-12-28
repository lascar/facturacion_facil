# Changelog: Mejoras en Facturas y Clientes

## Fecha: 2024-12-28

### 🎯 Objetivos
1. Confirmar y mejorar la claridad de que el DNI/NIE/NIF es opcional para los clientes creados desde facturas
2. Corregir el botón "Guardar" para nuevos clientes
3. Reorganizar el layout de la ventana de facturas
4. Optimizar el espacio: Estado sur la même ligne que Número y Fecha

### ✅ Estado Previo
El DNI ya era opcional en el código:
- ✅ Base de datos: columna `dni_nie` permite NULL
- ✅ Validación: acepta valores vacíos
- ✅ Servicio: solo requiere el campo `nombre`
- ✅ UI: algunos labels indicaban "(opcional)"

### 🔧 Cambios Realizados

#### 1. Mejora de Labels en UI (ui/client_autocomplete_widget.py)
**Archivo**: `ui/client_autocomplete_widget.py`
**Líneas**: 422-433

**Antes:**
```python
details_layout.addWidget(QLabel("NIF/CIF (opcional):"), 0, 0)
details_layout.addWidget(QLabel("Teléfono:"), 0, 2)
details_layout.addWidget(QLabel("Email:"), 1, 0)
details_layout.addWidget(QLabel("Dirección:"), 2, 0)
```

**Después:**
```python
details_layout.addWidget(QLabel("NIF/CIF (opcional):"), 0, 0)
details_layout.addWidget(QLabel("Teléfono (opcional):"), 0, 2)
details_layout.addWidget(QLabel("Email (opcional):"), 1, 0)
details_layout.addWidget(QLabel("Dirección (opcional):"), 2, 0)
```

**Razón**: Mayor claridad y consistencia en la interfaz de usuario.

#### 2. Corrección del Botón "Guardar" para Nuevos Clientes
**Archivo**: `ui/client_autocomplete_widget.py`
**Líneas**: 528-531, 576-615

**Problema**: El botón "Guardar" estaba desactivado para nuevos clientes hasta que se modificara algún campo (incluyendo el NIF que es opcional).

**Solución**:
- Activar automáticamente `has_changes = True` para nuevos clientes
- Mantener el botón "Guardar" activado mientras se edita un nuevo cliente
- Para clientes existentes, mantener el comportamiento original (solo activar si hay cambios)

**Código modificado**:
```python
# En show_client_details (línea 530):
self.has_changes = client.get('is_new', False)  # True para nuevos clientes

# En on_data_changed (líneas 593-602):
if self.current_client.get('is_new', False):
    has_changes = True  # Siempre True para nuevos clientes
else:
    # Comparar con datos originales para clientes existentes
    has_changes = (...)
```

**Razón**: Permitir guardar nuevos clientes sin necesidad de rellenar campos opcionales como el NIF.

#### 3. Reorganización del Layout de Facturas
**Archivo**: `ui/facturas_pyqt5.py`
**Líneas**: 130-175, 269-287

**Problema**: El layout anterior tenía toda la información en un solo scroll, con información de factura y cliente en 2 columnas horizontales. Estado estaba sur une deuxième ligne.

**Solución**: Reorganizar en 3 secciones verticales independientes:
1. **Información de Factura**: Fixe (sin scroll), siempre visible, Estado sur la même ligne que Número y Fecha
2. **Cliente**: Con su propio scroll vertical (max 300px - espace gagné)
3. **Productos**: Con su propio scroll vertical (min 300px)

**Código modificado**:
```python
# Antes: Todo en un solo scroll con 2 columnas
scroll_area = QScrollArea()
form_content = QWidget()
self.setup_factura_client_section(content_layout)  # 2 columnas

# Después: 3 secciones independientes
info_group = self.create_basic_info_section()  # Fixe
form_layout.addWidget(info_group)

client_scroll = QScrollArea()  # Scroll propio
client_scroll.setMaximumHeight(300)  # Augmenté de 250px à 300px
client_group = self.create_client_section()
client_scroll.setWidget(client_group)

products_scroll = QScrollArea()  # Scroll propio
products_scroll.setMinimumHeight(300)
```

**Cambios adicionales**:
- Estado movido a la ligne 0 (columnas 4-5) en lugar de ligne 1
- Cliente scroll aumentado de 250px a 300px (espace gagné)

**Métodos eliminados**:
- `setup_factura_client_section()` - Layout de 2 columnas ya no usado
- `setup_basic_info_section()` - Duplicado

**Razón**: Mejor organización visual, navegación más intuitiva, información de factura siempre visible sur UNE ligne.

#### 4. Documentación Creada

**Archivos nuevos:**
- `docs/DNI_OPCIONAL_CONFIRMACION.md`: Documentación técnica completa
- `docs/RESUMEN_DNI_OPCIONAL.md`: Resumen ejecutivo
- `docs/FIX_BOTON_GUARDAR.md`: Documentación de la corrección del botón Guardar
- `docs/LAYOUT_FACTURA_REORGANIZADO.md`: Documentación del nuevo layout
- `test/manual/test_dni_opcional_ui.py`: Test manual para verificación DNI opcional
- `test/manual/test_nuevo_cliente_guardar_button.py`: Test para botón Guardar
- `CHANGELOG_DNI_OPCIONAL.md`: Este archivo

### 🧪 Pruebas Realizadas

#### Test 1: Validación DNI Opcional
```bash
$ python3 test/manual/test_dni_opcional_ui.py
✅ DNI vide est valide (optionnel)
✅ DNI None est valide (optionnel)
✅ DNI avec espaces est valide (optionnel)
✅ DNI valide est accepté
✅ Cliente créé avec succès, ID: 554
✅ Facture créée avec succès, ID: 442
```

#### Test 2: Botón Guardar para Nuevo Cliente
```bash
$ python3 test/manual/test_nuevo_cliente_guardar_button.py
✅ Le bouton Guardar est ACTIVÉ (nuevo cliente sin NIF)
✅ Le bouton Guardar est DÉSACTIVÉ (cliente existente sin cambios)
✅ TEST RÉUSSI
```

### 📊 Impacto

**Archivos modificados**: 2
- `ui/client_autocomplete_widget.py` (líneas 422-433, 528-531, 576-615)
- `ui/facturas_pyqt5.py` (líneas 130-175, eliminación de métodos duplicados)

**Archivos creados**: 7
- `docs/DNI_OPCIONAL_CONFIRMACION.md`
- `docs/RESUMEN_DNI_OPCIONAL.md`
- `test/manual/test_dni_opcional_ui.py`
- `test/manual/test_nuevo_cliente_guardar_button.py`
- `CHANGELOG_DNI_OPCIONAL.md`

**Funcionalidad afectada**:
- ✅ **Mejora**: Botón "Guardar" ahora activado para nuevos clientes sin necesidad de rellenar campos opcionales
- ✅ **Mejora**: Labels más claros indicando "(opcional)" en todos los campos opcionales
- ✅ **Mejora**: Layout de facturas reorganizado con scrolls independientes
- ✅ **Mejora**: Información de factura siempre visible (fixe)
- ✅ **Sin cambios**: La lógica de validación y guardado permanece igual

### ✨ Resultado Final

**DNI Opcional:**
- ✅ El DNI/NIE/NIF es completamente opcional para los clientes
- ✅ Se puede crear un cliente sin DNI
- ✅ Se puede crear una factura con un cliente sin DNI
- ✅ La interfaz indica claramente que es "(opcional)"
- ✅ La validación solo se aplica si se proporciona un valor

**Botón Guardar:**
- ✅ El botón "Guardar" está activado para nuevos clientes
- ✅ No es necesario rellenar campos opcionales para activar el botón
- ✅ Para clientes existentes, el botón solo se activa si hay cambios

**Layout de Facturas:**
- ✅ Información de factura siempre visible (fixe, sin scroll)
- ✅ Cliente con scroll independiente (max 250px)
- ✅ Productos con scroll independiente (min 300px)
- ✅ Mejor organización visual y navegación más intuitiva

### 📝 Notas

1. **Compatibilidad**: Los cambios son 100% compatibles con el código existente
2. **Base de datos**: No se requieren migraciones
3. **Tests**: Todos los tests existentes siguen funcionando
4. **UI**: Mejora de la experiencia de usuario con labels más claros

### 🔍 Verificación

Para verificar que el DNI es opcional, ejecutar:
```bash
python3 test/manual/test_dni_opcional_ui.py
```

### 📚 Referencias

- **Issue/Request**: "le dni ne doit pas être obligatoire pour les clients qui sont créés à partir d'une facture"
- **Documentación**: `docs/RESUMEN_DNI_OPCIONAL.md`
- **Tests**: `test/manual/test_dni_opcional_ui.py`

---

**Autor**: Augment Agent
**Fecha**: 2024-12-28
**Versión**: 1.0

