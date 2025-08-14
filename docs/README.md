# Programa de Observación de Máquinas

Este programa permite registrar y gestionar observaciones de máquinas industriales de manera eficiente y organizada.

## 📋 Gestión de Versiones

La versión del programa se gestiona centralizadamente desde el archivo `version.py`. Para cambiar la versión en todo el programa:

1. **Abrir el archivo `version.py`**
2. **Modificar las variables de versión:**
   ```python
   VERSION_MAJOR = 1    # Versión principal
   VERSION_MINOR = 2    # Versión menor
   VERSION_PATCH = 0    # Parche/corrección
   VERSION_NAME = "Nombre de la versión"
   RELEASE_DATE = "YYYY-MM-DD"
   ```
3. **Guardar el archivo**

¡La versión se actualizará automáticamente en toda la aplicación!

### Dónde se muestra la versión:
- Título de la ventana principal
- Encabezado de la interfaz
- Mensajes de inicio del programa
- Pruebas del sistema
- Documentación

## Descripción
Programa con interfaz gráfica (GUI) desarrollado en Python para gestionar observaciones de máquinas en archivos Excel. Permite registrar observaciones por fecha y máquina, creando automáticamente nuevas pestañas por fecha cuando sea necesario.

## Características
- **Interfaz gráfica intuitiva** con tkinter
- **Gestión automática de fechas** - crea pestañas nuevas por fecha
- **Plantilla de máquinas** predefinida
- **Registro de observaciones** por máquina y fecha
- **Integración con Excel** usando openpyxl

## Estructura del Proyecto
```
Programa observación/
├── README.md
├── requirements.txt
├── main.py
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── excel/
│   ├── __init__.py
│   └── excel_manager.py
├── data/
│   ├── plantilla_maquinas.xlsx
│   └── observaciones.xlsx
└── utils/
    ├── __init__.py
    └── helpers.py
```

## Instalación
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar el programa:
   ```bash
   python main.py
   ```

## Uso

### Registro de Observaciones
1. Seleccionar la fecha deseada
2. Elegir la línea de producción
3. Seleccionar la máquina de la lista filtrada
4. Introducir la observación
5. Guardar - el programa creará automáticamente la pestaña de fecha si no existe

### Sistema de Filtrado (v1.3)
1. **Filtros Rápidos**: Seleccionar entre "Día actual", "1 semana", "15 días", "1 mes"
2. **Filtro Personalizado**: Elegir rango de fechas específico
3. **Aplicar Filtro**: Ver observaciones del período seleccionado
4. **Información Contextual**: Descripción del rango y contador de observaciones

## Tecnologías
- **Python 3.8+**
- **tkinter** - Interfaz gráfica
- **openpyxl** - Manipulación de archivos Excel
- **datetime** - Gestión de fechas