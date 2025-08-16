"""
Módulo de Base de Datos para Sistema de Observaciones
Versión 2.0 - Migración de Excel a SQLite
"""

from .database_manager import DatabaseManager
from .models import ObservacionModel, UsuarioModel, ConfiguracionModel
from .migration import MigrationManager

__version__ = "2.0.0"
__author__ = "Copy Valls Team"

# Exportar clases principales
__all__ = [
    'DatabaseManager',
    'ObservacionModel', 
    'UsuarioModel',
    'ConfiguracionModel',
    'MigrationManager'
]