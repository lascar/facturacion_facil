#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple pour les clients sans GUI bloquante
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_clientes_without_gui():
    """Test des clients sans interface GUI"""
    
    print("🧪 TEST CLIENTES SANS GUI")
    print("=" * 40)
    
    try:
        # Configuration du framework
        from gui import set_gui_framework
        set_gui_framework('pyqt5')
        print("✅ Framework PyQt5 configuré")
        
        # Test d'importation
        from database.models import Cliente
        print("✅ Modèle Cliente importé")
        
        # Test de création de client
        cliente = Cliente()
        cliente.nombre = "Test Cliente Simple"
        cliente.dni_nie = "12345678B"
        cliente.email = "test@simple.com"
        cliente.telefono = "999888777"
        cliente.direccion = "Dirección de prueba simple"
        
        # Sauvegarder
        cliente_id = cliente.save()
        assert cliente_id is not None, "Cliente debe haberse guardado"
        print(f"✅ Cliente guardado con ID: {cliente_id}")
        
        # Vérifier
        cliente_creado = Cliente.get_by_nombre("Test Cliente Simple")
        assert cliente_creado is not None, "Cliente debe haberse creado"
        assert cliente_creado.email == "test@simple.com", "Email debe coincidir"
        print(f"✅ Cliente verificado: {cliente_creado.nombre}")
        
        # Test de mise à jour
        cliente_creado.telefono = "111111111"
        cliente_creado.save()
        
        cliente_actualizado = Cliente.get_by_id(cliente_id)
        assert cliente_actualizado.telefono == "111111111", "Teléfono debe haberse actualizado"
        print("✅ Cliente actualizado correctamente")
        
        # Test de suppression
        cliente_actualizado.delete()
        cliente_eliminado = Cliente.get_by_id(cliente_id)
        assert cliente_eliminado is None, "Cliente debe haberse eliminado"
        print("✅ Cliente eliminado correctamente")
        
        print("\n🎉 TODOS LOS TESTS PASARON")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_clientes_gui_import():
    """Test d'importation des modules GUI sans création de fenêtre"""
    
    print("\n🧪 TEST IMPORTATION GUI")
    print("=" * 40)
    
    try:
        # Test d'importation du module GUI
        from ui.clientes_pyqt5 import ClientesPyQt5Window
        print("✅ Module ClientesPyQt5Window importé")
        
        # Vérifier que la classe existe et a les bonnes méthodes
        assert hasattr(ClientesPyQt5Window, '__init__'), "Classe doit avoir __init__"
        print("✅ Classe ClientesPyQt5Window valide")
        
        # Test d'importation des dépendances PyQt5
        from PyQt5.QtWidgets import QApplication, QWidget
        from PyQt5.QtCore import QObject
        print("✅ Dépendances PyQt5 disponibles")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES TESTS CLIENTS")
    print("=" * 50)
    
    success1 = test_clientes_without_gui()
    success2 = test_clientes_gui_import()
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        sys.exit(1)
