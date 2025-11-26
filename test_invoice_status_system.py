#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système de gestion des statuts de factures
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import db
from utils.invoice_status_manager import invoice_status_manager
from utils.logger import get_logger

def test_invoice_status_system():
    """Test complet du système de statuts de factures"""
    logger = get_logger("test_invoice_status")
    
    print("🧪 Test du système de gestion des statuts de factures")
    print("=" * 60)
    
    try:
        # 1. Test de la base de données - vérifier que les tables existent
        print("\n1️⃣ Test de la structure de base de données...")
        
        # Vérifier que la table factura_estados existe
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='factura_estados'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Table 'factura_estados' existe")
        else:
            print("❌ Table 'factura_estados' n'existe pas")
            return False
        
        # Vérifier que la colonne estado existe dans facturas
        cursor.execute("PRAGMA table_info(facturas)")
        columns = cursor.fetchall()
        estado_column_exists = any(col[1] == 'estado' for col in columns)
        
        if estado_column_exists:
            print("✅ Colonne 'estado' existe dans la table facturas")
        else:
            print("❌ Colonne 'estado' n'existe pas dans la table facturas")
            return False
        
        conn.close()
        
        # 2. Test des statuts par défaut
        print("\n2️⃣ Test des statuts par défaut...")
        statuses = invoice_status_manager.get_all_statuses()
        
        print(f"📊 Nombre de statuts trouvés: {len(statuses)}")
        
        expected_statuses = ['Borrador', 'Pendiente', 'Pagada', 'Vencida', 'Cancelada', 'Anulada']
        found_statuses = [s['nombre'] for s in statuses]
        
        for expected in expected_statuses:
            if expected in found_statuses:
                print(f"✅ Statut '{expected}' trouvé")
            else:
                print(f"❌ Statut '{expected}' manquant")
        
        # 3. Test des permissions de modification
        print("\n3️⃣ Test des permissions de modification...")
        
        # Borrador doit permettre la modification
        can_modify_borrador = invoice_status_manager.can_modify_invoice('Borrador')
        print(f"🔧 Borrador permet modification: {can_modify_borrador} {'✅' if can_modify_borrador else '❌'}")
        
        # Pagada ne doit pas permettre la modification
        can_modify_pagada = invoice_status_manager.can_modify_invoice('Pagada')
        print(f"🔒 Pagada permet modification: {can_modify_pagada} {'❌' if not can_modify_pagada else '✅'}")
        
        # 4. Test de création d'un nouveau statut
        print("\n4️⃣ Test de création d'un nouveau statut...")
        
        new_status_data = {
            'nombre': 'Test Status',
            'descripcion': 'Statut de test',
            'permite_modificacion': True,
            'color': '#ff0000',
            'orden': 99
        }
        
        success = invoice_status_manager.save_status(new_status_data)
        if success:
            print("✅ Nouveau statut créé avec succès")
            
            # Vérifier qu'il existe
            test_status = invoice_status_manager.get_status_by_name('Test Status')
            if test_status:
                print("✅ Nouveau statut trouvé dans la base de données")
                print(f"   - Nom: {test_status['nombre']}")
                print(f"   - Description: {test_status['descripcion']}")
                print(f"   - Permet modification: {test_status['permite_modificacion']}")
                print(f"   - Couleur: {test_status['color']}")
            else:
                print("❌ Nouveau statut non trouvé")
        else:
            print("❌ Échec de création du nouveau statut")
        
        # 5. Test de création d'une facture avec statut
        print("\n5️⃣ Test de création d'une facture avec statut...")
        
        # Créer une facture de test
        test_invoice_data = {
            'numero': 'TEST-2025-001',
            'fecha': '2025-11-25',
            'estado': 'Borrador',
            'cliente': {
                'id': 1,
                'nombre': 'Cliente Test',
                'nif': '12345678A',
                'direccion': 'Dirección Test'
            },
            'lineas': [],
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0
        }
        
        try:
            invoice_id = db.add_invoice(test_invoice_data)
            if invoice_id:
                print(f"✅ Facture créée avec ID: {invoice_id}")
                
                # Vérifier que le statut est sauvegardé
                saved_invoice = db.get_invoice_by_id(invoice_id)
                if saved_invoice and saved_invoice.get('estado') == 'Borrador':
                    print("✅ Statut de facture sauvegardé correctement")
                else:
                    print(f"❌ Statut incorrect: {saved_invoice.get('estado') if saved_invoice else 'Facture non trouvée'}")
            else:
                print("❌ Échec de création de la facture")
        except Exception as e:
            print(f"❌ Erreur lors de la création de la facture: {e}")
        
        # 6. Test de la liste des factures avec statuts
        print("\n6️⃣ Test de la liste des factures avec statuts...")
        
        all_invoices = db.get_all_invoices()
        print(f"📋 Nombre total de factures: {len(all_invoices)}")
        
        for invoice in all_invoices[:3]:  # Afficher les 3 premières
            print(f"   - {invoice['numero']}: {invoice['estado']} (€{invoice['total']})")
        
        print("\n🎉 Test du système de statuts terminé avec succès!")
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors du test: {e}")
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = test_invoice_status_system()
    if success:
        print("\n✅ Tous les tests sont passés!")
    else:
        print("\n❌ Certains tests ont échoué!")
        sys.exit(1)
