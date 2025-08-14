@echo off
chcp 65001 >nul
echo ========================================
echo    PRUEBAS DEL PROGRAMA DE OBSERVACION
echo ========================================
echo.
echo Ejecutando pruebas...
echo.

REM Intentar con py
echo [1/4] Probando con py...
where py >nul 2>&1
if %errorlevel% == 0 (
    echo Python Launcher encontrado
    echo Ejecutando pruebas...
    py test_programa.py
    if %errorlevel% == 0 (
        echo Pruebas ejecutadas exitosamente
        goto :success
    ) else (
        echo Error en las pruebas, pero continuando...
    )
) else (
    echo Python Launcher no encontrado
)

REM Intentar con python
echo.
echo [2/4] Probando con python...
where python >nul 2>&1
if %errorlevel% == 0 (
    echo Python encontrado
    echo Ejecutando pruebas...
    python test_programa.py
    if %errorlevel% == 0 (
        echo Pruebas ejecutadas exitosamente
        goto :success
    )
) else (
    echo Python no encontrado
)

REM Intentar con ruta completa de Microsoft Store
echo.
echo [3/4] Probando con ruta de Microsoft Store...
if exist "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" (
    echo Python de Microsoft Store encontrado
    echo Ejecutando pruebas...
    "C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\python.exe" test_programa.py
    if %errorlevel% == 0 (
        echo Pruebas ejecutadas exitosamente
        goto :success
    )
) else (
    echo Python de Microsoft Store no encontrado
)

REM Intentar con rutas comunes
echo.
echo [4/4] Probando con rutas comunes...
if exist "C:\Program Files\Python312\python.exe" (
    echo Python en Program Files encontrado
    echo Ejecutando pruebas...
    "C:\Program Files\Python312\python.exe" test_programa.py
    if %errorlevel% == 0 (
        echo Pruebas ejecutadas exitosamente
        goto :success
    )
)

if exist "C:\Python312\python.exe" (
    echo Python en C:\Python312 encontrado
    echo Ejecutando pruebas...
    "C:\Python312\python.exe" test_programa.py
    if %errorlevel% == 0 (
        echo Pruebas ejecutadas exitosamente
        goto :success
    )
)

echo.
echo ========================================
echo ERROR: No se pudo ejecutar las pruebas
echo ========================================
echo.
echo SOLUCION:
echo 1. Deshabilitar aliases de Python en Windows:
echo    - Configuracion ^> Aplicaciones ^> Configuracion avanzada
echo    - Alias de ejecucion de aplicaciones
echo    - Desactivar python.exe y python3.exe
echo.
echo 2. O reinstalar Python desde python.org
echo    - Marcar "Add Python to PATH"
echo.
goto :end

:success
echo.
echo ========================================
echo       PRUEBAS FINALIZADAS
echo ========================================
echo.
echo Las pruebas se ejecutaron correctamente.
echo Revisa los resultados arriba.
echo.

:end
echo Presiona cualquier tecla para cerrar...
pause >nul