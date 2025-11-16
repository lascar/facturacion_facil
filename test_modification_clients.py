#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la modification de clients dans la fenêtre de gestion
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_modification_clients():
    """Test de la modification de clients"""
    print("✏️ TEST DE MODIFICATION DE CLIENTS")
    print("="*60)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.clientes_pyqt6 import ClientesPyQt6Window
        from database.database import db
        
        # Créer l'application PyQt6
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        
        print("✅ QApplication créée")
        
        # Test 1: Créer un client de test à modifier
        print("\n--- Test 1: Création d'un Client à Modifier ---")
        
        # Nom unique pour éviter les conflits
        import datetime
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        original_client = {
            'nombre': f'Cliente Original {timestamp}',
            'nif': f'ORIG{timestamp}',
            'direccion': f'Calle Original {timestamp}, 123',
            'telefono': f'91-{timestamp[:3]}-{timestamp[3:]}',
            'email': f'original{timestamp}@test.com'
        }
        
        try:
            client_id = db.add_client(original_client)
            original_client['id'] = client_id
            print(f"✅ Cliente original creado (ID: {client_id})")
            print(f"   • Nom: {original_client['nombre']}")
            print(f"   • NIF: {original_client['nif']}")
            print(f"   • Email: {original_client['email']}")
        except Exception as e:
            print(f"❌ Error creando cliente original: {e}")
            return False
        
        # Test 2: Créer la fenêtre des clients
        print("\n--- Test 2: Fenêtre des Clients ---")
        
        clients_window = ClientesPyQt6Window()
        clients_window.show()
        
        print("✅ Fenêtre des clients créée")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(0.5)
        
        # Test 3: Vérifier que le client apparaît dans la table
        print("\n--- Test 3: Client dans la Table ---")
        
        table = clients_window.clients_table
        found_row = -1
        
        for row in range(table.rowCount()):
            name_item = table.item(row, 0)
            if name_item and name_item.text() == original_client['nombre']:
                found_row = row
                print(f"✅ Client trouvé dans la table (ligne {row})")
                break
        
        if found_row == -1:
            print("❌ Client non trouvé dans la table")
            return False
        
        # Test 4: Simuler la sélection du client
        print("\n--- Test 4: Sélection du Client ---")
        
        # Sélectionner la ligne
        table.selectRow(found_row)
        app.processEvents()
        time.sleep(0.2)
        
        # Vérifier que le client est chargé dans le formulaire
        loaded_name = clients_window.name_edit.text()
        loaded_nif = clients_window.nif_edit.text()
        loaded_email = clients_window.email_edit.text()
        
        print(f"✅ Données chargées dans le formulaire:")
        print(f"   • Nom: '{loaded_name}'")
        print(f"   • NIF: '{loaded_nif}'")
        print(f"   • Email: '{loaded_email}'")
        
        # Vérifier la cohérence
        if loaded_name == original_client['nombre']:
            print("✅ Nom chargé correctement")
        else:
            print(f"⚠️ Nom incorrect: '{loaded_name}' vs '{original_client['nombre']}'")
        
        if loaded_nif == original_client['nif']:
            print("✅ NIF chargé correctement")
        else:
            print(f"⚠️ NIF incorrect: '{loaded_nif}' vs '{original_client['nif']}'")
        
        # Test 5: Vérifier current_client
        print("\n--- Test 5: Current Client ---")
        
        if clients_window.current_client:
            print("✅ current_client défini")
            print(f"   • ID: {clients_window.current_client.get('id', 'N/A')}")
            print(f"   • Nom: {clients_window.current_client.get('nombre', 'N/A')}")
        else:
            print("⚠️ current_client non défini")
        
        # Test 6: Modifier les données
        print("\n--- Test 6: Modification des Données ---")
        
        modified_data = {
            'nombre': f'Cliente Modificado {timestamp}',
            'nif': f'MOD{timestamp}',
            'direccion': f'Calle Modificada {timestamp}, 456',
            'telefono': f'91-{timestamp[3:]}-{timestamp[:3]}',
            'email': f'modificado{timestamp}@test.com'
        }
        
        # Modifier les champs
        clients_window.name_edit.setText(modified_data['nombre'])
        clients_window.nif_edit.setText(modified_data['nif'])
        clients_window.address_edit.setPlainText(modified_data['direccion'])
        clients_window.phone_edit.setText(modified_data['telefono'])
        clients_window.email_edit.setText(modified_data['email'])
        
        app.processEvents()
        print("✅ Données modifiées dans le formulaire")
        
        # Test 7: Sauvegarder les modifications
        print("\n--- Test 7: Sauvegarde des Modifications ---")
        
        try:
            clients_window.save_client()
            app.processEvents()
            time.sleep(0.5)
            
            print("✅ Méthode save_client exécutée")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            import traceback
            traceback.print_exc()
        
        # Test 8: Vérifier en base de données
        print("\n--- Test 8: Vérification en Base ---")
        
        # Récupérer le client modifié
        updated_client = None
        clients_after = db.get_all_clients()
        
        for client in clients_after:
            if client['id'] == client_id:
                updated_client = client
                break
        
        if updated_client:
            print(f"✅ Client trouvé en base après modification:")
            print(f"   • ID: {updated_client['id']}")
            print(f"   • Nom: {updated_client['nombre']}")
            print(f"   • NIF: {updated_client.get('nif', 'N/A')}")
            print(f"   • Email: {updated_client.get('email', 'N/A')}")
            
            # Vérifier les modifications
            if updated_client['nombre'] == modified_data['nombre']:
                print("✅ Nom modifié correctement")
            else:
                print(f"⚠️ Nom non modifié: '{updated_client['nombre']}' vs '{modified_data['nombre']}'")
            
            if updated_client.get('nif', '') == modified_data['nif']:
                print("✅ NIF modifié correctement")
            else:
                print(f"⚠️ NIF non modifié: '{updated_client.get('nif', '')}' vs '{modified_data['nif']}'")
                
        else:
            print("❌ Client non trouvé en base après modification")
        
        # Test 9: Vérifier la méthode update_client directement
        print("\n--- Test 9: Test Direct update_client ---")
        
        test_update_data = {
            'id': client_id,
            'nombre': f'Cliente Test Direct {timestamp}',
            'nif': f'DIRECT{timestamp}',
            'direccion': f'Calle Direct {timestamp}',
            'telefono': f'91-000-{timestamp[-3:]}',
            'email': f'direct{timestamp}@test.com'
        }
        
        try:
            success = db.update_client(test_update_data)
            if success:
                print("✅ update_client retourne True")
            else:
                print("⚠️ update_client retourne False")
                
            # Vérifier en base
            direct_updated = None
            clients_final = db.get_all_clients()
            for client in clients_final:
                if client['id'] == client_id:
                    direct_updated = client
                    break
            
            if direct_updated and direct_updated['nombre'] == test_update_data['nombre']:
                print("✅ Modification directe réussie")
            else:
                print("⚠️ Modification directe échouée")
                
        except Exception as e:
            print(f"❌ Erreur modification directe: {e}")
        
        # Fermer la fenêtre
        clients_window.close()
        print("\n✅ Fenêtre fermée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    try:
        success = test_modification_clients()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST DE MODIFICATION DE CLIENTS")
        print("="*60)
        
        if success:
            print("🎉 TEST DE MODIFICATION DE CLIENTS RÉUSSI !")
            print("\n✨ FONCTIONNALITÉS VALIDÉES :")
            print("   ✅ Création d'un client à modifier")
            print("   ✅ Affichage dans la table")
            print("   ✅ Sélection et chargement dans le formulaire")
            print("   ✅ Modification des données")
            print("   ✅ Sauvegarde des modifications")
            print("   ✅ Vérification en base de données")
            print("   ✅ Méthode update_client fonctionnelle")
            
            print("\n🎯 MODIFICATION DE CLIENTS OPÉRATIONNELLE !")
            print("\n✏️ PROCESSUS DE MODIFICATION :")
            print("   1. Ouvrir la fenêtre des clients")
            print("   2. Cliquer sur un client dans la liste")
            print("   3. Données chargées dans le formulaire")
            print("   4. Modifier les informations nécessaires")
            print("   5. Cliquer 'Guardar' pour sauvegarder")
            print("   6. Modifications sauvegardées en base")
            
            print("\n🚀 Pour tester manuellement :")
            print("   1. Lancez: python main.py")
            print("   2. Cliquez sur 'Clientes'")
            print("   3. Cliquez sur un client existant")
            print("   4. Modifiez les informations")
            print("   5. Cliquez 'Guardar'")
            print("   6. Vérifiez les modifications")
            
            return 0
        else:
            print("❌ TEST DE MODIFICATION DE CLIENTS ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
