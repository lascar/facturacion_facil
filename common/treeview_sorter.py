# -*- coding: utf-8 -*-
"""
Sistema de ordenación para TreeView con soporte para diferentes tipos de datos
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import re
from utils.logger import get_logger

logger = get_logger("treeview_sorter")

class TreeViewSorter:
    """Clase para manejar la ordenación de TreeView por columnas"""
    
    def __init__(self, treeview):
        self.treeview = treeview
        self.sort_columns = {}  # Diccionario para rastrear el estado de ordenación
        self.setup_column_sorting()
    
    def setup_column_sorting(self):
        """Configura el sorting para todas las columnas del TreeView"""
        try:
            # Obtener todas las columnas
            columns = list(self.treeview['columns'])
            if self.treeview['show'] == 'tree headings':
                columns.insert(0, '#0')  # Incluir la columna del árbol si está visible
            
            # Configurar cada columna para sorting
            for col in columns:
                self.treeview.heading(col, command=lambda c=col: self.sort_by_column(c))
                self.sort_columns[col] = {'reverse': False, 'type': 'text'}
                
                # Añadir indicador visual inicial
                current_text = self.treeview.heading(col, 'text')
                if current_text and not current_text.endswith(' ↕'):
                    self.treeview.heading(col, text=current_text + ' ↕')
            
            logger.info(f"Configurado sorting para {len(columns)} columnas")
            
        except Exception as e:
            logger.error(f"Error configurando sorting: {e}")
    
    def sort_by_column(self, col):
        """Ordena el TreeView por la columna especificada"""
        try:
            # Obtener todos los items
            items = [(self.treeview.set(item, col), item) for item in self.treeview.get_children('')]
            
            # Determinar el tipo de datos para ordenación apropiada
            data_type = self.detect_data_type(items, col)
            self.sort_columns[col]['type'] = data_type
            
            # Ordenar según el tipo de datos
            if data_type == 'numeric':
                items.sort(key=lambda x: self.parse_numeric(x[0]), reverse=self.sort_columns[col]['reverse'])
            elif data_type == 'date':
                items.sort(key=lambda x: self.parse_date(x[0]), reverse=self.sort_columns[col]['reverse'])
            elif data_type == 'currency':
                items.sort(key=lambda x: self.parse_currency(x[0]), reverse=self.sort_columns[col]['reverse'])
            else:  # text
                items.sort(key=lambda x: str(x[0]).lower(), reverse=self.sort_columns[col]['reverse'])
            
            # Reordenar items en el TreeView
            for index, (val, item) in enumerate(items):
                self.treeview.move(item, '', index)
            
            # Actualizar indicadores visuales
            self.update_column_indicators(col)
            
            # Alternar dirección para próximo click
            self.sort_columns[col]['reverse'] = not self.sort_columns[col]['reverse']
            
            logger.debug(f"Ordenado por columna {col} ({data_type}), reverse={not self.sort_columns[col]['reverse']}")
            
        except Exception as e:
            logger.error(f"Error ordenando por columna {col}: {e}")
    
    def detect_data_type(self, items, col):
        """Detecta el tipo de datos en la columna para ordenación apropiada"""
        if not items:
            return 'text'
        
        # Tomar una muestra de los primeros valores no vacíos
        sample_values = []
        for value, _ in items[:10]:  # Muestra de 10 items
            if value and str(value).strip():
                sample_values.append(str(value).strip())
        
        if not sample_values:
            return 'text'
        
        # Detectar moneda (€, $, etc.)
        currency_pattern = r'^[€$£¥]\s*[\d,.]+'
        if any(re.match(currency_pattern, val) for val in sample_values):
            return 'currency'
        
        # Detectar números
        numeric_pattern = r'^-?\d+([.,]\d+)?$'
        if all(re.match(numeric_pattern, val.replace(',', '')) for val in sample_values):
            return 'numeric'
        
        # Detectar fechas (varios formatos)
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
            r'^\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
        ]
        if any(any(re.match(pattern, val) for pattern in date_patterns) for val in sample_values):
            return 'date'
        
        return 'text'
    
    def parse_numeric(self, value):
        """Convierte un valor a número para ordenación"""
        try:
            # Limpiar el valor
            clean_value = str(value).replace(',', '').replace(' ', '')
            return float(clean_value)
        except (ValueError, TypeError):
            return 0.0
    
    def parse_currency(self, value):
        """Convierte un valor de moneda a número para ordenación"""
        try:
            # Remover símbolos de moneda y espacios
            clean_value = re.sub(r'[€$£¥\s]', '', str(value))
            clean_value = clean_value.replace(',', '.')
            return float(clean_value)
        except (ValueError, TypeError):
            return 0.0
    
    def parse_date(self, value):
        """Convierte un valor de fecha a datetime para ordenación"""
        try:
            date_str = str(value).strip()
            
            # Intentar diferentes formatos de fecha
            date_formats = [
                '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S',
                '%d/%m/%Y',
                '%d-%m-%Y',
                '%d/%m/%Y %H:%M:%S',
                '%d-%m-%Y %H:%M:%S'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Si no se puede parsear, devolver fecha mínima
            return datetime.min
            
        except Exception:
            return datetime.min
    
    def update_column_indicators(self, sorted_col):
        """Actualiza los indicadores visuales de ordenación en las columnas"""
        try:
            # Obtener todas las columnas
            columns = list(self.treeview['columns'])
            if self.treeview['show'] == 'tree headings':
                columns.insert(0, '#0')
            
            for col in columns:
                current_text = self.treeview.heading(col, 'text')
                if current_text:
                    # Limpiar indicadores existentes
                    clean_text = current_text.replace(' ↑', '').replace(' ↓', '').replace(' ↕', '')
                    
                    if col == sorted_col:
                        # Añadir indicador de ordenación activa
                        if self.sort_columns[col]['reverse']:
                            new_text = clean_text + ' ↓'
                        else:
                            new_text = clean_text + ' ↑'
                    else:
                        # Añadir indicador de ordenación disponible
                        new_text = clean_text + ' ↕'
                    
                    self.treeview.heading(col, text=new_text)
            
        except Exception as e:
            logger.error(f"Error actualizando indicadores de columna: {e}")
    
    def set_column_type(self, col, data_type):
        """Permite establecer manualmente el tipo de datos de una columna"""
        if col in self.sort_columns:
            self.sort_columns[col]['type'] = data_type
            logger.debug(f"Tipo de columna {col} establecido a {data_type}")
    
    def reset_sorting(self):
        """Resetea el estado de ordenación de todas las columnas"""
        try:
            for col in self.sort_columns:
                self.sort_columns[col]['reverse'] = False
                
                # Limpiar indicadores visuales
                current_text = self.treeview.heading(col, 'text')
                if current_text:
                    clean_text = current_text.replace(' ↑', '').replace(' ↓', '').replace(' ↕', '')
                    self.treeview.heading(col, text=clean_text + ' ↕')
            
            logger.info("Estado de ordenación reseteado")
            
        except Exception as e:
            logger.error(f"Error reseteando ordenación: {e}")

def add_sorting_to_treeview(treeview):
    """Función de conveniencia para añadir sorting a un TreeView existente"""
    return TreeViewSorter(treeview)
