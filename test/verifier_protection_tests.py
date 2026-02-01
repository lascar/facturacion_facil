#!/usr/bin/env python3
"""
Vérifie que les tests ne peuvent pas polluer la base de données de production
Ce script doit être exécuté AVANT tout test via run_organized_tests.sh
"""
import os
import sys
import sqlite3

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def error(msg):
    print(f"{RED}   ❌ {msg}{NC}")
    return False

def success(msg):
    print(f"{GREEN}   ✅ {msg}{NC}")
    return True

def warning(msg):
    print(f"{YELLOW}   ⚠️  {msg}{NC}")

def info(msg):
    print(f"{BLUE}   ℹ️  {msg}{NC}")

def verifier_protection():
    print("="*60)
    print("🛡️  VÉRIFICATION PROTECTION BASE DE DONNÉES")
    print("="*60)
    print()
    
    erreurs = []
    warnings = []
    
    # 1. Vérifier que PYTEST_RUNNING est utilisé dans database.py
    print("1. Vérification de PYTEST_RUNNING dans database.py...")
    try:
        with open('database/database.py', 'r') as f:
            content = f.read()
            if 'PYTEST_RUNNING' in content and 'TEST_DATABASE_PATH' in content:
                success("Protection PYTEST_RUNNING + TEST_DATABASE_PATH présente")
            else:
                erreurs.append("Protection DB manquante")
                error("Protection PYTEST_RUNNING ou TEST_DATABASE_PATH MANQUANTE!")
    except Exception as e:
        erreurs.append(f"Erreur lecture database.py: {e}")
        error(f"Erreur: {e}")
    
    # 2. Vérifier les fixtures de test
    print("\n2. Vérification des fixtures de test isolées...")
    try:
        if os.path.exists('test/unit/conftest.py'):
            with open('test/unit/conftest.py', 'r') as f:
                content = f.read()
                if 'tempfile' in content and 'unit_db' in content:
                    success("Fixtures unit_db utilisent tempfile")
                else:
                    warnings.append("Vérifier les fixtures unit_db")
                    warning("Vérifier que unit_db utilise bien tempfile")
        else:
            warnings.append("test/unit/conftest.py manquant")
            warning("test/unit/conftest.py non trouvé")
    except Exception as e:
        warnings.append(f"Erreur vérification fixtures: {e}")
        warning(f"Erreur: {e}")
    
    # 3. Vérifier isolation config.json dans les tests behaviour
    print("\n3. Vérification isolation config.json...")
    test_files = [
        'test/behaviour/test_organizacion_forma_pago_behaviour.py',
        'test/behaviour/test_organizacion_config_json_only_behaviour.py',
        'test/behaviour/test_forma_pago_pdf_visibility_behaviour.py'
    ]
    
    for fichier in test_files:
        if os.path.exists(fichier):
            try:
                with open(fichier, 'r') as f:
                    content = f.read()
                    if 'tmp_path' in content and 'config_file' in content:
                        success(f"{os.path.basename(fichier)} utilise tmp_path")
                    else:
                        warnings.append(f"{fichier} doit utiliser tmp_path")
                        warning(f"{os.path.basename(fichier)} - vérifier isolation")
            except Exception as e:
                warnings.append(f"Erreur lecture {fichier}")
                warning(f"Erreur {fichier}: {e}")
    
    # 4. Vérification CRITIQUE: Données de test dans la DB de production
    print("\n4. Vérification CRITIQUE: Pas de données de test en production...")
    try:
        db_path = 'base_de_datos/facturacion.db'
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Compter les données de test
            patterns_test = ['%Test%', '%test%', '%TEST%', '%Cliente Test%', '%Producto Test%']
            
            test_data_found = False
            
            # Produits
            cursor.execute("SELECT COUNT(*) FROM productos WHERE nombre LIKE ? OR nombre LIKE ?", 
                          ('%Test%', '%test%'))
            test_prod = cursor.fetchone()[0]
            if test_prod > 0:
                test_data_found = True
                erreurs.append(f"{test_prod} produits de test trouvés")
                error(f"{test_prod} produits de test trouvés dans la DB!")
            
            # Factures
            cursor.execute("SELECT COUNT(*) FROM facturas WHERE numero_factura LIKE ? OR numero_factura LIKE ? OR nombre_cliente LIKE ?",
                          ('%TEST%', '%TEST%', '%Test%'))
            test_fact = cursor.fetchone()[0]
            if test_fact > 0:
                test_data_found = True
                erreurs.append(f"{test_fact} factures de test trouvées")
                error(f"{test_fact} factures de test trouvées dans la DB!")
            
            # Clients
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE nombre LIKE ? OR nombre LIKE ?",
                          ('%Test%', '%test%'))
            test_cli = cursor.fetchone()[0]
            if test_cli > 0:
                test_data_found = True
                erreurs.append(f"{test_cli} clients de test trouvés")
                error(f"{test_cli} clients de test trouvés dans la DB!")
            
            # Organisation
            cursor.execute("SELECT nombre FROM organizacion WHERE id = 1")
            org = cursor.fetchone()
            if org and org[0] and ('test' in org[0].lower() or org[0] == ''):
                if org[0] == '':
                    info("Organisation vide (OK pour nouveau setup)")
                else:
                    test_data_found = True
                    erreurs.append(f"Organisation '{org[0]}' semble être un test")
                    error(f"Organisation '{org[0]}' semble être des données de test!")
            
            conn.close()
            
            if not test_data_found:
                success("Aucune donnée de test détectée dans la DB")
        else:
            warning("Base de données inexistante (premier lancement?)")
    except Exception as e:
        erreurs.append(f"Erreur vérification DB: {e}")
        error(f"Erreur lors de la vérification: {e}")
    
    # 5. Vérification CRITIQUE: config.json ne doit pas contenir de données de test
    print("\n5. Vérification CRITIQUE: config.json ne contient pas de données de test...")
    try:
        config_path = 'config/config.json'
        if os.path.exists(config_path):
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            org = config.get('organizacion_defaults', {})
            config_test_found = False
            
            if org:
                # Vérifier le nom
                nombre = org.get('nombre', '')
                if nombre and ('test' in nombre.lower() or 'empresa' in nombre.lower() or 'test' in nombre.lower()):
                    config_test_found = True
                    erreurs.append(f"config.json: nom '{nombre}' semble être un test")
                    error(f"config.json contient un nom de test: '{nombre}'!")
                
                # Vérifier l'email
                email = org.get('email', '')
                if email and ('test' in email.lower() or 'empresa.com' in email.lower() or 'example.com' in email.lower()):
                    config_test_found = True
                    erreurs.append(f"config.json: email '{email}' semble être un test")
                    error(f"config.json contient un email de test: '{email}'!")
                
                # Vérifier CIF
                cif = org.get('cif', '')
                if cif and cif in ['B12345678', '12345678', '']:
                    pass  # CIF vide ou générique OK si autres champs vides
                
                # Si des champs sont remplis avec des données suspectes
                forma_pago = org.get('forma_pago', '')
                if forma_pago and 'ES00 0000' in forma_pago:
                    # C'est la valeur par défaut, OK
                    pass
                
                if not config_test_found:
                    if nombre and email:
                        success("config.json contient des données (pas de test détecté)")
                    else:
                        info("config.json partiellement vide (OK pour nouveau setup)")
            else:
                info("config.json sans organizacion_defaults (OK pour nouveau setup)")
        else:
            info("config.json inexistant (OK pour premier lancement)")
    except Exception as e:
        erreurs.append(f"Erreur vérification config.json: {e}")
        error(f"Erreur config.json: {e}")
    
    # Résumé
    print()
    print("="*60)
    
    if erreurs:
        print(f"{RED}❌ ERREURS CRITIQUES DÉTECTÉES:{NC}")
        for e in erreurs:
            print(f"   • {e}")
        print()
        print(f"{YELLOW}🔧 Solutions:{NC}")
        print("   1. Nettoyer la base: python3 -c \"import sqlite3; conn=sqlite3.connect('base_de_datos/facturacion.db'); cursor=conn.cursor(); cursor.execute('DELETE FROM productos WHERE nom LIKE \"%Test%\"'); conn.commit(); conn.close()\"")
        print("   2. Vérifier database/database.py utilise bien PYTEST_RUNNING")
        print("   3. Vérifier les fixtures dans test/conftest.py")
        print()
        return 1
    elif warnings:
        print(f"{YELLOW}⚠️  AVERTISSEMENTS (non bloquants):{NC}")
        for w in warnings:
            print(f"   • {w}")
        print()
        success("Protection OK malgré les avertissements")
        return 0
    else:
        print(f"{GREEN}✅ PROTECTION OK - Les tests sont correctement isolés{NC}")
        return 0

if __name__ == '__main__':
    sys.exit(verifier_protection())
