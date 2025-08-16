#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir el error de sintaxis en main_window.py línea 391
"""

import os
import sys
from file_modifier import FileModifier

def fix_syntax_error():
    """Corrige el error de sintaxis en la línea 391"""
    
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
        
        # Texto problemático (líneas 390-392)
        old_text = '''            "¿Estás seguro de que quieres eliminar TODAS las observaciones?

⚠️ Esta acción NO se puede deshacer."'''
        
        # Texto corregido
        new_text = '''            "¿Estás seguro de que quieres eliminar TODAS las observaciones?\n\n⚠️ Esta acción NO se puede deshacer."'''
        
        # Realizar el reemplazo
        if modifier.replace_text(old_text, new_text):
            print("✅ Error de sintaxis corregido exitosamente")
            print("📝 Se corrigió la cadena de texto no cerrada en línea 391")
            return True
        else:
            print("⚠️ No se encontró el texto a reemplazar")
            return False
            
    except Exception as e:
        print(f"❌ Error al corregir el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Corrigiendo error de sintaxis en main_window.py...")
    
    if fix_syntax_error():
        print("\n✅ ¡Corrección completada!")
        print("\n📋 Resumen:")
        print("   • Se corrigió la cadena de texto no cerrada")
        print("   • Se escaparon correctamente los caracteres de nueva línea")
        print("   • El archivo debería ejecutarse sin errores de sintaxis")
        print("\n🚀 Ahora puedes ejecutar: py main.py")
    else:
        print("\n❌ No se pudo completar la corrección")
        print("   Revisa los mensajes de error anteriores")