# Deubaso Composifity
# Presets

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import colors, font_family, font_small, name, size_window, version
from master import *



def Window(window, title: str):
    '''Главное окно'''
    # Окно
    window.setWindowTitle(title)
    window.setWindowIcon(QIcon(str(files['icon_i'])))
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
    
            font-family: '{font_family}';
            font-size: 40px;
        }}
    ''')

    # Версия
    text_version = QLabel(f'Version: {version}', window)
    text_version.setGeometry(5, 5, 200, 20)
    text_version.setStyleSheet(f'''
        background: transparent;
        color: {colors['sub_text']};
        font-family: '{font_family}';
        font-size: {font_small}px;
    ''')
