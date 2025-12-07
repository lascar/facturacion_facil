#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du système de nettoyage de données
Lance l'interface d'organisation avec le bouton de nettoyage
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.organizacion_pyqt5 import OrganizacionPyQt5Window
from utils.logger import get_logger

def main():
    """Fonction principale pour la démonstration"""
    logger = get_logger("demo_data_cleanup")
    
    print("🚀 DÉMONSTRATION - Système de Nettoyage de Données")
    print("=" * 55)
    print()
    print("Cette démonstration lance l'interface d'organisation")
    print("avec le nouveau bouton rouge de nettoyage de données.")
    print()
    print("📋 Fonctionnalités disponibles:")
    print("• Bouton rouge '🗑️ Limpiar Datos' dans l'interface d'organisation")
    print("• Dialogue de nettoyage sélectif avec options:")
    print("  - Eliminar facturas")
    print("  - Eliminar productos y stocks")
    print("  - Eliminar clientes sin facturas")
    print("  - Eliminar TODOS los clientes")
    print("  - ELIMINAR TODO")
    print("• Backup automático antes de la eliminación")
    print("• Estadísticas en tiempo real de la base de datos")
    print("• Confirmación obligatoria antes de eliminar")
    print()
    print("🔒 Medidas de seguridad:")
    print("• Backup automático activado por defecto")
    print("• Confirmación doble antes de eliminar")
    print("• Opción de cancelar en cualquier momento")
    print("• Barra de progreso durante la operación")
    print()
    print("📖 Instrucciones:")
    print("1. Se abrirá la ventana de configuración de organización")
    print("2. Busca el botón rojo '🗑️ Limpiar Datos' en la parte inferior")
    print("3. Haz clic en el botón para abrir el diálogo de limpieza")
    print("4. Selecciona las opciones de limpieza deseadas")
    print("5. Confirma la operación")
    print()
    print("⚠️  ATENCIÓN: Esta es una demostración con la base de datos real.")
    print("   Se recomienda hacer un backup manual antes de probar.")
    print()
    
    # Preguntar al usuario si quiere continuar
    respuesta = input("¿Quieres continuar con la demostración? (s/N): ").strip().lower()
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Demostración cancelada.")
        return
    
    try:
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        
        # Configurar estilo de la aplicación
        app.setStyle('Fusion')
        
        # Crear ventana de organización
        logger.info("Iniciando ventana de organización con sistema de limpieza")
        window = OrganizacionPyQt5Window()
        
        # Mostrar la ventana
        window.show()
        window.raise_()
        window.activateWindow()
        
        print("\n✅ Ventana de organización abierta.")
        print("   Busca el botón rojo '🗑️ Limpiar Datos' en la parte inferior.")
        print("   Cierra la ventana para terminar la demostración.")
        
        # Ejecutar la aplicación
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Error en la demostración: {e}")
        print(f"\n❌ Error durante la demostración: {e}")
        print("   Verifica que todas las dependencias estén instaladas.")
        sys.exit(1)

if __name__ == "__main__":
    main()
