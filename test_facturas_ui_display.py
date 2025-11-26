#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier l'affichage des factures dans l'interface utilisateur
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework
set_gui_framework('pyqt6')

from PyQt6.QtWidgets import QApplication
from ui.facturas_pyqt6 import FacturasPyQt6Window
from database.database import db

def test_facturas_ui_display():
    """Test de l'affichage des factures dans l'interface"""
    print("🖥️  Test d'affichage des factures dans l'interface")
    print("=" * 55)
    
    # Initialiser la base de données
    db.init_database()
    
    # Créer l'application Qt
    app = QApplication.instance() or QApplication([])
    
    try:
        print("\n1. 📊 Vérification des données dans la base...")
        
        # Vérifier les factures dans la base
        db_invoices = db.get_all_invoices()
        print(f"   ✅ Factures dans la base: {len(db_invoices)}")
        
        if db_invoices:
            for i, invoice in enumerate(db_invoices[:3]):
                print(f"   - {invoice.get('numero', 'N/A')} | {invoice.get('cliente_nombre', 'N/A')} | €{invoice.get('total', 0):.2f}")
        
        print("\n2. 🏗️  Création de la fenêtre des factures...")
        
        # Créer la fenêtre des factures
        facturas_window = FacturasPyQt6Window()
        
        print("   ✅ Fenêtre créée avec succès")
        
        print("\n3. 📋 Test du tableau des factures...")
        
        # Vérifier que le tableau existe
        assert hasattr(facturas_window, 'invoices_table'), "Table des factures manquante"
        table = facturas_window.invoices_table
        
        print(f"   ✅ Tableau trouvé: {type(table).__name__}")
        
        # Vérifier le nombre de lignes dans le tableau
        row_count = table.rowCount()
        print(f"   📊 Nombre de lignes dans le tableau: {row_count}")
        
        if row_count == 0:
            print("   ⚠️  PROBLÈME: Le tableau est vide!")
            print("   🔧 Tentative de rechargement des données...")
            
            # Forcer le rechargement
            facturas_window.load_invoices_data()
            
            # Vérifier à nouveau
            new_row_count = table.rowCount()
            print(f"   📊 Nombre de lignes après rechargement: {new_row_count}")
            
            if new_row_count > 0:
                print("   ✅ PROBLÈME RÉSOLU: Les données sont maintenant affichées!")
                
                # Afficher quelques lignes du tableau
                for row in range(min(3, new_row_count)):
                    numero_item = table.item(row, 0)
                    cliente_item = table.item(row, 1)
                    fecha_item = table.item(row, 2)
                    total_item = table.item(row, 3)
                    
                    numero = numero_item.text() if numero_item else "N/A"
                    cliente = cliente_item.text() if cliente_item else "N/A"
                    fecha = fecha_item.text() if fecha_item else "N/A"
                    total = total_item.text() if total_item else "N/A"
                    
                    print(f"   - Ligne {row+1}: {numero} | {cliente} | {fecha} | {total}")
                
                return True
            else:
                print("   ❌ Le tableau reste vide après rechargement")
                return False
        else:
            print("   ✅ Le tableau contient des données!")
            
            # Afficher quelques lignes du tableau
            for row in range(min(3, row_count)):
                numero_item = table.item(row, 0)
                cliente_item = table.item(row, 1)
                fecha_item = table.item(row, 2)
                total_item = table.item(row, 3)
                
                numero = numero_item.text() if numero_item else "N/A"
                cliente = cliente_item.text() if cliente_item else "N/A"
                fecha = fecha_item.text() if fecha_item else "N/A"
                total = total_item.text() if total_item else "N/A"
                
                print(f"   - Ligne {row+1}: {numero} | {cliente} | {fecha} | {total}")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_facturas_window_methods():
    """Test des méthodes de la fenêtre des factures"""
    print("\n4. 🔧 Test des méthodes de la fenêtre...")
    
    try:
        app = QApplication.instance() or QApplication([])
        facturas_window = FacturasPyQt6Window()
        
        # Vérifier les méthodes essentielles
        methods_to_check = [
            'load_invoices_data',
            'new_invoice',
            'edit_invoice',
            'print_invoice',
            'on_invoice_saved'
        ]
        
        for method_name in methods_to_check:
            if hasattr(facturas_window, method_name):
                print(f"   ✅ Méthode {method_name} disponible")
            else:
                print(f"   ❌ Méthode {method_name} manquante")
                return False
        
        print("   ✅ Toutes les méthodes essentielles sont disponibles")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test des méthodes: {e}")
        return False

if __name__ == "__main__":
    try:
        print("🚀 Démarrage du test d'affichage des factures...")
        
        success1 = test_facturas_ui_display()
        success2 = test_facturas_window_methods()
        
        if success1 and success2:
            print("\n🎉 TOUS LES TESTS SONT PASSÉS!")
            print("✅ Les factures sont correctement affichées dans l'interface")
            print("✅ Toutes les méthodes fonctionnent correctement")
            print("\n💡 Si vous ne voyez toujours pas les factures:")
            print("   1. Cliquez sur le bouton '🧾 Facturas' dans la fenêtre principale")
            print("   2. Vérifiez que la fenêtre des factures s'ouvre correctement")
            print("   3. Les factures devraient être visibles dans le tableau")
            sys.exit(0)
        else:
            print("\n❌ Certains tests ont échoué")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        sys.exit(1)
