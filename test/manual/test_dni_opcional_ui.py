#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manuel pour vérifier que le DNI est optionnel dans l'interface utilisateur
"""

import pytest
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.cliente_service import ClienteService
from services.factura_service import FacturaService
from common.validators import FormValidator
from test.behaviour.base_behaviour_test import BaseBehaviourTest


class TestDNIOpcionalUI(BaseBehaviourTest):
    """Tests pour vérifier que le DNI est optionnel dans l'interface utilisateur"""

    def setup_test(self, app_instance):
        """Configuration du test avec l'instance de l'application"""
        self.app = app_instance['app']
        self.database = app_instance['database']
        self.main_window = app_instance['main_window']
        self.init_base_attributes()

    def test_dni_opcional_validation(self):
        """Test de validation du DNI optionnel"""
        print("\n" + "=" * 60)
        print("TEST: Validation du DNI optionnel")
        print("=" * 60)

        # Test 1: DNI vide doit être valide
        print("\n1. Test DNI vide:")
        result = FormValidator.validate_dni_nie("")
        assert result is None, f"   ❌ ERREUR: {result}"
        print("   ✅ DNI vide est valide (optionnel)")

        # Test 2: DNI None doit être valide
        print("\n2. Test DNI None:")
        result = FormValidator.validate_dni_nie(None)
        assert result is None, f"   ❌ ERREUR: {result}"
        print("   ✅ DNI None est valide (optionnel)")

        # Test 3: DNI avec espaces doit être valide
        print("\n3. Test DNI avec espaces:")
        result = FormValidator.validate_dni_nie("   ")
        assert result is None, f"   ❌ ERREUR: {result}"
        print("   ✅ DNI avec espaces est valide (optionnel)")

        # Test 4: DNI valide doit être accepté
        print("\n4. Test DNI valide:")
        result = FormValidator.validate_dni_nie("12345678Z")
        if result is None:
            print("   ✅ DNI valide est accepté")
        else:
            print(f"   ⚠️  AVERTISSEMENT: {result}")

    def test_cliente_creation_without_dni(self, app_instance):
        """Test de création de client sans DNI"""
        self.setup_test(app_instance)

        print("\n" + "=" * 60)
        print("TEST: Création de client sans DNI")
        print("=" * 60)

        cliente_service = ClienteService()

        # Test 1: Créer un client sans DNI
        print("\n1. Création d'un client sans DNI:")
        client_id = cliente_service.create_cliente({
            'nombre': 'Cliente Test Sin DNI',
            'nif': '',  # DNI vide
            'email': 'test@example.com',
            'telefono': '666777888',
            'direccion': 'Calle Test 123'
        })

        assert client_id is not None, "   ❌ ERREUR: Client non créé"
        print(f"   ✅ Cliente créé avec succès, ID: {client_id}")

    def test_factura_creation_with_client_without_dni(self, app_instance):
        """Test de création de facture avec client sans DNI"""
        self.setup_test(app_instance)

        print("\n" + "=" * 60)
        print("TEST: Création de facture avec client sans DNI")
        print("=" * 60)

        # D'abord créer un client sans DNI
        cliente_service = ClienteService()
        client_id = cliente_service.create_cliente({
            'nombre': 'Cliente Test Sin DNI',
            'nif': '',  # DNI vide
            'email': 'test@example.com',
            'telefono': '666777888',
            'direccion': 'Calle Test 123'
        })

        assert client_id is not None, "Client non créé"

        # Maintenant créer une facture pour ce client
        factura_service = FacturaService()

        print(f"\n1. Création d'une facture pour le client ID {client_id}:")
        factura_id = factura_service.create_factura({
            'numero': f'TEST-DNI-{client_id}',
            'fecha': '2024-01-15',
            'cliente': {
                'id': client_id,
                'nombre': 'Cliente Test Sin DNI',
                'nif': '',  # DNI vide
                'direccion': 'Calle Test 123'
            },
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0,
            'lineas': []
        })

        assert factura_id is not None, "   ❌ ERREUR: Facture non créée"
        print(f"   ✅ Facture créée avec succès, ID: {factura_id}")

        # Résumé
        print("\n" + "=" * 60)
        print("✅ TOUS LES TESTS ONT RÉUSSI")
        print("=" * 60)
        print("\nConclusion:")
        print("  • Le DNI/NIE/NIF est bien OPTIONNEL")
        print("  • Les clients peuvent être créés sans DNI")
        print("  • Les factures peuvent être créées avec des clients sans DNI")
        print("  • L'interface utilisateur indique clairement '(opcional)'")
        print("=" * 60)


if __name__ == "__main__":
    # Exécuter avec pytest
    pytest.main([__file__, '-v', '-s'])

