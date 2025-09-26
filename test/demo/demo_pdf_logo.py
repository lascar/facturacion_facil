#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du logo dans les PDFs
Ce script génère un PDF avec logo pour vérification visuelle
"""

import os
import sys
import tempfile
from PIL import Image, ImageDraw, ImageFont

# Ajouter le répertoire racine au path pour les imports
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, root_dir)

from database.models import Organizacion, Factura, FacturaItem, Producto
from utils.pdf_generator import PDFGenerator


def create_demo_logo():
    """Crée un logo de démonstration"""
    temp_dir = tempfile.mkdtemp()
    logo_path = os.path.join(temp_dir, "demo_logo.png")
    
    # Créer un logo professionnel
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Fond dégradé simulé avec rectangles
    colors = ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd']
    for i, color in enumerate(colors):
        y_start = i * 50
        y_end = (i + 1) * 50
        draw.rectangle([0, y_start, 400, y_end], fill=color)
    
    # Texte de l'entreprise
    try:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    except:
        font_large = None
        font_small = None
    
    # Nom de l'entreprise
    draw.text((50, 60), "FACTURACIÓN FÁCIL", fill='white', font=font_large)
    draw.text((50, 100), "Soluciones de Facturación", fill='white', font=font_small)
    
    # Icône simple (círculo)
    draw.ellipse([300, 50, 370, 120], fill='#fbbf24', outline='white', width=3)
    draw.text((320, 75), "€", fill='white', font=font_large)
    
    img.save(logo_path)
    return logo_path


def demo_pdf_with_logo():
    """Démonstration de génération PDF avec logo"""
    print("🎯 Démonstration du logo dans les PDFs")
    print("=" * 50)
    
    # Créer logo de démonstration
    print("\n1️⃣ Création du logo de démonstration...")
    logo_path = create_demo_logo()
    print(f"   ✅ Logo créé: {os.path.basename(logo_path)}")
    
    try:
        # Configurer organisation avec logo
        print("\n2️⃣ Configuration de l'organisation avec logo...")
        org = Organizacion(
            nombre="Facturación Fácil S.L.",
            direccion="Calle Innovación 123, 28001 Madrid, España",
            telefono="+34 91 123 45 67",
            email="info@facturacionfacil.es",
            cif="B12345678",
            logo_path=logo_path
        )
        org.save()
        print(f"   ✅ Organización configurada: {org.nombre}")
        print(f"   🖼️  Logo asignado: {os.path.basename(logo_path)}")
        
        # Crear productos de demostración
        print("\n3️⃣ Creación de productos de demostración...")
        productos = [
            Producto(
                nombre="Licencia Software Anual",
                referencia="LIC-2024-001",
                precio=299.99,
                categoria="Software",
                descripcion="Licencia anual del software de facturación",
                iva_recomendado=21.0
            ),
            Producto(
                nombre="Soporte Técnico Premium",
                referencia="SUP-PREM-001",
                precio=150.00,
                categoria="Servicios",
                descripcion="Soporte técnico premium 24/7",
                iva_recomendado=21.0
            ),
            Producto(
                nombre="Formación Personalizada",
                referencia="FORM-PERS-001",
                precio=450.00,
                categoria="Formación",
                descripcion="Formación personalizada en el uso del software",
                iva_recomendado=21.0
            )
        ]
        
        for producto in productos:
            producto.save()
            print(f"   ✅ Producto creado: {producto.nombre}")
        
        # Crear factura completa
        print("\n4️⃣ Creación de factura de demostración...")
        factura = Factura(
            numero_factura="DEMO-2024-001",
            fecha_factura="2024-01-15",
            nombre_cliente="Empresa Cliente Demo S.L.",
            dni_nie_cliente="B87654321",
            direccion_cliente="Avenida Cliente 456, 08001 Barcelona, España",
            email_cliente="cliente@empresademo.com",
            telefono_cliente="+34 93 987 65 43",
            subtotal=0.0,
            total_iva=0.0,
            total_factura=0.0,
            modo_pago="transferencia"
        )
        factura.save()
        print(f"   ✅ Factura creada: {factura.numero_factura}")
        
        # Añadir items a la factura
        print("\n5️⃣ Añadiendo items a la factura...")
        items_data = [
            (productos[0].id, 1, 299.99),  # 1 licencia
            (productos[1].id, 6, 150.00),  # 6 meses soporte
            (productos[2].id, 1, 450.00)   # 1 formación
        ]
        
        items = []
        subtotal = 0.0
        total_iva = 0.0
        
        for producto_id, cantidad, precio_unitario in items_data:
            item = FacturaItem(
                factura_id=factura.id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                iva_aplicado=21.0,
                descuento=0.0
            )
            item.calculate_totals()
            item.save()
            items.append(item)
            
            subtotal += item.subtotal
            total_iva += item.iva_amount
            
            producto = Producto.get_by_id(producto_id)
            print(f"   ✅ Item añadido: {cantidad}x {producto.nombre} = {item.total:.2f}€")
        
        # Actualizar totales de la factura
        factura.subtotal = subtotal
        factura.total_iva = total_iva
        factura.total_factura = subtotal + total_iva
        factura.save()
        factura.items = items
        
        print(f"\n   💰 Subtotal: {factura.subtotal:.2f}€")
        print(f"   💰 IVA: {factura.total_iva:.2f}€")
        print(f"   💰 Total: {factura.total_factura:.2f}€")
        
        # Generar PDF
        print("\n6️⃣ Generación del PDF con logo...")
        pdf_generator = PDFGenerator()
        
        # Crear archivo en directorio actual
        output_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(output_dir, "demo_factura_con_logo.pdf")
        
        result_path = pdf_generator.generar_factura_pdf(
            factura, 
            output_path=pdf_path, 
            auto_open=False
        )
        
        print(f"   ✅ PDF generado exitosamente!")
        print(f"   📄 Archivo: {pdf_path}")
        print(f"   📊 Tamaño: {os.path.getsize(pdf_path)} bytes")
        
        # Verificaciones
        print("\n7️⃣ Verificaciones...")
        assert os.path.exists(pdf_path), "El archivo PDF no existe"
        assert os.path.getsize(pdf_path) > 1000, "El archivo PDF es demasiado pequeño"
        print("   ✅ PDF existe y tiene contenido")
        
        print("\n🎉 ¡Démonstration completada exitosamente!")
        print(f"\n📋 Resumen:")
        print(f"   🏢 Empresa: {org.nombre}")
        print(f"   🖼️  Logo: Incluido en el PDF")
        print(f"   📄 Factura: {factura.numero_factura}")
        print(f"   💰 Total: {factura.total_factura:.2f}€")
        print(f"   📁 Archivo: {pdf_path}")
        
        print(f"\n🔍 Para verificar el logo, abra el archivo PDF:")
        print(f"   {pdf_path}")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error durante la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        # Limpiar logo temporal
        if os.path.exists(logo_path):
            os.unlink(logo_path)
            temp_dir = os.path.dirname(logo_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)


if __name__ == "__main__":
    demo_pdf_with_logo()
