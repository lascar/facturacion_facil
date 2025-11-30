#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'élimination d'un client avec des factures associées
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from database.database import db
from ui.clientes_pyqt5 import ClientesPyQt5Window
from ui.facturas_pyqt5 import FacturasPyQt5Window

def create_test_data():
    """Créer des données de test : client avec factures"""
    print("🔧 Création des données de test...")
    
    # Créer un client de test
    client_data = {
        'nombre': 'Cliente Test Eliminación',
        'dni_nie': '12345678Z',
        'direccion': 'Calle Test 123',
        'email': 'test@example.com',
        'telefono': '666777888'
    }
    
    client_id = db.add_client(client_data)
    print(f"✅ Client créé avec ID: {client_id}")
    
    # Créer quelques factures pour ce client
    for i in range(3):
        invoice_data = {
            'numero': f'TEST-ELIM-{i+1:03d}',
            'fecha': '2024-11-30',
            'cliente': {
                'id': client_id,
                'nombre': client_data['nombre'],
                'nif': client_data['dni_nie'],
                'direccion': client_data['direccion']
            },
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0,
            'estado': 'Borrador',
            'lineas': []  # Pas de lignes pour ce test
        }

        invoice_id = db.add_invoice(invoice_data)
        print(f"✅ Facture {i+1} créée avec ID: {invoice_id}")
    
    return client_id

def test_client_deletion_with_invoices():
    """Test de l'élimination d'un client avec factures"""
    print("🧪 Test d'élimination d'un client avec factures")
    
    app = QApplication(sys.argv)
    
    try:
        # Créer les données de test
        client_id = create_test_data()
        
        # Ouvrir la fenêtre des clients
        clients_window = ClientesPyQt5Window()
        clients_window.show()
        
        print("\n📋 Instructions pour le test manuel :")
        print("1. Chercher le client 'Cliente Test Eliminación'")
        print("2. Le sélectionner dans la liste")
        print("3. Cliquer sur 'Eliminar'")
        print("4. Vérifier que le dialogue d'options s'affiche")
        print("5. Tester les différentes options :")
        print("   - 'Ver Facturas' : Affiche les informations")
        print("   - 'Eliminar Facturas' : Demande confirmation et supprime tout")
        print("   - 'Cancelar' : Ferme le dialogue")
        print("\n🎯 Résultat attendu :")
        print("- Le client ne peut pas être supprimé directement")
        print("- Un dialogue avec options s'affiche")
        print("- L'utilisateur peut choisir comment procéder")
        
        # Vérifier que le client existe avec des factures
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM facturas WHERE cliente_id = ?", (client_id,))
        invoice_count = cursor.fetchone()[0]
        conn.close()
        
        print(f"\n📊 État actuel :")
        print(f"- Client ID: {client_id}")
        print(f"- Nombre de factures: {invoice_count}")
        
        # Lancer l'application
        app.exec_()
        
    except Exception as e:
        print(f"❌ Erreur pendant le test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Nettoyer les données de test (optionnel)
        try:
            print("\n🧹 Nettoyage des données de test...")
            
            # Supprimer les factures de test
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM facturas WHERE numero_factura LIKE 'TEST-ELIM-%'")
            deleted_invoices = cursor.rowcount
            
            # Supprimer le client de test
            cursor.execute("DELETE FROM clientes WHERE nombre = 'Cliente Test Eliminación'")
            deleted_clients = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            print(f"✅ Nettoyage terminé: {deleted_invoices} factures, {deleted_clients} clients supprimés")
            
        except Exception as e:
            print(f"⚠️ Erreur pendant le nettoyage: {e}")

def test_database_constraint():
    """Test de la contrainte de base de données"""
    print("\n🔍 Test de la contrainte de base de données...")
    
    try:
        # Créer un client avec factures
        client_id = create_test_data()
        
        # Essayer de supprimer le client directement (doit échouer)
        try:
            db.delete_client(client_id)
            print("❌ ERREUR: La suppression du client a réussi alors qu'elle devrait échouer")
        except Exception as e:
            print(f"✅ Contrainte respectée: {e}")
        
        # Nettoyer
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM facturas WHERE cliente_id = ?", (client_id,))
        cursor.execute("DELETE FROM clientes WHERE id = ?", (client_id,))
        conn.commit()
        conn.close()
        print("✅ Données de test nettoyées")
        
    except Exception as e:
        print(f"❌ Erreur pendant le test de contrainte: {e}")

if __name__ == "__main__":
    print("========================================")
    print("  Test Élimination Client avec Factures")
    print("========================================")
    
    # Test de la contrainte de base de données
    test_database_constraint()
    
    # Test de l'interface utilisateur
    test_client_deletion_with_invoices()
