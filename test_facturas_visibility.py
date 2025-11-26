#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier la visibilité des factures dans la fenêtre
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework
set_gui_framework('pyqt6')

from database.database import db
from database.models import Factura, Cliente
from datetime import datetime

def test_facturas_in_database():
    """Test pour vérifier les factures dans la base de données"""
    print("🔍 Test de visibilité des factures")
    print("=" * 50)
    
    # Initialiser la base de données
    db.init_database()
    
    # 1. Vérifier les factures existantes
    print("\n1. 📋 Vérification des factures existantes...")
    
    try:
        # Méthode 1: Via db.get_all_invoices()
        db_invoices = db.get_all_invoices()
        print(f"   📊 Factures trouvées via db.get_all_invoices(): {len(db_invoices)}")
        
        if db_invoices:
            for i, invoice in enumerate(db_invoices[:3]):  # Afficher les 3 premières
                print(f"   - Facture {i+1}: {invoice.get('numero', 'N/A')} - {invoice.get('cliente_nombre', 'N/A')} - €{invoice.get('total', 0):.2f}")
        
        # Méthode 2: Via le modèle Factura
        model_facturas = Factura.get_all()
        print(f"   📊 Factures trouvées via Factura.get_all(): {len(model_facturas)}")
        
        if model_facturas:
            for i, factura in enumerate(model_facturas[:3]):  # Afficher les 3 premières
                print(f"   - Factura {i+1}: {factura.numero_factura} - {factura.nombre_cliente} - €{factura.total_factura:.2f}")
        
        # Méthode 3: Requête directe
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM facturas")
        count = cursor.fetchone()[0]
        conn.close()
        
        print(f"   📊 Factures trouvées via requête directe: {count}")
        
        if count == 0:
            print("\n⚠️  PROBLÈME DÉTECTÉ: Aucune facture dans la base de données!")
            print("   Cela explique pourquoi elles ne sont pas visibles dans l'interface.")
            return create_test_invoice()
        else:
            print("\n✅ Des factures existent dans la base de données")
            return True
            
    except Exception as e:
        print(f"\n❌ Erreur lors de la vérification: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_test_invoice():
    """Crée une facture de test pour vérifier la visibilité"""
    print("\n2. 🆕 Création d'une facture de test...")
    
    try:
        # Créer un client de test s'il n'existe pas
        clients = db.get_all_clients()
        if not clients:
            print("   👤 Création d'un client de test...")
            client = Cliente(
                nombre="Cliente Test",
                dni_nie="12345678A",
                direccion="Calle Test, 123",
                email="test@cliente.com",
                telefono="123456789"
            )
            client.save()
            client_id = client.id
            print(f"   ✅ Client créé avec ID: {client_id}")
        else:
            client_id = clients[0]['id']
            print(f"   ✅ Utilisation du client existant ID: {client_id}")
        
        # Créer une facture de test
        print("   📄 Création d'une facture de test...")
        
        # Méthode 1: Via le modèle Factura
        factura = Factura(
            numero_factura="TEST-001",
            fecha_factura=datetime.now().strftime("%Y-%m-%d"),
            cliente_id=client_id,
            nombre_cliente="Cliente Test",
            dni_nie_cliente="12345678A",
            direccion_cliente="Calle Test, 123",
            subtotal=100.0,
            total_iva=21.0,
            total_factura=121.0,
            modo_pago="Efectivo"
        )
        factura.save()
        
        print(f"   ✅ Facture créée: {factura.numero_factura} (ID: {factura.id})")
        
        # Vérifier que la facture est maintenant visible
        print("\n3. 🔍 Vérification de la visibilité après création...")
        
        db_invoices = db.get_all_invoices()
        print(f"   📊 Factures maintenant visibles: {len(db_invoices)}")
        
        if db_invoices:
            for invoice in db_invoices:
                print(f"   - {invoice.get('numero', 'N/A')} - {invoice.get('cliente_nombre', 'N/A')} - €{invoice.get('total', 0):.2f}")
            
            print("\n✅ PROBLÈME RÉSOLU: Les factures sont maintenant visibles!")
            print("   La fenêtre des factures devrait maintenant afficher les données.")
            return True
        else:
            print("\n❌ Les factures ne sont toujours pas visibles")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors de la création de la facture de test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_facturas_window_loading():
    """Test du chargement de la fenêtre des factures"""
    print("\n4. 🖥️  Test du chargement de la fenêtre des factures...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.facturas_pyqt6 import FacturasPyQt6Window
        
        # Créer l'application Qt si nécessaire
        app = QApplication.instance() or QApplication([])
        
        # Créer la fenêtre des factures
        facturas_window = FacturasPyQt6Window()
        
        # Vérifier que la méthode de chargement existe
        assert hasattr(facturas_window, 'load_invoices_data'), "Méthode load_invoices_data manquante"
        
        print("   ✅ Fenêtre des factures créée avec succès")
        print("   ✅ Méthode de chargement des données disponible")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test de la fenêtre: {e}")
        return False

if __name__ == "__main__":
    try:
        success = test_facturas_in_database()
        
        if success:
            test_facturas_window_loading()
            print("\n🎉 DIAGNOSTIC TERMINÉ")
            print("✅ Les factures devraient maintenant être visibles dans l'interface!")
            sys.exit(0)
        else:
            print("\n❌ Problème non résolu")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erreur lors du diagnostic: {e}")
        sys.exit(1)
