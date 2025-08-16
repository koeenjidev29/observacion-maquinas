#!/usr/bin/env python3
"""
Script ejecutable para migrar de Excel a SQLite
Ejecuta la migración completa de datos
"""

import os
import sys
from database.migration import MigrationManager

def main():
    print("🚀 MIGRACIÓN DE EXCEL A SQLITE")
    print("=" * 40)
    
    # Rutas por defecto
    excel_path = "data/observaciones.xlsx"
    db_path = "data/observaciones.db"
    
    # Verificar que existe el archivo Excel
    if not os.path.exists(excel_path):
        print(f"❌ Error: No se encontró el archivo Excel en {excel_path}")
        print("   Asegúrate de que el archivo existe antes de ejecutar la migración.")
        input("\nPresiona Enter para salir...")
        return False
    
    # Confirmar migración
    print(f"📁 Archivo Excel: {excel_path}")
    print(f"🗄️  Base de datos SQLite: {db_path}")
    print()
    
    confirm = input("¿Deseas continuar con la migración? (s/N): ").lower().strip()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Migración cancelada por el usuario.")
        input("\nPresiona Enter para salir...")
        return False
    
    # Ejecutar migración
    try:
        migration = MigrationManager(excel_path, db_path)
        success = migration.run_full_migration()
        
        if success:
            print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
            print("\n📋 Próximos pasos:")
            print("   1. La aplicación ahora usará SQLite automáticamente")
            print("   2. Tus datos Excel están respaldados")
            print("   3. Puedes ejecutar la aplicación normalmente")
            print("\n✅ El sistema está listo para usar.")
        else:
            print("\n⚠️  Migración completada con advertencias.")
            print("   Revisa los mensajes anteriores para más detalles.")
        
        input("\nPresiona Enter para salir...")
        return success
        
    except Exception as e:
        print(f"\n💥 Error durante la migración: {e}")
        print("\n🔧 Posibles soluciones:")
        print("   1. Verifica que el archivo Excel no esté abierto")
        print("   2. Asegúrate de tener permisos de escritura")
        print("   3. Verifica que el archivo Excel no esté corrupto")
        
        input("\nPresiona Enter para salir...")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)