# Deubaso Composifity
# Initialization

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json
import logging
import math
import os
import re
import secrets
import subprocess
import sys
import threading
from datetime import timedelta, datetime
from fractions import Fraction
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pprint import pp
from urllib.parse import urlparse

# Сторонние библиотеки
packages = ['ffmpeg-python', 'yt-dlp', 'beautifulsoup4', 'curl-cffi', 'PySide6', 'mutagen']

try:
    import ffmpeg
    import yt_dlp
    from bs4 import BeautifulSoup
    from curl_cffi import requests
    from PySide6.QtGui import *
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from mutagen.mp4 import MP4

except ImportError:
    print('The required modules are missing. Module installation begins...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *packages])

finally:
    import ffmpeg
    import yt_dlp
    from bs4 import BeautifulSoup
    from curl_cffi import requests
    from PySide6.QtGui import *
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from mutagen.mp4 import MP4

# Локальные модули
try:
    from core import *
    from master_window import *
    from logger import *
    log = Log()

except Exception:
    pass



# Файлы
project = Path(__file__).resolve().parent.parent
files = {
    # Папка bin
    'ffmpeg_e': project / 'bin' / 'ffmpeg.exe',
    'ffprobe_e': project / 'bin' / 'ffprobe.exe',
    # Папка config
    'settings_j': project / 'config' / 'settings.json',
    'sites_j': project / 'config' / 'sites.json',
    # Папка data
    'history_j': project / 'data' / 'history.json',
    'videos_j': project / 'data' / 'videos.json',
    # Папка modules
    'core_p': project / 'modules' / 'core.py',
    'logger_p': project / 'modules' / 'logger.py',
    'master_window_p': project / 'modules' / 'master_window.py',
    'settings_p': project / 'modules' / 'settings.py',
    # Папка resources
    'download_i': project / 'resources' / 'download.png',
    'icon_i': project / 'resources' / 'icon.png',
    'link_i': project / 'resources' / 'link.png',
    'preview_i': project / 'resources' / 'preview.png',
    'settings_i': project / 'resources' / 'settings.png',
    'stop_i': project / 'resources' / 'stop.png'
}

# Основное
name = 'Deubaso Composifity'
version = '2026.07.23.6b'
size_window = [1000, 600]
border_radius = 10

# Цвета
colors = {
    'main_start': 'rgb(7, 17, 37)',
    'main_end': 'rgb(34, 42, 65)',
    'text': 'rgb(255, 255, 255)',
    'sub_text': 'rgb(180, 180, 180)',
    'stroke': 'rgba(0, 0, 0, 0)',
    'fill': 'rgba(255, 255, 255, 0.15)',
    'hover_stroke': 'rgb(1, 179, 189)',
    'hover_fill': 'rgba(0, 67, 112, 0.5)',
    'hover_start': 'rgb(99, 146, 234)',
    'hover_end': 'rgb(2, 219, 172)',
    'hover_start_pressed': 'rgba(99, 146, 234, 0.4)',
    'hover_end_pressed': 'rgba(2, 219, 172, 0.4)',
    'warning': 'rgb(255, 193, 62)',
    'error': 'rgb(227, 88, 111)'
}

# Шрифт
font_family = 'GungsuhW33-Regular'
font_big = 18
font_small = 14



def Files():
    '''Проверка наличия файлов'''
    error = False
    for name, path in files.items():
        if not path.is_file():
            if name == 'ffmpeg' or name == 'ffprobe':
                print(f'"{path}" not found.')
                print('You can download it here: https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45.')
                print('After downloading, move the exe file to the bin folder in the root of the project.')
                error = True

            elif name == 'videos':
                print(f'"{path}" not found.')

            else:
                print(f'"{path}" not found.')
                error = True

    if error:
        sys.exit(1)



if __name__ == '__main__':
    Files()

    try:
        log.info('Start')
        app = QApplication(sys.argv)

        core = CORE(files)
        master = MASTER_WINDOW(files, core, name, version, colors, size_window, font_family, font_big, font_small, border_radius)
        core.signal = master

        master.window.show()
        sys.exit(app.exec())

    except Exception as e:
        log.critical(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')
