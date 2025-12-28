#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test manuel pour vérifier que le bouton Guardar est activé pour un nouveau client
même sans remplir le NIF/CIF
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PyQt5.QtWidgets import QApplication
from ui.client_autocomplete_widget import ClientDetailsWidget


def test_nuevo_cliente_guardar_button():
    """Test que le bouton Guardar est activé pour un nouveau client"""
    print("=" * 70)
    print("TEST: Bouton Guardar activé pour nouveau client sans NIF")
    print("=" * 70)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    # Créer le widget
    widget = ClientDetailsWidget()
    
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
    
    # Vérifier l'état du bouton Guardar
    print("\n2. Vérification de l'état du bouton Guardar:")
    if widget.save_btn.isEnabled():
        print("   ✅ Le bouton Guardar est ACTIVÉ")
        print("   ✅ On peut sauvegarder le client sans remplir le NIF")
        result = True
    else:
        print("   ❌ Le bouton Guardar est DÉSACTIVÉ")
        print("   ❌ PROBLÈME: On ne peut pas sauvegarder sans remplir le NIF")
        result = False
    
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
    if result:
        print("✅ TEST RÉUSSI")
        print("=" * 70)
        print("\nLe bouton Guardar est correctement activé pour un nouveau client,")
        print("même sans remplir le NIF/CIF (qui est optionnel).")
    else:
        print("❌ TEST ÉCHOUÉ")
        print("=" * 70)
        print("\nLe bouton Guardar n'est pas activé pour un nouveau client.")
        print("Il faut corriger la logique dans ClientDetailsWidget.")
    print("=" * 70)
    
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(test_nuevo_cliente_guardar_button())

