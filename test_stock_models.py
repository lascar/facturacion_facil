#!/usr/bin/env python3
"""
Test des modèles de stock sans interface graphique
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.models import Producto, Stock, StockMovement

def test_stock_models():
    """Test des modèles de stock"""
    
    print("=== Test des modèles de stock ===\n")
    
    # 1. Créer un produit de test
    print("1. Création d'un produit de test...")
    producto = Producto(
        nombre="Producto Test Stock",
        referencia="STOCK001",
        precio=15.50,
        categoria="Test",
        descripcion="Producto para test de stock"
    )
    producto.save()
    print(f"   ✓ Producto creado con ID: {producto.id}")
    
    # 2. Vérifier que le stock a été créé automatiquement
    print("\n2. Vérification du stock initial...")
    stock_inicial = Stock.get_by_product(producto.id)
    print(f"   ✓ Stock inicial: {stock_inicial} unidades")
    
    # 3. Obtenir tous les stocks
    print("\n3. Obtention de tous les stocks...")
    todos_stocks = Stock.get_all()
    print(f"   ✓ Total de productos con stock: {len(todos_stocks)}")
    for stock_info in todos_stocks[-3:]:  # Mostrar los últimos 3
        print(f"      - {stock_info[2]} ({stock_info[3]}): {stock_info[1]} unidades")
    
    # 4. Actualizar stock manualmente
    print("\n4. Actualización manual de stock...")
    nuevo_stock = Stock(producto.id, 25)
    nuevo_stock.save()
    stock_actualizado = Stock.get_by_product(producto.id)
    print(f"   ✓ Stock actualizado: {stock_actualizado} unidades")
    
    # 5. Crear movimientos de stock
    print("\n5. Creación de movimientos de stock...")
    
    # Entrada
    movimiento1 = StockMovement.create(
        producto.id, 
        10, 
        "ENTRADA", 
        "Entrada inicial de mercancía"
    )
    print(f"   ✓ Movimiento de entrada creado: +10 unidades")
    
    # Salida
    movimiento2 = StockMovement.create(
        producto.id, 
        -3, 
        "SALIDA", 
        "Salida por venta"
    )
    print(f"   ✓ Movimiento de salida creado: -3 unidades")
    
    # Ajuste
    movimiento3 = StockMovement.create(
        producto.id, 
        -2, 
        "AJUSTE_NEGATIVO", 
        "Ajuste por inventario"
    )
    print(f"   ✓ Movimiento de ajuste creado: -2 unidades")
    
    # 6. Obtener historial de movimientos
    print("\n6. Historial de movimientos...")
    movimientos = StockMovement.get_by_product(producto.id)
    print(f"   ✓ Total de movimientos: {len(movimientos)}")
    for mov in movimientos:
        signo = "+" if mov.cantidad > 0 else ""
        print(f"      - {mov.tipo}: {signo}{mov.cantidad} - {mov.descripcion}")
    
    # 7. Test de stock bajo
    print("\n7. Test de productos con stock bajo...")
    
    # Crear producto con stock bajo
    producto_bajo = Producto(
        nombre="Producto Stock Bajo",
        referencia="BAJO001",
        precio=5.00,
        categoria="Test",
        descripcion="Producto con stock bajo"
    )
    producto_bajo.save()
    
    # Establecer stock bajo
    stock_bajo = Stock(producto_bajo.id, 3)
    stock_bajo.save()
    
    # Obtener productos con stock bajo
    productos_stock_bajo = Stock.get_low_stock(5)
    print(f"   ✓ Productos con stock bajo (≤5): {len(productos_stock_bajo)}")
    for stock_info in productos_stock_bajo:
        print(f"      - {stock_info[2]} ({stock_info[3]}): {stock_info[1]} unidades")
    
    # 8. Test de actualización por venta
    print("\n8. Test de actualización por venta...")
    stock_antes = Stock.get_by_product(producto.id)
    print(f"   Stock antes de venta: {stock_antes}")
    
    Stock.update_stock(producto.id, 5)  # Vender 5 unidades
    
    stock_despues = Stock.get_by_product(producto.id)
    print(f"   Stock después de venta: {stock_despues}")
    print(f"   ✓ Diferencia: -{stock_antes - stock_despues} unidades")
    
    # Verificar que se creó el movimiento de venta
    movimientos_actualizados = StockMovement.get_by_product(producto.id)
    ultimo_movimiento = movimientos_actualizados[0]  # El más reciente
    print(f"   ✓ Último movimiento: {ultimo_movimiento.tipo} - {ultimo_movimiento.cantidad}")
    
    print("\n=== Test completado exitosamente ===")

if __name__ == "__main__":
    test_stock_models()
