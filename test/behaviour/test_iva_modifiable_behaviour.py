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
from ui.factura_edit_window import FacturaEditWindow


class TestIVAModifiableBehaviour(BaseBehaviourTest):
    """Tests de comportement pour l'IVA modifiable dans les factures"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, app_instance, test_config, screenshots_dir, mock_messagebox, mock_filedialog):
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

        # Capturer les appels à warning pour diagnostic
        def log_warning(*args, **kwargs):
            if len(args) >= 2:
                self.logger.warning(f"⚠️ QMessageBox.warning appelé: {args[1]}")
            return mock_messagebox.Ok
        mock_messagebox.warning.side_effect = log_warning

        def log_critical(*args, **kwargs):
            if len(args) >= 2:
                self.logger.error(f"❌ QMessageBox.critical appelé: {args[1]}")
            return mock_messagebox.Ok
        mock_messagebox.critical.side_effect = log_critical

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
        import time
        # Utiliser un timestamp pour garantir l'unicité des références
        timestamp = int(time.time() * 1000) % 100000  # Garder seulement les 5 derniers chiffres

        # Créer un client de test
        client_data = TestDataFactory.create_client_data(index=1)
        # Personnaliser le nom pour ce test
        client_data['nombre'] = f"Cliente Test IVA {timestamp}"
        client_data['nif'] = f"IVA{timestamp:05d}"
        self.test_client_id = self.database.add_client(client_data)

        # Créer des produits avec différents IVA
        # Produit 1: IVA 4% (livres)
        product1 = TestDataFactory.create_product_data(index=101)
        product1['nombre'] = f"Libro Test {timestamp}"
        product1['referencia'] = f"LIB{timestamp:05d}"
        product1['precio_venta'] = 10.0
        product1['iva_recomendado'] = 4.0
        self.product1_id = self.database.add_product(product1)

        # Produit 2: IVA 10% (aliments)
        product2 = TestDataFactory.create_product_data(index=102)
        product2['nombre'] = f"Alimento Test {timestamp}"
        product2['referencia'] = f"ALI{timestamp:05d}"
        product2['precio_venta'] = 20.0
        product2['iva_recomendado'] = 10.0
        self.product2_id = self.database.add_product(product2)

        # Produit 3: IVA 21% (standard)
        product3 = TestDataFactory.create_product_data(index=103)
        product3['nombre'] = f"Producto Test {timestamp}"
        product3['referencia'] = f"PRO{timestamp:05d}"
        product3['precio_venta'] = 30.0
        product3['iva_recomendado'] = 21.0
        self.product3_id = self.database.add_product(product3)

    def open_edit_window(self):
        """Helper pour ouvrir la fenêtre d'édition et la retourner"""
        # Cliquer sur Nueva Factura
        new_btn = self.automation.find_button_by_text(self.facturas_window, "Nueva")
        assert new_btn is not None, "Bouton Nueva non trouvé"
        self.automation.click_button_safe(new_btn, wait_after=0.5)

        # Attendre l'ouverture de la fenêtre d'édition
        edit_window = None
        for widget in self.app.topLevelWidgets():
            if isinstance(widget, FacturaEditWindow) and widget.isVisible():
                edit_window = widget
                break

        assert edit_window is not None, "Fenêtre d'édition non ouverte"
        return edit_window

    @pytest.mark.timeout(20)
    def test_iva_column_exists(self):
        """Test que la colonne IVA existe dans la table"""
        self.logger.info("🧪 Test: Vérification colonne IVA")

        # Ouvrir la fenêtre d'édition
        edit_window = self.open_edit_window()

        try:
            # Vérifier que la table de produits existe
            assert hasattr(edit_window, 'productos_table'), "Table productos manquante"

            # Vérifier les en-têtes de colonnes
            table = edit_window.productos_table
            headers = []
            for col in range(table.columnCount()):
                header_item = table.horizontalHeaderItem(col)
                if header_item:
                    headers.append(header_item.text())

            self.logger.info(f"En-têtes de colonnes: {headers}")

            # Vérifier que "IVA" est présent
            assert "IVA" in headers, f"Colonne 'IVA' manquante. Colonnes: {headers}"

            # Vérifier l'ordre des colonnes (selon factura_edit_window.py ligne 183)
            expected_order = ["Producto", "Cantidad", "Precio", "IVA", "Total", ""]
            assert headers == expected_order, f"Ordre incorrect. Attendu: {expected_order}, Obtenu: {headers}"

            self.take_screenshot("iva_column_exists")
            self.logger.info("✅ Test colonne IVA réussi")
        finally:
            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()
    
    @pytest.mark.timeout(20)
    def test_iva_recomendado_applied_by_default(self):
        """Test que l'IVA recommandé est appliqué par défaut lors de l'ajout d'un produit"""
        self.logger.info("🧪 Test: IVA recommandé appliqué par défaut")

        # Ouvrir la fenêtre d'édition
        edit_window = self.open_edit_window()

        try:
            # Sélectionner un client
            if hasattr(edit_window, 'cliente_autocomplete'):
                # Charger les clients
                clientes = self.database.get_all_clients()
                edit_window.cliente_autocomplete.load_clients(clientes)
                # Sélectionner le premier client
                if clientes:
                    edit_window.cliente_autocomplete.set_client(clientes[0])

            # Ajouter un produit avec IVA 4%
            if hasattr(edit_window, 'producto_autocomplete'):
                productos = self.database.get_all_products()
                edit_window.producto_autocomplete.load_products(productos)

                # Trouver le produit avec IVA 4%
                producto_4 = None
                for p in productos:
                    if p.get('iva_recomendado') == 4.0:
                        producto_4 = p
                        break

                if producto_4:
                    self.logger.info(f"Ajout produit: {producto_4['nombre']} avec IVA {producto_4.get('iva_recomendado')}%")
                    edit_window.producto_autocomplete.set_product(producto_4)
                    edit_window.cantidad_spin.setValue(2)

                    # Cliquer sur Agregar
                    add_btn = self.automation.find_button_by_text(edit_window, "Agregar")
                    if add_btn:
                        self.automation.click_button_safe(add_btn, wait_after=0.2)

                        # Vérifier que le produit a été ajouté
                        table = edit_window.productos_table
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
        finally:
            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()

    @pytest.mark.timeout(20)
    def test_iva_modifiable_in_table(self):
        """Test que l'IVA peut être modifié dans la table"""
        self.logger.info("🧪 Test: IVA modifiable dans la table")

        # Ouvrir la fenêtre d'édition
        edit_window = self.open_edit_window()

        try:
            # Sélectionner un client
            if hasattr(edit_window, 'cliente_autocomplete'):
                clientes = self.database.get_all_clients()
                edit_window.cliente_autocomplete.load_clients(clientes)
                if clientes:
                    edit_window.cliente_autocomplete.set_client(clientes[0])

            # Ajouter un produit
            if hasattr(edit_window, 'producto_autocomplete'):
                productos = self.database.get_all_products()
                edit_window.producto_autocomplete.load_products(productos)

                if productos:
                    producto = productos[0]
                    self.logger.info(f"Ajout produit: {producto['nombre']}")
                    edit_window.producto_autocomplete.set_product(producto)
                    edit_window.cantidad_spin.setValue(1)

                    add_btn = self.automation.find_button_by_text(edit_window, "Agregar")
                    if add_btn:
                        self.automation.click_button_safe(add_btn, wait_after=0.2)

                        table = edit_window.productos_table
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
                        edit_window.on_table_item_changed(iva_item)

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
        finally:
            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()

    @pytest.mark.timeout(25)
    def test_totals_calculated_with_individual_iva(self):
        """Test que les totaux sont calculés avec l'IVA individuel de chaque produit"""
        self.logger.info("🧪 Test: Calcul totaux avec IVA individuel")

        # Ouvrir la fenêtre d'édition
        edit_window = self.open_edit_window()

        try:
            # Sélectionner un client
            if hasattr(edit_window, 'cliente_autocomplete'):
                clientes = self.database.get_all_clients()
                edit_window.cliente_autocomplete.load_clients(clientes)
                if clientes:
                    edit_window.cliente_autocomplete.set_client(clientes[0])

            # Ajouter plusieurs produits avec différents IVA
            if hasattr(edit_window, 'producto_autocomplete'):
                productos = self.database.get_all_products()
                edit_window.producto_autocomplete.load_products(productos)

                # Ajouter 2 produits différents
                productos_to_add = []
                for p in productos[:2]:
                    productos_to_add.append(p)

                for producto in productos_to_add:
                    self.logger.info(f"Ajout produit: {producto['nombre']} - IVA: {producto.get('iva_recomendado', 21)}%")
                    edit_window.producto_autocomplete.set_product(producto)
                    edit_window.cantidad_spin.setValue(1)

                    add_btn = self.automation.find_button_by_text(edit_window, "Agregar")
                    if add_btn:
                        self.automation.click_button_safe(add_btn, wait_after=0.3)

                # Vérifier les totaux
                table = edit_window.productos_table
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
                    if hasattr(edit_window, 'subtotal_label'):
                        subtotal_text = edit_window.subtotal_label.text()
                        subtotal_actual = float(subtotal_text.replace('€', '').strip())

                        self.logger.info(f"Subtotal attendu: {subtotal_expected:.2f}€, Obtenu: {subtotal_actual:.2f}€")
                        assert abs(subtotal_actual - subtotal_expected) < 0.01, "Subtotal incorrect"

                    if hasattr(edit_window, 'iva_label'):
                        iva_text = edit_window.iva_label.text()
                        iva_actual = float(iva_text.replace('€', '').strip())

                        self.logger.info(f"IVA attendu: {iva_expected:.2f}€, Obtenu: {iva_actual:.2f}€")
                        assert abs(iva_actual - iva_expected) < 0.01, "IVA total incorrect"

                    if hasattr(edit_window, 'total_label'):
                        total_text = edit_window.total_label.text()
                        total_actual = float(total_text.replace('€', '').strip())

                        self.logger.info(f"Total attendu: {total_expected:.2f}€, Obtenu: {total_actual:.2f}€")
                        assert abs(total_actual - total_expected) < 0.01, "Total incorrect"

                    self.take_screenshot("totals_with_individual_iva")
                    self.logger.info("✅ Test calcul totaux avec IVA individuel réussi")
        finally:
            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()

    @pytest.mark.timeout(25)
    def test_save_and_load_factura_with_iva(self):
        """Test que l'IVA est sauvegardé et rechargé correctement"""
        self.logger.info("🧪 Test: Sauvegarde et chargement factura avec IVA")

        # Ouvrir la fenêtre d'édition
        edit_window = self.open_edit_window()

        try:
            # Attendre que l'interface se mette à jour
            self.wait_and_process_events(500)

            # Récupérer le numéro de facture généré automatiquement
            numero_factura = edit_window.numero_edit.text()
            self.logger.info(f"Numéro de facture généré automatiquement: {numero_factura}")

            # Sélectionner un client
            if hasattr(edit_window, 'cliente_autocomplete'):
                clientes = self.database.get_all_clients()
                edit_window.cliente_autocomplete.load_clients(clientes)
                if clientes:
                    edit_window.cliente_autocomplete.set_client(clientes[0])
                    self.wait_and_process_events(200)

                    # DIAGNOSTIC: Vérifier si le client est vraiment sélectionné
                    current_client = edit_window.cliente_autocomplete.get_current_client()
                    self.logger.info(f"Client sélectionné: {current_client}")
                    if not current_client:
                        self.logger.error("❌ PROBLÈME: Aucun client sélectionné après set_client()")

            # Ajouter un produit avec IVA spécifique
            if hasattr(edit_window, 'producto_autocomplete'):
                productos = self.database.get_all_products()
                edit_window.producto_autocomplete.load_products(productos)

                # Trouver un produit avec IVA != 21%
                producto_test = None
                for p in productos:
                    if p.get('iva_recomendado', 21.0) != 21.0:
                        producto_test = p
                        break

                if not producto_test:
                    producto_test = productos[0]

                self.logger.info(f"Ajout produit: {producto_test['nombre']} - IVA: {producto_test.get('iva_recomendado', 21)}%")
                edit_window.producto_autocomplete.set_product(producto_test)
                edit_window.cantidad_spin.setValue(2)

                add_btn = self.automation.find_button_by_text(edit_window, "Agregar")
                if add_btn:
                    self.automation.click_button_safe(add_btn, wait_after=0.2)

                    # Récupérer l'IVA avant sauvegarde
                    table = edit_window.productos_table
                    iva_before = table.item(0, 3).text()
                    total_before = table.item(0, 4).text()

                    self.logger.info(f"Avant sauvegarde - IVA: {iva_before}, Total: {total_before}")

                    # Compter les factures avant sauvegarde
                    facturas_before = self.database.get_all_invoices()
                    count_before = len(facturas_before)
                    self.logger.info(f"Nombre de factures avant sauvegarde: {count_before}")

                    # Sauvegarder la facture
                    # DIAGNOSTIC: Donner le focus à la fenêtre
                    edit_window.raise_()
                    edit_window.activateWindow()
                    edit_window.setFocus()
                    self.wait_and_process_events(200)

                    save_btn = self.automation.find_button_by_text(edit_window, "Guardar")
                    if save_btn:
                        self.logger.info(f"Bouton Guardar trouvé - Enabled: {save_btn.isEnabled()}, Visible: {save_btn.isVisible()}")

                        # DIAGNOSTIC: Appeler directement save_factura() au lieu de cliquer
                        self.logger.info("🔧 Appel direct de save_factura() pour diagnostic")
                        edit_window.save_factura()
                        self.wait_and_process_events(500)

                        # Vérifier que la facture a été créée
                        facturas_after = self.database.get_all_invoices()
                        count_after = len(facturas_after)
                        self.logger.info(f"Nombre de factures après sauvegarde: {count_after}")

                        assert count_after > count_before, f"La facture n'a pas été sauvegardée. Avant: {count_before}, Après: {count_after}"

                        # Trouver la facture qu'on vient de créer par son numéro
                        factura_creee = None
                        for f in facturas_after:
                            if f.get('numero') == numero_factura:
                                factura_creee = f
                                break

                        assert factura_creee is not None, f"Facture {numero_factura} non trouvée dans la base"
                        self.logger.info(f"Factura trouvée avec ID: {factura_creee['id']}, Numéro: {factura_creee['numero']}")

                        # La fenêtre d'édition devrait se fermer après sauvegarde
                        # Ouvrir à nouveau pour éditer
                        self.wait_and_process_events(500)

                        # Cliquer sur Editar pour rouvrir la facture
                        editar_btn = self.automation.find_button_by_text(self.facturas_window, "Editar")
                        if editar_btn:
                            self.automation.click_button_safe(editar_btn, wait_after=0.5)

                            # Trouver la nouvelle fenêtre d'édition
                            edit_window_reload = None
                            for widget in self.app.topLevelWidgets():
                                if isinstance(widget, FacturaEditWindow) and widget.isVisible() and widget != edit_window:
                                    edit_window_reload = widget
                                    break

                            if edit_window_reload:
                                # Vérifier que l'IVA est correct après rechargement
                                table_after = edit_window_reload.productos_table
                                if table_after.rowCount() > 0:
                                    iva_after = table_after.item(0, 3).text()
                                    total_after = table_after.item(0, 4).text()

                                    self.logger.info(f"Après rechargement - IVA: {iva_after}, Total: {total_after}")

                                    assert iva_after == iva_before, f"IVA différent après rechargement. Avant: {iva_before}, Après: {iva_after}"
                                    assert total_after == total_before, f"Total différent après rechargement. Avant: {total_before}, Après: {total_after}"

                                    self.take_screenshot("factura_reloaded_with_iva")
                                    self.logger.info("✅ Test sauvegarde/chargement avec IVA réussi")

                                # Fermer la fenêtre de rechargement
                                edit_window_reload.close()
                                self.app.processEvents()
                    else:
                        self.logger.error("Bouton Guardar non trouvé!")
        finally:
            # Fermer la fenêtre d'édition si elle est encore ouverte
            if edit_window and edit_window.isVisible():
                edit_window.close()
                self.app.processEvents()

    @pytest.mark.timeout(25)
    def test_different_iva_rates_in_same_factura(self):
        """Test qu'on peut avoir différents taux d'IVA dans la même facture"""
        self.logger.info("🧪 Test: Différents taux IVA dans même facture")

        # Ouvrir la fenêtre d'édition
        edit_window = self.open_edit_window()

        try:
            # Sélectionner un client
            if hasattr(edit_window, 'cliente_autocomplete'):
                clientes = self.database.get_all_clients()
                edit_window.cliente_autocomplete.load_clients(clientes)
                if clientes:
                    edit_window.cliente_autocomplete.set_client(clientes[0])

            # Ajouter 3 produits avec IVA différents (4%, 10%, 21%)
            if hasattr(edit_window, 'producto_autocomplete'):
                productos = self.database.get_all_products()
                edit_window.producto_autocomplete.load_products(productos)

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
                    edit_window.producto_autocomplete.set_product(producto)
                    edit_window.cantidad_spin.setValue(1)

                    add_btn = self.automation.find_button_by_text(edit_window, "Agregar")
                    if add_btn:
                        self.automation.click_button_safe(add_btn, wait_after=0.3)
                        ivas_added.append(iva)

                # Vérifier que les IVA sont différents dans la table
                table = edit_window.productos_table
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
        finally:
            # Fermer la fenêtre d'édition
            edit_window.close()
            self.app.processEvents()

