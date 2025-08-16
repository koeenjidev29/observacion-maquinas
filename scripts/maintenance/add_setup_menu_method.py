#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar el método setup_menu faltante a MainWindow
"""

import os
import re
from datetime import datetime

def add_setup_menu_method():
    """Agrega el método setup_menu faltante a main_window.py"""
    
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
    def setup_menu(self):
        """Configura el menú principal de la aplicación"""
        # Crear barra de menú
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 Archivo", menu=file_menu)
        file_menu.add_command(label="📊 Exportar a Excel", command=self.export_to_excel)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Cerrar Sesión", command=self.handle_logout)
        file_menu.add_command(label="❌ Salir", command=self.close)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ Ver", menu=view_menu)
        view_menu.add_command(label="🔄 Actualizar", command=self.refresh_data)
        view_menu.add_command(label="📈 Estadísticas", command=self.show_statistics)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Herramientas", menu=tools_menu)
        tools_menu.add_command(label="⚙️ Configuración", command=self.show_config)
        tools_menu.add_command(label="🗑️ Limpiar Datos", command=self.clear_all_data)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Ayuda", menu=help_menu)
        help_menu.add_command(label="ℹ️ Acerca de", command=self.show_about)
        help_menu.add_command(label="📖 Manual", command=self.show_help)
    
    def export_to_excel(self):
        """Exporta los datos actuales a Excel"""
        try:
            # Implementar exportación a Excel
            messagebox.showinfo("Exportar", "Funcionalidad de exportación - Próximamente disponible")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def refresh_data(self):
        """Actualiza los datos mostrados"""
        try:
            self.load_observations()
            messagebox.showinfo("Actualizar", "Datos actualizados correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")
    
    def show_statistics(self):
        """Muestra estadísticas del sistema"""
        try:
            stats = self.db_manager.get_statistics()
            stats_text = f"""📊 Estadísticas del Sistema
            
📝 Total de observaciones: {stats.get('total', 0)}
🏭 Máquinas registradas: {len(stats.get('por_maquina', {}))}
👥 Usuarios activos: {len(stats.get('por_usuario', {}))}
📅 Último registro: {stats.get('ultima_fecha', 'N/A')}"""
            messagebox.showinfo("Estadísticas", stats_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener estadísticas: {e}")
    
    def clear_all_data(self):
        """Limpia todos los datos (con confirmación)"""
        result = messagebox.askyesno(
            "⚠️ Confirmar",
            "¿Estás seguro de que quieres eliminar TODAS las observaciones?\n\n⚠️ Esta acción NO se puede deshacer."
        )
        if result:
            try:
                self.db_manager.clear_all_observations()
                self.load_observations()
                messagebox.showinfo("Éxito", "Todos los datos han sido eliminados")
            except Exception as e:
                messagebox.showerror("Error", f"Error al limpiar datos: {e}")
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        from version import get_full_version_string
        about_text = f"""📊 Sistema de Observaciones de Máquinas
        
🏷️ Versión: {get_full_version_string()}
👤 Usuario: {self.user_name}
🎭 Rol: {self.get_role_display_name(self.user_role)}
💾 Base de datos: SQLite

© 2024 - Sistema de Gestión Industrial"""
        messagebox.showinfo("Acerca de", about_text)
    
    def show_help(self):
        """Muestra ayuda del sistema"""
        help_text = """📖 Manual de Usuario
        
🔹 Crear observación: Botón 'Nueva Observación'
🔹 Filtrar datos: Usar los campos de filtro
🔹 Exportar: Menú Archivo > Exportar a Excel
🔹 Estadísticas: Menú Ver > Estadísticas

💡 Tip: Usa Ctrl+F para búsqueda rápida"""
        messagebox.showinfo("Ayuda", help_text)
'''
        
        # Buscar el lugar donde insertar (después de show_user_profile)
        pattern = r'(def show_user_profile\(self\):.*?messagebox\.showinfo\("Perfil de Usuario", profile_info\))'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # Insertar después de show_user_profile
            insertion_point = match.end()
            new_content = content[:insertion_point] + method_to_add + content[insertion_point:]
            
            # Escribir archivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Método setup_menu() y métodos relacionados agregados exitosamente")
            print(f"📝 Archivo modificado: {file_path}")
            return True
        else:
            print("❌ Error: No se encontró el método show_user_profile para insertar después")
            return False
            
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Agregando método setup_menu y métodos de menú a MainWindow...")
    success = add_setup_menu_method()
    
    if success:
        print("\n🎉 ¡Proceso completado! Los métodos de menú han sido agregados.")
        print("\n📋 Métodos agregados:")
        print("   • setup_menu() - Configura la barra de menú")
        print("   • export_to_excel() - Exportación a Excel")
        print("   • refresh_data() - Actualizar datos")
        print("   • show_statistics() - Mostrar estadísticas")
        print("   • clear_all_data() - Limpiar todos los datos")
        print("   • show_about() - Información de la app")
        print("   • show_help() - Manual de usuario")
    else:
        print("\n❌ El proceso falló. Revisa los errores anteriores.")