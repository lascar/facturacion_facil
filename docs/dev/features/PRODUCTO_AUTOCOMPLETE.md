> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**

---

# 🔍 Sistema de Autocompletado de Productos

## 📋 Descripción

Sistema avanzado de autocompletado para la selección de productos en Facturación Fácil. Permite a los usuarios buscar y seleccionar productos escribiendo el nombre, referencia o categoría, con sugerencias en tiempo real y información de stock.

## ✨ Características

### 🎯 **Funcionalidades Principales**
- **Búsqueda en tiempo real** mientras el usuario escribe
- **Búsqueda múltiple** por nombre, referencia y categoría
- **Información de stock** integrada en las sugerencias
- **Navegación con teclado** (flechas, Enter, Escape)
- **Validación automática** de selecciones
- **Interfaz intuitiva** con dropdown de sugerencias

### 📊 **Información Mostrada**
- **Nombre del producto** y referencia
- **Precio** formateado con moneda
- **Estado del stock** (Disponible, Stock bajo, Sin stock)
- **Categoría** del producto
- **Indicadores visuales** de estado de stock

## 🚀 Uso Básico

### **Implementación Simple**
```python
from common.producto_autocomplete import ProductoAutocomplete

# Crear widget de autocompletado
autocomplete = ProductoAutocomplete(
    parent_frame,
    placeholder_text="Buscar producto...",
    include_stock_info=True
)
autocomplete.pack(fill="x", padx=10, pady=5)

# Configurar callback para selección
def on_producto_selected(producto_data):
    print(f"Seleccionado: {producto_data['nombre']}")

autocomplete.set_on_select_callback(on_producto_selected)
```

### **Obtener Producto Seleccionado**
```python
# Obtener objeto Producto completo
producto = autocomplete.get_selected_producto()

# Obtener solo el ID
producto_id = autocomplete.get_selected_producto_id()

# Obtener información completa
info = autocomplete.get_selected_producto_info()
```

## 🔧 API Detallada

### **Clase ProductoAutocomplete**

#### **Constructor**
```python
ProductoAutocomplete(
    parent,
    placeholder_text="Buscar producto...",
    include_stock_info=True,
    width=300,
    height=40,
    **kwargs
)
```

**Parámetros:**
- `parent`: Widget padre
- `placeholder_text`: Texto de placeholder
- `include_stock_info`: Incluir información de stock
- `width/height`: Dimensiones del widget

#### **Métodos Principales**
```python
# Configuración
def set_on_select_callback(callback)
def refresh_data()
def clear()

# Selección programática
def set_producto_by_id(producto_id)
def set_producto_by_referencia(referencia)

# Obtener datos
def get_selected_producto()
def get_selected_producto_id()
def get_selected_producto_info()

# Validación
def validate_selection()
def get_validation_error()

# Filtrado
def filter_by_categoria(categoria)
```

## 🎨 Integración en Diálogos

### **Reemplazo de ComboBox en Facturas**
```python
# ANTES: ComboBox estático
self.producto_combo = ctk.CTkComboBox(
    frame, 
    values=productos_names,
    command=self.on_producto_selected
)

# DESPUÉS: Autocompletado dinámico
self.producto_autocomplete = ProductoAutocomplete(
    frame,
    placeholder_text="Escriba para buscar producto...",
    include_stock_info=True
)
self.producto_autocomplete.set_on_select_callback(self.on_producto_selected)
```

### **Callback de Selección**
```python
def on_producto_selected(self, producto_data):
    """Callback cuando se selecciona un producto"""
    # Actualizar información del producto
    self.update_producto_info(producto_data)
    
    # Cargar datos en formulario
    self.precio_entry.delete(0, tk.END)
    self.precio_entry.insert(0, str(producto_data['precio']))
    
    self.iva_entry.delete(0, tk.END)
    self.iva_entry.insert(0, str(producto_data['iva_recomendado']))
```

## 🔍 Funcionalidades de Búsqueda

### **Tipos de Búsqueda Soportados**
```python
# Por nombre (parcial, insensible a mayúsculas)
"laptop" → "Laptop Dell Inspiron"
"MOUSE" → "Mouse Logitech"

# Por referencia
"DELL001" → "Laptop Dell Inspiron - DELL001"
"LOG" → "Mouse Logitech - LOG001"

# Por categoría
"Periféricos" → Todos los productos de esa categoría
"informática" → Productos de informática
```

### **Configuración de Búsqueda**
```python
# Personalizar campos de búsqueda
autocomplete.search_fields = ['nombre', 'referencia', 'categoria', 'descripcion']

# Configurar límites
autocomplete.min_chars = 2      # Mínimo 2 caracteres
autocomplete.max_suggestions = 15  # Máximo 15 sugerencias
```

## 📊 Información de Stock Integrada

### **Indicadores de Stock**
- **🟢 Stock: 25** - Stock normal (>5 unidades)
- **🟡 Stock bajo: 3** - Stock bajo (1-5 unidades)  
- **🔴 Sin stock** - Sin unidades disponibles

### **Formato de Sugerencias**
```
Laptop Dell Inspiron - DELL001 - €899.99 (Stock: 15)
Mouse Logitech - LOG001 - €25.50 (Stock bajo: 3)
Teclado Mecánico - TEC001 - €75.00 (Sin stock)
```

## ⌨️ Navegación con Teclado

### **Atajos de Teclado**
- **↓ (Flecha abajo)**: Navegar a siguiente sugerencia
- **↑ (Flecha arriba)**: Navegar a sugerencia anterior
- **Enter**: Seleccionar sugerencia actual
- **Escape**: Cerrar dropdown de sugerencias
- **Tab**: Salir del campo (mantiene texto)

### **Comportamiento del Dropdown**
- **Aparece automáticamente** al escribir (≥2 caracteres)
- **Se oculta** al seleccionar o presionar Escape
- **Sigue el foco** del campo de entrada
- **Posicionamiento inteligente** debajo del campo

## ✅ Validación y Manejo de Errores

### **Validación de Selección**
```python
# Validar que hay una selección válida
if autocomplete.validate_selection():
    producto = autocomplete.get_selected_producto()
    # Procesar producto...
else:
    error = autocomplete.get_validation_error()
    messagebox.showerror("Error", error)
```

### **Mensajes de Error**
- `"Debe seleccionar un producto"` - Campo vacío
- `"Debe seleccionar un producto válido de la lista"` - Texto no coincide con selección

### **Manejo de Casos Edge**
```python
# Producto no encontrado por ID
if not autocomplete.set_producto_by_id(999):
    print("Producto no encontrado")

# Referencia inexistente
if not autocomplete.set_producto_by_referencia("NOEXISTE"):
    print("Referencia no encontrada")
```

## 🧪 Testing y Demostración

### **Ejecutar Tests**
```bash
# Tests unitarios completos
python -m pytest test/ui/test_producto_autocomplete.py -v

# Test específico
python -m pytest test/ui/test_producto_autocomplete.py::TestProductoAutocomplete::test_search_by_name -v
```

### **Demostración Interactiva**
```bash
# Demo completa con datos de ejemplo
python test/demo/demo_producto_autocomplete.py
```

### **Tests Incluidos**
- ✅ Inicialización del componente
- ✅ Búsqueda por nombre, referencia, categoría
- ✅ Búsqueda insensible a mayúsculas
- ✅ Límites de caracteres y sugerencias
- ✅ Selección programática por ID/referencia
- ✅ Validación de selecciones
- ✅ Callbacks y eventos
- ✅ Limpieza y refrescado de datos

## 🔄 Migración desde ComboBox

### **Pasos de Migración**
1. **Reemplazar imports**:
   ```python
   from common.producto_autocomplete import ProductoAutocomplete
   ```

2. **Cambiar creación del widget**:
   ```python
   # Antes
   self.producto_combo = ctk.CTkComboBox(...)
   
   # Después  
   self.producto_autocomplete = ProductoAutocomplete(...)
   ```

3. **Actualizar callback**:
   ```python
   # Antes
   def on_producto_selected(self, selection):
       # Buscar producto por texto...
   
   # Después
   def on_producto_selected(self, producto_data):
       # Usar producto_data directamente...
   ```

4. **Cambiar validación**:
   ```python
   # Antes
   if not self.producto_seleccionado:
       errors.append("Seleccione un producto")
   
   # Después
   if not self.producto_autocomplete.validate_selection():
       errors.append(self.producto_autocomplete.get_validation_error())
   ```

## 🎯 Beneficios del Nuevo Sistema

### **Para Usuarios**
- **Búsqueda más rápida**: Escribir es más rápido que navegar en lista
- **Búsqueda flexible**: Por nombre, referencia o categoría
- **Información inmediata**: Stock visible en las sugerencias
- **UX moderna**: Comportamiento similar a buscadores web

### **Para Desarrolladores**
- **API simple**: Fácil de implementar y usar
- **Altamente configurable**: Personalizable para diferentes casos
- **Bien testado**: Suite completa de tests automatizados
- **Documentado**: Documentación completa y ejemplos

### **Para el Sistema**
- **Performance**: Carga datos una vez, filtra en memoria
- **Escalable**: Funciona bien con cientos de productos
- **Mantenible**: Código modular y reutilizable
- **Extensible**: Fácil añadir nuevas funcionalidades

## 🔧 Configuración Avanzada

### **Personalizar Formato de Display**
```python
class CustomProductoAutocomplete(ProductoAutocomplete):
    def format_suggestion_display(self, item):
        # Formato personalizado
        return f"{item['nombre']} | {item['referencia']} | €{item['precio']:.2f}"
    
    def get_selected_display_text(self, item):
        # Texto en el campo al seleccionar
        return f"{item['nombre']} ({item['referencia']})"
```

### **Filtrado Personalizado**
```python
# Filtrar solo productos con stock
autocomplete.suggestions_data = [
    item for item in autocomplete.suggestions_data 
    if item.get('stock_info') and 'Sin stock' not in item['stock_info']
]
```

---

**El sistema de autocompletado transforma la experiencia de selección de productos en Facturación Fácil!** 🎉

*Búsqueda rápida, intuitiva y con información completa al alcance de los dedos.*

---

> **[⬆️ Volver al índice](../INDEX.md)** | **[📖 README](../README.md)** | **[🏠 Inicio](../../README.md)**
