"""
Excepciones personalizadas para la aplicación Facturación Fácil
"""


class FacturacionError(Exception):
    """Excepción base para todos los errores de la aplicación"""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class DatabaseError(FacturacionError):
    """Errores relacionados con la base de datos"""
    pass


class DatabaseConnectionError(DatabaseError):
    """Error al conectar con la base de datos"""
    pass


class DatabaseQueryError(DatabaseError):
    """Error al ejecutar una consulta"""
    pass


class DatabaseIntegrityError(DatabaseError):
    """Error de integridad de datos"""
    pass


class ValidationError(FacturacionError):
    """Errores de validación de datos"""
    pass


class ClientValidationError(ValidationError):
    """Error de validación de datos de cliente"""
    pass


class ProductValidationError(ValidationError):
    """Error de validación de datos de producto"""
    pass


class InvoiceValidationError(ValidationError):
    """Error de validación de datos de factura"""
    pass


class OrganizationValidationError(ValidationError):
    """Error de validación de datos de organización"""
    pass


class BusinessLogicError(FacturacionError):
    """Errores de lógica de negocio"""
    pass


class InsufficientStockError(BusinessLogicError):
    """Stock insuficiente para completar la operación"""
    def __init__(self, product_name: str, requested: int, available: int):
        message = f"Stock insuficiente para '{product_name}'"
        details = {
            'producto': product_name,
            'solicitado': requested,
            'disponible': available
        }
        super().__init__(message, details)


class DuplicateInvoiceNumberError(BusinessLogicError):
    """Número de factura duplicado"""
    def __init__(self, invoice_number: str):
        message = f"El número de factura '{invoice_number}' ya existe"
        details = {'numero_factura': invoice_number}
        super().__init__(message, details)


class FileOperationError(FacturacionError):
    """Errores relacionados con operaciones de archivos"""
    pass


class PDFGenerationError(FileOperationError):
    """Error al generar un PDF"""
    pass


class ImageProcessingError(FileOperationError):
    """Error al procesar una imagen"""
    pass


class ConfigurationError(FacturacionError):
    """Errores de configuración"""
    pass


class MissingConfigurationError(ConfigurationError):
    """Configuración requerida no encontrada"""
    def __init__(self, config_key: str):
        message = f"Configuración requerida no encontrada: '{config_key}'"
        details = {'clave': config_key}
        super().__init__(message, details)


class UIError(FacturacionError):
    """Errores relacionados con la interfaz de usuario"""
    pass


class WidgetNotFoundError(UIError):
    """Widget no encontrado en la interfaz"""
    def __init__(self, widget_name: str):
        message = f"Widget no encontrado: '{widget_name}'"
        details = {'widget': widget_name}
        super().__init__(message, details)


class InvalidOperationError(FacturacionError):
    """Operación inválida en el contexto actual"""
    pass


class PermissionError(FacturacionError):
    """Error de permisos"""
    pass


class DataNotFoundError(FacturacionError):
    """Datos no encontrados"""
    def __init__(self, entity_type: str, entity_id: any):
        message = f"{entity_type} no encontrado"
        details = {'tipo': entity_type, 'id': entity_id}
        super().__init__(message, details)


class ClientNotFoundError(DataNotFoundError):
    """Cliente no encontrado"""
    def __init__(self, client_id: int):
        super().__init__("Cliente", client_id)


class ProductNotFoundError(DataNotFoundError):
    """Producto no encontrado"""
    def __init__(self, product_id: int):
        super().__init__("Producto", product_id)


class InvoiceNotFoundError(DataNotFoundError):
    """Factura no encontrada"""
    def __init__(self, invoice_id: int):
        super().__init__("Factura", invoice_id)


class OrganizationNotFoundError(DataNotFoundError):
    """Organización no encontrada"""
    def __init__(self, org_id: int = 1):
        super().__init__("Organización", org_id)

