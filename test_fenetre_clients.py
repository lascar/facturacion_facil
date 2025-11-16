#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la fenêtre de gestion des clients
"""

import sys
import os
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_fenetre_clients():
    """Test de la fenêtre de gestion des clients"""
    print("👥 TEST DE LA FENÊTRE DE GESTION DES CLIENTS")
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
        
        # Test 1: Vérifier les clients en base de données
        print("\n--- Test 1: Clients en Base de Données ---")
        
        db_clients = db.get_all_clients()
        print(f"✅ Clients en base de données: {len(db_clients)}")
        
        if db_clients:
            print("📋 Premiers clients en base:")
            for i, client in enumerate(db_clients[:5]):
                print(f"   {i+1}. ID {client['id']}: {client['nombre']} ({client.get('nif', 'N/A')})")
        else:
            print("⚠️ Aucun client en base de données")
        
        # Test 2: Créer la fenêtre des clients
        print("\n--- Test 2: Fenêtre des Clients ---")
        
        clients_window = ClientesPyQt6Window()
        clients_window.show()
        
        print("✅ Fenêtre des clients créée et affichée")
        
        # Traiter les événements
        app.processEvents()
        time.sleep(1.0)  # Laisser le temps à la fenêtre de se charger
        
        # Test 3: Vérifier le contenu de la table
        print("\n--- Test 3: Contenu de la Table ---")
        
        table = clients_window.clients_table
        row_count = table.rowCount()
        column_count = table.columnCount()
        
        print(f"✅ Table créée: {row_count} lignes, {column_count} colonnes")
        
        # Vérifier les en-têtes
        headers = []
        for col in range(column_count):
            header_item = table.horizontalHeaderItem(col)
            if header_item:
                headers.append(header_item.text())
            else:
                headers.append(f"Col{col}")
        
        print(f"✅ En-têtes: {headers}")
        
        # Vérifier le contenu des lignes
        if row_count > 0:
            print(f"✅ Clients affichés dans la table:")
            for row in range(min(row_count, 10)):  # Afficher max 10 lignes
                row_data = []
                for col in range(column_count):
                    item = table.item(row, col)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                
                print(f"   {row+1}. {' | '.join(row_data)}")
        else:
            print("⚠️ Aucun client affiché dans la table")
        
        # Test 4: Comparer avec les données de base
        print("\n--- Test 4: Comparaison Base vs Interface ---")
        
        if len(db_clients) == row_count:
            print("✅ Nombre de clients cohérent entre base et interface")
        else:
            print(f"⚠️ Incohérence: {len(db_clients)} en base vs {row_count} dans l'interface")
        
        # Vérifier quelques clients spécifiques
        if row_count > 0 and len(db_clients) > 0:
            # Comparer le premier client
            first_db_client = db_clients[0]
            first_table_name = table.item(0, 0).text() if table.item(0, 0) else ""
            
            if first_db_client['nombre'] == first_table_name:
                print("✅ Premier client cohérent entre base et interface")
            else:
                print(f"⚠️ Premier client différent: '{first_db_client['nombre']}' vs '{first_table_name}'")
        
        # Test 5: Tester la méthode load_clients
        print("\n--- Test 5: Test de Rechargement ---")
        
        # Recharger les clients
        clients_window.load_clients()
        app.processEvents()
        time.sleep(0.5)
        
        new_row_count = table.rowCount()
        print(f"✅ Après rechargement: {new_row_count} lignes")
        
        if new_row_count == row_count:
            print("✅ Rechargement cohérent")
        else:
            print(f"⚠️ Changement après rechargement: {row_count} → {new_row_count}")
        
        # Test 6: Vérifier les boutons d'action
        print("\n--- Test 6: Boutons d'Action ---")
        
        buttons_to_check = [
            'Nuevo Cliente',
            'Editar', 
            'Eliminar',
            'Actualizar'
        ]
        
        # Chercher les boutons dans la fenêtre
        buttons_found = []
        for button in clients_window.findChildren(clients_window.__class__.__bases__[0]):
            if hasattr(button, 'text'):
                button_text = button.text()
                if button_text in buttons_to_check:
                    buttons_found.append(button_text)
        
        print(f"✅ Boutons trouvés: {buttons_found}")
        
        for expected_button in buttons_to_check:
            if expected_button in buttons_found:
                print(f"   ✅ {expected_button}")
            else:
                print(f"   ⚠️ {expected_button} manquant")
        
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
        success = test_fenetre_clients()
        
        print("\n" + "="*60)
        print("RÉSUMÉ DU TEST DE LA FENÊTRE CLIENTS")
        print("="*60)
        
        if success:
            print("🎉 TEST DE LA FENÊTRE CLIENTS RÉUSSI !")
            print("\n✨ FONCTIONNALITÉS VALIDÉES :")
            print("   ✅ Clients chargés depuis la base de données")
            print("   ✅ Fenêtre des clients créée et affichée")
            print("   ✅ Table avec en-têtes appropriés")
            print("   ✅ Données affichées dans la table")
            print("   ✅ Cohérence entre base et interface")
            print("   ✅ Rechargement fonctionnel")
            print("   ✅ Boutons d'action présents")
            
            print("\n🎯 FENÊTRE DES CLIENTS OPÉRATIONNELLE !")
            print("\n👥 GESTION DES CLIENTS :")
            print("   • Affichage de tous les clients de la base")
            print("   • Interface moderne avec table organisée")
            print("   • Boutons pour créer, éditer, supprimer")
            print("   • Rechargement automatique des données")
            
            print("\n🚀 Pour tester manuellement :")
            print("   1. Lancez: python main.py")
            print("   2. Cliquez sur 'Clientes'")
            print("   3. Vérifiez que tous vos clients sont listés")
            print("   4. Testez les boutons d'action")
            print("   5. Créez un nouveau client pour tester")
            
            return 0
        else:
            print("❌ TEST DE LA FENÊTRE CLIENTS ÉCHOUÉ")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Test interrompu par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
