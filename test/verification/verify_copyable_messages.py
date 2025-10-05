#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification pour s'assurer que tous les messages d'erreur 
utilisent les dialogues copiables avec bouton "Copiar"
"""
import os
import sys
import re

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class CopyableMessageVerifier:
    """Vérificateur de messages copiables"""
    
    def __init__(self):
        self.root_dir = os.path.join(os.path.dirname(__file__), '..', '..')
        self.issues_found = []
        self.files_checked = 0
        self.total_messageboxes = 0
        self.copyable_messages = 0
        
        # Fichiers à exclure (tests, demos, etc.)
        self.excluded_patterns = [
            r'test/',
            r'tests/',
            r'__pycache__/',
            r'\.pyc$',
            r'demo_',
            r'test_'
        ]
        
        # Patterns de messagebox à détecter
        self.messagebox_patterns = [
            r'messagebox\.showerror\s*\(',
            r'messagebox\.showwarning\s*\(',
            r'messagebox\.showinfo\s*\(',
            r'messagebox\.askyesno\s*\(',
            r'messagebox\.askquestion\s*\(',
            r'messagebox\.askokcancel\s*\(',
            r'messagebox\.askyesnocancel\s*\(',
            r'messagebox\.askretrycancel\s*\('
        ]
        
        # Patterns de messages copiables
        self.copyable_patterns = [
            r'show_copyable_error\s*\(',
            r'show_copyable_warning\s*\(',
            r'show_copyable_info\s*\(',
            r'show_copyable_confirm\s*\(',
            r'show_copyable_success\s*\(',
            r'self\._show_message\s*\('
        ]
    
    def should_exclude_file(self, filepath):
        """Verifica si un archivo debe ser excluido"""
        for pattern in self.excluded_patterns:
            if re.search(pattern, filepath):
                return True
        return False
    
    def analyze_file(self, filepath):
        """Analiza un archivo Python en busca de messageboxes"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar messageboxes estándar
            messagebox_matches = []
            for pattern in self.messagebox_patterns:
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    line_content = content.split('\n')[line_num - 1].strip()
                    messagebox_matches.append((line_num, line_content, pattern))
            
            # Buscar mensajes copiables
            copyable_matches = []
            for pattern in self.copyable_patterns:
                matches = re.finditer(pattern, content, re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    line_content = content.split('\n')[line_num - 1].strip()
                    copyable_matches.append((line_num, line_content, pattern))
            
            # Verificar si hay fallbacks válidos
            valid_fallbacks = self.check_fallbacks(content, messagebox_matches)
            
            return {
                'messageboxes': messagebox_matches,
                'copyable': copyable_matches,
                'valid_fallbacks': valid_fallbacks,
                'content': content
            }
            
        except Exception as e:
            print(f"❌ Error analizando {filepath}: {e}")
            return None
    
    def check_fallbacks(self, content, messagebox_matches):
        """Verifica si los messageboxes están en bloques de fallback válidos"""
        valid_fallbacks = []
        
        for line_num, line_content, pattern in messagebox_matches:
            # Buscar contexto alrededor de la línea
            lines = content.split('\n')
            start_context = max(0, line_num - 10)
            end_context = min(len(lines), line_num + 5)
            context = '\n'.join(lines[start_context:end_context])
            
            # Verificar si está en un bloque try/except con show_copyable
            is_fallback = (
                'except' in context and 
                ('show_copyable' in context or 'fallback' in context.lower())
            )
            
            if is_fallback:
                valid_fallbacks.append((line_num, line_content))
        
        return valid_fallbacks
    
    def scan_directory(self):
        """Escanea todos los archivos Python en el directorio"""
        print("🔍 Escaneando archivos Python en busca de messageboxes...")
        
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    relative_path = os.path.relpath(filepath, self.root_dir)
                    
                    if self.should_exclude_file(relative_path):
                        continue
                    
                    self.files_checked += 1
                    result = self.analyze_file(filepath)
                    
                    if result:
                        self.process_file_result(relative_path, result)
    
    def process_file_result(self, filepath, result):
        """Procesa los resultados del análisis de un archivo"""
        messageboxes = result['messageboxes']
        copyable = result['copyable']
        valid_fallbacks = result['valid_fallbacks']
        
        self.total_messageboxes += len(messageboxes)
        self.copyable_messages += len(copyable)
        
        # Messageboxes problemáticos (no en fallbacks válidos)
        problematic_messageboxes = []
        for mb in messageboxes:
            line_num, line_content, pattern = mb
            is_valid_fallback = any(fb[0] == line_num for fb in valid_fallbacks)
            if not is_valid_fallback:
                problematic_messageboxes.append(mb)
        
        if problematic_messageboxes:
            self.issues_found.append({
                'file': filepath,
                'problematic_messageboxes': problematic_messageboxes,
                'copyable_count': len(copyable),
                'total_messageboxes': len(messageboxes)
            })
    
    def generate_report(self):
        """Genera un reporte de los resultados"""
        print("\n" + "=" * 80)
        print("📊 REPORTE DE VERIFICACIÓN DE MENSAJES COPIABLES")
        print("=" * 80)
        
        print(f"\n📁 Archivos analizados: {self.files_checked}")
        print(f"📋 Total messageboxes encontrados: {self.total_messageboxes}")
        print(f"✅ Mensajes copiables encontrados: {self.copyable_messages}")
        
        if self.issues_found:
            print(f"\n⚠️  PROBLEMAS ENCONTRADOS: {len(self.issues_found)} archivos")
            print("-" * 80)
            
            for issue in self.issues_found:
                print(f"\n📄 Archivo: {issue['file']}")
                print(f"   📊 Messageboxes problemáticos: {len(issue['problematic_messageboxes'])}")
                print(f"   ✅ Mensajes copiables: {issue['copyable_count']}")
                
                for line_num, line_content, pattern in issue['problematic_messageboxes']:
                    print(f"   ❌ Línea {line_num}: {line_content[:80]}...")
                    print(f"      Pattern: {pattern}")
        else:
            print("\n🎉 ¡EXCELENTE! No se encontraron problemas.")
            print("   Todos los mensajes de error utilizan diálogos copiables.")
        
        # Estadísticas
        if self.total_messageboxes > 0:
            percentage = (self.copyable_messages / (self.total_messageboxes + self.copyable_messages)) * 100
            print(f"\n📈 Porcentaje de mensajes copiables: {percentage:.1f}%")
        
        print("\n" + "=" * 80)
        
        return len(self.issues_found) == 0
    
    def suggest_fixes(self):
        """Sugiere correcciones para los problemas encontrados"""
        if not self.issues_found:
            return
        
        print("\n💡 SUGERENCIAS DE CORRECCIÓN:")
        print("-" * 80)
        
        for issue in self.issues_found:
            print(f"\n📄 {issue['file']}:")
            
            for line_num, line_content, pattern in issue['problematic_messageboxes']:
                print(f"\n   Línea {line_num}:")
                print(f"   ❌ Actual: {line_content}")
                
                # Sugerir reemplazo
                if 'showerror' in pattern:
                    print(f"   ✅ Sugerido: show_copyable_error(parent, title, message)")
                elif 'showwarning' in pattern:
                    print(f"   ✅ Sugerido: show_copyable_warning(parent, title, message)")
                elif 'showinfo' in pattern:
                    print(f"   ✅ Sugerido: show_copyable_info(parent, title, message)")
                elif 'askyesno' in pattern:
                    print(f"   ✅ Sugerido: show_copyable_confirm(parent, title, message)")
                else:
                    print(f"   ✅ Sugerido: Usar función copiable equivalente")
                
                print(f"   📝 Agregar import: from common.custom_dialogs import show_copyable_*")

def main():
    """Función principal"""
    print("🚀 Verificador de Mensajes Copiables")
    print("Verificando que todos los mensajes de error tengan botón 'Copiar'...")
    
    verifier = CopyableMessageVerifier()
    verifier.scan_directory()
    success = verifier.generate_report()
    
    if not success:
        verifier.suggest_fixes()
        print("\n🔧 Para corregir automáticamente, ejecute:")
        print("   python test/verification/fix_copyable_messages.py")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
