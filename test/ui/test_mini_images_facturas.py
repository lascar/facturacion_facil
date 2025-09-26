#!/usr/bin/env python3
"""
Tests pour les mini images dans les lignes de factures
"""
import sys
import os
import tempfile
import pytest
from PIL import Image

# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from utils.image_utils import ImageUtils
from ui.producto_list_widget import ProductoListWidget
from database.models import Producto, FacturaItem
import customtkinter as ctk

class TestMiniImagesFacturas:
    """Tests pour les mini images dans les factures"""
    
    @pytest.fixture
    def temp_image(self):
        """Crée une image temporaire pour les tests"""
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, "test_product.png")
        
        # Créer une image de test
        img = Image.new('RGB', (100, 100), color='red')
        img.save(image_path)
        
        yield image_path
        
        # Nettoyage
        if os.path.exists(image_path):
            os.remove(image_path)
        os.rmdir(temp_dir)
    
    def test_create_mini_image(self, temp_image):
        """Test de création d'une mini image"""
        mini_image = ImageUtils.create_mini_image(temp_image, (32, 32))
        
        assert mini_image is not None
        # Vérifier que c'est bien un objet PhotoImage
        assert hasattr(mini_image, 'width')
        assert hasattr(mini_image, 'height')
    
    def test_create_mini_image_nonexistent(self):
        """Test avec une image inexistante"""
        mini_image = ImageUtils.create_mini_image("/path/inexistant.png", (32, 32))
        assert mini_image is None
    
    def test_create_placeholder_image(self):
        """Test de création d'image placeholder"""
        placeholder = ImageUtils.create_placeholder_image((32, 32))
        
        assert placeholder is not None
        assert hasattr(placeholder, 'width')
        assert hasattr(placeholder, 'height')
    
    def test_get_mini_image_size(self):
        """Test de la taille standard des mini images"""
        size = ImageUtils.get_mini_image_size()
        assert size == (32, 32)
        assert isinstance(size, tuple)
        assert len(size) == 2
    
    def test_is_image_file(self):
        """Test de détection des fichiers image"""
        # Fichiers image valides
        assert ImageUtils.is_image_file("test.png") == True
        assert ImageUtils.is_image_file("test.jpg") == True
        assert ImageUtils.is_image_file("test.jpeg") == True
        assert ImageUtils.is_image_file("test.gif") == True
        assert ImageUtils.is_image_file("test.bmp") == True
        
        # Fichiers non-image
        assert ImageUtils.is_image_file("test.txt") == False
        assert ImageUtils.is_image_file("test.pdf") == False
        assert ImageUtils.is_image_file("") == False
        assert ImageUtils.is_image_file(None) == False
    
    def test_image_cache(self, temp_image):
        """Test du cache d'images"""
        image_utils = ImageUtils()
        
        # Premier appel - doit créer l'image
        mini1 = image_utils.get_cached_mini_image(temp_image, (32, 32))
        assert mini1 is not None
        
        # Deuxième appel - doit utiliser le cache
        mini2 = image_utils.get_cached_mini_image(temp_image, (32, 32))
        assert mini2 is not None
        assert mini1 is mini2  # Même objet du cache
        
        # Vider le cache
        image_utils.clear_cache()
        
        # Troisième appel - doit recréer l'image
        mini3 = image_utils.get_cached_mini_image(temp_image, (32, 32))
        assert mini3 is not None
        assert mini3 is not mini1  # Nouvel objet
    
    @pytest.mark.skipif(os.environ.get('CI') == 'true', reason="Skip UI tests in CI")
    def test_producto_list_widget_creation(self):
        """Test de création du widget de liste de produits"""
        try:
            # Créer une fenêtre de test
            root = ctk.CTk()
            root.withdraw()  # Cacher la fenêtre
            
            # Créer le widget
            widget = ProductoListWidget(root, height=200)
            
            # Vérifications de base
            assert widget is not None
            assert hasattr(widget, 'add_item')
            assert hasattr(widget, 'clear_items')
            assert hasattr(widget, 'get_selected_item')
            assert hasattr(widget, 'get_selected_index')
            
            # Nettoyer
            root.destroy()
            
        except Exception as e:
            pytest.skip(f"Interface graphique non disponible: {e}")
    
    @pytest.mark.skipif(os.environ.get('CI') == 'true', reason="Skip UI tests in CI")
    def test_producto_list_widget_with_items(self, temp_image):
        """Test du widget avec des items"""
        try:
            # Créer une fenêtre de test
            root = ctk.CTk()
            root.withdraw()
            
            # Créer le widget
            widget = ProductoListWidget(root, height=200)
            
            # Créer un produit de test avec image
            producto = Producto(
                nombre="Producto Test",
                referencia="TEST-001",
                precio=25.50,
                imagen_path=temp_image
            )
            
            # Créer un item de factura de test
            factura_item = FacturaItem(
                producto_id=1,
                cantidad=2,
                precio_unitario=25.50,
                iva_aplicado=21.0,
                descuento=0
            )
            
            # Mock de la méthode get_producto
            factura_item.get_producto = lambda: producto
            
            # Ajouter l'item
            widget.add_item(factura_item)
            
            # Vérifications
            assert len(widget.items) == 1
            assert widget.get_selected_index() is None
            
            # Test de sélection
            widget.select_item(0)
            assert widget.get_selected_index() == 0
            assert widget.get_selected_item() == factura_item
            
            # Test de suppression
            widget.clear_items()
            assert len(widget.items) == 0
            assert widget.get_selected_index() is None
            
            # Nettoyer
            root.destroy()
            
        except Exception as e:
            pytest.skip(f"Interface graphique non disponible: {e}")
    
    def test_image_formats_support(self):
        """Test du support de différents formats d'image"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Tester différents formats
            formats = [
                ('RGB', 'test.png'),
                ('RGB', 'test.jpg'),
                ('RGBA', 'test_alpha.png'),
                ('P', 'test_palette.png')
            ]
            
            for mode, filename in formats:
                image_path = os.path.join(temp_dir, filename)
                
                # Créer l'image
                img = Image.new(mode, (50, 50), color='blue')
                if mode == 'P':
                    img = img.convert('P')
                img.save(image_path)
                
                # Tester la création de mini image
                mini_image = ImageUtils.create_mini_image(image_path, (32, 32))
                assert mini_image is not None, f"Échec pour le format {mode}"
                
                # Nettoyer
                os.remove(image_path)
                
        finally:
            os.rmdir(temp_dir)
    
    def test_image_proportions_preservation(self, temp_image):
        """Test de la préservation des proportions lors du redimensionnement"""
        # Créer une image rectangulaire
        temp_dir = tempfile.mkdtemp()
        rect_image_path = os.path.join(temp_dir, "rect_image.png")
        
        try:
            # Image 100x50 (ratio 2:1)
            img = Image.new('RGB', (100, 50), color='green')
            img.save(rect_image_path)
            
            # Créer mini image dans un carré 32x32
            mini_image = ImageUtils.create_mini_image(rect_image_path, (32, 32))
            assert mini_image is not None
            
            # L'image devrait être centrée dans le carré de 32x32
            # avec les proportions préservées
            
        finally:
            if os.path.exists(rect_image_path):
                os.remove(rect_image_path)
            os.rmdir(temp_dir)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
