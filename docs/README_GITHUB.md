# 🏭 Programa de Observación de Máquinas

> Sistema completo para el registro y filtrado de observaciones de máquinas industriales con interfaz gráfica en Python.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![Excel](https://img.shields.io/badge/Data-Excel-orange.svg)](https://openpyxl.readthedocs.io/)
[![Version](https://img.shields.io/badge/Version-1.3.8-red.svg)](./version.py)

## 📋 Descripción

Programa desarrollado para el registro sistemático de observaciones en máquinas industriales, con capacidades avanzadas de filtrado por períodos y organización por líneas de producción.

### ✨ Características Principales

- 🖥️ **Interfaz Gráfica Intuitiva** - Desarrollada con Tkinter
- 📊 **Gestión de Datos Excel** - Organización automática por fechas
- 🔍 **Sistema de Filtrado Avanzado** - Por períodos y fechas personalizadas
- 🏭 **Organización por Líneas** - Filtrado automático de máquinas por línea
- 📅 **Múltiples Períodos** - Día actual, semana, 15 días, mes, personalizado
- 🔄 **Sistema de Versiones Centralizado** - Control de versiones integrado
- ✅ **Validación de Datos** - Controles de integridad automáticos

## 🚀 Instalación y Uso

### Prerrequisitos

- Python 3.8 o superior
- Windows (probado en Windows 10/11)

### Instalación Rápida

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/koeenjidev29/observacion-maquinas.git
   cd observacion-maquinas
   ```

2. **Instalación automática**
   ```bash
   # Instala Python, dependencias y ejecuta el programa
   scripts\instalar_y_ejecutar.bat
   ```

### Uso Diario

```bash
# Ejecutar el programa
ejecutar.bat

# Ejecutar pruebas
pruebas.bat
```

## 📁 Estructura del Proyecto

```
Programa observación/
├── 📄 ejecutar.bat          # ⚡ Acceso rápido al programa
├── 📄 pruebas.bat           # 🧪 Acceso rápido a las pruebas
├── 📄 main.py               # 🎯 Archivo principal
├── 📄 version.py            # 🏷️ Control de versiones
├── 📄 requirements.txt      # 📦 Dependencias Python
│
├── 📂 docs/                 # 📚 Documentación completa
├── 📂 scripts/              # 🔧 Scripts de ejecución
├── 📂 gui/                  # 🖥️ Interfaz gráfica
├── 📂 excel/                # 📊 Manejo de Excel
├── 📂 utils/                # 🛠️ Utilidades
└── 📂 data/                 # 💾 Datos y plantillas
```

## 🎯 Funcionalidades

### Sistema de Filtrado (v1.3)

- **Filtros Rápidos**: Día actual, 1 semana, 15 días, 1 mes
- **Filtro Personalizado**: Selección de rango de fechas específico
- **Información Contextual**: Descripción del período y contador de observaciones
- **Tabla Expandida**: Columnas de Fecha, Línea, Máquina, Observación y Usuario

### Organización por Líneas

- **Líneas Predefinidas**: L1, L2, L3, L4, L5, L6
- **Filtrado Automático**: Las máquinas se filtran según la línea seleccionada
- **Validación**: Control de coherencia entre línea y máquina

### Gestión de Datos

- **Excel Automático**: Creación automática de pestañas por fecha
- **Formato Consistente**: Estructura estandarizada de datos
- **Backup Automático**: Respaldo de datos antes de modificaciones

## 🔧 Desarrollo

### Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje principal
- **Tkinter** - Interfaz gráfica
- **openpyxl** - Manejo de archivos Excel
- **datetime** - Manejo de fechas y períodos

### Arquitectura

```
🏗️ Arquitectura Modular
├── GUI Layer (gui/)
├── Business Logic (utils/)
├── Data Layer (excel/)
└── Configuration (version.py)
```

### Scripts de Desarrollo

```bash
# Ejecutar pruebas completas
python test_programa.py

# Pruebas básicas
python test_simple.py

# Crear plantilla Excel
python data/crear_plantilla.py
```

## 📚 Documentación

Documentación completa disponible en la carpeta [`docs/`](docs/):

- **[README.md](docs/README.md)** - Documentación técnica completa
- **[INSTALACION.md](docs/INSTALACION.md)** - Guía de instalación detallada
- **[SISTEMA_VERSIONES.md](docs/SISTEMA_VERSIONES.md)** - Control de versiones
- **[CAMBIOS_VERSION_1.3.md](docs/CAMBIOS_VERSION_1.3.md)** - Últimas funcionalidades

## 🔄 Historial de Versiones

### v1.3.0 (2024-12-20) - Sistema de Filtrado por Períodos
- ✅ Filtrado avanzado por períodos
- ✅ Filtros personalizados
- ✅ Tabla expandida con más información
- ✅ Interfaz mejorada

### v1.2.0 - Sistema de Líneas y Máquinas
- ✅ Organización por líneas de producción
- ✅ Filtrado automático de máquinas
- ✅ Validaciones mejoradas

### v1.1.0 - Funcionalidades Base
- ✅ Interfaz gráfica completa
- ✅ Gestión de Excel automática
- ✅ Sistema de validaciones

## 🤝 Contribución

### Cómo Contribuir

1. Fork del proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código

- **PEP 8** - Estilo de código Python
- **Documentación** - Comentarios en español
- **Pruebas** - Incluir pruebas para nuevas funcionalidades
- **Versionado** - Actualizar `version.py` para cambios

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**koeenji dev**
- Versión actual: 1.3.8
- Fecha: 2024-12-20

## 🆘 Soporte

### Problemas Comunes

1. **Python no encontrado**: Ejecutar `scripts\instalar_y_ejecutar.bat`
2. **Error de Excel**: Verificar que el archivo no esté abierto
3. **Problemas de interfaz**: Verificar resolución de pantalla

### Reportar Problemas

Crear un [Issue](https://github.com/koeenjidev29/observacion-maquinas/issues) con:
- Descripción del problema
- Pasos para reproducir
- Versión del programa
- Sistema operativo

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐