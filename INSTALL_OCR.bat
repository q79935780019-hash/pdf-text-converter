@echo off
chcp 65001 > nul
color 0A
title PDF Text Converter - Установка зависимостей OCR

echo.
echo ============================================================
echo       УСТАНОВКА ЗАВИСИМОСТЕЙ ДЛЯ OCR (TESSERACT И POPPLER)
echo ============================================================
echo.
echo Эти программы нужны для распознавания текста
echo.

REM Проверка администратора
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Требуются права администратора!
    echo.
    echo Запустите этот файл ПРАВОЙ КНОПКОЙ мыши и выберите:
    echo "Запустить от имени администратора"
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ЭТАП 1: УСТАНОВКА TESSERACT OCR
echo ============================================================
echo.
echo Сейчас откроется браузер для скачивания Tesseract
echo.
echo ЧТО ДЕЛАТЬ:
echo 1. Найдите файл tesseract-ocr-w64-setup-v5.x.exe
echo 2. Скачайте его
echo 3. Запустите установщик
echo 4. При установке - просто нажимайте "Next" → "Install"
echo 5. Запомните путь установки (обычно C:\Program Files\Tesseract-OCR)
echo.
echo Нажмите Enter для открытия браузера...
pause

start https://github.com/UB-Mannheim/tesseract/wiki

echo.
echo Ждем 5 секунд...
timeout /t 5

echo.
echo ============================================================
echo ЭТАП 2: УСТАНОВКА POPPLER
echo ============================================================
echo.
echo Сейчас откроется браузер для скачивания Poppler
echo.
echo ЧТО ДЕЛАТЬ:
echo 1. Найдите "Release" (последнюю версию)
echo 2. Скачайте архив Release-ХХ (windows версию)
echo 3. Распакуйте архив
echo 4. Скопируйте папку poppler в C:\Program Files\poppler
echo    (должна быть: C:\Program Files\poppler\bin и другие папки)
echo.
echo Нажмите Enter для открытия браузера...
pause

start https://github.com/oschwartz10612/poppler-windows/releases/

echo.
echo ============================================================
echo ПРОВЕРКА УСТАНОВКИ
echo ============================================================
echo.
echo После установки Tesseract и Poppler проверьте:
echo.
echo 1. Откройте File Explorer (Пуск → Этот компьютер)
echo 2. В адресной строке напишите: C:\Program Files\Tesseract-OCR
echo    - Должна существовать папка с файлом tesseract.exe
echo.
echo 3. В адресной строке напишите: C:\Program Files\poppler
echo    - Должны быть папки: bin, include, lib и т.д.
echo.
echo Если оба пути существуют - ВСЁ ПРАВИЛЬНО!
echo.
echo Нажмите Enter для завершения...
pause

echo.
echo ГОТОВО!
echo.
echo Теперь запустите файл BUILD_EXE.bat чтобы создать приложение!
echo.
pause
