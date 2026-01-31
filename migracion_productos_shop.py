#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migration pour importer les produits depuis 'Productos tienda.xls'
vers la base de données SQLite de Facturación Fácil.
"""

import os
import sys
import sqlite3
from datetime import datetime

# Configuration
EXCEL_FILE = "Productos tienda.xls"
DB_PATH = "base_de_datos/facturacion.db"

def check_dependencies():
    """Vérifie que xlrd est installé"""
    try:
        import xlrd
        return xlrd
    except ImportError:
        print("❌ ERREUR: Le module 'xlrd' n'est pas installé.")
        print("   Installez-le avec: pip install xlrd")
        sys.exit(1)

def connect_db():
    """Connecte à la base de données SQLite"""
    try:
        # Vérifier que le répertoire existe
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # Activer WAL mode pour meilleure concurrence
        conn.execute("PRAGMA journal_mode=WAL")
        return conn
    except Exception as e:
        print(f"❌ ERREUR: Impossible de connecter à la base de données: {e}")
        sys.exit(1)

def init_tables(conn):
    """Initialise les tables nécessaires si elles n'existent pas"""
    cursor = conn.cursor()
    
    # Table productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            referencia TEXT UNIQUE,
            precio REAL NOT NULL,
            categoria TEXT,
            descripcion TEXT,
            imagen_path TEXT,
            iva_recomendado REAL DEFAULT 21.0,
            talla TEXT,
            sin_stock INTEGER DEFAULT 0,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table stock
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            producto_id INTEGER PRIMARY KEY,
            cantidad_disponible INTEGER DEFAULT 0,
            stock_minimo INTEGER DEFAULT 0,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    ''')
    
    conn.commit()
    print("✅ Tables vérifiées/initialisées")

def clean_value(value, default=""):
    """Nettoie une valeur du fichier Excel"""
    if value is None:
        return default
    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return default
    return value

def parse_price(value):
    """Parse un prix depuis le fichier Excel"""
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

def parse_iva(value):
    """Parse le pourcentage d'IVA"""
    if value is None or value == "":
        return 21.0  # IVA par défaut
    try:
        # Gérer le format 0.04 → 4%
        iva = float(value)
        if iva < 1:
            iva = iva * 100
        return iva
    except (ValueError, TypeError):
        return 21.0

def parse_stock(value):
    """Parse la quantité de stock"""
    if value is None or value == "":
        return 0
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return 0

def product_exists(cursor, referencia):
    """Vérifie si un produit avec cette référence existe déjà"""
    if not referencia:
        return False
    cursor.execute("SELECT id FROM productos WHERE referencia = ?", (referencia,))
    return cursor.fetchone() is not None

def migrate_products():
    """Fonction principale de migration"""
    print("=" * 60)
    print("MIGRATION DES PRODUITS DEPUIS EXCEL")
    print("=" * 60)
    print()
    
    # Vérifier que le fichier Excel existe
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ ERREUR: Fichier '{EXCEL_FILE}' non trouvé")
        print(f"   Chemin recherché: {os.path.abspath(EXCEL_FILE)}")
        return False
    
    print(f"📁 Fichier Excel: {EXCEL_FILE}")
    print(f"🗄️  Base de données: {DB_PATH}")
    print()
    
    # Importer xlrd
    xlrd = check_dependencies()
    
    # Connecter à la base de données
    conn = connect_db()
    cursor = conn.cursor()
    
    # Initialiser les tables
    init_tables(conn)
    
    # Ouvrir le fichier Excel
    try:
        workbook = xlrd.open_workbook(EXCEL_FILE)
        sheet = workbook.sheet_by_index(0)
    except Exception as e:
        print(f"❌ ERREUR: Impossible d'ouvrir le fichier Excel: {e}")
        return False
    
    print(f"📊 Feuille: {sheet.name}")
    print(f"   Lignes: {sheet.nrows}")
    print(f"   Colonnes: {sheet.ncols}")
    print()
    
    # Statistiques
    stats = {
        'total': 0,
        'imported': 0,
        'skipped': 0,
        'errors': 0,
        'empty': 0
    }
    
    # Parcourir les lignes (sauter l'en-tête)
    for row_idx in range(1, sheet.nrows):
        stats['total'] += 1
        
        # Lire les valeurs
        nombre = clean_value(sheet.cell_value(row_idx, 0))
        talla = clean_value(sheet.cell_value(row_idx, 1))
        referencia = clean_value(sheet.cell_value(row_idx, 2))
        precio = parse_price(sheet.cell_value(row_idx, 3))
        iva = parse_iva(sheet.cell_value(row_idx, 4))
        stock = parse_stock(sheet.cell_value(row_idx, 5))
        
        # Ignorer les lignes vides (sans nom ni référence)
        if not nombre and not referencia:
            stats['empty'] += 1
            continue
        
        # Si pas de nom mais une référence, utiliser la référence comme nom
        if not nombre and referencia:
            nombre = referencia
        
        # Vérifier si le produit existe déjà
        if product_exists(cursor, referencia):
            print(f"⏭️  Ignoré (existe déjà): {referencia}")
            stats['skipped'] += 1
            continue
        
        try:
            # Insérer le produit
            cursor.execute('''
                INSERT INTO productos (nombre, referencia, precio, categoria, 
                                      descripcion, imagen_path, iva_recomendado, talla)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nombre,
                referencia if referencia else None,  # Référence optionnelle
                precio,
                "General",  # Catégorie par défaut
                "",  # Description vide
                "",  # Pas d'image
                iva,
                talla if talla else None
            ))
            
            producto_id = cursor.lastrowid
            
            # Créer l'entrée dans la table stock
            cursor.execute('''
                INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(producto_id) DO UPDATE SET
                    cantidad_disponible = excluded.cantidad_disponible,
                    fecha_actualizacion = CURRENT_TIMESTAMP
            ''', (producto_id, stock))
            
            conn.commit()
            
            print(f"✅ Importé: {nombre[:40]:<40} | Ref: {referencia[:20]:<20} | Stock: {stock:>3}")
            stats['imported'] += 1
            
        except Exception as e:
            print(f"❌ Erreur ligne {row_idx + 1} ({nombre}): {e}")
            stats['errors'] += 1
            conn.rollback()
    
    # Fermer les connexions
    conn.close()
    
    # Afficher les statistiques
    print()
    print("=" * 60)
    print("RÉSULTATS DE LA MIGRATION")
    print("=" * 60)
    print(f"   Total lignes:     {stats['total']}")
    print(f"   ✅ Importés:      {stats['imported']}")
    print(f"   ⏭️  Ignorés (doublons): {stats['skipped']}")
    print(f"   ⚪ Vides:          {stats['empty']}")
    print(f"   ❌ Erreurs:        {stats['errors']}")
    print("=" * 60)
    
    return stats['errors'] == 0

if __name__ == "__main__":
    success = migrate_products()
    sys.exit(0 if success else 1)
