#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir referencias a excel_manager en main_window.py
"""

import re

def fix_excel_references():
    file_path = 'gui/main_window.py'
    
    # Leer el archivo
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazos específicos
    replacements = [
        (r'self\.excel_manager\.close_workbook\(\)', 'self.db_manager.close()'),
        (r'self\.excel_manager\.get_next_id\(\)', 'self.db_manager.get_next_id()'),
        (r'self\.excel_manager\.get_all_observations_with_id\(\)', 'self.db_manager.get_all_observations_with_id()'),
        (r'self\.excel_manager\.get_observations_by_date\(([^)]+)\)', r'self.db_manager.get_observations_by_date(\1)'),
        (r'self\.excel_manager\.clear_all_observations\(\)', 'self.db_manager.clear_all_observations()'),
        (r'self\.excel_manager\.excel_path', 'self.db_manager.db_path'),
        (r'self\.excel_manager\.open_excel_file\(\)', 'True  # Database always available'),
        (r'f"📊 Total de observaciones: \{self\.excel_manager\.get_next_id\(\) - 1\}"', 
         'f"📊 Total de observaciones: {self.db_manager.get_statistics().get(\'total_observaciones\', 0)}"'),
        (r'f"📁 Archivo Excel: \{self\.excel_manager\.excel_path\}"',
         'f"📁 Base de datos: {self.db_manager.db_path}"')
    ]
    
    # Aplicar reemplazos
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Escribir el archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Referencias a excel_manager corregidas exitosamente")

if __name__ == "__main__":
    fix_excel_references()