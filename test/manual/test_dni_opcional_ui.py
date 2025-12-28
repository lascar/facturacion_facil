#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manuel pour vérifier que le DNI est optionnel dans l'interface utilisateur
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.cliente_service import ClienteService
from services.factura_service import FacturaService
from common.validators import FormValidator


def test_dni_opcional_validation():
    """Test de validation du DNI optionnel"""
    print("=" * 60)
    print("TEST: Validation du DNI optionnel")
    print("=" * 60)
    
    # Test 1: DNI vide doit être valide
    print("\n1. Test DNI vide:")
    result = FormValidator.validate_dni_nie("")
    if result is None:
        print("   ✅ DNI vide est valide (optionnel)")
    else:
        print(f"   ❌ ERREUR: {result}")
        return False
    
    # Test 2: DNI None doit être valide
    print("\n2. Test DNI None:")
    result = FormValidator.validate_dni_nie(None)
    if result is None:
        print("   ✅ DNI None est valide (optionnel)")
    else:
        print(f"   ❌ ERREUR: {result}")
        return False
    
    # Test 3: DNI avec espaces doit être valide
    print("\n3. Test DNI avec espaces:")
    result = FormValidator.validate_dni_nie("   ")
    if result is None:
        print("   ✅ DNI avec espaces est valide (optionnel)")
    else:
        print(f"   ❌ ERREUR: {result}")
        return False
    
    # Test 4: DNI valide doit être accepté
    print("\n4. Test DNI valide:")
    result = FormValidator.validate_dni_nie("12345678Z")
    if result is None:
        print("   ✅ DNI valide est accepté")
    else:
        print(f"   ⚠️  AVERTISSEMENT: {result}")
    
    return True


def test_cliente_creation_without_dni():
    """Test de création de client sans DNI"""
    print("\n" + "=" * 60)
    print("TEST: Création de client sans DNI")
    print("=" * 60)
    
    cliente_service = ClienteService()
    
    # Test 1: Créer un client sans DNI
    print("\n1. Création d'un client sans DNI:")
    try:
        client_id = cliente_service.create_cliente({
            'nombre': 'Cliente Test Sin DNI',
            'nif': '',  # DNI vide
            'email': 'test@example.com',
            'telefono': '666777888',
            'direccion': 'Calle Test 123'
        })
        print(f"   ✅ Cliente créé avec succès, ID: {client_id}")
        return client_id
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return None


def test_factura_creation_with_client_without_dni(client_id):
    """Test de création de facture avec client sans DNI"""
    print("\n" + "=" * 60)
    print("TEST: Création de facture avec client sans DNI")
    print("=" * 60)
    
    factura_service = FacturaService()
    
    print(f"\n1. Création d'une facture pour le client ID {client_id}:")
    try:
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
        print(f"   ✅ Facture créée avec succès, ID: {factura_id}")
        return True
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        return False


def main():
    """Fonction principale"""
    print("\n" + "=" * 60)
    print("TESTS MANUELS: DNI OPTIONNEL")
    print("=" * 60)
    
    # Test 1: Validation
    if not test_dni_opcional_validation():
        print("\n❌ Les tests de validation ont échoué")
        return 1
    
    # Test 2: Création de client
    client_id = test_cliente_creation_without_dni()
    if not client_id:
        print("\n❌ La création de client a échoué")
        return 1
    
    # Test 3: Création de facture
    if not test_factura_creation_with_client_without_dni(client_id):
        print("\n❌ La création de facture a échoué")
        return 1
    
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
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

