# -*- coding: utf-8 -*-
"""
Service métier pour la gestion des factures
Sépare la logique métier de la présentation UI
"""

from typing import Optional, List, Dict, Any
from services.base_service import BaseService
from utils.decorators import log_execution, log_performance
from utils.exceptions import (
    InvoiceValidationError, InvoiceNotFoundError,
    DatabaseError, InsufficientStockError
)


class FacturaService(BaseService):
    """Service métier pour les factures"""
    
    @log_execution
    @log_performance(threshold_seconds=0.5)
    def get_all_facturas(self) -> List[Dict[str, Any]]:
        """
        Obtenir toutes les factures
        
        Returns:
            Liste de dictionnaires de factures
            
        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            return self.db.get_all_invoices()
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo facturas",
                details={'error': str(e)}
            )
    
    @log_execution
    def get_factura_by_id(self, factura_id: int) -> Dict[str, Any]:
        """
        Obtenir une facture par son ID
        
        Args:
            factura_id: ID de la facture
            
        Returns:
            Dictionnaire de la facture avec ses lignes
            
        Raises:
            InvoiceNotFoundError: Si la facture n'existe pas
            DatabaseError: En cas d'erreur de base de données
        """
        self.validate_id(factura_id, 'factura', InvoiceValidationError)
        
        try:
            factura = self.db.get_invoice_by_id(factura_id)
            if not factura:
                raise InvoiceNotFoundError(factura_id)
            return factura
        except InvoiceNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo factura {factura_id}",
                details={'id': factura_id, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.5)
    def create_factura(self, factura_data: Dict[str, Any]) -> int:
        """
        Créer une nouvelle facture
        
        Args:
            factura_data: Données de la facture (incluant 'lineas')
            
        Returns:
            ID de la facture créée
            
        Raises:
            InvoiceValidationError: Si les données sont invalides
            InsufficientStockError: Si le stock est insuffisant
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        self._validate_factura_data(factura_data)
        
        # Vérifier le stock si nécessaire
        if factura_data.get('lineas'):
            self._validate_stock_availability(factura_data['lineas'])
        
        try:
            factura_id = self.db.add_invoice(factura_data)
            self.logger.info(f"Factura creada con ID: {factura_id}")
            return factura_id
        except Exception as e:
            raise DatabaseError(
                f"Error creando factura",
                details={'data': factura_data, 'error': str(e)}
            )
    
    @log_execution
    @log_performance(threshold_seconds=0.5)
    def update_factura(self, factura_data: Dict[str, Any]) -> bool:
        """
        Mettre à jour une facture existante
        
        Args:
            factura_data: Données de la facture (doit contenir 'id')
            
        Returns:
            True si la mise à jour a réussi
            
        Raises:
            InvoiceValidationError: Si les données sont invalides
            InvoiceNotFoundError: Si la facture n'existe pas
            DatabaseError: En cas d'erreur de base de données
        """
        # Validation
        if 'id' not in factura_data:
            raise InvoiceValidationError(
                "ID de factura requerido para actualización",
                details={'data': factura_data}
            )
        
        self.validate_id(factura_data['id'], 'factura', InvoiceValidationError)
        self._validate_factura_data(factura_data)
        
        try:
            success = self.db.update_invoice(factura_data)
            if not success:
                raise InvoiceNotFoundError(factura_data['id'])
            self.logger.info(f"Factura {factura_data['id']} actualizada")
            return True
        except InvoiceNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error actualizando factura {factura_data.get('id')}",
                details={'data': factura_data, 'error': str(e)}
            )

    @log_execution
    def delete_factura(self, factura_id: int) -> bool:
        """
        Supprimer une facture

        Args:
            factura_id: ID de la facture à supprimer

        Returns:
            True si la suppression a réussi

        Raises:
            InvoiceValidationError: Si l'ID est invalide
            DatabaseError: En cas d'erreur de base de données
        """
        self.validate_id(factura_id, 'factura', InvoiceValidationError)

        try:
            success = self.db.delete_invoice(factura_id)
            self.logger.info(f"Factura {factura_id} eliminada")
            return success
        except Exception as e:
            raise DatabaseError(
                f"Error eliminando factura {factura_id}",
                details={'id': factura_id, 'error': str(e)}
            )

    @log_execution
    def calculate_totals(self, lineas: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculer les totaux d'une facture

        Args:
            lineas: Liste des lignes de la facture

        Returns:
            Dictionnaire avec subtotal, iva_total, total

        Raises:
            InvoiceValidationError: Si les données sont invalides
        """
        if not lineas:
            return {
                'subtotal': 0.0,
                'iva_total': 0.0,
                'total': 0.0
            }

        try:
            subtotal = 0.0
            iva_total = 0.0

            for linea in lineas:
                cantidad = float(linea.get('cantidad', 0))
                precio_unitario = float(linea.get('precio_unitario', 0))
                iva_porcentaje = float(linea.get('iva', 0))

                linea_subtotal = cantidad * precio_unitario
                linea_iva = linea_subtotal * (iva_porcentaje / 100)

                subtotal += linea_subtotal
                iva_total += linea_iva

            total = subtotal + iva_total

            return {
                'subtotal': round(subtotal, 2),
                'iva_total': round(iva_total, 2),
                'total': round(total, 2)
            }
        except (ValueError, TypeError, KeyError) as e:
            raise InvoiceValidationError(
                f"Error calculando totales",
                details={'lineas': lineas, 'error': str(e)}
            )

    def get_last_invoice_number(self) -> Optional[str]:
        """
        Obtenir le dernier numéro de facture

        Returns:
            Dernier numéro de facture ou None

        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            return self.db.get_last_invoice_number()
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo último número de factura",
                details={'error': str(e)}
            )

    def generate_factura_number(self) -> str:
        """
        Générer un nouveau numéro de facture en respectant la configuration

        Returns:
            Nouveau numéro de facture (format selon config ou FAC-XXXX)

        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            from utils.factura_numbering import FacturaNumberingService
            
            # Utiliser le service de numérotation qui respecte la configuration
            numbering_service = FacturaNumberingService(self.db)
            numero = numbering_service.get_next_numero_factura()
            
            self.logger.info(f"Número de factura generado: {numero}")
            return numero

        except Exception as e:
            # En cas d'erreur, fallback vers l'ancienne méthode
            self.logger.warning(f"Error usando FacturaNumberingService, usando fallback: {e}")
            
            try:
                last_number = self.get_last_invoice_number()
                if last_number:
                    import re
                    match = re.search(r'(\d+)$', last_number)
                    if match:
                        next_num = int(match.group(1)) + 1
                        return f"FAC-{next_num:04d}"
                return "FAC-0001"
            except Exception as e2:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                self.logger.error(f"Error en fallback: {e2}")
                return f"FAC-{timestamp}"

    def _validate_factura_data(self, data: Dict[str, Any]) -> None:
        """
        Valider les données d'une facture

        Args:
            data: Données de la facture à valider

        Raises:
            InvoiceValidationError: Si les données sont invalides
        """
        # Champs requis
        required_fields = ['numero', 'fecha']
        self.validate_required_fields(data, required_fields, InvoiceValidationError)

        # Validation du client
        if 'cliente' in data:
            cliente = data['cliente']
            if not isinstance(cliente, dict) or not cliente.get('nombre'):
                raise InvoiceValidationError(
                    "Cliente inválido o sin nombre",
                    details={'cliente': cliente}
                )

        # Validation des montants
        if 'subtotal' in data:
            self.validate_positive_number(data['subtotal'], 'subtotal', InvoiceValidationError)

        if 'total' in data:
            self.validate_positive_number(data['total'], 'total', InvoiceValidationError)

        # Validation des lignes
        if 'lineas' in data:
            if not isinstance(data['lineas'], list):
                raise InvoiceValidationError(
                    "Líneas debe ser una lista",
                    details={'lineas': data['lineas']}
                )

            for i, linea in enumerate(data['lineas']):
                self._validate_linea(linea, i)

    def _validate_linea(self, linea: Dict[str, Any], index: int) -> None:
        """
        Valider une ligne de facture

        Args:
            linea: Données de la ligne
            index: Index de la ligne dans la liste

        Raises:
            InvoiceValidationError: Si les données sont invalides
        """
        # Champs requis
        if 'producto_id' not in linea:
            raise InvoiceValidationError(
                f"Línea {index}: producto_id requerido",
                details={'linea': linea, 'index': index}
            )

        if 'cantidad' not in linea:
            raise InvoiceValidationError(
                f"Línea {index}: cantidad requerida",
                details={'linea': linea, 'index': index}
            )

        if 'precio_unitario' not in linea:
            raise InvoiceValidationError(
                f"Línea {index}: precio_unitario requerido",
                details={'linea': linea, 'index': index}
            )

        # Validation des valeurs
        try:
            cantidad = int(linea['cantidad'])
            if cantidad <= 0:
                raise InvoiceValidationError(
                    f"Línea {index}: cantidad debe ser mayor que 0",
                    details={'cantidad': cantidad, 'index': index}
                )
        except (ValueError, TypeError):
            raise InvoiceValidationError(
                f"Línea {index}: cantidad inválida",
                details={'cantidad': linea['cantidad'], 'index': index}
            )

        try:
            precio = float(linea['precio_unitario'])
            if precio < 0:
                raise InvoiceValidationError(
                    f"Línea {index}: precio_unitario no puede ser negativo",
                    details={'precio': precio, 'index': index}
                )
        except (ValueError, TypeError):
            raise InvoiceValidationError(
                f"Línea {index}: precio_unitario inválido",
                details={'precio': linea['precio_unitario'], 'index': index}
            )

    def _validate_stock_availability(self, lineas: List[Dict[str, Any]]) -> None:
        """
        Vérifier la disponibilité du stock pour les lignes de facture
        Salta la verificación para productos marcados como "sin stock"

        Args:
            lineas: Liste des lignes de la facture

        Raises:
            InsufficientStockError: Si le stock est insuffisant
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            for linea in lineas:
                producto_id = linea.get('producto_id')
                cantidad = int(linea.get('cantidad', 0))

                # Obtenir le produit
                producto = self.db.get_product_by_id(producto_id)
                if not producto:
                    raise InvoiceValidationError(
                        f"Producto {producto_id} no encontrado",
                        details={'producto_id': producto_id}
                    )

                # Vérifier le stock (solo si el producto gestiona stock)
                sin_stock = producto.get('sin_stock', 0)
                if not sin_stock:
                    stock_actual = producto.get('stock_actual', 0)
                    if stock_actual < cantidad:
                        raise InsufficientStockError(
                            producto.get('nombre', 'producto'),
                            cantidad,
                            stock_actual
                        )
        except (InsufficientStockError, InvoiceValidationError):
            raise
        except Exception as e:
            raise DatabaseError(
                f"Error verificando stock",
                details={'error': str(e)}
            )

    @log_execution
    def delete_factura(self, factura_id: int) -> bool:
        """
        Supprimer une facture

        Args:
            factura_id: ID de la facture à supprimer

        Returns:
            True si la suppression a réussi

        Raises:
            InvoiceValidationError: Si l'ID est invalide
            DatabaseError: En cas d'erreur de base de données
        """
        self.validate_id(factura_id, 'factura', InvoiceValidationError)

        try:
            success = self.db.delete_invoice(factura_id)
            self.logger.info(f"Factura {factura_id} eliminada")
            return success
        except Exception as e:
            raise DatabaseError(
                f"Error eliminando factura {factura_id}",
                details={'id': factura_id, 'error': str(e)}
            )

    @log_execution
    def calculate_totals(self, lineas: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculer les totaux d'une facture

        Args:
            lineas: Liste des lignes de la facture

        Returns:
            Dictionnaire avec subtotal, iva_total, total

        Raises:
            InvoiceValidationError: Si les données sont invalides
        """
        if not lineas:
            return {
                'subtotal': 0.0,
                'iva_total': 0.0,
                'total': 0.0
            }

        try:
            subtotal = 0.0
            iva_total = 0.0

            for linea in lineas:
                cantidad = float(linea.get('cantidad', 0))
                precio_unitario = float(linea.get('precio_unitario', 0))
                iva_porcentaje = float(linea.get('iva', 0))

                linea_subtotal = cantidad * precio_unitario
                linea_iva = linea_subtotal * (iva_porcentaje / 100)

                subtotal += linea_subtotal
                iva_total += linea_iva

            total = subtotal + iva_total

            return {
                'subtotal': round(subtotal, 2),
                'iva_total': round(iva_total, 2),
                'total': round(total, 2)
            }
        except (ValueError, TypeError, KeyError) as e:
            raise InvoiceValidationError(
                f"Error calculando totales",
                details={'lineas': lineas, 'error': str(e)}
            )

    def get_last_invoice_number(self) -> Optional[str]:
        """
        Obtenir le dernier numéro de facture

        Returns:
            Dernier numéro de facture ou None

        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            return self.db.get_last_invoice_number()
        except Exception as e:
            raise DatabaseError(
                f"Error obteniendo último número de factura",
                details={'error': str(e)}
            )

    def generate_factura_number(self) -> str:
        """
        Générer un nouveau numéro de facture en respectant la configuration

        Returns:
            Nouveau numéro de facture (format selon config ou FAC-XXXX)

        Raises:
            DatabaseError: En cas d'erreur de base de données
        """
        try:
            from utils.factura_numbering import FacturaNumberingService
            
            # Utiliser le service de numérotation qui respecte la configuration
            numbering_service = FacturaNumberingService(self.db)
            numero = numbering_service.get_next_numero_factura()
            
            self.logger.info(f"Número de factura generado: {numero}")
            return numero

        except Exception as e:
            # En cas d'erreur, fallback vers l'ancienne méthode
            self.logger.warning(f"Error usando FacturaNumberingService, usando fallback: {e}")
            
            try:
                last_number = self.get_last_invoice_number()
                if last_number:
                    import re
                    match = re.search(r'(\d+)$', last_number)
                    if match:
                        next_num = int(match.group(1)) + 1
                        return f"FAC-{next_num:04d}"
                return "FAC-0001"
            except Exception as e2:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                self.logger.error(f"Error en fallback: {e2}")
                return f"FAC-{timestamp}"

