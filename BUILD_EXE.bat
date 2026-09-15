@echo off
chcp 65001 > nul
color 0A
title PDF Text Converter - Создание приложения

echo.
echo ============================================================
echo   PDF TEXT CONVERTER - СОЗДАНИЕ ГОТОВОГО ПРИЛОЖЕНИЯ (EXE)
echo ============================================================
echo.
echo Сейчас будет создана готовая программа для Windows!
echo Это займет 2-3 минуты...
echo.

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не установлен!
    echo.
    echo Сначала установите Python с https://www.python.org/
    echo (выберите опцию "Add Python to PATH")
    echo.
    pause
    exit /b 1
)

echo [1/3] Установка PyInstaller...
pip install -q pyinstaller

echo [2/3] Установка всех нужных библиотек...
pip install -q -r requirements.txt

echo [3/3] Создание приложения...
python create_exe.py

echo.
echo ============================================================
echo ГОТОВО!
echo ============================================================
echo.
echo Программа находится здесь: dist\PDFTextConverter.exe
echo.
echo Теперь вы можете:
echo - Запустить PDFTextConverter.exe (двойной клик)
echo - Скопировать .exe куда угодно на компьютер
echo - Создать ярлык на рабочем столе
echo.
echo Программа работает БЕЗ Python и БЕЗ установки!
echo.
pause