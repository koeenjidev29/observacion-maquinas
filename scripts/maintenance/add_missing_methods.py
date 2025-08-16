#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar métodos faltantes a MainWindow
Agrega get_role_display_name() y get_user_icon() que están siendo llamados pero no existen
"""

import os
import re
from datetime import datetime

def add_missing_methods():
    """Agrega los métodos faltantes a main_window.py"""
    
    # Ruta del archivo
    file_path = os.path.join('gui', 'main_window.py')
    
    if not os.path.exists(file_path):
        print(f"❌ Error: No se encontró el archivo {file_path}")
        return False
    
    # Crear backup
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Leer archivo original
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Crear backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📁 Backup creado: {backup_path}")
        
        # Métodos a agregar
        methods_to_add = '''
    def get_role_display_name(self, role):
        """Obtiene el nombre de visualización del rol"""
        role_names = {
            'admin': 'Administrador',
            'administrador': 'Administrador', 
            'supervisor': 'Supervisor',
            'operador': 'Operador',
            'tecnico': 'Técnico',
            'invitado': 'Invitado'
        }
        return role_names.get(role, 'Usuario')
    
    def get_user_icon(self, role):
        """Obtiene el icono del usuario según su rol"""
        role_icons = {
            'admin': '👑',
            'administrador': '👑',
            'supervisor': '👨‍💼', 
            'operador': '👷',
            'tecnico': '🔧',
            'invitado': '👤'
        }
        return role_icons.get(role, '👤')
'''
        
        # Buscar el lugar donde insertar (después de get_role_info)
        pattern = r'(def get_role_info\(self\):.*?return role_info\.get\(self\.user_role, "Rol no definido"\))'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Insertar después de get_role_info
            insertion_point = match.end()
            new_content = content[:insertion_point] + methods_to_add + content[insertion_point:]
            
            # Escribir archivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Métodos agregados exitosamente:")
            print("   - get_role_display_name()")
            print("   - get_user_icon()")
            print(f"📝 Archivo modificado: {file_path}")
            return True
        else:
            print("❌ Error: No se encontró el método get_role_info para insertar después")
            return False
            
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Agregando métodos faltantes a MainWindow...")
    success = add_missing_methods()
    
    if success:
        print("\n🎉 ¡Proceso completado! Ahora puedes ejecutar la aplicación sin errores.")
        print("\n📋 Métodos agregados:")
        print("   • get_role_display_name(role) - Devuelve nombre legible del rol")
        print("   • get_user_icon(role) - Devuelve emoji según el rol")
    else:
        print("\n❌ El proceso falló. Revisa los errores anteriores.")