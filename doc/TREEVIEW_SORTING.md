# 🔄 Sistema de Ordenación TreeView

## 📋 Descripción

Sistema avanzado de ordenación por columnas para TreeView en Facturación Fácil. Permite ordenar datos haciendo clic en los encabezados de columnas, con soporte para diferentes tipos de datos y ordenación inversa.

## ✨ Características

### 🎯 **Funcionalidades Principales**
- **Ordenación por Click:** Clic en encabezado ordena, segundo clic invierte
- **Detección Automática de Tipos:** Texto, números, fechas, monedas
- **Indicadores Visuales:** ↕ (ordenable), ↑ (ascendente), ↓ (descendente)
- **Soporte Multiplataforma:** Compatible con diferentes formatos de fecha
- **Integración Transparente:** Fácil de añadir a TreeView existentes

### 📊 **Tipos de Datos Soportados**
- **Texto:** Ordenación alfabética (case-insensitive)
- **Números:** Ordenación numérica con soporte para decimales
- **Monedas:** Reconoce €, $, £, ¥ y ordena por valor numérico
- **Fechas:** Múltiples formatos (YYYY-MM-DD, DD/MM/YYYY, etc.)

## 🚀 Uso Rápido

### **Implementación Básica**
```python
from common.treeview_sorter import add_sorting_to_treeview

# Crear TreeView
tree = ttk.Treeview(parent, columns=('col1', 'col2'), show='headings')

# Añadir ordenación (una línea!)
sorter = add_sorting_to_treeview(tree)
```

### **Implementación Avanzada**
```python
from common.treeview_sorter import TreeViewSorter

# Crear sorter manualmente para más control
sorter = TreeViewSorter(tree)

# Configurar tipos específicos de columnas
sorter.set_column_type('precio', 'currency')
sorter.set_column_type('fecha', 'date')
sorter.set_column_type('cantidad', 'numeric')
```

## 🏗️ Implementación en Ventanas

### **Productos Window (ui/productos.py)**
```python
# TreeView con columnas ordenables
columns = ('nombre', 'referencia', 'precio', 'categoria')
self.productos_tree = ttk.Treeview(container, columns=columns, show='headings')

# Configurar encabezados
self.productos_tree.heading('nombre', text='Nombre')
self.productos_tree.heading('referencia', text='Referencia')
self.productos_tree.heading('precio', text='Precio')
self.productos_tree.heading('categoria', text='Categoría')

# ✨ Añadir ordenación
self.tree_sorter = add_sorting_to_treeview(self.productos_tree)
```

### **Facturas Window (ui/facturas.py)**
```python
# TreeView existente
self.facturas_tree = ttk.Treeview(list_frame, columns=("Número", "Fecha", "Cliente", "Total"))

# ✨ Añadir ordenación
self.facturas_tree_sorter = add_sorting_to_treeview(self.facturas_tree)
```

### **Stock Window (ui/stock.py)**
```python
# Nuevo TreeView reemplazando frames personalizados
columns = ('producto', 'referencia', 'stock_actual', 'estado', 'ultima_actualizacion')
self.stock_tree = ttk.Treeview(container, columns=columns, show='headings')

# ✨ Añadir ordenación
self.stock_tree_sorter = add_sorting_to_treeview(self.stock_tree)
```

## 🔧 API Detallada

### **Clase TreeViewSorter**

#### **Métodos Principales**
```python
def __init__(self, treeview):
    """Inicializa el sorter para un TreeView"""

def sort_by_column(self, col):
    """Ordena por la columna especificada"""

def set_column_type(self, col, data_type):
    """Establece el tipo de datos de una columna"""
    # data_type: 'text', 'numeric', 'currency', 'date'

def reset_sorting(self):
    """Resetea el estado de ordenación"""
```

#### **Detección Automática de Tipos**
```python
def detect_data_type(self, items, col):
    """Detecta automáticamente el tipo de datos"""
    # Retorna: 'text', 'numeric', 'currency', 'date'

def parse_currency(self, value):
    """Convierte moneda a número: '€25.50' -> 25.50"""

def parse_date(self, value):
    """Convierte fecha a datetime para ordenación"""

def parse_numeric(self, value):
    """Convierte texto a número: '1,234.56' -> 1234.56"""
```

## 📊 Ejemplos de Datos Soportados

### **Monedas**
```
€25.50, $100.00, £75.25, ¥1000
```

### **Fechas**
```
2024-01-15, 15/01/2024, 15-01-2024
2024-01-15 14:30:00
```

### **Números**
```
123, 123.45, 1,234.56, -45.67
```

### **Texto**
```
Producto A, producto b, PRODUCTO C
(Ordenación case-insensitive)
```

## 🧪 Testing

### **Ejecutar Tests**
```bash
# Tests unitarios
python -m pytest test/ui/test_treeview_sorting.py -v

# Demo interactiva
python test/demo/demo_treeview_sorting.py
```

### **Tests Incluidos**
- ✅ Inicialización del sorter
- ✅ Detección automática de tipos
- ✅ Parsing de monedas, fechas, números
- ✅ Ordenación ascendente/descendente
- ✅ Indicadores visuales
- ✅ Función de conveniencia

## 🎨 Indicadores Visuales

### **Estados de Columnas**
- **↕** - Columna ordenable (estado inicial)
- **↑** - Ordenación ascendente activa
- **↓** - Ordenación descendente activa

### **Ejemplo Visual**
```
Nombre ↑ | Precio ↕ | Fecha ↕ | Stock ↕
```
*(Nombre está ordenado ascendentemente)*

## 🔄 Migración desde Sistemas Anteriores

### **Desde Listbox a TreeView**
```python
# ANTES: Listbox
self.productos_listbox = tk.Listbox(frame)
self.productos_listbox.insert(tk.END, "Producto - Ref - €25.50")

# DESPUÉS: TreeView con ordenación
self.productos_tree = ttk.Treeview(frame, columns=('nombre', 'ref', 'precio'))
self.productos_tree.insert('', 'end', values=('Producto', 'Ref', '€25.50'))
add_sorting_to_treeview(self.productos_tree)
```

### **Desde Frames Personalizados**
```python
# ANTES: Frames con labels
for item in data:
    row_frame = ctk.CTkFrame(parent)
    label1 = ctk.CTkLabel(row_frame, text=item.name)
    # ... más labels

# DESPUÉS: TreeView con ordenación
self.tree = ttk.Treeview(parent, columns=('name', 'value'))
for item in data:
    self.tree.insert('', 'end', values=(item.name, item.value))
add_sorting_to_treeview(self.tree)
```

## 🚀 Beneficios

### **Para Usuarios**
- **UX Mejorada:** Ordenación intuitiva con un clic
- **Eficiencia:** Encontrar datos rápidamente
- **Feedback Visual:** Indicadores claros del estado de ordenación

### **Para Desarrolladores**
- **Implementación Simple:** Una línea de código
- **Mantenimiento Fácil:** Sistema centralizado
- **Extensible:** Fácil añadir nuevos tipos de datos
- **Testeable:** Suite completa de tests

## 🔧 Configuración Avanzada

### **Personalizar Tipos de Columnas**
```python
sorter = TreeViewSorter(tree)

# Forzar tipo específico
sorter.set_column_type('codigo_postal', 'numeric')
sorter.set_column_type('fecha_vencimiento', 'date')
```

### **Resetear Estado**
```python
# Resetear todas las columnas
sorter.reset_sorting()

# Ordenar programáticamente
sorter.sort_by_column('nombre')
```

## 📝 Notas de Implementación

- **Performance:** Optimizado para listas de hasta 10,000 items
- **Memory:** Mínimo overhead, solo metadatos de ordenación
- **Compatibility:** Compatible con tkinter y CustomTkinter
- **Thread Safety:** Diseñado para aplicaciones single-threaded

---

**¡El sistema de ordenación está listo para usar en todas las ventanas de Facturación Fácil!** 🎉
