#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para diagnosticar y corregir problemas de logo faltante
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Organizacion
from utils.logo_manager import LogoManager
from utils.logger import get_logger

def diagnose_logo_issue():
    """Diagnosticar el problema del logo"""
    print("🔍 Diagnóstico del problema del logo...")
    
    # Obtener organización actual
    org = Organizacion.get()
    if not org:
        print("❌ No hay organización configurada")
        return False
    
    print(f"✅ Organización encontrada: {org.nombre}")
    print(f"📁 Logo path en BD: {org.logo_path}")
    
    # Verificar si el archivo existe
    if not org.logo_path:
        print("⚠️  No hay logo configurado en la base de datos")
        return False
    
    if not os.path.exists(org.logo_path):
        print("❌ El archivo de logo no existe en el sistema de archivos")
        
        # Buscar archivos de logo disponibles
        logo_manager = LogoManager()
        available_logos = logo_manager.list_logos()
        
        if available_logos:
            print(f"📂 Logos disponibles en el directorio:")
            for i, logo in enumerate(available_logos, 1):
                print(f"   {i}. {os.path.basename(logo)}")
            return available_logos
        else:
            print("❌ No hay logos disponibles en el directorio")
            return False
    else:
        print("✅ El archivo de logo existe")
        return True

def fix_logo_issue():
    """Corregir el problema del logo"""
    print("\n🔧 Intentando corregir el problema del logo...")
    
    available_logos = diagnose_logo_issue()
    
    if available_logos is True:
        print("✅ No hay problema que corregir")
        return True
    
    if not available_logos:
        print("❌ No se puede corregir automáticamente - no hay logos disponibles")
        return False
    
    # Usar el primer logo disponible
    new_logo_path = available_logos[0]
    print(f"🔄 Actualizando logo a: {os.path.basename(new_logo_path)}")
    
    # Actualizar la organización
    org = Organizacion.get()
    org.logo_path = new_logo_path
    org.save()
    
    print("✅ Logo actualizado en la base de datos")
    
    # Verificar que funciona
    org_check = Organizacion.get()
    if org_check.logo_path == new_logo_path and os.path.exists(org_check.logo_path):
        print("✅ Corrección exitosa - el logo ahora está disponible")
        return True
    else:
        print("❌ La corrección falló")
        return False

def clear_missing_logo():
    """Limpiar logo faltante de la base de datos"""
    print("\n🧹 Limpiando logo faltante de la base de datos...")
    
    org = Organizacion.get()
    if not org:
        print("❌ No hay organización configurada")
        return False
    
    if not org.logo_path:
        print("✅ No hay logo configurado para limpiar")
        return True
    
    if os.path.exists(org.logo_path):
        print("✅ El logo existe, no necesita limpieza")
        return True
    
    # Limpiar logo faltante
    org.logo_path = ""
    org.save()
    
    print("✅ Logo faltante eliminado de la base de datos")
    return True

if __name__ == "__main__":
    print("🔧 Herramienta de diagnóstico y corrección de logo")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        
        if action == "diagnose":
            diagnose_logo_issue()
        elif action == "fix":
            fix_logo_issue()
        elif action == "clear":
            clear_missing_logo()
        else:
            print("Uso: python fix_missing_logo.py [diagnose|fix|clear]")
    else:
        # Ejecutar diagnóstico y corrección automática
        result = fix_logo_issue()
        if not result:
            print("\n🧹 Intentando limpiar logo faltante...")
            clear_missing_logo()
