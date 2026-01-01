#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manuel pour vérifier que le bouton Guardar est activé pour un nouveau client
même sans remplir le NIF/CIF
"""

import pytest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PyQt5.QtWidgets import QApplication
from ui.client_autocomplete_widget import ClientDetailsWidget
from test.behaviour.base_behaviour_test import BaseBehaviourTest


class TestNuevoClienteGuardarButton(BaseBehaviourTest):
    """Tests pour vérifier que le bouton Guardar est activé pour un nouveau client"""

    def setup_test(self, app_instance):
        """Configuration du test avec l'instance de l'application"""
        self.app = app_instance['app']
        self.database = app_instance['database']
        self.main_window = app_instance['main_window']
        self.init_base_attributes()

    def test_nuevo_cliente_guardar_button(self, app_instance):
        """Test que le bouton Guardar est activé pour un nouveau client"""
        self.setup_test(app_instance)

        print("\n" + "=" * 70)
        print("TEST: Bouton Guardar activé pour nouveau client sans NIF")
        print("=" * 70)

        # Créer le widget
        widget = ClientDetailsWidget()
        widget.show()
        self.app.processEvents()

        try:
            # Simuler un nouveau client (sans NIF)
            new_client = {
                'id': None,
                'nombre': 'Nuevo Cliente Test',
                'nif': '',  # NIF vide
                'telefono': '',
                'email': '',
                'direccion': '',
                'is_new': True
            }

            print("\n1. Affichage d'un nouveau client sans NIF:")
            print(f"   - Nombre: {new_client['nombre']}")
            print(f"   - NIF: '{new_client['nif']}' (vide)")
            print(f"   - is_new: {new_client['is_new']}")

            # Afficher les détails du client
            widget.show_client_details(new_client)
            self.app.processEvents()

            # Vérifier l'état du bouton Guardar
            print("\n2. Vérification de l'état du bouton Guardar:")
            assert widget.save_btn.isEnabled(), (
                "   ❌ Le bouton Guardar est DÉSACTIVÉ\n"
                "   ❌ PROBLÈME: On ne peut pas sauvegarder sans remplir le NIF"
            )

            print("   ✅ Le bouton Guardar est ACTIVÉ")
            print("   ✅ On peut sauvegarder le client sans remplir le NIF")

            # Vérifier has_changes
            print(f"\n3. État interne:")
            print(f"   - has_changes: {widget.has_changes}")
            print(f"   - save_btn.isEnabled(): {widget.save_btn.isEnabled()}")

            # Test avec un client existant (pour comparaison)
            print("\n" + "=" * 70)
            print("COMPARAISON: Client existant")
            print("=" * 70)

            existing_client = {
                'id': 123,
                'nombre': 'Cliente Existente',
                'nif': '12345678A',
                'telefono': '666777888',
                'email': 'test@example.com',
                'direccion': 'Calle Test 123',
                'is_new': False
            }

            print("\n1. Affichage d'un client existant:")
            print(f"   - Nombre: {existing_client['nombre']}")
            print(f"   - NIF: {existing_client['nif']}")
            print(f"   - is_new: {existing_client['is_new']}")

            widget.show_client_details(existing_client)
            self.app.processEvents()

            print("\n2. Vérification de l'état du bouton Guardar:")
            if widget.save_btn.isEnabled():
                print("   ⚠️  Le bouton Guardar est ACTIVÉ")
                print("   ⚠️  (devrait être désactivé car pas de changements)")
            else:
                print("   ✅ Le bouton Guardar est DÉSACTIVÉ")
                print("   ✅ Normal: pas de changements détectés")

            print(f"\n3. État interne:")
            print(f"   - has_changes: {widget.has_changes}")
            print(f"   - save_btn.isEnabled(): {widget.save_btn.isEnabled()}")

            # Résumé
            print("\n" + "=" * 70)
            print("✅ TEST RÉUSSI")
            print("=" * 70)
            print("\nLe bouton Guardar est correctement activé pour un nouveau client,")
            print("même sans remplir le NIF/CIF (qui est optionnel).")
            print("=" * 70)

        finally:
            # Fermer le widget proprement
            widget.close()
            self.app.processEvents()


if __name__ == "__main__":
    # Exécuter avec pytest
    pytest.main([__file__, '-v', '-s'])

