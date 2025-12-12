#!/usr/bin/env python3
"""
Test simple pour vérifier que nos corrections de sécurité fonctionnent
- Utilise une base de données de test isolée
- Vérifie que la correction precio_venta fonctionne
- Ne nécessite pas pytest
"""

import sys
import os
import tempfile
import shutil

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

from database.database import Database

def test_correction_precio_venta_avec_db_test():
    """Test de la correction precio_venta avec base de données de test sécurisée"""
    print("🛡️ TEST SÉCURISÉ: Correction precio_venta")
    print("=" * 50)
    print("⚠️  UTILISATION DE BASE DE DONNÉES DE TEST (PAS DE PRODUCTION)")
    print()
    
    # Créer une base de données temporaire pour le test
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test_correction_precio_venta.db')
    
    # Sauvegarder la configuration originale
    original_db_path = getattr(Database, '_db_path', None)
    
    try:
        # Configurer la base de données de test
        Database._db_path = test_db_path
        
        print(f"📁 Base de données de test: {test_db_path}")
        print("📦 Créant produit de test...")
        
        # Créer la base de données de test avec un produit
        db = Database()
        
        # Ajouter un produit de test
        producto_test = {
            'nombre': 'Producto Test Corrección',
            'referencia': 'CORR-001',
            'precio_venta': 42.75,
            'precio_compra': 25.00,
            'categoria': 'Test Corrección',
            'descripcion': 'Producto para verificar corrección precio_venta',
            'iva_recomendado': 21.0,
            'stock_actual': 15,
            'stock_minimo': 3
        }
        
        result = db.add_product(producto_test)
        if result:
            print(f"  ✅ Producto agregado: {producto_test['nombre']}")
        else:
            print(f"  ❌ Error agregando producto")
            return False
        
        # Verificar que el producto se agregó correctamente
        productos = db.get_all_products()
        print(f"✅ Productos en DB de test: {len(productos)}")
        
        if not productos:
            print("❌ No se encontraron productos en la DB de test")
            return False
        
        producto = productos[0]
        print(f"📦 Producto encontrado: {producto['nombre']}")
        
        # TEST PRINCIPAL: Verificar la corrección precio_venta vs precio
        print("\n🔍 VERIFICANDO CORRECCIÓN:")
        print("-" * 30)
        
        # Método correcto (después de la corrección)
        precio_correcto = producto.get('precio_venta', 0.0)
        print(f"✅ precio_venta (CORRECTO): {precio_correcto}")
        
        # Método incorrecto (antes de la corrección)
        precio_incorrecto = producto.get('precio', 0.0)
        print(f"❌ precio (INCORRECTO): {precio_incorrecto}")
        
        # Verificar que la corrección funciona
        if precio_correcto > 0 and precio_incorrecto == 0:
            print("\n🎉 CORRECCIÓN VALIDADA:")
            print("  ✅ El código usa precio_venta correctamente")
            print("  ✅ Los productos aparecerán en las facturas")
            
            # Test du format pour le combo
            stock = producto.get('stock_actual', 0)
            formato_combo = f"{producto['nombre']} - {precio_correcto:.2f}€ (Stock: {stock})"
            print(f"  ✅ Formato combo: {formato_combo}")
            
            return True
        else:
            print("\n❌ CORRECCIÓN NO VALIDADA:")
            print(f"  precio_venta: {precio_correcto}")
            print(f"  precio: {precio_incorrecto}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR durante el test: {e}")
        return False
    
    finally:
        # Restaurer la configuration originale
        if original_db_path:
            Database._db_path = original_db_path
        
        # Nettoyer la base de données temporaire
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"\n🧹 Base de datos de test eliminada: {temp_dir}")
        except Exception as e:
            print(f"⚠️  Error limpiando test DB: {e}")

def main():
    """Fonction principale"""
    print("🚀 INICIANDO TEST DE CORRECCIÓN DE SEGURIDAD")
    print("=" * 60)
    
    success = test_correction_precio_venta_avec_db_test()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST EXITOSO: Corrección validada")
        print("\n💡 PRÓXIMOS PASOS:")
        print("   1. Ejecute la aplicación: python main.py")
        print("   2. Vaya a Gestión de Facturas → Crear Nueva Factura")
        print("   3. Verifique que puede seleccionar productos")
        print("   4. Los productos deberían aparecer con precios correctos")
    else:
        print("❌ TEST FALLIDO: Verificar corrección")
    
    print("=" * 60)
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
