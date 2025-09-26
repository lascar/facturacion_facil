import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Producto, Organizacion, Stock

class TestProducto:
    """Tests pour le modèle Producto"""
    
    def test_producto_creation(self, sample_producto_data):
        """Test la création d'un produit"""
        producto = Producto(**sample_producto_data)
        
        assert producto.nombre == sample_producto_data['nombre']
        assert producto.referencia == sample_producto_data['referencia']
        assert producto.precio == sample_producto_data['precio']
        assert producto.categoria == sample_producto_data['categoria']
        assert producto.descripcion == sample_producto_data['descripcion']
        assert producto.iva_recomendado == sample_producto_data['iva_recomendado']
        assert producto.id is None  # Nouveau produit n'a pas d'ID
    
    def test_producto_creation_with_defaults(self):
        """Test la création d'un produit avec valeurs par défaut"""
        producto = Producto()
        
        assert producto.nombre == ""
        assert producto.referencia == ""
        assert producto.precio == 0.0
        assert producto.categoria == ""
        assert producto.descripcion == ""
        assert producto.imagen_path == ""
        assert producto.iva_recomendado == 21.0
        assert producto.id is None
    
    def test_producto_save_new(self, sample_producto, temp_db):
        """Test la sauvegarde d'un nouveau produit"""
        # Vérifier qu'il n'a pas d'ID initialement
        assert sample_producto.id is None
        
        # Sauvegarder
        sample_producto.save()
        
        # Vérifier qu'il a maintenant un ID
        assert sample_producto.id is not None
        assert sample_producto.id > 0
        
        # Vérifier qu'une entrée stock a été créée
        stock_results = temp_db.execute_query(
            "SELECT cantidad_disponible FROM stock WHERE producto_id = ?",
            (sample_producto.id,)
        )
        assert len(stock_results) == 1
        assert stock_results[0][0] == 0  # Stock initial à 0
    
    def test_producto_save_existing(self, sample_producto, temp_db):
        """Test la mise à jour d'un produit existant"""
        # Sauvegarder d'abord
        sample_producto.save()
        original_id = sample_producto.id
        
        # Modifier et sauvegarder à nouveau
        sample_producto.nombre = "Nom Modifié"
        sample_producto.precio = 999.99
        sample_producto.save()
        
        # Vérifier que l'ID n'a pas changé
        assert sample_producto.id == original_id
        
        # Vérifier que les modifications ont été sauvegardées
        results = temp_db.execute_query(
            "SELECT nombre, precio FROM productos WHERE id = ?",
            (original_id,)
        )
        assert results[0][0] == "Nom Modifié"
        assert results[0][1] == 999.99
    
    def test_producto_delete(self, sample_producto, temp_db):
        """Test la suppression d'un produit"""
        # Sauvegarder d'abord
        sample_producto.save()
        producto_id = sample_producto.id
        
        # Vérifier qu'il existe
        results = temp_db.execute_query(
            "SELECT COUNT(*) FROM productos WHERE id = ?",
            (producto_id,)
        )
        assert results[0][0] == 1
        
        # Supprimer
        sample_producto.delete()
        
        # Vérifier qu'il n'existe plus
        results = temp_db.execute_query(
            "SELECT COUNT(*) FROM productos WHERE id = ?",
            (producto_id,)
        )
        assert results[0][0] == 0
        
        # Vérifier que le stock associé a aussi été supprimé
        stock_results = temp_db.execute_query(
            "SELECT COUNT(*) FROM stock WHERE producto_id = ?",
            (producto_id,)
        )
        assert stock_results[0][0] == 0
    
    def test_producto_get_all(self, productos_list, temp_db):
        """Test la récupération de tous les produits"""
        # Sauvegarder tous les produits
        for producto in productos_list:
            producto.save()
        
        # Récupérer tous les produits
        all_productos = Producto.get_all()
        
        assert len(all_productos) == len(productos_list)
        
        # Vérifier que tous les produits sont des instances de Producto
        for producto in all_productos:
            assert isinstance(producto, Producto)
            assert producto.id is not None
    
    def test_producto_get_by_id(self, sample_producto, temp_db):
        """Test la récupération d'un produit par ID"""
        # Sauvegarder
        sample_producto.save()
        producto_id = sample_producto.id
        
        # Récupérer par ID
        retrieved_producto = Producto.get_by_id(producto_id)
        
        assert retrieved_producto is not None
        assert retrieved_producto.id == producto_id
        assert retrieved_producto.nombre == sample_producto.nombre
        assert retrieved_producto.referencia == sample_producto.referencia
        assert retrieved_producto.precio == sample_producto.precio
    
    def test_producto_get_by_id_not_found(self, temp_db):
        """Test la récupération d'un produit inexistant"""
        retrieved_producto = Producto.get_by_id(99999)
        assert retrieved_producto is None
    
    def test_producto_unique_referencia(self, sample_producto_data, temp_db):
        """Test l'unicité de la référence"""
        # Créer deux produits avec la même référence
        producto1 = Producto(**sample_producto_data)
        producto2 = Producto(**sample_producto_data)
        
        # Le premier devrait se sauvegarder sans problème
        producto1.save()
        assert producto1.id is not None
        
        # Le second devrait lever une exception
        with pytest.raises(Exception):  # Violation de contrainte UNIQUE
            producto2.save()

class TestOrganizacion:
    """Tests pour le modèle Organizacion"""
    
    def test_organizacion_creation(self, sample_organizacion_data):
        """Test la création d'une organisation"""
        org = Organizacion(**sample_organizacion_data)
        
        assert org.nombre == sample_organizacion_data['nombre']
        assert org.direccion == sample_organizacion_data['direccion']
        assert org.telefono == sample_organizacion_data['telefono']
        assert org.email == sample_organizacion_data['email']
        assert org.cif == sample_organizacion_data['cif']
        assert org.logo_path == sample_organizacion_data['logo_path']
    
    def test_organizacion_creation_with_defaults(self):
        """Test la création d'une organisation avec valeurs par défaut"""
        org = Organizacion()
        
        assert org.nombre == ""
        assert org.direccion == ""
        assert org.telefono == ""
        assert org.email == ""
        assert org.cif == ""
        assert org.logo_path == ""
    
    def test_organizacion_save_new(self, sample_organizacion, temp_db):
        """Test la sauvegarde d'une nouvelle organisation"""
        sample_organizacion.save()
        
        # Vérifier qu'elle a été sauvegardée
        results = temp_db.execute_query("SELECT * FROM organizacion WHERE id = 1")
        assert len(results) == 1
        
        row = results[0]
        assert row[1] == sample_organizacion.nombre
        assert row[2] == sample_organizacion.direccion
        assert row[3] == sample_organizacion.telefono
        assert row[4] == sample_organizacion.email
        assert row[5] == sample_organizacion.cif
    
    def test_organizacion_save_update(self, sample_organizacion, temp_db):
        """Test la mise à jour d'une organisation existante"""
        # Sauvegarder d'abord
        sample_organizacion.save()
        
        # Modifier et sauvegarder à nouveau
        sample_organizacion.nombre = "Nouveau Nom"
        sample_organizacion.email = "nouveau@email.com"
        sample_organizacion.save()
        
        # Vérifier qu'il n'y a toujours qu'une seule organisation
        results = temp_db.execute_query("SELECT COUNT(*) FROM organizacion")
        assert results[0][0] == 1
        
        # Vérifier les modifications
        results = temp_db.execute_query("SELECT nombre, email FROM organizacion WHERE id = 1")
        assert results[0][0] == "Nouveau Nom"
        assert results[0][1] == "nouveau@email.com"
    
    def test_organizacion_get(self, sample_organizacion, temp_db):
        """Test la récupération des données d'organisation"""
        # Sauvegarder
        sample_organizacion.save()
        
        # Récupérer
        retrieved_org = Organizacion.get()
        
        assert retrieved_org is not None
        assert retrieved_org.nombre == sample_organizacion.nombre
        assert retrieved_org.direccion == sample_organizacion.direccion
        assert retrieved_org.telefono == sample_organizacion.telefono
        assert retrieved_org.email == sample_organizacion.email
        assert retrieved_org.cif == sample_organizacion.cif
    
    def test_organizacion_get_empty(self, temp_db):
        """Test la récupération quand aucune organisation n'existe"""
        retrieved_org = Organizacion.get()
        
        assert retrieved_org is not None
        assert retrieved_org.nombre == ""
        assert retrieved_org.direccion == ""
        assert retrieved_org.telefono == ""
        assert retrieved_org.email == ""
        assert retrieved_org.cif == ""

class TestStock:
    """Tests pour le modèle Stock"""
    
    def test_stock_creation(self):
        """Test la création d'un stock"""
        stock = Stock(producto_id=1, cantidad_disponible=50)
        
        assert stock.producto_id == 1
        assert stock.cantidad_disponible == 50
    
    def test_stock_creation_with_defaults(self):
        """Test la création d'un stock avec valeurs par défaut"""
        stock = Stock(producto_id=1)
        
        assert stock.producto_id == 1
        assert stock.cantidad_disponible == 0
    
    def test_stock_create_for_product(self, temp_db):
        """Test la création de stock pour un produit"""
        Stock.create_for_product(1)
        
        results = temp_db.execute_query("SELECT * FROM stock WHERE producto_id = 1")
        assert len(results) == 1
        assert results[0][1] == 0  # cantidad_disponible
    
    def test_stock_get_by_product(self, temp_db):
        """Test la récupération du stock d'un produit"""
        # Créer un stock
        temp_db.execute_query(
            "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, ?)",
            (1, 25)
        )
        
        cantidad = Stock.get_by_product(1)
        assert cantidad == 25
    
    def test_stock_get_by_product_not_found(self, temp_db):
        """Test la récupération du stock d'un produit inexistant"""
        cantidad = Stock.get_by_product(99999)
        assert cantidad == 0
    
    def test_stock_update_stock(self, temp_db):
        """Test la mise à jour du stock après vente"""
        # Créer un stock initial
        temp_db.execute_query(
            "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, ?)",
            (1, 100)
        )
        
        # Vendre 30 unités
        Stock.update_stock(1, 30)
        
        # Vérifier le nouveau stock
        cantidad = Stock.get_by_product(1)
        assert cantidad == 70
    
    def test_stock_update_stock_negative_prevention(self, temp_db):
        """Test que le stock ne peut pas devenir négatif"""
        # Créer un stock initial
        temp_db.execute_query(
            "INSERT INTO stock (producto_id, cantidad_disponible) VALUES (?, ?)",
            (1, 10)
        )
        
        # Essayer de vendre plus que disponible
        Stock.update_stock(1, 15)
        
        # Le stock devrait être à 0, pas négatif
        cantidad = Stock.get_by_product(1)
        assert cantidad == 0
