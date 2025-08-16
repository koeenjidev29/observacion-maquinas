"""
Modelos de datos para el sistema de observaciones
Define la estructura de las tablas SQLite
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any

class BaseModel:
    """Clase base para todos los modelos"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_connection(self):
        """Obtiene conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
        return conn

class ObservacionModel(BaseModel):
    """Modelo para la tabla de observaciones"""
    
    TABLE_NAME = "observaciones"
    
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS observaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE NOT NULL,
        hora TIME NOT NULL,
        linea VARCHAR(50),
        maquina VARCHAR(100) NOT NULL,
        observacion TEXT NOT NULL,
        subcategoria VARCHAR(100) DEFAULT 'General',
        usuario VARCHAR(100) NOT NULL,
        estado VARCHAR(20) DEFAULT 'activa',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    def create_table(self):
        """Crea la tabla de observaciones"""
        with self.get_connection() as conn:
            conn.execute(self.CREATE_TABLE_SQL)
            conn.commit()
    
    def insert(self, fecha: str, hora: str, linea: str, maquina: str, 
               observacion: str, usuario: str, subcategoria: str = 'General') -> int:
        """Inserta una nueva observación"""
        sql = """
        INSERT INTO observaciones (fecha, hora, linea, maquina, observacion, subcategoria, usuario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, (fecha, hora, linea, maquina, observacion, subcategoria, usuario))
            conn.commit()
            return cursor.lastrowid
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Obtiene todas las observaciones"""
        sql = "SELECT * FROM observaciones WHERE estado = 'activa' ORDER BY id DESC"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_filtered(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Obtiene observaciones filtradas"""
        conditions = ["estado = 'activa'"]
        params = []
        
        if filters.get('id'):
            conditions.append("id = ?")
            params.append(filters['id'])
        
        if filters.get('usuario'):
            conditions.append("usuario LIKE ?")
            params.append(f"%{filters['usuario']}%")
        
        if filters.get('maquina'):
            conditions.append("maquina LIKE ?")
            params.append(f"%{filters['maquina']}%")
        
        if filters.get('fecha_desde'):
            conditions.append("fecha >= ?")
            params.append(filters['fecha_desde'])
        
        if filters.get('fecha_hasta'):
            conditions.append("fecha <= ?")
            params.append(filters['fecha_hasta'])
        
        sql = f"SELECT * FROM observaciones WHERE {' AND '.join(conditions)} ORDER BY id DESC"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de observaciones"""
        sql = """
        SELECT 
            COUNT(*) as total_observaciones,
            COUNT(DISTINCT maquina) as total_maquinas,
            COUNT(DISTINCT usuario) as total_usuarios,
            COUNT(CASE WHEN subcategoria = 'Crítica' THEN 1 END) as observaciones_criticas
        FROM observaciones 
        WHERE estado = 'activa'
        """
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql)
            return dict(cursor.fetchone())

class UsuarioModel(BaseModel):
    """Modelo para la tabla de usuarios"""
    
    TABLE_NAME = "usuarios"
    
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        rol VARCHAR(50) NOT NULL,
        activo BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    def create_table(self):
        """Crea la tabla de usuarios"""
        with self.get_connection() as conn:
            conn.execute(self.CREATE_TABLE_SQL)
            conn.commit()
    
    def insert(self, nombre: str, rol: str) -> int:
        """Inserta un nuevo usuario"""
        sql = "INSERT INTO usuarios (nombre, rol) VALUES (?, ?)"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, (nombre, rol))
            conn.commit()
            return cursor.lastrowid
    
    def get_all_active(self) -> List[Dict[str, Any]]:
        """Obtiene todos los usuarios activos"""
        sql = "SELECT * FROM usuarios WHERE activo = 1 ORDER BY nombre"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql)
            return [dict(row) for row in cursor.fetchall()]

class ConfiguracionModel(BaseModel):
    """Modelo para la tabla de configuración"""
    
    TABLE_NAME = "configuracion"
    
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS configuracion (
        clave VARCHAR(100) PRIMARY KEY,
        valor TEXT,
        descripcion TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    def create_table(self):
        """Crea la tabla de configuración"""
        with self.get_connection() as conn:
            conn.execute(self.CREATE_TABLE_SQL)
            conn.commit()
    
    def set_config(self, clave: str, valor: str, descripcion: str = None):
        """Establece un valor de configuración"""
        sql = """
        INSERT OR REPLACE INTO configuracion (clave, valor, descripcion, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """
        
        with self.get_connection() as conn:
            conn.execute(sql, (clave, valor, descripcion))
            conn.commit()
    
    def get_config(self, clave: str, default: str = None) -> Optional[str]:
        """Obtiene un valor de configuración"""
        sql = "SELECT valor FROM configuracion WHERE clave = ?"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, (clave,))
            row = cursor.fetchone()
            return row['valor'] if row else default