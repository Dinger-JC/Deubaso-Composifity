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

# Индивидуальная папка
(project / 'data').mkdir(parents = True, exist_ok = True)

# Файлы
files = {
    'bin': {
        'ffmpeg': project / 'bin' / 'ffmpeg.exe',
        'ffprobe': project / 'bin' / 'ffprobe.exe'
    },
    'content': {
        'colors': project / 'content' / 'colors.json',
        'config': project / 'content' / 'config.py',
        'font_logs': project / 'content' / 'jetbrains_mono_nl.ttf',
        'presets': project / 'content' / 'presets.py',
        'sites': project / 'content' / 'sites.json',
        'font': project / 'content' / 'universal_antiqua.ttf'
    },
    'data': {
        'history': project / 'data' / 'history.json',
        'logs': project / 'data' / 'logs.log',
        'settings': project / 'data' / 'settings.json',
        'videos': project / 'data' / 'videos.json'
    },
    'images': {
        'png': {
            'other': {
                'logo': project / 'images' / 'png' / 'other' / 'logo.png',
                'preview': project / 'images' / 'png' / 'other' / 'preview.png'
            }
        },
        'svg': {
            'blocks': {
                'clock': project / 'images' / 'svg' / 'bars' / 'clock.svg',
                'folder': project / 'images' / 'svg' / 'bars' / 'folder.svg'
            },
            'buttons': {
                'github': project / 'images' / 'svg' / 'buttons' / 'github.svg',
                'info': project / 'images' / 'svg' / 'buttons' / 'info.svg',
                'logs': project / 'images' / 'svg' / 'buttons' / 'logs.svg',
                'settings': project / 'images' / 'svg' / 'buttons' / 'settings.svg',
                'stop': project / 'images' / 'svg' / 'buttons' / 'stop.svg',
                'telegram': project / 'images' / 'svg' / 'buttons' / 'telegram.svg',
                'tiktok': project / 'images' / 'svg' / 'buttons' / 'tiktok.svg',
                'trash': project / 'images' / 'svg' / 'buttons' / 'trash.svg'
            },
            'other': {
                'download': project / 'images' / 'svg' / 'other' / 'download.svg',
                'link': project / 'images' / 'svg' / 'other' / 'link.svg'
            }
        }
    },
    'modules': {
        'core': project / 'modules' / 'core.py',
        'history': project / 'modules' / 'history.py',
        'info': project / 'modules' / 'info.py',
        'initialization': project / 'modules' / 'initialization.py',
        'logger': project / 'modules' / 'logger.py',
        'logs': project / 'modules' / 'logs.py',
        'main': project / 'modules' / 'main.py',
        'settings': project / 'modules' / 'settings.py'
    }
}

# Поддерживаемые сайты
with open(files['content']['sites'], encoding = 'utf-8') as file:
    sites = json.load(file)

# Настройки
if not files['data']['settings'].is_file():
    settings = {
        'path': str(Path.home() / 'Videos'),
        'history': 1
    }
    with open(files['data']['settings'], 'w', encoding = 'utf-8') as file:
        json.dump(settings, file, ensure_ascii = False, indent = 2)
else:
    with open(files['data']['settings'], encoding = 'utf-8') as file:
        settings = json.load(file)

# История
if not files['data']['history'].is_file():
    with open(files['data']['history'], 'w', encoding = 'utf-8') as file:
        json.dump({}, file, indent = 4, ensure_ascii = False)

# Константы
placeholder = 'Strip2, Rule34Video, XGroovy, AnalMedia'
chrome = '131'
tags = ('4k', '2k', '1080p', '720p', '640p', '480p', '360p', '240p', '144p')
factor = {
    'KiB': 1_024,
    'MiB': 1_048_576,
    'GiB': 1_073_741_824
}
