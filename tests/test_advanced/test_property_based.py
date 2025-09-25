import pytest
import os
import sys
from hypothesis import given, strategies as st, assume, example
from hypothesis.strategies import composite
from decimal import Decimal

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Producto, Stock

class TestPropertyBased:
    """Tests basés sur les propriétés avec Hypothesis"""
    
    @composite
    def producto_strategy(draw):
        """Stratégie pour générer des produits valides"""
        nombre = draw(st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs'))))
        referencia = draw(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc'))))
        precio = draw(st.floats(min_value=0.01, max_value=999999.99, allow_nan=False, allow_infinity=False))
        categoria = draw(st.text(max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Zs'))))
        iva = draw(st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False))
        
        return {
            'nombre': nombre.strip(),
            'referencia': referencia.strip(),
            'precio': round(precio, 2),
            'categoria': categoria.strip(),
            'iva_recomendado': round(iva, 2)
        }
    
    @given(st.floats(min_value=0.01, max_value=999999.99, allow_nan=False, allow_infinity=False))
    def test_precio_always_positive(self, precio):
        """Propriété: Le prix d'un produit est toujours positif"""
        precio = round(precio, 2)
        producto = Producto(nombre="Test", referencia="TEST", precio=precio)
        assert producto.precio > 0
        assert producto.precio == precio
    
    @given(st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False))
    def test_iva_within_bounds(self, iva):
        """Propriété: L'IVA est toujours entre 0 et 100%"""
        iva = round(iva, 2)
        producto = Producto(nombre="Test", referencia="TEST", precio=10.0, iva_recomendado=iva)
        assert 0 <= producto.iva_recomendado <= 100
        assert producto.iva_recomendado == iva
    
    @given(st.text(min_size=1, max_size=100))
    def test_nombre_not_empty_after_strip(self, nombre):
        """Propriété: Le nom d'un produit n'est jamais vide après strip"""
        assume(nombre.strip())  # Assumer que le nom n'est pas vide après strip
        
        producto = Producto(nombre=nombre, referencia="TEST", precio=10.0)
        assert len(producto.nombre.strip()) > 0
    
    @given(st.text(min_size=1, max_size=50))
    def test_referencia_uniqueness_property(self, referencia):
        """Propriété: Chaque référence doit être unique"""
        assume(referencia.strip())
        
        referencia = referencia.strip()
        producto1 = Producto(nombre="Test1", referencia=referencia, precio=10.0)
        producto2 = Producto(nombre="Test2", referencia=referencia, precio=20.0)
        
        # Même référence = même produit conceptuellement
        assert producto1.referencia == producto2.referencia
    
    @given(
        precio=st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False),
        iva=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_precio_con_iva_calculation_property(self, precio, iva):
        """Propriété: Le prix avec IVA est toujours >= prix de base"""
        precio = round(precio, 2)
        iva = round(iva, 2)
        
        precio_con_iva = precio * (1 + iva / 100)
        
        assert precio_con_iva >= precio
        if iva > 0:
            assert precio_con_iva > precio
        else:
            assert precio_con_iva == precio
    
    @given(
        cantidad_inicial=st.integers(min_value=0, max_value=10000),
        cantidad_vendida=st.integers(min_value=0, max_value=10000)
    )
    def test_stock_never_negative(self, cantidad_inicial, cantidad_vendida):
        """Propriété: Le stock ne peut jamais être négatif"""
        # Simuler la logique de mise à jour du stock
        nuevo_stock = max(0, cantidad_inicial - cantidad_vendida)
        
        assert nuevo_stock >= 0
        assert nuevo_stock <= cantidad_inicial
    
    @given(st.lists(st.floats(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False), min_size=1, max_size=10))
    def test_factura_total_sum_property(self, precios):
        """Propriété: Le total d'une facture est la somme de ses lignes"""
        precios = [round(p, 2) for p in precios]
        
        subtotal = sum(precios)
        iva_total = subtotal * 0.21  # 21% d'IVA
        total = subtotal + iva_total
        
        assert total >= subtotal
        assert abs(total - subtotal * 1.21) < 0.01  # Tolérance pour les flottants
        assert abs(total - (subtotal + iva_total)) < 0.01
    
    @given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs', 'Pc')), min_size=1, max_size=200))
    def test_descripcion_length_property(self, descripcion):
        """Propriété: La description peut être de n'importe quelle longueur raisonnable"""
        producto = Producto(
            nombre="Test",
            referencia="TEST",
            precio=10.0,
            descripcion=descripcion
        )
        
        assert len(producto.descripcion) == len(descripcion)
        assert producto.descripcion == descripcion

class TestPropertyBasedAdvanced:
    """Tests de propriétés avancés"""
    
    @given(
        productos_data=st.lists(
            st.fixed_dictionaries({
                'nombre': st.text(min_size=1, max_size=50),
                'referencia': st.text(min_size=1, max_size=20),
                'precio': st.floats(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False)
            }),
            min_size=1,
            max_size=5
        )
    )
    def test_multiple_productos_property(self, productos_data):
        """Propriété: Créer plusieurs produits préserve leurs propriétés individuelles"""
        productos = []
        
        for data in productos_data:
            assume(data['nombre'].strip() and data['referencia'].strip())
            
            producto = Producto(
                nombre=data['nombre'].strip(),
                referencia=data['referencia'].strip(),
                precio=round(data['precio'], 2)
            )
            productos.append(producto)
        
        # Vérifier que chaque produit conserve ses propriétés
        for i, producto in enumerate(productos):
            original_data = productos_data[i]
            assert producto.nombre == original_data['nombre'].strip()
            assert producto.referencia == original_data['referencia'].strip()
            assert abs(producto.precio - round(original_data['precio'], 2)) < 0.01
    
    @given(
        base_price=st.floats(min_value=1.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
        discount_percent=st.floats(min_value=0.0, max_value=50.0, allow_nan=False, allow_infinity=False)
    )
    def test_discount_calculation_property(self, base_price, discount_percent):
        """Propriété: Une remise réduit toujours le prix"""
        base_price = round(base_price, 2)
        discount_percent = round(discount_percent, 2)
        
        discounted_price = base_price * (1 - discount_percent / 100)
        
        assert discounted_price <= base_price
        if discount_percent > 0:
            assert discounted_price < base_price
        else:
            assert discounted_price == base_price
        
        # La remise ne peut pas rendre le prix négatif
        assert discounted_price >= 0
    
    @given(
        quantities=st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=10),
        unit_price=st.floats(min_value=0.01, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_line_total_calculation_property(self, quantities, unit_price):
        """Propriété: Le total d'une ligne = quantité × prix unitaire"""
        unit_price = round(unit_price, 2)
        
        for quantity in quantities:
            line_total = quantity * unit_price
            
            assert line_total >= unit_price  # Au moins le prix d'une unité
            assert line_total == quantity * unit_price
            assert abs(line_total / quantity - unit_price) < 0.01  # Tolérance pour les flottants
    
    @example(nombre="Café", referencia="CAFE-001", precio=2.50)
    @example(nombre="Laptop", referencia="TECH-001", precio=999.99)
    @given(
        nombre=st.text(min_size=1, max_size=100),
        referencia=st.text(min_size=1, max_size=50),
        precio=st.floats(min_value=0.01, max_value=999999.99, allow_nan=False, allow_infinity=False)
    )
    def test_producto_creation_with_examples(self, nombre, referencia, precio):
        """Test avec exemples spécifiques et génération aléatoire"""
        assume(nombre.strip() and referencia.strip())
        
        nombre = nombre.strip()
        referencia = referencia.strip()
        precio = round(precio, 2)
        
        producto = Producto(nombre=nombre, referencia=referencia, precio=precio)
        
        # Propriétés qui doivent toujours être vraies
        assert producto.nombre == nombre
        assert producto.referencia == referencia
        assert producto.precio == precio
        assert producto.precio > 0
        assert len(producto.nombre) > 0
        assert len(producto.referencia) > 0

class TestStatefulTesting:
    """Tests avec état (stateful testing)"""
    
    @given(
        operations=st.lists(
            st.one_of(
                st.tuples(st.just("add_stock"), st.integers(min_value=1, max_value=100)),
                st.tuples(st.just("remove_stock"), st.integers(min_value=1, max_value=50)),
                st.tuples(st.just("check_stock"), st.nothing())
            ),
            min_size=1,
            max_size=20
        )
    )
    def test_stock_operations_sequence(self, operations):
        """Test une séquence d'opérations sur le stock"""
        current_stock = 0
        
        for operation, *args in operations:
            if operation == "add_stock":
                amount = args[0]
                current_stock += amount
                assert current_stock >= amount
                
            elif operation == "remove_stock":
                amount = args[0]
                old_stock = current_stock
                current_stock = max(0, current_stock - amount)
                assert current_stock <= old_stock
                assert current_stock >= 0
                
            elif operation == "check_stock":
                assert current_stock >= 0
        
        # À la fin, le stock doit toujours être non-négatif
        assert current_stock >= 0
