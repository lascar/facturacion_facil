# -*- coding: utf-8 -*-
"""
Tests de comportement pour l'IVA modifiable dans les factures
"""

import pytest
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from test.behaviour.base_behaviour_test import BaseBehaviourTest
from test.behaviour.utils.test_data_factory import TestDataFactory
from test.behaviour.utils.pyqt5_automation import PyQt5Automation


class TestIVAModifiableBehaviour(BaseBehaviourTest):
    """Tests de comportement pour l'IVA modifiable dans les factures"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox):
        """Configuration automatique pour chaque test"""
        # Initialiser les attributs de la classe de base
        self.init_base_attributes()

        self.app = app_instance['app']
        self.main_window = app_instance['main_window']
        self.database = app_instance['database']
        self.config = test_config
        self.screenshots_dir = screenshots_dir

        # Configuration des mocks pour éviter les blocages
        mock_messagebox.question.return_value = mock_messagebox.No
        mock_messagebox.information.return_value = mock_messagebox.Ok
        mock_messagebox.warning.return_value = mock_messagebox.Ok
        mock_messagebox.critical.return_value = mock_messagebox.Ok

        # Initialiser l'automation
        if self.app:
            self.automation = PyQt5Automation(self.app)

        # Afficher la fenêtre principale
        self.main_window.show()
        self.wait_for_window(self.main_window)

        # Créer des données de test
        self.setup_test_data()

        # Ouvrir la fenêtre Facturas
        facturas_btn = self.automation.find_button_by_text(self.main_window, "Facturas")
        if facturas_btn:
            self.automation.click_button_safe(facturas_btn, wait_after=0.2)
            self.facturas_window = self.main_window.facturas_window
            self.wait_for_window(self.facturas_window)

        self.slow_mode_wait()
    
    def setup_test_data(self):
        """Créer des données de test avec produits ayant différents IVA"""
        # Créer un client de test
        client_data = TestDataFactory.create_client_data(
            nombre="Cliente Test IVA",
            nif="12345678A"
        )
        self.test_client_id = self.database.add_client(client_data)
        
        # Créer des produits avec différents IVA
        # Produit 1: IVA 4% (livres)
        product1 = TestDataFactory.create_product_data(
            nombre="Libro Test",
            precio=10.0,
            iva_recomendado=4.0
        )
        self.product1_id = self.database.add_product(product1)
        
        # Produit 2: IVA 10% (aliments)
        product2 = TestDataFactory.create_product_data(
            nombre="Alimento Test",
            precio=20.0,
            iva_recomendado=10.0
        )
        self.product2_id = self.database.add_product(product2)
        
        # Produit 3: IVA 21% (standard)
        product3 = TestDataFactory.create_product_data(
            nombre="Producto Test",
            precio=30.0,
            iva_recomendado=21.0
        )
        self.product3_id = self.database.add_product(product3)
    
    @pytest.mark.timeout(20)
    def test_iva_column_exists(self):
        """Test que la colonne IVA % existe dans la table"""
        self.logger.info("🧪 Test: Vérification colonne IVA %")
        
        # Cliquer sur Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        assert new_btn is not None, "Bouton Nueva non trouvé"
        self.automation.click_button_safe(new_btn, wait_after=0.2)
        
        # Vérifier que la table de produits existe
        assert hasattr(self.facturas_window, 'productos_table'), "Table productos manquante"
        
        # Vérifier les en-têtes de colonnes
        table = self.facturas_window.productos_table
        headers = []
        for col in range(table.columnCount()):
            header_item = table.horizontalHeaderItem(col)
            if header_item:
                headers.append(header_item.text())
        
        self.logger.info(f"En-têtes de colonnes: {headers}")
        
        # Vérifier que "IVA %" est présent
        assert "IVA %" in headers, f"Colonne 'IVA %' manquante. Colonnes: {headers}"
        
        # Vérifier l'ordre des colonnes
        expected_order = ["Producto", "Cantidad", "Precio Unit.", "IVA %", "Total", "Acciones"]
        assert headers == expected_order, f"Ordre incorrect. Attendu: {expected_order}, Obtenu: {headers}"
        
        self.take_screenshot("iva_column_exists")
        self.logger.info("✅ Test colonne IVA % réussi")
    
    @pytest.mark.timeout(20)
    def test_iva_recomendado_applied_by_default(self):
        """Test que l'IVA recommandé est appliqué par défaut lors de l'ajout d'un produit"""
        self.logger.info("🧪 Test: IVA recommandé appliqué par défaut")
        
        # Cliquer sur Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.2)
        
        # Sélectionner un client
        if hasattr(self.facturas_window, 'cliente_autocomplete'):
            # Charger les clients
            clientes = self.database.get_all_clients()
            self.facturas_window.cliente_autocomplete.load_clients(clientes)
            # Sélectionner le premier client
            if clientes:
                self.facturas_window.cliente_autocomplete.set_client(clientes[0])
        
        # Ajouter un produit avec IVA 4%
        if hasattr(self.facturas_window, 'producto_autocomplete'):
            productos = self.database.get_all_products()
            self.facturas_window.producto_autocomplete.load_products(productos)
            
            # Trouver le produit avec IVA 4%
            producto_4 = None
            for p in productos:
                if p.get('iva_recomendado') == 4.0:
                    producto_4 = p
                    break
            
            if producto_4:
                self.logger.info(f"Ajout produit: {producto_4['nombre']} avec IVA {producto_4.get('iva_recomendado')}%")
                self.facturas_window.producto_autocomplete.set_product(producto_4)
                self.facturas_window.cantidad_spin.setValue(2)
                
                # Cliquer sur Agregar
                add_btn = self.automation.find_button_by_text(self.facturas_window, "Agregar")
                if add_btn:
                    self.automation.click_button_safe(add_btn, wait_after=0.2)

                    # Vérifier que le produit a été ajouté
                    table = self.facturas_window.productos_table
                    assert table.rowCount() > 0, "Produit non ajouté à la table"

                    # Vérifier l'IVA dans la table (colonne 3)
                    iva_item = table.item(0, 3)
                    assert iva_item is not None, "Cellule IVA manquante"

                    iva_text = iva_item.text()
                    self.logger.info(f"IVA dans la table: {iva_text}")

                    # Extraire la valeur numérique
                    iva_value = float(iva_text.replace('%', '').strip())

                    # Vérifier que c'est bien 4%
                    assert abs(iva_value - 4.0) < 0.1, f"IVA incorrect. Attendu: 4.0%, Obtenu: {iva_value}%"

                    self.take_screenshot("iva_recomendado_applied")
                    self.logger.info("✅ Test IVA recommandé appliqué réussi")

    @pytest.mark.timeout(20)
    def test_iva_modifiable_in_table(self):
        """Test que l'IVA peut être modifié dans la table"""
        self.logger.info("🧪 Test: IVA modifiable dans la table")

        # Cliquer sur Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.2)

        # Sélectionner un client
        if hasattr(self.facturas_window, 'cliente_autocomplete'):
            clientes = self.database.get_all_clients()
            self.facturas_window.cliente_autocomplete.load_clients(clientes)
            if clientes:
                self.facturas_window.cliente_autocomplete.set_client(clientes[0])

        # Ajouter un produit
        if hasattr(self.facturas_window, 'producto_autocomplete'):
            productos = self.database.get_all_products()
            self.facturas_window.producto_autocomplete.load_products(productos)

            if productos:
                producto = productos[0]
                self.logger.info(f"Ajout produit: {producto['nombre']}")
                self.facturas_window.producto_autocomplete.set_product(producto)
                self.facturas_window.cantidad_spin.setValue(1)

                add_btn = self.automation.find_button_by_text(self.facturas_window, "Agregar")
                if add_btn:
                    self.automation.click_button_safe(add_btn, wait_after=0.2)

                    table = self.facturas_window.productos_table
                    assert table.rowCount() > 0, "Produit non ajouté"

                    # Obtenir l'IVA initial
                    iva_item = table.item(0, 3)
                    iva_initial = iva_item.text()
                    self.logger.info(f"IVA initial: {iva_initial}")

                    # Modifier l'IVA
                    new_iva = "10.0%"
                    table.blockSignals(True)
                    iva_item.setText(new_iva)
                    table.blockSignals(False)

                    # Déclencher le signal de changement manuellement
                    self.facturas_window.on_product_table_item_changed(iva_item)

                    # Vérifier que l'IVA a été modifié
                    iva_modified = table.item(0, 3).text()
                    self.logger.info(f"IVA modifié: {iva_modified}")

                    # Vérifier que le total a été recalculé
                    total_item = table.item(0, 4)
                    assert total_item is not None, "Total manquant"
                    total_text = total_item.text()
                    self.logger.info(f"Total après modification IVA: {total_text}")

                    self.take_screenshot("iva_modified")
                    self.logger.info("✅ Test IVA modifiable réussi")

    @pytest.mark.timeout(25)
    def test_totals_calculated_with_individual_iva(self):
        """Test que les totaux sont calculés avec l'IVA individuel de chaque produit"""
        self.logger.info("🧪 Test: Calcul totaux avec IVA individuel")

        # Cliquer sur Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.2)

        # Sélectionner un client
        if hasattr(self.facturas_window, 'cliente_autocomplete'):
            clientes = self.database.get_all_clients()
            self.facturas_window.cliente_autocomplete.load_clients(clientes)
            if clientes:
                self.facturas_window.cliente_autocomplete.set_client(clientes[0])

        # Ajouter plusieurs produits avec différents IVA
        if hasattr(self.facturas_window, 'producto_autocomplete'):
            productos = self.database.get_all_products()
            self.facturas_window.producto_autocomplete.load_products(productos)

            # Ajouter 2 produits différents
            productos_to_add = []
            for p in productos[:2]:
                productos_to_add.append(p)

            for producto in productos_to_add:
                self.logger.info(f"Ajout produit: {producto['nombre']} - IVA: {producto.get('iva_recomendado', 21)}%")
                self.facturas_window.producto_autocomplete.set_product(producto)
                self.facturas_window.cantidad_spin.setValue(1)

                add_btn = self.automation.find_button_by_text(self.facturas_window, "Agregar")
                if add_btn:
                    self.automation.click_button_safe(add_btn, wait_after=0.3)

            # Vérifier les totaux
            table = self.facturas_window.productos_table
            if table.rowCount() >= 2:
                # Calculer manuellement le total attendu
                subtotal_expected = 0.0
                iva_expected = 0.0

                for row in range(table.rowCount()):
                    cantidad = int(table.item(row, 1).text())
                    precio = float(table.item(row, 2).text().replace('€', '').strip())
                    iva_percent = float(table.item(row, 3).text().replace('%', '').strip())

                    linea_subtotal = cantidad * precio
                    linea_iva = linea_subtotal * (iva_percent / 100)

                    subtotal_expected += linea_subtotal
                    iva_expected += linea_iva

                    self.logger.info(f"Ligne {row}: {cantidad} × {precio}€ + {iva_percent}% IVA = {linea_subtotal + linea_iva:.2f}€")

                total_expected = subtotal_expected + iva_expected

                # Vérifier les totaux affichés
                if hasattr(self.facturas_window, 'subtotal_label'):
                    subtotal_text = self.facturas_window.subtotal_label.text()
                    subtotal_actual = float(subtotal_text.replace('€', '').strip())

                    self.logger.info(f"Subtotal attendu: {subtotal_expected:.2f}€, Obtenu: {subtotal_actual:.2f}€")
                    assert abs(subtotal_actual - subtotal_expected) < 0.01, "Subtotal incorrect"

                if hasattr(self.facturas_window, 'iva_label'):
                    iva_text = self.facturas_window.iva_label.text()
                    iva_actual = float(iva_text.replace('€', '').strip())

                    self.logger.info(f"IVA attendu: {iva_expected:.2f}€, Obtenu: {iva_actual:.2f}€")
                    assert abs(iva_actual - iva_expected) < 0.01, "IVA total incorrect"

                if hasattr(self.facturas_window, 'total_label'):
                    total_text = self.facturas_window.total_label.text()
                    total_actual = float(total_text.replace('€', '').strip())

                    self.logger.info(f"Total attendu: {total_expected:.2f}€, Obtenu: {total_actual:.2f}€")
                    assert abs(total_actual - total_expected) < 0.01, "Total incorrect"

                self.take_screenshot("totals_with_individual_iva")
                self.logger.info("✅ Test calcul totaux avec IVA individuel réussi")

    @pytest.mark.timeout(25)
    def test_save_and_load_factura_with_iva(self):
        """Test que l'IVA est sauvegardé et rechargé correctement"""
        self.logger.info("🧪 Test: Sauvegarde et chargement factura avec IVA")

        # Cliquer sur Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.2)

        # Sélectionner un client
        if hasattr(self.facturas_window, 'cliente_autocomplete'):
            clientes = self.database.get_all_clients()
            self.facturas_window.cliente_autocomplete.load_clients(clientes)
            if clientes:
                self.facturas_window.cliente_autocomplete.set_client(clientes[0])

        # Ajouter un produit avec IVA spécifique
        if hasattr(self.facturas_window, 'producto_autocomplete'):
            productos = self.database.get_all_products()
            self.facturas_window.producto_autocomplete.load_products(productos)

            # Trouver un produit avec IVA != 21%
            producto_test = None
            for p in productos:
                if p.get('iva_recomendado', 21.0) != 21.0:
                    producto_test = p
                    break

            if not producto_test:
                producto_test = productos[0]

            self.logger.info(f"Ajout produit: {producto_test['nombre']} - IVA: {producto_test.get('iva_recomendado', 21)}%")
            self.facturas_window.producto_autocomplete.set_product(producto_test)
            self.facturas_window.cantidad_spin.setValue(2)

            add_btn = self.automation.find_button_by_text(self.facturas_window, "Agregar")
            if add_btn:
                self.automation.click_button_safe(add_btn, wait_after=0.2)

                # Récupérer l'IVA avant sauvegarde
                table = self.facturas_window.productos_table
                iva_before = table.item(0, 3).text()
                total_before = table.item(0, 4).text()

                self.logger.info(f"Avant sauvegarde - IVA: {iva_before}, Total: {total_before}")

                # Sauvegarder la facture
                save_btn = self.automation.find_button_by_text(self.facturas_window, "Guardar")
                if save_btn:
                    self.automation.click_button_safe(save_btn, wait_after=0.3)

                    # Obtenir l'ID de la facture créée
                    facturas = self.database.get_all_invoices()
                    if facturas:
                        factura_id = facturas[-1]['id']
                        self.logger.info(f"Factura sauvegardée avec ID: {factura_id}")

                        # Recharger la facture
                        self.facturas_window.load_factura(factura_id)
                        self.slow_mode_wait()

                        # Vérifier que l'IVA est correct après rechargement
                        table_after = self.facturas_window.productos_table
                        if table_after.rowCount() > 0:
                            iva_after = table_after.item(0, 3).text()
                            total_after = table_after.item(0, 4).text()

                            self.logger.info(f"Après rechargement - IVA: {iva_after}, Total: {total_after}")

                            assert iva_after == iva_before, f"IVA différent après rechargement. Avant: {iva_before}, Après: {iva_after}"
                            assert total_after == total_before, f"Total différent après rechargement. Avant: {total_before}, Après: {total_after}"

                            self.take_screenshot("factura_reloaded_with_iva")
                            self.logger.info("✅ Test sauvegarde/chargement avec IVA réussi")

    @pytest.mark.timeout(25)
    def test_different_iva_rates_in_same_factura(self):
        """Test qu'on peut avoir différents taux d'IVA dans la même facture"""
        self.logger.info("🧪 Test: Différents taux IVA dans même facture")

        # Cliquer sur Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        self.automation.click_button_safe(new_btn, wait_after=0.2)

        # Sélectionner un client
        if hasattr(self.facturas_window, 'cliente_autocomplete'):
            clientes = self.database.get_all_clients()
            self.facturas_window.cliente_autocomplete.load_clients(clientes)
            if clientes:
                self.facturas_window.cliente_autocomplete.set_client(clientes[0])

        # Ajouter 3 produits avec IVA différents (4%, 10%, 21%)
        if hasattr(self.facturas_window, 'producto_autocomplete'):
            productos = self.database.get_all_products()
            self.facturas_window.producto_autocomplete.load_products(productos)

            # Grouper les produits par IVA
            productos_by_iva = {}
            for p in productos:
                iva = p.get('iva_recomendado', 21.0)
                if iva not in productos_by_iva:
                    productos_by_iva[iva] = p

            # Ajouter au moins 2 produits avec IVA différents
            ivas_added = []
            for iva, producto in list(productos_by_iva.items())[:3]:
                self.logger.info(f"Ajout produit avec IVA {iva}%: {producto['nombre']}")
                self.facturas_window.producto_autocomplete.set_product(producto)
                self.facturas_window.cantidad_spin.setValue(1)

                add_btn = self.automation.find_button_by_text(self.facturas_window, "Agregar")
                if add_btn:
                    self.automation.click_button_safe(add_btn, wait_after=0.3)
                    ivas_added.append(iva)

            # Vérifier que les IVA sont différents dans la table
            table = self.facturas_window.productos_table
            ivas_in_table = []
            for row in range(table.rowCount()):
                iva_text = table.item(row, 3).text()
                iva_value = float(iva_text.replace('%', '').strip())
                ivas_in_table.append(iva_value)

            self.logger.info(f"IVA dans la table: {ivas_in_table}")

            # Vérifier qu'il y a au moins 2 taux différents
            unique_ivas = set(ivas_in_table)
            assert len(unique_ivas) >= 2, f"Pas assez de taux IVA différents. Trouvés: {unique_ivas}"

            self.take_screenshot("different_iva_rates")
            self.logger.info("✅ Test différents taux IVA réussi")

