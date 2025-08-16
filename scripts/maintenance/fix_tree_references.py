#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir las referencias incorrectas de self.tree a self.observations_tree
"""

import os
import sys
from file_modifier import FileModifier

def fix_tree_references():
    """Corrige las referencias incorrectas de self.tree"""
    
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
        
        # Lista de reemplazos a realizar
        replacements = [
            ("self.tree.get_children()", "self.observations_tree.get_children()"),
            ("self.tree.delete(item)", "self.observations_tree.delete(item)"),
            ("self.tree.insert(", "self.observations_tree.insert("),
            ("len(self.tree.get_children())", "len(self.observations_tree.get_children())")
        ]
        
        changes_made = 0
        
        # Realizar todos los reemplazos
        for old_text, new_text in replacements:
            if modifier.replace_text(old_text, new_text):
                changes_made += 1
                print(f"✅ Reemplazado: {old_text} → {new_text}")
        
        if changes_made > 0:
            print(f"\n✅ Se realizaron {changes_made} correcciones exitosamente")
            return True
        else:
            print("⚠️ No se encontraron referencias a corregir")
            return False
            
    except Exception as e:
        print(f"❌ Error al corregir el archivo: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Corrigiendo referencias de TreeView en main_window.py...")
    
    if fix_tree_references():
        print("\n✅ ¡Corrección completada!")
        print("\n📋 Resumen:")
        print("   • Se corrigieron todas las referencias self.tree → self.observations_tree")
        print("   • El TreeView ahora usa el nombre correcto del atributo")
        print("   • Se corrigieron métodos: get_children(), delete(), insert()")
        print("\n🚀 Ahora puedes ejecutar: py main.py")
    else:
        print("\n❌ No se pudo completar la corrección")
        print("   Revisa los mensajes de error anteriores")