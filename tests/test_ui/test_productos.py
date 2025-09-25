import pytest
import tkinter as tk
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ui.productos import ProductosWindow
from database.models import Producto

class TestProductosWindow:
    """Tests pour la fenêtre de gestion des produits"""
    
    @pytest.fixture
    def mock_parent(self):
        """Mock de la fenêtre parent"""
        parent = Mock()
        parent.winfo_exists.return_value = True
        return parent
    
    @pytest.fixture
    def productos_window(self, mock_parent):
        """Fixture pour créer une fenêtre de produits"""
        with patch('customtkinter.CTkToplevel'), \
             patch('ui.productos.ProductosWindow.create_widgets'), \
             patch('ui.productos.ProductosWindow.load_productos'):
            window = ProductosWindow(mock_parent)
            
            # Mock des widgets
            window.nombre_entry = Mock()
            window.referencia_entry = Mock()
            window.precio_entry = Mock()
            window.categoria_entry = Mock()
            window.iva_entry = Mock()
            window.descripcion_text = Mock()
            window.imagen_label = Mock()
            window.productos_listbox = Mock()
            
            # Variables
            window.productos = []
            window.selected_producto = None
            window.imagen_path = ""
            
            return window
    
    def test_nuevo_producto(self, productos_window):
        """Test la création d'un nouveau produit"""
        productos_window.limpiar_formulario = Mock()
        
        productos_window.nuevo_producto()
        
        assert productos_window.selected_producto is None
        productos_window.limpiar_formulario.assert_called_once()
    
    def test_limpiar_formulario(self, productos_window):
        """Test le nettoyage du formulaire"""
        # Configurer les mocks
        productos_window.nombre_entry.delete = Mock()
        productos_window.nombre_entry.insert = Mock()
        productos_window.referencia_entry.delete = Mock()
        productos_window.precio_entry.delete = Mock()
        productos_window.categoria_entry.delete = Mock()
        productos_window.iva_entry.delete = Mock()
        productos_window.iva_entry.insert = Mock()
        productos_window.descripcion_text.delete = Mock()
        productos_window.imagen_label.configure = Mock()
        
        # Définir un produit sélectionné
        productos_window.selected_producto = Mock()
        productos_window.imagen_path = "test_path"
        
        productos_window.limpiar_formulario()
        
        # Vérifier que tous les champs sont nettoyés
        productos_window.nombre_entry.delete.assert_called_with(0, tk.END)
        productos_window.referencia_entry.delete.assert_called_with(0, tk.END)
        productos_window.precio_entry.delete.assert_called_with(0, tk.END)
        productos_window.categoria_entry.delete.assert_called_with(0, tk.END)
        productos_window.iva_entry.delete.assert_called_with(0, tk.END)
        productos_window.iva_entry.insert.assert_called_with(0, "21.0")
        productos_window.descripcion_text.delete.assert_called_with("1.0", tk.END)
        
        # Vérifier la réinitialisation des variables
        assert productos_window.selected_producto is None
        assert productos_window.imagen_path == ""
        productos_window.imagen_label.configure.assert_called_with(text="Ninguna imagen seleccionada")
    
    def test_validate_form_valid_data(self, productos_window):
        """Test la validation avec des données valides"""
        # Configurer les mocks avec des données valides
        productos_window.nombre_entry.get.return_value = "Producto Test"
        productos_window.referencia_entry.get.return_value = "TEST001"
        productos_window.precio_entry.get.return_value = "25.50"
        productos_window.iva_entry.get.return_value = "21.0"
        
        errors = productos_window.validate_form()
        
        assert errors == []
    
    def test_validate_form_empty_nombre(self, productos_window):
        """Test la validation avec nom vide"""
        productos_window.nombre_entry.get.return_value = ""
        productos_window.referencia_entry.get.return_value = "TEST001"
        productos_window.precio_entry.get.return_value = "25.50"
        productos_window.iva_entry.get.return_value = "21.0"
        
        errors = productos_window.validate_form()
        
        assert len(errors) > 0
        assert any("Nombre" in error for error in errors)
    
    def test_validate_form_empty_referencia(self, productos_window):
        """Test la validation avec référence vide"""
        productos_window.nombre_entry.get.return_value = "Producto Test"
        productos_window.referencia_entry.get.return_value = ""
        productos_window.precio_entry.get.return_value = "25.50"
        productos_window.iva_entry.get.return_value = "21.0"
        
        errors = productos_window.validate_form()
        
        assert len(errors) > 0
        assert any("Referencia" in error for error in errors)
    
    def test_validate_form_invalid_precio(self, productos_window):
        """Test la validation avec prix invalide"""
        productos_window.nombre_entry.get.return_value = "Producto Test"
        productos_window.referencia_entry.get.return_value = "TEST001"
        productos_window.precio_entry.get.return_value = "invalid_price"
        productos_window.iva_entry.get.return_value = "21.0"
        
        errors = productos_window.validate_form()
        
        assert len(errors) > 0
        assert any("precio" in error.lower() for error in errors)
    
    def test_validate_form_negative_precio(self, productos_window):
        """Test la validation avec prix négatif"""
        productos_window.nombre_entry.get.return_value = "Producto Test"
        productos_window.referencia_entry.get.return_value = "TEST001"
        productos_window.precio_entry.get.return_value = "-10.50"
        productos_window.iva_entry.get.return_value = "21.0"
        
        errors = productos_window.validate_form()
        
        assert len(errors) > 0
        assert any("precio" in error.lower() for error in errors)
    
    def test_validate_form_invalid_iva(self, productos_window):
        """Test la validation avec IVA invalide"""
        productos_window.nombre_entry.get.return_value = "Producto Test"
        productos_window.referencia_entry.get.return_value = "TEST001"
        productos_window.precio_entry.get.return_value = "25.50"
        productos_window.iva_entry.get.return_value = "invalid_iva"
        
        errors = productos_window.validate_form()
        
        assert len(errors) > 0
        assert any("iva" in error.lower() for error in errors)
    
    def test_validate_form_iva_out_of_range(self, productos_window):
        """Test la validation avec IVA hors limites"""
        productos_window.nombre_entry.get.return_value = "Producto Test"
        productos_window.referencia_entry.get.return_value = "TEST001"
        productos_window.precio_entry.get.return_value = "25.50"
        productos_window.iva_entry.get.return_value = "150.0"  # > 100
        
        errors = productos_window.validate_form()
        
        assert len(errors) > 0
        assert any("iva" in error.lower() for error in errors)
    
    @patch('tkinter.messagebox.showerror')
    def test_guardar_producto_validation_error(self, mock_showerror, productos_window):
        """Test la sauvegarde avec erreur de validation"""
        productos_window.validate_form = Mock(return_value=["Error de validation"])
        
        productos_window.guardar_producto()
        
        mock_showerror.assert_called_once()
    
    @patch('tkinter.messagebox.showinfo')
    def test_guardar_producto_new_success(self, mock_showinfo, productos_window):
        """Test la sauvegarde réussie d'un nouveau produit"""
        # Configurer les mocks
        productos_window.validate_form = Mock(return_value=[])
        productos_window.selected_producto = None
        productos_window.nombre_entry.get.return_value = "Nuevo Producto"
        productos_window.referencia_entry.get.return_value = "NEW001"
        productos_window.precio_entry.get.return_value = "15.75"
        productos_window.categoria_entry.get.return_value = "Categoría"
        productos_window.iva_entry.get.return_value = "21.0"
        productos_window.descripcion_text.get.return_value = "Descripción"
        productos_window.imagen_path = ""
        productos_window.load_productos = Mock()
        productos_window.limpiar_formulario = Mock()
        
        with patch.object(Producto, 'save') as mock_save:
            productos_window.guardar_producto()
            
            mock_save.assert_called_once()
            mock_showinfo.assert_called_once()
            productos_window.load_productos.assert_called_once()
            productos_window.limpiar_formulario.assert_called_once()
    
    @patch('tkinter.messagebox.showinfo')
    def test_guardar_producto_update_success(self, mock_showinfo, productos_window):
        """Test la mise à jour réussie d'un produit existant"""
        # Configurer les mocks
        productos_window.validate_form = Mock(return_value=[])
        productos_window.selected_producto = Mock(spec=Producto)
        # Configurer les attributs du producto mock
        productos_window.selected_producto.referencia = "OLD001"  # Valeur initiale pour le logging
        productos_window.selected_producto.save = Mock()

        productos_window.nombre_entry.get.return_value = "Producto Modificado"
        productos_window.referencia_entry.get.return_value = "MOD001"
        productos_window.precio_entry.get.return_value = "25.99"
        productos_window.categoria_entry.get.return_value = "Nueva Categoría"
        productos_window.iva_entry.get.return_value = "10.0"
        productos_window.descripcion_text.get.return_value = "Nueva descripción"
        productos_window.imagen_path = "nueva_imagen.jpg"
        productos_window.load_productos = Mock()
        productos_window.limpiar_formulario = Mock()
        
        productos_window.guardar_producto()
        
        # Vérifier que les propriétés ont été mises à jour
        assert productos_window.selected_producto.nombre == "Producto Modificado"
        assert productos_window.selected_producto.referencia == "MOD001"
        assert productos_window.selected_producto.precio == 25.99
        assert productos_window.selected_producto.categoria == "Nueva Categoría"
        assert productos_window.selected_producto.iva_recomendado == 10.0
        assert productos_window.selected_producto.descripcion == "Nueva descripción"
        assert productos_window.selected_producto.imagen_path == "nueva_imagen.jpg"
        
        productos_window.selected_producto.save.assert_called_once()
        mock_showinfo.assert_called_once()
    
    @patch('tkinter.messagebox.showerror')
    def test_guardar_producto_database_error(self, mock_showerror, productos_window):
        """Test la gestion d'erreur lors de la sauvegarde"""
        productos_window.validate_form = Mock(return_value=[])
        productos_window.selected_producto = None
        productos_window.nombre_entry.get.return_value = "Test"
        productos_window.referencia_entry.get.return_value = "TEST"
        productos_window.precio_entry.get.return_value = "10.0"
        productos_window.categoria_entry.get.return_value = ""
        productos_window.iva_entry.get.return_value = "21.0"
        productos_window.descripcion_text.get.return_value = ""
        productos_window.imagen_path = ""
        
        with patch.object(Producto, 'save', side_effect=Exception("Database error")):
            productos_window.guardar_producto()
            
            mock_showerror.assert_called_once()
    
    @patch('tkinter.messagebox.showwarning')
    def test_eliminar_producto_no_selection(self, mock_showwarning, productos_window):
        """Test la suppression sans sélection"""
        productos_window.selected_producto = None
        
        productos_window.eliminar_producto()
        
        mock_showwarning.assert_called_once()
    
    @patch('tkinter.messagebox.askyesno', return_value=False)
    def test_eliminar_producto_cancelled(self, mock_askyesno, productos_window):
        """Test l'annulation de la suppression"""
        productos_window.selected_producto = Mock(spec=Producto)
        
        productos_window.eliminar_producto()
        
        mock_askyesno.assert_called_once()
        productos_window.selected_producto.delete.assert_not_called()
    
    @patch('tkinter.messagebox.askyesno', return_value=True)
    @patch('tkinter.messagebox.showinfo')
    def test_eliminar_producto_confirmed(self, mock_showinfo, mock_askyesno, productos_window):
        """Test la suppression confirmée"""
        productos_window.selected_producto = Mock(spec=Producto)
        productos_window.load_productos = Mock()
        productos_window.limpiar_formulario = Mock()
        
        productos_window.eliminar_producto()
        
        mock_askyesno.assert_called_once()
        productos_window.selected_producto.delete.assert_called_once()
        mock_showinfo.assert_called_once()
        productos_window.load_productos.assert_called_once()
        productos_window.limpiar_formulario.assert_called_once()
    
    def test_load_producto_to_form(self, productos_window, sample_producto_data):
        """Test le chargement d'un produit dans le formulaire"""
        # Créer un produit avec des données
        producto = Producto(**sample_producto_data)
        producto.id = 1
        productos_window.selected_producto = producto
        
        # Configurer les mocks
        productos_window.nombre_entry.delete = Mock()
        productos_window.nombre_entry.insert = Mock()
        productos_window.referencia_entry.delete = Mock()
        productos_window.referencia_entry.insert = Mock()
        productos_window.precio_entry.delete = Mock()
        productos_window.precio_entry.insert = Mock()
        productos_window.categoria_entry.delete = Mock()
        productos_window.categoria_entry.insert = Mock()
        productos_window.iva_entry.delete = Mock()
        productos_window.iva_entry.insert = Mock()
        productos_window.descripcion_text.delete = Mock()
        productos_window.descripcion_text.insert = Mock()
        productos_window.imagen_label.configure = Mock()
        
        productos_window.load_producto_to_form()
        
        # Vérifier que les champs sont remplis
        productos_window.nombre_entry.insert.assert_called_with(0, producto.nombre)
        productos_window.referencia_entry.insert.assert_called_with(0, producto.referencia)
        productos_window.precio_entry.insert.assert_called_with(0, str(producto.precio))
        productos_window.categoria_entry.insert.assert_called_with(0, producto.categoria)
        productos_window.iva_entry.insert.assert_called_with(0, str(producto.iva_recomendado))
        productos_window.descripcion_text.insert.assert_called_with("1.0", producto.descripcion)
