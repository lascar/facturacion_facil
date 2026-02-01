#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la disposition du PDF de facture
"""

import os
import sys
from datetime import datetime

# Ajouter le répertoire racine au PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, root_dir)

from utils.pdf_generator import PDFGenerator
from utils.logger import get_logger

logger = get_logger("test_pdf_layout")

def test_pdf_generation():
    """Teste la génération d'un PDF avec la nouvelle disposition"""
    
    # Données de test pour une facture
    invoice_data = {
        'numero': '20250031',
        'fecha': '15/02/2025',
        'vencimiento': '15/03/2025',
        'estado': 'Pendiente',
        'cliente': {
            'nombre': 'Ventas IX marcha',
            'nif': 'B12345678',
            'direccion': 'Calle Ejemplo, 123\n28001 Madrid',
            'email': 'cliente@ejemplo.com',
            'telefono': '+34 91 123 45 67'
        },
        'lineas': [
            {
                'producto_referencia': 'CAM-001',
                'producto_nombre': 'Camiseta técnica oficial la Desbandá',
                'cantidad': 13,
                'precio_unitario': 16.53,
                'descuento': 0,
                'iva_aplicado': 21,
                'total': 214.89
            },
            {
                'producto_referencia': 'CAM-002',
                'producto_nombre': 'Camiseta algodón flecha',
                'cantidad': 4,
                'precio_unitario': 9.92,
                'descuento': 0,
                'iva_aplicado': 21,
                'total': 39.68
            },
            {
                'producto_referencia': 'CAM-003',
                'producto_nombre': 'Camiseta niña',
                'cantidad': 3,
                'precio_unitario': 8.27,
                'descuento': 0,
                'iva_aplicado': 21,
                'total': 24.81
            },
        ],
        'subtotal': 2054.81,
        'iva_total': 431.51,
        'total': 2486.32
    }
    
    # Créer le dossier de test si nécessaire (dans le dossier behaviour)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(script_dir, "test_pdfs")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        logger.info(f"Dossier de test créé: {test_dir}")
    
    # Générer le nom du fichier
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"Test_Factura_Layout_{timestamp}.pdf"
    pdf_path = os.path.join(test_dir, pdf_filename)
    
    # Créer le générateur PDF
    pdf_generator = PDFGenerator()
    
    # Générer le PDF
    logger.info(f"Génération du PDF de test: {pdf_path}")
    success = pdf_generator.generate_invoice_pdf(invoice_data, pdf_path)
    
    # Vérifier le succès avec assertion (pytest ne doit pas retourner de valeur)
    assert success, "Échec de la génération du PDF"
    
    logger.info(f"✅ PDF généré avec succès: {pdf_path}")
    print(f"\n✅ PDF de test généré avec succès!")
    print(f"📄 Fichier: {pdf_path}")
    print(f"\nVérifie que:")
    print(f"  1. Le logo est en haut à gauche")
    print(f"  2. Les informations de l'entreprise sont à côté du logo")
    print(f"  3. 'FACTURA' et le numéro sont en haut à droite")
    print(f"  4. Aucun bouton de l'interface n'est visible")
    
    # Ouvrir le PDF automatiquement (uniquement si exécuté directement, pas en pytest)
    if not os.environ.get('PYTEST_RUNNING'):
        try:
            import subprocess
            import platform
            
            sistema = platform.system().lower()
            if sistema == "linux":
                subprocess.run(["xdg-open", pdf_path], check=False)
            elif sistema == "darwin":
                subprocess.run(["open", pdf_path], check=False)
            elif sistema == "windows":
                os.startfile(pdf_path)
            
            logger.info("PDF ouvert automatiquement")
        except Exception as e:
            logger.warning(f"Impossible d'ouvrir automatiquement le PDF: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE DISPOSITION DU PDF DE FACTURE")
    print("=" * 60)
    print()
    
    try:
        test_pdf_generation()
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ {e}")
        sys.exit(1)

