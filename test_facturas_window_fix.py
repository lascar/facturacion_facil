#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que la correction de la fenêtre des factures fonctionne
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import set_gui_framework
set_gui_framework('pyqt6')

from PyQt6.QtWidgets import QApplication
from ui.main_window_pyqt6 import MainWindowPyQt6
from database.database import db

def test_facturas_window_fix():
    """Test de la correction de la fenêtre des factures"""
    print("🔧 Test de la correction de la fenêtre des factures")
    print("=" * 55)
    
    # Initialiser la base de données
    db.init_database()
    
    # Créer l'application Qt
    app = QApplication.instance() or QApplication([])
    
    try:
        print("\n1. 📊 Vérification des factures dans la base...")
        
        # Vérifier les factures dans la base
        db_invoices = db.get_all_invoices()
        print(f"   ✅ Factures dans la base: {len(db_invoices)}")
        
        if db_invoices:
            for i, invoice in enumerate(db_invoices[:3]):
                print(f"   - {invoice.get('numero', 'N/A')} | {invoice.get('cliente_nombre', 'N/A')} | €{invoice.get('total', 0):.2f}")
        
        print("\n2. 🏗️  Test de la fenêtre principale...")
        
        # Créer la fenêtre principale
        main_window = MainWindowPyQt6()
        
        print("   ✅ Fenêtre principale créée")
        
        # Vérifier que la méthode open_facturas existe
        assert hasattr(main_window, 'open_facturas'), "Méthode open_facturas manquante"
        print("   ✅ Méthode open_facturas disponible")
        
        print("\n3. 🧾 Test d'ouverture de la fenêtre des factures...")
        
        # Simuler le clic sur le bouton facturas
        main_window.open_facturas()
        
        # Vérifier que la fenêtre des factures a été créée
        assert main_window.facturas_window is not None, "Fenêtre des factures non créée"
        print("   ✅ Fenêtre des factures créée")
        
        # Vérifier le type de la fenêtre
        from ui.facturas_pyqt6 import FacturasPyQt6Window
        assert isinstance(main_window.facturas_window, FacturasPyQt6Window), "Mauvais type de fenêtre"
        print("   ✅ Type de fenêtre correct: FacturasPyQt6Window")
        
        # Vérifier que la fenêtre contient le tableau des factures
        facturas_window = main_window.facturas_window
        assert hasattr(facturas_window, 'invoices_table'), "Tableau des factures manquant"
        print("   ✅ Tableau des factures présent")
        
        # Vérifier le contenu du tableau
        table = facturas_window.invoices_table
        row_count = table.rowCount()
        print(f"   📊 Nombre de lignes dans le tableau: {row_count}")
        
        if row_count > 0:
            print("   ✅ Le tableau contient des données!")
            
            # Afficher quelques lignes
            for row in range(min(3, row_count)):
                numero_item = table.item(row, 0)
                fecha_item = table.item(row, 1)
                cliente_item = table.item(row, 2)
                total_item = table.item(row, 3)
                
                numero = numero_item.text() if numero_item else "N/A"
                fecha = fecha_item.text() if fecha_item else "N/A"
                cliente = cliente_item.text() if cliente_item else "N/A"
                total = total_item.text() if total_item else "N/A"
                
                print(f"   - Ligne {row+1}: {numero} | {fecha} | {cliente} | {total}")
            
            print("\n🎉 PROBLÈME RÉSOLU!")
            print("✅ La fenêtre des factures affiche maintenant correctement les factures")
            print("✅ Vous devriez maintenant voir toutes vos factures créées")
            return True
        else:
            print("   ⚠️  Le tableau est encore vide")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_facturas_window_fix()
        
        if success:
            print("\n🚀 CORRECTION RÉUSSIE!")
            print("💡 Instructions pour voir vos factures:")
            print("   1. Lancez l'application: python main.py")
            print("   2. Cliquez sur le bouton '🧾 Facturas'")
            print("   3. Vous devriez maintenant voir toutes vos factures!")
            sys.exit(0)
        else:
            print("\n❌ La correction n'a pas complètement résolu le problème")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        sys.exit(1)
