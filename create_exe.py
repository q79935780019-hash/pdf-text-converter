"""
Скрипт для создания готового EXE файла
Запустите этот файл один раз и получите готовую программу!

Требует: pip install pyinstaller
"""

import PyInstaller.__main__
import os
import sys

print("=" * 60)
print("СОЗДАНИЕ ГОТОВОГО ПРИЛОЖЕНИЯ (EXE)")
print("=" * 60)
print()

# Проверка наличия pyinstaller
try:
    import PyInstaller
except ImportError:
    print("Установка PyInstaller...")
    os.system("pip install pyinstaller")

print("Создание EXE файла... Это займет 2-3 минуты...")
print()

PyInstaller.__main__.run([
    'main.py',
    '--onefile',                    # Один файл вместо папки
    '--windowed',                   # Графический интерфейс (без консоли)
    '--name=PDFTextConverter',      # Имя программы
    '--distpath=./dist',            # Папка с готовой программой
    '--buildpath=./build',          
    '--specpath=./build',
    '--icon=NONE',                  # Без иконки (можно добавить потом)
    '--hidden-import=pytesseract',
    '--hidden-import=pdf2image',
    '--hidden-import=PIL',
    '--hidden-import=docx',
    '--collect-all=pytesseract',
    '--collect-all=pdf2image',
])

print()
print("=" * 60)
print("✅ ГОТОВО!")
print("=" * 60)
print()
print("Ваша программа находится в папке: dist/")
print()
print("Файл: dist/PDFTextConverter.exe")
print()
print("Можете:")
print("1. Запустить PDFTextConverter.exe сразу")
print("2. Создать ярлык на рабочем столе")
print("3. Скопировать где угодно на компьютер")
print()
print("Программа работает БЕЗ Python и БЕЗ установки!")
print()
input("Нажмите Enter для завершения...")