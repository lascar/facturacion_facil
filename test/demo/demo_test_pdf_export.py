#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test de l'exportation PDF avec interface graphique
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import customtkinter as ctk
from database.database import db
from database.models import Factura
from ui.facturas import FacturasWindow
from utils.logger import get_logger

def demo_pdf_export_with_gui():
    """Test de l'exportation PDF avec interface graphique"""
    
    print("🧪 TEST - Exportation PDF avec Interface Graphique")
    print("=" * 60)
    
    # Initialiser la base de données
    db.init_database()
    
    try:
        print("1️⃣ Vérification des facturas disponibles...")
        
        facturas = Factura.get_all()
        if len(facturas) == 0:
            print("   ❌ No hay facturas disponibles para test")
            return False
        
        print(f"   ✅ {len(facturas)} facturas disponibles")
        primera_factura = facturas[0]
        print(f"   📋 Factura de test: {primera_factura.numero_factura}")
        
        print("\n2️⃣ Creando interfaz de test...")
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Exportación PDF")
        app.geometry("800x600")
        
        # Variable pour stocker le résultat
        test_result = {"success": False, "error": None}
        
        # Créer la fenêtre de facturas
        try:
            facturas_window = FacturasWindow(app)
            print("   ✅ Ventana de facturas creada")
        except Exception as e:
            print(f"   ❌ Error creando ventana de facturas: {e}")
            app.destroy()
            return False
        
        print("\n3️⃣ Simulando selección de factura...")
        
        def simulate_selection_and_export():
            """Simule la sélection et l'exportation"""
            try:
                print("   🔄 Simulando selección...")
                
                # Simuler la sélection directement
                facturas_window.selected_factura = primera_factura
                print(f"   ✅ selected_factura establecida: {facturas_window.selected_factura.numero_factura}")
                
                # Vérifier l'état avant exportation
                print("   🔍 Verificando estado antes de exportar...")
                print(f"      selected_factura: {facturas_window.selected_factura is not None}")
                print(f"      Número: {facturas_window.selected_factura.numero_factura if facturas_window.selected_factura else 'None'}")
                
                # Essayer l'exportation
                print("   📄 Intentando exportar PDF...")
                facturas_window.exportar_pdf()
                
                test_result["success"] = True
                print("   ✅ Exportación PDF completada sin errores")
                
            except Exception as e:
                test_result["error"] = str(e)
                print(f"   ❌ Error durante exportación: {e}")
                import traceback
                traceback.print_exc()
            
            # Cerrar la aplicación después del test
            app.after(1000, app.quit)
        
        # Crear interfaz de test
        info_frame = ctk.CTkFrame(app)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=f"TEST DE EXPORTACIÓN PDF\n\n"
                 f"Factura de test: {primera_factura.numero_factura}\n"
                 f"Cliente: {primera_factura.nombre_cliente}\n"
                 f"Total: €{primera_factura.total_factura:.2f}\n\n"
                 f"Haz clic en el botón para probar la exportación:",
            font=ctk.CTkFont(size=12),
            justify="center"
        )
        info_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Botón de test
        test_btn = ctk.CTkButton(
            info_frame,
            text="🔍 Probar Exportación PDF",
            command=simulate_selection_and_export,
            fg_color="#2E8B57",
            hover_color="#228B22",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        test_btn.pack(pady=20)
        
        # Label de resultado
        result_label = ctk.CTkLabel(
            info_frame,
            text="Resultado aparecerá aquí",
            font=ctk.CTkFont(size=12)
        )
        result_label.pack(pady=10)
        
        def update_result():
            """Actualiza el resultado en la interfaz"""
            if test_result["success"]:
                result_label.configure(
                    text="✅ EXPORTACIÓN EXITOSA\nEl PDF se generó correctamente",
                    text_color="green"
                )
            elif test_result["error"]:
                result_label.configure(
                    text=f"❌ ERROR EN EXPORTACIÓN\n{test_result['error'][:100]}...",
                    text_color="red"
                )
            
            # Programar siguiente actualización
            app.after(500, update_result)
        
        # Iniciar actualización de resultado
        app.after(500, update_result)
        
        print("\n🚀 Iniciando aplicación de test...")
        print("💡 Haz clic en el botón para probar la exportación PDF")
        
        # Ejecutar la aplicación
        app.mainloop()
        
        # Resultado final
        if test_result["success"]:
            print("\n✅ TEST EXITOSO - PDF exportado correctamente")
            return True
        elif test_result["error"]:
            print(f"\n❌ TEST FALLIDO - Error: {test_result['error']}")
            return False
        else:
            print("\n⚠️ TEST INCOMPLETO - No se ejecutó la exportación")
            return False
        
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_direct_pdf_method():
    """Test directo del método de exportación PDF"""
    
    print("\n🔬 TEST DIRECTO - Método exportar_pdf")
    print("-" * 40)
    
    try:
        # Importar la clase de métodos
        from ui.facturas_methods import FacturasMethodsMixin
        
        # Crear una clase de test
        class TestPDFExport(FacturasMethodsMixin):
            def __init__(self):
                self.logger = get_logger("test_pdf_direct")
                self.selected_factura = None
                self.window = None
            
            def _show_message(self, msg_type, title, message):
                print(f"[{msg_type.upper()}] {title}: {message}")
        
        # Crear instancia de test
        test_instance = TestPDFExport()
        
        # Obtener una factura
        facturas = Factura.get_all()
        if len(facturas) == 0:
            print("   ❌ No hay facturas para test directo")
            return False
        
        primera_factura = facturas[0]
        print(f"   📋 Usando factura: {primera_factura.numero_factura}")
        
        # Test 1: Sin factura seleccionada
        print("   🔍 Test 1: Sin factura seleccionada")
        test_instance.selected_factura = None
        try:
            test_instance.exportar_pdf()
            print("      ⚠️ No se mostró error (inesperado)")
        except Exception as e:
            print(f"      ✅ Error esperado: {e}")
        
        # Test 2: Con factura seleccionada
        print("   🔍 Test 2: Con factura seleccionada")
        test_instance.selected_factura = primera_factura
        try:
            test_instance.exportar_pdf()
            print("      ✅ Método ejecutado sin errores")
            return True
        except Exception as e:
            print(f"      ❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"   ❌ Error en test directo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TESTS DE EXPORTACIÓN PDF")
    print("=" * 70)
    
    # Test 1: Método directo
    print("FASE 1: Test directo del método")
    success1 = demo_direct_pdf_method()
    
    if success1:
        print("\n" + "=" * 70)
        print("FASE 2: Test con interfaz gráfica")
        success2 = demo_pdf_export_with_gui()
    else:
        print("\n❌ Test directo falló - No continuar con interfaz gráfica")
        success2 = False
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE TESTS:")
    print(f"   Test directo: {'✅ ÉXITO' if success1 else '❌ FALLO'}")
    print(f"   Test con GUI: {'✅ ÉXITO' if success2 else '❌ FALLO'}")
    
    if success1 and success2:
        print("\n🎉 TODOS LOS TESTS EXITOSOS")
        print("La exportación PDF funciona correctamente")
    elif success1:
        print("\n⚠️ MÉTODO FUNCIONA, PROBLEMA EN GUI")
        print("El método de exportación funciona, pero hay problemas en la interfaz")
        print("Revisar la selección de facturas en la aplicación real")
    else:
        print("\n❌ PROBLEMAS EN EXPORTACIÓN PDF")
        print("Revisar la implementación del método exportar_pdf")
    
    print("\n📚 INFORMACIÓN ADICIONAL:")
    print("• Si ReportLab no está instalado: pip install reportlab")
    print("• Logs detallados en: logs/facturacion_facil.log")
    print("• Buscar líneas con '🔍 DEBUG PDF'")
    print("• Verificar permisos de escritura en directorio de PDFs")
