# 📋 Sistema de Versiones Centralizado

## Descripción

El programa ahora cuenta con un **sistema de versiones centralizado** que permite cambiar la versión en toda la aplicación modificando únicamente un archivo.

## 🎯 Archivo Principal: `version.py`

Todo el control de versiones se maneja desde el archivo `version.py`. Este archivo contiene:

```python
# Información de versión principal
VERSION_MAJOR = 1    # Versión principal (cambios importantes)
VERSION_MINOR = 2    # Versión menor (nuevas características)
VERSION_PATCH = 1    # Parche (correcciones de errores)

# Información adicional
VERSION_NAME = "Sistema de Versiones Centralizado"  # Nombre descriptivo
RELEASE_DATE = "2024-12-19"  # Fecha de lanzamiento
AUTHOR = "Sistema de Observación"  # Autor
```

## 🔄 Cómo Cambiar la Versión

### Paso 1: Abrir el archivo
Abrir `version.py` en cualquier editor de texto.

### Paso 2: Modificar los valores
```python
# Para una nueva versión mayor (ej: 2.0.0)
VERSION_MAJOR = 2
VERSION_MINOR = 0
VERSION_PATCH = 0
VERSION_NAME = "Nueva Versión Mayor"
RELEASE_DATE = "2024-12-20"

# Para una nueva característica (ej: 1.3.0)
VERSION_MAJOR = 1
VERSION_MINOR = 3
VERSION_PATCH = 0
VERSION_NAME = "Nueva Característica"

# Para una corrección (ej: 1.2.2)
VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 2
VERSION_NAME = "Corrección de Errores"
```

### Paso 3: Guardar el archivo
Guardar `version.py` y ¡listo!

## 📍 Dónde se Muestra la Versión

La versión se actualiza automáticamente en:

### 1. **Ventana Principal**
- Título de la ventana: `"Programa de Observación de Máquinas v1.2.1 - Sistema de Versiones Centralizado (2024-12-19)"`
- Encabezado de la interfaz: `"v1.2.1 - Sistema de Versiones Centralizado"`

### 2. **Consola de Inicio**
- Mensaje al ejecutar `main.py`
- Información completa de versión

### 3. **Sistema de Pruebas**
- Encabezado de `test_programa.py`
- Información de versión en las pruebas

### 4. **Archivos Batch**
- Los archivos `.bat` ejecutan el programa que muestra la versión

## 🛠️ Funciones Disponibles

El archivo `version.py` proporciona varias funciones útiles:

```python
# Obtener solo el número de versión
get_version_info()  # Retorna diccionario completo

# Obtener versión formateada
get_version_string()  # "v1.2.1 - Sistema de Versiones Centralizado"

# Obtener versión completa
get_full_version_string()  # "Programa de Observación... v1.2.1 - ... (2024-12-19)"

# Acceso directo
__version__  # "1.2.1"
```

## 📝 Ejemplos Prácticos

### Ejemplo 1: Actualizar a versión 2.0.0
```python
VERSION_MAJOR = 2
VERSION_MINOR = 0
VERSION_PATCH = 0
VERSION_NAME = "Interfaz Renovada"
RELEASE_DATE = "2024-12-25"
```

### Ejemplo 2: Corrección menor 1.2.2
```python
VERSION_MAJOR = 1
VERSION_MINOR = 2
VERSION_PATCH = 2
VERSION_NAME = "Corrección de Bugs"
RELEASE_DATE = "2024-12-20"
```

### Ejemplo 3: Nueva característica 1.3.0
```python
VERSION_MAJOR = 1
VERSION_MINOR = 3
VERSION_PATCH = 0
VERSION_NAME = "Exportar a PDF"
RELEASE_DATE = "2024-12-30"
```

## ✅ Ventajas del Sistema

1. **Centralizado**: Un solo archivo controla toda la versión
2. **Automático**: Se actualiza en toda la aplicación
3. **Consistente**: No hay discrepancias entre diferentes partes
4. **Fácil**: Solo modificar un archivo
5. **Completo**: Incluye nombre, fecha y autor
6. **Flexible**: Múltiples formatos de visualización

## 🔍 Verificación

Para verificar que la versión se actualizó correctamente:

1. **Ejecutar el programa**: `ejecutar_programa.bat`
2. **Ejecutar pruebas**: `ejecutar_pruebas.bat`
3. **Verificar la interfaz**: La versión aparece en el título y encabezado
4. **Revisar la consola**: Mensajes de inicio muestran la nueva versión

---

**¡Ahora cambiar la versión del programa es tan fácil como editar una línea!** 🎉