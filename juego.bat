@echo off
:: Obtener el nombre del usuario
set user=%USERNAME%
echo. 
color d
:: Activacion del entorno virtual
echo [Iniciando protocolo de activacion...]
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    source venv/bin/activate
)
timeout /t 2 > nul
echo [Preparativos completos, %user%. Ejecutando el juego...]
timeout /t 2 > nul

echo #########################################################
timeout /t 1 > nul
echo "                      /\_/\                            "
echo "                     ( o.o )                           "
echo "                      > ^ <                            "
echo #########################################################

timeout /t 2 > nul

:: Ejecutar el juego
python menu.py

pause
