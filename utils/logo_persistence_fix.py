#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaire de correction de la persistance du logo
"""

import os
import sys
from PIL import Image

# Ajouter le répertoire racine au path si nécessaire
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Organizacion
from utils.logo_manager import LogoManager
# from utils.logger import log_info, log_warning, log_error


class LogoPersistenceFix:
    """Utilitaire pour corriger les problèmes de persistance du logo"""
    
    def __init__(self):
        self.logo_manager = LogoManager()
    
    def diagnose_logo_issues(self):
        """Diagnostiquer les problèmes de logo"""
        log_info("🔍 Diagnostic des problèmes de logo")
        
        issues = []
        
        # Vérifier l'organisation
        org = Organizacion.get()
        if not org or not org.nombre:
            issues.append("no_organization")
            self.logger.warning("Aucune organisation configurée")
            return issues
        
        self.logger.info(f"Organisation trouvée: {org.nombre}")
        
        # Vérifier le logo configuré
        if not org.logo_path:
            issues.append("no_logo_configured")
            self.logger.warning("Aucun logo configuré")
            return issues
        
        self.logger.info(f"Logo configuré: {org.logo_path}")
        
        # Vérifier l'existence du fichier
        if not os.path.exists(org.logo_path):
            issues.append("logo_file_missing")
            self.logger.error(f"Fichier logo manquant: {org.logo_path}")
            return issues
        
        # Vérifier le répertoire permanent
        if self.logo_manager.logo_directory not in org.logo_path:
            issues.append("logo_not_permanent")
            self.logger.warning(f"Logo pas dans répertoire permanent: {org.logo_path}")
        
        # Vérifier la chargeabilité
        try:
            with Image.open(org.logo_path) as img:
                self.logger.info(f"Logo chargeable: {img.size}")
        except Exception as e:
            issues.append("logo_not_loadable")
            self.logger.error(f"Logo non chargeable: {e}")
        
        if not issues:
            self.logger.info("✅ Aucun problème de logo détecté")
        
        return issues
    
    def fix_logo_persistence(self):
        """Corriger les problèmes de persistance du logo"""
        self.logger.info("🔧 Correction des problèmes de persistance du logo")
        
        issues = self.diagnose_logo_issues()
        
        if "no_organization" in issues:
            self.logger.info("Création d'une organisation de démonstration...")
            return self._create_demo_organization()
        
        if "no_logo_configured" in issues:
            self.logger.info("Aucun logo à corriger")
            return True
        
        if "logo_file_missing" in issues:
            self.logger.error("Fichier logo manquant - impossible de corriger automatiquement")
            self.logger.info("Solution: sélectionner un nouveau logo dans l'interface")
            return False
        
        if "logo_not_permanent" in issues:
            self.logger.info("Correction: déplacement vers répertoire permanent...")
            return self._move_logo_to_permanent()
        
        if "logo_not_loadable" in issues:
            self.logger.error("Logo corrompu - impossible de corriger automatiquement")
            self.logger.info("Solution: sélectionner un nouveau logo dans l'interface")
            return False
        
        self.logger.info("✅ Aucune correction nécessaire")
        return True
    
    def _create_demo_organization(self):
        """Créer une organisation de démonstration avec logo"""
        try:
            # Créer un logo de démonstration
            import tempfile
            temp_dir = tempfile.mkdtemp()
            temp_logo = os.path.join(temp_dir, "demo_logo.png")
            
            # Créer une image simple
            img = Image.new('RGB', (200, 100), color='#2E86AB')
            img.save(temp_logo)
            
            # Copier vers répertoire permanent
            permanent_logo = self.logo_manager.save_logo(temp_logo, "Empresa Demo")
            
            if permanent_logo:
                # Créer organisation
                org = Organizacion(
                    nombre="Empresa Demo",
                    direccion="123 Calle Demo, Madrid, España",
                    telefono="+34 91 123 45 67",
                    email="demo@empresa.com",
                    cif="B12345678",
                    logo_path=permanent_logo
                )
                org.save()
                
                self.logger.info(f"✅ Organisation de démonstration créée: {org.nombre}")
                self.logger.info(f"✅ Logo configuré: {permanent_logo}")
                
                # Nettoyer
                os.remove(temp_logo)
                os.rmdir(temp_dir)
                
                return True
            else:
                self.logger.error("Échec création logo permanent")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur création organisation de démonstration: {e}")
            return False
    
    def _move_logo_to_permanent(self):
        """Déplacer le logo vers le répertoire permanent"""
        try:
            org = Organizacion.get()
            if not org or not org.logo_path:
                return False
            
            # Copier vers répertoire permanent
            permanent_logo = self.logo_manager.save_logo(org.logo_path, org.nombre)
            
            if permanent_logo:
                # Mettre à jour l'organisation
                org.logo_path = permanent_logo
                org.save()
                
                self.logger.info(f"✅ Logo déplacé vers: {permanent_logo}")
                return True
            else:
                self.logger.error("Échec déplacement logo")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur déplacement logo: {e}")
            return False
    
    def verify_logo_persistence(self):
        """Vérifier que le logo persiste correctement"""
        self.logger.info("🔍 Vérification de la persistance du logo")
        
        # Test 1: Vérifier l'état actuel
        issues = self.diagnose_logo_issues()
        if issues:
            self.logger.error(f"Problèmes détectés: {issues}")
            return False
        
        # Test 2: Simuler redémarrage (nouvelle instance)
        org = Organizacion.get()
        if not org or not org.logo_path:
            self.logger.error("Aucune organisation ou logo après redémarrage simulé")
            return False
        
        # Test 3: Vérifier l'existence du fichier
        if not os.path.exists(org.logo_path):
            self.logger.error(f"Fichier logo manquant après redémarrage: {org.logo_path}")
            return False
        
        # Test 4: Vérifier la chargeabilité
        try:
            with Image.open(org.logo_path) as img:
                self.logger.info(f"✅ Logo persistant et chargeable: {img.size}")
                return True
        except Exception as e:
            self.logger.error(f"Logo non chargeable après redémarrage: {e}")
            return False
    
    def run_complete_fix(self):
        """Exécuter une correction complète"""
        self.logger.info("🚀 Correction complète de la persistance du logo")
        
        # Étape 1: Diagnostic
        self.logger.info("Étape 1: Diagnostic...")
        issues = self.diagnose_logo_issues()
        
        # Étape 2: Correction
        self.logger.info("Étape 2: Correction...")
        fix_success = self.fix_logo_persistence()
        
        if not fix_success:
            self.logger.error("❌ Échec de la correction")
            return False
        
        # Étape 3: Vérification
        self.logger.info("Étape 3: Vérification...")
        verify_success = self.verify_logo_persistence()
        
        if verify_success:
            self.logger.info("🎉 Correction complète réussie!")
            self.logger.info("Le logo devrait maintenant persister entre les redémarrages")
            return True
        else:
            self.logger.error("❌ Échec de la vérification")
            return False


def main():
    """Fonction principale pour exécution en ligne de commande"""
    print("🔧 Utilitaire de correction de la persistance du logo")
    print("=" * 55)
    
    fixer = LogoPersistenceFix()
    
    # Exécuter la correction complète
    success = fixer.run_complete_fix()
    
    if success:
        print("\n✅ Correction terminée avec succès!")
        print("Le logo de l'entreprise devrait maintenant persister entre les redémarrages.")
    else:
        print("\n❌ Correction échouée!")
        print("Veuillez vérifier les logs pour plus de détails.")
        print("Solution manuelle: configurer un nouveau logo dans l'interface d'organisation.")
    
    return success


if __name__ == "__main__":
    main()
