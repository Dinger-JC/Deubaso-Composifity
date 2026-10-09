# Deubaso Composifity
# Info

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Локальные модули
from config import files
from logger import Log
from presets import *

log = Log()



class INFO():
    '''Окно информации'''
    def __init__(self, parent_window):
        '''Инициализация'''
        # Основное
        self.window = QMainWindow(parent_window)

        # Отрисовка
        Window(self.window, f'{name} - Info', 'Info')

        self.Info()

    def Info(self):
        '''Карточка'''
        card = QFrame(self.window)
        card.setGeometry(margin, 95, length, 486)
        card.setStyleSheet(f'''
            QFrame {{
                background-color: {colors['other']['fill']};
                border: 2px solid {colors['other']['stroke']};
                border-radius: {border_radius_small}px;
            }}
        ''')

        text = (
            'Deubaso Composifity is Copyright © 2026 by Dinger_JC, All rights reserved'
            '\n\nThis is a modern app for downloading videos from 18+ websites. It downloads videos and previews in the best quality.'
            '\n\nYou have the right to use and make unlimited copies of this application. The author does not provide or imply any guarantees. The author is not responsible for data loss, damages, loss of profits, or any other type of loss resulting from the use or inability to use this application.'
            '\n\nAny suggestions, requests, or comments are welcome!'
        )

        title = QLabel(name, card)
        title.setGeometry(margin, 20, 922, size_big)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        title.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        title.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;

                color: {colors['signal']['text']};
                font-size: 30px;
            }}
        ''')

        info = QLabel(text, card)
        info.setGeometry(margin, 90, 922, 397)
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        info.setStyleSheet(f'''
            QLabel {{
                background: transparent;
                border: none;

                color: {colors['signal']['text']};
                font-size: {font_big}px;
            }}
        ''')

    def Show(self):
        '''Показ окна'''
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()
