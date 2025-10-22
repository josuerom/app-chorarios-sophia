@echo off
title Generador de ejecutable
echo ===============================================
echo     Creando entorno y ejecutable .EXE
echo ===============================================
echo.

REM 1. Eliminar restos anteriores
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del app.spec 2>nul

REM 2. Instalar dependencias necesarias
echo Instalando dependencias...
pip install -r requirements.txt >nul 2>&1
echo Dependencias instaladas.

REM 3. Generar ejecutable con icono y sin consola
echo Empaquetando aplicacion con PyInstaller...
pyinstaller --onefile --noconsole ^
--icon=static/icono.ico ^
--add-data "src;src" ^
--add-data "static;static" ^
app.py

REM 4. Limpiar archivos temporales
echo Limpiando temporales...
rmdir /s /q build 2>nul
del app.spec 2>nul


REM 5. Ejecución del programa resultante
dist\app.exe

echo.
echo === Compilacion finalizada exitosamente ===
echo El archivo ejecutable se encuentra en: dist\app.exe