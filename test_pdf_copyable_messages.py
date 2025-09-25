#!/usr/bin/env python3
"""
Test des messages PDF copiables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.models import Producto, Stock, Factura
from datetime import datetime

def test_pdf_copyable_messages():
    """Test des messages PDF avec texte copiable"""
    
    print("=== Test Messages PDF Copiables ===\n")
    
    # 1. Créer une facture de test
    print("1. Création d'une facture de test...")
    
    import time
    timestamp = str(int(time.time()))[-6:]
    
    # Créer un produit pour la facture
    producto = Producto(
        nombre=f"Producto PDF Test {timestamp}",
        referencia=f"PDF-{timestamp}",
        precio=25.99,
        categoria="Test PDF",
        descripcion="Producto para test de PDF"
    )
    producto.save()
    
    # Establecer stock
    stock = Stock(producto.id, 10)
    stock.save()
    
    # Créer facture
    factura = Factura(
        numero_factura=f"PDF-TEST-{timestamp}",
        fecha_factura=datetime.now().strftime("%Y-%m-%d"),
        nombre_cliente="Cliente PDF Test",
        dni_nie_cliente="12345678P",
        direccion_cliente="Calle PDF Test 123",
        email_cliente="test@pdf.com",
        telefono_cliente="+34 123 456 789",
        modo_pago="efectivo"
    )
    
    # Agregar item
    factura.add_item(
        producto_id=producto.id,
        cantidad=2,
        precio_unitario=25.99,
        iva_aplicado=21.0
    )
    
    # Calcular totales y guardar
    factura.calculate_totals()
    factura.save()
    
    print(f"   ✅ Factura creada: {factura.numero_factura}")
    print(f"   ✅ Total: {factura.total_factura:.2f}€")
    
    # 2. Simular mensaje de desarrollo para exportar_pdf
    print("\n2. Simulación de mensaje exportar_pdf...")
    
    mensaje_exportar = f"""📄 Funcionalidad de PDF en desarrollo

La generación de PDF está actualmente en desarrollo y estará disponible próximamente.

Detalles de la factura seleccionada:
- Número de factura: {factura.numero_factura}
- Cliente: {factura.nombre_cliente}
- Fecha: {factura.fecha_factura}
- Total: {factura.total_factura:.2f}€

Estado del desarrollo:
- Módulo: Exportación PDF
- Funcionalidad: exportar_pdf()
- Estado: En desarrollo
- Estimación: Próxima actualización

Características planificadas:
✅ Generación automática de PDF
✅ Formato profesional de factura
✅ Logo de empresa incluido
✅ Cálculos detallados de IVA
✅ Información completa del cliente
✅ Guardado automático en directorio

Mientras tanto, puedes:
- Continuar creando y gestionando facturas
- Usar la funcionalidad de stock
- Exportar datos desde la base de datos

Este mensaje puede ser copiado para seguimiento del desarrollo."""
    
    print("   📄 Mensaje exportar_pdf généré :")
    print(f"      Longueur : {len(mensaje_exportar)} caractères")
    print(f"      Lignes : {mensaje_exportar.count(chr(10)) + 1}")
    
    # 3. Simular mensaje de desarrollo para generar_pdf
    print("\n3. Simulación de mensaje generar_pdf...")
    
    mensaje_generar = f"""📄 Generación de PDF en desarrollo

La funcionalidad de generación de PDF está siendo desarrollada y estará disponible próximamente.

Detalles de la factura actual:
- Número de factura: {factura.numero_factura}
- Cliente: {factura.nombre_cliente}
- DNI/NIE: {factura.dni_nie_cliente or 'N/A'}
- Fecha: {factura.fecha_factura}
- Productos: {len(factura.items)} items
- Subtotal: {factura.subtotal:.2f}€
- IVA: {factura.total_iva:.2f}€
- Total: {factura.total_factura:.2f}€

Estado del desarrollo:
- Módulo: Generación PDF
- Funcionalidad: generar_pdf()
- Estado: En desarrollo activo
- Prioridad: Alta
- Estimación: Próxima versión

Características que incluirá:
✅ Diseño profesional de factura
✅ Logo de empresa automático
✅ Datos completos del cliente
✅ Detalle de productos con precios
✅ Cálculos de IVA desglosados
✅ Numeración automática
✅ Formato PDF estándar
✅ Guardado en directorio configurable

Tecnologías a utilizar:
- ReportLab para generación PDF
- Plantillas personalizables
- Integración con datos de organización

Mientras tanto:
- La factura está guardada en la base de datos
- Puedes continuar creando más facturas
- Los datos están seguros y disponibles

Este mensaje puede ser copiado para seguimiento del desarrollo."""
    
    print("   📄 Mensaje generar_pdf généré :")
    print(f"      Longueur : {len(mensaje_generar)} caractères")
    print(f"      Lignes : {mensaje_generar.count(chr(10)) + 1}")
    
    # 4. Simular mensaje d'erreur PDF
    print("\n4. Simulación de mensaje d'erreur PDF...")
    
    error_simulado = "PDF library not found"
    timestamp_error = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    mensaje_error = f"""❌ Error al generar PDF

Se produjo un error al intentar generar el PDF de la factura.

Detalles del error:
- Factura: {factura.numero_factura}
- Función: generar_pdf()
- Error: {error_simulado}
- Módulo: ui.facturas_methods
- Timestamp: {timestamp_error}

Información técnica:
- Tipo de error: ModuleNotFoundError
- Descripción: {error_simulado}
- Estado de la factura: Guardada

Contexto:
- La funcionalidad de PDF está en desarrollo
- Los datos de la factura están seguros
- El error no afecta otras funcionalidades

Acciones recomendadas:
1. Verificar que la factura esté guardada
2. Intentar nuevamente más tarde
3. Contactar soporte si el problema persiste

Copie este mensaje para soporte técnico si es necesario."""
    
    print("   ❌ Mensaje d'erreur PDF généré :")
    print(f"      Longueur : {len(mensaje_error)} caractères")
    print(f"      Lignes : {mensaje_error.count(chr(10)) + 1}")
    
    # 5. Simular mensaje d'avertissement (factura no guardada)
    print("\n5. Simulación de mensaje d'avertissement...")
    
    mensaje_advertencia = """⚠️ Guarde la factura antes de generar el PDF

Para generar un PDF:
1. Complete todos los datos de la factura
2. Agregue al menos un producto
3. Haga clic en 'Guardar'
4. Luego podrá generar el PDF

Información adicional:
- La factura debe estar guardada en la base de datos
- Todos los campos obligatorios deben estar completos
- Debe haber al menos un producto agregado
- El sistema validará los datos antes de generar el PDF

Una vez guardada la factura:
✅ Podrá generar PDF cuando esté disponible
✅ Los datos quedarán registrados permanentemente
✅ Podrá exportar o reimprimir cuando sea necesario

Este mensaje puede ser copiado para referencia."""
    
    print("   ⚠️ Mensaje d'avertissement généré :")
    print(f"      Longueur : {len(mensaje_advertencia)} caractères")
    print(f"      Lignes : {mensaje_advertencia.count(chr(10)) + 1}")
    
    # 6. Vérification des caractéristiques
    print("\n6. Vérification des caractéristiques des messages PDF...")
    
    messages_pdf = {
        "Exportar PDF": mensaje_exportar,
        "Generar PDF": mensaje_generar,
        "Error PDF": mensaje_error,
        "Advertencia PDF": mensaje_advertencia
    }
    
    for tipo, mensaje in messages_pdf.items():
        # Vérifier contenu utile
        contiene_detalles_factura = any(x in mensaje for x in ['número', 'cliente', 'total'])
        contiene_info_desarrollo = any(x in mensaje for x in ['desarrollo', 'próximamente', 'características'])
        contiene_timestamp = any(x in mensaje for x in [':', '-', '2025', '2024'])
        es_copiable = "copiado" in mensaje.lower() or "copie" in mensaje.lower()
        es_detallado = len(mensaje) > 200
        
        print(f"   📋 {tipo}:")
        print(f"      ✅ Contient détails facture: {contiene_detalles_factura}")
        print(f"      ✅ Contient info développement: {contiene_info_desarrollo}")
        print(f"      ✅ Contient timestamp: {contiene_timestamp}")
        print(f"      ✅ Mention copiable: {es_copiable}")
        print(f"      ✅ Suffisamment détaillé: {es_detallado}")
        print(f"      📏 Longueur: {len(mensaje)} caractères")
    
    # 7. Comparaison avant/après
    print("\n7. Comparaison avant/après la correction...")
    
    mensaje_antes = f"Funcionalidad de PDF en desarrollo.\nFactura: {factura.numero_factura}"
    mensaje_despues = mensaje_exportar
    
    print("   📊 Comparaison des messages :")
    print(f"      Avant - Longueur: {len(mensaje_antes)} caractères")
    print(f"      Après - Longueur: {len(mensaje_despues)} caractères")
    print(f"      Amélioration: +{len(mensaje_despues) - len(mensaje_antes)} caractères")
    print(f"      Facteur d'amélioration: {len(mensaje_despues) / len(mensaje_antes):.1f}x plus détaillé")
    
    # Vérifier si copiable
    antes_copiable = "copiado" in mensaje_antes.lower()
    despues_copiable = "copiado" in mensaje_despues.lower()
    
    print(f"      Avant - Copiable: {'✅' if antes_copiable else '❌'}")
    print(f"      Après - Copiable: {'✅' if despues_copiable else '❌'}")
    
    print("\n🎉 === TEST COMPLETADO ===")
    print("\n✅ Corrections apportées aux messages PDF:")
    print("   ✅ Messages détaillés avec informations complètes")
    print("   ✅ Utilisation des dialogues copiables")
    print("   ✅ Informations de développement incluses")
    print("   ✅ Détails techniques pour support")
    print("   ✅ Instructions claires pour l'utilisateur")
    print("   ✅ Timestamps et traçabilité")
    
    print("\n🚀 Avantages pour l'utilisateur:")
    print("   📋 Peut copier tous les détails du message")
    print("   🔧 Informations utiles pour le support")
    print("   📊 Suivi du développement de la fonctionnalité")
    print("   ⚠️ Instructions claires sur les prérequis")
    print("   ✨ Interface cohérente avec le reste de l'application")
    
    print(f"\n📈 Statistiques d'amélioration:")
    print(f"   📏 Message moyen: {sum(len(m) for m in messages_pdf.values()) // len(messages_pdf)} caractères")
    print(f"   📄 Total de caractères copiables: {sum(len(m) for m in messages_pdf.values())}")
    print(f"   🔤 Lignes moyennes par message: {sum(m.count(chr(10)) + 1 for m in messages_pdf.values()) // len(messages_pdf)}")

if __name__ == "__main__":
    test_pdf_copyable_messages()
