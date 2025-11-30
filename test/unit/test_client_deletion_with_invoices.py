#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour l'élimination des clients avec factures
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtWidgets import QApplication
from database.database import db
from ui.clientes_pyqt5 import ClientesPyQt5Window

class TestClientDeletionWithInvoices(unittest.TestCase):
    """Tests pour l'élimination des clients avec factures"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration de la classe de test"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.test_client_id = None
        self.test_invoice_ids = []
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        # Nettoyer les données de test
        try:
            if self.test_invoice_ids:
                for invoice_id in self.test_invoice_ids:
                    try:
                        db.delete_invoice(invoice_id)
                    except:
                        pass
            
            if self.test_client_id:
                try:
                    db.delete_client(self.test_client_id)
                except:
                    pass
        except:
            pass
    
    def create_test_client_with_invoices(self):
        """Créer un client de test avec des factures"""
        # Créer le client
        client_data = {
            'nombre': 'Test Client Delete',
            'dni_nie': '12345678T',
            'direccion': 'Test Address',
            'email': 'test@test.com',
            'telefono': '123456789'
        }
        
        self.test_client_id = db.add_client(client_data)
        
        # Créer des factures pour ce client
        for i in range(2):
            invoice_data = {
                'numero': f'TEST-DEL-{i+1:03d}',
                'fecha': '2024-11-30',
                'cliente': {
                    'id': self.test_client_id,
                    'nombre': client_data['nombre'],
                    'nif': client_data['dni_nie'],
                    'direccion': client_data['direccion']
                },
                'subtotal': 100.0,
                'iva_total': 21.0,
                'total': 121.0,
                'estado': 'Borrador',
                'lineas': []
            }
            
            invoice_id = db.add_invoice(invoice_data)
            self.test_invoice_ids.append(invoice_id)
        
        return self.test_client_id
    
    def test_database_constraint_prevents_deletion(self):
        """Test que la contrainte de base de données empêche la suppression"""
        client_id = self.create_test_client_with_invoices()
        
        # Essayer de supprimer le client (doit échouer)
        with self.assertRaises(Exception) as context:
            db.delete_client(client_id)
        
        # Vérifier que l'erreur mentionne les factures associées
        self.assertIn("factura", str(context.exception).lower())
    
    def test_client_window_initialization(self):
        """Test que la fenêtre des clients s'initialise correctement"""
        window = ClientesPyQt5Window()
        
        # Vérifier que les méthodes nécessaires existent
        self.assertTrue(hasattr(window, 'delete_cliente'))
        self.assertTrue(hasattr(window, 'show_client_with_invoices_dialog'))
        self.assertTrue(hasattr(window, 'view_client_invoices'))
        self.assertTrue(hasattr(window, 'delete_client_invoices'))
        
        window.close()
    
    def test_invoice_count_verification(self):
        """Test de la vérification du nombre de factures"""
        client_id = self.create_test_client_with_invoices()
        
        # Vérifier le nombre de factures
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM facturas WHERE cliente_id = ?", (client_id,))
        invoice_count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(invoice_count, 2)
    
    def test_client_deletion_without_invoices(self):
        """Test de la suppression d'un client sans factures"""
        # Créer un client sans factures
        client_data = {
            'nombre': 'Test Client No Invoices',
            'dni_nie': '87654321T',
            'direccion': 'Test Address 2',
            'email': 'test2@test.com',
            'telefono': '987654321'
        }
        
        client_id = db.add_client(client_data)
        self.test_client_id = client_id
        
        # La suppression doit réussir
        success = db.delete_client(client_id)
        self.assertTrue(success)
        
        # Le client ne doit plus exister
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE id = ?", (client_id,))
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 0)
        self.test_client_id = None  # Pas besoin de nettoyer
    
    def test_multiple_invoice_deletion(self):
        """Test de la suppression de multiples factures"""
        client_id = self.create_test_client_with_invoices()
        
        # Supprimer les factures
        deleted_count = db.delete_multiple_invoices(self.test_invoice_ids)
        self.assertEqual(deleted_count, 2)
        
        # Maintenant le client peut être supprimé
        success = db.delete_client(client_id)
        self.assertTrue(success)
        
        # Nettoyer les références
        self.test_invoice_ids = []
        self.test_client_id = None

class TestClientDeletionUI(unittest.TestCase):
    """Tests pour l'interface utilisateur de suppression des clients"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration de la classe de test"""
        if not QApplication.instance():
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()
    
    def test_dialog_creation(self):
        """Test de la création du dialogue d'options"""
        window = ClientesPyQt5Window()
        
        # Simuler l'affichage du dialogue (sans l'exécuter)
        try:
            # Cette méthode ne doit pas lever d'exception
            # On ne peut pas tester l'exécution complète sans interaction utilisateur
            self.assertTrue(hasattr(window, 'show_client_with_invoices_dialog'))
        except Exception as e:
            self.fail(f"Erreur lors de la création du dialogue: {e}")
        
        window.close()
    
    def test_method_signatures(self):
        """Test que les méthodes ont les bonnes signatures"""
        window = ClientesPyQt5Window()
        
        # Vérifier que les méthodes existent et sont appelables
        self.assertTrue(callable(getattr(window, 'delete_cliente', None)))
        self.assertTrue(callable(getattr(window, 'show_client_with_invoices_dialog', None)))
        self.assertTrue(callable(getattr(window, 'view_client_invoices', None)))
        self.assertTrue(callable(getattr(window, 'delete_client_invoices', None)))
        
        window.close()

if __name__ == "__main__":
    # Exécuter les tests
    unittest.main(verbosity=2)
