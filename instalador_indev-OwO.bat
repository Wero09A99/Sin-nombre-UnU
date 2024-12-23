@echo off
:: Obtener el nombre del usuario
set user=%USERNAME%
color d

echo.
echo [\033[0;32mPA_recreate by Wero09Anano UwU\033[0m]
echo.
echo [\033[1;33mHola, %user%! Preparando el entorno para ti...\033[0m]
timeout /t 2 > nul

:: Secuencia de inicializacion falsa
echo [\033[1;34m[PA_Recreate]: Iniciando secuencia de inicializacion...\033[0m]
timeout /t 2 > nul

echo [\033[1;35m[PA_Recreate]: Estableciendo modulos basicos...\033[0m]
python -m venv venv
timeout /t 2 > nul

echo [\033[1;36m[PA_Recreate]: Cargando subsistemas...\033[0m]
timeout /t 1 > nul

:: Activacion del entorno virtual
echo [\033[1;33m[PA_Recreate]: Iniciando protocolo de activacion...\033[0m]
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    source venv/bin/activate
)
timeout /t 2 > nul

echo [\033[1;34m[PA_Recreate]: Analizando dependencias criticas...\033[0m]
timeout /t 2 > nul

:: Actualizacion de pip
echo [\033[1;35m[PA_Recreate]: Optimizando componentes para %user%...\033[0m]
python -m pip install --upgrade pip
timeout /t 3 > nul

echo [\033[1;36m[PA_Recreate]: Verificacion de datos completada...\033[0m]
timeout /t 1 > nul

:: Instalacion de dependencias
echo [\033[1;33m[PA_Recreate]: Cargando librerias esenciales...\033[0m]
for /f "tokens=*" %%i in (package_PA_Clone.txt) do (
    python -m pip install %%i
)
timeout /t 3 > nul

color 5

echo [\033[1;32m[PA_Recreate]: Sincronizacion finalizada.\033[0m]
timeout /t 1 > nul

echo [\033[1;34m[PA_Recreate]: Preparativos completos, %user%. Ejecutando el juego...\033[0m]
timeout /t 2 > nul

:: Ejecutar el juego
python game.py

pause
