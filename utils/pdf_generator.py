# -*- coding: utf-8 -*-
"""
Générateur de PDF professionnel pour les factures
"""

import os
import platform
import subprocess
import tempfile
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfgen import canvas
from utils.logger import get_logger

class FacturaPDFGenerator:
    """Générateur de PDF professionnel pour les factures"""
    
    def __init__(self):
        self.logger = get_logger("pdf_generator")
        self.page_width, self.page_height = A4
        self.margin = 2 * cm
        self.config_file = "config/config.json"

        # Styles
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configure les styles personnalisés - fonts plus petites pour style épuré"""
        # Style pour le titre principal - réduit
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=14,  # Réduit de 24 à 14
            textColor=colors.black,
            alignment=TA_CENTER,
            spaceAfter=12
        ))

        # Style pour les en-têtes de section - simplifié
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=9,  # Réduit de 14 à 9
            textColor=colors.black,
            # backgroundColor supprimé pour style épuré
            borderPadding=4,
            spaceAfter=6
        ))

        # Style pour les informations importantes - réduit
        self.styles.add(ParagraphStyle(
            name='ImportantInfo',
            parent=self.styles['Normal'],
            fontSize=8,  # Réduit de 12 à 8
            textColor=colors.black,
            fontName='Helvetica-Bold'
        ))

        # Style pour le total - réduit
        self.styles.add(ParagraphStyle(
            name='TotalStyle',
            parent=self.styles['Normal'],
            fontSize=10,  # Réduit de 16 à 10
            textColor=colors.black,
            fontName='Helvetica-Bold',
            alignment=TA_RIGHT
        ))
    
    def generate_invoice_pdf(self, invoice_data, output_path):
        """Génère un PDF de facture professionnel"""
        try:
            self.logger.info(f"Generando PDF de factura: {invoice_data.get('numero', 'N/A')}")
            
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
            
            # En-tête avec logo et informations entreprise
            story.extend(self.create_header(invoice_data))
            
            # Informations de la facture
            story.extend(self.create_invoice_info(invoice_data))
            
            # Informations client
            story.extend(self.create_client_info(invoice_data))
            
            # Table des lignes de facture
            story.extend(self.create_invoice_lines_table(invoice_data))
            
            # Totaux
            story.extend(self.create_totals_section(invoice_data))
            
            # Pied de page avec conditions
            story.extend(self.create_footer(invoice_data))
            
            # Générer le PDF
            doc.build(story)
            
            self.logger.info(f"PDF generado exitosamente: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generando PDF: {e}")
            raise e
    
    def create_header(self, invoice_data):
        """Crée l'en-tête de la facture"""
        elements = []

        # Table pour l'en-tête (logo + info entreprise | titre facture)
        header_data = []

        # Chercher un logo
        logo_path = self.find_company_logo()
        logo_cell = None

        if logo_path:
            try:
                # Logo avec redimensionnement proportionnel
                logo_cell = self.create_logo_image(logo_path, max_width=3*cm, max_height=3*cm)
                if logo_cell:
                    self.logger.info(f"Logo chargé avec succès: {logo_path}")
                else:
                    self.logger.warning(f"Logo non chargé: {logo_path}")
            except Exception as e:
                self.logger.error(f"Erreur lors du chargement du logo {logo_path}: {e}")
                logo_cell = None

        # Récupérer les informations de l'organisation configurée
        company_info = self.get_company_info()

        # Titre FACTURA Nº aligné à droite sur une ligne, en gras
        invoice_title = f"""
        <b style="font-size:14pt; color:#000000;">FACTURA Nº {invoice_data.get('numero', 'N/A')}</b>
        """

        # Si on a un logo, créer une disposition avec logo + info entreprise à gauche
        if logo_cell:
            # Sous-table pour logo + info entreprise
            left_section = Table(
                [[logo_cell, Paragraph(company_info, self.styles['Normal'])]],
                colWidths=[3.5*cm, 7*cm]
            )
            left_section.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, 0), 10),
            ]))

            # Table principale avec section gauche et titre à droite
            header_data.append([
                left_section,
                Paragraph(invoice_title, self.styles['Normal'])
            ])

            header_table = Table(header_data, colWidths=[10.5*cm, 7*cm])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ]))
        else:
            # Sans logo, juste info entreprise à gauche et titre à droite
            header_data.append([
                Paragraph(company_info, self.styles['Normal']),
                Paragraph(invoice_title, self.styles['Normal'])
            ])

            header_table = Table(header_data, colWidths=[10.5*cm, 7*cm])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ]))

        elements.append(header_table)
        elements.append(Spacer(1, 20))

        return elements

    def create_invoice_info(self, invoice_data):
        """Crée la section d'informations de la facture et client - date à gauche, client à droite"""
        elements = []

        # Style avec font plus petite, aligné à gauche
        small_style_left = ParagraphStyle(
            name='SmallInfoLeft',
            parent=self.styles['Normal'],
            fontSize=8,
            leading=12,
            alignment=TA_LEFT
        )

        # Style avec font plus petite, aligné à droite
        small_style_right = ParagraphStyle(
            name='SmallInfoRight',
            parent=self.styles['Normal'],
            fontSize=8,
            leading=12,
            alignment=TA_RIGHT
        )

        # Date à gauche
        fecha = invoice_data.get('fecha', 'N/A')
        fecha_text = f"<b>FECHA</b> {fecha}"
        fecha_para = Paragraph(fecha_text, small_style_left)

        # Informations client à droite - format texte simple
        client = invoice_data.get('cliente', {})

        client_lines = []
        client_lines.append(f"<b>Cliente:</b> {client.get('nombre', 'N/A')}")

        if client.get('telefono'):
            client_lines.append(f"<b>Teléfono:</b> {client.get('telefono')}")

        if client.get('direccion'):
            # Séparer adresse et code postal
            direccion_completa = client.get('direccion', '')
            # Chercher le code postal (5 chiffres) et la ville
            import re
            match = re.search(r'(\d{5})\s+(.+)$', direccion_completa, re.MULTILINE)
            if match:
                # Adresse sans le code postal et la ville
                direccion_sin_cp = direccion_completa[:direccion_completa.find(match.group(0))].strip()
                codigo_postal_ciudad = f"{match.group(1)} {match.group(2)}"

                if direccion_sin_cp:
                    client_lines.append(f"<b>Dirección:</b> {direccion_sin_cp.replace(chr(10), ', ')}")
                client_lines.append(codigo_postal_ciudad)
            else:
                # Si pas de code postal trouvé, afficher l'adresse telle quelle
                client_lines.append(f"<b>Dirección:</b> {direccion_completa.replace(chr(10), ', ')}")

        client_text = "<br/>".join(client_lines)
        client_para = Paragraph(client_text, small_style_right)

        # Table principale : fecha à gauche, client à droite
        # MÊME LARGEUR que le tableau produits = 7cm + 1.8cm + 2cm + 1.5cm + 1.5cm + 2.5cm = 16.3cm
        # Cette table définit le cadre de toute la mise en page
        product_table_width = 16.3*cm

        # Répartition : fecha prend ~40%, client prend ~60%
        fecha_col_width = 6.5*cm
        client_col_width = 9.8*cm

        main_table = Table([[fecha_para, client_para]], colWidths=[fecha_col_width, client_col_width])
        main_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # FECHA à gauche
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Client à droite
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        elements.append(main_table)
        elements.append(Spacer(1, 15))

        return elements

    def create_client_info(self, invoice_data):
        """Crée la section d'informations client - DEPRECATED, fusionné avec create_invoice_info"""
        # Cette fonction n'est plus utilisée, les infos client sont dans create_invoice_info
        return []

    def create_invoice_lines_table(self, invoice_data):
        """Crée la table des lignes de facture - style épuré sans bordures"""
        elements = []

        # Espace avant le tableau
        elements.append(Spacer(1, 10))

        # En-têtes de la table - avec toutes les colonnes incluant Desc% et IVA%
        headers = ['', 'Unidades', 'Precio', 'Desc.%', 'IVA%', 'Total']

        # Données des lignes
        table_data = [headers]

        lineas = invoice_data.get('lineas', [])
        for linea in lineas:
            # Nom du produit seulement (pas de référence séparée)
            producto_nombre = linea.get('producto_nombre', linea.get('descripcion', 'Producto'))

            row = [
                producto_nombre,
                str(linea.get('cantidad', 0)),
                f"{linea.get('precio_unitario', 0):.2f}",
                f"{linea.get('descuento', 0):.1f}%",
                f"{linea.get('iva_aplicado', 0):.1f}%",
                f"{linea.get('total', 0):.2f}"
            ]
            table_data.append(row)

        # Créer la table avec toutes les colonnes
        lines_table = Table(table_data, colWidths=[7*cm, 1.8*cm, 2*cm, 1.5*cm, 1.5*cm, 2.5*cm])

        # Style épuré avec en-tête fond vert, en gras, sans bordures
        lines_table.setStyle(TableStyle([
            # En-tête - fond vert, en gras, sans bordures
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#90EE90')),  # Vert clair
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),      # Nom produit à gauche
            ('ALIGN', (1, 0), (-1, 0), 'RIGHT'),    # Unidades, Precio, Desc, IVA, Total à droite

            # Corps de la table - fonts plus petites
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),     # Nom produit à gauche
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),   # Chiffres à droite
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # PAS de bordures - style épuré
            # ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),  # RETIRÉ

            # PAS d'alternance de couleurs - fond blanc partout
            # ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),  # RETIRÉ

            # Padding minimal
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))

        elements.append(lines_table)
        elements.append(Spacer(1, 20))

        return elements

    def create_totals_section(self, invoice_data):
        """Crée la section des totaux - style épuré sans bordures"""
        elements = []

        # Table des totaux (alignée à droite) - style simplifié
        totals_data = [
            ['Base Imponible', f"{invoice_data.get('subtotal', 0):.2f}"],
            ['IVA    21%', f"{invoice_data.get('iva_total', 0):.2f}"],
            ['', ''],  # Ligne vide
            ['Total', f"{invoice_data.get('total', 0):.2f}"]
        ]

        totals_table = Table(totals_data, colWidths=[4*cm, 3*cm])
        totals_table.setStyle(TableStyle([
            # Alignement
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Styles des labels - fonts plus petites
            ('FONTNAME', (0, 0), (0, -2), 'Helvetica'),
            ('FONTSIZE', (0, 0), (0, -2), 8),  # Réduit de 11 à 8
            ('TEXTCOLOR', (0, 0), (0, -2), colors.black),

            # Style du total final - fond vert, en gras
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#90EE90')),  # Fond vert
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),  # Réduit de 14 à 10
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),

            # PAS de bordures
            # ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#e74c3c')),  # RETIRÉ
            # ('LINEBELOW', (0, -1), (-1, -1), 2, colors.HexColor('#e74c3c')),  # RETIRÉ

            # Padding minimal
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))

        # Centrer la table des totaux à droite
        totals_wrapper = Table([[totals_table]], colWidths=[self.page_width - 2*self.margin])
        totals_wrapper.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))

        elements.append(totals_wrapper)
        elements.append(Spacer(1, 20))

        return elements

    def get_default_config(self):
        """Obtenir la configuration par défaut"""
        return {
            'condiciones_pago': '• El pago de esta factura deberá realizarse antes de la fecha de vencimiento.\n• Pasados 30 días de la fecha de vencimiento, se aplicarán intereses de demora.\n• Para cualquier consulta, contacte con nosotros.',
            'informacion_legal': '• Esta factura se emite de acuerdo con la normativa fiscal vigente.\n• Conserve este documento para sus registros contables.',
            'condiciones_pago_visible': 1,
            'informacion_legal_visible': 1
        }

    def load_config_data(self):
        """Charger les données depuis config.json avec fusion intelligente des défauts"""
        try:
            # Obtenir les valeurs par défaut
            defaults = self.get_default_config()

            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    org_defaults = config.get('organizacion_defaults', {})

                    # Commencer avec toutes les valeurs existantes
                    merged = org_defaults.copy()

                    # Ajouter les valeurs par défaut pour les clés manquantes
                    missing_keys = set(defaults.keys()) - set(org_defaults.keys())
                    if missing_keys:
                        self.logger.info(f"Ajout des valeurs par défaut manquantes dans config.json: {missing_keys}")
                        # Mettre à jour seulement les clés manquantes
                        for key in missing_keys:
                            merged[key] = defaults[key]
                            org_defaults[key] = defaults[key]

                        # Sauvegarder la version fusionnée
                        config['organizacion_defaults'] = org_defaults
                        with open(self.config_file, 'w', encoding='utf-8') as f_write:
                            json.dump(config, f_write, indent=2, ensure_ascii=False)

                    return merged
            else:
                # Si le fichier n'existe pas, retourner les défauts
                # (le fichier sera créé par organizacion_pyqt5.py)
                self.logger.warning("config.json n'existe pas, utilisation des valeurs par défaut")
                return defaults

        except Exception as e:
            self.logger.error(f"Erreur chargement config.json: {e}")
            return self.get_default_config()

    def create_footer(self, invoice_data):
        """Crée le pied de page avec conditions"""
        elements = []

        # Charger les condiciones_pago et informacion_legal depuis config.json
        config_data = self.load_config_data()

        # Récupérer les flags de visibilité (par défaut à 1 = visible)
        condiciones_pago_visible = config_data.get('condiciones_pago_visible', 1)
        informacion_legal_visible = config_data.get('informacion_legal_visible', 1)

        # Construire les sections du footer selon la visibilité
        footer_parts = []

        # Ajouter les conditions de paiement si visibles
        if condiciones_pago_visible:
            condiciones_pago = config_data.get('condiciones_pago',
                '• El pago de esta factura deberá realizarse antes de la fecha de vencimiento.\n'
                '• Pasados 30 días de la fecha de vencimiento, se aplicarán intereses de demora.\n'
                '• Para cualquier consulta, contacte con nosotros.')

            if condiciones_pago.strip():  # Seulement si non vide
                condiciones_pago_html = condiciones_pago.replace('\n', '<br/>')
                footer_parts.append(f"<b>CONDICIONES DE PAGO:</b><br/>{condiciones_pago_html}")

        # Ajouter les informations légales si visibles
        if informacion_legal_visible:
            informacion_legal = config_data.get('informacion_legal',
                '• Esta factura se emite de acuerdo con la normativa fiscal vigente.\n'
                '• Conserve este documento para sus registros contables.')

            if informacion_legal.strip():  # Seulement si non vide
                informacion_legal_html = informacion_legal.replace('\n', '<br/>')
                footer_parts.append(f"<b>INFORMACIÓN LEGAL:</b><br/>{informacion_legal_html}")

        # PAS de signature de génération automatique - retiré pour style épuré
        # footer_parts.append(f"<i>Factura generada automáticamente por Facturación Fácil - {datetime.now().strftime('%d/%m/%Y %H:%M')}</i>")

        # Construire le footer final en joignant les parties avec double saut de ligne
        footer_text = "<br/><br/>".join(footer_parts)

        footer_style = ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_LEFT,
            leftIndent=0,
            rightIndent=0
        )

        elements.append(Paragraph(footer_text, footer_style))

        return elements

    def find_company_logo(self):
        """Cherche le logo de l'entreprise en priorité dans la configuration d'organisation"""
        try:
            # Importer ici pour éviter les imports circulaires
            from database.models import Organizacion

            # 1. PRIORITÉ : Logo configuré dans l'organisation
            organizacion = Organizacion.get()
            if organizacion and organizacion.logo_path:
                logo_path = organizacion.logo_path.strip()
                if logo_path and os.path.exists(logo_path):
                    self.logger.info(f"Logo configuré trouvé: {logo_path}")
                    return logo_path
                else:
                    self.logger.warning(f"Logo configuré n'existe pas: {logo_path}")

        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération du logo configuré: {e}")

        # 2. FALLBACK : Chercher dans les chemins par défaut
        self.logger.info("Recherche du logo dans les chemins par défaut...")
        possible_paths = [
            "data/logos/logo.png",
            "data/logos/logo.jpg",
            "assets/logo.png",
            "assets/icon.png",
            "logo/logo.png",
            "logo/logo.jpg",
            "logo.png",
            "logo.jpg"
        ]

        # Chercher d'abord dans les chemins spécifiques
        for path in possible_paths:
            if os.path.exists(path):
                self.logger.info(f"Logo par défaut trouvé: {path}")
                return path

        # Chercher dans le dossier data/logos/ pour n'importe quel fichier image
        logos_dir = "data/logos"
        if os.path.exists(logos_dir):
            for filename in os.listdir(logos_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    logo_path = os.path.join(logos_dir, filename)
                    self.logger.info(f"Logo trouvé dans data/logos/: {logo_path}")
                    return logo_path

        # Chercher dans le dossier logo/
        logo_dir = "logo"
        if os.path.exists(logo_dir):
            for filename in os.listdir(logo_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    logo_path = os.path.join(logo_dir, filename)
                    self.logger.info(f"Logo trouvé dans logo/: {logo_path}")
                    return logo_path

        self.logger.warning("Aucun logo trouvé")
        return None

    def get_company_info(self):
        """Récupère les informations de l'entreprise depuis la configuration d'organisation"""
        try:
            # Importer ici pour éviter les imports circulaires
            from database.models import Organizacion

            # Récupérer les données de l'organisation
            organizacion = Organizacion.get()
            if organizacion:
                # Construire les informations de l'entreprise avec les données configurées
                company_name = organizacion.nombre or "FACTURACIÓN FÁCIL"
                company_cif = f"CIF: {organizacion.cif}" if organizacion.cif else ""
                company_address = organizacion.direccion or "Dirección no configurada"
                company_phone = f"Tel: {organizacion.telefono}" if organizacion.telefono else ""
                company_email = f"Email: {organizacion.email}" if organizacion.email else ""

                # Construire le HTML avec les données réelles
                info_parts = [f"<b>{company_name}</b>"]

                if company_cif:
                    info_parts.append(company_cif)

                if company_address:
                    # Remplacer les retours à la ligne par <br/>
                    address_formatted = company_address.replace('\n', '<br/>')
                    info_parts.append(address_formatted)

                if company_phone:
                    info_parts.append(company_phone)

                if company_email:
                    info_parts.append(company_email)

                company_info = "<br/>".join(info_parts)
                self.logger.info("Informations d'entreprise récupérées depuis la configuration")
                return company_info

        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des informations d'entreprise: {e}")

        # Fallback : informations par défaut
        self.logger.warning("Utilisation des informations d'entreprise par défaut")
        return """
        <b>FACTURACIÓN FÁCIL</b><br/>
        Calle Ejemplo, 123<br/>
        28001 Madrid, España<br/>
        Tel: +34 91 123 45 67<br/>
        Email: info@facturacionfacil.com
        """

    def generar_factura_pdf(self, factura, output_path=None, auto_open=True):
        """Méthode de compatibilité pour générer un PDF de facture"""
        try:
            # Si pas de chemin spécifié, créer un fichier temporaire
            if output_path is None:
                temp_dir = tempfile.gettempdir()
                numero_safe = getattr(factura, 'numero_factura', 'SIN_NUMERO').replace('/', '_')
                output_path = os.path.join(temp_dir, f"factura_{numero_safe}.pdf")

            # Préparer les données de la facture
            invoice_data = {
                'numero': getattr(factura, 'numero_factura', 'SIN_NUMERO'),
                'fecha': getattr(factura, 'fecha_factura', 'N/A'),
                'vencimiento': getattr(factura, 'fecha_factura', 'N/A'),  # Usar misma fecha si no hay vencimiento
                'estado': 'Pendiente',
                'cliente': {
                    'nombre': getattr(factura, 'nombre_cliente', 'Cliente'),
                    'nif': getattr(factura, 'dni_nie_cliente', ''),
                    'direccion': getattr(factura, 'direccion_cliente', ''),
                    'email': getattr(factura, 'email_cliente', ''),
                    'telefono': getattr(factura, 'telefono_cliente', '')
                },
                'lineas': [],
                'subtotal': getattr(factura, 'subtotal', 0),
                'iva_total': getattr(factura, 'total_iva', 0),
                'total': getattr(factura, 'total_factura', 0)
            }

            # Ajouter les lignes de facture si disponibles
            if hasattr(factura, 'items') and factura.items:
                for item in factura.items:
                    # Obtenir le produit pour la référence et description
                    producto = None
                    if hasattr(item, 'get_producto'):
                        producto = item.get_producto()

                    invoice_data['lineas'].append({
                        'producto_referencia': getattr(producto, 'referencia', '') if producto else f"PROD_{getattr(item, 'producto_id', '')}",
                        'producto_nombre': getattr(producto, 'nombre', '') if producto else 'Producto',
                        'cantidad': getattr(item, 'cantidad', 0),
                        'precio_unitario': getattr(item, 'precio_unitario', 0),
                        'descuento': getattr(item, 'descuento', 0),
                        'iva_aplicado': getattr(item, 'iva_aplicado', 0),
                        'total': getattr(item, 'total', 0)
                    })

            # Générer le PDF
            success = self.generate_invoice_pdf(invoice_data, output_path)

            if success and auto_open:
                # Vérifier les variables d'environnement pour désactiver l'ouverture
                should_disable = (
                    os.getenv('DISABLE_PDF_OPEN') == '1' or
                    os.getenv('PYTEST_CURRENT_TEST') is not None or
                    os.getenv('TESTING') == '1'
                )
                if not should_disable:
                    self.open_pdf_file(output_path)
                else:
                    self.logger.info("PDF no abierto - Modo test detectado o DISABLE_PDF_OPEN activado")

            return output_path if success else None

        except Exception as e:
            self.logger.error(f"Error en generar_factura_pdf: {e}")
            raise e

    def create_logo_image(self, logo_path, max_width=3*cm, max_height=3*cm):
        """Crée une image du logo avec redimensionnement proportionnel"""
        try:
            if not logo_path or not os.path.exists(logo_path):
                return None

            # Créer l'objet Image de ReportLab
            logo_img = Image(logo_path)

            # Obtenir les dimensions originales
            original_width = logo_img.drawWidth
            original_height = logo_img.drawHeight

            # Calculer le ratio de redimensionnement
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            ratio = min(width_ratio, height_ratio)

            # Appliquer le redimensionnement
            logo_img.drawWidth = original_width * ratio
            logo_img.drawHeight = original_height * ratio

            return logo_img

        except Exception as e:
            self.logger.error(f"Error creando imagen de logo: {e}")
            return None

    def open_pdf_file(self, pdf_path):
        """Ouvre le fichier PDF avec l'application par défaut"""
        try:
            # Vérifier les variables d'environnement pour désactiver l'ouverture
            should_disable = (
                os.getenv('DISABLE_PDF_OPEN') == '1' or
                os.getenv('PYTEST_CURRENT_TEST') is not None or
                os.getenv('TESTING') == '1'
            )

            if should_disable:
                self.logger.info("PDF no abierto - Modo test detectado o DISABLE_PDF_OPEN activado")
                return True  # Retourner True car c'est le comportement attendu

            if not os.path.exists(pdf_path):
                self.logger.error(f"Archivo PDF no existe: {pdf_path}")
                return False

            system = platform.system()

            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", pdf_path], check=True)
            else:  # Linux y otros
                subprocess.run(["xdg-open", pdf_path], check=True)

            self.logger.info(f"PDF abierto exitosamente: {pdf_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error abriendo PDF: {e}")
            return False

# Instance globale du générateur
pdf_generator = FacturaPDFGenerator()

# Alias pour compatibilité avec les tests existants
PDFGenerator = FacturaPDFGenerator
