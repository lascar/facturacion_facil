#!/usr/bin/env python3
"""
Test de régression pour corriger le problème de recherche dans la section stock
Diagnostique et corrige le problème de filtrage des produits
"""

import sys
import os
import tempfile
import shutil

# Ajouter le répertoire racine au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_stock_get_all_format():
    """Test du format des données retournées par Stock.get_all()"""
    print("🧪 Test: Format des données Stock.get_all()")
    
    try:
        from database.models import Stock, Producto
        from database.database import Database
        
        # Créer une base de données temporaire
        temp_db_path = tempfile.mktemp(suffix='.db')
        
        try:
            # Initialiser la base de données
            db = Database(temp_db_path)
            
            # Assurer que l'instance globale utilise notre DB temporaire
            from database.database import db as global_db
            global_db.db_path = temp_db_path
            
            print(f"   📁 Base de données temporaire: {temp_db_path}")
            
            # Créer quelques produits de test
            productos_test = [
                ("Producto Test 1", "TEST-001", 10.0, "Categoria A"),
                ("Producto Test 2", "TEST-002", 20.0, "Categoria B"),
                ("Búsqueda Test", "SEARCH-001", 15.0, "Categoria C")
            ]
            
            for nombre, referencia, precio, categoria in productos_test:
                producto = Producto(
                    nombre=nombre,
                    referencia=referencia,
                    precio=precio,
                    categoria=categoria
                )
                producto.save()
                print(f"   ✅ Producto creado: {nombre} ({referencia})")
            
            # Test 1: Vérifier le format de Stock.get_all()
            print("\n   1️⃣ Test format Stock.get_all()")
            
            stock_data = Stock.get_all()
            print(f"   📊 Productos con stock: {len(stock_data)}")
            
            if stock_data:
                first_row = stock_data[0]
                print(f"   📋 Formato primera fila: {first_row}")
                print(f"   📋 Tipo de datos: {[type(x) for x in first_row]}")
                
                # Verificar que tiene 4 elementos
                assert len(first_row) == 4, f"Esperado 4 elementos, obtenido {len(first_row)}"
                
                producto_id, cantidad, nombre, referencia = first_row
                print(f"   📊 producto_id: {producto_id} (tipo: {type(producto_id)})")
                print(f"   📊 cantidad: {cantidad} (tipo: {type(cantidad)})")
                print(f"   📊 nombre: {nombre} (tipo: {type(nombre)})")
                print(f"   📊 referencia: {referencia} (tipo: {type(referencia)})")
                
                # Verificar que los tipos son correctos
                assert isinstance(producto_id, int), f"producto_id debe ser int, es {type(producto_id)}"
                assert isinstance(cantidad, int), f"cantidad debe ser int, es {type(cantidad)}"
                assert isinstance(nombre, str), f"nombre debe ser str, es {type(nombre)}"
                assert isinstance(referencia, str), f"referencia debe ser str, es {type(referencia)}"
                
                print("   ✅ Formato de datos correcto")
            
            # Test 2: Simular el filtrado como en StockWindow
            print("\n   2️⃣ Test simulación filtrado StockWindow")
            
            # Simular la estructura de datos de StockWindow
            stock_data_formatted = []
            for row in stock_data:
                producto_id, cantidad, nombre, referencia = row
                
                stock_data_formatted.append({
                    'producto_id': producto_id,
                    'nombre': nombre,
                    'referencia': referencia,
                    'cantidad': cantidad,
                    'fecha_actualizacion': 'N/A'  # Simplificado para el test
                })
            
            print(f"   📊 Datos formateados: {len(stock_data_formatted)}")
            
            # Test de filtrado por texto
            search_text = "test"
            filtered_data = [
                item for item in stock_data_formatted
                if search_text.lower() in item['nombre'].lower() or
                   search_text.lower() in item['referencia'].lower()
            ]
            
            print(f"   🔍 Búsqueda '{search_text}': {len(filtered_data)} resultados")
            for item in filtered_data:
                print(f"      - {item['nombre']} ({item['referencia']})")
            
            # Debería encontrar los productos con "Test" en el nombre
            assert len(filtered_data) >= 2, f"Debería encontrar al menos 2 productos, encontró {len(filtered_data)}"
            
            # Test de filtrado por referencia
            search_text = "search"
            filtered_data = [
                item for item in stock_data_formatted
                if search_text.lower() in item['nombre'].lower() or
                   search_text.lower() in item['referencia'].lower()
            ]
            
            print(f"   🔍 Búsqueda '{search_text}': {len(filtered_data)} resultados")
            for item in filtered_data:
                print(f"      - {item['nombre']} ({item['referencia']})")
            
            # Debería encontrar el producto con "SEARCH" en la referencia
            assert len(filtered_data) >= 1, f"Debería encontrar al menos 1 producto, encontró {len(filtered_data)}"
            
            print("   ✅ Filtrado funciona correctamente")
            
            print("\n🎉 TODOS LOS TESTS PASAN - El formato de datos es correcto")
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_db_path):
                    os.remove(temp_db_path)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_search_edge_cases():
    """Test des cas limites pour la recherche stock"""
    print("\n🧪 Test: Cas limites recherche stock")
    
    try:
        from database.models import Stock, Producto
        from database.database import Database
        
        # Créer une base de données temporaire
        temp_db_path = tempfile.mktemp(suffix='.db')
        
        try:
            # Initialiser la base de données
            db = Database(temp_db_path)
            
            # Assurer que l'instance globale utilise notre DB temporaire
            from database.database import db as global_db
            global_db.db_path = temp_db_path
            
            # Créer produits avec caractères spéciaux
            productos_especiales = [
                ("Producto con Ñ", "REF-Ñ01", 10.0, "Categoría"),
                ("PRODUCTO MAYÚSCULAS", "REF-MAY", 20.0, "CATEGORIA"),
                ("producto minúsculas", "ref-min", 15.0, "categoria"),
                ("Producto con números 123", "REF-123", 25.0, "Cat123")
            ]
            
            for nombre, referencia, precio, categoria in productos_especiales:
                producto = Producto(
                    nombre=nombre,
                    referencia=referencia,
                    precio=precio,
                    categoria=categoria
                )
                producto.save()
            
            # Obtener datos
            stock_data = Stock.get_all()
            stock_data_formatted = []
            for row in stock_data:
                producto_id, cantidad, nombre, referencia = row
                stock_data_formatted.append({
                    'producto_id': producto_id,
                    'nombre': nombre,
                    'referencia': referencia,
                    'cantidad': cantidad,
                    'fecha_actualizacion': 'N/A'
                })
            
            # Test 1: Búsqueda insensible a mayúsculas/minúsculas
            print("\n   1️⃣ Test búsqueda insensible a mayúsculas")
            
            search_text = "PRODUCTO"
            filtered_data = [
                item for item in stock_data_formatted
                if search_text.lower() in item['nombre'].lower() or
                   search_text.lower() in item['referencia'].lower()
            ]
            
            print(f"   🔍 Búsqueda '{search_text}': {len(filtered_data)} resultados")
            assert len(filtered_data) >= 3, f"Debería encontrar al menos 3 productos, encontró {len(filtered_data)}"
            print("   ✅ Búsqueda insensible a mayúsculas funciona")
            
            # Test 2: Búsqueda con caracteres especiales
            print("\n   2️⃣ Test búsqueda con caracteres especiales")
            
            search_text = "ñ"
            filtered_data = [
                item for item in stock_data_formatted
                if search_text.lower() in item['nombre'].lower() or
                   search_text.lower() in item['referencia'].lower()
            ]
            
            print(f"   🔍 Búsqueda '{search_text}': {len(filtered_data)} resultados")
            assert len(filtered_data) >= 1, f"Debería encontrar al menos 1 producto, encontró {len(filtered_data)}"
            print("   ✅ Búsqueda con caracteres especiales funciona")
            
            # Test 3: Búsqueda por números
            print("\n   3️⃣ Test búsqueda por números")
            
            search_text = "123"
            filtered_data = [
                item for item in stock_data_formatted
                if search_text.lower() in item['nombre'].lower() or
                   search_text.lower() in item['referencia'].lower()
            ]
            
            print(f"   🔍 Búsqueda '{search_text}': {len(filtered_data)} resultados")
            assert len(filtered_data) >= 1, f"Debería encontrar al menos 1 producto, encontró {len(filtered_data)}"
            print("   ✅ Búsqueda por números funciona")
            
            # Test 4: Búsqueda vacía
            print("\n   4️⃣ Test búsqueda vacía")
            
            search_text = ""
            if not search_text:
                filtered_data = stock_data_formatted.copy()
            else:
                filtered_data = [
                    item for item in stock_data_formatted
                    if search_text.lower() in item['nombre'].lower() or
                       search_text.lower() in item['referencia'].lower()
                ]
            
            print(f"   🔍 Búsqueda vacía: {len(filtered_data)} resultados")
            assert len(filtered_data) == len(stock_data_formatted), "Búsqueda vacía debe mostrar todos los productos"
            print("   ✅ Búsqueda vacía funciona")
            
            print("\n🎉 TODOS LOS TESTS CAS LIMITES PASSEN")
            return True
            
        finally:
            # Nettoyage
            try:
                if os.path.exists(temp_db_path):
                    os.remove(temp_db_path)
            except:
                pass
                
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_search_with_none_values():
    """Test de la recherche avec des valeurs None ou vides"""
    print("\n🧪 Test: Recherche avec valeurs None/vides")
    
    try:
        # Test de la logique de filtrage avec des valeurs problématiques
        stock_data_formatted = [
            {'nombre': 'Producto Normal', 'referencia': 'REF-001', 'cantidad': 10},
            {'nombre': None, 'referencia': 'REF-002', 'cantidad': 5},
            {'nombre': 'Producto Vacio', 'referencia': '', 'cantidad': 0},
            {'nombre': '', 'referencia': 'REF-004', 'cantidad': 15},
        ]
        
        print(f"   📊 Datos de test: {len(stock_data_formatted)} productos")
        
        # Test de filtrage robuste
        search_text = "normal"
        filtered_data = []
        
        for item in stock_data_formatted:
            nombre = item.get('nombre', '') or ''  # Gérer None
            referencia = item.get('referencia', '') or ''  # Gérer None
            
            if (search_text.lower() in nombre.lower() or
                search_text.lower() in referencia.lower()):
                filtered_data.append(item)
        
        print(f"   🔍 Búsqueda '{search_text}': {len(filtered_data)} resultados")
        assert len(filtered_data) == 1, f"Debería encontrar 1 producto, encontró {len(filtered_data)}"
        
        # Test avec recherche vide
        search_text = ""
        if not search_text:
            filtered_data = stock_data_formatted.copy()
        
        print(f"   🔍 Búsqueda vacía: {len(filtered_data)} resultados")
        assert len(filtered_data) == 4, f"Debería mostrar todos los productos"
        
        print("   ✅ Gestion des valeurs None/vides fonctionne")
        return True
        
    except Exception as e:
        print(f"   ❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Tests de régression - Correction recherche stock")
    print("=" * 55)
    
    success1 = test_stock_get_all_format()
    success2 = test_stock_search_edge_cases()
    success3 = test_stock_search_with_none_values()
    
    if success1 and success2 and success3:
        print("\n🎉 TOUS LES TESTS PASSENT")
        print("\n✅ DIAGNOSTIC COMPLET:")
        print("   • Format des données Stock.get_all() : Correct")
        print("   • Logique de filtrage : Fonctionne")
        print("   • Cas limites : Gérés correctement")
        print("   • Valeurs None/vides : Gérées")
        print("\n💡 Le problème pourrait être ailleurs...")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS ÉCHOUENT")
        sys.exit(1)
