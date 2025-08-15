# -*- coding: utf-8 -*-
"""
Sistema de Versiones - Observación de Máquinas
Autor: koeenji dev
"""

import datetime

# Información de versión
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 8
VERSION_BUILD = 4  # Rediseño corporativo completo

# Versión completa
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}.{VERSION_BUILD}"

# Información adicional
VERSION_NAME = "Rediseño Corporativo COPY VALLS"
RELEASE_DATE = "2024-12-20"
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
    """
    Retorna la versión como string simple
    """
    return VERSION

def get_full_version_string():
    """
    Retorna la versión completa con nombre
    """
    return f"{VERSION_NAME} v{VERSION} ({RELEASE_DATE})"

def get_development_info():
    """
    Información para desarrolladores
    """
    return {
        'version': VERSION,
        'build_date': RELEASE_DATE,
        'author': AUTHOR,
        'python_version': '3.8+'
    }

# Variable de compatibilidad
__version__ = VERSION

if __name__ == "__main__":
    print(f"Versión: {get_full_version_string()}")
    print(f"Información completa: {get_version_info()}")