# -*- coding: utf-8 -*-
"""
Générateur de PDF pour les rapports (Informes)
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from utils.logger import get_logger


class InformePDFGenerator:
    """Générateur de PDF pour les rapports de facturation et stock"""

    def __init__(self):
        self.logger = get_logger("informe_pdf_generator")
        self.page_width, self.page_height = A4
        self.margin = 2 * cm

        # Styles
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Configure les styles personnalisés"""
        # Style pour le titre principal
        self.styles.add(ParagraphStyle(
            name='TitleStyle',
            parent=self.styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2c3e50'),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            spaceAfter=20
        ))

        # Style pour les sous-titres
        self.styles.add(ParagraphStyle(
            name='SubtitleStyle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            fontName='Helvetica-Bold',
            spaceAfter=10
        ))

        # Style pour les totaux
        self.styles.add(ParagraphStyle(
            name='TotalStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#e74c3c'),
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        ))

    def generate_facturacion_pdf(self, informe_data, output_path):
        """Génère un PDF de rapport de facturation"""
        try:
            self.logger.info(f"Generando PDF de informe de facturación: {output_path}")

            # Créer le document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )

            # Construire le contenu
            story = []

            # Titre
            periodo = informe_data.get('periodo', {})
            title = f"Informe de Facturación<br/>{periodo.get('inicio', '')} - {periodo.get('fin', '')}"
            story.append(Paragraph(title, self.styles['TitleStyle']))
            story.append(Spacer(1, 20))

            # Liste des clients (au début)
            story.extend(self.create_lista_clientes(informe_data))

            # Liste des factures avec désglose IVA
            story.extend(self.create_facturas_detalladas_table(informe_data))

            # Résumé général avec désglose IVA intégré
            story.extend(self.create_facturacion_resumen_con_iva(informe_data))

            # Top produits
            story.extend(self.create_top_productos(informe_data))

            # Générer le PDF
            doc.build(story)

            self.logger.info(f"PDF de informe de facturación generado: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error generando PDF de informe de facturación: {e}")
            raise e

    def generate_stock_pdf(self, informe_data, output_path):
        """Génère un PDF de rapport de stock"""
        try:
            self.logger.info(f"Generando PDF de informe de stock: {output_path}")

            # Créer le document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=self.margin,
                leftMargin=self.margin,
                topMargin=self.margin,
                bottomMargin=self.margin
            )

            # Construire le contenu
            story = []

            # Titre
            title = f"Informe de Stock<br/>{datetime.now().strftime('%d/%m/%Y %H:%M')}"
            story.append(Paragraph(title, self.styles['TitleStyle']))
            story.append(Spacer(1, 20))

            # Résumé
            story.extend(self.create_stock_resumen(informe_data))

            # Décomposition par catégorie
            story.extend(self.create_stock_por_categoria(informe_data))

            # Liste des produits
            story.extend(self.create_productos_table(informe_data))

            # Générer le PDF
            doc.build(story)

            self.logger.info(f"PDF de informe de stock generado: {output_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error generando PDF de informe de stock: {e}")
            raise e
    def create_lista_clientes(self, informe_data):
        """Crée la liste des clients séparés par virgule"""
        elements = []

        lista_clientes = informe_data.get('lista_clientes', [])

        if not lista_clientes:
            return elements

        # Titre de section
        elements.append(Paragraph("Lista de Clientes", self.styles['SubtitleStyle']))

        # Liste des clients séparés par virgule
        nombres_clientes = [cliente.get('nombre', 'N/A') for cliente in lista_clientes]
        clientes_text = ', '.join(nombres_clientes)

        elements.append(Paragraph(clientes_text, self.styles['Normal']))
        elements.append(Spacer(1, 20))

        return elements

    def create_facturacion_resumen_con_iva(self, informe_data):
        """Crée le résumé général avec désglose IVA intégré dans une seule table"""
        elements = []

        resumen = informe_data.get('resumen', {})
        desglose_iva = informe_data.get('desglose_iva', [])

        # Titre de section (sans PageBreak pour layout continu)
        elements.append(Paragraph("Resumen General", self.styles['SubtitleStyle']))

        # Table unique avec résumé général et désglose IVA intégré
        data = [
            ['Concepto', 'Valor'],
            ['Número de Facturas', str(resumen.get('num_facturas', 0))],
            ['', ''],  # Ligne vide pour séparation
        ]

        # Ajouter le désglose IVA
        if desglose_iva:
            data.append(['Desglose por IVA', ''])
            for item in desglose_iva:
                tasa = f"  IVA {item.get('iva_aplicado', 0):.0f}%"
                base = item.get('base_imponible', 0)
                iva = item.get('total_iva', 0)
                data.append([tasa, f"Base: {base:.2f} € + IVA: {iva:.2f} €"])

            data.append(['', ''])  # Ligne vide pour séparation

        # Ajouter les totaux
        data.append(['Total sin IVA', f"{resumen.get('subtotal', 0):.2f} €"])
        data.append(['Total IVA', f"{resumen.get('total_iva', 0):.2f} €"])
        data.append(['TOTAL CON IVA', f"{resumen.get('total', 0):.2f} €"])

        table = Table(data, colWidths=[10*cm, 6*cm])
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            # Corps
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            # Ligne TOTAL CON IVA en gras et rouge
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 13),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        return elements

    def create_facturacion_resumen(self, informe_data):
        """Crée la section résumé du rapport de facturation"""
        elements = []

        resumen = informe_data.get('resumen', {})

        # Titre de section
        elements.append(Paragraph("Resumen General", self.styles['SubtitleStyle']))

        # Table de résumé
        data = [
            ['Concepto', 'Valor'],
            ['Número de Facturas', str(resumen.get('num_facturas', 0))],
            ['Subtotal', f"{resumen.get('subtotal', 0):.2f} €"],
            ['Total IVA', f"{resumen.get('total_iva', 0):.2f} €"],
            ['Total', f"{resumen.get('total', 0):.2f} €"],
            ['Promedio por Factura', f"{resumen.get('promedio_factura', 0):.2f} €"]
        ]

        table = Table(data, colWidths=[10*cm, 6*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        return elements

    def create_desglose_iva(self, informe_data):
        """Crée la section décomposition IVA"""
        elements = []

        desglose = informe_data.get('desglose_iva', [])

        if not desglose:
            return elements

        # Titre de section
        elements.append(Paragraph("Desglose por IVA", self.styles['SubtitleStyle']))

        # Table de décomposition
        data = [['Tasa IVA', 'Base Imponible', 'IVA', 'Total']]

        for item in desglose:
            data.append([
                f"{item.get('iva_aplicado', 0):.0f}%",
                f"{item.get('base_imponible', 0):.2f} €",
                f"{item.get('total_iva', 0):.2f} €",
                f"{item.get('total', 0):.2f} €"
            ])

        table = Table(data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        return elements

    def create_top_productos(self, informe_data):
        """Crée la section top produits"""
        elements = []

        top_productos = informe_data.get('productos_mas_vendidos', [])

        if not top_productos:
            return elements

        # Titre de section
        elements.append(Paragraph("Top 10 Productos Más Vendidos", self.styles['SubtitleStyle']))

        # Table des produits
        data = [['Producto', 'Cantidad', 'Total Vendido']]

        for producto in top_productos[:10]:
            data.append([
                producto.get('nombre', 'N/A'),
                str(producto.get('cantidad', 0)),
                f"{producto.get('importe', 0):.2f} €"
            ])

        table = Table(data, colWidths=[10*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        return elements

    def create_facturas_detalladas_table(self, informe_data):
        """Crée la table des factures avec désglose IVA par facture"""
        elements = []

        facturas = informe_data.get('facturas', [])

        if not facturas:
            return elements

        # Titre de section (sans PageBreak pour layout continu)
        elements.append(Paragraph("Detalle de Facturas", self.styles['SubtitleStyle']))

        for factura in facturas:
            # Informations de base de la facture
            factura_info = f"<b>Factura {factura.get('numero', 'N/A')}</b> - {factura.get('fecha', 'N/A')} - {factura.get('cliente', 'N/A')} - Estado: {factura.get('estado', 'N/A')}"
            elements.append(Paragraph(factura_info, self.styles['Normal']))
            elements.append(Spacer(1, 5))

            # Désglose IVA de cette facture
            desglose_iva = factura.get('desglose_iva', [])

            if desglose_iva:
                # Table du désglose IVA
                data = [['Tasa IVA', 'Base Imponible', 'IVA', 'Total']]

                for item in desglose_iva:
                    base = item.get('base_imponible', 0)
                    iva = item.get('total_iva', 0)
                    total = base + iva
                    data.append([
                        f"{item.get('iva_aplicado', 0):.0f}%",
                        f"{base:.2f} €",
                        f"{iva:.2f} €",
                        f"{total:.2f} €"
                    ])

                # Ligne de total
                total_base = sum(item.get('base_imponible', 0) for item in desglose_iva)
                total_iva = sum(item.get('total_iva', 0) for item in desglose_iva)
                total_factura = total_base + total_iva

                data.append([
                    'TOTAL',
                    f"{total_base:.2f} €",
                    f"{total_iva:.2f} €",
                    f"{total_factura:.2f} €"
                ])

                table = Table(data, colWidths=[3*cm, 4*cm, 3.5*cm, 3.5*cm])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e74c3c')),
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
                ]))

                elements.append(table)
            else:
                # Si pas de désglose, afficher juste le total
                total_text = f"Total: {factura.get('total', 0):.2f} €"
                elements.append(Paragraph(total_text, self.styles['Normal']))

            elements.append(Spacer(1, 15))

        return elements

    def create_facturas_table(self, informe_data):
        """Crée la table des factures (ancienne version, conservée pour compatibilité)"""
        elements = []

        facturas = informe_data.get('facturas', [])

        if not facturas:
            return elements

        # Titre de section
        elements.append(PageBreak())
        elements.append(Paragraph("Detalle de Facturas", self.styles['SubtitleStyle']))

        # Table des factures
        data = [['Número', 'Fecha', 'Cliente', 'Subtotal', 'IVA', 'Total']]

        for factura in facturas:
            data.append([
                factura.get('numero', 'N/A'),
                factura.get('fecha', 'N/A'),
                factura.get('cliente', 'N/A')[:30],  # Limiter la longueur
                f"{factura.get('subtotal', 0):.2f} €",
                f"{factura.get('iva', 0):.2f} €",
                f"{factura.get('total', 0):.2f} €"
            ])

        table = Table(data, colWidths=[2.5*cm, 2.5*cm, 5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))

        elements.append(table)

        return elements

    def create_stock_resumen(self, informe_data):
        """Crée la section résumé du rapport de stock"""
        elements = []

        resumen = informe_data.get('resumen', {})

        # Titre de section
        elements.append(Paragraph("Resumen General", self.styles['SubtitleStyle']))

        # Table de résumé
        data = [
            ['Concepto', 'Valor'],
            ['Total Productos', str(resumen.get('total_productos', 0))],
            ['Productos Sin Stock', str(resumen.get('productos_sin_stock', 0))],
            ['Valor Total Stock', f"{resumen.get('valor_total_stock', 0):.2f} €"]
        ]

        table = Table(data, colWidths=[10*cm, 6*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        return elements

    def create_stock_por_categoria(self, informe_data):
        """Crée la section décomposition par catégorie"""
        elements = []

        por_categoria = informe_data.get('por_categoria', [])

        if not por_categoria:
            return elements

        # Titre de section
        elements.append(Paragraph("Desglose por Categoría", self.styles['SubtitleStyle']))

        # Table de décomposition
        data = [['Categoría', 'Productos', 'Stock Total', 'Valor Total']]

        for cat in por_categoria:
            data.append([
                cat.get('categoria', 'Sin categoría'),
                str(cat.get('num_productos', 0)),
                str(cat.get('stock_total', 0)),
                f"{cat.get('valor_total', 0):.2f} €"
            ])

        table = Table(data, colWidths=[6*cm, 3*cm, 3*cm, 4*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        return elements

    def create_productos_table(self, informe_data):
        """Crée la table des produits"""
        elements = []

        productos = informe_data.get('productos', [])

        if not productos:
            return elements

        # Titre de section
        elements.append(PageBreak())
        elements.append(Paragraph("Detalle de Productos", self.styles['SubtitleStyle']))

        # Table des produits
        data = [['Producto', 'Categoría', 'Stock Actual', 'Stock Mínimo', 'Precio', 'Valor Total']]

        for producto in productos:
            stock_actual = producto.get('stock_actual', 0)
            stock_minimo = producto.get('stock_minimo', 0)
            precio = producto.get('precio', 0)
            valor_total = stock_actual * precio

            data.append([
                producto.get('nombre', 'N/A')[:30],
                producto.get('categoria', 'N/A')[:15],
                str(stock_actual),
                str(stock_minimo),
                f"{precio:.2f} €",
                f"{valor_total:.2f} €"
            ])

        table = Table(data, colWidths=[6*cm, 2.5*cm, 2*cm, 2*cm, 2*cm, 2*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))

        elements.append(table)

        return elements


# Instance globale du générateur
informe_pdf_generator = InformePDFGenerator()

