#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir la referencia incorrecta al método de DatabaseManager
"""

import os
import sys
from file_modifier import FileModifier

def fix_database_method():
    """Corrige la referencia incorrecta get_observations_by_date"""
    
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
        
        # Texto problemático
        old_text = '''            # Usar DatabaseManager para obtener observaciones por fecha
            observations = self.db_manager.get_observations_by_date(today)'''
        
        # Texto corregido
        new_text = '''            # Usar DatabaseManager para obtener observaciones por fecha
            observations = self.db_manager.get_observations_by_filters({'fecha': today})'''
        
        # Realizar el reemplazo
        if modifier.replace_text(old_text, new_text):
            print("✅ Método de base de datos corregido exitosamente")
            print("📝 Se cambió get_observations_by_date por get_observations_by_filters")
            return True
        else:
            print("⚠️ Intentando método alternativo...")
            
            # Método alternativo: solo reemplazar la línea del método
            old_line = "            observations = self.db_manager.get_observations_by_date(today)"
            new_line = "            observations = self.db_manager.get_observations_by_filters({'fecha': today})"
            
            if modifier.replace_text(old_line, new_line):
                print("✅ Método corregido con método alternativo")
                return True
            else:
                print("❌ No se pudo encontrar la línea a corregir")
                return False
            
    except Exception as e:
        print(f"❌ Error al corregir el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Corrigiendo método de DatabaseManager en main_window.py...")
    
    if fix_database_method():
        print("\n✅ ¡Corrección completada!")
        print("\n📋 Resumen:")
        print("   • Se corrigió get_observations_by_date() → get_observations_by_filters()")
        print("   • Se agregó el filtro de fecha como parámetro: {'fecha': today}")
        print("   • El método ahora es compatible con DatabaseManager")
        print("\n🚀 Ahora puedes ejecutar: py main.py")
    else:
        print("\n❌ No se pudo completar la corrección")
        print("   Revisa los mensajes de error anteriores")