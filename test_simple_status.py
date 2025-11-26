#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple du système de statuts
"""

import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🧪 Test simple du système de statuts de factures")
    print("=" * 50)
    
    # Test d'import
    print("1. Test des imports...")
    from database.database import db
    print("✅ Import database.db réussi")
    
    from utils.invoice_status_manager import invoice_status_manager
    print("✅ Import invoice_status_manager réussi")
    
    # Test de la base de données
    print("\n2. Test de la base de données...")
    
    # Initialiser la base de données
    db.init_database()
    print("✅ Base de données initialisée")
    
    # Test des statuts
    print("\n3. Test des statuts...")
    statuses = invoice_status_manager.get_all_statuses()
    print(f"✅ {len(statuses)} statuts trouvés")
    
    for status in statuses:
        print(f"   - {status['nombre']}: {status['descripcion']} (Modifiable: {status['permite_modificacion']})")
    
    # Test de permissions
    print("\n4. Test des permissions...")
    can_modify_borrador = invoice_status_manager.can_modify_invoice('Borrador')
    print(f"✅ Borrador modifiable: {can_modify_borrador}")
    
    can_modify_pagada = invoice_status_manager.can_modify_invoice('Pagada')
    print(f"✅ Pagada modifiable: {can_modify_pagada}")
    
    print("\n🎉 Test terminé avec succès!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
