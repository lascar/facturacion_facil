# -*- coding: utf-8 -*-
"""
Tests para los validadores comunes
"""
import pytest
from common.validators import FormValidator, CalculationHelper, ValidationError

class TestFormValidator:
    """Tests para FormValidator"""
    
    def test_validate_required_field_valid(self):
        """Test validación de campo requerido válido"""
        result = FormValidator.validate_required_field("Valor válido", "Campo Test")
        assert result is None
    
    def test_validate_required_field_empty(self):
        """Test validación de campo requerido vacío"""
        result = FormValidator.validate_required_field("", "Campo Test")
        assert result is not None
        assert "Campo Test" in result
        assert "requerido" in result
    
    def test_validate_required_field_whitespace(self):
        """Test validación de campo con solo espacios"""
        result = FormValidator.validate_required_field("   ", "Campo Test")
        assert result is not None
        assert "Campo Test" in result
    
    def test_validate_required_field_none(self):
        """Test validación de campo None"""
        result = FormValidator.validate_required_field(None, "Campo Test")
        assert result is not None
    
    def test_validate_precio_valid(self):
        """Test validación de precio válido"""
        valid_prices = ["10.50", "0", "0.01", "999.99", "1000"]
        for price in valid_prices:
            result = FormValidator.validate_precio(price)
            assert result is None, f"Precio {price} debería ser válido"
    
    def test_validate_precio_invalid(self):
        """Test validación de precio inválido"""
        invalid_prices = ["-10", "abc", "", "10.5.5", "-0.01"]
        for price in invalid_prices:
            result = FormValidator.validate_precio(price)
            assert result is not None, f"Precio {price} debería ser inválido"
            assert "precio" in result.lower()
    
    def test_validate_cantidad_valid(self):
        """Test validación de cantidad válida"""
        valid_quantities = ["1", "10", "100", "0"]
        for qty in valid_quantities:
            result = FormValidator.validate_cantidad(qty)
            assert result is None, f"Cantidad {qty} debería ser válida"
    
    def test_validate_cantidad_invalid(self):
        """Test validación de cantidad inválida"""
        invalid_quantities = ["-1", "1.5", "abc", "", "10.0"]
        for qty in invalid_quantities:
            result = FormValidator.validate_cantidad(qty)
            assert result is not None, f"Cantidad {qty} debería ser inválida"
            assert "cantidad" in result.lower()
    
    def test_validate_iva_valid(self):
        """Test validación de IVA válido"""
        valid_ivas = ["0", "21", "10.5", "100", "4"]
        for iva in valid_ivas:
            result = FormValidator.validate_iva(iva)
            assert result is None, f"IVA {iva} debería ser válido"
    
    def test_validate_iva_invalid(self):
        """Test validación de IVA inválido"""
        invalid_ivas = ["-1", "101", "abc", "", "21.5.5"]
        for iva in invalid_ivas:
            result = FormValidator.validate_iva(iva)
            assert result is not None, f"IVA {iva} debería ser inválido"
            assert "iva" in result.lower()
    
    def test_validate_email_valid(self):
        """Test validación de email válido"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "test123@test-domain.com",
            ""  # Email vacío es válido (opcional)
        ]
        for email in valid_emails:
            result = FormValidator.validate_email(email)
            assert result is None, f"Email {email} debería ser válido"
    
    def test_validate_email_invalid(self):
        """Test validación de email inválido"""
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "test@",
            "test@domain",
            "test.domain.com"
        ]
        for email in invalid_emails:
            result = FormValidator.validate_email(email)
            assert result is not None, f"Email {email} debería ser inválido"
            assert "email" in result.lower()
    
    def test_validate_phone_valid(self):
        """Test validación de teléfono válido"""
        valid_phones = [
            "123456789",
            "+34 123 456 789",
            "(91) 123-4567",
            "91-123-4567",
            ""  # Teléfono vacío es válido (opcional)
        ]
        for phone in valid_phones:
            result = FormValidator.validate_phone(phone)
            assert result is None, f"Teléfono {phone} debería ser válido"
    
    def test_validate_phone_invalid(self):
        """Test validación de teléfono inválido"""
        invalid_phones = [
            "abc123",
            "123@456",
            "123#456"
        ]
        for phone in invalid_phones:
            result = FormValidator.validate_phone(phone)
            assert result is not None, f"Teléfono {phone} debería ser inválido"
    
    def test_validate_dni_nie_valid(self):
        """Test validación de DNI/NIE válido"""
        valid_docs = [
            "12345678A",
            "X1234567A",
            "Y1234567B",
            "Z1234567C",
            ""  # DNI vacío es válido (opcional)
        ]
        for doc in valid_docs:
            result = FormValidator.validate_dni_nie(doc)
            assert result is None, f"DNI/NIE {doc} debería ser válido"
    
    def test_validate_dni_nie_invalid(self):
        """Test validación de DNI/NIE inválido"""
        invalid_docs = [
            "1234567A",  # Muy corto
            "123456789A",  # Muy largo
            "12345678",  # Sin letra
            "A1234567A",  # Letra incorrecta al inicio
            "1234567AA"  # Dos letras al final
        ]
        for doc in invalid_docs:
            result = FormValidator.validate_dni_nie(doc)
            assert result is not None, f"DNI/NIE {doc} debería ser inválido"

class TestCalculationHelper:
    """Tests para CalculationHelper"""
    
    def test_calculate_iva_amount(self):
        """Test cálculo de importe de IVA"""
        # 100€ con 21% IVA = 21€
        result = CalculationHelper.calculate_iva_amount(100, 21)
        assert abs(result - 21.0) < 0.01
        
        # 50€ con 10% IVA = 5€
        result = CalculationHelper.calculate_iva_amount(50, 10)
        assert abs(result - 5.0) < 0.01
        
        # 0€ con cualquier IVA = 0€
        result = CalculationHelper.calculate_iva_amount(0, 21)
        assert result == 0.0
    
    def test_calculate_iva_amount_invalid_input(self):
        """Test cálculo de IVA con entrada inválida"""
        result = CalculationHelper.calculate_iva_amount("invalid", 21)
        assert result == 0.0
        
        result = CalculationHelper.calculate_iva_amount(100, "invalid")
        assert result == 0.0
    
    def test_calculate_precio_con_iva(self):
        """Test cálculo de precio con IVA"""
        # 100€ + 21% IVA = 121€
        result = CalculationHelper.calculate_precio_con_iva(100, 21)
        assert abs(result - 121.0) < 0.01
        
        # 50€ + 10% IVA = 55€
        result = CalculationHelper.calculate_precio_con_iva(50, 10)
        assert abs(result - 55.0) < 0.01
        
        # 100€ + 0% IVA = 100€
        result = CalculationHelper.calculate_precio_con_iva(100, 0)
        assert abs(result - 100.0) < 0.01
    
    def test_calculate_line_total_basic(self):
        """Test cálculo básico de total de línea"""
        # 2 unidades × 10€ con 21% IVA = 24.2€
        result = CalculationHelper.calculate_line_total(10.0, 2, 21.0, 0)
        
        assert abs(result['subtotal'] - 20.0) < 0.01
        assert abs(result['descuento_amount'] - 0.0) < 0.01
        assert abs(result['iva_amount'] - 4.2) < 0.01
        assert abs(result['total'] - 24.2) < 0.01
    
    def test_calculate_line_total_with_discount(self):
        """Test cálculo de línea con descuento"""
        # 1 unidad × 100€ con 10% descuento y 21% IVA
        # Subtotal: 100€
        # Descuento: 10€
        # Base para IVA: 90€
        # IVA: 18.9€
        # Total: 108.9€
        result = CalculationHelper.calculate_line_total(100.0, 1, 21.0, 10.0)
        
        assert abs(result['subtotal'] - 90.0) < 0.01
        assert abs(result['descuento_amount'] - 10.0) < 0.01
        assert abs(result['iva_amount'] - 18.9) < 0.01
        assert abs(result['total'] - 108.9) < 0.01
    
    def test_calculate_line_total_complex(self):
        """Test cálculo complejo de línea"""
        # 3 unidades × 25€ con 15% descuento y 10% IVA
        # Subtotal base: 75€
        # Descuento: 11.25€
        # Base para IVA: 63.75€
        # IVA: 6.375€
        # Total: 70.125€
        result = CalculationHelper.calculate_line_total(25.0, 3, 10.0, 15.0)
        
        assert abs(result['subtotal'] - 63.75) < 0.01
        assert abs(result['descuento_amount'] - 11.25) < 0.01
        assert abs(result['iva_amount'] - 6.375) < 0.01
        assert abs(result['total'] - 70.125) < 0.01
    
    def test_calculate_line_total_invalid_input(self):
        """Test cálculo con entrada inválida"""
        result = CalculationHelper.calculate_line_total("invalid", 1, 21, 0)
        
        assert result['subtotal'] == 0.0
        assert result['descuento_amount'] == 0.0
        assert result['iva_amount'] == 0.0
        assert result['total'] == 0.0
    
    def test_format_currency(self):
        """Test formateo de moneda"""
        assert CalculationHelper.format_currency(123.45) == "123.45 €"
        assert CalculationHelper.format_currency(0) == "0.00 €"
        assert CalculationHelper.format_currency(1000.1) == "1000.10 €"
        
        # Con símbolo personalizado
        assert CalculationHelper.format_currency(100, "$") == "100.00 $"
    
    def test_format_currency_invalid_input(self):
        """Test formateo de moneda con entrada inválida"""
        assert CalculationHelper.format_currency("invalid") == "0.00 €"
        assert CalculationHelper.format_currency(None) == "0.00 €"
    
    def test_format_percentage(self):
        """Test formateo de porcentaje"""
        assert CalculationHelper.format_percentage(21) == "21.0%"
        assert CalculationHelper.format_percentage(10.5) == "10.5%"
        assert CalculationHelper.format_percentage(0) == "0.0%"
    
    def test_format_percentage_invalid_input(self):
        """Test formateo de porcentaje con entrada inválida"""
        assert CalculationHelper.format_percentage("invalid") == "0.0%"
        assert CalculationHelper.format_percentage(None) == "0.0%"
