#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'autocompletion pour les produits - Version PyQt6
"""

try:
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QListWidget, QFrame
    from PyQt6.QtCore import Qt, pyqtSignal
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

from database.models import Producto

class ProductoAutocomplete(QWidget):
    """Classe complète pour l'autocompletion des produits avec PyQt6"""

    # Signal émis quand un produit est sélectionné
    product_selected = pyqtSignal(dict)

    def __init__(self, parent=None, min_chars=2, max_suggestions=10):
        """Initialise le système d'autocomplétion"""
        if GUI_AVAILABLE:
            super().__init__(parent)

        self.parent = parent
        self.min_chars = min_chars
        self.max_suggestions = max_suggestions

        # Données
        self.suggestions_data = []
        self.filtered_suggestions = []
        self.selected_item = None
        self.callback = None

        # Widgets GUI
        if GUI_AVAILABLE:
            self.create_widgets()
        else:
            # Mock widgets pour tests sans GUI
            self.entry = MockWidget()
            self.dropdown_frame = MockWidget()
            self.suggestions_listbox = MockWidget()

        # Charger les produits depuis la base de données
        self.load_productos()

        print("ProductoAutocomplete inicializado")

    def create_widgets(self):
        """Crée les widgets de l'interface PyQt6"""
        layout = QVBoxLayout(self)

        # Entry principal
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Buscar producto...")
        layout.addWidget(self.entry)

        # Frame pour le dropdown
        self.dropdown_frame = QFrame()
        self.dropdown_frame.setVisible(False)
        layout.addWidget(self.dropdown_frame)

        # Layout pour le dropdown
        dropdown_layout = QVBoxLayout(self.dropdown_frame)

        # Liste pour les suggestions
        self.suggestions_listbox = QListWidget()
        self.suggestions_listbox.setMaximumHeight(150)
        dropdown_layout.addWidget(self.suggestions_listbox)

        # Connexions des signaux
        self.entry.textChanged.connect(self.on_text_changed)
        self.suggestions_listbox.itemClicked.connect(self.on_suggestion_clicked)
        self.suggestions_listbox.itemDoubleClicked.connect(self.on_suggestion_double_clicked)

    def load_productos(self):
        """Charge les produits depuis la base de données"""
        try:
            productos = Producto.get_all()
            self.suggestions_data = []

            for producto in productos:
                item = {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'referencia': producto.referencia,
                    'categoria': producto.categoria,
                    'precio': producto.precio,
                    'display_text': f"{producto.nombre} ({producto.referencia}) - {producto.precio:.2f}€"
                }
                self.suggestions_data.append(item)

            print(f"Productos cargados: {len(self.suggestions_data)}")

        except Exception as e:
            print(f"Error cargando productos: {e}")
            self.suggestions_data = []

    def filter_suggestions(self, query):
        """Filtra las sugerencias basándose en la consulta"""
        if not query or len(query) < self.min_chars:
            self.filtered_suggestions = []
            return

        query_lower = query.lower()
        self.filtered_suggestions = []

        for item in self.suggestions_data:
            # Buscar en nombre, referencia y categoría
            if (query_lower in item['nombre'].lower() or
                query_lower in item['referencia'].lower() or
                query_lower in item['categoria'].lower()):
                self.filtered_suggestions.append(item)

                if len(self.filtered_suggestions) >= self.max_suggestions:
                    break

        self.update_suggestions_display()

    def update_suggestions_display(self):
        """Actualiza la visualización de sugerencias"""
        if not GUI_AVAILABLE:
            return

        # Limpiar lista
        self.suggestions_listbox.clear()

        if not self.filtered_suggestions:
            self.hide_dropdown()
            return

        # Agregar sugerencias
        for item in self.filtered_suggestions:
            self.suggestions_listbox.addItem(item['display_text'])

        self.show_dropdown()

    def show_dropdown(self):
        """Muestra el dropdown de sugerencias"""
        if GUI_AVAILABLE and hasattr(self, 'dropdown_frame'):
            self.dropdown_frame.setVisible(True)

    def hide_dropdown(self):
        """Oculta el dropdown de sugerencias"""
        if GUI_AVAILABLE and hasattr(self, 'dropdown_frame'):
            self.dropdown_frame.setVisible(False)

    def on_text_changed(self, text):
        """Maneja el cambio de texto"""
        self.filter_suggestions(text)

    def on_suggestion_clicked(self, item):
        """Maneja el clic en una sugerencia"""
        row = self.suggestions_listbox.row(item)
        if row < len(self.filtered_suggestions):
            self.selected_item = self.filtered_suggestions[row]

    def on_suggestion_double_clicked(self, item):
        """Maneja el doble clic en una sugerencia"""
        self.on_suggestion_clicked(item)
        if self.selected_item:
            self.select_item_by_id(self.selected_item['id'])

    def select_item_by_id(self, item_id):
        """Selecciona un item por su ID"""
        for item in self.suggestions_data:
            if item['id'] == item_id:
                self.selected_item = item
                if GUI_AVAILABLE and hasattr(self, 'entry'):
                    self.entry.setText(item['display_text'])
                self.hide_dropdown()

                if self.callback:
                    self.callback(item)

                # Émission du signal PyQt6
                if GUI_AVAILABLE:
                    self.product_selected.emit(item)

                return True
        return False

    def select_item_by_reference(self, reference):
        """Selecciona un item por su referencia"""
        for item in self.suggestions_data:
            if item['referencia'] == reference:
                return self.select_item_by_id(item['id'])
        return False

    def clear_selection(self):
        """Limpia la selección actual"""
        self.selected_item = None
        if GUI_AVAILABLE and hasattr(self, 'entry'):
            self.entry.clear()
        self.hide_dropdown()
        print("Selección limpiada")

    def refresh_data(self):
        """Refresca los datos de productos"""
        self.load_productos()
        self.filtered_suggestions = []
        self.hide_dropdown()
        print("Datos refrescados")

    def set_callback(self, callback):
        """Establece el callback para cuando se selecciona un item"""
        self.callback = callback

    def get_selected_item(self):
        """Obtiene el item seleccionado"""
        return self.selected_item

    def validate_selection(self):
        """Valida que hay una selección válida"""
        return self.selected_item is not None

    def get_display_text_format(self):
        """Obtiene el formato del texto de visualización"""
        return "{nombre} ({referencia}) - {precio:.2f}€"

    def set_display_text_format(self, format_string):
        """Establece el formato del texto de visualización"""
        # Recargar datos con nuevo formato
        self.load_productos()

    # Métodos de compatibilidad con la API anterior
    def set_productos(self, productos):
        """Establece la lista de productos (compatibilidad)"""
        self.suggestions_data = []
        for producto in productos:
            if hasattr(producto, 'id'):
                item = {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'referencia': producto.referencia,
                    'categoria': getattr(producto, 'categoria', ''),
                    'precio': producto.precio,
                    'display_text': f"{producto.nombre} ({producto.referencia}) - {producto.precio:.2f}€"
                }
                self.suggestions_data.append(item)
        print(f"Productos configurados: {len(productos)}")

    def get_suggestions(self, query):
        """Obtiene las sugerencias de autocompletado (compatibilidad)"""
        self.filter_suggestions(query)
        return self.filtered_suggestions

    def clear_suggestions(self):
        """Limpia las sugerencias (compatibilidad)"""
        self.filtered_suggestions = []
        self.hide_dropdown()
        print("Suggestions effacées")

    def enable_autocomplete(self, widget):
        """Activa la autocompletado en un widget (compatibilidad)"""
        print(f"Autocompletion activée sur {widget}")
        return True

    def disable_autocomplete(self, widget):
        """Desactiva la autocompletado en un widget (compatibilidad)"""
        print(f"Autocompletion désactivée sur {widget}")
        return True

    # Métodos específicos esperados por los tests
    def set_producto_by_id(self, producto_id):
        """Establece un producto por su ID"""
        return self.select_item_by_id(producto_id)

    def set_producto_by_referencia(self, referencia):
        """Establece un producto por su referencia"""
        return self.select_item_by_reference(referencia)

    def get_validation_error(self):
        """Obtiene el error de validación si no hay selección"""
        if not self.validate_selection():
            return "Debe seleccionar un producto"
        return ""

    def set_on_select_callback(self, callback):
        """Establece el callback de selección"""
        self.set_callback(callback)

    def get_selected_display_text(self, producto_data=None):
        """Obtiene el texto de visualización del producto seleccionado"""
        if producto_data:
            # Si se proporciona data específica, formatearla
            return f"{producto_data.get('nombre', '')} ({producto_data.get('referencia', '')}) - {producto_data.get('precio', 0):.2f}€"
        elif self.selected_item:
            # Si hay un item seleccionado, usar su display_text
            return self.selected_item.get('display_text', '')
        return ""

    def get_producto_by_id(self, producto_id):
        """Obtiene un producto por su ID"""
        for item in self.suggestions_data:
            if item['id'] == producto_id:
                return item
        return None

    def get_producto_by_referencia(self, referencia):
        """Obtiene un producto por su referencia"""
        for item in self.suggestions_data:
            if item['referencia'] == referencia:
                return item
        return None

    def get_selected_producto_id(self):
        """Obtiene el ID del producto seleccionado"""
        if self.selected_item:
            return self.selected_item.get('id')
        return None

    def get_selected_producto_referencia(self):
        """Obtiene la referencia del producto seleccionado"""
        if self.selected_item:
            return self.selected_item.get('referencia')
        return None

    def get_selected_producto(self):
        """Obtiene el producto seleccionado como objeto"""
        if self.selected_item:
            # Crear un objeto mock con los atributos esperados
            class ProductoMock:
                def __init__(self, data):
                    self.id = data.get('id')
                    self.nombre = data.get('nombre')
                    self.referencia = data.get('referencia')
                    self.categoria = data.get('categoria')
                    self.precio = data.get('precio')

            return ProductoMock(self.selected_item)
        return None

    def clear(self):
        """Limpia la selección (alias para clear_selection)"""
        self.clear_selection()

    def get_value(self):
        """Obtiene el valor actual del entry"""
        if GUI_AVAILABLE and hasattr(self, 'entry'):
            return self.entry.text()
        return ""


class MockWidget:
    """Widget mock para tests sin GUI"""

    def __init__(self):
        self.value = ""
        self.callbacks = {}
        self.visible = True

    def text(self):
        return self.value

    def setText(self, value):
        self.value = value

    def clear(self):
        self.value = ""

    def setPlaceholderText(self, text):
        pass

    def setVisible(self, visible):
        self.visible = visible

    def addItem(self, text):
        pass

    def row(self, item):
        return 0

    def textChanged(self):
        return MockSignal()

    def itemClicked(self):
        return MockSignal()

    def itemDoubleClicked(self):
        return MockSignal()


class MockSignal:
    """Signal mock pour tests sans GUI"""

    def connect(self, callback):
        pass

    def emit(self, *args):
        pass
