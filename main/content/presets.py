# Deubaso Composifity
# Presets

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json

# Сторонние библиотеки
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvg import *
from PySide6.QtWidgets import *

# Локальные модули
from config import *



# Константы
name = 'Deubaso Composifity'
version = '2026.10.19.0'

size_window = (1000, 600)
size_preview = (534, 300)
size_icon = QSize(30, 30)
size_big = 50
size_small = 30

bottom = size_window[1] - 70
margin = 20
length = size_window[0] - margin * 2

border_radius_small = 10
border_radius_big = 15

font_small = 14
font_big = 18
font_family = ''

with open(files['content']['colors'], encoding = 'utf-8') as file:
    colors = json.load(file)



def Window(window, title: str, name: str):
    '''Главное окно'''
    window.setWindowTitle(title)
    window.setWindowIcon(QIcon(str(files['images']['png']['other']['logo'])))
    window.setFixedSize(size_window[0], size_window[1])
    window.setStyleSheet(f'''
        QMainWindow {{
            background-color: {STYLES.main_gradient}
        }}
    ''')

    text_top = QLabel(name, window)
    text_top.setGeometry(margin, 20, length, 55)
    text_top.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
    text_top.setStyleSheet(f'''
        QLabel {{
            color: {STYLES.active_gradient}
            font-size: 40px;
        }}
    ''')

    text_version = QLabel(f'Version: {version}', window)
    text_version.setGeometry(5, 5, 200, 20)
    text_version.setStyleSheet(f'''
        background: transparent;
        color: {colors['signal']['info']};
        font-size: {font_small}px;
        font-family: {files['content']['font_logs']};
    ''')



class STYLES:
    empty = '''
        background: transparent;
        border: none;
    '''

    tooltip = f'''
        QToolTip {{
            background-color: {colors['tooltip']['fill']};
            border: 2px solid {colors['tooltip']['stroke']};
            border-radius: 4px;

            color: {colors['signal']['text']};
            font-size: {font_big}px;
            padding: 2px;
        }}
    '''

    main_gradient = f'''
        qlineargradient(
            spread:pad,
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {colors['main']['start']},
            stop:1 {colors['main']['end']}
        );
    '''

    active_gradient = f'''
        qlineargradient(
            spread:pad,
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {colors['download']['start']},
            stop:1 {colors['download']['end']}
        );
    '''

    push_gradient = f'''
        qlineargradient(
            spread:pad,
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {colors['download']['start_pressed']},
            stop:1 {colors['download']['end_pressed']}
        );
    '''

    button = f'''
        QPushButton {{
            background-color: {colors['other']['fill']};
            border: 2px solid {colors['other']['stroke']};
            border-radius: {border_radius_small}px;
        }}
    '''

    button_hover = f'''
        QPushButton:hover {{
            background-color: {colors['tooltip']['fill']};
            border-color: {colors['tooltip']['stroke']};
        }}
    '''

    button_pressed = f'''
        QPushButton:pressed {{
            background-color: {colors['other']['press']};
            border-color: {colors['other']['stroke']};
        }}
    '''



class Main_Layouts:
    blocks = {
        'speed': {
            'geometry': [574, 280, 122, 80],
            'title': 'Speed'
        },
        'max_speed': {
            'geometry': [716, 280, 122, 80],
            'title': 'Max speed'
        },
        'size': {
            'geometry': [858, 280, 122, 80],
            'title': 'Size'
        },
        'quality': {
            'geometry': [574, 380, 122, 80],
            'title': 'Quality'
        },
        'fps': {
            'geometry': [716, 380, 122, 80],
            'title': 'FPS'
        },
        'duration': {
            'geometry': [858, 380, 122, 80],
            'title': 'Duration'
        }
    }

    buttons = {
        'download_video': {
            'geometry': [574, bottom, 264, size_big],
            'title': 'Download video',
            'tooltip': 'Download video',
            'icon': None
        },
        'stop': {
            'geometry': [858, bottom, size_big, size_big],
            'title': None,
            'tooltip': 'Abort the download',
            'icon': files['images']['svg']['buttons']['stop']
        },
        'settings': {
            'geometry': [930, bottom, size_big, size_big],
            'title': None,
            'tooltip': 'Settings',
            'icon': files['images']['svg']['buttons']['settings']
        }
    }

class Settings_Layouts:
    blocks = {
        'history': {
            'geometry': [margin, 95, length, size_big],
            'tooltip': 'Record link history',
            'icon': files['images']['svg']['blocks']['clock']
        },
        'folder': {
            'geometry': [margin, 165, length, size_big],
            'tooltip': 'Path for saving downloaded videos',
            'icon': files['images']['svg']['blocks']['folder']
        }
    }

    buttons = {
        'github': {
            'geometry': [930, bottom, size_big, size_big],
            'tooltip': 'Open GitHub repository',
            'icon': files['images']['svg']['buttons']['github'],
            'link': 'https://github.com/Dinger-JC/Deubaso-Composifity'
        },
        'telegram': {
            'geometry': [860, bottom, size_big, size_big],
            'tooltip': 'Open Telegram channel',
            'icon': files['images']['svg']['buttons']['telegram'],
            'link': 'https://t.me/Jitus_Circus'
        },
        'tiktok': {
            'geometry': [790, bottom, size_big, size_big],
            'tooltip': 'Open TikTok account',
            'icon': files['images']['svg']['buttons']['tiktok'],
            'link': 'https://www.tiktok.com/@dinger_jc'
        },
        'info': {
            'geometry': [margin, bottom, size_big, size_big],
            'tooltip': 'Info',
            'icon': files['images']['svg']['buttons']['info']
        },
        'logs': {
            'geometry': [margin * 2 + size_big, bottom, size_big, size_big],
            'tooltip': 'Logs',
            'icon': files['images']['svg']['buttons']['logs']
        },
        'clear_history': {
            'geometry': [margin * 3 + size_big * 2, bottom, size_big, size_big],
            'tooltip': 'Clear history',
            'icon': files['images']['svg']['buttons']['trash'],
            'command': 'clear'
        }
    }
