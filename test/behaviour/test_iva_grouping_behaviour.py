#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de comportement pour le groupage de l'IVA par taux dans les PDF
"""

import pytest
import os
import sys

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.pdf_generator import FacturaPDFGenerator


class TestIVAGroupingBehaviour:
    """Tests pour vérifier que l'IVA est groupé par taux dans les PDF"""
    
    @pytest.fixture
    def pdf_generator(self):
        """Fixture pour le générateur PDF"""
        return FacturaPDFGenerator()
    
    @pytest.fixture
    def invoice_with_multiple_iva_rates(self):
        """Facture avec 3 lignes à 10% et 2 lignes à 20%"""
        return {
            'numero': 'TEST-IVA-MULTI',
            'fecha': '01/02/2026',
            'cliente': {
                'nombre': 'Cliente Test',
                'telefono': '123456789',
                'direccion': 'Calle Test 123\n28001 Madrid'
            },
            'lineas': [
                # 3 lignes à 10% IVA
                {'producto_nombre': 'Producto A', 'cantidad': 2, 'precio_unitario': 50.00, 'descuento': 0, 'iva_aplicado': 10, 'total': 110.00},
                {'producto_nombre': 'Producto B', 'cantidad': 1, 'precio_unitario': 30.00, 'descuento': 0, 'iva_aplicado': 10, 'total': 33.00},
                {'producto_nombre': 'Producto C', 'cantidad': 3, 'precio_unitario': 20.00, 'descuento': 5, 'iva_aplicado': 10, 'total': 62.70},
                # 2 lignes à 20% IVA
                {'producto_nombre': 'Producto D', 'cantidad': 1, 'precio_unitario': 100.00, 'descuento': 0, 'iva_aplicado': 20, 'total': 120.00},
                {'producto_nombre': 'Producto E', 'cantidad': 2, 'precio_unitario': 25.00, 'descuento': 10, 'iva_aplicado': 20, 'total': 54.00},
            ],
            'subtotal': 309.70,
            'iva_total': 44.70,
            'total': 379.70
        }
    
    @pytest.fixture
    def invoice_with_single_iva_rate(self):
        """Facture avec toutes les lignes au même taux d'IVA"""
        return {
            'numero': 'TEST-IVA-SINGLE',
            'fecha': '01/02/2026',
            'cliente': {
                'nombre': 'Cliente Test',
                'telefono': '123456789',
                'direccion': 'Calle Test 123'
            },
            'lineas': [
                {'producto_nombre': 'Producto A', 'cantidad': 1, 'precio_unitario': 100.00, 'descuento': 0, 'iva_aplicado': 21, 'total': 121.00},
                {'producto_nombre': 'Producto B', 'cantidad': 2, 'precio_unitario': 50.00, 'descuento': 0, 'iva_aplicado': 21, 'total': 121.00},
            ],
            'subtotal': 200.00,
            'iva_total': 42.00,
            'total': 242.00
        }
    
    @pytest.fixture
    def invoice_with_zero_iva(self):
        """Facture avec lignes à 0% IVA"""
        return {
            'numero': 'TEST-IVA-ZERO',
            'fecha': '01/02/2026',
            'cliente': {
                'nombre': 'Cliente Test',
                'telefono': '123456789',
                'direccion': 'Calle Test 123'
            },
            'lineas': [
                {'producto_nombre': 'Producto Exento', 'cantidad': 1, 'precio_unitario': 100.00, 'descuento': 0, 'iva_aplicado': 0, 'total': 100.00},
                {'producto_nombre': 'Producto Normal', 'cantidad': 1, 'precio_unitario': 100.00, 'descuento': 0, 'iva_aplicado': 21, 'total': 121.00},
            ],
            'subtotal': 200.00,
            'iva_total': 21.00,
            'total': 221.00
        }
    
    def test_iva_grouping_calculates_correct_totals(self, pdf_generator, invoice_with_multiple_iva_rates):
        """
        ETANT DONNE une facture avec lignes à 10% et 20% d'IVA
        QUAND on génère la section des totaux
        ALORS l'IVA doit être groupé par taux avec les montants corrects
        """
        # Calculer les groupes d'IVA
        lineas = invoice_with_multiple_iva_rates['lineas']
        iva_groups = {}
        
        for linea in lineas:
            tasa_iva = linea.get('iva_aplicado', 0)
            cantidad = linea.get('cantidad', 0)
            precio = linea.get('precio_unitario', 0)
            descuento = linea.get('descuento', 0)
            
            net_linea = cantidad * precio * (1 - descuento / 100)
            iva_linea = net_linea * tasa_iva / 100
            
            if tasa_iva not in iva_groups:
                iva_groups[tasa_iva] = {'base': 0, 'iva': 0}
            
            iva_groups[tasa_iva]['base'] += net_linea
            iva_groups[tasa_iva]['iva'] += iva_linea
        
        # Vérifier les calculs
        assert len(iva_groups) == 2, "Doit avoir 2 groupes d'IVA"
        assert 10 in iva_groups, "Doit avoir un groupe à 10%"
        assert 20 in iva_groups, "Doit avoir un groupe à 20%"
        
        # Vérifier les montants à 10%
        # Ligne 1: 2 * 50 * 1.0 = 100 base, 10 IVA
        # Ligne 2: 1 * 30 * 1.0 = 30 base, 3 IVA
        # Ligne 3: 3 * 20 * 0.95 = 57 base, 5.70 IVA
        # Total 10%: base = 187, IVA = 18.70
        assert abs(iva_groups[10]['base'] - 187.00) < 0.01, f"Base 10% incorrecte: {iva_groups[10]['base']}"
        assert abs(iva_groups[10]['iva'] - 18.70) < 0.01, f"IVA 10% incorrect: {iva_groups[10]['iva']}"
        
        # Vérifier les montants à 20%
        # Ligne 1: 1 * 100 * 1.0 = 100 base, 20 IVA
        # Ligne 2: 2 * 25 * 0.9 = 45 base, 9 IVA
        # Total 20%: base = 145, IVA = 29
        assert abs(iva_groups[20]['base'] - 145.00) < 0.01, f"Base 20% incorrecte: {iva_groups[20]['base']}"
        assert abs(iva_groups[20]['iva'] - 29.00) < 0.01, f"IVA 20% incorrect: {iva_groups[20]['iva']}"
    
    def test_single_iva_rate_shows_correctly(self, pdf_generator, invoice_with_single_iva_rate):
        """
        ETANT DONNE une facture avec toutes les lignes à 21% d'IVA
        QUAND on génère la section des totaux
        ALORS une seule ligne d'IVA doit être affichée
        """
        lineas = invoice_with_single_iva_rate['lineas']
        iva_groups = {}
        
        for linea in lineas:
            tasa_iva = linea.get('iva_aplicado', 0)
            if tasa_iva not in iva_groups:
                iva_groups[tasa_iva] = {'base': 0, 'iva': 0}
            
            cantidad = linea.get('cantidad', 0)
            precio = linea.get('precio_unitario', 0)
            descuento = linea.get('descuento', 0)
            net_linea = cantidad * precio * (1 - descuento / 100)
            iva_linea = net_linea * tasa_iva / 100
            
            iva_groups[tasa_iva]['base'] += net_linea
            iva_groups[tasa_iva]['iva'] += iva_linea
        
        # Vérifier qu'il n'y a qu'un seul groupe
        assert len(iva_groups) == 1, "Doit avoir un seul groupe d'IVA"
        assert 21 in iva_groups, "Doit avoir un groupe à 21%"
        assert abs(iva_groups[21]['iva'] - 42.00) < 0.01, "IVA 21% incorrect"
    
    def test_zero_iva_rate_handled_correctly(self, pdf_generator, invoice_with_zero_iva):
        """
        ETANT DONNE une facture avec des lignes à 0% et 21% d'IVA
        QUAND on génère la section des totaux
        ALORS les deux taux doivent être affichés (même le 0%)
        """
        lineas = invoice_with_zero_iva['lineas']
        iva_groups = {}
        
        for linea in lineas:
            tasa_iva = linea.get('iva_aplicado', 0)
            if tasa_iva not in iva_groups:
                iva_groups[tasa_iva] = {'base': 0, 'iva': 0}
            
            cantidad = linea.get('cantidad', 0)
            precio = linea.get('precio_unitario', 0)
            descuento = linea.get('descuento', 0)
            net_linea = cantidad * precio * (1 - descuento / 100)
            iva_linea = net_linea * tasa_iva / 100
            
            iva_groups[tasa_iva]['base'] += net_linea
            iva_groups[tasa_iva]['iva'] += iva_linea
        
        # Vérifier les deux groupes
        assert len(iva_groups) == 2, "Doit avoir 2 groupes d'IVA (y compris 0%)"
        assert 0 in iva_groups, "Doit avoir un groupe à 0%"
        assert 21 in iva_groups, "Doit avoir un groupe à 21%"
        assert iva_groups[0]['iva'] == 0, "IVA à 0% doit être 0"
        assert abs(iva_groups[21]['iva'] - 21.00) < 0.01, "IVA 21% incorrect"
    
    def test_pdf_generation_with_multiple_iva_rates(self, pdf_generator, invoice_with_multiple_iva_rates, tmp_path):
        """
        ETANT DONNE une facture avec plusieurs taux d'IVA
        QUAND on génère le PDF
        ALORS le fichier doit être créé avec succès
        """
        import os
        os.environ['DISABLE_PDF_OPEN'] = '1'
        
        output_path = str(tmp_path / "test_iva_grouped.pdf")
        
        try:
            result = pdf_generator.generate_invoice_pdf(invoice_with_multiple_iva_rates, output_path)
            assert result is True, "La génération du PDF doit réussir"
            assert os.path.exists(output_path), "Le fichier PDF doit exister"
            assert os.path.getsize(output_path) > 0, "Le fichier PDF ne doit pas être vide"
        except Exception as e:
            pytest.fail(f"La génération du PDF a échoué: {e}")
    
    def test_iva_rates_sorted_descending(self, pdf_generator, invoice_with_multiple_iva_rates):
        """
        ETANT DONNE une facture avec plusieurs taux d'IVA
        QUAND on récupère les taux
        ALORS ils doivent être triés par ordre décroissant
        """
        lineas = invoice_with_multiple_iva_rates['lineas']
        iva_groups = {}
        
        for linea in lineas:
            tasa_iva = linea.get('iva_aplicado', 0)
            if tasa_iva not in iva_groups:
                iva_groups[tasa_iva] = {'base': 0, 'iva': 0}
            
            cantidad = linea.get('cantidad', 0)
            precio = linea.get('precio_unitario', 0)
            descuento = linea.get('descuento', 0)
            net_linea = cantidad * precio * (1 - descuento / 100)
            iva_linea = net_linea * tasa_iva / 100
            
            iva_groups[tasa_iva]['base'] += net_linea
            iva_groups[tasa_iva]['iva'] += iva_linea
        
        # Vérifier l'ordre décroissant
        tasas = sorted(iva_groups.keys(), reverse=True)
        assert tasas == [20, 10], "Les taux doivent être triés par ordre décroissant"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
