# Deubaso Composifity
# Initialization

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import ctypes
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
from urllib.parse import urlparse

# Сторонние библиотеки
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
    from config import files, font_family
    from core import *
    from master_window import *
    from logger import *
    log = Log()

except ImportError:
    print(f'Could not import modules.')



def Files():
    '''Проверка наличия файлов'''
    error = False
    for name, path in files.items():
        if not path.is_file():
            if name == 'ffmpeg_exe' or name == 'ffprobe_exe':
                print(f'"{path}" not found.')
                print('You can download it here: https://github.com/GyanD/codexffmpeg/releases/tag/2026-01-05-git-2892815c45.')
                print('After downloading, move the exe file to the bin folder in the root of the project.')
                error = True

            elif name == 'videos_json':
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
        app.setQuitOnLastWindowClosed(True)
        app.setFont(font_family)

        lock = QLockFile(str(Path(sys.argv[0]).resolve().with_name('app.lock')))
        lock.setStaleLockTime(0)
        if not lock.tryLock(100):
            QMessageBox.warning(None, 'Внимание', 'Приложение уже запущено!')
            sys.exit(0)

        core = CORE()
        master_window = MASTER_WINDOW(core)
        core.signal = master_window

        sys.exit(app.exec())

    except Exception as e:
        log.critical(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')
