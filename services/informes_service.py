# -*- coding: utf-8 -*-
"""
Service pour générer les rapports (informes) de facturation et stock
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
from services.base_service import BaseService
from utils.decorators import log_execution, log_performance
from utils.exceptions import ValidationError, DatabaseError


class InformesService(BaseService):
    """Service pour générer les rapports de facturation et stock"""
    
    @log_execution
    @log_performance(threshold_seconds=1.0)
    def get_informe_facturacion(
        self, 
        fecha_inicio: str, 
        fecha_fin: str
    ) -> Dict[str, Any]:
        """
        Générer un rapport de facturation pour une période donnée
        
        Args:
            fecha_inicio: Date de début (format: YYYY-MM-DD)
            fecha_fin: Date de fin (format: YYYY-MM-DD)
            
        Returns:
            Dict avec les statistiques de facturation
            
        Raises:
            ValidationError: Si les dates sont invalides
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation des dates
        try:
            inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            
            if inicio > fin:
                raise ValidationError(
                    "La fecha de inicio no puede ser posterior a la fecha de fin",
                    details={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
                )
        except ValueError as e:
            raise ValidationError(
                f"Formato de fecha inválido: {str(e)}",
                details={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
            )
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # Obtenir toutes les factures de la période avec informations client
            cursor.execute("""
                SELECT f.id, f.numero_factura, f.fecha_factura, f.nombre_cliente,
                       f.subtotal, f.total_iva, f.total_factura, f.estado,
                       f.cliente_id, f.dni_nie_cliente
                FROM facturas f
                WHERE f.fecha_factura BETWEEN ? AND ?
                ORDER BY f.fecha_factura ASC
            """, (fecha_inicio, fecha_fin))

            # Utiliser list comprehension pour construire la liste de facturas
            rows = cursor.fetchall()
            facturas = [
                {
                    'id': row[0],
                    'numero': row[1],
                    'fecha': row[2],
                    'cliente': row[3],
                    'subtotal': row[4] or 0.0,
                    'iva': row[5] or 0.0,
                    'total': row[6] or 0.0,
                    'estado': row[7] or 'Borrador',
                    'cliente_id': row[8],
                    'dni_nie': row[9] or ''
                }
                for row in rows
            ]

            # Calculer les totaux avec sum() et comprehensions
            total_subtotal = sum(f['subtotal'] for f in facturas)
            total_iva = sum(f['iva'] for f in facturas)
            total_general = sum(f['total'] for f in facturas)
            num_facturas = len(facturas)
            
            # Obtenir les statistiques par IVA (global)
            # Calculer la base imposable: cantidad * precio_unitario * (1 - descuento/100)
            # Calculer l'IVA: base_imposable * (iva_aplicado/100)
            cursor.execute("""
                SELECT fi.iva_aplicado,
                       SUM(fi.cantidad * fi.precio_unitario * (1 - COALESCE(fi.descuento, 0)/100)) as base_imponible,
                       SUM(fi.cantidad * fi.precio_unitario * (1 - COALESCE(fi.descuento, 0)/100) * fi.iva_aplicado / 100) as total_iva
                FROM factura_items fi
                JOIN facturas f ON fi.factura_id = f.id
                WHERE f.fecha_factura BETWEEN ? AND ?
                GROUP BY fi.iva_aplicado
                ORDER BY fi.iva_aplicado
            """, (fecha_inicio, fecha_fin))

            # Utiliser list comprehension pour le décomposition IVA
            desglose_iva = [
                {
                    'iva_aplicado': row[0],
                    'base_imponible': round(row[1] or 0.0, 2),
                    'total_iva': round(row[2] or 0.0, 2),
                    'total': round((row[1] or 0.0) + (row[2] or 0.0), 2)
                }
                for row in cursor.fetchall()
            ]

            # Obtenir le désglose IVA par facture
            cursor.execute("""
                SELECT fi.factura_id, fi.iva_aplicado,
                       SUM(fi.cantidad * fi.precio_unitario * (1 - COALESCE(fi.descuento, 0)/100)) as base_imponible,
                       SUM(fi.cantidad * fi.precio_unitario * (1 - COALESCE(fi.descuento, 0)/100) * fi.iva_aplicado / 100) as total_iva
                FROM factura_items fi
                JOIN facturas f ON fi.factura_id = f.id
                WHERE f.fecha_factura BETWEEN ? AND ?
                GROUP BY fi.factura_id, fi.iva_aplicado
                ORDER BY fi.factura_id, fi.iva_aplicado
            """, (fecha_inicio, fecha_fin))

            # Organiser le désglose IVA par facture
            desglose_iva_por_factura = {}
            for row in cursor.fetchall():
                factura_id = row[0]
                if factura_id not in desglose_iva_por_factura:
                    desglose_iva_por_factura[factura_id] = []
                desglose_iva_por_factura[factura_id].append({
                    'iva_aplicado': row[1],
                    'base_imponible': round(row[2] or 0.0, 2),
                    'total_iva': round(row[3] or 0.0, 2)
                })

            # Ajouter le désglose IVA à chaque facture
            for factura in facturas:
                factura['desglose_iva'] = desglose_iva_por_factura.get(factura['id'], [])

            # Obtenir la liste unique des clients avec DNI
            clientes_unicos = {}
            for factura in facturas:
                cliente_id = factura.get('cliente_id')
                if cliente_id and cliente_id not in clientes_unicos:
                    clientes_unicos[cliente_id] = {
                        'nombre': factura['cliente'],
                        'dni_nie': factura['dni_nie']
                    }

            lista_clientes = [
                {'nombre': v['nombre'], 'dni_nie': v['dni_nie']}
                for k, v in clientes_unicos.items()
            ]
            lista_clientes.sort(key=lambda x: x['nombre'])
            
            # Obtenir les produits les plus vendus
            cursor.execute("""
                SELECT p.nombre, p.referencia,
                       SUM(fi.cantidad) as cantidad_total,
                       SUM(fi.total) as importe_total
                FROM factura_items fi
                JOIN facturas f ON fi.factura_id = f.id
                JOIN productos p ON fi.producto_id = p.id
                WHERE f.fecha_factura BETWEEN ? AND ?
                GROUP BY fi.producto_id, p.nombre, p.referencia
                ORDER BY cantidad_total DESC
                LIMIT 10
            """, (fecha_inicio, fecha_fin))
            
            # Utiliser list comprehension pour les produits les plus vendus
            productos_mas_vendidos = [
                {
                    'nombre': row[0],
                    'referencia': row[1],
                    'cantidad': row[2],
                    'importe': row[3] or 0.0
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()

            return {
                'periodo': {
                    'inicio': fecha_inicio,
                    'fin': fecha_fin
                },
                'resumen': {
                    'num_facturas': num_facturas,
                    'subtotal': round(total_subtotal, 2),
                    'total_iva': round(total_iva, 2),
                    'total': round(total_general, 2),
                    'promedio_factura': round(total_general / num_facturas, 2) if num_facturas > 0 else 0.0
                },
                'facturas': facturas,
                'desglose_iva': desglose_iva,
                'lista_clientes': lista_clientes,
                'productos_mas_vendidos': productos_mas_vendidos
            }
            
        except Exception as e:
            raise DatabaseError(
                f"Error generando informe de facturación",
                details={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'error': str(e)}
            )

    @log_execution
    @log_performance(threshold_seconds=0.5)
    def get_informe_stock(
        self,
        producto_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Générer un rapport de stock pour tous les produits ou une sélection

        Args:
            producto_ids: Liste des IDs de produits (None = tous les produits)

        Returns:
            Dict avec les informations de stock

        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Construire la requête selon la sélection
            if producto_ids and len(producto_ids) > 0:
                placeholders = ','.join(['?'] * len(producto_ids))
                query = f"""
                    SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria,
                           COALESCE(s.cantidad_disponible, 0) as stock_actual,
                           COALESCE(s.stock_minimo, 0) as stock_minimo,
                           s.fecha_actualizacion
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    WHERE p.id IN ({placeholders})
                    ORDER BY p.nombre
                """
                cursor.execute(query, producto_ids)
            else:
                cursor.execute("""
                    SELECT p.id, p.nombre, p.referencia, p.precio, p.categoria,
                           COALESCE(s.cantidad_disponible, 0) as stock_actual,
                           COALESCE(s.stock_minimo, 0) as stock_minimo,
                           s.fecha_actualizacion
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    ORDER BY p.nombre
                """)

            # Utiliser list comprehension pour construire la liste de productos
            rows = cursor.fetchall()
            productos = [
                {
                    'id': row[0],
                    'nombre': row[1],
                    'referencia': row[2],
                    'precio': row[3] or 0.0,
                    'categoria': row[4] or 'Sin categoría',
                    'stock_actual': row[5],
                    'stock_minimo': row[6],
                    'valor_stock': round(row[5] * (row[3] or 0.0), 2),
                    'fecha_actualizacion': row[7] or 'N/A'
                }
                for row in rows
            ]

            # Calculer les totaux avec sum() et comprehensions
            total_productos = len(productos)
            total_valor_stock = sum(p['valor_stock'] for p in productos)
            productos_sin_stock = sum(1 for p in productos if p['stock_actual'] == 0)

            # Obtener estadísticas por categoría
            if producto_ids and len(producto_ids) > 0:
                placeholders = ','.join(['?'] * len(producto_ids))
                query = f"""
                    SELECT p.categoria,
                           COUNT(*) as num_productos,
                           SUM(COALESCE(s.cantidad_disponible, 0)) as stock_total,
                           SUM(COALESCE(s.cantidad_disponible, 0) * p.precio) as valor_total
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    WHERE p.id IN ({placeholders})
                    GROUP BY p.categoria
                    ORDER BY valor_total DESC
                """
                cursor.execute(query, producto_ids)
            else:
                cursor.execute("""
                    SELECT p.categoria,
                           COUNT(*) as num_productos,
                           SUM(COALESCE(s.cantidad_disponible, 0)) as stock_total,
                           SUM(COALESCE(s.cantidad_disponible, 0) * p.precio) as valor_total
                    FROM productos p
                    LEFT JOIN stock s ON p.id = s.producto_id
                    GROUP BY p.categoria
                    ORDER BY valor_total DESC
                """)

            # Utiliser list comprehension pour les statistiques par catégorie
            por_categoria = [
                {
                    'categoria': row[0] or 'Sin categoría',
                    'num_productos': row[1],
                    'stock_total': row[2] or 0,
                    'valor_total': round(row[3] or 0.0, 2)
                }
                for row in cursor.fetchall()
            ]

            conn.close()

            return {
                'resumen': {
                    'total_productos': total_productos,
                    'productos_sin_stock': productos_sin_stock,
                    'valor_total_stock': round(total_valor_stock, 2)
                },
                'productos': productos,
                'por_categoria': por_categoria
            }

        except Exception as e:
            raise DatabaseError(
                f"Error generando informe de stock",
                details={'producto_ids': producto_ids, 'error': str(e)}
            )

