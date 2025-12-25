#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migration des produits depuis 'Productos tienda.xls(x)' vers la table 'productos'
Supporte les formats .xls (xlrd) et .xlsx (openpyxl)
Mapping des colonnes :
- NOMBRE (col 1) → categoria (BDD)
- TALLA (col 2) → talla (BDD)
- REFERENCIA (col 3) → nombre (BDD - nom du produit)
- PRECIO (col 4) → precio (BDD)
- IVA (col 5) → iva (BDD) - format: 4% → 4.00
- STOCK (col 6) → stock (BDD)
"""

import sys
import sqlite3
from pathlib import Path

# Essayer d'importer xlrd et openpyxl
try:
    import xlrd
    HAS_XLRD = True
except ImportError:
    HAS_XLRD = False

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

def parse_iva(iva_value):
    """Convertir IVA: 4% → 4.00, 0.04 → 4.00"""
    if iva_value is None or iva_value == '':
        return 21.0
    
    if isinstance(iva_value, (int, float)):
        if 0 < iva_value < 1:
            return round(iva_value * 100, 2)
        return round(float(iva_value), 2)
    
    if isinstance(iva_value, str):
        iva_str = iva_value.strip().replace('%', '').replace(',', '.')
        if iva_str == '':
            return 21.0
        try:
            iva_num = float(iva_str)
            if 0 < iva_num < 1:
                return round(iva_num * 100, 2)
            return round(iva_num, 2)
        except ValueError:
            return 21.0
    
    return 21.0

def read_excel_file(excel_path):
    """Lire un fichier Excel (.xls ou .xlsx) et retourner les données"""
    file_ext = Path(excel_path).suffix.lower()

    if file_ext == '.xls':
        if not HAS_XLRD:
            print("❌ xlrd n'est pas installé. Installez-le avec: pip install xlrd")
            return None

        # Lire avec xlrd
        workbook = xlrd.open_workbook(excel_path)
        sheet = workbook.sheet_by_index(0)

        # Convertir en format unifié
        data = []
        for row_idx in range(sheet.nrows):
            row = []
            for col_idx in range(sheet.ncols):
                row.append(sheet.cell_value(row_idx, col_idx))
            data.append(row)

        return data, sheet.nrows, sheet.ncols

    elif file_ext == '.xlsx':
        if not HAS_OPENPYXL:
            print("❌ openpyxl n'est pas installé. Installez-le avec: pip install openpyxl")
            return None

        # Lire avec openpyxl - NE PAS utiliser data_only=True car les valeurs peuvent être None
        # si le fichier n'a jamais été ouvert dans Excel
        workbook = openpyxl.load_workbook(excel_path, data_only=False)
        sheet = workbook.active

        # Convertir en format unifié
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(list(row))

        nrows = len(data)
        ncols = len(data[0]) if data else 0

        return data, nrows, ncols

    else:
        print(f"❌ Format de fichier non supporté: {file_ext}")
        return None

def migrate():
    """Migrer les produits depuis Excel vers productos"""
    # Chercher le fichier Excel (priorité à .xlsx puis .xls)
    excel_files = [
        'Productos tienda-1.xlsx',
        'Productos tienda.xlsx',
        'Productos tienda.xls'
    ]

    excel_path = None
    for file in excel_files:
        if Path(file).exists():
            excel_path = file
            break

    if not excel_path:
        print(f"❌ Aucun fichier Excel trouvé parmi: {', '.join(excel_files)}")
        return False

    db_path = 'base_de_datos/facturacion.db'

    print("\n" + "="*70)
    print(f"MIGRATION: {excel_path} → productos (base_de_datos/facturacion.db)")
    print("="*70)

    # Vérifications
    if not Path(db_path).exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        # Charger Excel
        print(f"\n📂 Chargement: {excel_path}")
        result = read_excel_file(excel_path)
        if not result:
            return False

        data, nrows, ncols = result
        print(f"   ✅ {nrows} lignes, {ncols} colonnes")

        # Connexion BDD
        print(f"\n💾 Connexion: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Supprimer la table products_shop si elle existe
        print("\n🗑️  Suppression de la table 'products_shop' si elle existe...")
        cursor.execute("DROP TABLE IF EXISTS products_shop")

        # Ajouter la colonne talla si elle n'existe pas
        print("🔧 Vérification de la colonne 'talla'...")
        cursor.execute("PRAGMA table_info(productos)")
        columns = [row[1] for row in cursor.fetchall()]
        if 'talla' not in columns:
            print("   ➕ Ajout de la colonne 'talla'...")
            cursor.execute("ALTER TABLE productos ADD COLUMN talla TEXT")
            conn.commit()
            print("   ✅ Colonne 'talla' ajoutée")
        else:
            print("   ✅ Colonne 'talla' existe déjà")

        # Vider les tables productos et stock
        print("🗑️  Suppression des données existantes dans 'productos' et 'stock'...")
        cursor.execute("DELETE FROM stock")
        cursor.execute("DELETE FROM productos")
        conn.commit()

        # Import
        print("\n📥 Importation...")
        imported = 0
        skipped = 0

        for row_idx in range(1, nrows):
            try:
                row = data[row_idx]

                # Lire colonnes
                col_nombre = row[0] if len(row) > 0 else None      # NOMBRE → categoria
                col_talla = row[1] if len(row) > 1 else None       # TALLA → talla
                col_referencia = row[2] if len(row) > 2 else None  # REFERENCIA → nombre
                col_precio = row[3] if len(row) > 3 else None      # PRECIO → precio
                col_iva = row[4] if len(row) > 4 else None         # IVA → iva
                col_stock = row[5] if len(row) > 5 else None       # STOCK → stock
                
                # Mapping
                categoria = str(col_nombre).strip() if col_nombre else None
                talla = str(col_talla).strip() if col_talla else None
                nombre = str(col_referencia).strip() if col_referencia else None

                # Validation
                if not nombre or nombre == '' or nombre == 'None':
                    skipped += 1
                    continue

                # Conversion robuste pour gérer les différents types de données
                # Prix
                try:
                    precio = float(col_precio) if col_precio is not None and col_precio != '' else 0.0
                except (ValueError, TypeError):
                    precio = 0.0

                # IVA
                iva = parse_iva(col_iva)

                # Stock - conversion robuste pour gérer int, float, string, None
                try:
                    if col_stock is None or col_stock == '':
                        stock = 0
                    elif isinstance(col_stock, (int, float)):
                        stock = int(col_stock)
                    else:
                        stock = int(float(str(col_stock).strip()))
                except (ValueError, TypeError):
                    stock = 0

                # Insert dans productos (sans stock_actual car géré dans table stock)
                cursor.execute("""
                    INSERT INTO productos (nombre, categoria, talla, precio, iva_recomendado,
                                         referencia, descripcion, imagen_path,
                                         fecha_creacion, fecha_actualizacion)
                    VALUES (?, ?, ?, ?, ?, NULL, '', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """, (nombre, categoria, talla, precio, iva))

                producto_id = cursor.lastrowid

                # Insert dans la table stock
                cursor.execute("""
                    INSERT INTO stock (producto_id, cantidad_disponible, fecha_actualizacion)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (producto_id, stock))

                imported += 1

                # Debug: afficher les 5 premiers produits avec leur stock
                if imported <= 5:
                    print(f"   🔍 Debug: {nombre[:30]:30} | Stock: {stock:3} (type: {type(col_stock).__name__}, valeur brute: {col_stock})")

                if imported % 20 == 0:
                    print(f"   ✅ {imported} produits...")
                
            except Exception as e:
                print(f"   ❌ Ligne {row_idx + 1}: {e}")
                skipped += 1
        
        # Premier commit pour sauvegarder les données
        conn.commit()
        print("\n🔍 Vérification post-commit...")

        # Vérification des stocks importés DANS LA MÊME TRANSACTION
        cursor.execute("SELECT COUNT(*) FROM stock WHERE cantidad_disponible > 0")
        stock_non_zero = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(cantidad_disponible) FROM stock")
        total_stock = cursor.fetchone()[0] or 0

        print(f"   📊 Vérification interne: {stock_non_zero} produits avec stock, total: {total_stock}")

        # Deuxième commit pour être sûr
        conn.commit()

        # Fermer la connexion
        conn.close()

        # Vérification EXTERNE après fermeture
        print("🔍 Vérification externe (nouvelle connexion)...")
        conn2 = sqlite3.connect(db_path)
        cursor2 = conn2.cursor()
        cursor2.execute("SELECT COUNT(*) FROM stock WHERE cantidad_disponible > 0")
        stock_non_zero_ext = cursor2.fetchone()[0]
        cursor2.execute("SELECT SUM(cantidad_disponible) FROM stock")
        total_stock_ext = cursor2.fetchone()[0] or 0
        conn2.close()

        print(f"   📊 Vérification externe: {stock_non_zero_ext} produits avec stock, total: {total_stock_ext}")

        # Vérification FINALE après un délai (pour debug)
        import time
        print("\n⏳ Attente de 2 secondes pour vérification finale...")
        time.sleep(2)

        conn3 = sqlite3.connect(db_path)
        cursor3 = conn3.cursor()
        cursor3.execute("SELECT COUNT(*) FROM stock WHERE cantidad_disponible > 0")
        stock_final = cursor3.fetchone()[0]
        cursor3.execute("SELECT SUM(cantidad_disponible) FROM stock")
        total_final = cursor3.fetchone()[0] or 0
        cursor3.close()
        conn3.close()

        print(f"   📊 Vérification FINALE: {stock_final} produits avec stock, total: {total_final}")

        if total_final == 0 and total_stock_ext > 0:
            print("\n⚠️  ALERTE: Les stocks ont été effacés entre la vérification externe et la vérification finale!")
            print("   Cela suggère qu'un autre processus modifie la base de données.")

        # Résumé
        print("\n" + "="*70)
        print("✅ MIGRATION TERMINÉE")
        print("="*70)
        print(f"   ✅ Importés: {imported}")
        print(f"   ⚠️  Ignorés: {skipped}")
        print(f"   📊 Total: {nrows - 1}")
        print(f"   📦 Produits avec stock > 0: {stock_non_zero}/{imported}")
        print(f"   📊 Stock total: {total_stock} unités")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)

