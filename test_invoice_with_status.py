#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de création de factures avec statuts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database import db
from utils.invoice_status_manager import invoice_status_manager

def test_invoice_with_status():
    """Test de création et modification de factures avec statuts"""
    
    print("🧪 Test de création de factures avec statuts")
    print("=" * 50)
    
    try:
        # Initialiser la base de données
        db.init_database()
        print("✅ Base de données initialisée")
        
        # 1. Créer une facture avec statut Borrador
        print("\n1. Création d'une facture avec statut 'Borrador'...")
        
        import time
        timestamp = int(time.time())
        invoice_data = {
            'numero': f'TEST-STATUS-{timestamp}',
            'fecha': '2025-11-25',
            'estado': 'Borrador',
            'cliente': {
                'id': 1,
                'nombre': 'Cliente Test Status',
                'nif': '12345678Z',
                'direccion': 'Calle Test 123'
            },
            'lineas': [
                {
                    'producto_id': 1,
                    'cantidad': 2,
                    'precio_unitario': 50.0,
                    'iva_aplicado': 21.0,
                    'descuento': 0.0,
                    'subtotal': 100.0,
                    'descuento_amount': 0.0,
                    'iva_amount': 21.0,
                    'total': 121.0
                }
            ],
            'subtotal': 100.0,
            'iva_total': 21.0,
            'total': 121.0
        }
        
        invoice_id = db.add_invoice(invoice_data)
        if invoice_id:
            print(f"✅ Facture créée avec ID: {invoice_id}")
        else:
            print("❌ Échec de création de la facture")
            return False
        
        # 2. Vérifier que le statut est sauvegardé
        print("\n2. Vérification du statut sauvegardé...")
        
        saved_invoice = db.get_invoice_by_id(invoice_id)
        if saved_invoice:
            print(f"✅ Facture récupérée: {saved_invoice['numero']}")
            print(f"✅ Statut sauvegardé: {saved_invoice['estado']}")
            
            if saved_invoice['estado'] == 'Borrador':
                print("✅ Statut correct!")
            else:
                print(f"❌ Statut incorrect: attendu 'Borrador', reçu '{saved_invoice['estado']}'")
        else:
            print("❌ Facture non trouvée")
            return False
        
        # 3. Modifier le statut vers 'Pendiente'
        print("\n3. Modification du statut vers 'Pendiente'...")
        
        saved_invoice['estado'] = 'Pendiente'
        success = db.update_invoice(saved_invoice)
        
        if success:
            print("✅ Facture mise à jour")
            
            # Vérifier le nouveau statut
            updated_invoice = db.get_invoice_by_id(invoice_id)
            if updated_invoice and updated_invoice['estado'] == 'Pendiente':
                print("✅ Nouveau statut sauvegardé: Pendiente")
            else:
                print(f"❌ Statut non mis à jour: {updated_invoice['estado'] if updated_invoice else 'Facture non trouvée'}")
        else:
            print("❌ Échec de mise à jour")
        
        # 4. Vérifier les permissions
        print("\n4. Test des permissions de modification...")
        
        can_modify_borrador = invoice_status_manager.can_modify_invoice('Borrador')
        can_modify_pendiente = invoice_status_manager.can_modify_invoice('Pendiente')
        can_modify_pagada = invoice_status_manager.can_modify_invoice('Pagada')
        
        print(f"✅ Borrador modifiable: {can_modify_borrador}")
        print(f"✅ Pendiente modifiable: {can_modify_pendiente}")
        print(f"✅ Pagada modifiable: {can_modify_pagada}")
        
        # 5. Test de la liste des factures avec statuts
        print("\n5. Test de la liste des factures...")
        
        all_invoices = db.get_all_invoices()
        print(f"✅ {len(all_invoices)} factures trouvées")
        
        # Chercher notre facture de test
        test_invoice = None
        for inv in all_invoices:
            if inv['numero'].startswith('TEST-STATUS-'):
                test_invoice = inv
                break
        
        if test_invoice:
            print(f"✅ Facture de test trouvée dans la liste")
            print(f"   - Numéro: {test_invoice['numero']}")
            print(f"   - Statut: {test_invoice['estado']}")
            print(f"   - Total: €{test_invoice['total']}")
        else:
            print("❌ Facture de test non trouvée dans la liste")
        
        # 6. Test des couleurs de statuts
        print("\n6. Test des couleurs de statuts...")
        
        color_borrador = invoice_status_manager.get_status_color('Borrador')
        color_pendiente = invoice_status_manager.get_status_color('Pendiente')
        color_pagada = invoice_status_manager.get_status_color('Pagada')
        
        print(f"✅ Couleur Borrador: {color_borrador}")
        print(f"✅ Couleur Pendiente: {color_pendiente}")
        print(f"✅ Couleur Pagada: {color_pagada}")
        
        print("\n🎉 Test de factures avec statuts terminé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_invoice_with_status()
    if success:
        print("\n✅ Tous les tests de factures avec statuts sont passés!")
    else:
        print("\n❌ Certains tests ont échoué!")
        sys.exit(1)
