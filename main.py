import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QTextEdit, QComboBox, QTabWidget, QScrollArea,
                             QMessageBox, QProgressBar, QSpinBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from docx import Document
import cv2
import numpy as np

# Пути к Tesseract и Poppler
TESERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Program Files\poppler\bin'

class OCRWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, file_path, output_format):
        super().__init__()
        self.file_path = file_path
        self.output_format = output_format
    
    def run(self):
        try:
            pytesseract.pytesseract.pytesseract_cmd = TESSERACT_PATH
            
            if self.file_path.lower().endswith('.pdf'):
                images = convert_from_path(self.file_path, poppler_path=POPPLER_PATH)
                full_text = ""
                for idx, img in enumerate(images):
                    self.progress.emit(int((idx / len(images)) * 100))
                    text = pytesseract.image_to_string(img, lang='rus+eng')
                    full_text += f"--- Страница {idx + 1} ---\n{text}\n\n"
            else:
                image = Image.open(self.file_path)
                full_text = pytesseract.image_to_string(image, lang='rus+eng')
                self.progress.emit(100)
            
            # Очищение текста
            full_text = self.clean_text(full_text)
            
            # Сохранение результата
            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
            
            if self.output_format == "txt":
                output_path = os.path.join(os.path.dirname(self.file_path), f"{base_name}_result.txt")
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_text)
            elif self.output_format == "docx":
                output_path = os.path.join(os.path.dirname(self.file_path), f"{base_name}_result.docx")
                doc = Document()
                doc.add_paragraph(full_text)
                doc.save(output_path)
            
            self.finished.emit(f"✓ Готово! Файл сохранён:\n{output_path}\n\n{full_text[:500]}...")
            
        except Exception as e:
            self.error.emit(f"Ошибка: {str(e)}")
    
    def clean_text(self, text):
        """Улучшение качества распознанного текста"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 2:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

class ImageRotator(QWidget):
    def __init__(self):
        super().__init__()
        self.current_image = None
        self.current_angle = 0
        self.image_path = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        
        btn_load = QPushButton("Загрузить картинку")
        btn_load.clicked.connect(self.load_image)
        btn_layout.addWidget(btn_load)
        
        btn_rotate_left = QPushButton("↻ Влево (90°)")
        btn_rotate_left.clicked.connect(self.rotate_left)
        btn_layout.addWidget(btn_rotate_left)
        
        btn_rotate_right = QPushButton("↺ Вправо (90°)")
        btn_rotate_right.clicked.connect(self.rotate_right)
        btn_layout.addWidget(btn_rotate_right)
        
        self.spin_angle = QSpinBox()
        self.spin_angle.setRange(0, 360)
        self.spin_angle.setValue(0)
        self.spin_angle.valueChanged.connect(self.rotate_custom)
        btn_layout.addWidget(QLabel("Угол:"))
        btn_layout.addWidget(self.spin_angle)
        
        btn_to_pdf = QPushButton("💾 Сохранить как PDF")
        btn_to_pdf.clicked.connect(self.save_as_pdf)
        btn_layout.addWidget(btn_to_pdf)
        
        layout.addLayout(btn_layout)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 400)
        layout.addWidget(self.image_label)
        
        self.setLayout(layout)
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите картинку", "", 
                                                    "Images (*.jpg *.jpeg *.png *.bmp)")
        if file_path:
            self.image_path = file_path
            self.current_image = Image.open(file_path)
            self.current_angle = 0
            self.spin_angle.setValue(0)
            self.display_image()
    
    def rotate_left(self):
        self.current_angle = (self.current_angle + 90) % 360
        self.spin_angle.setValue(self.current_angle)
    
    def rotate_right(self):
        self.current_angle = (self.current_angle - 90) % 360
        self.spin_angle.setValue(self.current_angle)
    
    def rotate_custom(self, angle):
        self.current_angle = angle
        self.display_image()
    
    def display_image(self):
        if self.current_image:
            rotated = self.current_image.rotate(self.current_angle, expand=True)
            rotated.thumbnail((400, 400))
            
            qt_image = QImage(rotated.tobytes(), rotated.width(), rotated.height(), 
                            rotated.width() * 3, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)
    
    def save_as_pdf(self):
        if not self.current_image:
            QMessageBox.warning(self, "Ошибка", "Загрузите картинку сначала!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как PDF", "", "PDF (*.pdf)")
        if file_path:
            rotated = self.current_image.rotate(self.current_angle, expand=True)
            rotated = rotated.convert('RGB')
            rotated.save(file_path, 'PDF')
            QMessageBox.information(self, "Успех", f"PDF сохранён:\n{file_path}")

class OCRTab(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.ocr_worker = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Кнопка загрузки
        btn_layout = QHBoxLayout()
        btn_load = QPushButton("📂 Загрузить PDF или картинку")
        btn_load.clicked.connect(self.load_file)
        btn_layout.addWidget(btn_load)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Текстовый файл (.txt)", "Документ Word (.docx)"])
        btn_layout.addWidget(QLabel("Формат сохранения:"))
        btn_layout.addWidget(self.format_combo)
        
        btn_start = QPushButton("▶ Распознать текст")
        btn_start.clicked.connect(self.start_ocr)
        btn_layout.addWidget(btn_start)
        
        layout.addLayout(btn_layout)
        
        # Инфо о файле
        self.file_info = QLabel("Файл не выбран")
        layout.addWidget(self.file_info)
        
        # Прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Результат
        layout.addWidget(QLabel("Результат:"))
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
    
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", 
                                                    "All Files (*.pdf *.jpg *.jpeg *.png *.bmp)")
        if file_path:
            self.selected_file = file_path
            self.file_info.setText(f"✓ Выбран: {os.path.basename(file_path)}")
    
    def start_ocr(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Ошибка", "Выберите файл сначала!")
            return
        
        output_format = "txt" if "txt" in self.format_combo.currentText() else "docx"
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.result_text.setText("⏳ Обработка...")
        
        self.ocr_worker = OCRWorker(self.selected_file, output_format)
        self.ocr_worker.progress.connect(self.progress_bar.setValue)
        self.ocr_worker.finished.connect(self.on_finished)
        self.ocr_worker.error.connect(self.on_error)
        self.ocr_worker.start()
    
    def on_finished(self, message):
        self.result_text.setText(message)
        self.progress_bar.setVisible(False)
    
    def on_error(self, error_msg):
        self.result_text.setText(f"❌ {error_msg}")
        self.progress_bar.setVisible(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("PDF & Image to Text Converter")
        self.setGeometry(100, 100, 900, 700)
        
        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        
        # Вкладки
        tabs = QTabWidget()
        
        ocr_tab = OCRTab()
        tabs.addTab(ocr_tab, "📄 OCR (PDF → Текст)")
        
        rotator_tab = ImageRotator()
        tabs.addTab(rotator_tab, "🖼️ Конвертер (Картинка → PDF)")
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        central.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())