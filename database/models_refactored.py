#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modèles refactorisés avec dataclasses et type annotations
Refactorisation Pythonic - Phase 2

Principes appliqués:
- Dataclasses pour réduire le boilerplate
- Type annotations complètes
- List comprehensions au lieu de boucles manuelles
- Séparation des responsabilités (data vs logic)
"""

from dataclasses import dataclass, field
from typing import Optional, ClassVar
from datetime import datetime

from .database import db
from config.constants import DEFAULT_IVA, DEFAULT_STOCK_MINIMO


# ============================================================================
# DATACLASS: Cliente
# ============================================================================

@dataclass
class ClienteRefactored:
    """
    Modèle de données pour un client

    Utilise @dataclass pour générer automatiquement:
    - __init__()
    - __repr__()
    - __eq__()
    """
    nombre: str = ""
    dni_nie: str = ""
    direccion: str = ""
    email: str = ""
    telefono: str = ""
    id: Optional[int] = None

    def save(self) -> int:
        """Guarda el cliente en la base de datos"""
        if self.id:
            # Actualizar cliente existente
            query = '''UPDATE clientes SET nombre=?, dni_nie=?, direccion=?, email=?, telefono=?,
                      fecha_actualizacion=CURRENT_TIMESTAMP WHERE id=?'''
            params = (self.nombre, self.dni_nie, self.direccion, self.email, self.telefono, self.id)
            db.execute_query(query, params)
        else:
            # Crear nuevo cliente
            query = '''INSERT INTO clientes (nombre, dni_nie, direccion, email, telefono)
                      VALUES (?, ?, ?, ?, ?)'''
            params = (self.nombre, self.dni_nie, self.direccion, self.email, self.telefono)
            self.id = db.execute_query(query, params)
        return self.id

    def delete(self) -> None:
        """Elimina el cliente de la base de datos"""
        if self.id:
            db.execute_query("DELETE FROM clientes WHERE id=?", (self.id,))

    @staticmethod
    def get_all() -> list['ClienteRefactored']:
        """Obtiene todos los clientes - Versión Pythonic con list comprehension"""
        query = "SELECT * FROM clientes ORDER BY nombre"
        results = db.execute_query(query)

        # ✅ List comprehension au lieu de boucle manuelle
        return [
            ClienteRefactored(
                id=row[0],
                nombre=row[1],
                dni_nie=row[2],
                direccion=row[3],
                email=row[4],
                telefono=row[5]
            )
            for row in results
        ]

    @staticmethod
    def get_by_id(cliente_id: int) -> Optional['ClienteRefactored']:
        """Obtiene un cliente por su ID"""
        query = "SELECT * FROM clientes WHERE id=?"
        results = db.execute_query(query, (cliente_id,))

        if not results:
            return None

        row = results[0]
        return ClienteRefactored(
            id=row[0],
            nombre=row[1],
            dni_nie=row[2],
            direccion=row[3],
            email=row[4],
            telefono=row[5]
        )

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional['ClienteRefactored']:
        """Obtiene un cliente por su nombre"""
        query = "SELECT * FROM clientes WHERE nombre=?"
        results = db.execute_query(query, (nombre,))

        if not results:
            return None

        row = results[0]
        return ClienteRefactored(
            id=row[0],
            nombre=row[1],
            dni_nie=row[2],
            direccion=row[3],
            email=row[4],
            telefono=row[5]
        )

    @staticmethod
    def search(search_term: str) -> list['ClienteRefactored']:
        """Busca clientes por nombre, DNI/NIE o email - Versión Pythonic"""
        query = '''SELECT * FROM clientes
                  WHERE nombre LIKE ? OR dni_nie LIKE ? OR email LIKE ?
                  ORDER BY nombre'''
        search_pattern = f"%{search_term}%"
        results = db.execute_query(query, (search_pattern, search_pattern, search_pattern))

        # ✅ List comprehension
        return [
            ClienteRefactored(
                id=row[0],
                nombre=row[1],
                dni_nie=row[2],
                direccion=row[3],
                email=row[4],
                telefono=row[5]
            )
            for row in results
        ]


# ============================================================================
# DATACLASS: Producto
# ============================================================================

@dataclass
class ProductoRefactored:
    """Modèle de données pour un produit"""
    nombre: str = ""
    referencia: str = ""
    precio: float = 0.0
    categoria: str = ""
    descripcion: str = ""
    imagen_path: str = ""
    iva_recomendado: float = DEFAULT_IVA
    id: Optional[int] = None

    def get_stock_actual(self, db_path: Optional[str] = None) -> int:
        """Obtiene el stock actual desde la tabla stock"""
        from .models import Stock
        return Stock.get_by_product(self.id, db_path) if self.id else 0

    def get_stock_minimo(self) -> int:
        """Obtiene el stock mínimo"""
        return DEFAULT_STOCK_MINIMO

    def save(self) -> int:
        """Guarda el producto en la base de datos"""
        if self.id:
            query = '''UPDATE productos SET nombre=?, referencia=?, precio=?,
                      categoria=?, descripcion=?, imagen_path=?, iva_recomendado=?
                      WHERE id=?'''
            params = (self.nombre, self.referencia, self.precio, self.categoria,
                     self.descripcion, self.imagen_path, self.iva_recomendado, self.id)
            db.execute_query(query, params)
        else:
            query = '''INSERT INTO productos (nombre, referencia, precio, categoria,
                      descripcion, imagen_path, iva_recomendado)
                      VALUES (?, ?, ?, ?, ?, ?, ?)'''
            params = (self.nombre, self.referencia, self.precio, self.categoria,
                     self.descripcion, self.imagen_path, self.iva_recomendado)
            self.id = db.execute_query(query, params)

            from .models import Stock
            Stock.create_for_product(self.id)

        return self.id

    def delete(self) -> None:
        """Elimina el producto"""
        if self.id:
            db.execute_query("DELETE FROM stock WHERE producto_id=?", (self.id,))
            db.execute_query("DELETE FROM productos WHERE id=?", (self.id,))

    @staticmethod
    def get_all() -> list['ProductoRefactored']:
        """Obtiene todos los productos - Pythonic con list comprehension"""
        query = "SELECT * FROM productos ORDER BY nombre"
        results = db.execute_query(query)

        return [
            ProductoRefactored(
                id=row[0], nombre=row[1], referencia=row[2], precio=row[3],
                categoria=row[4], descripcion=row[5], imagen_path=row[6],
                iva_recomendado=row[7]
            )
            for row in results
        ]

    @staticmethod
    def get_by_id(producto_id: int) -> Optional['ProductoRefactored']:
        """Obtiene un producto por ID"""
        query = "SELECT * FROM productos WHERE id=?"
        results = db.execute_query(query, (producto_id,))

        if not results:
            return None

        row = results[0]
        return ProductoRefactored(
            id=row[0], nombre=row[1], referencia=row[2], precio=row[3],
            categoria=row[4], descripcion=row[5], imagen_path=row[6],
            iva_recomendado=row[7]
        )


# ============================================================================
# HELPER FUNCTIONS - Conversion entre models
# ============================================================================

def cliente_to_refactored(cliente) -> ClienteRefactored:
    """Convertit un Cliente classique en ClienteRefactored"""
    return ClienteRefactored(
        id=cliente.id,
        nombre=cliente.nombre,
        dni_nie=cliente.dni_nie,
        direccion=cliente.direccion,
        email=cliente.email,
        telefono=cliente.telefono
    )


def producto_to_refactored(producto) -> ProductoRefactored:
    """Convertit un Producto classique en ProductoRefactored"""
    return ProductoRefactored(
        id=producto.id,
        nombre=producto.nombre,
        referencia=producto.referencia,
        precio=producto.precio,
        categoria=producto.categoria,
        descripcion=producto.descripcion,
        imagen_path=producto.imagen_path,
        iva_recomendado=producto.iva_recomendado
    )
