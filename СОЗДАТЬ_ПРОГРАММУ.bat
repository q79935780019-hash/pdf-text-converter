@echo off
chcp 65001 > nul
title PDF Text Converter - АВТОМАТИЧЕСКОЕ СОЗДАНИЕ EXE

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║   PDF TEXT CONVERTER - СОЗДАНИЕ ГОТОВОЙ ПРОГРАММЫ        ║
echo ║                                                            ║
echo ║   Эта программа АВТОМАТИЧЕСКИ создаст файл EXE            ║
echo ║   Потом Python можно будет УДАЛИТЬ!                       ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.
echo Проверка системы...
echo.

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    cls
    color 0C
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                      ОШИБКА!                              ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Python НЕ УСТАНОВЛЕН!
    echo.
    echo Установите Python отсюда:
    echo https://www.python.org/downloads/
    echo.
    echo ВАЖНО: При установке выберите:
    echo   ☑ Add Python to PATH
    echo.
    echo После установки запустите этот файл снова.
    echo.
    pause
    exit /b 1
)

color 0A
cls

echo ╔════════════════════════════════════════════════════════════╗
echo ║  [1/5] УСТАНОВКА ЗАВИСИМОСТЕЙ...                          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pip install -q pyinstaller pytesseract pillow pdf2image python-docx PyQt6 opencv-python numpy

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ОШИБКА при установке зависимостей!
    echo.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  [2/5] ПРОВЕРКА TESSERACT И POPPLER...                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

if not exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    color 0C
    echo.
    echo ⚠️  TESSERACT НЕ НАЙДЕН!
    echo.
    echo Установите Tesseract OCR отсюда:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo После установки запустите этот файл снова.
    echo.
    pause
    exit /b 1
)

if not exist "C:\Program Files\poppler\bin" (
    color 0C
    echo.
    echo ⚠️  POPPLER НЕ НАЙДЕН!
    echo.
    echo Установите Poppler отсюда:
    echo https://github.com/oschwartz10612/poppler-windows/releases/
    echo.
    echo После установки запустите этот файл снова.
    echo.
    pause
    exit /b 1
)

color 0A
echo ✓ Tesseract найден
echo ✓ Poppler найден
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║  [3/5] СОЗДАНИЕ ПРИЛОЖЕНИЯ (это займет 2-3 минуты)        ║
echo ║        Не закрывайте это окно!                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pyinstaller main.py --onefile --windowed --name=PDFTextConverter --distpath=./dist --buildpath=./build --specpath=./build --hidden-import=pytesseract --hidden-import=pdf2image --hidden-import=PIL --hidden-import=docx --collect-all=pytesseract --collect-all=pdf2image

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ОШИБКА при создании EXE!
    echo.
    pause
    exit /b 1
)

color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ ГОТОВО! ПРОГРАММА СОЗДАНА! ✅             ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo.
echo Готовый файл находится здесь:
echo.
echo   dist\PDFTextConverter.exe
echo.
echo.
echo ═══════════════════════════════════════════════════════════════
echo  ЧТО ДАЛЬШЕ?
echo ═══════════════════════════════════════════════════════════════
echo.
echo 1. Откройте папку dist/
echo.
echo 2. Найдите файл PDFTextConverter.exe
echo.
echo 3. ИСПОЛЬЗУЙТЕ ПРОГРАММУ:
echo    - Двойной клик = программа запустится
echo    - Можно скопировать на рабочий стол
echo    - Можно отправить кому-нибудь
echo    - Можно скопировать куда угодно на компьютер
echo.
echo 4. PYTHON МОЖНО УДАЛИТЬ (он больше не нужен!)
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo ПРОГРАММА ПОЛНОСТЬЮ ГОТОВА К ИСПОЛЬЗОВАНИЮ! 🎉
echo.
echo Нажмите Enter чтобы открыть папку с программой...
echo.
pause

REM Открыть папку dist
start dist

echo.
echo Окно закроется через 3 секунды...
timeout /t 3 /nobreak
