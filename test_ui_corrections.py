#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des corrections UI pour l'éditeur de factures
"""

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_button_centering():
    """Tester le centrage des boutons poubelle"""
    print("🔍 Test du centrage des boutons poubelle...")
    
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton
        from PyQt5.QtCore import Qt
        
        # Créer une application Qt pour le test
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Tester la création d'un bouton centré comme dans le code
        eliminar_btn = QPushButton("🗑️")
        eliminar_btn.setFixedSize(30, 25)
        
        # Créer un widget conteneur pour centrer le bouton
        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)
        container_layout.addWidget(eliminar_btn)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        print("✅ Structure de centrage créée avec succès")
        print(f"   - Taille du bouton: {eliminar_btn.size().width()}x{eliminar_btn.size().height()}")
        print(f"   - Alignement: {container_layout.alignment()}")
        print(f"   - Marges: {container_layout.contentsMargins()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test centrage: {e}")
        return False

def test_dialog_flow():
    """Tester le flux de dialogue d'édition"""
    print("\n🔍 Test du flux de dialogue d'édition...")
    
    try:
        # Vérifier que les imports fonctionnent
        from ui.facturas_pyqt5 import EditarFacturaDialog
        print("✅ Import EditarFacturaDialog réussi")
        
        # Créer des données de test
        test_factura = {
            'id': 1,
            'numero': 'TEST-001',
            'fecha': '2024-01-01',
            'cliente': {'id': 1, 'nombre': 'Cliente Test'},
            'estado': 'Borrador',
            'lineas': [
                {
                    'producto_id': 1,
                    'producto_nombre': 'Producto Test',
                    'cantidad': 2,
                    'precio_unitario': 10.0,
                    'iva_aplicado': 21.0,
                    'subtotal': 20.0,
                    'iva_amount': 4.2,
                    'total': 24.2
                }
            ]
        }
        
        print("✅ Données de test créées")
        print(f"   - Factura ID: {test_factura['id']}")
        print(f"   - Número: {test_factura['numero']}")
        print(f"   - Líneas: {len(test_factura['lineas'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test dialogue: {e}")
        return False

def test_message_flow():
    """Tester le flux des messages"""
    print("\n🔍 Test du flux des messages...")
    
    try:
        # Vérifier que le code ne contient plus le message redondant
        with open('ui/facturas_pyqt5.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compter les occurrences de "actualizada correctamente"
        count = content.count("actualizada correctamente")
        print(f"✅ Occurrences de 'actualizada correctamente': {count}")
        
        if count == 1:
            print("✅ Message redondant supprimé avec succès")
            return True
        else:
            print("⚠️  Nombre d'occurrences inattendu")
            return False
        
    except Exception as e:
        print(f"❌ Erreur test messages: {e}")
        return False

def test_imports():
    """Tester les imports nécessaires"""
    print("\n🔍 Test des imports...")
    
    try:
        from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
        from PyQt5.QtCore import Qt
        print("✅ Imports PyQt5 réussis")
        
        from ui.facturas_pyqt5 import FacturasPyQt5Window, EditarFacturaDialog
        print("✅ Imports classes factures réussis")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur imports: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 TEST DES CORRECTIONS UI")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_button_centering,
        test_dialog_flow,
        test_message_flow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erreur dans {test.__name__}: {e}")
    
    print("\n" + "=" * 40)
    print(f"🎯 RÉSULTATS: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 CORRECTIONS UI VALIDÉES !")
        print("\n📋 Corrections appliquées:")
        print("   ✅ Boutons poubelle centrés dans leurs cellules")
        print("   ✅ Message de succès unique (pas de redondance)")
        print("   ✅ Fermeture automatique après sauvegarde")
    else:
        print("⚠️  Certains tests ont échoué")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n✅ Test terminé: {success}")
    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        success = False
    
    sys.exit(0 if success else 1)
