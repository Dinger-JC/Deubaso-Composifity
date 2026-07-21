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
    from master_window import *
    from logger import *
    log = Log(__name__)

except ImportError:
    print('Could not import local modules.')
    sys.exit(1)



if __name__ == '__main__':
    try:
        log.info('Start')
        app = QApplication(sys.argv)

        core = CORE()
        master = MASTER_WINDOW(core, '2026.07.21.1b')
        core.gui = master

        master.window.show()
        sys.exit(app.exec())

    except Exception as e:
        log.critical(f'Unexpected error: {e}')

    finally:
        log.info('Shutdown')
