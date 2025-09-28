#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Monitor en tiempo real de la aplicación - Stock y PDF
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import threading
from datetime import datetime
from database.database import db
from database.models import Factura, Stock, StockMovement
from utils.logger import get_logger

class RealTimeMonitor:
    """Monitor en tiempo real de la aplicación"""
    
    def __init__(self):
        self.logger = get_logger("real_time_monitor")
        self.running = False
        self.last_factura_count = 0
        self.last_stock_movements = 0
        self.monitoring_thread = None
        
        # Estadísticas
        self.stats = {
            'facturas_created': 0,
            'stock_updates': 0,
            'pdf_exports': 0,
            'errors': 0,
            'start_time': None
        }
    
    def start_monitoring(self):
        """Inicia el monitoreo en tiempo real"""
        print("🔍 MONITOR EN TIEMPO REAL - Facturación Fácil")
        print("=" * 60)
        print("Monitoreando:")
        print("   • 📊 Creación de facturas")
        print("   • 🔄 Actualizaciones de stock")
        print("   • 📄 Exportaciones PDF")
        print("   • ❌ Errores del sistema")
        print("   • 📈 Estadísticas en tiempo real")
        print("\nPresiona Ctrl+C para detener el monitor")
        print("-" * 60)
        
        self.running = True
        self.stats['start_time'] = datetime.now()
        
        # Obtener estado inicial
        db.init_database()
        self.last_factura_count = len(Factura.get_all())
        self.last_stock_movements = len(StockMovement.get_all())
        
        # Iniciar thread de monitoreo
        self.monitoring_thread = threading.Thread(target=self._monitor_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        try:
            # Loop principal de interfaz
            self._display_loop()
        except KeyboardInterrupt:
            print("\n\n🛑 Deteniendo monitor...")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Detiene el monitoreo"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        self._show_final_stats()
    
    def _monitor_loop(self):
        """Loop principal de monitoreo"""
        while self.running:
            try:
                self._check_facturas()
                self._check_stock_movements()
                self._check_logs()
                time.sleep(2)  # Verificar cada 2 segundos
            except Exception as e:
                self.logger.error(f"Error en monitor loop: {e}")
                self.stats['errors'] += 1
                time.sleep(5)
    
    def _check_facturas(self):
        """Verifica nuevas facturas"""
        try:
            current_count = len(Factura.get_all())
            if current_count > self.last_factura_count:
                new_facturas = current_count - self.last_factura_count
                self.stats['facturas_created'] += new_facturas
                self.last_factura_count = current_count
                
                # Obtener la última factura
                facturas = Factura.get_all()
                if facturas:
                    ultima_factura = facturas[-1]
                    self._log_event("📊 NUEVA FACTURA", 
                                  f"{ultima_factura.numero_factura} - {ultima_factura.nombre_cliente} - €{ultima_factura.total_factura:.2f}")
        except Exception as e:
            self.logger.error(f"Error verificando facturas: {e}")
    
    def _check_stock_movements(self):
        """Verifica movimientos de stock"""
        try:
            current_movements = len(StockMovement.get_all())
            if current_movements > self.last_stock_movements:
                new_movements = current_movements - self.last_stock_movements
                self.stats['stock_updates'] += new_movements
                self.last_stock_movements = current_movements
                
                # Obtener el último movimiento
                movements = StockMovement.get_all()
                if movements:
                    ultimo_movimiento = movements[-1]
                    self._log_event("🔄 STOCK ACTUALIZADO", 
                                  f"Producto ID {ultimo_movimiento.producto_id} - {ultimo_movimiento.tipo} - Cantidad: {ultimo_movimiento.cantidad}")
        except Exception as e:
            self.logger.error(f"Error verificando movimientos de stock: {e}")
    
    def _check_logs(self):
        """Verifica logs para detectar exportaciones PDF y errores"""
        try:
            # Leer las últimas líneas del log
            log_file = "logs/facturacion_facil.log"
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                # Verificar las últimas 10 líneas
                recent_lines = lines[-10:] if len(lines) >= 10 else lines
                
                for line in recent_lines:
                    if "exportar_pdf" in line.lower() and "INFO" in line:
                        if not hasattr(self, '_last_pdf_log') or line != self._last_pdf_log:
                            self.stats['pdf_exports'] += 1
                            self._log_event("📄 PDF EXPORTADO", "Factura exportada a PDF")
                            self._last_pdf_log = line
                    
                    elif "ERROR" in line:
                        if not hasattr(self, '_last_error_log') or line != self._last_error_log:
                            self.stats['errors'] += 1
                            error_msg = line.split(" - ")[-1].strip() if " - " in line else "Error desconocido"
                            self._log_event("❌ ERROR", error_msg[:50] + "..." if len(error_msg) > 50 else error_msg)
                            self._last_error_log = line
                            
        except Exception as e:
            self.logger.error(f"Error verificando logs: {e}")
    
    def _log_event(self, event_type, message):
        """Registra un evento"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {event_type}: {message}")
    
    def _display_loop(self):
        """Loop de visualización de estadísticas"""
        while self.running:
            try:
                # Limpiar pantalla cada 10 segundos
                time.sleep(10)
                if self.running:
                    self._show_stats()
            except KeyboardInterrupt:
                break
    
    def _show_stats(self):
        """Muestra estadísticas actuales"""
        if not self.running:
            return
            
        print("\n" + "=" * 60)
        print("📈 ESTADÍSTICAS EN TIEMPO REAL")
        print("=" * 60)
        
        # Tiempo de ejecución
        if self.stats['start_time']:
            elapsed = datetime.now() - self.stats['start_time']
            elapsed_str = str(elapsed).split('.')[0]  # Sin microsegundos
            print(f"⏱️  Tiempo de monitoreo: {elapsed_str}")
        
        # Estadísticas principales
        print(f"📊 Facturas creadas: {self.stats['facturas_created']}")
        print(f"🔄 Actualizaciones de stock: {self.stats['stock_updates']}")
        print(f"📄 Exportaciones PDF: {self.stats['pdf_exports']}")
        print(f"❌ Errores detectados: {self.stats['errors']}")
        
        # Estado actual del sistema
        try:
            total_facturas = len(Factura.get_all())
            total_movements = len(StockMovement.get_all())
            print(f"\n📋 Estado actual:")
            print(f"   • Total facturas en BD: {total_facturas}")
            print(f"   • Total movimientos stock: {total_movements}")
            
            # Stock bajo
            productos_stock_bajo = self._get_low_stock_products()
            if productos_stock_bajo:
                print(f"   • ⚠️  Productos con stock bajo: {len(productos_stock_bajo)}")
                for producto_id, stock_actual in productos_stock_bajo[:3]:  # Mostrar solo los primeros 3
                    print(f"     - Producto ID {producto_id}: {stock_actual} unidades")
            else:
                print(f"   • ✅ No hay productos con stock bajo")
                
        except Exception as e:
            print(f"   • ❌ Error obteniendo estado: {e}")
        
        print("-" * 60)
        print("Monitoreando... (Ctrl+C para detener)")
    
    def _get_low_stock_products(self):
        """Obtiene productos con stock bajo"""
        try:
            from database.models import Producto
            productos = Producto.get_all()
            stock_bajo = []
            
            for producto in productos:
                stock_actual = Stock.get_by_product(producto.id)
                if stock_actual <= 5:  # Stock bajo
                    stock_bajo.append((producto.id, stock_actual))
            
            return sorted(stock_bajo, key=lambda x: x[1])  # Ordenar por stock
        except Exception as e:
            self.logger.error(f"Error obteniendo productos con stock bajo: {e}")
            return []
    
    def _show_final_stats(self):
        """Muestra estadísticas finales"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL DEL MONITOREO")
        print("=" * 60)
        
        if self.stats['start_time']:
            elapsed = datetime.now() - self.stats['start_time']
            elapsed_str = str(elapsed).split('.')[0]
            print(f"⏱️  Duración total: {elapsed_str}")
        
        print(f"📊 Facturas creadas: {self.stats['facturas_created']}")
        print(f"🔄 Actualizaciones de stock: {self.stats['stock_updates']}")
        print(f"📄 Exportaciones PDF: {self.stats['pdf_exports']}")
        print(f"❌ Errores detectados: {self.stats['errors']}")
        
        # Análisis
        total_activity = (self.stats['facturas_created'] + 
                         self.stats['stock_updates'] + 
                         self.stats['pdf_exports'])
        
        if total_activity > 0:
            print(f"\n📈 Análisis:")
            print(f"   • Actividad total: {total_activity} eventos")
            if self.stats['facturas_created'] > 0:
                ratio_stock = self.stats['stock_updates'] / self.stats['facturas_created']
                print(f"   • Ratio stock/facturas: {ratio_stock:.2f}")
                if ratio_stock >= 0.8:
                    print(f"   • ✅ Stock se actualiza correctamente")
                else:
                    print(f"   • ⚠️ Algunas facturas no actualizaron stock")
            
            if self.stats['errors'] == 0:
                print(f"   • ✅ Sin errores durante el monitoreo")
            else:
                print(f"   • ⚠️ {self.stats['errors']} errores detectados")
        else:
            print(f"\n📋 No se detectó actividad durante el monitoreo")
            print(f"   • La aplicación puede no estar en uso")
            print(f"   • O el monitoreo fue muy breve")
        
        print("\n🎯 Monitor finalizado correctamente")

def main():
    """Función principal"""
    print("🚀 INICIANDO MONITOR EN TIEMPO REAL")
    print("Este monitor detecta automáticamente:")
    print("   • Nuevas facturas creadas")
    print("   • Actualizaciones de stock")
    print("   • Exportaciones PDF")
    print("   • Errores del sistema")
    print("\nUsa la aplicación normalmente en otra ventana")
    print("El monitor mostrará la actividad en tiempo real")
    
    monitor = RealTimeMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
