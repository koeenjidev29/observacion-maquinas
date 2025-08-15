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
VERSION_BUILD = 2  # 🆕 ACTUALIZADO: Nueva versión incremental

# Versión completa
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}.{VERSION_BUILD}"

# Información adicional
VERSION_NAME = "Sistema de Temas Moderno y Perfil Clicable"  # 🆕 ACTUALIZADO
RELEASE_DATE = "2024-12-20"  # 🆕 ACTUALIZADO
AUTHOR = "koeenji dev"

def get_version_info():
    """
    Retorna un diccionario con toda la información de versión
    """
    return {
        'version': VERSION,
        'version_name': VERSION_NAME,
        'release_date': RELEASE_DATE,
        'author': AUTHOR,
        'major': VERSION_MAJOR,
        'minor': VERSION_MINOR,
        'patch': VERSION_PATCH,
        'build': VERSION_BUILD
    }

def get_version_string():
    """Retorna solo el número de versión"""
    return VERSION

def get_full_version_string():
    """Retorna la versión completa con nombre"""
    return f"{VERSION} - {VERSION_NAME}"

__version__ = VERSION