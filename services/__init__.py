# -*- coding: utf-8 -*-
"""
Services métier pour la séparation UI / Logique
"""

from services.base_service import BaseService
from services.producto_service import ProductoService
from services.cliente_service import ClienteService
from services.organizacion_service import OrganizacionService
from services.factura_service import FacturaService
from services.stock_service import StockService
from services.informes_service import InformesService

__all__ = [
    'BaseService',
    'ProductoService',
    'ClienteService',
    'OrganizacionService',
    'FacturaService',
    'StockService',
    'InformesService'
]

