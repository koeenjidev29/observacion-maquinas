"""
DatabaseManager - Reemplaza ExcelManager para usar SQLite
Maneja todas las operaciones de base de datos para observaciones
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from .models import ObservacionModel, UsuarioModel, ConfiguracionModel

class DatabaseManager:
    """Gestor principal de la base de datos SQLite"""
    
    def __init__(self, db_path: str = "data/observaciones.db"):
        self.db_path = db_path
        self.ensure_database_exists()
        
        # Inicializar modelos
        self.observacion_model = ObservacionModel(db_path)
        self.usuario_model = UsuarioModel(db_path)
        self.configuracion_model = ConfiguracionModel(db_path)
        
        # Crear tablas si no existen
        self.initialize_database()
    
    def ensure_database_exists(self):
        """Asegura que el directorio y archivo de base de datos existan"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def initialize_database(self):
        """Inicializa la base de datos creando todas las tablas"""
        try:
            self.observacion_model.create_table()
            self.usuario_model.create_table()
            self.configuracion_model.create_table()
            
            # Insertar configuración inicial si no existe
            self._insert_initial_config()
            
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
            raise
    
    def _insert_initial_config(self):
        """Inserta configuración inicial"""
        initial_configs = [
            ('app_version', '2.0.0', 'Versión de la aplicación'),
            ('backup_enabled', 'true', 'Backup automático habilitado'),
            ('backup_interval_days', '7', 'Intervalo de backup en días'),
            ('max_observations_per_page', '100', 'Máximo de observaciones por página')
        ]
        
        for clave, valor, descripcion in initial_configs:
            if not self.configuracion_model.get_config(clave):
                self.configuracion_model.set_config(clave, valor, descripcion)
    
    # Métodos compatibles con ExcelManager
    
    def save_observation(self, fecha: str, hora: str, linea: str, maquina: str, 
                        observacion: str, usuario: str) -> bool:
        """Guarda una nueva observación (compatible con ExcelManager)"""
        try:
            # Extraer subcategoría de la observación si existe
            subcategoria = self._extract_subcategory(observacion)
            
            observation_id = self.observacion_model.insert(
                fecha=fecha,
                hora=hora,
                linea=linea,
                maquina=maquina,
                observacion=observacion,
                usuario=usuario,
                subcategoria=subcategoria
            )
            
            return observation_id > 0
            
        except Exception as e:
            print(f"Error guardando observación: {e}")
            return False
    
    def _extract_subcategory(self, observacion: str) -> str:
        """Extrae subcategoría de la observación (similar a ExcelManager)"""
        # Buscar patrones como [Subcategoría] al inicio
        if observacion.startswith('[') and ']' in observacion:
            end_bracket = observacion.find(']')
            return observacion[1:end_bracket]
        return 'General'
    
    def get_all_observations_with_id(self) -> List[Dict[str, Any]]:
        """Obtiene todas las observaciones con ID (compatible con ExcelManager)"""
        try:
            observations = self.observacion_model.get_all()
            
            # Convertir a formato compatible con ExcelManager
            result = []
            for obs in observations:
                result.append({
                    'ID': obs['id'],
                    'Fecha': obs['fecha'],
                    'Hora': obs['hora'],
                    'Línea': obs['linea'] or '',
                    'Máquina': obs['maquina'],
                    'Observación': obs['observacion'],
                    'Usuario': obs['usuario'],
                    'Subcategoría': obs['subcategoria']
                })
            
            return result
            
        except Exception as e:
            print(f"Error obteniendo observaciones: {e}")
            return []
    
    def get_observations_by_filters(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtiene observaciones filtradas"""
        try:
            observations = self.observacion_model.get_filtered(filters)
            
            # Convertir a formato compatible
            result = []
            for obs in observations:
                result.append({
                    'ID': obs['id'],
                    'Fecha': obs['fecha'],
                    'Hora': obs['hora'],
                    'Línea': obs['linea'] or '',
                    'Máquina': obs['maquina'],
                    'Observación': obs['observacion'],
                    'Usuario': obs['usuario'],
                    'Subcategoría': obs['subcategoria']
                })
            
            return result
            
        except Exception as e:
            print(f"Error filtrando observaciones: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de observaciones"""
        try:
            return self.observacion_model.get_statistics()
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
    
    def get_machines(self) -> List[str]:
        """Obtiene lista única de máquinas"""
        try:
            with self.observacion_model.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT DISTINCT maquina FROM observaciones ORDER BY maquina"
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo máquinas: {e}")
            return []
    
    def get_users(self) -> List[str]:
        """Obtiene lista única de usuarios"""
        try:
            with self.observacion_model.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT DISTINCT usuario FROM observaciones ORDER BY usuario"
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error obteniendo usuarios: {e}")
            return []
    
    def backup_to_excel(self, excel_path: str) -> bool:
        """Exporta datos a Excel como backup"""
        try:
            import pandas as pd
            
            observations = self.get_all_observations_with_id()
            if not observations:
                return False
            
            df = pd.DataFrame(observations)
            df.to_excel(excel_path, index=False, sheet_name='Observaciones')
            
            return True
            
        except Exception as e:
            print(f"Error creando backup Excel: {e}")
            return False
    
    def get_next_id(self) -> int:
        """Obtiene el siguiente ID disponible (compatible con ExcelManager)"""
        try:
            with self.observacion_model.get_connection() as conn:
                cursor = conn.execute("SELECT MAX(id) FROM observaciones")
                max_id = cursor.fetchone()[0]
                return (max_id or 0) + 1
        except Exception as e:
            print(f"Error obteniendo siguiente ID: {e}")
            return 1
    
    def close(self):
        """Cierra conexiones (para compatibilidad)"""
        # SQLite se cierra automáticamente, pero mantenemos el método
        pass
    
    # Métodos adicionales específicos de SQLite
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL personalizada"""
        try:
            with self.observacion_model.get_connection() as conn:
                cursor = conn.execute(query, params)
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            return []
    
    def get_database_info(self) -> Dict[str, Any]:
        """Obtiene información de la base de datos"""
        try:
            with self.observacion_model.get_connection() as conn:
                # Información de tablas
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                tables = [row[0] for row in cursor.fetchall()]
                
                # Tamaño de archivo
                db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
                
                # Conteo de observaciones
                cursor = conn.execute("SELECT COUNT(*) FROM observaciones")
                total_observations = cursor.fetchone()[0]
                
                return {
                    'database_path': self.db_path,
                    'database_size_bytes': db_size,
                    'database_size_mb': round(db_size / (1024 * 1024), 2),
                    'tables': tables,
                    'total_observations': total_observations,
                    'created_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"Error obteniendo información de BD: {e}")
            return {}