#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire des statuts de factures
"""

from database.database import db
from utils.logger import get_logger

class InvoiceStatusManager:
    """Gestionnaire pour les statuts de factures"""
    
    def __init__(self):
        self.logger = get_logger("invoice_status_manager")
    
    def get_all_statuses(self):
        """Obtient tous les statuts actifs"""
        return db.get_all_invoice_statuses()
    
    def get_status_by_name(self, name):
        """Obtient un statut par nom"""
        return db.get_invoice_status_by_name(name)
    
    def can_modify_invoice(self, status_name):
        """Vérifie si une facture avec ce statut peut être modifiée"""
        status = self.get_status_by_name(status_name)
        if status:
            return status['permite_modificacion']
        return False  # Par défaut, ne pas permettre la modification
    
    def get_status_color(self, status_name):
        """Obtient la couleur d'un statut"""
        status = self.get_status_by_name(status_name)
        if status:
            return status['color']
        return '#6c757d'  # Couleur par défaut (gris)
    
    def get_modifiable_statuses(self):
        """Obtient tous les statuts qui permettent la modification"""
        all_statuses = self.get_all_statuses()
        return [status for status in all_statuses if status['permite_modificacion']]

    def get_non_modifiable_statuses(self):
        """Obtient tous les statuts qui ne permettent pas la modification"""
        all_statuses = self.get_all_statuses()
        return [status for status in all_statuses if not status['permite_modificacion']]
    
    def save_status(self, status_data):
        """Sauvegarde un statut"""
        try:
            # Validation des données
            if not status_data.get('nombre'):
                raise ValueError("Le nom du statut est obligatoire")
            
            if not status_data.get('descripcion'):
                status_data['descripcion'] = status_data['nombre']
            
            if not status_data.get('color'):
                status_data['color'] = '#007bff'
            
            if not status_data.get('orden'):
                # Obtenir le prochain ordre disponible
                all_statuses = self.get_all_statuses()
                max_orden = max([s['orden'] for s in all_statuses], default=0)
                status_data['orden'] = max_orden + 1
            
            # Assurer que permite_modificacion est un booléen
            status_data['permite_modificacion'] = bool(status_data.get('permite_modificacion', False))
            
            success = db.save_invoice_status(status_data)
            
            if success:
                self.logger.info(f"Statut sauvegardé: {status_data['nombre']}")
            else:
                self.logger.error(f"Erreur lors de la sauvegarde du statut: {status_data['nombre']}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du statut: {e}")
            return False
    
    def delete_status(self, status_id):
        """Supprime un statut (le marque comme inactif)"""
        try:
            success = db.delete_invoice_status(status_id)
            
            if success:
                self.logger.info(f"Statut supprimé: ID {status_id}")
            else:
                self.logger.error(f"Erreur lors de la suppression du statut: ID {status_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du statut: {e}")
            return False
    
    def get_default_status(self):
        """Obtient le statut par défaut (Borrador)"""
        return self.get_status_by_name('Borrador')
    
    def get_status_names(self):
        """Obtient la liste des noms de statuts"""
        statuses = self.get_all_statuses()
        return [status['nombre'] for status in statuses]
    
    def validate_status_transition(self, from_status, to_status):
        """Valide si une transition de statut est autorisée"""
        # Règles de transition basiques
        # Peut être étendu selon les besoins métier
        
        if from_status == to_status:
            return True  # Pas de changement
        
        # Borrador peut aller vers n'importe quel statut
        if from_status == 'Borrador':
            return True
        
        # Les statuts finaux (Pagada, Anulada, Cancelada) ne peuvent pas changer
        final_statuses = ['Pagada', 'Anulada', 'Cancelada']
        if from_status in final_statuses:
            return False
        
        # Autres transitions autorisées par défaut
        return True

# Instance globale
invoice_status_manager = InvoiceStatusManager()
