# Deubaso Composifity
# Presets

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from master import *



def Window(
    window, size_window: list,
    title: str, subtitle: str, icon: str,
    color_start_window: str, color_end_window: str,
    color_start_title: str, color_end_title: str,
    color_version: str,
    font_family: str, font_size: str,
    version: str
):
    '''Главное окно'''
    # Окно
    window.setWindowTitle(title)
    window.setWindowIcon(QIcon(str(icon)))
    window.setFixedSize(size_window[0], size_window[1])
    window.setStyleSheet(f'''
        QMainWindow {{
            background-color: qlineargradient(
                spread:pad, 
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {color_start_window}, 
                stop:1 {color_end_window}
            );
        }}
    ''')

    # Заголовок окна
    text_top = QLabel(subtitle, window)
    text_top.setGeometry(20, 20, 960, 55)
    text_top.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    text_top.setStyleSheet(f'''
        QLabel {{
            color: qlineargradient(
                spread:pad,
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {color_start_title},
                stop:1 {color_end_title}
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
        color: {color_version};
        font-family: '{font_family}';
        font-size: {font_size}px;
    ''')
