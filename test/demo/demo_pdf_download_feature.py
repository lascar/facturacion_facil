#!/usr/bin/env python3
"""
Démonstration de la nouvelle fonctionnalité de téléchargement PDF configurable
"""

import sys
import os
import tempfile
# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def demo_pdf_download_feature():
    """Démonstration complète de la fonctionnalité"""
    
    print("🎯 === DÉMONSTRATION FONCTIONNALITÉ TÉLÉCHARGEMENT PDF ===\n")
    
    try:
        from database.models import Organizacion, Producto, Factura, FacturaItem
        from utils.pdf_generator import PDFGenerator
        from datetime import datetime
        import time
        
        print("📋 Cette démonstration montre comment:")
        print("   1. Configurer un répertoire de téléchargement PDF dans l'organisation")
        print("   2. Générer des PDFs qui s'ouvrent automatiquement")
        print("   3. Utiliser le répertoire configuré pour sauvegarder les PDFs")
        print("   4. Conserver le dernier choix de répertoire\n")
        
        # Étape 1: Configuration de l'organisation
        print("1️⃣ Configuration de l'organisation avec répertoire PDF")
        
        # Créer un répertoire de démonstration
        demo_dir = os.path.expanduser("~/Downloads/Facturas_Demo")
        os.makedirs(demo_dir, exist_ok=True)
        print(f"   📁 Répertoire créé: {demo_dir}")
        
        # Configurer l'organisation
        org = Organizacion.get()
        org.nombre = "Empresa Demo PDF"
        org.directorio_descargas_pdf = demo_dir
        org.save()
        print("   ✅ Organisation configurée avec répertoire PDF")
        
        # Étape 2: Créer des données de démonstration
        print("\n2️⃣ Création de données de démonstration")
        
        # Produit de démonstration
        unique_ref = f"DEMO-{int(time.time())}"
        producto = Producto(
            nombre="Producto Demostración",
            referencia=unique_ref,
            precio=99.99,
            iva_recomendado=21.0,
            categoria="Demo",
            descripcion="Producto para demostrar la funcionalidad PDF"
        )
        producto.save()
        print("   ✅ Produit de démonstration créé")
        
        # Facture de démonstration
        unique_factura = f"DEMO-{int(time.time())}"
        factura = Factura(
            numero_factura=unique_factura,
            fecha_factura=datetime.now().date(),
            nombre_cliente="Cliente Demostración",
            dni_nie_cliente="12345678Z",
            direccion_cliente="Calle Demo 123, Madrid",
            email_cliente="demo@cliente.com",
            telefono_cliente="+34 123 456 789",
            subtotal=99.99,
            total_iva=20.99,
            total_factura=120.98,
            modo_pago="tarjeta"
        )
        factura.save()
        print("   ✅ Facture de démonstration créée")
        
        # Item de facture
        item = FacturaItem(
            factura_id=factura.id,
            producto_id=producto.id,
            cantidad=1,
            precio_unitario=99.99,
            iva_aplicado=21.0,
            descuento=0
        )
        item.save()
        print("   ✅ Item de facture ajouté")
        
        # Étape 3: Génération PDF avec ouverture automatique
        print("\n3️⃣ Génération PDF avec ouverture automatique")
        
        pdf_generator = PDFGenerator()
        
        print("   🔄 Génération du PDF...")
        pdf_path = pdf_generator.generar_factura_pdf(factura, auto_open=False)
        
        print(f"   ✅ PDF généré: {os.path.basename(pdf_path)}")
        print(f"   📁 Emplacement: {pdf_path}")
        print(f"   📊 Taille: {os.path.getsize(pdf_path) / 1024:.1f} KB")
        print("   💡 En mode normal, le PDF s'ouvrirait automatiquement!")
        
        # Étape 4: Démonstration du fallback
        print("\n4️⃣ Démonstration du système de fallback")
        
        # Sauvegarder le répertoire actuel
        original_dir = org.directorio_descargas_pdf
        
        # Configurer un répertoire inexistant
        org.directorio_descargas_pdf = "/repertoire/inexistant"
        org.save()
        
        print("   ⚠️  Répertoire configuré inexistant")
        print("   🔄 Génération PDF avec fallback...")
        
        pdf_path_fallback = pdf_generator.generar_factura_pdf(factura, auto_open=False)
        print(f"   ✅ PDF généré avec fallback: {os.path.basename(pdf_path_fallback)}")
        print(f"   📁 Emplacement fallback: {pdf_path_fallback}")
        
        # Restaurer le répertoire original
        org.directorio_descargas_pdf = original_dir
        org.save()
        print("   🔄 Répertoire original restauré")
        
        # Étape 5: Informations sur l'interface utilisateur
        print("\n5️⃣ Interface utilisateur")
        print("   Dans l'interface d'organisation, vous trouverez:")
        print("   • Un nouveau champ 'Directorio por defecto para descargas de PDF'")
        print("   • Un bouton 'Seleccionar' pour choisir le répertoire")
        print("   • Le dernier répertoire choisi est conservé automatiquement")
        print("   • Les PDFs générés s'ouvrent automatiquement")
        
        # Étape 6: Avantages de la fonctionnalité
        print("\n6️⃣ Avantages de cette fonctionnalité")
        print("   ✅ PDFs sauvegardés dans un répertoire choisi par l'utilisateur")
        print("   ✅ Ouverture automatique pour visualisation immédiate")
        print("   ✅ Conservation du dernier choix de répertoire")
        print("   ✅ Système de fallback robuste")
        print("   ✅ Compatible avec tous les systèmes d'exploitation")
        print("   ✅ Intégration transparente avec l'interface existante")
        
        print(f"\n🎉 === DÉMONSTRATION TERMINÉE ===")
        print(f"📁 Vos PDFs de démonstration sont dans: {demo_dir}")
        print("💡 Vous pouvez maintenant utiliser cette fonctionnalité dans l'application!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_pdf_download_feature()
    sys.exit(0 if success else 1)
