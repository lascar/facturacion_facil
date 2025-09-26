# -*- coding: utf-8 -*-
"""
Generador de PDF para facturas
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from database.models import Organizacion
from utils.logger import get_logger

class PDFGenerator:
    """Generador de PDF para facturas"""
    
    def __init__(self):
        self.logger = get_logger("pdf_generator")
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        # Estilo para el título principal
        self.styles.add(ParagraphStyle(
            name='TituloFactura',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=20
        ))
        
        # Estilo para información de empresa
        self.styles.add(ParagraphStyle(
            name='InfoEmpresa',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Estilo para información de cliente
        self.styles.add(ParagraphStyle(
            name='InfoCliente',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=6
        ))
        
        # Estilo para totales
        self.styles.add(ParagraphStyle(
            name='Totales',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_RIGHT,
            fontName='Helvetica-Bold'
        ))
        
        # Estilo para observaciones
        self.styles.add(ParagraphStyle(
            name='Observaciones',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_LEFT,
            textColor=colors.grey
        ))
    
    def generar_factura_pdf(self, factura, output_path=None, auto_open=True):
        """
        Genera un PDF de la factura

        Args:
            factura: Objeto Factura con todos los datos
            output_path: Ruta donde guardar el PDF (opcional)
            auto_open: Si True, abre automáticamente el PDF generado

        Returns:
            str: Ruta del archivo PDF generado
        """
        try:
            # Determinar ruta de salida
            if not output_path:
                # Obtener directorio configurado de la organización
                from database.models import Organizacion
                org = Organizacion.get()

                if org.directorio_descargas_pdf and os.path.exists(org.directorio_descargas_pdf):
                    pdf_dir = org.directorio_descargas_pdf
                else:
                    # Fallback al directorio por defecto
                    pdf_dir = os.path.join(os.getcwd(), "pdfs")

                # Crear directorio si no existe
                os.makedirs(pdf_dir, exist_ok=True)

                # Nombre del archivo
                filename = f"Factura_{factura.numero_factura.replace('/', '_')}.pdf"
                output_path = os.path.join(pdf_dir, filename)
            
            # Crear documento PDF
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm
            )
            
            # Construir contenido
            story = []
            
            # Encabezado con información de empresa
            self.add_header(story, factura)
            
            # Información de la factura
            self.add_factura_info(story, factura)
            
            # Información del cliente
            self.add_cliente_info(story, factura)
            
            # Tabla de productos
            self.add_productos_table(story, factura)
            
            # Totales
            self.add_totales(story, factura)
            
            # Pie de página
            self.add_footer(story, factura)
            
            # Generar PDF
            doc.build(story)

            self.logger.info(f"PDF generado exitosamente: {output_path}")

            # Abrir automáticamente el PDF si se solicita
            if auto_open:
                self.open_pdf_file(output_path)

            return output_path

        except Exception as e:
            self.logger.error(f"Error generando PDF: {e}")
            raise

    def open_pdf_file(self, pdf_path):
        """Abre el archivo PDF con el visor configurado o el predeterminado del sistema"""
        try:
            import platform
            import subprocess

            # Obtener visor personalizado de la organización
            from database.models import Organizacion
            org = Organizacion.get()

            # Si hay un visor personalizado configurado y existe
            if org.visor_pdf_personalizado and os.path.exists(org.visor_pdf_personalizado):
                try:
                    # Usar el visor personalizado
                    subprocess.run([org.visor_pdf_personalizado, pdf_path], check=False)
                    self.logger.info(f"PDF abierto con visor personalizado: {org.visor_pdf_personalizado}")
                    return
                except Exception as e:
                    self.logger.warning(f"Error usando visor personalizado {org.visor_pdf_personalizado}: {e}")
                    # Continuar con el visor predeterminado

            # Usar el visor predeterminado del sistema
            system = platform.system()

            if system == "Windows":
                os.startfile(pdf_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux y otros
                subprocess.run(["xdg-open", pdf_path])

            self.logger.info(f"PDF abierto con visor predeterminado del sistema: {pdf_path}")

        except Exception as e:
            self.logger.warning(f"No se pudo abrir automáticamente el PDF: {e}")
            # No lanzar excepción, es una funcionalidad opcional
    
    def add_header(self, story, factura):
        """Añade el encabezado con información de la empresa y logo"""
        try:
            # Obtener información de la organización
            org = Organizacion.get()

            if org:
                # Crear tabla para logo y información de empresa
                header_data = []

                # Verificar si hay logo
                logo_cell = self.create_logo_image(org.logo_path)

                # Información de la empresa
                empresa_info = f"""
                <b>{org.nombre}</b><br/>
                <b>Dirección:</b> {org.direccion}<br/>
                <b>Teléfono:</b> {org.telefono}<br/>
                <b>Email:</b> {org.email}<br/>
                <b>CIF:</b> {org.cif}
                """

                empresa_paragraph = Paragraph(empresa_info, self.styles['InfoEmpresa'])

                # Si hay logo, crear tabla con logo a la izquierda y info a la derecha
                if logo_cell:
                    header_data = [[logo_cell, empresa_paragraph]]
                    header_table = Table(header_data, colWidths=[4*cm, 12*cm])
                    header_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Logo a la izquierda
                        ('ALIGN', (1, 0), (1, 0), 'LEFT'),   # Info a la izquierda
                        ('LEFTPADDING', (0, 0), (-1, -1), 0),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                        ('TOPPADDING', (0, 0), (-1, -1), 0),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ]))
                    story.append(header_table)
                else:
                    # Sin logo, solo información de empresa
                    story.append(empresa_paragraph)

                # Título FACTURA centrado
                factura_title = Paragraph(
                    "<b>FACTURA</b>",
                    self.styles['TituloFactura']
                )
                story.append(factura_title)

            else:
                # Información por defecto si no hay organización configurada
                default_title = Paragraph("<b>FACTURA</b>", self.styles['TituloFactura'])
                story.append(default_title)

            story.append(Spacer(1, 0.5*cm))

        except Exception as e:
            self.logger.error(f"Error añadiendo encabezado: {e}")
            # Añadir título básico en caso de error
            story.append(Paragraph("<b>FACTURA</b>", self.styles['TituloFactura']))
            story.append(Spacer(1, 1*cm))

    def create_logo_image(self, logo_path, max_width=3*cm, max_height=3*cm):
        """Crea una imagen del logo con redimensionamiento proporcional"""
        if not logo_path or not os.path.exists(logo_path):
            return None

        try:
            from PIL import Image as PILImage

            # Abrir imagen para obtener dimensiones originales
            with PILImage.open(logo_path) as pil_img:
                original_width, original_height = pil_img.size

            # Calcular dimensiones manteniendo proporción
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            scale_ratio = min(width_ratio, height_ratio)

            # Nuevas dimensiones
            new_width = original_width * scale_ratio
            new_height = original_height * scale_ratio

            # Crear imagen ReportLab con dimensiones calculadas
            logo_img = Image(logo_path, width=new_width, height=new_height)

            self.logger.debug(f"Logo cargado: {os.path.basename(logo_path)} ({new_width:.1f}x{new_height:.1f})")
            return logo_img

        except Exception as e:
            self.logger.warning(f"Error cargando logo {logo_path}: {e}")
            return None

    def add_factura_info(self, story, factura):
        """Añade información básica de la factura"""
        # Crear tabla con información de factura
        factura_data = [
            ['Número de Factura:', factura.numero_factura],
            ['Fecha:', factura.fecha_factura],
            ['Modo de Pago:', factura.modo_pago.title()]
        ]
        
        factura_table = Table(factura_data, colWidths=[4*cm, 6*cm])
        factura_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(factura_table)
        story.append(Spacer(1, 0.5*cm))
    
    def add_cliente_info(self, story, factura):
        """Añade información del cliente"""
        cliente_title = Paragraph("<b>DATOS DEL CLIENTE</b>", self.styles['Heading2'])
        story.append(cliente_title)
        
        # Información del cliente
        cliente_info = f"""
        <b>Nombre:</b> {factura.nombre_cliente}<br/>
        """
        
        if factura.dni_nie_cliente:
            cliente_info += f"<b>DNI/NIE:</b> {factura.dni_nie_cliente}<br/>"
        
        if factura.direccion_cliente:
            cliente_info += f"<b>Dirección:</b> {factura.direccion_cliente}<br/>"
        
        if factura.telefono_cliente:
            cliente_info += f"<b>Teléfono:</b> {factura.telefono_cliente}<br/>"
        
        if factura.email_cliente:
            cliente_info += f"<b>Email:</b> {factura.email_cliente}<br/>"
        
        cliente_paragraph = Paragraph(cliente_info, self.styles['InfoCliente'])
        story.append(cliente_paragraph)
        story.append(Spacer(1, 0.5*cm))
    
    def add_productos_table(self, story, factura):
        """Añade la tabla de productos"""
        productos_title = Paragraph("<b>DETALLE DE PRODUCTOS</b>", self.styles['Heading2'])
        story.append(productos_title)
        story.append(Spacer(1, 0.3*cm))
        
        # Encabezados de la tabla
        headers = ['Producto', 'Cantidad', 'Precio Unit.', 'IVA %', 'Subtotal', 'Total']
        
        # Datos de productos
        productos_data = [headers]
        
        for item in factura.items:
            producto = item.get_producto()
            producto_nombre = producto.nombre if producto else f"Producto ID: {item.producto_id}"
            
            subtotal = item.cantidad * item.precio_unitario
            iva_amount = subtotal * (item.iva_aplicado / 100)
            total_item = subtotal + iva_amount
            
            row = [
                producto_nombre,
                str(item.cantidad),
                f"{item.precio_unitario:.2f}€",
                f"{item.iva_aplicado:.1f}%",
                f"{subtotal:.2f}€",
                f"{total_item:.2f}€"
            ]
            productos_data.append(row)
        
        # Crear tabla
        productos_table = Table(productos_data, colWidths=[6*cm, 2*cm, 2.5*cm, 2*cm, 2.5*cm, 2.5*cm])
        
        # Estilo de la tabla
        productos_table.setStyle(TableStyle([
            # Encabezados
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Datos
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Cantidad, precios centrados
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),     # Nombre producto a la izquierda
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            
            # Alternar colores de filas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(productos_table)
        story.append(Spacer(1, 0.5*cm))
    
    def add_totales(self, story, factura):
        """Añade la sección de totales"""
        # Crear tabla de totales
        totales_data = [
            ['Subtotal:', f"{factura.subtotal:.2f}€"],
            ['IVA:', f"{factura.total_iva:.2f}€"],
            ['TOTAL:', f"{factura.total_factura:.2f}€"]
        ]
        
        totales_table = Table(totales_data, colWidths=[4*cm, 3*cm])
        totales_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 1), 12),
            ('FONTSIZE', (0, 2), (-1, 2), 14),  # Total más grande
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            
            # Línea superior para el total
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.darkblue),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.darkblue),
        ]))
        
        # Alinear a la derecha
        totales_frame = Table([[totales_table]], colWidths=[17*cm])
        totales_frame.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ]))
        
        story.append(totales_frame)
        story.append(Spacer(1, 1*cm))
    
    def add_footer(self, story, factura):
        """Añade pie de página con observaciones"""
        # Observaciones generales
        observaciones = f"""
        <b>Observaciones:</b><br/>
        • Esta factura ha sido generada automáticamente por el sistema de facturación.<br/>
        • Fecha de generación: {datetime.now().strftime("%d/%m/%Y %H:%M")}<br/>
        • Para cualquier consulta, contacte con nosotros usando los datos de contacto indicados.<br/>
        """
        
        # Agregar observaciones personalizadas si existen
        if hasattr(factura, 'observaciones') and factura.observaciones:
            observaciones += f"• {factura.observaciones}<br/>"
        
        observaciones_paragraph = Paragraph(observaciones, self.styles['Observaciones'])
        story.append(observaciones_paragraph)
        
        # Línea de separación
        story.append(Spacer(1, 0.5*cm))
        linea = Table([['_' * 100]], colWidths=[17*cm])
        linea.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (0, 0), 8),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.grey),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ]))
        story.append(linea)
        
        # Texto final
        final_text = Paragraph(
            "<i>Gracias por confiar en nuestros servicios</i>",
            self.styles['Observaciones']
        )
        story.append(final_text)
