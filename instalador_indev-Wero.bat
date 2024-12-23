@echo off
:: Obtener el nombre del usuario
set user=%USERNAME%
color d

echo.
echo [Hola, %user%! Preparando el entorno para ti...]
timeout /t 2 > nul

:: Secuencia de inicializacion falsa
echo [Iniciando secuencia de inicializacion...]
timeout /t 2 > nul

echo [Estableciendo modulos bsicos...]
python -m venv venv
timeout /t 2 > nul

echo [Cargando subsistemas...]
timeout /t 1 > nul

:: Activación del entorno virtual
echo [Iniciando protocolo de activación...]
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    source venv/bin/activate
)
timeout /t 2 > nul

echo [Analizando dependencias criticas...]
timeout /t 2 > nul

:: Actualización de pip
echo [Optimizando componentes para %user%...]
python -m pip install --upgrade pip
timeout /t 3 > nul

echo [Verificación de datos completada...]
timeout /t 1 > nul

:: Instalación de dependencias
echo [Cargando librerías esenciales...]
for /f "tokens=*" %%i in (package_PA_Clone.txt) do (
    python -m pip install %%i
)
timeout /t 3 > nul

color 5

echo [Sincronización finalizada.]
timeout /t 1 > nul

echo [Preparativos completos, %user%. Ejecutando el juego...]
timeout /t 2 > nul
@echo off
echo #########################################################
timeout /t 1 > nul
echo "                      /\_/\                            "
echo "                     ( o.o )                           "
echo "                      > ^ <                            "
echo #########################################################
timeout /t 2 > nul
:: Ejecutar el juego
python game.py

pause
