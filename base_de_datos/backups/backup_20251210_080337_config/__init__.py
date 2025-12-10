# -*- coding: utf-8 -*-
"""
Module de configuration pour Facturación Fácil
"""

from .config import Config

# Instance globale de configuration
app_config = Config()

__all__ = ['Config', 'app_config']
