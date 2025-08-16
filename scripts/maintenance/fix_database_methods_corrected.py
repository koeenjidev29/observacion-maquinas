#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar métodos faltantes al DatabaseManager
"""

import os
import sys
from datetime import datetime

def add_missing_methods():
    """Agrega los métodos get_all_observations y search_observations al DatabaseManager"""
    
    # Obtener la ruta absoluta del directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    database_manager_path = os.path.join(project_root, 'database', 'database_manager.py')
    
    # Normalizar la ruta
    database_manager_path = os.path.normpath(database_manager_path)
    
    print(f"🔍 Buscando archivo en: {database_manager_path}")
    
    if not os.path.exists(database_manager_path):
        print(f"❌ Error: No se encontró {database_manager_path}")
        return False
    
    # Leer archivo actual
    with open(database_manager_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si los métodos ya existen
    if 'def get_all_observations(self)' in content:
        print("ℹ️  El método get_all_observations ya existe")
        return True
    
    # Métodos a agregar
    new_methods = '''
    def get_all_observations(self):
        """Obtiene todas las observaciones en formato compatible con main_window"""
        try:
            observations = self.observacion_model.get_all()
            
            # Convertir a formato esperado por main_window
            result = []
            for obs in observations:
                result.append({
                    'id': obs['id'],
                    'fecha': obs['fecha'],
                    'hora': obs['hora'],
                    'linea': obs['linea'] or '',
                    'maquina': obs['maquina'],
                    'operador': obs['usuario'],  # Mapear usuario a operador
                    'observacion': obs['observacion'],
                    'accion_tomada': obs.get('accion_tomada', ''),  # Campo nuevo
                    'estado': obs.get('estado', 'Pendiente')  # Campo nuevo
                })
            
            return result
            
        except Exception as e:
            print(f"Error obteniendo observaciones: {e}")
            return []
    
    def search_observations(self, search_term: str):
        """Busca observaciones por término"""
        try:
            if not search_term.strip():
                return self.get_all_observations()
            
            # Buscar en múltiples campos
            with self.observacion_model.get_connection() as conn:
                query = """
                    SELECT * FROM observaciones 
                    WHERE observacion LIKE ? 
                       OR maquina LIKE ? 
                       OR usuario LIKE ?
                       OR linea LIKE ?
                    ORDER BY fecha DESC, hora DESC
                """
                
                search_pattern = f"%{search_term}%"
                cursor = conn.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
                
                columns = [description[0] for description in cursor.description]
                observations = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                # Convertir a formato esperado
                result = []
                for obs in observations:
                    result.append({
                        'id': obs['id'],
                        'fecha': obs['fecha'],
                        'hora': obs['hora'],
                        'linea': obs['linea'] or '',
                        'maquina': obs['maquina'],
                        'operador': obs['usuario'],
                        'observacion': obs['observacion'],
                        'accion_tomada': obs.get('accion_tomada', ''),
                        'estado': obs.get('estado', 'Pendiente')
                    })
                
                return result
                
        except Exception as e:
            print(f"Error buscando observaciones: {e}")
            return []
'''
    
    # Buscar donde insertar los métodos (antes del último método)
    insertion_point = content.rfind('    def get_database_info(self)')
    
    if insertion_point == -1:
        # Si no encuentra get_database_info, buscar otro punto de inserción
        insertion_point = content.rfind('class DatabaseManager')
        if insertion_point != -1:
            # Buscar el final de la clase
            class_end = content.find('\n\n', insertion_point)
            if class_end == -1:
                insertion_point = len(content) - 1
            else:
                insertion_point = class_end
        else:
            print("❌ Error: No se encontró punto de inserción")
            return False
    
    # Insertar los nuevos métodos
    new_content = content[:insertion_point] + new_methods + "\n" + content[insertion_point:]
    
    # Crear backup
    backup_path = f"{database_manager_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Escribir archivo actualizado
    with open(database_manager_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Métodos agregados exitosamente al DatabaseManager")
    print(f"📁 Backup creado: {backup_path}")
    return True

if __name__ == "__main__":
    print("🔧 Agregando métodos faltantes al DatabaseManager...")
    
    if add_missing_methods():
        print("\n🎉 ¡Corrección completada!")
        print("\n📋 Métodos agregados:")
        print("   • get_all_observations()")
        print("   • search_observations(search_term)")
        print("\n✨ Ahora la lista de observaciones debería funcionar correctamente.")
    else:
        print("\n❌ Error en la corrección")