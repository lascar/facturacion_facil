import pytest
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.translations import get_text, TEXTS

class TestTranslations:
    """Tests pour le système de traductions"""
    
    def test_get_text_existing_key(self):
        """Test la récupération d'un texte existant"""
        text = get_text("app_title")
        assert text == "Facturación Fácil"
        assert isinstance(text, str)
    
    def test_get_text_non_existing_key(self):
        """Test la récupération d'une clé inexistante"""
        text = get_text("non_existing_key")
        assert text == "non_existing_key"  # Retourne la clé elle-même
    
    def test_get_text_empty_key(self):
        """Test avec une clé vide"""
        text = get_text("")
        assert text == ""
    
    def test_get_text_none_key(self):
        """Test avec une clé None"""
        text = get_text(None)
        assert text is None
    
    def test_all_main_sections_have_translations(self):
        """Test que toutes les sections principales ont des traductions"""
        required_keys = [
            "app_title",
            "productos", 
            "organizacion",
            "stock",
            "facturas",
            "nueva_factura",
            "salir"
        ]
        
        for key in required_keys:
            assert key in TEXTS, f"Missing translation for key: {key}"
            assert TEXTS[key] != "", f"Empty translation for key: {key}"
    
    def test_producto_fields_have_translations(self):
        """Test que tous les champs de produit ont des traductions"""
        producto_keys = [
            "nombre",
            "referencia", 
            "precio",
            "cantidad",
            "categoria",
            "descripcion",
            "imagen",
            "iva_recomendado"
        ]
        
        for key in producto_keys:
            assert key in TEXTS, f"Missing translation for producto field: {key}"
            assert TEXTS[key] != "", f"Empty translation for producto field: {key}"
    
    def test_organizacion_fields_have_translations(self):
        """Test que tous les champs d'organisation ont des traductions"""
        org_keys = [
            "nombre_empresa",
            "direccion",
            "telefono", 
            "email",
            "cif",
            "logo"
        ]
        
        for key in org_keys:
            assert key in TEXTS, f"Missing translation for organizacion field: {key}"
            assert TEXTS[key] != "", f"Empty translation for organizacion field: {key}"
    
    def test_factura_fields_have_translations(self):
        """Test que tous les champs de facture ont des traductions"""
        factura_keys = [
            "nombre_cliente",
            "dni_nie",
            "direccion_cliente",
            "email_cliente",
            "telefono_cliente",
            "fecha_factura",
            "numero_factura",
            "precio_unitario",
            "precio_total",
            "iva_aplicado",
            "subtotal",
            "total_iva",
            "total_factura",
            "modo_pago"
        ]
        
        for key in factura_keys:
            assert key in TEXTS, f"Missing translation for factura field: {key}"
            assert TEXTS[key] != "", f"Empty translation for factura field: {key}"
    
    def test_button_texts_have_translations(self):
        """Test que tous les textes de boutons ont des traductions"""
        button_keys = [
            "guardar",
            "cancelar",
            "si",
            "no", 
            "aceptar",
            "buscar",
            "limpiar",
            "nuevo_producto",
            "editar_producto",
            "eliminar_producto"
        ]
        
        for key in button_keys:
            assert key in TEXTS, f"Missing translation for button: {key}"
            assert TEXTS[key] != "", f"Empty translation for button: {key}"
    
    def test_message_texts_have_translations(self):
        """Test que tous les messages ont des traductions"""
        message_keys = [
            "producto_guardado",
            "producto_eliminado",
            "organizacion_guardada",
            "stock_actualizado",
            "factura_generada",
            "error",
            "confirmar",
            "confirmar_eliminacion",
            "campo_requerido",
            "precio_invalido",
            "cantidad_invalida",
            "iva_invalido"
        ]
        
        for key in message_keys:
            assert key in TEXTS, f"Missing translation for message: {key}"
            assert TEXTS[key] != "", f"Empty translation for message: {key}"
    
    def test_payment_methods_have_translations(self):
        """Test que les modes de paiement ont des traductions"""
        payment_keys = ["efectivo", "tarjeta", "transferencia"]
        
        for key in payment_keys:
            assert key in TEXTS, f"Missing translation for payment method: {key}"
            assert TEXTS[key] != "", f"Empty translation for payment method: {key}"
    
    def test_translations_are_in_spanish(self):
        """Test que les traductions sont bien en espagnol"""
        spanish_indicators = {
            "app_title": ["Facturación", "Fácil"],
            "productos": ["Productos"],
            "organizacion": ["Organización"],
            "nueva_factura": ["Nueva", "Factura"],
            "guardar": ["Guardar"],
            "cancelar": ["Cancelar"],
            "confirmar_eliminacion": ["seguro", "eliminar"]
        }
        
        for key, indicators in spanish_indicators.items():
            text = TEXTS[key]
            for indicator in indicators:
                assert indicator.lower() in text.lower(), f"Translation for {key} doesn't seem to be in Spanish"
    
    def test_no_empty_translations(self):
        """Test qu'aucune traduction n'est vide"""
        for key, value in TEXTS.items():
            assert value != "", f"Empty translation for key: {key}"
            assert value is not None, f"None translation for key: {key}"
    
    def test_translations_consistency(self):
        """Test la cohérence des traductions"""
        # Vérifier que les termes similaires sont traduits de manière cohérente
        assert TEXTS["nombre"] == "Nombre"  # Utilisé pour produit et client
        assert TEXTS["email"] == "Email"    # Utilisé pour organisation et client
        assert TEXTS["telefono"] == "Teléfono"  # Utilisé pour organisation et client
        
    def test_special_characters_in_translations(self):
        """Test que les caractères spéciaux espagnols sont présents"""
        spanish_chars = ['ñ', 'á', 'é', 'í', 'ó', 'ú', 'ü']
        
        # Compter les occurrences de caractères espagnols
        all_text = " ".join(TEXTS.values()).lower()
        spanish_char_count = sum(1 for char in all_text if char in spanish_chars)
        
        # Il devrait y avoir au moins quelques caractères espagnols
        assert spanish_char_count > 0, "No Spanish special characters found in translations"
    
    @pytest.mark.parametrize("key,expected_type", [
        ("app_title", str),
        ("productos", str),
        ("precio", str),
        ("guardar", str),
        ("error", str)
    ])
    def test_translation_types(self, key, expected_type):
        """Test que les traductions sont du bon type"""
        text = get_text(key)
        assert isinstance(text, expected_type), f"Translation for {key} is not of type {expected_type}"
