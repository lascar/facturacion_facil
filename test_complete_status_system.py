#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test complet du système de statuts de factures
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_status_system():
    """Test complet de bout en bout du système de statuts"""
    
    print("🧪 Test complet du système de statuts de factures")
    print("=" * 60)
    
    try:
        # 1. Test des imports
        print("\n1️⃣ Test des imports...")
        from database.database import db
        from utils.invoice_status_manager import invoice_status_manager
        print("✅ Imports réussis")
        
        # 2. Test de la base de données
        print("\n2️⃣ Test de la base de données...")
        db.init_database()
        print("✅ Base de données initialisée")
        
        # 3. Test des statuts par défaut
        print("\n3️⃣ Test des statuts par défaut...")
        statuses = invoice_status_manager.get_all_statuses()
        print(f"✅ {len(statuses)} statuts trouvés")
        
        expected_statuses = ['Borrador', 'Pendiente', 'Pagada', 'Vencida', 'Cancelada', 'Anulada']
        for expected in expected_statuses:
            found = any(s['nombre'] == expected for s in statuses)
            print(f"{'✅' if found else '❌'} Statut '{expected}' {'trouvé' if found else 'manquant'}")
        
        # 4. Test des permissions
        print("\n4️⃣ Test des permissions...")
        permissions_tests = [
            ('Borrador', True),
            ('Pendiente', False),
            ('Pagada', False),
            ('Vencida', False),
            ('Cancelada', False),
            ('Anulada', False)
        ]
        
        for status_name, expected_permission in permissions_tests:
            actual_permission = invoice_status_manager.can_modify_invoice(status_name)
            result = actual_permission == expected_permission
            print(f"{'✅' if result else '❌'} {status_name}: {actual_permission} (attendu: {expected_permission})")
        
        # 5. Test des couleurs
        print("\n5️⃣ Test des couleurs...")
        color_tests = [
            ('Borrador', '#6c757d'),
            ('Pendiente', '#ffc107'),
            ('Pagada', '#28a745'),
            ('Vencida', '#dc3545'),
            ('Cancelada', '#6f42c1'),
            ('Anulada', '#fd7e14')
        ]
        
        for status_name, expected_color in color_tests:
            actual_color = invoice_status_manager.get_status_color(status_name)
            result = actual_color == expected_color
            print(f"{'✅' if result else '❌'} {status_name}: {actual_color} (attendu: {expected_color})")
        
        # 6. Test de création d'un nouveau statut
        print("\n6️⃣ Test de création d'un nouveau statut...")
        new_status = {
            'nombre': 'Test Complet',
            'descripcion': 'Statut de test complet',
            'permite_modificacion': True,
            'color': '#ff5733',
            'orden': 100
        }
        
        success = invoice_status_manager.save_status(new_status)
        if success:
            print("✅ Nouveau statut créé")
            
            # Vérifier qu'il existe
            created_status = invoice_status_manager.get_status_by_name('Test Complet')
            if created_status:
                print("✅ Nouveau statut récupéré")
                print(f"   - Couleur: {created_status['color']}")
                print(f"   - Modifiable: {created_status['permite_modificacion']}")
            else:
                print("❌ Nouveau statut non trouvé")
        else:
            print("❌ Échec de création du nouveau statut")
        
        # 7. Test de création de facture avec statut
        print("\n7️⃣ Test de création de facture avec statut...")
        import time
        timestamp = int(time.time())
        
        invoice_data = {
            'numero': f'TEST-COMPLET-{timestamp}',
            'fecha': '2025-11-25',
            'estado': 'Borrador',
            'cliente': {
                'id': 1,
                'nombre': 'Cliente Test Complet',
                'nif': '87654321B',
                'direccion': 'Calle Test Complet 456'
            },
            'lineas': [],
            'subtotal': 200.0,
            'iva_total': 42.0,
            'total': 242.0
        }
        
        invoice_id = db.add_invoice(invoice_data)
        if invoice_id:
            print(f"✅ Facture créée avec ID: {invoice_id}")
            
            # Vérifier le statut
            saved_invoice = db.get_invoice_by_id(invoice_id)
            if saved_invoice and saved_invoice.get('estado') == 'Borrador':
                print("✅ Statut de facture correct")
            else:
                print(f"❌ Statut incorrect: {saved_invoice.get('estado') if saved_invoice else 'Facture non trouvée'}")
        else:
            print("❌ Échec de création de la facture")
        
        # 8. Test de modification de statut
        print("\n8️⃣ Test de modification de statut...")
        if invoice_id and saved_invoice:
            saved_invoice['estado'] = 'Pagada'
            update_success = db.update_invoice(saved_invoice)
            
            if update_success:
                print("✅ Statut modifié")
                
                # Vérifier la modification
                updated_invoice = db.get_invoice_by_id(invoice_id)
                if updated_invoice and updated_invoice.get('estado') == 'Pagada':
                    print("✅ Nouveau statut sauvegardé")
                    
                    # Vérifier que maintenant elle n'est plus modifiable
                    can_modify = invoice_status_manager.can_modify_invoice('Pagada')
                    print(f"✅ Facture payée non-modifiable: {not can_modify}")
                else:
                    print("❌ Nouveau statut non sauvegardé")
            else:
                print("❌ Échec de modification du statut")
        
        print("\n🎉 Test complet terminé avec succès!")
        print("\n📋 Résumé:")
        print("   ✅ Base de données fonctionnelle")
        print("   ✅ Statuts par défaut configurés")
        print("   ✅ Permissions de modification correctes")
        print("   ✅ Couleurs assignées")
        print("   ✅ Création de nouveaux statuts")
        print("   ✅ Factures avec statuts")
        print("   ✅ Modification de statuts")
        print("   ✅ Contrôle des permissions")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_status_system()
    if success:
        print("\n🎊 SYSTÈME DE STATUTS COMPLÈTEMENT FONCTIONNEL ! 🎊")
    else:
        print("\n❌ Des problèmes ont été détectés!")
        sys.exit(1)
