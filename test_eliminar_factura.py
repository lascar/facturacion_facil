#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du bouton Eliminar pour les factures
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from gui import set_gui_framework
from database.database import db
from ui.facturas_pyqt5 import FacturasPyQt5Window

def test_eliminar_button():
    """Test du bouton Eliminar dans la fenêtre Facturas"""
    
    print("🧪 TEST BOUTON ELIMINAR FACTURAS")
    print("=" * 40)
    
    # Configurer PyQt5
    set_gui_framework('pyqt5')
    
    # Créer l'application
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre Facturas
        print("🧾 Création de la fenêtre Facturas...")
        facturas_window = FacturasPyQt5Window()
        
        # Vérifier que le bouton Eliminar existe
        has_eliminar_btn = hasattr(facturas_window, 'eliminar_btn')
        print(f"🗑️  Bouton Eliminar présent: {has_eliminar_btn}")
        
        if has_eliminar_btn:
            # Vérifier le texte du bouton
            button_text = facturas_window.eliminar_btn.text()
            print(f"📝 Texte du bouton: '{button_text}'")
            
            # Vérifier que la méthode eliminar_factura existe
            has_method = hasattr(facturas_window, 'eliminar_factura')
            print(f"⚙️  Méthode eliminar_factura: {has_method}")
            
            # Vérifier que le bouton est connecté
            is_connected = facturas_window.eliminar_btn.receivers(facturas_window.eliminar_btn.clicked) > 0
            print(f"🔗 Bouton connecté: {is_connected}")
        
        # Vérifier les autres boutons pour comparaison
        print("\n📊 Autres boutons présents:")
        buttons = ['new_btn', 'view_btn', 'refresh_btn']
        for btn_name in buttons:
            if hasattr(facturas_window, btn_name):
                btn = getattr(facturas_window, btn_name)
                print(f"   ✅ {btn_name}: '{btn.text()}'")
            else:
                print(f"   ❌ {btn_name}: Non trouvé")
        
        # Vérifier les factures existantes
        print("\n📋 Factures dans la base de données:")
        facturas = db.get_all_invoices()
        print(f"   📊 Nombre de factures: {len(facturas)}")
        
        if facturas:
            for i, factura in enumerate(facturas[:3]):  # Afficher les 3 premières
                numero = factura.get('numero', 'N/A')
                cliente = factura.get('cliente', 'N/A')
                print(f"   {i+1}. Factura {numero} - Cliente: {cliente}")
            
            if len(facturas) > 3:
                print(f"   ... et {len(facturas) - 3} autres")
        else:
            print("   ⚠️  Aucune facture trouvée")
        
        print("\n🎯 RÉSULTAT DU TEST:")
        if has_eliminar_btn and has_method:
            print("✅ SUCCÈS - Le bouton Eliminar est correctement implémenté!")
            print("📋 Instructions pour tester:")
            print("   1. Lancez l'application: python main.py")
            print("   2. Ouvrez la fenêtre Facturas")
            print("   3. Sélectionnez une facture")
            print("   4. Cliquez sur '🗑️ Eliminar'")
            print("   5. Confirmez la suppression")
        else:
            print("❌ ÉCHEC - Le bouton Eliminar n'est pas correctement implémenté")
        
        return has_eliminar_btn and has_method
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

if __name__ == "__main__":
    success = test_eliminar_button()
    sys.exit(0 if success else 1)
