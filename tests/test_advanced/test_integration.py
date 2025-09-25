import pytest
import os
import sys
import tempfile
import sqlite3
from unittest.mock import patch, MagicMock

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Producto, Stock, Organizacion
from database.database import Database

class TestIntegrationWorkflows:
    """Tests d'intégration de workflows complets"""
    
    def test_complete_product_lifecycle(self, temp_db):
        """Test du cycle de vie complet d'un produit"""
        # 1. Créer un produit
        producto = Producto(
            nombre="Producto Lifecycle",
            referencia="LIFE-001",
            precio=25.50,
            categoria="Test",
            iva_recomendado=21.0,
            descripcion="Producto para test de lifecycle"
        )
        
        # 2. Sauvegarder le produit
        producto.save()
        assert producto.id is not None
        
        # 3. Vérifier que le stock a été créé automatiquement
        stock_inicial = Stock.get_by_product(producto.id)
        assert stock_inicial == 0
        
        # 4. Ajouter du stock
        temp_db.execute_query(
            "UPDATE stock SET cantidad_disponible = ? WHERE producto_id = ?",
            (100, producto.id)
        )
        
        stock_actual = Stock.get_by_product(producto.id)
        assert stock_actual == 100
        
        # 5. Simuler une vente (réduire le stock)
        Stock.update_stock(producto.id, 25)
        stock_despues_venta = Stock.get_by_product(producto.id)
        assert stock_despues_venta == 75
        
        # 6. Modifier le produit
        producto.precio = 30.00
        producto.descripcion = "Descripción actualizada"
        producto.save()
        
        # 7. Vérifier les modifications
        producto_recuperado = Producto.get_by_id(producto.id)
        assert producto_recuperado.precio == 30.00
        assert producto_recuperado.descripcion == "Descripción actualizada"
        
        # 8. Supprimer le produit
        producto.delete()
        
        # 9. Vérifier que le produit et son stock ont été supprimés
        producto_eliminado = Producto.get_by_id(producto.id)
        assert producto_eliminado is None
        
        stock_eliminado = Stock.get_by_product(producto.id)
        assert stock_eliminado == 0
    
    def test_organization_setup_workflow(self, temp_db):
        """Test du workflow de configuration d'organisation"""
        # 1. Vérifier qu'aucune organisation n'existe initialement
        org_inicial = Organizacion.get()
        assert org_inicial.nombre == ""
        
        # 2. Créer une nouvelle organisation
        nueva_org = Organizacion(
            nombre="Mi Empresa S.L.",
            direccion="Calle Principal 123, Madrid",
            telefono="+34 91 123 45 67",
            email="info@miempresa.es",
            cif="B12345678",
            logo_path="/path/to/logo.png"
        )
        
        # 3. Sauvegarder l'organisation
        nueva_org.save()
        
        # 4. Récupérer et vérifier
        org_guardada = Organizacion.get()
        assert org_guardada.nombre == "Mi Empresa S.L."
        assert org_guardada.direccion == "Calle Principal 123, Madrid"
        assert org_guardada.telefono == "+34 91 123 45 67"
        assert org_guardada.email == "info@miempresa.es"
        assert org_guardada.cif == "B12345678"
        
        # 5. Modifier l'organisation
        org_guardada.telefono = "+34 91 987 65 43"
        org_guardada.email = "contacto@miempresa.es"
        org_guardada.save()
        
        # 6. Vérifier les modifications
        org_modificada = Organizacion.get()
        assert org_modificada.telefono == "+34 91 987 65 43"
        assert org_modificada.email == "contacto@miempresa.es"
        assert org_modificada.nombre == "Mi Empresa S.L."  # Inchangé
    
    def test_inventory_management_workflow(self, temp_db):
        """Test du workflow de gestion d'inventaire"""
        # 1. Créer plusieurs produits
        productos = []
        for i in range(5):
            producto = Producto(
                nombre=f"Producto Inventario {i+1}",
                referencia=f"INV-{i+1:03d}",
                precio=float((i+1) * 10),
                categoria="Inventario"
            )
            producto.save()
            productos.append(producto)
        
        # 2. Ajouter du stock initial à tous les produits
        for i, producto in enumerate(productos):
            stock_inicial = (i + 1) * 50  # 50, 100, 150, 200, 250
            temp_db.execute_query(
                "UPDATE stock SET cantidad_disponible = ? WHERE producto_id = ?",
                (stock_inicial, producto.id)
            )
        
        # 3. Vérifier le stock total
        stock_data = Stock.get_all()
        assert len(stock_data) == 5
        
        total_stock = sum(row[1] for row in stock_data)  # cantidad_disponible
        assert total_stock == 750  # 50+100+150+200+250
        
        # 4. Simuler des ventes
        ventas = [
            (productos[0].id, 10),  # Vendre 10 du premier produit
            (productos[1].id, 25),  # Vendre 25 du deuxième
            (productos[2].id, 50),  # Vendre 50 du troisième
        ]
        
        for producto_id, cantidad_vendida in ventas:
            Stock.update_stock(producto_id, cantidad_vendida)
        
        # 5. Vérifier les stocks après ventes
        stocks_esperados = [40, 75, 100, 200, 250]  # Après les ventes
        for i, producto in enumerate(productos):
            stock_actual = Stock.get_by_product(producto.id)
            assert stock_actual == stocks_esperados[i]
        
        # 6. Vérifier qu'on ne peut pas avoir de stock négatif
        Stock.update_stock(productos[0].id, 100)  # Essayer de vendre plus que disponible
        stock_final = Stock.get_by_product(productos[0].id)
        assert stock_final == 0  # Devrait être 0, pas négatif
    
    def test_database_transaction_workflow(self, temp_db):
        """Test du workflow de transactions de base de données"""
        # 1. Créer un produit
        producto = Producto(
            nombre="Transaction Test",
            referencia="TRANS-001",
            precio=15.75
        )
        producto.save()
        
        # 2. Vérifier l'état initial
        productos_iniciales = Producto.get_all()
        assert len(productos_iniciales) == 1
        
        # 3. Simuler une transaction complexe (création de facture)
        try:
            # Créer plusieurs lignes de facture avec la nouvelle structure
            for i in range(3):
                cantidad = i + 1
                precio_unitario = producto.precio
                iva_aplicado = 21.0
                descuento = 0.0

                # Calcular totales
                subtotal = precio_unitario * cantidad
                descuento_amount = subtotal * (descuento / 100)
                subtotal_con_descuento = subtotal - descuento_amount
                iva_amount = subtotal_con_descuento * (iva_aplicado / 100)
                total = subtotal_con_descuento + iva_amount

                temp_db.execute_query(
                    "INSERT INTO factura_items (factura_id, producto_id, cantidad, precio_unitario, iva_aplicado, descuento, subtotal, descuento_amount, iva_amount, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (1, producto.id, cantidad, precio_unitario, iva_aplicado, descuento, subtotal_con_descuento, descuento_amount, iva_amount, total)
                )
            
            # Mettre à jour le stock
            Stock.update_stock(producto.id, 6)  # Total vendu: 1+2+3 = 6
            
            # Créer la facture principale
            temp_db.execute_query(
                "INSERT INTO facturas (numero_factura, fecha_factura, nombre_cliente, subtotal, total_iva, total_factura) VALUES (?, ?, ?, ?, ?, ?)",
                ("2024-0001", "2024-01-01", "Cliente Test", 94.50, 19.85, 114.35)
            )
            
        except Exception as e:
            pytest.fail(f"Transaction failed: {e}")
        
        # 4. Vérifier que tout a été créé correctement
        facturas = temp_db.execute_query("SELECT COUNT(*) FROM facturas")[0][0]
        assert facturas == 1
        
        items = temp_db.execute_query("SELECT COUNT(*) FROM factura_items")[0][0]
        assert items == 3
    
    def test_error_handling_workflow(self, temp_db):
        """Test du workflow de gestion d'erreurs"""
        # 1. Essayer de créer un produit avec référence dupliquée
        producto1 = Producto(
            nombre="Producto Original",
            referencia="DUP-001",
            precio=10.0
        )
        producto1.save()
        
        producto2 = Producto(
            nombre="Producto Duplicado",
            referencia="DUP-001",  # Même référence
            precio=20.0
        )
        
        # Cela devrait lever une exception
        with pytest.raises(Exception):
            producto2.save()
        
        # 2. Vérifier qu'un seul produit existe
        productos = Producto.get_all()
        assert len(productos) == 1
        assert productos[0].nombre == "Producto Original"
        
        # 3. Essayer de récupérer un produit inexistant
        producto_inexistant = Producto.get_by_id(99999)
        assert producto_inexistant is None
        
        # 4. Essayer de mettre à jour le stock d'un produit inexistant
        stock_inexistant = Stock.get_by_product(99999)
        assert stock_inexistant == 0
        
        # 5. Mettre à jour le stock sans erreur (produit inexistant)
        # Cette opération ne devrait pas lever d'exception même si le produit n'existe pas
        try:
            Stock.update_stock(99999, 10)
        except Exception:
            pass  # Acceptable si l'opération échoue pour un produit inexistant

        stock_apres = Stock.get_by_product(99999)
        assert stock_apres == 0

class TestSystemIntegration:
    """Tests d'intégration système"""
    
    def test_database_backup_restore_simulation(self, temp_db):
        """Simulation de sauvegarde et restauration de base de données"""
        # 1. Créer des données de test
        org = Organizacion(
            nombre="Empresa Test",
            direccion="Test Address",
            telefono="123456789",
            email="test@test.com",
            cif="A12345678"
        )
        org.save()
        
        productos_originales = []
        for i in range(3):
            producto = Producto(
                nombre=f"Backup Product {i}",
                referencia=f"BACKUP-{i:03d}",
                precio=float(i + 1) * 10
            )
            producto.save()
            productos_originales.append(producto)
        
        # 2. "Sauvegarder" les données (les lire)
        backup_org = Organizacion.get()
        backup_productos = Producto.get_all()
        
        assert backup_org.nombre == "Empresa Test"
        assert len(backup_productos) == 3
        
        # 3. Simuler une perte de données (supprimer tout)
        for producto in productos_originales:
            producto.delete()
        
        # 4. Vérifier que les données ont été supprimées
        productos_despues_perdida = Producto.get_all()
        assert len(productos_despues_perdida) == 0
        
        # 5. "Restaurer" les données
        for producto_backup in backup_productos:
            producto_restaurado = Producto(
                nombre=producto_backup.nombre,
                referencia=producto_backup.referencia,
                precio=producto_backup.precio,
                categoria=producto_backup.categoria,
                descripcion=producto_backup.descripcion,
                iva_recomendado=producto_backup.iva_recomendado
            )
            producto_restaurado.save()
        
        # 6. Vérifier la restauration
        productos_restaurados = Producto.get_all()
        assert len(productos_restaurados) == 3
        
        for original, restaurado in zip(backup_productos, productos_restaurados):
            assert original.nombre == restaurado.nombre
            assert original.referencia == restaurado.referencia
            assert original.precio == restaurado.precio
    
    @pytest.mark.slow
    def test_stress_test_simulation(self, temp_db):
        """Simulation de test de stress"""
        import time
        
        start_time = time.time()
        
        # 1. Créer beaucoup de produits rapidement
        productos_creados = []
        for i in range(100):
            producto = Producto(
                nombre=f"Stress Product {i}",
                referencia=f"STRESS-{i:04d}",
                precio=float(i + 1)
            )
            producto.save()
            productos_creados.append(producto.id)
        
        creation_time = time.time() - start_time
        
        # 2. Effectuer beaucoup de lectures
        read_start = time.time()
        for _ in range(50):
            all_products = Producto.get_all()
            assert len(all_products) == 100
        
        read_time = time.time() - read_start
        
        # 3. Effectuer beaucoup de mises à jour
        update_start = time.time()
        for producto_id in productos_creados[:50]:  # Mettre à jour la moitié
            producto = Producto.get_by_id(producto_id)
            producto.precio = producto.precio * 1.1  # Augmenter de 10%
            producto.save()
        
        update_time = time.time() - update_start
        
        # 4. Vérifications de performance
        assert creation_time < 10.0  # Moins de 10 secondes pour créer 100 produits
        assert read_time < 5.0       # Moins de 5 secondes pour 50 lectures
        assert update_time < 10.0    # Moins de 10 secondes pour 50 mises à jour
        
        total_time = time.time() - start_time
        assert total_time < 30.0     # Moins de 30 secondes au total
        
        # 5. Vérifier l'intégrité des données
        final_products = Producto.get_all()
        assert len(final_products) == 100
        
        # Vérifier que les prix ont été mis à jour
        updated_products = [p for p in final_products if p.precio != float(p.id)]
        assert len(updated_products) >= 50
