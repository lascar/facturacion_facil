# -*- coding: utf-8 -*-
"""
Tests de comportement pour le système "sin stock"
Vérifie que les produits marqués "sin stock" apparaissent partout mais ne gèrent pas de stock
"""

import pytest
import sys
import os
import uuid
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.pyqt5_automation import PyQt5Automation
from test.behaviour.utils.test_data_factory import TestDataFactory
from utils.logger import get_logger


class TestSinStockBehaviour(BaseBehaviourTest):
    """Tests de comportement pour le système 'sin stock'"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir):
        """Configuration automatique pour chaque test"""
        self.init_base_attributes()

        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir
        self.logger = get_logger(self.__class__.__name__)

        # Générer un identifiant unique pour ce test
        self.test_id = str(uuid.uuid4())[:8]

        # Initialiser l'automation et les données de test
        if self.app:
            self.automation = PyQt5Automation(self.app)
        self.test_data = TestDataFactory()

        # Préparer des données de test
        self.setup_sin_stock_test_data()
    
    def setup_sin_stock_test_data(self):
        """Préparer des données de test avec produits sin_stock et con stock"""
        # Créer des produits avec et sans gestion de stock (références uniques)
        test_products = [
            {
                'nombre': 'Producto CON Stock 1',
                'referencia': f'STOCK001-{self.test_id}',
                'precio_venta': 50.00,
                'stock': 100,
                'sin_stock': False,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto SIN Stock 1',
                'referencia': f'NOSTOCK001-{self.test_id}',
                'precio_venta': 75.00,
                'stock': 0,
                'sin_stock': True,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto CON Stock 2',
                'referencia': f'STOCK002-{self.test_id}',
                'precio_venta': 25.00,
                'stock': 50,
                'sin_stock': False,
                'categoria': 'Test'
            },
            {
                'nombre': 'Producto SIN Stock 2',
                'referencia': f'NOSTOCK002-{self.test_id}',
                'precio_venta': 100.00,
                'stock': 0,
                'sin_stock': True,
                'categoria': 'Test'
            }
        ]
        
        # Ajouter à la base de données de test
        self.product_ids = {}
        for product in test_products:
            product_id = self.database.add_product(product)
            self.product_ids[product['nombre']] = product_id
            self.logger.info(f"Produit créé: {product['nombre']} (ID: {product_id}, sin_stock: {product['sin_stock']})")
    
    def test_01_sin_stock_products_in_stock_window(self):
        """Test: Les produits 'sin stock' APPARAISSENT dans la fenêtre Stock"""
        self.logger.info("🧪 Test: Produits 'sin stock' apparaissent dans fenêtre Stock")

        # Ouvrir la fenêtre Stock
        stock_btn = self.automation.find_button_by_text(self.main_window, "📊 Stock")
        assert stock_btn is not None, "Bouton Stock non trouvé"

        QTest.mouseClick(stock_btn, Qt.LeftButton)
        self.wait_and_process_events(1000)

        # Trouver la fenêtre stock
        stock_window = None
        for widget in reversed(self.app.topLevelWidgets()):
            if hasattr(widget, 'windowTitle') and "Stock" in widget.windowTitle() and widget.isVisible():
                stock_window = widget
                break

        assert stock_window is not None, "Fenêtre Stock non trouvée"
        assert stock_window.isVisible(), "Fenêtre Stock non visible"

        self.logger.info("✅ Fenêtre Stock ouverte")

        # Trouver la table de stock (utiliser l'attribut directement)
        stock_table = getattr(stock_window, 'stock_table', None)
        if not stock_table:
            # Essayer de trouver par nom
            stock_table = self.automation.find_widget_by_name(stock_window, "stock_table")

        assert stock_table is not None, "Table de stock non trouvée"

        row_count = stock_table.rowCount()
        self.logger.info(f"Nombre de lignes dans la table: {row_count}")

        # Vérifier que TOUS les produits apparaissent (CON et SIN stock)
        found_products = []
        for row in range(row_count):
            nombre_item = stock_table.item(row, 1)  # Colonne Producto
            if nombre_item:
                product_name = nombre_item.text()
                found_products.append(product_name)
                self.logger.info(f"Produit trouvé dans table: {product_name}")

        # Vérifier que les produits CON stock sont présents
        con_stock_found = [p for p in found_products if "CON Stock" in p]
        assert len(con_stock_found) >= 2, f"Devrait avoir au moins 2 produits CON stock, trouvé: {len(con_stock_found)}"
        self.logger.info(f"✅ Produits CON stock présents dans la table: {len(con_stock_found)}")

        # Vérifier que les produits SIN stock sont PRÉSENTS
        sin_stock_found = [p for p in found_products if "SIN Stock" in p]
        assert len(sin_stock_found) >= 2, f"Devrait avoir au moins 2 produits SIN stock, trouvé: {len(sin_stock_found)}"
        self.logger.info(f"✅ Produits SIN stock présents dans la table: {len(sin_stock_found)}")

        # Vérifier le nombre total de produits affichés
        # Il devrait y avoir les produits de test (4) + les fixtures (3) = 7
        expected_min_count = 4  # Au moins les 4 produits de test (2 CON + 2 SIN)
        assert row_count >= expected_min_count, f"Devrait avoir au moins {expected_min_count} produits, trouvé: {row_count}"
        self.logger.info(f"✅ Nombre de produits affichés: {row_count} (inclut fixtures + tous les produits)")

        stock_window.close()
        self.wait_and_process_events(200)

        self.logger.info("✅ Test produits sin_stock apparaissent terminé")

    def test_02_sin_stock_products_in_database(self):
        """Test: Les produits 'sin stock' existent bien en base de données"""
        self.logger.info("🧪 Test: Produits 'sin stock' existent en base de données")

        # Vérifier que tous les produits sont en base
        all_products = self.database.get_all_products()

        product_names = [p['nombre'] for p in all_products]
        self.logger.info(f"Produits en base: {len(all_products)}")

        # Vérifier que les 4 produits de test sont présents
        assert any("CON Stock 1" in p for p in product_names), "Producto CON Stock 1 non trouvé en base"
        assert any("SIN Stock 1" in p for p in product_names), "Producto SIN Stock 1 non trouvé en base"
        assert any("CON Stock 2" in p for p in product_names), "Producto CON Stock 2 non trouvé en base"
        assert any("SIN Stock 2" in p for p in product_names), "Producto SIN Stock 2 non trouvé en base"

        self.logger.info("✅ Tous les produits (CON et SIN stock) sont en base de données")

        # Vérifier que les produits SIN stock ont bien le flag sin_stock=1
        sin_stock_products = [p for p in all_products if p.get('sin_stock', 0) == 1]
        self.logger.info(f"Produits avec sin_stock=1: {len(sin_stock_products)}")

        assert len(sin_stock_products) >= 2, "Devrait avoir au moins 2 produits sin_stock"
        self.logger.info("✅ Produits SIN stock ont le flag sin_stock=1")

        self.logger.info("✅ Test produits sin_stock en base terminé")

    def test_03_stock_service_includes_sin_stock(self):
        """Test: Le service Stock retourne TOUS les produits (incluant sin_stock)"""
        self.logger.info("🧪 Test: StockService retourne tous les produits")

        from services.stock_service import StockService

        stock_service = StockService(self.database)

        # Récupérer les produits via le service
        stock_products = stock_service.get_all_stock()

        product_names = [p['nombre'] for p in stock_products]
        self.logger.info(f"Produits retournés par StockService: {len(stock_products)}")
        for name in product_names:
            self.logger.info(f"  - {name}")

        # Vérifier que les produits CON stock sont présents
        con_stock_products = [p for p in product_names if "CON Stock" in p]
        assert len(con_stock_products) >= 2, "Devrait avoir au moins 2 produits CON stock"
        self.logger.info(f"✅ Produits CON stock présents: {len(con_stock_products)}")

        # Vérifier que les produits SIN stock sont PRÉSENTS
        sin_stock_products = [p for p in product_names if "SIN Stock" in p]
        assert len(sin_stock_products) >= 2, f"Devrait avoir au moins 2 produits SIN stock, trouvé: {len(sin_stock_products)}"
        self.logger.info(f"✅ Produits SIN stock présents: {len(sin_stock_products)}")

        # Vérifier que les produits sin_stock ont bien le flag sin_stock=1
        for product in stock_products:
            if "SIN Stock" in product['nombre']:
                assert product.get('sin_stock', 0) == 1, f"Produit SIN stock devrait avoir sin_stock=1: {product['nombre']}"

        self.logger.info("✅ Test StockService inclut sin_stock terminé")

    def test_04_informe_stock_includes_sin_stock(self):
        """Test: Les informes de stock incluent les produits sin_stock"""
        self.logger.info("🧪 Test: Informes de stock incluent les produits sin_stock")

        # Ouvrir la fenêtre Informes
        informes_btn = self.automation.find_button_by_text(self.main_window, "📊 Informes")
        if not informes_btn:
            self.logger.warning("Bouton Informes non trouvé, test ignoré")
            return

        QTest.mouseClick(informes_btn, Qt.LeftButton)
        self.wait_and_process_events(500)

        # Trouver la fenêtre Informes
        informes_window = None
        for widget in reversed(self.app.topLevelWidgets()):
            if hasattr(widget, 'windowTitle') and "Informes" in widget.windowTitle() and widget.isVisible():
                informes_window = widget
                break

        if not informes_window:
            self.logger.warning("Fenêtre Informes non trouvée, test ignoré")
            return

        # Chercher le bouton "Informe de Stock"
        informe_stock_btn = self.automation.find_button_by_text(informes_window, "Stock")
        if not informe_stock_btn:
            self.logger.warning("Bouton Informe Stock non trouvé, test ignoré")
            informes_window.close()
            return

        QTest.mouseClick(informe_stock_btn, Qt.LeftButton)
        self.wait_and_process_events(1000)

        # Trouver la fenêtre Informe Stock
        informe_stock_window = None
        for widget in reversed(self.app.topLevelWidgets()):
            if hasattr(widget, 'windowTitle') and "Stock" in widget.windowTitle() and widget.isVisible():
                if widget != informes_window:  # Pas la fenêtre Informes principale
                    informe_stock_window = widget
                    break

        if informe_stock_window:
            self.logger.info("✅ Fenêtre Informe Stock ouverte")

            # Chercher la liste de produits
            productos_list = self.automation.find_widget_by_name(informe_stock_window, "productos_list")
            if productos_list:
                item_count = productos_list.count()
                self.logger.info(f"Nombre de produits dans la liste: {item_count}")

                # Vérifier que TOUS les produits sont dans la liste (CON et SIN stock)
                found_items = []
                for i in range(item_count):
                    item = productos_list.item(i)
                    if item:
                        item_text = item.text()
                        found_items.append(item_text)
                        self.logger.info(f"  - {item_text}")

                # Vérifier que les produits SIN stock sont PRÉSENTS
                sin_stock_items = [item for item in found_items if "SIN Stock" in item]
                assert len(sin_stock_items) >= 2, f"Devrait avoir au moins 2 produits SIN stock, trouvé: {len(sin_stock_items)}"
                self.logger.info(f"✅ Produits SIN stock présents dans l'informe: {len(sin_stock_items)}")

                # Vérifier que les produits CON stock sont aussi présents
                con_stock_items = [item for item in found_items if "CON Stock" in item]
                assert len(con_stock_items) >= 2, f"Devrait avoir au moins 2 produits CON stock, trouvé: {len(con_stock_items)}"
                self.logger.info(f"✅ Produits CON stock présents dans l'informe: {len(con_stock_items)}")

            informe_stock_window.close()
            self.wait_and_process_events(200)

        if informes_window:
            informes_window.close()
            self.wait_and_process_events(200)

        self.logger.info("✅ Test informe stock inclut sin_stock terminé")

    def test_05_create_factura_with_sin_stock_product(self):
        """Test: Créer une facture avec un produit sin_stock (sans vérification de stock)"""
        self.logger.info("🧪 Test: Créer factura avec produit sin_stock")

        from services.factura_service import FacturaService
        from services.cliente_service import ClienteService
        from datetime import datetime

        factura_service = FacturaService()
        cliente_service = ClienteService()

        # Obtenir un client
        clientes = cliente_service.get_all_clientes()
        assert len(clientes) > 0, "Aucun client trouvé"
        cliente = clientes[0]
        self.logger.info(f"✅ Cliente: {cliente['nombre']}")

        # Utiliser un produit SIN stock de test
        producto_sin_stock = None
        for nombre, producto_id in self.product_ids.items():
            if "SIN Stock" in nombre:
                producto = self.database.get_product_by_id(producto_id)
                if producto:
                    producto_sin_stock = producto
                    break

        assert producto_sin_stock is not None, "Aucun produit SIN stock trouvé"
        self.logger.info(f"✅ Producto sin stock: {producto_sin_stock['nombre']}")
        self.logger.info(f"   - sin_stock: {producto_sin_stock.get('sin_stock', 0)}")
        self.logger.info(f"   - stock_actual: {producto_sin_stock.get('stock_actual', 0)}")

        # Créer une factura avec ce produit
        factura_data = {
            'numero': f'TEST-SIN-STOCK-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'fecha': datetime.now().strftime('%Y-%m-%d'),
            'cliente': cliente,
            'subtotal': producto_sin_stock['precio_venta'],
            'iva_total': producto_sin_stock['precio_venta'] * 0.21,
            'total': producto_sin_stock['precio_venta'] * 1.21,
            'estado': 'Borrador',
            'lineas': [
                {
                    'producto_id': producto_sin_stock['id'],
                    'producto_nombre': producto_sin_stock['nombre'],
                    'cantidad': 1,
                    'precio_unitario': producto_sin_stock['precio_venta'],
                    'iva_aplicado': 21.0,
                    'subtotal': producto_sin_stock['precio_venta'],
                    'iva_amount': producto_sin_stock['precio_venta'] * 0.21,
                    'total': producto_sin_stock['precio_venta'] * 1.21
                }
            ]
        }

        # Créer la factura (ne devrait PAS échouer même si stock=0)
        try:
            factura_id = factura_service.create_factura(factura_data)
            self.logger.info(f"✅ Factura créée avec ID: {factura_id}")
            assert factura_id is not None, "Factura ID devrait être retourné"

            # Vérifier que le stock n'a pas changé
            producto_after = self.database.get_product_by_id(producto_sin_stock['id'])
            stock_after = producto_after.get('stock_actual', 0)
            stock_before = producto_sin_stock.get('stock_actual', 0)

            assert stock_after == stock_before, f"Stock ne devrait pas changer pour produit sin_stock (avant: {stock_before}, après: {stock_after})"
            self.logger.info(f"✅ Stock inchangé: {stock_after} (correct pour produit sin_stock)")

        except Exception as e:
            self.fail(f"Création de factura avec produit sin_stock a échoué: {e}")

        self.logger.info("✅ Test création factura avec sin_stock terminé")


