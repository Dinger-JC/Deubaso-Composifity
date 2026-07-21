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
import string
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

except ImportError:
    print('Could not import local modules.')
    sys.exit(1)



project = Path(__file__).resolve().parent.parent
files = {
    # Папка bin
    'ffmpeg': project / 'bin' / 'ffmpeg.exe',
    'ffprobe': project / 'bin' / 'ffprobe.exe',
    # Папка config
    'settings': project / 'config' / 'settings.json',
    'sites': project / 'config' / 'sites.json',
    # Папка data
    'history': project / 'data' / 'history.json',
    'videos': project / 'data' / 'videos.json',
    # Папка resources
    'icon_icon': project / 'resources' / 'icon.png',
    'link_icon': project / 'resources' / 'link.png',
    'download_icon': project / 'resources' / 'download.png',
    'stop_icon': project / 'resources' / 'stop.png',
    'settings_icon': project / 'resources' / 'settings.png',
    'preview_icon': project / 'resources' / 'preview.png'
}

def Files(files):
    '''Проверка наличия файлов'''
    error = False
    for name, path in files.items():
        if not path.is_file():
            if name == 'ffmpeg' or name == 'ffprobe':
                log.critical(f'The "{path}" file was not found.')
                log.critical('You can download it here: https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45.')
                log.critical('After downloading, move the exe file to the bin folder in the root of the project.')
                error = True

            elif name == 'history':
                return

            elif name == 'videos':
                log.warning(f'The "{path}" file was not found.')
                return

            else:
                log.critical(f'The "{path}" file was not found.')
                error = True

    if error:
        os._exit(0)



if __name__ == '__main__':
    try:
        Files(files)

        log.info('Start')
        app = QApplication(sys.argv)

        core = CORE(files)
        master = MASTER_WINDOW(files, core, '2026.07.21.2b')
        core.gui = master

        master.window.show()
        sys.exit(app.exec())

    except Exception as e:
        log.critical(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')
