# -*- coding: utf-8 -*-
"""
Archivo de configuración de versión del Programa de Observación de Máquinas

Este archivo centraliza toda la información de versión del programa.
Para actualizar la versión, solo modifica los valores en este archivo.
"""

# Información de versión principal
VERSION_MAJOR = 1
VERSION_MINOR = 3
VERSION_PATCH = 8
VERSION_BUILD = 1  # 🆕 NUEVO: Versión incremental

# Versión completa
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}.{VERSION_BUILD}"

# Información adicional
VERSION_NAME = "Rediseño de Tablas Profesional"  # 🆕 ACTUALIZADO
RELEASE_DATE = "2024-12-20"  # 🆕 ACTUALIZADO
AUTHOR = "koeenji dev"

# Función para obtener información completa de versión
def get_version_info():
    """Retorna información completa de la versión"""
    return {
        'version': VERSION,
        'major': VERSION_MAJOR,
        'minor': VERSION_MINOR,
        'patch': VERSION_PATCH,
        'build': VERSION_BUILD,  # 🆕 NUEVO
        'name': VERSION_NAME,
        'release_date': RELEASE_DATE,
        'author': AUTHOR
    }

def get_version_string():
    """Retorna la versión como string formateado"""
    return f"v{VERSION} - {VERSION_NAME}"

def get_full_version_string():
    """Retorna la versión completa con fecha"""
    return f"Programa de Observación de Máquinas v{VERSION} - {VERSION_NAME} ({RELEASE_DATE})"

# Para compatibilidad con imports directos
__version__ = VERSION