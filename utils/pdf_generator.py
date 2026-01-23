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
        """Configure les styles personnalisés"""
        # Style pour le titre principal
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Style pour les en-têtes de section
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            backgroundColor=colors.HexColor('#ecf0f1'),
            borderPadding=8,
            spaceAfter=10
        ))
        
        # Style pour les informations importantes
        self.styles.add(ParagraphStyle(
            name='ImportantInfo',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            fontName='Helvetica-Bold'
        ))
        
        # Style pour le total
        self.styles.add(ParagraphStyle(
            name='TotalStyle',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#e74c3c'),
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
        
        # Table pour l'en-tête (logo + info entreprise + titre facture)
        header_data = []
        
        # Ligne 1: Logo, Info entreprise, Titre facture
        logo_cell = "LOGO"
        
        # Chercher un logo
        logo_path = self.find_company_logo()
        if logo_path:
            try:
                logo_cell = Image(logo_path, width=60, height=40)
                self.logger.info(f"Logo chargé avec succès: {logo_path}")
            except Exception as e:
                self.logger.error(f"Erreur lors du chargement du logo {logo_path}: {e}")
                logo_cell = "LOGO"
        else:
            self.logger.warning("Aucun logo disponible, utilisation du texte 'LOGO'")
        
        # Récupérer les informations de l'organisation configurée
        company_info = self.get_company_info()
        
        invoice_title = f"""
        <b style="font-size:18pt; color:#e74c3c;">FACTURA</b><br/>
        <b style="font-size:14pt;">{invoice_data.get('numero', 'N/A')}</b>
        """
        
        header_data.append([
            logo_cell,
            Paragraph(company_info, self.styles['Normal']),
            Paragraph(invoice_title, self.styles['Normal'])
        ])
        
        header_table = Table(header_data, colWidths=[4*cm, 8*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        elements.append(header_table)
        elements.append(Spacer(1, 20))
        
        return elements

    def create_invoice_info(self, invoice_data):
        """Crée la section d'informations de la facture"""
        elements = []

        # Table des informations de facture
        info_data = [
            ['Fecha:', invoice_data.get('fecha', 'N/A')],
            ['Vencimiento:', invoice_data.get('vencimiento', 'N/A')],
            ['Estado:', invoice_data.get('estado', 'Pendiente')]
        ]

        info_table = Table(info_data, colWidths=[4*cm, 6*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements.append(info_table)
        elements.append(Spacer(1, 20))

        return elements

    def create_client_info(self, invoice_data):
        """Crée la section d'informations client"""
        elements = []

        # Titre de section
        elements.append(Paragraph("DATOS DEL CLIENTE", self.styles['SectionHeader']))

        client = invoice_data.get('cliente', {})

        # Construire les informations client avec tous les champs
        client_info_parts = [f"<b>{client.get('nombre', 'N/A')}</b>"]

        if client.get('nif'):
            client_info_parts.append(f"NIF/CIF: {client.get('nif')}")

        if client.get('direccion'):
            client_info_parts.append(client.get('direccion').replace('\n', '<br/>'))

        if client.get('email'):
            client_info_parts.append(f"Email: {client.get('email')}")

        if client.get('telefono'):
            client_info_parts.append(f"Tel: {client.get('telefono')}")

        client_info = "<br/>".join(client_info_parts)

        elements.append(Paragraph(client_info, self.styles['Normal']))
        elements.append(Spacer(1, 20))

        return elements

    def create_invoice_lines_table(self, invoice_data):
        """Crée la table des lignes de facture"""
        elements = []

        # Titre de section
        elements.append(Paragraph("DETALLE DE LA FACTURA", self.styles['SectionHeader']))

        # En-têtes de la table
        headers = ['Producto', 'Descripción', 'Cant.', 'Precio Unit.', 'Desc.%', 'IVA%', 'Total']

        # Données des lignes
        table_data = [headers]

        lineas = invoice_data.get('lineas', [])
        for linea in lineas:
            # Utiliser les bonnes clés pour les données du produit
            producto_ref = linea.get('producto_referencia', 'N/A')
            producto_nombre = linea.get('producto_nombre', linea.get('descripcion', 'Producto'))

            # Utiliser Paragraph pour permettre le retour à la ligne automatique
            producto_ref_para = Paragraph(str(producto_ref), self.styles['Normal'])
            producto_nombre_para = Paragraph(str(producto_nombre), self.styles['Normal'])

            row = [
                producto_ref_para,
                producto_nombre_para,
                str(linea.get('cantidad', 0)),
                f"{linea.get('precio_unitario', 0):.2f} €",
                f"{linea.get('descuento', 0):.1f}%",  # Utiliser 'descuento' au lieu de 'descuento_pct'
                f"{linea.get('iva_aplicado', 0):.1f}%",  # Utiliser 'iva_aplicado' au lieu de 'iva_pct'
                f"{linea.get('total', 0):.2f} €"
            ]
            table_data.append(row)

        # Créer la table
        lines_table = Table(table_data, colWidths=[3*cm, 5*cm, 1.5*cm, 2.5*cm, 1.5*cm, 1.5*cm, 2.5*cm])

        # Style de la table
        lines_table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

            # Corps de la table
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (2, 1), (-1, -1), 'CENTER'),  # Quantité, prix, etc. centrés
            ('ALIGN', (0, 1), (1, -1), 'LEFT'),     # Produit et description à gauche
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), # Alignement vertical au milieu

            # Bordures
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),

            # Alternance de couleurs
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),

            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(lines_table)
        elements.append(Spacer(1, 20))

        return elements

    def create_totals_section(self, invoice_data):
        """Crée la section des totaux"""
        elements = []

        # Table des totaux (alignée à droite)
        totals_data = [
            ['Subtotal:', f"{invoice_data.get('subtotal', 0):.2f} €"],
            ['IVA Total:', f"{invoice_data.get('iva_total', 0):.2f} €"],
            ['', ''],  # Ligne vide
            ['TOTAL:', f"{invoice_data.get('total', 0):.2f} €"]
        ]

        totals_table = Table(totals_data, colWidths=[4*cm, 3*cm])
        totals_table.setStyle(TableStyle([
            # Alignement
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Styles des labels
            ('FONTNAME', (0, 0), (0, -2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -2), 11),
            ('TEXTCOLOR', (0, 0), (0, -2), colors.HexColor('#2c3e50')),

            # Style du total final
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 14),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#e74c3c')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8f9fa')),

            # Bordures pour le total
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#e74c3c')),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.HexColor('#e74c3c')),

            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        # Centrer la table des totaux à droite
        totals_wrapper = Table([[totals_table]], colWidths=[self.page_width - 2*self.margin])
        totals_wrapper.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ]))

        elements.append(totals_wrapper)
        elements.append(Spacer(1, 30))

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

        # Ajouter la signature de génération automatique
        footer_parts.append(f"<i>Factura generada automáticamente por Facturación Fácil - {datetime.now().strftime('%d/%m/%Y %H:%M')}</i>")

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
