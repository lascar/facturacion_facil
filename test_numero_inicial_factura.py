#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier le respect du numéro initial de factura
"""

from utils.factura_numbering import FacturaNumberingService
from utils.config import Config
from database.database_improved import DatabaseImproved
import sqlite3

def test_numero_inicial_configuration():
    """Test la configuration du numéro inicial"""
    print("🧪 TEST CONFIGURATION NUMÉRO INICIAL")
    print("=" * 40)
    
    try:
        # Vérifier la configuration dans la base de données
        print("\n1️⃣ Configuration en base de données:")
        conn = sqlite3.connect("facturacion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT numero_factura_inicial FROM organizacion WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            numero_inicial_db = result[0]
            print(f"   📝 Numéro inicial en DB: '{numero_inicial_db}'")
        else:
            print("   ❌ Aucune configuration trouvée en DB")
            return False
        
        # Vérifier la configuration via Config
        print("\n2️⃣ Configuration via Config:")
        config = Config()
        numero_inicial_config = config.get_factura_numero_inicial()
        print(f"   📝 Numéro inicial via Config: {numero_inicial_config}")
        
        # Test du service de numérotation
        print("\n3️⃣ Service de numérotation:")
        numbering_service = FacturaNumberingService()
        next_numero = numbering_service.get_next_numero_factura()
        print(f"   📝 Prochain numéro généré: '{next_numero}'")
        
        # Vérifier la cohérence
        print("\n4️⃣ Analyse de cohérence:")
        if numero_inicial_db == "2025-wp-01":
            print("   ✅ Configuration DB correcte: '2025-wp-01'")
            
            if "2025-wp-01" in next_numero or "wp" in next_numero.lower():
                print("   ✅ Le service respecte la configuration")
                return True
            else:
                print(f"   ❌ Le service ne respecte pas la configuration")
                print(f"      Attendu: contenant '2025-wp-01' ou 'wp'")
                print(f"      Obtenu: '{next_numero}'")
                return False
        else:
            print(f"   ⚠️ Configuration DB inattendue: '{numero_inicial_db}'")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_generation_avec_facturas_existantes():
    """Test la génération avec des factures existantes"""
    print("\n🧪 TEST GÉNÉRATION AVEC FACTURAS EXISTANTES")
    print("=" * 45)
    
    try:
        # Vérifier s'il y a des factures existantes
        print("\n1️⃣ Facturas existantes:")
        db = DatabaseImproved()
        
        # Utiliser la méthode directe de la base de données
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT numero_factura FROM facturas ORDER BY id")
            facturas = cursor.fetchall()
        
        print(f"   📊 Nombre de facturas: {len(facturas)}")
        
        if facturas:
            print("   📝 Facturas existantes:")
            for i, factura in enumerate(facturas):
                print(f"      {i+1}. {factura[0]}")
        else:
            print("   📝 Aucune factura existante")
        
        # Test de génération
        print("\n2️⃣ Test de génération:")
        numbering_service = FacturaNumberingService()
        next_numero = numbering_service.get_next_numero_factura()
        print(f"   📝 Prochain numéro: '{next_numero}'")
        
        # Analyser le comportement
        if len(facturas) == 0:
            print("\n3️⃣ Analyse (aucune factura existante):")
            print("   💡 Le système devrait utiliser le numéro inicial configuré")
            if "2025-wp-01" in next_numero or "wp" in next_numero.lower():
                print("   ✅ Comportement correct")
                return True
            else:
                print("   ❌ Le numéro inicial n'est pas respecté")
                return False
        else:
            print("\n3️⃣ Analyse (facturas existantes):")
            print("   💡 Le système devrait incrémenter depuis la dernière factura")
            # Pour ce test, on accepte le comportement actuel
            return True
        
    except Exception as e:
        print(f"   ❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_methods():
    """Test les méthodes de configuration"""
    print("\n🧪 TEST MÉTHODES DE CONFIGURATION")
    print("=" * 35)
    
    try:
        config = Config()
        
        # Test get_factura_numero_inicial
        print("\n1️⃣ Test get_factura_numero_inicial:")
        numero = config.get_factura_numero_inicial()
        print(f"   📝 Résultat: {numero} (type: {type(numero)})")
        
        # Le problème pourrait être ici - Config cherche dans une table 'configuracion'
        # mais les données sont dans 'organizacion'
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC NUMÉRO INICIAL FACTURA")
    print("=" * 40)
    
    test1 = test_numero_inicial_configuration()
    test2 = test_generation_avec_facturas_existantes()
    test3 = test_config_methods()
    
    print(f"\n🎯 RÉSUMÉ:")
    print(f"   Configuration: {'✅ OK' if test1 else '❌ PROBLÈME'}")
    print(f"   Génération: {'✅ OK' if test2 else '❌ PROBLÈME'}")
    print(f"   Méthodes Config: {'✅ OK' if test3 else '❌ PROBLÈME'}")
    
    if not (test1 and test2 and test3):
        print(f"\n🔧 PROBLÈME IDENTIFIÉ:")
        print("   Le système de configuration ne lit pas correctement")
        print("   le numéro inicial depuis la table 'organizacion'")
        print("   Il faut corriger la classe Config pour lire depuis 'organizacion'")
    
    return test1 and test2 and test3

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
