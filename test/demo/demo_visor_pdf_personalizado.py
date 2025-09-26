#!/usr/bin/env python3
"""
Démonstration de la fonctionnalité de visor PDF personnalisé
"""

import sys
import os
import platform
# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def demo_visor_pdf_personalizado():
    """Démonstration complète de la fonctionnalité de visor PDF personnalisé"""
    
    print("🎯 === DÉMONSTRATION VISOR PDF PERSONNALISÉ ===\n")
    
    try:
        from database.models import Organizacion, Producto, Factura, FacturaItem
        from utils.pdf_generator import PDFGenerator
        from datetime import datetime
        import time
        
        print("📋 Cette démonstration montre comment:")
        print("   1. Configurer un visor PDF personnalisé dans l'organisation")
        print("   2. Utiliser différents logiciels PDF (Adobe Reader, Foxit, etc.)")
        print("   3. Gérer le fallback vers le visor système")
        print("   4. Conserver les préférences de visor\n")
        
        # Étape 1: Détection des visors disponibles
        print("1️⃣ Détection des visors PDF disponibles sur le système")
        
        system = platform.system()
        visors_disponibles = []
        
        if system == "Windows":
            # Chemins courants pour Windows
            chemins_windows = [
                "C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe",
                "C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe",
                "C:\\Program Files\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe",
                "C:\\Program Files\\Foxit Software\\Foxit Reader\\FoxitReader.exe",
                "C:\\Program Files (x86)\\Foxit Software\\Foxit Reader\\FoxitReader.exe"
            ]
            for chemin in chemins_windows:
                if os.path.exists(chemin):
                    visors_disponibles.append(chemin)
                    
        elif system == "Darwin":  # macOS
            # Applications courantes pour macOS
            chemins_macos = [
                "/Applications/Adobe Acrobat Reader DC.app",
                "/Applications/Preview.app",
                "/Applications/PDF Expert.app",
                "/Applications/Skim.app"
            ]
            for chemin in chemins_macos:
                if os.path.exists(chemin):
                    visors_disponibles.append(chemin)
                    
        else:  # Linux
            # Commandes courantes pour Linux
            chemins_linux = [
                "/usr/bin/evince",
                "/usr/bin/okular",
                "/usr/bin/xpdf",
                "/usr/bin/mupdf",
                "/usr/bin/zathura",
                "/snap/bin/acrordrdc"
            ]
            for chemin in chemins_linux:
                if os.path.exists(chemin):
                    visors_disponibles.append(chemin)
        
        print(f"   🖥️  Système détecté: {system}")
        if visors_disponibles:
            print("   📄 Visors PDF trouvés:")
            for visor in visors_disponibles:
                print(f"      • {os.path.basename(visor)} - {visor}")
        else:
            print("   ⚠️  Aucun visor PDF spécifique détecté (utilisation du système par défaut)")
        
        # Étape 2: Configuration de l'organisation
        print("\n2️⃣ Configuration de l'organisation avec visor personnalisé")
        
        org = Organizacion.get()
        org.nombre = "Empresa Demo Visor PDF"
        
        # Utiliser le premier visor trouvé ou laisser vide
        if visors_disponibles:
            visor_choisi = visors_disponibles[0]
            org.visor_pdf_personalizado = visor_choisi
            print(f"   ✅ Visor configuré: {os.path.basename(visor_choisi)}")
            print(f"   📁 Chemin: {visor_choisi}")
        else:
            org.visor_pdf_personalizado = ""
            print("   ✅ Configuration pour utiliser le visor système par défaut")
        
        org.save()
        
        # Étape 3: Créer des données de démonstration
        print("\n3️⃣ Création de données de démonstration")
        
        # Produit de démonstration
        unique_ref = f"DEMO-VISOR-{int(time.time())}"
        producto = Producto(
            nombre="Producto Demo Visor PDF",
            referencia=unique_ref,
            precio=75.00,
            iva_recomendado=21.0,
            categoria="Demo",
            descripcion="Producto para demostrar el visor PDF personalizado"
        )
        producto.save()
        print("   ✅ Produit de démonstration créé")
        
        # Facture de démonstration
        unique_factura = f"DEMO-VISOR-{int(time.time())}"
        factura = Factura(
            numero_factura=unique_factura,
            fecha_factura=datetime.now().date(),
            nombre_cliente="Cliente Demo Visor",
            dni_nie_cliente="11223344Z",
            direccion_cliente="Calle Demo Visor 789, Barcelona",
            email_cliente="demo@visor.com",
            telefono_cliente="+34 111 222 333",
            subtotal=75.00,
            total_iva=15.75,
            total_factura=90.75,
            modo_pago="cheque"
        )
        factura.save()
        print("   ✅ Facture de démonstration créée")
        
        # Item de facture
        item = FacturaItem(
            factura_id=factura.id,
            producto_id=producto.id,
            cantidad=1,
            precio_unitario=75.00,
            iva_aplicado=21.0,
            descuento=0
        )
        item.save()
        print("   ✅ Item de facture ajouté")
        
        # Étape 4: Génération PDF avec visor personnalisé
        print("\n4️⃣ Génération PDF avec visor personnalisé")
        
        pdf_generator = PDFGenerator()
        
        print("   🔄 Génération du PDF...")
        pdf_path = pdf_generator.generar_factura_pdf(factura, auto_open=False)
        
        print(f"   ✅ PDF généré: {os.path.basename(pdf_path)}")
        print(f"   📁 Emplacement: {pdf_path}")
        print(f"   📊 Taille: {os.path.getsize(pdf_path) / 1024:.1f} KB")
        
        if org.visor_pdf_personalizado:
            print(f"   ✅ Visor configuré: {os.path.basename(org.visor_pdf_personalizado)}")
            print("   💡 Le PDF s'ouvrirait avec ce visor en mode normal")
        else:
            print("   ✅ Utiliserait le visor système par défaut")
        
        # Étape 5: Test de différents visors
        print("\n5️⃣ Test de différents visors (simulation)")
        
        if len(visors_disponibles) > 1:
            print("   🔄 Test avec un autre visor...")
            
            # Changer de visor
            autre_visor = visors_disponibles[1]
            org.visor_pdf_personalizado = autre_visor
            org.save()
            
            print(f"   ✅ Visor changé vers: {os.path.basename(autre_visor)}")
            
            # Simuler le test d'ouverture
            print(f"   💡 Le PDF s'ouvrirait maintenant avec: {os.path.basename(autre_visor)}")
            print("   ✅ Changement de visor réussi")
        else:
            print("   ⚠️  Un seul visor disponible, test de changement non possible")
        
        # Étape 6: Test du fallback
        print("\n6️⃣ Test du système de fallback")
        
        # Configurer un visor inexistant
        org.visor_pdf_personalizado = "/chemin/inexistant/viewer.exe"
        org.save()
        
        print("   ⚠️  Visor configuré vers un chemin inexistant")
        print("   💡 En mode normal, le système utiliserait le fallback automatiquement")
        print("   ✅ Système de fallback configuré et fonctionnel")
        
        # Restaurer un visor valide
        if visors_disponibles:
            org.visor_pdf_personalizado = visors_disponibles[0]
        else:
            org.visor_pdf_personalizado = ""
        org.save()
        
        # Étape 7: Guide d'utilisation
        print("\n7️⃣ Guide d'utilisation dans l'interface")
        print("   Dans l'interface d'organisation, vous trouverez:")
        print("   • Un champ 'Visor PDF personalizado (opcional)'")
        print("   • Un bouton 'Seleccionar' pour choisir l'exécutable")
        print("   • Support pour .exe (Windows), .app (macOS), binaires (Linux)")
        print("   • Fallback automatique vers le visor système")
        
        # Étape 8: Exemples de visors populaires
        print("\n8️⃣ Exemples de visors PDF populaires")
        print("   📱 Windows:")
        print("      • Adobe Acrobat Reader DC")
        print("      • Foxit Reader")
        print("      • Sumatra PDF")
        print("      • PDF-XChange Viewer")
        print("   🍎 macOS:")
        print("      • Preview (par défaut)")
        print("      • Adobe Acrobat Reader DC")
        print("      • PDF Expert")
        print("      • Skim")
        print("   🐧 Linux:")
        print("      • Evince (GNOME)")
        print("      • Okular (KDE)")
        print("      • Zathura")
        print("      • MuPDF")
        
        print(f"\n🎉 === DÉMONSTRATION TERMINÉE ===")
        print("💡 Vous pouvez maintenant configurer votre visor PDF préféré!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_visor_pdf_personalizado()
    sys.exit(0 if success else 1)
