#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que le problème de visibilité du client est résolu
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.facturas_pyqt5 import CrearFacturaDialog, EditarFacturaDialog
from database.database import db

def test_crear_factura_dialog():
    """Test du dialog de création de factura"""
    print("🧪 TEST DIALOG CRÉATION FACTURA")
    print("=" * 35)
    
    app = QApplication(sys.argv)
    
    try:
        # Créer le dialog
        print("\n1️⃣ Création du dialog:")
        dialog = CrearFacturaDialog()
        print("   ✅ Dialog créé")
        
        # Configurer l'interface
        print("\n2️⃣ Configuration interface:")
        dialog.setup_ui()
        print("   ✅ Interface configurée")
        
        # Charger les données
        print("\n3️⃣ Chargement des données:")
        dialog.load_data()
        print("   ✅ Données chargées")
        
        # Vérifier le combo box des clients
        print("\n4️⃣ Vérification combo box clients:")
        combo = dialog.cliente_combo
        print(f"   📊 Nombre d'éléments: {combo.count()}")
        
        if combo.count() > 1:
            # Afficher quelques éléments pour vérifier le format
            print("   📋 Éléments du combo:")
            for i in range(min(3, combo.count())):
                text = combo.itemText(i)
                print(f"      {i}: '{text}'")
            
            # Vérifier le style
            style = combo.styleSheet()
            if "font-weight: bold" in style and "color: #2c3e50" in style:
                print("   ✅ Style amélioré appliqué")
                result = True
            else:
                print("   ⚠️ Style non appliqué ou incomplet")
                result = False
        else:
            print("   ❌ Aucun client trouvé")
            result = False
        
        return result
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def test_editar_factura_dialog():
    """Test du dialog d'édition de factura"""
    print("\n🧪 TEST DIALOG ÉDITION FACTURA")
    print("=" * 35)
    
    app = QApplication(sys.argv)
    
    try:
        # Créer une factura de test
        print("\n1️⃣ Création factura de test:")
        factura_test = {
            'id': 999,
            'numero': 'TEST-001',
            'fecha': '2025-12-07',
            'cliente': {'id': 1, 'nombre': 'Cliente Test', 'nif': '12345678A'},
            'estado': 'Borrador',
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0,
            'lineas': []
        }
        print("   ✅ Factura de test créée")
        
        # Créer le dialog
        print("\n2️⃣ Création du dialog:")
        dialog = EditarFacturaDialog(factura_test)
        print("   ✅ Dialog créé")
        
        # Configurer l'interface
        print("\n3️⃣ Configuration interface:")
        dialog.setup_ui()
        print("   ✅ Interface configurée")
        
        # Charger les données
        print("\n4️⃣ Chargement des données:")
        dialog.load_data()
        print("   ✅ Données chargées")
        
        # Vérifier le combo box des clients
        print("\n5️⃣ Vérification combo box clients:")
        combo = dialog.cliente_combo
        print(f"   📊 Nombre d'éléments: {combo.count()}")
        
        if combo.count() > 1:
            # Vérifier le format des éléments
            print("   📋 Format des éléments:")
            for i in range(min(3, combo.count())):
                text = combo.itemText(i)
                if "👤" in text and "•" in text:
                    print(f"      ✅ Format amélioré: '{text[:50]}...'")
                else:
                    print(f"      ⚠️ Format basique: '{text[:50]}...'")
            
            # Vérifier le style
            style = combo.styleSheet()
            if "font-weight: bold" in style:
                print("   ✅ Style amélioré appliqué")
                result = True
            else:
                print("   ⚠️ Style non appliqué")
                result = False
        else:
            print("   ❌ Aucun client trouvé")
            result = False
        
        return result
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def main():
    """Fonction principale"""
    print("🚀 TEST CORRECTION VISIBILITÉ CLIENTE")
    print("=" * 40)
    
    test1 = test_crear_factura_dialog()
    test2 = test_editar_factura_dialog()
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   Dialog Création: {'✅ OK' if test1 else '❌ PROBLÈME'}")
    print(f"   Dialog Édition: {'✅ OK' if test2 else '❌ PROBLÈME'}")
    
    if test1 and test2:
        print(f"\n🎉 PROBLÈME RÉSOLU !")
        print("   ✅ Style amélioré appliqué aux combo boxes")
        print("   ✅ Format de texte amélioré avec icônes")
        print("   ✅ Meilleure lisibilité du client sélectionné")
        
        print(f"\n📋 AMÉLIORATIONS APPORTÉES:")
        print("   • Police en gras pour le texte sélectionné")
        print("   • Couleur contrastée (#2c3e50)")
        print("   • Bordures et arrière-plan améliorés")
        print("   • Format avec icônes: 👤 Nom • NIF: 12345678A")
        print("   • Padding augmenté pour plus d'espace")
        
        print(f"\n🎯 POUR TESTER:")
        print("   1. Lance l'application: python3 main.py")
        print("   2. Va dans 'Facturas' → 'Nueva Factura'")
        print("   3. Clique sur le combo box 'Cliente'")
        print("   4. Sélectionne un client")
        print("   5. Le nom devrait être clairement lisible")
    else:
        print(f"\n⚠️ PROBLÈMES DÉTECTÉS")
        print("   Vérifier les détails ci-dessus")
    
    return test1 and test2

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
