@echo off
title Simulador del Conectoma Cerebral Humano 3D
echo ======================================================================
echo   INICIANDO CONECTOMA CEREBRAL HUMANO 3D - REDES NEURONALES
echo ======================================================================
echo Verificando entorno Python...
python --version
if errorlevel 1 (
    echo [!] Python no detectado en el PATH. Abriendo version estatica en navegador...
    start frontend\index.html
    pause
    exit /b
)

echo Iniciando servidor Python con simulacion en tiempo real...
python backend\run_server.py
pause
