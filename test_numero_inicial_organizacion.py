#!/usr/bin/env python3
"""
Test du numéro initial de factura depuis l'organisation
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(__file__))

def test_config_numero_inicial():
    """Tester la lecture du numéro initial depuis la configuration"""
    print("🧪 TEST: Configuration Numéro Initial")
    print("=" * 40)
    
    try:
        from config.config import app_config
        
        # Lire le numéro initial configuré
        numero_inicial = app_config.get_factura_numero_inicial()
        
        print(f"📋 Numéro initial configuré: {numero_inicial}")
        print(f"📋 Type: {type(numero_inicial)}")
        
        # Vérifier que ce n'est pas la valeur par défaut
        if numero_inicial != 1:
            print("✅ Configuration personnalisée détectée")
            return True, numero_inicial
        else:
            print("⚠️  Utilise la valeur par défaut")
            return False, numero_inicial
            
    except Exception as e:
        print(f"❌ Erreur lecture configuration: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_factura_numbering_service():
    """Tester le service de numérotation"""
    print("\n🧪 TEST: Service de Numérotation")
    print("=" * 35)
    
    try:
        from utils.factura_numbering import FacturaNumberingService
        
        # Créer le service
        service = FacturaNumberingService()
        
        # Obtenir le prochain numéro
        proximo_numero = service.get_next_numero_factura()
        
        print(f"📋 Prochain numéro généré: {proximo_numero}")
        
        # Vérifier que ce n'est pas un format par défaut simple
        if "FAC-" not in proximo_numero and "F-" not in proximo_numero:
            print("✅ Format personnalisé utilisé")
            return True, proximo_numero
        else:
            print("⚠️  Format par défaut utilisé")
            return False, proximo_numero
            
    except Exception as e:
        print(f"❌ Erreur service numérotation: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_database_organizacion():
    """Tester la lecture directe de la base de données"""
    print("\n🧪 TEST: Base de Données Organisation")
    print("=" * 40)
    
    try:
        import sqlite3
        
        # Lire directement depuis la base de données
        conn = sqlite3.connect("base_de_datos/facturacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT numero_factura_inicial FROM organizacion WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            numero_db = result[0]
            print(f"📋 Numéro en base de données: {numero_db}")
            print(f"📋 Type: {type(numero_db)}")
            return True, numero_db
        else:
            print("⚠️  Aucune configuration trouvée en base")
            return False, None
            
    except Exception as e:
        print(f"❌ Erreur lecture base de données: {e}")
        return False, None

def test_integration_complete():
    """Test d'intégration complète"""
    print("\n🧪 TEST: Intégration Complète")
    print("=" * 30)
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.facturas_pyqt5 import CrearFacturaDialog
        
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        # Créer le dialog
        dialog = CrearFacturaDialog()
        
        # Générer un numéro de facture
        numero_generado = dialog.generate_invoice_number()
        
        print(f"📋 Numéro généré par dialog: {numero_generado}")
        
        # Vérifier que le format correspond à la configuration
        if "2025-wp" in numero_generado:
            print("✅ Format de l'organisation utilisé")
            return True, numero_generado
        else:
            print("⚠️  Format différent de l'organisation")
            return False, numero_generado
            
    except Exception as e:
        print(f"❌ Erreur test intégration: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    """Fonction principale"""
    print("🎯 TEST COMPLET: Numéro Initial Organisation")
    print("=" * 50)
    
    print("🎯 OBJECTIF:")
    print("   Vérifier que le numéro initial configuré dans l'organisation")
    print("   est correctement utilisé par la génération de nouvelles factures")
    print()
    
    # Exécuter les tests
    test1_success, numero_config = test_config_numero_inicial()
    test2_success, numero_service = test_factura_numbering_service()
    test3_success, numero_db = test_database_organizacion()
    test4_success, numero_dialog = test_integration_complete()
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES RÉSULTATS:")
    print(f"   📋 Configuration: {numero_config}")
    print(f"   📋 Service: {numero_service}")
    print(f"   📋 Base de données: {numero_db}")
    print(f"   📋 Dialog: {numero_dialog}")
    
    if all([test1_success, test2_success, test3_success, test4_success]):
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n✅ RÉSULTAT:")
        print("   🎯 Configuration organisation: Correctement lue")
        print("   🎯 Service numérotation: Utilise la configuration")
        print("   🎯 Dialog création: Génère le bon format")
        print("   ✅ Numéro initial organisation utilisé correctement")
        
        print("\n🚀 PROCHAINE ÉTAPE:")
        print("   Testez manuellement:")
        print("   python main.py → Gestión de Facturas → Nueva Factura")
        print(f"   Le numéro devrait commencer par: {numero_db}")
        
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("   Le numéro initial de l'organisation n'est pas utilisé")
        
        if not test1_success:
            print("   ❌ Configuration: Problème de lecture")
        if not test2_success:
            print("   ❌ Service: N'utilise pas la configuration")
        if not test3_success:
            print("   ❌ Base de données: Problème d'accès")
        if not test4_success:
            print("   ❌ Dialog: N'utilise pas le service correct")
    
    print("=" * 50)
    return all([test1_success, test2_success, test3_success, test4_success])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
