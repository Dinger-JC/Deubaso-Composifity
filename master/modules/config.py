# Deubaso Composifity
# Config

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json
import sys
from pathlib import Path



# Корневая папка проекта
if getattr(sys, 'frozen', False):
    project = Path(sys.executable).resolve().parent
else:
    project = Path(__file__).resolve().parent.parent

# Индивидуальная папка рядом с .exe
(project / 'data').mkdir(parents = True, exist_ok = True)

# Файлы
files = {
    'bin': {
        'ffmpeg': project / 'bin' / 'ffmpeg.exe',
        'ffprobe': project / 'bin' / 'ffprobe.exe'
    },
    'config': {
        'font': project / 'config' / 'gungsuh_w33.otf',
        'settings': project / 'config' / 'settings.json',
        'sites': project / 'config' / 'sites.json'
    },
    'data': {
        'history': project / 'data' / 'history.json',
        'logs': project / 'data' / 'logs.log',
        'videos': project / 'data' / 'videos.json'
    },
    'images': {
        'png': {
            'bars': {
                'clock': project / 'images' / 'png' / 'bars' / 'clock.png',
                'folder': project / 'images' / 'png' / 'bars' / 'folder.png'
            },
            'buttons': {
                'github': project / 'images' / 'png' / 'buttons' / 'github.png',
                'logs': project / 'images' / 'png' / 'buttons' / 'logs.png',
                'settings': project / 'images' / 'png' / 'buttons' / 'settings.png',
                'stop': project / 'images' / 'png' / 'buttons' / 'stop.png',
                'telegram': project / 'images' / 'png' / 'buttons' / 'telegram.png',
                'tiktok': project / 'images' / 'png' / 'buttons' / 'tiktok.png',
                'trash': project / 'images' / 'png' / 'buttons' / 'trash.png'
            },
            'other': {
                'download': project / 'images' / 'png' / 'other' / 'download.png',
                'link': project / 'images' / 'png' / 'other' / 'link.png',
                'logo': project / 'images' / 'png' / 'other' / 'logo.png',
                'preview': project / 'images' / 'png' / 'other' / 'preview.png'
            }
        },
        'svg': {
            'bars': {
                'clock': project / 'images' / 'svg' / 'bars' / 'clock.svg',
                'folder': project / 'images' / 'svg' / 'bars' / 'folder.svg'
            },
            'buttons': {
                'download_preview': project / 'images' / 'svg' / 'buttons' / 'download_preview.svg',
                'logs': project / 'images' / 'svg' / 'buttons' / 'logs.svg',
                'settings': project / 'images' / 'svg' / 'buttons' / 'settings.svg',
                'stop': project / 'images' / 'svg' / 'buttons' / 'stop.svg',
                'trash': project / 'images' / 'svg' / 'buttons' / 'trash.svg'
            },
            'other': {
                'download': project / 'images' / 'svg' / 'other' / 'download.svg',
                'link': project / 'images' / 'svg' / 'other' / 'link.svg'
            }
        }
    },
    'modules': {
        'config': project / 'modules' / 'config.py',
        'core': project / 'modules' / 'core.py',
        'history': project / 'modules' / 'history.py',
        'info': project / 'modules' / 'info.py',
        'logger': project / 'modules' / 'logger.py',
        'logs': project / 'modules' / 'logs.py',
        'master': project / 'modules' / 'master.py',
        'master_window': project / 'modules' / 'master_window.py',
        'presets': project / 'modules' / 'presets.py',
        'settings': project / 'modules' / 'settings.py'
    }
}

# Настройки
with open(files['config']['settings'], encoding = 'utf-8') as file:
    settings = json.load(file)

# Директория для сохранения порна
if settings.get('path', '').strip() in ('', 'C:\\Users\\{user}\\Videos'):
    settings['path'] = str(Path.home() / 'Videos')

# Поддерживаемые сайты
with open(files['config']['sites'], encoding = 'utf-8') as file:
    sites = json.load(file)

# Константы
chrome = '131'
tags = ['4k', '2k', '1080p', '720p', '640p', '480p', '360p', '240p', '144p']
factor = {
    'KiB': 1_024,
    'MiB': 1_048_576,
    'GiB': 1_073_741_824
}
