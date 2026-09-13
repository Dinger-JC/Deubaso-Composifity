# Deubaso Composifity
# Presets

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Сторонние библиотеки
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# Локальные модули
from config import files



# Основное
name = 'Deubaso Composifity'
version = '2026.09.14.0'
size_window = [1000, 600]
border_radius_small = 10
border_radius_big = 15
font_big = 18
font_small = 14
font_family = ''

# Цвета
colors = {
    # Задний фон
    'main_start': 'rgba(7, 17, 37, 1)',
    'main_end': 'rgba(14, 32, 65, 1)',
    # Текст
    'text': 'rgba(255, 255, 255, 1)',
    'info': 'rgba(180, 180, 180, 1)',
    'good': 'rgba(64, 218, 136, 1)',
    'warning': 'rgba(255, 193, 62, 1)',
    'error': 'rgba(227, 88, 111, 1)',
    # Градиенты
    'hover_start': 'rgba(99, 146, 234, 1)',
    'hover_end': 'rgba(2, 219, 172, 1)',
    'hover_start_pressed': 'rgba(99, 146, 234, 0.4)',
    'hover_end_pressed': 'rgba(2, 219, 172, 0.4)',
    # Другое
    'press': 'rgba(15, 20, 39, 1)',
    'stroke': 'rgba(0, 0, 0, 0)',
    'fill': 'rgba(255, 255, 255, 0.15)',
    'hover_stroke': 'rgba(1, 179, 189, 1)',
    'hover_fill': 'rgba(0, 67, 112, 0.5)'
}



def Window(window, title: str, name: str):
    '''Главное окно'''
    window.setWindowTitle(title)
    window.setWindowIcon(QIcon(str(files['images']['png']['other']['logo'])))
    window.setFixedSize(size_window[0], size_window[1])
    window.setStyleSheet(f'''
        QMainWindow {{
            background-color: qlineargradient(
                spread:pad, 
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['main_start']}, 
                stop:1 {colors['main_end']}
            );
        }}
    ''')

    # Заголовок окна
    text_top = QLabel(name, window)
    text_top.setGeometry(20, 20, 960, 55)
    text_top.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    text_top.setStyleSheet(f'''
        QLabel {{
            color: qlineargradient(
                spread:pad,
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {colors['hover_start']},
                stop:1 {colors['hover_end']}
            );
    
            font-size: 40px;
        }}
    ''')

    # Версия
    text_version = QLabel(f'Version: {version}', window)
    text_version.setGeometry(5, 5, 200, 20)
    text_version.setStyleSheet(f'''
        background: transparent;
        color: {colors['info']};
        font-size: {font_small}px;
    ''')
