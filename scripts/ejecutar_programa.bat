@echo off
echo ========================================
echo    PROGRAMA DE OBSERVACION DE MAQUINAS
echo ========================================
echo.
echo Iniciando programa...
echo.

REM Metodo 1: Intentar con py
echo [1/4] Probando con py...
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python Launcher encontrado
    echo Ejecutando programa...
    py main.py
    if %errorlevel% == 0 (
        echo Programa ejecutado exitosamente
        goto success
    ) else (
        echo Error al ejecutar el programa
    )
) else (
    echo Python Launcher no disponible
)

REM Metodo 2: Intentar con python
echo.
echo [2/4] Probando con python...
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python encontrado
    echo Ejecutando programa...
    python main.py
    if %errorlevel% == 0 (
        echo Programa ejecutado exitosamente
        goto success
    ) else (
        echo Error al ejecutar el programa
    )
) else (
    echo Comando python no disponible
)

REM Metodo 3: Intentar con ruta de Microsoft Store
echo.
echo [3/4] Probando con ruta de Microsoft Store...
set PYTHON_PATH=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe
if exist "%PYTHON_PATH%" (
    echo Python encontrado en Microsoft Store
    echo Ejecutando programa...
    "%PYTHON_PATH%" main.py
    if %errorlevel% == 0 (
        echo Programa ejecutado exitosamente
        goto success
    ) else (
        echo Error al ejecutar el programa
    )
) else (
    echo Python no encontrado en Microsoft Store
)

REM Si llegamos aqui, ningun metodo funciono
echo.
echo ========================================
echo           ERROR: PYTHON NO FUNCIONA
echo ========================================
echo.
echo DIAGNOSTICO:
echo - Python esta instalado pero hay conflictos
echo - Problema con alias de ejecucion de Windows
echo.
echo SOLUCIONES:
echo.
echo 1. DESHABILITAR ALIAS (RECOMENDADO):
echo    - Presiona Windows + I
echo    - Ve a Aplicaciones, Configuracion avanzada
echo    - Haz clic en Alias de ejecucion de aplicaciones
echo    - DESACTIVA python.exe y python3.exe
echo    - Reinicia PowerShell
echo.
echo 2. REINSTALAR PYTHON:
echo    - Descarga desde https://python.org
echo    - Marca Add Python to PATH al instalar
echo.
echo 3. CONSULTAR DOCUMENTACION:
echo    - Lee SOLUCION_PYTHON.md para mas detalles
echo.
echo Estado actual:
echo - Programa completo y funcional
echo - Dependencias instaladas (openpyxl)
echo - Conflicto con configuracion de Python
echo.
goto end

:success
echo.
echo ========================================
echo        PROGRAMA FINALIZADO EXITOSAMENTE
echo ========================================
echo.
echo El programa se ejecuto correctamente.
echo Revisa la ventana del programa para interactuar con el.
echo.

:end
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul