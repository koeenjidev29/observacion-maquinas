#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar el archivo version.txt con la versión actual del version.py
"""

import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from version import get_version_string

def update_version_txt():
    """Actualiza el archivo version.txt con la versión actual"""
    try:
        # Obtener la versión actual
        current_version = get_version_string()
        
        # Ruta del archivo version.txt
        version_txt_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'version.txt'
        )
        
        # Escribir la versión al archivo
        with open(version_txt_path, 'w', encoding='utf-8') as f:
            f.write(current_version)
        
        print(f"✅ Archivo version.txt actualizado con la versión: {current_version}")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar version.txt: {str(e)}")
        return False

if __name__ == "__main__":
    update_version_txt()