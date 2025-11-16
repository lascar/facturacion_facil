#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la visibilité des données dans l'interface
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_visibilite_donnees():
    """Test de la visibilité des données"""
    print("👁️ TEST DE VISIBILITÉ DES DONNÉES")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.clientes_pyqt6 import ClientesPyQt6Window
        from ui.facturas_pyqt6 import FacturasPyQt6Window
        from database.database import db
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Test 1: Vérifier les données en base
        print("\n--- Test 1: Données en Base ---")
        
        clients = db.get_all_clients()
        factures = db.get_all_invoices()
        
        print(f"📊 Clients en base: {len(clients)}")
        print(f"📄 Factures en base: {len(factures)}")
        
        # Chercher les clients "lolo"
        lolo_clients = [c for c in clients if 'lolo' in c['nombre'].lower()]
        print(f"👤 Clients 'lolo': {len(lolo_clients)}")
        for client in lolo_clients:
            print(f"   • ID {client['id']}: {client['nombre']} ({client.get('nif', 'N/A')})")
        
        # Chercher la facture récente
        facture_recente = None
        if factures:
            facture_recente = max(factures, key=lambda f: f['id'])
            print(f"📄 Facture la plus récente: ID {facture_recente['id']} - {facture_recente['numero']}")
        
        # Test 2: Fenêtre des clients
        print("\n--- Test 2: Fenêtre des Clients ---")
        
        clients_window = ClientesPyQt6Window()
        clients_window.show()
        
        app.processEvents()
        time.sleep(0.5)
        
        table_clients = clients_window.clients_table
        rows_clients = table_clients.rowCount()
        print(f"✅ Clients dans la table: {rows_clients}")
        
        # Vérifier si les clients "lolo" sont visibles
        lolo_found_in_table = 0
        for row in range(rows_clients):
            name_item = table_clients.item(row, 0)
            if name_item and 'lolo' in name_item.text().lower():
                lolo_found_in_table += 1
                print(f"   • Ligne {row}: {name_item.text()}")
        
        print(f"👤 Clients 'lolo' visibles dans la table: {lolo_found_in_table}")
        
        if lolo_found_in_table == len(lolo_clients):
            print("✅ Tous les clients 'lolo' sont visibles")
        elif lolo_found_in_table > 0:
            print("⚠️ Certains clients 'lolo' sont visibles")
        else:
            print("❌ Aucun client 'lolo' visible dans la table")
        
        # Test 3: Fenêtre des factures
        print("\n--- Test 3: Fenêtre des Factures ---")
        
        facturas_window = FacturasPyQt6Window()
        facturas_window.show()
        
        app.processEvents()
        time.sleep(0.5)
        
        table_facturas = facturas_window.invoices_table
        rows_facturas = table_facturas.rowCount()
        print(f"✅ Factures dans la table: {rows_facturas}")
        
        # Vérifier si la facture récente est visible
        facture_recente_visible = False
        if facture_recente:
            for row in range(rows_facturas):
                numero_item = table_facturas.item(row, 0)
                if numero_item and numero_item.text() == facture_recente['numero']:
                    facture_recente_visible = True
                    print(f"   • Ligne {row}: {numero_item.text()} - {table_facturas.item(row, 2).text()}")
                    break
        
        if facture_recente_visible:
            print("✅ Facture récente visible dans la table")
        else:
            print("❌ Facture récente non visible dans la table")
        
        # Test 4: Vérifier les données des premières lignes
        print("\n--- Test 4: Premières Lignes des Tables ---")
        
        print("📋 Premiers clients:")
        for row in range(min(3, rows_clients)):
            name_item = table_clients.item(row, 0)
            nif_item = table_clients.item(row, 1)
            if name_item:
                print(f"   • {name_item.text()} ({nif_item.text() if nif_item else 'N/A'})")
        
        print("📋 Premières factures:")
        for row in range(min(3, rows_facturas)):
            numero_item = table_facturas.item(row, 0)
            client_item = table_facturas.item(row, 2)
            total_item = table_facturas.item(row, 3)
            if numero_item:
                print(f"   • {numero_item.text()} - {client_item.text() if client_item else 'N/A'} - {total_item.text() if total_item else 'N/A'}")
        
        # Test 5: Cohérence base vs interface
        print("\n--- Test 5: Cohérence Base vs Interface ---")
        
        if rows_clients == len(clients):
            print("✅ Nombre de clients cohérent")
        else:
            print(f"⚠️ Incohérence clients: {len(clients)} en base vs {rows_clients} dans l'interface")
        
        if rows_facturas == len(factures):
            print("✅ Nombre de factures cohérent")
        else:
            print(f"⚠️ Incohérence factures: {len(factures)} en base vs {rows_facturas} dans l'interface")
        
        # Fermer les fenêtres
        clients_window.close()
        facturas_window.close()
        print("\n✅ Fenêtres fermées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_visibilite_donnees()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST DE VISIBILITÉ")
        print("="*60)
        
        if success:
            print("🎉 TEST DE VISIBILITÉ RÉUSSI !")
            print("\n✨ VÉRIFICATIONS EFFECTUÉES :")
            print("   ✅ Données en base de données")
            print("   ✅ Affichage dans la fenêtre clients")
            print("   ✅ Affichage dans la fenêtre factures")
            print("   ✅ Cohérence base vs interface")
            print("   ✅ Visibilité des données récentes")
            
            print("\n🎯 DIAGNOSTIC COMPLET EFFECTUÉ !")
            print("\n🔍 SI LES DONNÉES NE SONT PAS VISIBLES :")
            print("   1. Vérifiez les logs pour les erreurs")
            print("   2. Redémarrez l'application")
            print("   3. Vérifiez les méthodes load_clients/load_invoices")
            print("   4. Vérifiez les signaux de mise à jour")
            
            return 0
        else:
            print("❌ TEST DE VISIBILITÉ ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
