# Documentación Técnica - Programa de Observación de Máquinas

## Arquitectura del Sistema

### Visión General
El programa está diseñado con una arquitectura modular que separa la lógica de negocio, la interfaz de usuario y la gestión de datos.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GUI Layer     │    │  Business Logic │    │   Data Layer    │
│  (main_window)  │◄──►│   (helpers)     │◄──►│ (excel_manager) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes Principales

#### 1. Capa de Interfaz (GUI)
- **Archivo**: `gui/main_window.py`
- **Responsabilidad**: Interfaz gráfica de usuario con tkinter
- **Funciones principales**:
  - Captura de datos del usuario
  - Visualización de observaciones
  - Validación de entrada
  - Gestión de eventos

#### 2. Capa de Lógica de Negocio (Utils)
- **Archivo**: `utils/helpers.py`
- **Responsabilidad**: Funciones auxiliares y validaciones
- **Funciones principales**:
  - Validación de datos
  - Formateo de fechas
  - Gestión de máquinas por defecto
  - Utilidades generales

#### 3. Capa de Datos (Excel)
- **Archivo**: `excel/excel_manager.py`
- **Responsabilidad**: Gestión de archivos Excel
- **Funciones principales**:
  - Creación y gestión de pestañas por fecha
  - Escritura y lectura de observaciones
  - Formateo de celdas
  - Gestión de archivos

## Flujo de Datos

### 1. Flujo de Creación de Observación
```
Usuario ingresa datos → Validación (GUI) → Validación (Utils) → 
Guardado (ExcelManager) → Actualización de vista → Confirmación
```

### 2. Flujo de Carga de Observaciones
```
Selección de fecha → Consulta (ExcelManager) → Formateo (Utils) → 
Visualización (GUI)
```

## Estructura de Archivos Excel

### Organización por Pestañas
- **Nombre de pestaña**: Formato `DD-MM-YYYY` (ej: "14-08-2025")
- **Creación automática**: Se crea una nueva pestaña por cada fecha única
- **Estructura de columnas**:
  - A: Hora (HH:MM:SS)
  - B: Máquina
  - C: Observación
  - D: Usuario

### Formato de Celdas
- **Encabezados**: Fondo azul (#366092), texto blanco, negrita
- **Datos**: Texto negro, alineación izquierda, ajuste de texto
- **Anchos de columna**: Optimizados para contenido

## Clases Principales

### ExcelManager
```python
class ExcelManager:
    def __init__(self, excel_path)
    def load_or_create_workbook()
    def create_date_sheet(date)
    def add_observation(date, machine, observation, user)
    def get_observations_by_date(date)
    def save_workbook()
```

**Métodos clave**:
- `create_date_sheet()`: Crea nueva pestaña con formato
- `add_observation()`: Añade observación a la pestaña correspondiente
- `get_observations_by_date()`: Recupera observaciones de una fecha

### MainWindow
```python
class MainWindow:
    def __init__()
    def setup_ui()
    def save_observation()
    def load_observations()
    def clear_fields()
```

**Métodos clave**:
- `setup_ui()`: Configura la interfaz gráfica
- `save_observation()`: Procesa y guarda nueva observación
- `load_observations()`: Carga y muestra observaciones

## Validaciones Implementadas

### Validación de Observaciones
- **Longitud mínima**: 3 caracteres
- **Longitud máxima**: 500 caracteres
- **Contenido**: No puede estar vacía

### Validación de Máquinas
- **Existencia**: Debe estar en la lista predefinida
- **Selección**: Debe seleccionar una máquina

### Validación de Fechas
- **Formato**: YYYY-MM-DD
- **Validez**: Debe ser una fecha válida

## Gestión de Errores

### Tipos de Errores Manejados
1. **Errores de archivo**: Permisos, archivo bloqueado
2. **Errores de validación**: Datos inválidos
3. **Errores de importación**: Módulos faltantes
4. **Errores de interfaz**: Problemas con tkinter

### Estrategias de Manejo
- **Mensajes informativos**: Uso de messagebox para errores de usuario
- **Logging**: Registro de errores técnicos
- **Recuperación**: Intentos de recuperación automática
- **Fallbacks**: Opciones alternativas cuando es posible

## Configuración y Personalización

### Máquinas Predefinidas
Las máquinas se definen en `utils/helpers.py` en la función `get_default_machines()`:

```python
def get_default_machines():
    return [
        "Máquina A - Producción",
        "Máquina B - Ensamblaje",
        # ... más máquinas
    ]
```

### Rutas de Archivos
- **Archivo principal**: `data/observaciones.xlsx`
- **Plantilla**: `data/plantilla_maquinas.xlsx`
- **Configuración**: Definida en `ExcelManager.__init__()`

### Estilos de Interfaz
- **Tema**: 'clam' de ttk
- **Colores**: Azul corporativo (#366092)
- **Fuentes**: Arial para títulos, sistema para contenido

## Extensibilidad

### Añadir Nuevas Máquinas
1. Modificar `get_default_machines()` en `utils/helpers.py`
2. Reiniciar la aplicación

### Añadir Nuevos Campos
1. Modificar `create_date_sheet()` en `excel_manager.py`
2. Actualizar `add_observation()` y `get_observations_by_date()`
3. Modificar la interfaz en `main_window.py`

### Cambiar Formato de Fecha
1. Modificar `get_sheet_name_from_date()` en `excel_manager.py`
2. Actualizar funciones de validación en `helpers.py`

## Rendimiento

### Optimizaciones Implementadas
- **Carga lazy**: Solo se cargan observaciones cuando se necesitan
- **Caché de workbook**: Se mantiene el archivo Excel abierto
- **Validación temprana**: Se validan datos antes de procesamiento
- **Límites de visualización**: Se truncan observaciones largas en la tabla

### Limitaciones Conocidas
- **Archivos grandes**: Rendimiento puede degradarse con muchas observaciones
- **Concurrencia**: No soporta múltiples usuarios simultáneos
- **Memoria**: Mantiene todo el workbook en memoria

## Seguridad

### Medidas Implementadas
- **Validación de entrada**: Previene inyección de datos maliciosos
- **Manejo seguro de archivos**: Verificación de permisos
- **Sanitización**: Limpieza de datos de entrada

### Consideraciones
- **Backup**: Se recomienda backup regular del archivo Excel
- **Permisos**: Verificar permisos de escritura en directorio data/
- **Acceso**: Control de acceso a nivel de sistema operativo

## Mantenimiento

### Tareas Regulares
1. **Backup de datos**: Copiar `data/observaciones.xlsx`
2. **Limpieza de logs**: Si se implementa logging
3. **Actualización de dependencias**: `pip install -U -r requirements.txt`

### Monitoreo
- **Tamaño de archivo**: Vigilar crecimiento del archivo Excel
- **Rendimiento**: Tiempo de carga de observaciones
- **Errores**: Frecuencia de errores de usuario

## Troubleshooting

### Problemas Comunes

1. **"No se puede abrir el archivo Excel"**
   - Verificar que el archivo no esté abierto en Excel
   - Comprobar permisos de escritura
   - Verificar espacio en disco

2. **"Error al importar módulos"**
   - Ejecutar `pip install -r requirements.txt`
   - Verificar instalación de Python
   - Comprobar PATH de Python

3. **"La interfaz no responde"**
   - Cerrar y reiniciar la aplicación
   - Verificar recursos del sistema
   - Comprobar integridad del archivo Excel

### Logs y Debugging
Para habilitar debugging, modificar `main.py` para incluir:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```