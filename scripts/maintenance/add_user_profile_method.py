#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar el método show_user_profile faltante a MainWindow
"""

import os
import re
from datetime import datetime

def add_user_profile_method():
    """Agrega el método show_user_profile faltante a main_window.py"""
    
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
        
        # Método a agregar
        method_to_add = '''
    def show_user_profile(self):
        """Muestra el perfil del usuario actual"""
        profile_info = f"""👤 Perfil de Usuario
        
🏷️ Usuario: {self.user_name}
🎭 Rol: {self.get_role_display_name(self.user_role)}
📋 Descripción: {self.get_role_info()}

💡 Tip: Tu rol determina qué funciones puedes usar en el sistema."""
        
        messagebox.showinfo("Perfil de Usuario", profile_info)
'''
        
        # Buscar el lugar donde insertar (después de get_user_icon)
        pattern = r'(def get_user_icon\(self, role\):.*?return role_icons\.get\(role, \'👤\'\))'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Insertar después de get_user_icon
            insertion_point = match.end()
            new_content = content[:insertion_point] + method_to_add + content[insertion_point:]
            
            # Escribir archivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Método show_user_profile() agregado exitosamente")
            print(f"📝 Archivo modificado: {file_path}")
            return True
        else:
            print("❌ Error: No se encontró el método get_user_icon para insertar después")
            return False
            
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Agregando método show_user_profile a MainWindow...")
    success = add_user_profile_method()
    
    if success:
        print("\n🎉 ¡Proceso completado! El método show_user_profile() ha sido agregado.")
        print("\n📋 Funcionalidad agregada:")
        print("   • Muestra información del usuario actual")
        print("   • Incluye nombre, rol y descripción")
        print("   • Se activa al hacer clic en el nombre de usuario")
    else:
        print("\n❌ El proceso falló. Revisa los errores anteriores.")