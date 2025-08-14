#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que el programa funcione correctamente
"""

import sys
import os
from datetime import datetime

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from version import get_full_version_string
except ImportError:
    def get_full_version_string():
        return "Programa de Observación de Máquinas (versión no disponible)"

def test_imports():
    """Prueba que todos los módulos se puedan importar"""
    print("Probando importaciones...")
    
    try:
        import tkinter
        print("✅ tkinter - OK")
    except ImportError as e:
        print(f"❌ tkinter - ERROR: {e}")
        return False
    
    try:
        import openpyxl
        print("✅ openpyxl - OK")
    except ImportError as e:
        print(f"❌ openpyxl - ERROR: {e}")
        return False
    
    try:
        from excel.excel_manager import ExcelManager
        print("✅ ExcelManager - OK")
    except ImportError as e:
        print(f"❌ ExcelManager - ERROR: {e}")
        return False
    
    try:
        from utils.helpers import get_default_machines
        print("✅ helpers - OK")
    except ImportError as e:
        print(f"❌ helpers - ERROR: {e}")
        return False
    
    return True

def test_excel_functionality():
    """Prueba la funcionalidad básica de Excel"""
    print("\nProbando funcionalidad de Excel...")
    
    try:
        from excel.excel_manager import ExcelManager
        
        # Crear gestor de Excel de prueba
        test_file = "data/test_observaciones.xlsx"
        excel_manager = ExcelManager(test_file)
        
        # Probar crear pestaña
        today = datetime.now().strftime("%Y-%m-%d")
        excel_manager.create_date_sheet(today)
        print("✅ Creación de pestaña - OK")
        
        # Probar añadir observación
        excel_manager.add_observation(
            today, 
            "Máquina A - Producción", 
            "Prueba de observación automática", 
            "Sistema"
        )
        print("✅ Añadir observación - OK")
        
        # Probar leer observaciones
        observations = excel_manager.get_observations_by_date(today)
        if len(observations) > 0:
            print("✅ Leer observaciones - OK")
        else:
            print("❌ Leer observaciones - ERROR: No se encontraron observaciones")
            return False
        
        excel_manager.close()
        
        # Limpiar archivo de prueba
        if os.path.exists(test_file):
            os.remove(test_file)
            print("✅ Limpieza de archivos de prueba - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de Excel: {e}")
        return False

def test_utilities():
    """Prueba las funciones de utilidades"""
    print("\nProbando utilidades...")
    
    try:
        from utils.helpers import (
            get_default_machines, validate_observation, 
            validate_machine, get_today_date
        )
        
        # Probar obtener máquinas
        machines = get_default_machines()
        if len(machines) > 0:
            print(f"✅ Máquinas por defecto - OK ({len(machines)} máquinas)")
        else:
            print("❌ Máquinas por defecto - ERROR: Lista vacía")
            return False
        
        # Probar validación de observación
        valid, msg = validate_observation("Esta es una observación de prueba")
        if valid:
            print("✅ Validación de observación - OK")
        else:
            print(f"❌ Validación de observación - ERROR: {msg}")
            return False
        
        # Probar validación de máquina
        valid, msg = validate_machine(machines[0], machines)
        if valid:
            print("✅ Validación de máquina - OK")
        else:
            print(f"❌ Validación de máquina - ERROR: {msg}")
            return False
        
        # Probar fecha de hoy
        today = get_today_date()
        if today:
            print(f"✅ Fecha de hoy - OK ({today})")
        else:
            print("❌ Fecha de hoy - ERROR")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de utilidades: {e}")
        return False

def test_directories():
    """Prueba que los directorios necesarios existan"""
    print("\nProbando estructura de directorios...")
    
    required_dirs = ['gui', 'excel', 'utils', 'data']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"✅ Directorio {dir_name} - OK")
        else:
            print(f"❌ Directorio {dir_name} - ERROR: No existe")
            return False
    
    return True

def main():
    """Función principal de prueba"""
    print("=" * 60)
    print("PRUEBA DEL PROGRAMA DE OBSERVACIÓN DE MÁQUINAS")
    print(get_full_version_string())
    print("=" * 60)
    
    all_tests_passed = True
    
    # Ejecutar pruebas
    tests = [
        ("Estructura de directorios", test_directories),
        ("Importaciones", test_imports),
        ("Utilidades", test_utilities),
        ("Funcionalidad Excel", test_excel_functionality)
    ]
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if not test_func():
            all_tests_passed = False
            print(f"❌ FALLÓ: {test_name}")
        else:
            print(f"✅ PASÓ: {test_name}")
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 TODAS LAS PRUEBAS PASARON - El programa está listo para usar")
        print("\nPuede ejecutar el programa con: python main.py")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON - Revisar errores arriba")
        print("\nConsulte INSTALACION.md para solucionar problemas")
    print("=" * 60)
    
    return 0 if all_tests_passed else 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPresione Enter para continuar...")
    sys.exit(exit_code)