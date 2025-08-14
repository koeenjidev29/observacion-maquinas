#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa de Observación de Máquinas

Este programa permite registrar observaciones de máquinas por fecha,
creando automáticamente pestañas en Excel organizadas por fecha.

Autor: KoeenjiDEV
Versión: 1.3.8
Fecha: 2024
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.main_window import MainWindow
    from version import get_full_version_string
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrese de que todas las dependencias estén instaladas.")
    print("Ejecute: pip install -r requirements.txt")
    sys.exit(1)

def check_dependencies():
    """Verifica que las dependencias necesarias estén instaladas"""
    required_modules = ['openpyxl', 'tkinter']
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'tkinter':
                import tkinter
            else:
                __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"Faltan las siguientes dependencias: {', '.join(missing_modules)}\n"
        error_msg += "Por favor, instale las dependencias ejecutando:\n"
        error_msg += "pip install -r requirements.txt"
        
        # Mostrar error en ventana si tkinter está disponible
        try:
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            messagebox.showerror("Dependencias Faltantes", error_msg)
            root.destroy()
        except:
            print(error_msg)
        
        return False
    
    return True

def create_data_directory():
    """Crea el directorio de datos si no existe"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Directorio de datos creado: {data_dir}")

def main():
    """Función principal del programa"""
    print("=" * 50)
    print(get_full_version_string())
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        return 1
    
    # Crear directorio de datos
    create_data_directory()
    
    try:
        # Inicializar y ejecutar la aplicación
        print("Iniciando aplicación...")
        app = MainWindow()
        app.run()
        print("Aplicación cerrada correctamente.")
        return 0
        
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario.")
        return 0
        
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(error_msg)
        
        # Mostrar error en ventana si es posible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", error_msg)
            root.destroy()
        except:
            pass
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)