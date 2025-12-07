#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier que l'interface sauvegarde bien les catégories
"""

import sys
import sqlite3
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.productos_pyqt5 import ProductosPyQt5Window

def test_interface_categoria():
    """Test de l'interface pour la sauvegarde des catégories"""
    print("🧪 Test de l'interface de produits avec catégorie...")
    
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre de produits
        window = ProductosPyQt5Window()
        
        # Simuler la saisie d'un produit avec catégorie
        window.nombre_edit.setText("Producto Test Interface")
        window.referencia_edit.setText("TEST-INT-001")
        window.precio_edit.setValue(29.99)
        window.iva_edit.setValue(21.0)
        window.stock_edit.setValue(25)
        window.categoria_combo.setCurrentText("Categoria Interface Test")
        window.descripcion_edit.setPlainText("Producto para test de interface")
        
        print("   ✅ Données saisies dans l'interface")
        
        # Sauvegarder le produit
        window.save_producto()
        
        # Vérifier que le produit a été créé avec la catégorie
        if window.selected_producto_id:
            print(f"   ✅ Produit créé avec ID: {window.selected_producto_id}")
            
            # Vérifier directement dans la base de données
            conn = sqlite3.connect("facturacion.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nombre, categoria, referencia 
                FROM productos 
                WHERE id = ?
            """, (window.selected_producto_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                nombre, categoria, referencia = result
                print(f"   ✅ Produit trouvé: '{nombre}'")
                print(f"   ✅ Référence: '{referencia}'")
                
                if categoria == "Categoria Interface Test":
                    print(f"   ✅ Catégorie correctement sauvegardée: '{categoria}'")
                    
                    # Nettoyer le produit de test
                    conn = sqlite3.connect("facturacion.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM productos WHERE id = ?", (window.selected_producto_id,))
                    conn.commit()
                    conn.close()
                    print("   🧹 Produit de test nettoyé")
                    
                    return True
                else:
                    print(f"   ❌ Catégorie incorrecte: '{categoria}' (attendu: 'Categoria Interface Test')")
                    return False
            else:
                print("   ❌ Produit non trouvé dans la base de données")
                return False
        else:
            print("   ❌ Aucun ID de produit retourné")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    finally:
        app.quit()

def test_load_categories():
    """Test du chargement des catégories"""
    print("🧪 Test du chargement des catégories...")
    
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre de produits
        window = ProductosPyQt5Window()
        
        # Vérifier que les catégories sont chargées
        combo_count = window.categoria_combo.count()
        print(f"   ✅ {combo_count} éléments dans le combo catégorie")
        
        # Afficher les catégories disponibles
        categories = []
        for i in range(combo_count):
            text = window.categoria_combo.itemText(i)
            if text.strip():  # Ignorer l'option vide
                categories.append(text)
        
        print(f"   ✅ Catégories disponibles: {categories}")
        
        return combo_count > 0
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    finally:
        app.quit()

def test_categoria_vide():
    """Test avec catégorie vide"""
    print("🧪 Test avec catégorie vide...")
    
    app = QApplication(sys.argv)
    
    try:
        # Créer la fenêtre de produits
        window = ProductosPyQt5Window()
        
        # Simuler la saisie d'un produit sans catégorie
        window.nombre_edit.setText("Producto Sin Categoria Interface")
        window.referencia_edit.setText("TEST-NO-CAT-INT-001")
        window.precio_edit.setValue(19.99)
        window.iva_edit.setValue(21.0)
        window.stock_edit.setValue(15)
        window.categoria_combo.setCurrentText("")  # Catégorie vide
        window.descripcion_edit.setPlainText("Producto sin categoria")
        
        print("   ✅ Données saisies (catégorie vide)")
        
        # Sauvegarder le produit
        window.save_producto()
        
        # Vérifier que le produit a été créé sans catégorie
        if window.selected_producto_id:
            print(f"   ✅ Produit créé avec ID: {window.selected_producto_id}")
            
            # Vérifier directement dans la base de données
            conn = sqlite3.connect("facturacion.db")
            cursor = conn.cursor()
            cursor.execute("SELECT categoria FROM productos WHERE id = ?", (window.selected_producto_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result and result[0] is None:
                print("   ✅ Catégorie vide correctement sauvegardée (NULL)")
                
                # Nettoyer le produit de test
                conn = sqlite3.connect("facturacion.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id = ?", (window.selected_producto_id,))
                conn.commit()
                conn.close()
                print("   🧹 Produit de test nettoyé")
                
                return True
            else:
                print(f"   ❌ Catégorie vide mal gérée: {result}")
                return False
        else:
            print("   ❌ Aucun ID de produit retourné")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    finally:
        app.quit()

def main():
    """Fonction principale de test"""
    print("🔍 TEST DE L'INTERFACE POUR LES CATÉGORIES DE PRODUITS")
    print("=" * 55)
    
    tests = [
        ("Chargement catégories", test_load_categories),
        ("Sauvegarde avec catégorie", test_interface_categoria),
        ("Sauvegarde sans catégorie", test_categoria_vide)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: RÉUSSI")
            else:
                print(f"❌ {test_name}: ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
    
    # Résumé
    print(f"\n📊 RÉSUMÉ DES TESTS")
    print("=" * 20)
    print(f"✅ Tests réussis: {passed}/{total}")
    print(f"❌ Tests échoués: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS ONT RÉUSSI !")
        print("   L'interface sauvegarde correctement les catégories.")
        return True
    else:
        print(f"\n⚠️ {total - passed} test(s) ont échoué.")
        print("   Il y a encore des problèmes avec l'interface.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
