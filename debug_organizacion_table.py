#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug de la structure de la table organizacion
"""

import os
import sys
import sqlite3

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_organizacion_table():
    """Debug de la structure de la table organizacion"""
    print("🔍 Debug de la table organizacion")
    print("=" * 50)
    
    try:
        # Se connecter à la base de données
        db_path = "facturacion.db"
        if not os.path.exists(db_path):
            print(f"❌ Base de données non trouvée: {db_path}")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n1. Structure de la table organizacion:")
        cursor.execute("PRAGMA table_info(organizacion)")
        columns = cursor.fetchall()
        
        print("   Index | Nom                        | Type      | NotNull | Default | PK")
        print("   ------|----------------------------|-----------|---------|---------|---")
        for col in columns:
            print(f"   {col[0]:5} | {col[1]:26} | {col[2]:9} | {col[3]:7} | {str(col[4]):7} | {col[5]}")
        
        print(f"\n   Total colonnes: {len(columns)}")
        
        print("\n2. Données actuelles:")
        cursor.execute("SELECT * FROM organizacion WHERE id=1")
        row = cursor.fetchone()
        
        if row:
            print("   Index | Valeur")
            print("   ------|--------------------------------------------------")
            for i, value in enumerate(row):
                column_name = columns[i][1] if i < len(columns) else f"col_{i}"
                print(f"   {i:5} | {column_name:26} = {str(value)[:50]}")
        else:
            print("   ❌ Aucune donnée trouvée")
        
        print("\n3. Analyse du problème:")
        if row and len(row) > 9:
            directorio_pdf_value = row[9]
            print(f"   directorio_descargas_pdf (index 9) = '{directorio_pdf_value}'")
            
            if directorio_pdf_value and "2025-12-07" in str(directorio_pdf_value):
                print("   ⚠️  PROBLÈME DÉTECTÉ: La valeur ressemble à une date!")
                print("   💡 Il y a probablement un décalage dans l'ordre des colonnes")
                
                # Vérifier si fecha_actualizacion est à l'index 9
                if len(columns) > 11:
                    fecha_col = columns[11]
                    if fecha_col[1] == 'fecha_actualizacion':
                        print(f"   🔍 fecha_actualizacion devrait être à l'index 11, pas 9")
        
        print("\n4. Ordre attendu des colonnes:")
        expected_order = [
            "id", "nombre", "direccion", "telefono", "email", "cif", 
            "logo_path", "directorio_imagenes_defecto", "numero_factura_inicial",
            "directorio_descargas_pdf", "visor_pdf_personalizado", "fecha_actualizacion"
        ]
        
        print("   Index | Attendu                    | Actuel")
        print("   ------|----------------------------|----------------------------")
        for i, expected in enumerate(expected_order):
            actual = columns[i][1] if i < len(columns) else "MANQUANT"
            status = "✅" if expected == actual else "❌"
            print(f"   {i:5} | {expected:26} | {actual:26} {status}")
        
        conn.close()
        
        print("\n5. Solution recommandée:")
        if any(expected_order[i] != (columns[i][1] if i < len(columns) else "") for i in range(len(expected_order))):
            print("   🔧 La structure de la table doit être corrigée")
            print("   💡 Exécuter une migration pour réorganiser les colonnes")
        else:
            print("   ✅ La structure de la table est correcte")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du debug: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_organizacion_table()
    sys.exit(0 if success else 1)
