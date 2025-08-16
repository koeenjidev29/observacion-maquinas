#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar métodos faltantes al DatabaseManager
"""

import os
import sys

def add_missing_methods():
    """Agrega los métodos get_all_observations y search_observations al DatabaseManager"""
    
    # Corregir la ruta relativa
    database_manager_path = "../../database/database_manager.py"
    
    if not os.path.exists(database_manager_path):
        print(f"❌ Error: No se encontró {database_manager_path}")
        return False
    
    # Leer archivo actual
    with open(database_manager_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Métodos a agregar
    new_methods = '''
    def get_all_observations(self) -> List[Dict[str, Any]]:
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
    
    def search_observations(self, search_term: str) -> List[Dict[str, Any]]:
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
    from datetime import datetime
    
    print("🔧 Agregando métodos faltantes al DatabaseManager...")
    
    if add_missing_methods():
        print("\n🎉 ¡Corrección completada!")
        print("\n📋 Métodos agregados:")
        print("   • get_all_observations()")
        print("   • search_observations(search_term)")
        print("\n✨ Ahora la lista de observaciones debería funcionar correctamente.")
    else:
        print("\n❌ Error en la corrección")