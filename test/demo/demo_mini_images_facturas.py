#!/usr/bin/env python3
"""
Démonstration des mini images dans les lignes de factures
"""
import sys
import os
import tempfile
from PIL import Image

# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def demo_mini_images_facturas():
    """Démonstration complète des mini images dans les factures"""
    
    print("🎨 === DÉMONSTRATION MINI IMAGES DANS FACTURES ===\n")
    
    try:
        from utils.image_utils import ImageUtils
        from database.models import Producto, FacturaItem, Factura
        from datetime import datetime
        import time
        
        print("📋 Cette démonstration montre comment:")
        print("   1. Les produits affichent leurs images dans les lignes de facture")
        print("   2. Les images sont automatiquement redimensionnées en mini format")
        print("   3. Un placeholder est affiché pour les produits sans image")
        print("   4. Le cache d'images optimise les performances\n")
        
        # Étape 1: Créer des images de test
        print("1️⃣ Création d'images de test")
        
        temp_dir = tempfile.mkdtemp(prefix="demo_images_")
        print(f"   📁 Répertoire temporaire: {temp_dir}")
        
        # Créer différentes images de produits
        images_created = []
        
        # Image 1: Produit électronique (bleu)
        img1_path = os.path.join(temp_dir, "producto_electronico.png")
        img1 = Image.new('RGB', (120, 80), color='blue')
        img1.save(img1_path)
        images_created.append(("Producto Electrónico", img1_path))
        
        # Image 2: Produit alimentaire (vert)
        img2_path = os.path.join(temp_dir, "producto_alimentario.png")
        img2 = Image.new('RGB', (80, 120), color='green')
        img2.save(img2_path)
        images_created.append(("Producto Alimentario", img2_path))
        
        # Image 3: Produit textile (rouge)
        img3_path = os.path.join(temp_dir, "producto_textil.png")
        img3 = Image.new('RGB', (100, 100), color='red')
        img3.save(img3_path)
        images_created.append(("Producto Textil", img3_path))
        
        print(f"   ✅ {len(images_created)} images de test créées")
        
        # Étape 2: Créer des produits avec et sans images
        print("\n2️⃣ Création de produits de démonstration")
        
        productos = []
        
        # Produits avec images
        for i, (nombre, imagen_path) in enumerate(images_created, 1):
            unique_ref = f"DEMO-IMG-{int(time.time())}-{i}"
            producto = Producto(
                nombre=nombre,
                referencia=unique_ref,
                precio=50.00 + (i * 10),
                iva_recomendado=21.0,
                imagen_path=imagen_path,
                categoria="Demo con Imagen",
                descripcion=f"Producto de demostración {i} con imagen"
            )
            producto.save()
            productos.append(producto)
            print(f"   ✅ {nombre} creado con imagen")
        
        # Produit sans image
        unique_ref = f"DEMO-NO-IMG-{int(time.time())}"
        producto_sin_imagen = Producto(
            nombre="Producto Sin Imagen",
            referencia=unique_ref,
            precio=25.00,
            iva_recomendado=21.0,
            imagen_path="",  # Pas d'image
            categoria="Demo sin Imagen",
            descripcion="Producto de demostración sin imagen"
        )
        producto_sin_imagen.save()
        productos.append(producto_sin_imagen)
        print("   ✅ Producto Sin Imagen creado")
        
        # Étape 3: Test des utilitaires d'image
        print("\n3️⃣ Test des utilitaires d'image")
        
        # Test de création de mini images
        for producto in productos[:3]:  # Seulement ceux avec images
            print(f"   🔄 Test mini image pour: {producto.nombre}")
            
            mini_image = ImageUtils.create_mini_image(
                producto.imagen_path,
                ImageUtils.get_mini_image_size()
            )
            
            if mini_image:
                print(f"      ✅ Mini image créée (taille: {ImageUtils.get_mini_image_size()})")
            else:
                print(f"      ❌ Erreur création mini image")
        
        # Test placeholder
        print("   🔄 Test image placeholder")
        placeholder = ImageUtils.create_placeholder_image(ImageUtils.get_mini_image_size())
        if placeholder:
            print("      ✅ Image placeholder créée")
        else:
            print("      ❌ Erreur création placeholder")
        
        # Étape 4: Créer une facture de démonstration
        print("\n4️⃣ Création d'une facture de démonstration")
        
        unique_factura = f"DEMO-MINI-IMG-{int(time.time())}"
        factura = Factura(
            numero_factura=unique_factura,
            fecha_factura=datetime.now().date(),
            nombre_cliente="Cliente Demo Mini Imágenes",
            dni_nie_cliente="12345678Z",
            direccion_cliente="Calle Demo 123, Madrid",
            email_cliente="demo@miniimg.com",
            telefono_cliente="+34 123 456 789",
            subtotal=0,  # Se calculará
            total_iva=0,  # Se calculará
            total_factura=0,  # Se calculará
            modo_pago="tarjeta"
        )
        factura.save()
        print(f"   ✅ Factura creada: {unique_factura}")
        
        # Étape 5: Ajouter items à la facture
        print("\n5️⃣ Ajout d'items avec images à la facture")
        
        factura_items = []
        total_subtotal = 0
        total_iva = 0
        
        for i, producto in enumerate(productos, 1):
            item = FacturaItem(
                factura_id=factura.id,
                producto_id=producto.id,
                cantidad=i,  # Quantités différentes
                precio_unitario=producto.precio,
                iva_aplicado=21.0,
                descuento=0 if i % 2 == 0 else 5  # Alternance avec/sans remise
            )
            item.save()
            factura_items.append(item)
            
            # Calculer totaux
            subtotal_item = item.cantidad * item.precio_unitario * (1 - item.descuento / 100)
            iva_item = subtotal_item * (item.iva_aplicado / 100)
            total_subtotal += subtotal_item
            total_iva += iva_item
            
            status_img = "🖼️" if producto.imagen_path else "📷"
            print(f"   {status_img} {producto.nombre} - Qty: {item.cantidad} - €{producto.precio}")
        
        # Mettre à jour les totaux de la facture
        factura.subtotal = total_subtotal
        factura.total_iva = total_iva
        factura.total_factura = total_subtotal + total_iva
        factura.save()
        
        print(f"   ✅ {len(factura_items)} items ajoutés à la facture")
        
        # Étape 6: Simulation de l'affichage dans l'interface
        print("\n6️⃣ Simulation de l'affichage dans l'interface")
        
        print("   📋 Aperçu de la facture avec mini images:")
        print("   " + "="*70)
        print("   | Img | Producto                    | Qty | Precio | Total    |")
        print("   " + "="*70)
        
        for item in factura_items:
            producto = next(p for p in productos if p.id == item.producto_id)
            img_icon = "🖼️ " if producto.imagen_path else "📷 "
            total_item = item.cantidad * item.precio_unitario * (1 - item.descuento / 100)
            total_item += total_item * (item.iva_aplicado / 100)
            
            print(f"   | {img_icon} | {producto.nombre[:25]:<25} | {item.cantidad:3} | €{item.precio_unitario:5.2f} | €{total_item:6.2f} |")
        
        print("   " + "="*70)
        print(f"   | Total Factura: €{factura.total_factura:.2f}")
        print("   " + "="*70)
        
        # Étape 7: Test du cache d'images
        print("\n7️⃣ Test du cache d'images")
        
        image_utils = ImageUtils()
        
        # Premier chargement
        start_time = time.time()
        for producto in productos[:3]:
            if producto.imagen_path:
                image_utils.get_cached_mini_image(producto.imagen_path)
        first_load_time = time.time() - start_time
        
        # Deuxième chargement (depuis le cache)
        start_time = time.time()
        for producto in productos[:3]:
            if producto.imagen_path:
                image_utils.get_cached_mini_image(producto.imagen_path)
        cached_load_time = time.time() - start_time
        
        print(f"   ⏱️  Premier chargement: {first_load_time:.4f}s")
        print(f"   ⚡ Chargement depuis cache: {cached_load_time:.4f}s")
        print(f"   🚀 Amélioration: {(first_load_time/cached_load_time):.1f}x plus rapide")
        
        # Étape 8: Avantages de la fonctionnalité
        print("\n8️⃣ Avantages des mini images dans les factures")
        print("   ✅ **Identification visuelle** : Reconnaissance rapide des produits")
        print("   ✅ **Interface moderne** : Aspect professionnel et attrayant")
        print("   ✅ **Réduction d'erreurs** : Moins de confusion entre produits")
        print("   ✅ **Performance optimisée** : Cache intelligent des images")
        print("   ✅ **Compatibilité** : Support de tous formats d'image")
        print("   ✅ **Fallback élégant** : Placeholder pour produits sans image")
        
        # Nettoyage
        print("\n🧹 Nettoyage...")
        try:
            for _, image_path in images_created:
                if os.path.exists(image_path):
                    os.remove(image_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            print("   ✅ Images temporaires supprimées")
        except Exception as e:
            print(f"   ⚠️  Erreur lors du nettoyage: {e}")
        
        print(f"\n🎉 === DÉMONSTRATION TERMINÉE ===")
        print("💡 Les mini images sont maintenant intégrées dans l'interface de facturation!")
        print("🎯 Avantages: Identification visuelle, interface moderne, performance optimisée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_mini_images_facturas()
    sys.exit(0 if success else 1)
