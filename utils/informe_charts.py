# -*- coding: utf-8 -*-
"""
Générateur de graphiques pour les rapports
"""

import os
import tempfile
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Backend sans interface graphique
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.logger import get_logger


class InformeChartGenerator:
    """Générateur de graphiques pour les rapports"""
    
    def __init__(self):
        self.logger = get_logger("informe_charts")
        # Configuration du style
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def create_facturacion_chart(self, informe_data):
        """Créer un graphique pour le rapport de facturation"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Graphique 1: Décomposition par IVA
            desglose_iva = informe_data.get('desglose_iva', [])
            if desglose_iva:
                labels = [f"{item['iva_aplicado']:.0f}%" for item in desglose_iva]
                sizes = [item['total'] for item in desglose_iva]
                colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
                
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(sizes)])
                ax1.set_title('Distribución por Tasa de IVA', fontsize=12, fontweight='bold')
            
            # Graphique 2: Top 10 productos
            productos = informe_data.get('productos_mas_vendidos', [])[:10]
            if productos:
                nombres = [p['nombre'][:20] for p in productos]
                totales = [p['total_vendido'] for p in productos]
                
                ax2.barh(nombres, totales, color='#3498db')
                ax2.set_xlabel('Total Vendido (€)', fontsize=10)
                ax2.set_title('Top 10 Productos Más Vendidos', fontsize=12, fontweight='bold')
                ax2.invert_yaxis()
            
            plt.tight_layout()
            
            # Guardar en archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            plt.savefig(temp_file.name, dpi=100, bbox_inches='tight')
            plt.close(fig)
            
            self.logger.info(f"Gráfico de facturación generado: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            self.logger.error(f"Error generando gráfico de facturación: {e}")
            return None
    
    def create_stock_chart(self, informe_data):
        """Créer un graphique pour le rapport de stock"""
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Graphique 1: Distribución por categoría
            por_categoria = informe_data.get('por_categoria', [])
            if por_categoria:
                categorias = [cat['categoria'][:15] for cat in por_categoria]
                valores = [cat['valor_total'] for cat in por_categoria]
                colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
                
                ax1.pie(valores, labels=categorias, autopct='%1.1f%%', colors=colors[:len(valores)])
                ax1.set_title('Valor de Stock por Categoría', fontsize=12, fontweight='bold')
            
            # Graphique 2: Productos con bajo stock
            productos = informe_data.get('productos', [])
            productos_bajo_stock = [p for p in productos if p.get('stock_actual', 0) < 10][:10]
            
            if productos_bajo_stock:
                nombres = [p['nombre'][:20] for p in productos_bajo_stock]
                stocks = [p['stock_actual'] for p in productos_bajo_stock]
                
                colors_bars = ['#e74c3c' if s == 0 else '#f39c12' for s in stocks]
                ax2.barh(nombres, stocks, color=colors_bars)
                ax2.set_xlabel('Stock Actual', fontsize=10)
                ax2.set_title('Productos con Bajo Stock', fontsize=12, fontweight='bold')
                ax2.invert_yaxis()
            else:
                ax2.text(0.5, 0.5, 'No hay productos con bajo stock',
                        ha='center', va='center', fontsize=12)
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
                ax2.axis('off')
            
            plt.tight_layout()
            
            # Guardar en archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            plt.savefig(temp_file.name, dpi=100, bbox_inches='tight')
            plt.close(fig)
            
            self.logger.info(f"Gráfico de stock generado: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            self.logger.error(f"Error generando gráfico de stock: {e}")
            return None
    
    def create_qt_canvas(self, informe_data, tipo='facturacion'):
        """Créer un canvas Qt pour afficher dans l'interface"""
        try:
            fig = Figure(figsize=(10, 4))
            canvas = FigureCanvas(fig)
            
            if tipo == 'facturacion':
                ax1, ax2 = fig.subplots(1, 2)
                
                # Décomposition par IVA
                desglose_iva = informe_data.get('desglose_iva', [])
                if desglose_iva:
                    labels = [f"{item['iva_aplicado']:.0f}%" for item in desglose_iva]
                    sizes = [item['total'] for item in desglose_iva]
                    colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
                    
                    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(sizes)])
                    ax1.set_title('Distribución por IVA')
                
                # Top productos
                productos = informe_data.get('productos_mas_vendidos', [])[:10]
                if productos:
                    nombres = [p['nombre'][:15] for p in productos]
                    totales = [p['total_vendido'] for p in productos]
                    
                    ax2.barh(nombres, totales, color='#3498db')
                    ax2.set_xlabel('Total (€)')
                    ax2.set_title('Top 10 Productos')
                    ax2.invert_yaxis()
            
            fig.tight_layout()
            return canvas
            
        except Exception as e:
            self.logger.error(f"Error creando canvas Qt: {e}")
            return None


# Instance globale
informe_chart_generator = InformeChartGenerator()

