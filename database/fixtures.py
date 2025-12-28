#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixtures pour les tests - Données de test standardisées
"""

import sqlite3
from datetime import datetime, timedelta
from database.database import Database

class TestFixtures:
    """Gestionnaire de fixtures pour les tests"""

    def __init__(self, db_path=None):
        self.db_path = db_path
        self.db_improved = Database(db_path) if db_path else Database()
    
    def get_products_fixtures(self):
        """Retourne les données des 3 produits de test"""
        return [
            {
                'nombre': 'Laptop Dell Inspiron',
                'referencia': 'DELL001',
                'precio': 899.99,
                'categoria': 'Informatique',
                'descripcion': 'Ordinateur portable Dell Inspiron 15 pouces',
                'stock_actual': 25
            },
            {
                'nombre': 'Souris Logitech MX',
                'referencia': 'LOG001',
                'precio': 79.50,
                'categoria': 'Accessoires',
                'descripcion': 'Souris sans fil haute précision',
                'stock_actual': 150
            },
            {
                'nombre': 'Clavier Mécanique RGB',
                'referencia': 'KEY001',
                'precio': 129.99,
                'categoria': 'Accessoires',
                'descripcion': 'Clavier mécanique avec rétroéclairage RGB',
                'stock_actual': 75
            }
        ]
    
    def get_clients_fixtures(self):
        """Retourne les données des 3 clients de test"""
        return [
            {
                'nombre': 'Empresa Tech Solutions',
                'email': 'contact@techsolutions.com',
                'telefono': '+33 1 23 45 67 89',
                'direccion': '123 Avenue des Champs-Élysées, 75008 Paris',
                'nif': 'FR12345678901'
            },
            {
                'nombre': 'Boutique Informatique Plus',
                'email': 'info@infoplus.fr',
                'telefono': '+33 4 56 78 90 12',
                'direccion': '456 Rue de la République, 69002 Lyon',
                'nif': 'FR98765432109'
            },
            {
                'nombre': 'StartUp Innovation Lab',
                'email': 'hello@innovlab.com',
                'telefono': '+33 5 67 89 01 23',
                'direccion': '789 Boulevard Saint-Germain, 75006 Paris',
                'nif': 'FR11223344556'
            }
        ]
    
    def get_invoices_fixtures(self):
        """Retourne les données des 3 factures de test"""
        base_date = datetime.now() - timedelta(days=30)
        
        return [
            {
                'client_id': 1,  # Sera remplacé par l'ID réel
                'fecha': base_date.strftime('%Y-%m-%d'),
                'numero': 'FAC-2024-001',
                'estado': 'Enviada',
                'items': [
                    {'product_id': 1, 'cantidad': 2, 'precio_unitario': 899.99}  # 2 Laptops
                ]
            },
            {
                'client_id': 2,
                'fecha': (base_date + timedelta(days=5)).strftime('%Y-%m-%d'),
                'numero': 'FAC-2024-002',
                'estado': 'Pagada',
                'items': [
                    {'product_id': 2, 'cantidad': 5, 'precio_unitario': 79.50},   # 5 Souris
                    {'product_id': 3, 'cantidad': 3, 'precio_unitario': 129.99}  # 3 Claviers
                ]
            },
            {
                'client_id': 3,
                'fecha': (base_date + timedelta(days=10)).strftime('%Y-%m-%d'),
                'numero': 'FAC-2024-003',
                'estado': 'Borrador',
                'items': [
                    {'product_id': 1, 'cantidad': 1, 'precio_unitario': 899.99},  # 1 Laptop
                    {'product_id': 2, 'cantidad': 2, 'precio_unitario': 79.50},   # 2 Souris
                    {'product_id': 3, 'cantidad': 1, 'precio_unitario': 129.99}  # 1 Clavier
                ]
            }
        ]
    
    def create_fixtures(self):
        """Crée toutes les fixtures dans la base de données"""
        print("📦 Création des fixtures de test...")

        # 1. Créer les produits (vérifier si existent déjà)
        print("   Création des produits...")
        product_ids = []
        for product_data in self.get_products_fixtures():
            # Vérifier si le produit existe déjà par référence
            existing_products = self.db_improved.get_all_products()
            existing_product = next(
                (p for p in existing_products if p.get('referencia') == product_data['referencia']),
                None
            )

            if existing_product:
                product_id = existing_product['id']
                print(f"   ♻️  Produit existant réutilisé: {product_data['nombre']} (ID: {product_id})")
            else:
                product_id = self.db_improved.add_product(product_data)
                print(f"   ✅ Produit créé: {product_data['nombre']} (ID: {product_id})")

            product_ids.append(product_id)

        # 2. Créer les clients (vérifier si existent déjà)
        print("   Création des clients...")
        client_ids = []
        for client_data in self.get_clients_fixtures():
            # Vérifier si le client existe déjà par email
            existing_clients = self.db_improved.get_all_clients()
            existing_client = next(
                (c for c in existing_clients if c.get('email') == client_data['email']),
                None
            )

            if existing_client:
                client_id = existing_client['id']
                print(f"   ♻️  Client existant réutilisé: {client_data['nombre']} (ID: {client_id})")
            else:
                client_id = self.db_improved.add_client(client_data)
                print(f"   ✅ Client créé: {client_data['nombre']} (ID: {client_id})")

            client_ids.append(client_id)

        # 3. Créer les factures (version simplifiée avec SQL direct)
        print("   Création des factures...")
        invoice_ids = []
        invoices_data = self.get_invoices_fixtures()

        if self.db_path:
            conn = sqlite3.connect(self.db_path)
        else:
            conn = self.db_improved.get_connection()

        cursor = conn.cursor()

        try:
            for i, invoice_data in enumerate(invoices_data):
                # Remplacer les IDs par les vrais IDs
                client_id = client_ids[i]

                # Calculer les totaux
                subtotal = sum(item['cantidad'] * item['precio_unitario'] for item in invoice_data['items'])
                iva_total = subtotal * 0.21  # 21% IVA
                total = subtotal + iva_total

                # Créer la facture
                cursor.execute("""
                    INSERT INTO facturas (numero_factura, fecha_factura, cliente_id, nombre_cliente,
                                        subtotal, total_iva, total_factura, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    invoice_data['numero'],
                    invoice_data['fecha'],
                    client_id,
                    self.get_clients_fixtures()[i]['nombre'],
                    subtotal,
                    iva_total,
                    total,
                    invoice_data['estado']
                ))

                invoice_id = cursor.lastrowid

                # Ajouter les items
                for item in invoice_data['items']:
                    product_id = product_ids[item['product_id'] - 1]  # Ajuster l'index
                    product_data = self.get_products_fixtures()[item['product_id'] - 1]

                    # Calculer les montants
                    cantidad = item['cantidad']
                    precio_unitario = item['precio_unitario']
                    iva_aplicado = 21.0
                    descuento = 0.0
                    subtotal = cantidad * precio_unitario
                    descuento_amount = subtotal * (descuento / 100)
                    subtotal_con_descuento = subtotal - descuento_amount
                    iva_amount = subtotal_con_descuento * (iva_aplicado / 100)
                    total = subtotal_con_descuento + iva_amount

                    cursor.execute("""
                        INSERT INTO factura_items (factura_id, producto_id, cantidad, precio_unitario,
                                                 iva_aplicado, descuento, subtotal, descuento_amount,
                                                 iva_amount, total)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        invoice_id,
                        product_id,
                        cantidad,
                        precio_unitario,
                        iva_aplicado,
                        descuento,
                        subtotal,
                        descuento_amount,
                        iva_amount,
                        total
                    ))

                invoice_ids.append(invoice_id)
                print(f"   ✅ Facture créée: {invoice_data['numero']} (ID: {invoice_id})")

            conn.commit()

        finally:
            if self.db_path:  # Si c'est une base de test, fermer la connexion
                conn.close()

        print("   🎉 Fixtures créées avec succès !")

        return {
            'product_ids': product_ids,
            'client_ids': client_ids,
            'invoice_ids': invoice_ids
        }
    
    def get_fixtures_summary(self):
        """Retourne un résumé des fixtures"""
        products = self.db_improved.get_all_products()

        # Obtenir les clients avec SQL direct
        if self.db_path:
            conn = sqlite3.connect(self.db_path)
        else:
            conn = self.db_improved.get_connection()

        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM clientes")
            clients = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

            cursor.execute("SELECT * FROM facturas")
            invoices = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

        finally:
            if self.db_path:
                conn.close()

        return {
            'products_count': len(products),
            'clients_count': len(clients),
            'invoices_count': len(invoices),
            'products': products,
            'clients': clients,
            'invoices': invoices
        }
    
    def reset_to_fixtures(self):
        """Remet la base de données à l'état initial des fixtures"""
        print("🔄 Remise à l'état initial des fixtures...")
        
        # Nettoyer toutes les données
        self.clear_all_data()
        
        # Recréer les fixtures
        return self.create_fixtures()
    
    def clear_all_data(self):
        """Nettoie toutes les données de test"""
        if self.db_path:
            conn = sqlite3.connect(self.db_path)
        else:
            conn = self.db_improved.get_connection()
        
        cursor = conn.cursor()
        
        # Désactiver les contraintes de clés étrangères temporairement
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        # Supprimer dans l'ordre inverse des dépendances
        tables_to_clear = [
            'factura_items',
            'facturas', 
            'stock_movements',
            'stock',
            'productos',
            'clientes'
        ]
        
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table}")
                # Remettre l'auto-increment à 1
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
            except sqlite3.OperationalError:
                # Table n'existe pas, continuer
                pass
        
        # Réactiver les contraintes
        cursor.execute("PRAGMA foreign_keys = ON")
        
        conn.commit()
        if not self.db_path:  # Si c'est la connexion par défaut, ne pas la fermer
            conn.close()
        
        print("   🧹 Données nettoyées")
