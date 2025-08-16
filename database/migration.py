"""
Script de migración de Excel a SQLite
Importa todos los datos existentes del archivo Excel a la nueva base de datos
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from excel.excel_manager import ExcelManager
from database.database_manager import DatabaseManager

class MigrationManager:
    """Gestor de migración de Excel a SQLite"""
    
    def __init__(self, excel_path: str, db_path: str = "data/observaciones.db"):
        self.excel_path = excel_path
        self.db_path = db_path
        self.excel_manager = None
        self.db_manager = None
        
    def initialize_managers(self):
        """Inicializa los gestores de Excel y base de datos"""
        try:
            # Verificar que el archivo Excel existe
            if not os.path.exists(self.excel_path):
                raise FileNotFoundError(f"Archivo Excel no encontrado: {self.excel_path}")
            
            self.excel_manager = ExcelManager(self.excel_path)
            self.db_manager = DatabaseManager(self.db_path)
            
            print(f"✓ Gestores inicializados correctamente")
            print(f"  - Excel: {self.excel_path}")
            print(f"  - SQLite: {self.db_path}")
            
        except Exception as e:
            print(f"✗ Error inicializando gestores: {e}")
            raise
    
    def create_backup(self):
        """Crea backup del archivo Excel antes de la migración"""
        try:
            backup_path = f"{self.excel_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            import shutil
            shutil.copy2(self.excel_path, backup_path)
            
            print(f"✓ Backup creado: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"✗ Error creando backup: {e}")
            raise
    
    def migrate_observations(self) -> Dict[str, Any]:
        """Migra todas las observaciones de Excel a SQLite"""
        try:
            print("\n🔄 Iniciando migración de observaciones...")
            
            # Obtener todas las observaciones del Excel
            excel_observations = self.excel_manager.get_all_observations_with_id()
            
            if not excel_observations:
                print("⚠️  No se encontraron observaciones en Excel")
                return {'migrated': 0, 'errors': 0, 'skipped': 0}
            
            print(f"📊 Encontradas {len(excel_observations)} observaciones en Excel")
            
            migrated = 0
            errors = 0
            skipped = 0
            
            for i, obs in enumerate(excel_observations, 1):
                try:
                    # Validar datos requeridos
                    if not all([obs.get('Fecha'), obs.get('Máquina'), 
                               obs.get('Observación'), obs.get('Usuario')]):
                        print(f"⚠️  Observación {i} incompleta, saltando...")
                        skipped += 1
                        continue
                    
                    # Convertir formato de fecha si es necesario
                    fecha = self._normalize_date(obs['Fecha'])
                    hora = obs.get('Hora', '00:00')
                    
                    # Migrar observación
                    success = self.db_manager.save_observation(
                        fecha=fecha,
                        hora=hora,
                        linea=obs.get('Línea', ''),
                        maquina=obs['Máquina'],
                        observacion=obs['Observación'],
                        usuario=obs['Usuario']
                    )
                    
                    if success:
                        migrated += 1
                        if migrated % 50 == 0:
                            print(f"  📝 Migradas {migrated} observaciones...")
                    else:
                        errors += 1
                        print(f"✗ Error migrando observación {i}")
                        
                except Exception as e:
                    errors += 1
                    print(f"✗ Error procesando observación {i}: {e}")
            
            result = {
                'total_found': len(excel_observations),
                'migrated': migrated,
                'errors': errors,
                'skipped': skipped
            }
            
            print(f"\n✅ Migración completada:")
            print(f"  - Total encontradas: {result['total_found']}")
            print(f"  - Migradas exitosamente: {result['migrated']}")
            print(f"  - Errores: {result['errors']}")
            print(f"  - Saltadas: {result['skipped']}")
            
            return result
            
        except Exception as e:
            print(f"✗ Error durante migración: {e}")
            raise
    
    def _normalize_date(self, date_str: str) -> str:
        """Normaliza formato de fecha"""
        try:
            # Si ya está en formato correcto
            if isinstance(date_str, str) and len(date_str) == 10:
                # Convertir de dd-mm-yyyy a dd/mm/yyyy si es necesario
                if '-' in date_str:
                    return date_str.replace('-', '/')
                return date_str
            
            # Si es datetime, convertir a string
            if hasattr(date_str, 'strftime'):
                return date_str.strftime('%d/%m/%Y')
            
            return str(date_str)
            
        except Exception:
            return str(date_str)
    
    def verify_migration(self) -> bool:
        """Verifica que la migración fue exitosa"""
        try:
            print("\n🔍 Verificando migración...")
            
            # Contar observaciones en Excel
            excel_count = len(self.excel_manager.get_all_observations_with_id())
            
            # Contar observaciones en SQLite
            sqlite_count = len(self.db_manager.get_all_observations_with_id())
            
            print(f"📊 Observaciones en Excel: {excel_count}")
            print(f"📊 Observaciones en SQLite: {sqlite_count}")
            
            if sqlite_count >= excel_count:
                print("✅ Verificación exitosa: Todos los datos migrados")
                return True
            else:
                print(f"⚠️  Advertencia: Faltan {excel_count - sqlite_count} observaciones")
                return False
                
        except Exception as e:
            print(f"✗ Error verificando migración: {e}")
            return False
    
    def run_full_migration(self) -> bool:
        """Ejecuta migración completa con verificación"""
        try:
            print("🚀 Iniciando migración completa de Excel a SQLite")
            print("=" * 50)
            
            # 1. Inicializar gestores
            self.initialize_managers()
            
            # 2. Crear backup
            backup_path = self.create_backup()
            
            # 3. Migrar observaciones
            result = self.migrate_observations()
            
            # 4. Verificar migración
            verification_ok = self.verify_migration()
            
            # 5. Mostrar resumen final
            print("\n" + "=" * 50)
            print("📋 RESUMEN DE MIGRACIÓN")
            print("=" * 50)
            print(f"✓ Backup creado: {backup_path}")
            print(f"✓ Observaciones migradas: {result['migrated']}")
            print(f"✓ Errores: {result['errors']}")
            print(f"✓ Verificación: {'✅ OK' if verification_ok else '⚠️  Con advertencias'}")
            print(f"✓ Base de datos: {self.db_path}")
            
            if result['migrated'] > 0 and verification_ok:
                print("\n🎉 ¡Migración completada exitosamente!")
                print("   Ahora puedes usar el nuevo sistema con SQLite")
                return True
            else:
                print("\n⚠️  Migración completada con advertencias")
                return False
                
        except Exception as e:
            print(f"\n💥 Error durante migración completa: {e}")
            return False
        
        finally:
            # Limpiar recursos
            if self.excel_manager:
                self.excel_manager.close()
            if self.db_manager:
                self.db_manager.close()

def main():
    """Función principal para ejecutar migración"""
    # Rutas por defecto
    excel_path = "data/observaciones.xlsx"
    db_path = "data/observaciones.db"
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
    if len(sys.argv) > 2:
        db_path = sys.argv[2]
    
    # Ejecutar migración
    migration = MigrationManager(excel_path, db_path)
    success = migration.run_full_migration()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()