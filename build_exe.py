#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para construir el ejecutable de Facturación Fácil
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Verificar que todos los requisitos estén instalados"""
    print("🔍 Verificando requisitos...")
    
    required_packages = [
        'pyinstaller',
        'customtkinter',
        'pillow',
        'openpyxl',
        'reportlab'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
        print("💡 Instala con: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ Todos los requisitos están instalados")
    return True

def clean_build_dirs():
    """Limpiar directorios de construcción anteriores"""
    print("🧹 Limpiando directorios de construcción...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  🗑️  Eliminado: {dir_name}")
            except Exception as e:
                print(f"  ⚠️  No se pudo eliminar {dir_name}: {e}")
    
    # Limpiar archivos .pyc
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                except:
                    pass

def create_icon_if_missing():
    """Crear icono si no existe"""
    icon_path = Path('assets/icon.ico')
    
    if not icon_path.exists():
        print("🎨 Icono no encontrado, creando...")
        try:
            subprocess.run([sys.executable, 'create_icon.py'], check=True)
            print("✅ Icono creado exitosamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creando icono: {e}")
            return False
    else:
        print("✅ Icono encontrado")
    
    return True

def build_executable():
    """Construir el ejecutable usando PyInstaller"""
    print("🔨 Construyendo ejecutable...")
    
    # Comando PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',  # Limpiar cache
        '--noconfirm',  # No pedir confirmación
        'main.spec'  # Usar archivo .spec
    ]
    
    print(f"📝 Comando: {' '.join(cmd)}")
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Construcción exitosa")
            print("\n📦 Salida de PyInstaller:")
            print(result.stdout)
            return True
        else:
            print("❌ Error en la construcción")
            print("\n📄 Error de PyInstaller:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def verify_executable():
    """Verificar que el ejecutable se creó correctamente"""
    print("🔍 Verificando ejecutable...")
    
    exe_name = 'FacturacionFacil.exe' if sys.platform == 'win32' else 'FacturacionFacil'
    exe_path = Path('dist') / exe_name
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Ejecutable creado: {exe_path}")
        print(f"📏 Tamaño: {size_mb:.1f} MB")
        return True
    else:
        print(f"❌ Ejecutable no encontrado: {exe_path}")
        return False

def show_final_info():
    """Mostrar información final"""
    print("\n" + "="*50)
    print("🎉 CONSTRUCCIÓN COMPLETADA")
    print("="*50)
    
    exe_name = 'FacturacionFacil.exe' if sys.platform == 'win32' else 'FacturacionFacil'
    exe_path = Path('dist') / exe_name
    
    if exe_path.exists():
        print(f"📦 Ejecutable: {exe_path.absolute()}")
        print(f"📏 Tamaño: {exe_path.stat().st_size / (1024 * 1024):.1f} MB")
        print("\n💡 Para distribuir:")
        print(f"  1. Copia el archivo: {exe_path}")
        print("  2. Incluye la carpeta 'assets' si es necesaria")
        print("  3. El ejecutable es independiente y no requiere Python")
        
        print("\n🧪 Para probar:")
        print(f"  {exe_path}")
    else:
        print("❌ No se pudo crear el ejecutable")
        print("💡 Revisa los errores anteriores")

def main():
    """Función principal"""
    print("🚀 CONSTRUCCIÓN DE EJECUTABLE - FACTURACIÓN FÁCIL")
    print("="*50)
    
    # Verificar que estamos en el directorio correcto
    if not Path('main.py').exists():
        print("❌ Error: main.py no encontrado")
        print("💡 Ejecuta este script desde el directorio raíz del proyecto")
        return False
    
    # Pasos de construcción
    steps = [
        ("Verificar requisitos", check_requirements),
        ("Crear icono si falta", create_icon_if_missing),
        ("Limpiar directorios", clean_build_dirs),
        ("Construir ejecutable", build_executable),
        ("Verificar resultado", verify_executable),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Falló: {step_name}")
            return False
    
    show_final_info()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Construcción cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
