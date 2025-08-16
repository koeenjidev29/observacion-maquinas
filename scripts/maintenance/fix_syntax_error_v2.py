#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script corregido para arreglar el error de sintaxis en main_window.py línea 391
"""

import os
import sys
from file_modifier import FileModifier

def fix_syntax_error():
    """Corrige el error de sintaxis en las líneas 391-393"""
    
    # Ruta del archivo a corregir
    file_path = os.path.join('..', '..', 'gui', 'main_window.py')
    
    if not os.path.exists(file_path):
        print(f"❌ Error: No se encontró el archivo {file_path}")
        return False
    
    try:
        # Crear instancia del modificador
        modifier = FileModifier(file_path)
        
        # Crear backup
        backup_path = modifier.create_backup()
        print(f"✅ Backup creado: {backup_path}")
        
        # Texto problemático (formato exacto como aparece en el archivo)
        old_text = '''            "¿Estás seguro de que quieres eliminar TODAS las observaciones?

⚠️ Esta acción NO se puede deshacer."'''
        
        # Texto corregido (cadena de una sola línea con escapes)
        new_text = '''            "¿Estás seguro de que quieres eliminar TODAS las observaciones?\n\n⚠️ Esta acción NO se puede deshacer."'''
        
        # Realizar el reemplazo
        if modifier.replace_text(old_text, new_text):
            print("✅ Error de sintaxis corregido exitosamente")
            print("📝 Se corrigió la cadena de texto multilínea problemática")
            return True
        else:
            print("⚠️ Intentando método alternativo...")
            
            # Método alternativo: reemplazar línea por línea
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Buscar y corregir las líneas problemáticas
            for i, line in enumerate(lines):
                if '"¿Estás seguro de que quieres eliminar TODAS las observaciones?' in line:
                    # Reemplazar las líneas 391-393 con una sola línea corregida
                    lines[i] = '            "¿Estás seguro de que quieres eliminar TODAS las observaciones?\\n\\n⚠️ Esta acción NO se puede deshacer."\n'
                    # Eliminar las líneas siguientes que forman parte del string multilínea
                    if i + 1 < len(lines) and lines[i + 1].strip() == '':
                        lines[i + 1] = ''
                    if i + 2 < len(lines) and '⚠️ Esta acción NO se puede deshacer.' in lines[i + 2]:
                        lines[i + 2] = ''
                    break
            
            # Escribir el archivo corregido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print("✅ Error de sintaxis corregido con método alternativo")
            return True
            
    except Exception as e:
        print(f"❌ Error al corregir el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Corrigiendo error de sintaxis en main_window.py (versión 2)...")
    
    if fix_syntax_error():
        print("\n✅ ¡Corrección completada!")
        print("\n📋 Resumen:")
        print("   • Se corrigió la cadena de texto multilínea problemática")
        print("   • Se convirtió a formato de una sola línea con escapes")
        print("   • El archivo debería ejecutarse sin errores de sintaxis")
        print("\n🚀 Ahora puedes ejecutar: py main.py")
    else:
        print("\n❌ No se pudo completar la corrección")
        print("   Revisa los mensajes de error anteriores")