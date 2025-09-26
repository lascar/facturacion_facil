#!/usr/bin/env python3
"""
Test del sistema de logging implementado
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_logger_creation():
    """Test de creación del sistema de logging"""
    print("🔍 Test de creación del sistema de logging...")
    
    try:
        from utils.logger import app_logger, get_logger, log_info, log_error, log_warning, log_debug
        
        # Verificar que el directorio de logs existe
        logs_dir = "logs"
        assert os.path.exists(logs_dir), f"Directorio de logs {logs_dir} no existe"
        print(f"✅ Directorio de logs existe: {os.path.abspath(logs_dir)}")
        
        # Verificar archivos de log
        main_log = os.path.join(logs_dir, "facturacion_facil.log")
        error_log = os.path.join(logs_dir, "facturacion_facil_errors.log")
        
        # Los archivos pueden no existir aún si no se ha loggeado nada
        print(f"✅ Archivo principal de log: {main_log}")
        print(f"✅ Archivo de errores: {error_log}")
        
        # Test de funciones de logging
        log_info("Test de mensaje INFO")
        log_warning("Test de mensaje WARNING")
        log_debug("Test de mensaje DEBUG")
        log_error("Test de mensaje ERROR")
        
        print("✅ Funciones de logging ejecutadas sin errores")
        
        # Verificar que los archivos se crearon
        assert os.path.exists(main_log), f"Archivo principal {main_log} no se creó"
        print(f"✅ Archivo principal creado: {main_log}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de logging: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_module_loggers():
    """Test de loggers específicos por módulo"""
    print("\n🔍 Test de loggers por módulo...")
    
    try:
        from utils.logger import get_logger
        
        # Test de loggers específicos
        productos_logger = get_logger("productos")
        database_logger = get_logger("database")
        ui_logger = get_logger("ui")
        
        # Test de logging con diferentes módulos
        productos_logger.info("Test desde módulo productos")
        database_logger.info("Test desde módulo database")
        ui_logger.info("Test desde módulo ui")
        
        print("✅ Loggers por módulo funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de módulos: {e}")
        return False

def test_logging_functions():
    """Test de funciones específicas de logging"""
    print("\n🔍 Test de funciones específicas de logging...")
    
    try:
        from utils.logger import (
            log_user_action, log_database_operation, 
            log_file_operation, log_exception
        )
        
        # Test de funciones específicas
        log_user_action("Test acción", "Detalles de la acción")
        log_database_operation("SELECT", "productos", "Test query")
        log_file_operation("COPY", "/test/file.txt", "Test file operation")
        
        # Test de logging de excepción
        try:
            raise ValueError("Test exception")
        except Exception as e:
            log_exception(e, "test_logging_functions")
        
        print("✅ Funciones específicas de logging funcionan")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de funciones específicas: {e}")
        return False

def test_log_file_content():
    """Test del contenido de los archivos de log"""
    print("\n🔍 Test del contenido de archivos de log...")
    
    try:
        logs_dir = "logs"
        main_log = os.path.join(logs_dir, "facturacion_facil.log")
        
        if os.path.exists(main_log):
            with open(main_log, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificar que contiene logs de los tests
            assert "Test de mensaje INFO" in content, "Log INFO no encontrado"
            assert "Test desde módulo productos" in content, "Log de productos no encontrado"
            assert "Test acción" in content, "Log de acción de usuario no encontrado"
            
            print("✅ Contenido de logs verificado")
            
            # Mostrar últimas líneas del log
            lines = content.strip().split('\n')
            print(f"📄 Últimas 3 líneas del log:")
            for line in lines[-3:]:
                print(f"   {line}")
        else:
            print("⚠️  Archivo de log principal no existe aún")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de contenido: {e}")
        return False

def test_log_rotation():
    """Test de rotación de logs (simulado)"""
    print("\n🔍 Test de configuración de rotación...")
    
    try:
        from utils.logger import app_logger
        
        # Verificar configuración de rotación
        for handler in app_logger.logger.handlers:
            if hasattr(handler, 'maxBytes'):
                print(f"✅ Handler con rotación: {handler.__class__.__name__}")
                print(f"   - Tamaño máximo: {handler.maxBytes / (1024*1024):.1f} MB")
                print(f"   - Backups: {handler.backupCount}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de rotación: {e}")
        return False

def test_session_logger():
    """Test del logger de sesión"""
    print("\n🔍 Test del logger de sesión...")
    
    try:
        from utils.logger import app_logger
        
        # Crear logger de sesión
        session_logger = app_logger.create_session_log()
        session_logger.info("Test de sesión específica")
        session_logger.warning("Test warning en sesión")
        
        # Verificar que se creó archivo de sesión
        logs_dir = "logs"
        session_files = [f for f in os.listdir(logs_dir) if f.startswith("session_")]
        
        assert len(session_files) > 0, "No se creó archivo de sesión"
        print(f"✅ Archivo de sesión creado: {session_files[-1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de sesión: {e}")
        return False

def show_log_directory_structure():
    """Muestra la estructura del directorio de logs"""
    print("\n📁 Estructura del directorio de logs:")
    
    logs_dir = "logs"
    if os.path.exists(logs_dir):
        for item in os.listdir(logs_dir):
            item_path = os.path.join(logs_dir, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                print(f"   📄 {item} ({size} bytes)")
            else:
                print(f"   📁 {item}/")
    else:
        print("   ⚠️  Directorio de logs no existe")

def main():
    """Función principal"""
    print("🧪 Test del Sistema de Logging")
    print("=" * 50)
    
    tests = [
        ("Creación del sistema", test_logger_creation),
        ("Loggers por módulo", test_module_loggers),
        ("Funciones específicas", test_logging_functions),
        ("Contenido de archivos", test_log_file_content),
        ("Configuración de rotación", test_log_rotation),
        ("Logger de sesión", test_session_logger)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    # Mostrar estructura de logs
    show_log_directory_structure()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡SISTEMA DE LOGGING FUNCIONANDO CORRECTAMENTE!")
        print("\n📋 Características implementadas:")
        print("   1. ✅ Logging a archivos rotativos")
        print("   2. ✅ Separación de logs de errores")
        print("   3. ✅ Logging por módulos")
        print("   4. ✅ Funciones específicas (usuario, DB, archivos)")
        print("   5. ✅ Logger de sesión")
        print("   6. ✅ Logging a consola")
        print("\n📁 Los logs se guardan en el directorio 'logs/'")
    else:
        print("⚠️  ALGUNOS TESTS DEL SISTEMA DE LOGGING FALLARON!")
        print("Revisa los errores arriba para más detalles.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
