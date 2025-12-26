#!/usr/bin/env python3
"""
Script de profiling des services
Mesure les performances des opérations critiques
"""

import cProfile
import pstats
import io
import tempfile
import os
import logging
from datetime import datetime

# Désactiver le logging pour le profiling
logging.disable(logging.CRITICAL)

from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from services.organizacion_service import OrganizacionService
from services.factura_service import FacturaService


def profile_producto_service():
    """Profiler les opérations du ProductoService"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        service = ProductoService(temp_db.name)
        
        # Créer 100 produits
        for i in range(100):
            service.create_producto({
                'nombre': f'Producto {i}',
                'precio_venta': 10.0 + i,
                'iva_recomendado': 21.0,
                'stock': 100
            })
        
        # Lire tous les produits
        productos = service.get_all_productos()
        
        # Mettre à jour 50 produits
        for i in range(50):
            service.update_producto({
                'id': i + 1,
                'nombre': f'Producto Updated {i}',
                'precio_venta': 20.0 + i,
                'referencia': f'REF-UPD-{i}'
            })
        
        # Supprimer 25 produits
        for i in range(25):
            service.delete_producto(i + 1)
            
    finally:
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)


def profile_cliente_service():
    """Profiler les opérations du ClienteService"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        service = ClienteService(temp_db.name)
        
        # Créer 100 clients
        for i in range(100):
            service.create_cliente({
                'nombre': f'Cliente {i}',
                'email': f'cliente{i}@test.com',
                'nif': f'12345678{i % 10}'
            })
        
        # Lire tous les clients
        clientes = service.get_all_clientes()
        
        # Mettre à jour 50 clients
        for i in range(50):
            service.update_cliente({
                'id': i + 1,
                'nombre': f'Cliente Updated {i}',
                'email': f'updated{i}@test.com'
            })
            
    finally:
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)


def profile_factura_service():
    """Profiler les opérations du FacturaService"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    temp_db.close()
    
    try:
        # Créer les services
        producto_service = ProductoService(temp_db.name)
        cliente_service = ClienteService(temp_db.name)
        factura_service = FacturaService(temp_db.name)
        
        # Créer un produit et un client
        producto_id = producto_service.create_producto({
            'nombre': 'Producto Test',
            'precio_venta': 10.0,
            'iva_recomendado': 21.0,
            'stock': 1000
        })
        
        cliente_id = cliente_service.create_cliente({
            'nombre': 'Cliente Test',
            'email': 'test@test.com',
            'nif': '12345678A'
        })
        
        # Créer 50 factures
        for i in range(50):
            factura_service.create_factura({
                'numero': f'FAC-{i:04d}',
                'fecha': datetime.now().strftime('%Y-%m-%d'),
                'cliente': {
                    'id': cliente_id,
                    'nombre': 'Cliente Test',
                    'nif': '12345678A',
                    'direccion': 'Calle Test 123'
                },
                'subtotal': 10.0,
                'iva_total': 2.1,
                'total': 12.1,
                'lineas': [{
                    'producto_id': producto_id,
                    'cantidad': 1,
                    'precio_unitario': 10.0,
                    'iva': 21.0
                }]
            })
        
        # Lire toutes les factures
        facturas = factura_service.get_all_facturas()
        
    finally:
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)


def run_profiling():
    """Exécuter le profiling de tous les services"""
    print("=" * 80)
    print("PROFILING DES SERVICES")
    print("=" * 80)
    
    # Profiler ProductoService
    print("\n1. ProductoService")
    print("-" * 80)
    profiler = cProfile.Profile()
    profiler.enable()
    profile_producto_service()
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())
    
    # Profiler ClienteService
    print("\n2. ClienteService")
    print("-" * 80)
    profiler = cProfile.Profile()
    profiler.enable()
    profile_cliente_service()
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())
    
    # Profiler FacturaService
    print("\n3. FacturaService")
    print("-" * 80)
    profiler = cProfile.Profile()
    profiler.enable()
    profile_factura_service()
    profiler.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())


if __name__ == '__main__':
    run_profiling()

