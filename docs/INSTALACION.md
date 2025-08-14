# Guía de Instalación - Programa de Observación de Máquinas

## Requisitos Previos

### 1. Instalar Python
El programa requiere Python 3.8 o superior.

**Opción A: Desde Microsoft Store (Recomendado para Windows)**
1. Abrir Microsoft Store
2. Buscar "Python 3.11" o "Python 3.12"
3. Instalar la versión más reciente

**Opción B: Desde python.org**
1. Ir a https://www.python.org/downloads/
2. Descargar Python 3.11 o superior
3. Durante la instalación, **MARCAR** "Add Python to PATH"
4. Completar la instalación

### 2. Verificar la Instalación
Abrir PowerShell o Command Prompt y ejecutar:
```bash
python --version
```
Debe mostrar algo como: `Python 3.11.x`

## Instalación del Programa

### 1. Instalar Dependencias
En la carpeta del programa, ejecutar:
```bash
pip install -r requirements.txt
```

### 2. Crear Plantilla de Máquinas (Opcional)
Si desea crear la plantilla de Excel con datos de ejemplo:
```bash
python data\crear_plantilla.py
```

### 3. Ejecutar el Programa
```bash
python main.py
```

## Solución de Problemas

### Error: "no se encontró Python"
- Reinstalar Python marcando "Add Python to PATH"
- Reiniciar el sistema después de la instalación
- Usar `py` en lugar de `python`:
  ```bash
  py --version
  py main.py
  ```

### Error: "No module named 'openpyxl'"
- Ejecutar: `pip install openpyxl`
- O instalar todas las dependencias: `pip install -r requirements.txt`

### Error: "No module named 'tkinter'"
- En Windows: tkinter viene incluido con Python
- En Linux: `sudo apt-get install python3-tk`
- En macOS: tkinter viene incluido

### El programa no inicia
1. Verificar que Python esté instalado: `python --version`
2. Verificar dependencias: `pip list`
3. Ejecutar desde la carpeta del programa
4. Revisar permisos de escritura en la carpeta `data/`

## Estructura de Archivos

Después de la instalación, la estructura debe ser:
```
Programa observación/
├── README.md
├── INSTALACION.md
├── requirements.txt
├── main.py
├── gui/
│   ├── __init__.py
│   └── main_window.py
├── excel/
│   ├── __init__.py
│   └── excel_manager.py
├── data/
│   ├── crear_plantilla.py
│   ├── plantilla_maquinas.xlsx (se crea al ejecutar crear_plantilla.py)
│   └── observaciones.xlsx (se crea automáticamente)
└── utils/
    ├── __init__.py
    └── helpers.py
```

## Uso del Programa

1. **Ejecutar**: `python main.py`
2. **Seleccionar fecha**: Use el campo de fecha o el botón "Hoy"
3. **Elegir máquina**: Seleccione de la lista desplegable
4. **Escribir observación**: Ingrese la observación en el área de texto
5. **Guardar**: Haga clic en "Guardar Observación"

El programa creará automáticamente:
- Pestañas por fecha en el archivo Excel
- El archivo `observaciones.xlsx` en la carpeta `data/`

## Contacto y Soporte

Para problemas técnicos:
1. Verificar esta guía de instalación
2. Revisar los archivos de log si existen
3. Comprobar permisos de archivos y carpetas