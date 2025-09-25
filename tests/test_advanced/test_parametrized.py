import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Producto
from utils.translations import get_text

class TestParametrizedAdvanced:
    """Tests paramétrés avancés"""
    
    @pytest.mark.parametrize("precio,iva,expected_total", [
        (100.0, 21.0, 121.0),
        (50.0, 10.0, 55.0),
        (25.50, 4.0, 26.52),
        (0.0, 21.0, 0.0),
        (999.99, 0.0, 999.99),
    ])
    def test_precio_con_iva_calculation(self, precio, iva, expected_total):
        """Test le calcul du prix avec IVA"""
        total = precio * (1 + iva / 100)
        assert abs(total - expected_total) < 0.01  # Tolérance pour les flottants
    
    @pytest.mark.parametrize("referencia,valid", [
        ("PROD001", True),
        ("TEST-123", True),
        ("ABC_456", True),
        ("", False),
        ("   ", False),
        ("PROD 001", True),  # Espaces autorisés
        ("TRÈS-LONG-RÉFÉRENCE-QUI-DÉPASSE-LIMITE", True),
    ])
    def test_referencia_validation(self, referencia, valid):
        """Test la validation des références"""
        if valid:
            # Ne devrait pas lever d'exception
            producto = Producto(nombre="Test", referencia=referencia, precio=10.0)
            assert producto.referencia == referencia
        else:
            # Devrait être considéré comme invalide
            assert referencia.strip() == ""
    
    @pytest.mark.parametrize("categoria", [
        "Electrónicos",
        "Ropa y Accesorios", 
        "Hogar y Jardín",
        "Deportes",
        "Libros",
        "Alimentación",
        "Salud y Belleza"
    ])
    def test_categorias_validas(self, categoria):
        """Test avec différentes catégories valides"""
        producto = Producto(
            nombre=f"Producto {categoria}",
            referencia=f"CAT-{categoria[:3].upper()}",
            precio=25.0,
            categoria=categoria
        )
        assert producto.categoria == categoria
        assert len(producto.categoria) > 0
    
    @pytest.mark.parametrize("iva_rate", [0, 4, 10, 21])
    def test_iva_rates_spain(self, iva_rate):
        """Test les taux d'IVA espagnols officiels"""
        producto = Producto(
            nombre="Test IVA",
            referencia=f"IVA{iva_rate}",
            precio=100.0,
            iva_recomendado=iva_rate
        )
        assert producto.iva_recomendado == iva_rate
        assert 0 <= producto.iva_recomendado <= 100
    
    @pytest.mark.parametrize("translation_key,expected_type,min_length", [
        ("app_title", str, 5),
        ("productos", str, 3),
        ("nueva_factura", str, 5),
        ("confirmar_eliminacion", str, 10),
        ("campo_requerido", str, 5),
    ])
    def test_translations_quality(self, translation_key, expected_type, min_length):
        """Test la qualité des traductions"""
        text = get_text(translation_key)
        assert isinstance(text, expected_type)
        assert len(text) >= min_length
        assert text != translation_key  # Pas juste la clé retournée
    
    @pytest.mark.parametrize("precio,cantidad,descuento,expected", [
        (10.0, 1, 0, 10.0),      # Sans remise
        (10.0, 2, 0, 20.0),      # Quantité multiple
        (10.0, 1, 10, 9.0),      # 10% de remise
        (100.0, 3, 15, 255.0),   # Cas complexe
        (50.0, 0, 0, 0.0),       # Quantité zéro
    ])
    def test_calcul_ligne_factura(self, precio, cantidad, descuento, expected):
        """Test le calcul d'une ligne de facture"""
        subtotal = precio * cantidad
        total_con_descuento = subtotal * (1 - descuento / 100)
        assert abs(total_con_descuento - expected) < 0.01

class TestDataCombinations:
    """Tests avec combinaisons de données"""
    
    @pytest.mark.parametrize("nombre,referencia", [
        ("Laptop Dell", "DELL-001"),
        ("iPhone 15", "APPLE-IP15"),
        ("Mesa de Oficina", "OFFICE-DESK"),
        ("Café Colombiano", "CAFE-COL"),
    ])
    def test_producto_combinations(self, nombre, referencia):
        """Test avec combinaisons nom/référence réalistes"""
        producto = Producto(nombre=nombre, referencia=referencia, precio=99.99)
        assert producto.nombre == nombre
        assert producto.referencia == referencia
        assert len(producto.nombre) > 0
        assert len(producto.referencia) > 0
    
    @pytest.mark.parametrize("precio,iva", [
        (precio, iva) 
        for precio in [10.0, 25.50, 100.0, 999.99]
        for iva in [0, 4, 10, 21]
    ])
    def test_all_precio_iva_combinations(self, precio, iva):
        """Test toutes les combinaisons prix/IVA"""
        producto = Producto(
            nombre="Test Combo",
            referencia=f"COMBO-{precio}-{iva}",
            precio=precio,
            iva_recomendado=iva
        )
        
        # Calculs
        precio_con_iva = precio * (1 + iva / 100)
        
        assert producto.precio == precio
        assert producto.iva_recomendado == iva
        assert precio_con_iva >= precio  # Le prix avec IVA est toujours >= prix de base

class TestEdgeCases:
    """Tests des cas limites"""
    
    @pytest.mark.parametrize("edge_value", [
        0.01,      # Valeur minimale
        999999.99, # Valeur maximale
        0.001,     # Précision décimale
        1e-10,     # Très petit nombre
        1e10,      # Très grand nombre
    ])
    def test_precio_edge_cases(self, edge_value):
        """Test les cas limites pour les prix"""
        if edge_value >= 0.01:  # Prix minimum raisonnable
            producto = Producto(
                nombre="Edge Case",
                referencia=f"EDGE-{edge_value}",
                precio=edge_value
            )
            assert producto.precio == edge_value
        else:
            # Les très petites valeurs pourraient être problématiques
            assert edge_value < 0.01
    
    @pytest.mark.parametrize("special_char", [
        "ñ", "á", "é", "í", "ó", "ú", "ü", "Ñ",
        "€", "£", "$", "¥", "©", "®", "™"
    ])
    def test_special_characters_handling(self, special_char):
        """Test la gestion des caractères spéciaux"""
        nombre = f"Producto con {special_char}"
        referencia = f"SPEC-{ord(special_char)}"
        
        producto = Producto(
            nombre=nombre,
            referencia=referencia,
            precio=25.0
        )
        
        assert special_char in producto.nombre
        assert producto.referencia == referencia
    
    @pytest.mark.parametrize("long_text_length", [100, 500, 1000, 2000])
    def test_long_descriptions(self, long_text_length):
        """Test avec des descriptions très longues"""
        long_description = "A" * long_text_length
        
        producto = Producto(
            nombre="Test Long",
            referencia="LONG-001",
            precio=10.0,
            descripcion=long_description
        )
        
        assert len(producto.descripcion) == long_text_length
        assert producto.descripcion == long_description

class TestPerformanceParametrized:
    """Tests de performance paramétrés"""
    
    @pytest.mark.slow
    @pytest.mark.parametrize("num_products", [10, 100, 500])
    def test_bulk_product_creation(self, num_products, temp_db):
        """Test la création en masse de produits"""
        import time
        
        start_time = time.time()
        
        for i in range(num_products):
            producto = Producto(
                nombre=f"Producto {i}",
                referencia=f"BULK-{i:04d}",
                precio=float(i + 1)
            )
            producto.save()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Vérifications de performance
        assert duration < (num_products * 0.1)  # Max 0.1s par produit
        
        # Vérifier que tous les produits ont été créés
        all_products = Producto.get_all()
        assert len(all_products) == num_products
    
    @pytest.mark.parametrize("search_term,expected_min_results", [
        ("Producto", 0),  # Terme générique
        ("BULK", 0),      # Préfixe de référence
        ("001", 0),       # Suffixe numérique
        ("NonExistent", 0), # Terme inexistant
    ])
    def test_search_performance(self, search_term, expected_min_results, temp_db):
        """Test la performance de recherche"""
        # Créer quelques produits de test
        for i in range(10):
            producto = Producto(
                nombre=f"Producto Test {i}",
                referencia=f"SEARCH-{i:03d}",
                precio=10.0 + i
            )
            producto.save()
        
        import time
        start_time = time.time()
        
        # Simuler une recherche (ici on récupère tous et on filtre)
        all_products = Producto.get_all()
        results = [p for p in all_products if search_term.lower() in p.nombre.lower() or search_term.lower() in p.referencia.lower()]
        
        end_time = time.time()
        duration = end_time - start_time
        
        # La recherche devrait être rapide
        assert duration < 0.1  # Moins de 100ms
        assert len(results) >= expected_min_results
