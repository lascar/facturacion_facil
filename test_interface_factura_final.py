#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final pour vérifier que l'interface respecte le numéro inicial
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.facturas_pyqt5 import FacturasPyQt5Window
from utils.factura_numbering import FacturaNumberingService

def test_interface_factura_numero():
    """Test que l'interface génère le bon numéro"""
    print("🧪 TEST FINAL INTERFACE FACTURA")
    print("=" * 35)
    
    # Créer l'application Qt
    app = QApplication(sys.argv)
    
    try:
        # Test du service de numérotation
        print("\n1️⃣ Service de numérotation:")
        numbering_service = FacturaNumberingService()
        numero_service = numbering_service.get_next_numero_factura()
        print(f"   📝 Service génère: '{numero_service}'")
        
        # Test de l'interface
        print("\n2️⃣ Interface facturas:")
        from ui.facturas_pyqt5 import CrearFacturaDialog
        crear_dialog = CrearFacturaDialog()
        numero_interface = crear_dialog.generate_invoice_number()
        print(f"   📝 Interface génère: '{numero_interface}'")
        
        # Comparaison
        print("\n3️⃣ Comparaison:")
        if numero_service == numero_interface:
            print("   ✅ PARFAIT ! Interface et service cohérents")
            print(f"   🎯 Numéro généré: '{numero_interface}'")
            result = True
        else:
            print("   ❌ PROBLÈME ! Incohérence détectée")
            print(f"      Service: '{numero_service}'")
            print(f"      Interface: '{numero_interface}'")
            result = False
        
        # Test avec création d'une factura
        print("\n4️⃣ Test création factura:")
        crear_dialog.setup_ui()
        numero_ui = crear_dialog.numero_edit.text()
        print(f"   📝 Numéro dans UI: '{numero_ui}'")
        
        if numero_ui == numero_service:
            print("   ✅ UI affiche le bon numéro")
        else:
            print(f"   ⚠️ UI affiche: '{numero_ui}' au lieu de '{numero_service}'")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

def test_configuration_actuelle():
    """Vérifier la configuration actuelle"""
    print("\n🧪 CONFIGURATION ACTUELLE")
    print("=" * 30)
    
    try:
        import sqlite3
        
        # Vérifier la configuration en base
        print("\n1️⃣ Configuration en base:")
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT numero_factura_inicial FROM organizacion WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            config_db = result[0]
            print(f"   📝 Numéro inicial DB: '{config_db}'")
        else:
            print("   ❌ Aucune configuration trouvée")
            return False
        
        # Vérifier via Config
        print("\n2️⃣ Configuration via Config:")
        from config.config import app_config
        config_class = app_config.get_factura_numero_inicial()
        print(f"   📝 Config class: '{config_class}'")
        
        # Vérifier cohérence
        print("\n3️⃣ Cohérence:")
        if str(config_db) == str(config_class):
            print("   ✅ Configuration cohérente")
            return True
        else:
            print("   ❌ Configuration incohérente")
            print(f"      DB: '{config_db}'")
            print(f"      Config: '{config_class}'")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST FINAL NUMÉRO INICIAL FACTURA")
    print("=" * 40)
    
    test1 = test_configuration_actuelle()
    test2 = test_interface_factura_numero()
    
    print(f"\n🎯 RÉSUMÉ FINAL:")
    print(f"   Configuration: {'✅ OK' if test1 else '❌ PROBLÈME'}")
    print(f"   Interface: {'✅ OK' if test2 else '❌ PROBLÈME'}")
    
    if test1 and test2:
        print(f"\n🎉 PROBLÈME RÉSOLU !")
        print("   ✅ Le numéro inicial est maintenant respecté")
        print("   ✅ L'interface utilise le bon service")
        print("   ✅ La configuration fonctionne correctement")
        
        print(f"\n📋 POUR TESTER:")
        print("   1. Lance l'application: python3 main.py")
        print("   2. Va dans 'Facturas' → 'Nueva Factura'")
        print("   3. Le numéro devrait être '2025-wp-01'")
        print("   4. Après sauvegarde, la suivante sera '2025-wp-02'")
    else:
        print(f"\n⚠️ PROBLÈMES PERSISTANTS")
        print("   Vérifier les détails ci-dessus")
    
    return test1 and test2

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
