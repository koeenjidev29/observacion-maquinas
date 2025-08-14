# Inicio Rápido - Programa de Observación de Máquinas

## Ejecución Inmediata (Windows)

### Opción 1: Automática (Recomendada)
1. **Doble clic** en `instalar_y_ejecutar.bat`
2. El script automáticamente:
   - Verificará Python
   - Instalará dependencias
   - Ejecutará el programa

### Opción 2: Manual
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar programa
python main.py
```

## 📋 Uso del Programa

### Pasos Básicos
1. **Seleccionar fecha** (por defecto: hoy)
2. **Elegir máquina** de la lista desplegable
3. **Escribir observación** en el área de texto
4. **Hacer clic en "Guardar Observación"**

### Funciones Principales
- ✅ **Crear observaciones** por fecha y máquina
- ✅ **Ver observaciones** del día seleccionado
- ✅ **Pestañas automáticas** por fecha en Excel
- ✅ **Búsqueda por fecha** con botón "Hoy"
- ✅ **Validación automática** de datos

##  Archivos Generados

- `data/observaciones.xlsx` - Archivo principal con todas las observaciones
- Pestañas por fecha (formato: DD-MM-YYYY)

##  Solución Rápida de Problemas

### ❌ "No se encontró Python"
**Solución**: Instalar Python desde Microsoft Store o python.org

### ❌ "No module named 'openpyxl'"
**Solución**: `pip install openpyxl`

### ❌ El programa no inicia
**Solución**: Ejecutar `python test_programa.py` para diagnóstico

## Verificar Instalación

```bash
# Ejecutar pruebas automáticas
python test_programa.py
```

##  Documentación Completa

- `README.md` - Descripción general del proyecto
- `INSTALACION.md` - Guía detallada de instalación
- `DOCUMENTACION_TECNICA.md` - Documentación técnica completa

## Máquinas Predefinidas

- Máquina A - Producción
- Máquina B - Ensamblaje  
- Máquina C - Empaque
- Máquina D - Control Calidad
- Máquina E - Mantenimiento
- Máquina F - Logística
- Máquina G - Almacén
- Máquina H - Transporte

## 💡 Consejos de Uso

1. **Backup regular**: Copie `data/observaciones.xlsx` periódicamente
2. **Observaciones claras**: Sea específico en las observaciones
3. **Fechas correctas**: Verifique la fecha antes de guardar
4. **Cierre Excel**: No abra el archivo Excel mientras usa el programa

## 🆘 Soporte

Si tiene problemas:
1. Consulte `INSTALACION.md`
2. Ejecute `test_programa.py`
3. Revise `DOCUMENTACION_TECNICA.md`

---

**¡Listo para usar!** 🎉

Ejecute `instalar_y_ejecutar.bat` y comience a registrar observaciones.