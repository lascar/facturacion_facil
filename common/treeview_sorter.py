#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de tri pour TreeView - Compatibilité PyQt5
"""

class TreeViewSorter:
    """Classe pour gérer le tri des TreeView"""

    def __init__(self, treeview=None):
        self.treeview = treeview
        self.sort_column = 0
        self.sort_order = 'asc'
        print("TreeViewSorter inicializado")

    def set_treeview(self, treeview):
        """Définit le TreeView à trier"""
        self.treeview = treeview
        self.enable_sorting()

    def enable_sorting(self):
        """Active le tri sur le TreeView"""
        if not self.treeview:
            return False

        try:
            # Pour PyQt5, activer le tri sur les colonnes
            if hasattr(self.treeview, 'setSortingEnabled'):
                self.treeview.setSortingEnabled(True)

            # Activer le tri par clic sur les en-têtes
            if hasattr(self.treeview, 'header'):
                header = self.treeview.header()
                if hasattr(header, 'setSectionsClickable'):
                    header.setSectionsClickable(True)
                if hasattr(header, 'setSortIndicatorShown'):
                    header.setSortIndicatorShown(True)

            print("Tri activé pour TreeView PyQt5")
            return True

        except Exception as e:
            print(f"Erreur lors de l'activation du tri: {e}")
            return False

    def sort_by_column(self, column, order='asc'):
        """Trie par colonne"""
        self.sort_column = column
        self.sort_order = order
        print(f"Tri par colonne {column} en ordre {order}")
        return True

def add_sorting_to_treeview(treeview):
    """
    Ajoute la fonctionnalité de tri à un TreeView PyQt5

    Args:
        treeview: Widget TreeView PyQt5
    """
    sorter = TreeViewSorter(treeview)
    return sorter.enable_sorting()
