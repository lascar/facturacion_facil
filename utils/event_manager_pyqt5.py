#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire d'événements centralisé pour PyQt5
Synchronise les données entre les différentes fenêtres
"""

from PyQt5.QtCore import QObject, pyqtSignal
from utils.logger import get_logger

class EventManagerPyQt5(QObject):
    """Gestionnaire d'événements centralisé pour synchroniser les données entre fenêtres PyQt5"""
    
    # Signaux pour les différents types d'événements
    product_created = pyqtSignal(dict)      # Nouveau produit créé
    product_updated = pyqtSignal(dict)      # Produit modifié
    product_deleted = pyqtSignal(int)       # Produit supprimé (ID)
    
    stock_updated = pyqtSignal(int, int)    # Stock modifié (product_id, new_stock)
    stock_adjusted = pyqtSignal(int, int, int)  # Stock ajusté (product_id, old_stock, new_stock)
    
    invoice_created = pyqtSignal(dict)      # Nouvelle facture créée
    invoice_updated = pyqtSignal(dict)      # Facture modifiée
    
    client_created = pyqtSignal(dict)       # Nouveau client créé
    client_updated = pyqtSignal(dict)       # Client modifié
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger("EventManagerPyQt5")
        self.logger.info("Gestionnaire d'événements PyQt5 initialisé")
    
    def emit_product_created(self, product_data):
        """Émet un signal de création de produit"""
        self.logger.debug(f"Émission signal product_created: {product_data.get('nombre', 'N/A')}")
        self.product_created.emit(product_data)
    
    def emit_product_updated(self, product_data):
        """Émet un signal de modification de produit"""
        self.logger.debug(f"Émission signal product_updated: {product_data.get('nombre', 'N/A')}")
        self.product_updated.emit(product_data)
    
    def emit_product_deleted(self, product_id):
        """Émet un signal de suppression de produit"""
        self.logger.debug(f"Émission signal product_deleted: {product_id}")
        self.product_deleted.emit(product_id)
    
    def emit_stock_updated(self, product_id, new_stock):
        """Émet un signal de mise à jour de stock"""
        self.logger.debug(f"Émission signal stock_updated: produit {product_id}, nouveau stock {new_stock}")
        self.stock_updated.emit(product_id, new_stock)
    
    def emit_stock_adjusted(self, product_id, old_stock, new_stock):
        """Émet un signal d'ajustement de stock"""
        self.logger.debug(f"Émission signal stock_adjusted: produit {product_id}, {old_stock} -> {new_stock}")
        self.stock_adjusted.emit(product_id, old_stock, new_stock)
    
    def emit_invoice_created(self, invoice_data):
        """Émet un signal de création de facture"""
        self.logger.debug(f"Émission signal invoice_created: facture {invoice_data.get('numero', 'N/A')}")
        self.invoice_created.emit(invoice_data)
    
    def emit_invoice_updated(self, invoice_data):
        """Émet un signal de modification de facture"""
        self.logger.debug(f"Émission signal invoice_updated: facture {invoice_data.get('numero', 'N/A')}")
        self.invoice_updated.emit(invoice_data)
    
    def emit_client_created(self, client_data):
        """Émet un signal de création de client"""
        self.logger.debug(f"Émission signal client_created: {client_data.get('nombre', 'N/A')}")
        self.client_created.emit(client_data)
    
    def emit_client_updated(self, client_data):
        """Émet un signal de modification de client"""
        self.logger.debug(f"Émission signal client_updated: {client_data.get('nombre', 'N/A')}")
        self.client_updated.emit(client_data)

# Instance globale du gestionnaire d'événements PyQt5
event_manager = EventManagerPyQt5()
