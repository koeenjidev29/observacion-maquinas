#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple para verificar que Python funciona correctamente
"""

import sys
import os
from datetime import datetime

print("="*50)
print("    TEST SIMPLE DE PYTHON")
print("="*50)
print()

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Current time: {datetime.now()}")
print()

# Test de importación de tkinter
try:
    import tkinter as tk
    print("✓ tkinter importado correctamente")
except ImportError as e:
    print(f"✗ Error importando tkinter: {e}")

# Test de importación de openpyxl
try:
    import openpyxl
    print(f"✓ openpyxl importado correctamente (version: {openpyxl.__version__})")
except ImportError as e:
    print(f"✗ Error importando openpyxl: {e}")

print()
print("Test completado exitosamente!")
print("Python está funcionando correctamente.")
print()
input("Presiona Enter para continuar...")