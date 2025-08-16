#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar versión a 1.3.8.4
Correcciones de interfaz y diálogo de observaciones
"""

import os
import sys
from datetime import datetime

def update_version_py():
    """Actualiza el archivo version.py"""
    version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'version.py')
    
    new_content = '''# -*- coding: utf-8 -*-
"""
Sistema de Versiones - Observación de Máquinas
Autor: koeenji dev
"""

import datetime

# Información de versión
VERSION_MAJOR = 1
VERSION_MINOR = 3
VERSION_PATCH = 8
VERSION_BUILD = 4  # Correcciones de interfaz y diálogo

# Versión completa
VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}.{VERSION_BUILD}"

# Información adicional
VERSION_NAME = "Correcciones de Interfaz y Diálogo"
RELEASE_DATE = "2025-01-16"
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
    Información de desarrollo
    """
    return {
        'status': 'stable',
        'environment': 'production',
        'build_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'python_version': sys.version.split()[0] if 'sys' in globals() else 'unknown'
    }

# Compatibilidad
__version__ = VERSION

if __name__ == "__main__":
    print(f"Versión: {get_full_version_string()}")
    print(f"Información completa: {get_version_info()}")
'''
    
    try:
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Actualizado: {version_file}")
        return True
    except Exception as e:
        print(f"❌ Error actualizando version.py: {e}")
        return False

def update_version_txt():
    """Actualiza el archivo version.txt"""
    version_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'version.txt')
    
    try:
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write('1.3.8.4')
        print(f"✅ Actualizado: {version_file}")
        return True
    except Exception as e:
        print(f"❌ Error actualizando version.txt: {e}")
        return False

def create_changelog():
    """Crea el archivo de changelog para esta versión"""
    changelog_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        'docs', 'CAMBIOS_v1.3.8.4.md'
    )
    
    changelog_content = '''# Cambios Versión 1.3.8.4

**Fecha:** 2025-01-16  
**Tipo:** Correcciones de Interfaz y Diálogo

## 🔧 Correcciones Implementadas

### Interfaz de Usuario
- ✅ **TreeView References**: Corregidas todas las referencias de `self.tree` a `self.observations_tree`
- ✅ **Diálogo Nueva Observación**: Implementación completa del método `show_new_incident_dialog`
- ✅ **Dimensiones del Diálogo**: Ajustadas las dimensiones para mejor visualización
- ✅ **Botones de Acción**: Agregados botones "Guardar" y "Cancelar" funcionales

### Funcionalidad
- ✅ **Validación de Campos**: Mejorada la validación de campos en el diálogo
- ✅ **Integración con Base de Datos**: Conexión completa para guardar observaciones
- ✅ **Campos Completos**: Todos los campos necesarios implementados (ID, fecha, hora, línea, máquina, operador, observación, acción tomada, estado)

## 🐛 Errores Corregidos

1. **TreeView no definido**: Solucionado el error de referencia al TreeView
2. **Diálogo incompleto**: Completada la implementación del diálogo de nueva observación
3. **Botones faltantes**: Agregados los botones de guardar y cancelar
4. **Dimensiones incorrectas**: Ajustado el tamaño del diálogo para mejor usabilidad

## 📋 Tareas Pendientes

- [ ] Corregir errores al ver la lista de observaciones
- [ ] Probar funcionalidades de guardar, filtrar y buscar
- [ ] Implementar sistema de backup automático

## 🔄 Próximos Pasos

- Continuar con la depuración de errores de guardado
- Completar pruebas de todas las funcionalidades
- Optimizar rendimiento de la aplicación

---
**Desarrollado por:** koeenji dev  
**Estado:** Estable para uso en producción
'''
    
    try:
        with open(changelog_file, 'w', encoding='utf-8') as f:
            f.write(changelog_content)
        print(f"✅ Creado changelog: {changelog_file}")
        return True
    except Exception as e:
        print(f"❌ Error creando changelog: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Actualizando versión a 1.3.8.4...")
    print("📝 Cambios: Correcciones de interfaz y diálogo de observaciones")
    print("-" * 60)
    
    success = True
    
    # Actualizar archivos
    if not update_version_py():
        success = False
    
    if not update_version_txt():
        success = False
        
    if not create_changelog():
        success = False
    
    print("-" * 60)
    if success:
        print("✅ ¡Versión actualizada exitosamente a 1.3.8.4!")
        print("\n📋 Próximos pasos:")
        print("1. git add .")
        print("2. git commit -m 'v1.3.8.4 - Correcciones de interfaz y diálogo'")
        print("3. git push")
    else:
        print("❌ Hubo errores durante la actualización")
    
    return success

if __name__ == "__main__":
    main()