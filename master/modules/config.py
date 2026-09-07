# Deubaso Composifity
# Config

# Developer: Dinger_JC
# Project: https://github.com/Dinger-JC/Deubaso-Composifity
# Telegram channel: https://t.me/Jitus_Circus



# Стандартные библиотеки
import json
import os
import sys
from pathlib import Path



# Цвета
colors = {
    # Задний фон
    'main_start': 'rgba(7, 17, 37, 1)',
    'main_end': 'rgba(14, 32, 65, 1)',
    # Текст
    'text': 'rgba(255, 255, 255, 1)',
    'info': 'rgba(180, 180, 180, 1)',
    'good': 'rgba(64, 218, 136, 1)',
    'warning': 'rgba(255, 193, 62, 1)',
    'error': 'rgba(227, 88, 111, 1)',
    # Градиенты
    'hover_start': 'rgba(99, 146, 234, 1)',
    'hover_end': 'rgba(2, 219, 172, 1)',
    'hover_start_pressed': 'rgba(99, 146, 234, 0.4)',
    'hover_end_pressed': 'rgba(2, 219, 172, 0.4)',
    # Другое
    'press': 'rgba(15, 20, 39, 1)',
    'stroke': 'rgba(0, 0, 0, 0)',
    'fill': 'rgba(255, 255, 255, 0.15)',
    'hover_stroke': 'rgba(1, 179, 189, 1)',
    'hover_fill': 'rgba(0, 67, 112, 0.5)'
}

# Файлы
if getattr(sys, 'frozen', False):
    project = Path(sys.executable).resolve().parent

else:
    project = Path(__file__).resolve().parent.parent

# Рабочие папки рядом с exe
(project / 'config').mkdir(parents = True, exist_ok = True)
(project / 'data').mkdir(parents = True, exist_ok = True)

if not (project / 'config' / 'settings.json').exists():
    (project / 'config' / 'settings.json').write_text('{\n  "path": "D:/Saved Videos",\n  "history": 1\n}', encoding = 'utf-8')

if not (project / 'data' / 'history.json').exists():
    (project / 'data' / 'history.json').write_text('{}', encoding = 'utf-8')

if not (project / 'data' / 'videos.json').exists():
    (project / 'data' / 'videos.json').write_text('{}', encoding = 'utf-8')

files = {
    # Папка bin
    'ffmpeg_exe': project / 'bin' / 'ffmpeg.exe',
    'ffprobe_exe': project / 'bin' / 'ffprobe.exe',
    # Папка config
    'settings_json': project / 'config' / 'settings.json',
    'sites_json': project / 'config' / 'sites.json',
    # Папка data
    'history_json': project / 'data' / 'history.json',
    'logs_log': project / 'data' / 'logs.log',
    'videos_json': project / 'data' / 'videos.json',
    # Папка images / png
    'clock_png': project / 'images' / 'png' / 'clock.png',
    'download_png': project / 'images' / 'png' / 'download.png',
    'folder_png': project / 'images' / 'png' / 'folder.png',
    'link_png': project / 'images' / 'png' / 'link.png',
    'logo_png': project / 'images' / 'png' / 'logo.png',
    'preview_png': project / 'images' / 'png' / 'preview.png',
    'settings_png': project / 'images' / 'png' / 'settings.png',
    'stop_png': project / 'images' / 'png' / 'stop.png',
    'trash_png': project / 'images' / 'png' / 'trash.png',
    # Папка images / social
    'github_png': project / 'images' / 'social' / 'github.png',
    'telegram_png': project / 'images' / 'social' / 'telegram.png',
    'tiktok_png': project / 'images' / 'social' / 'tiktok.png',
    # Папка images / svg
    'clock_svg': project / 'images' / 'svg' / 'clock.svg',
    'download_svg': project / 'images' / 'svg' / 'download.svg',
    'folder_svg': project / 'images' / 'svg' / 'folder.svg',
    'link_svg': project / 'images' / 'svg' / 'link.svg',
    'preview_svg': project / 'images' / 'svg' / 'preview.svg',
    'settings_svg': project / 'images' / 'svg' / 'settings.svg',
    'stop_svg': project / 'images' / 'svg' / 'stop.svg',
    'trash_svg': project / 'images' / 'svg' / 'trash.svg',
    # Папка modules
    'config_py': project / 'modules' / 'config.py',
    'core_py': project / 'modules' / 'core.py',
    'history_py': project / 'modules' / 'history.py',
    'logger_py': project / 'modules' / 'logger.py',
    'master_window_py': project / 'modules' / 'master_window.py',
    'presets_py': project / 'modules' / 'presets.py',
    'settings_py': project / 'modules' / 'settings.py',
}

# Основное
name = 'Deubaso Composifity'
version = '2026.09.08.0r'
size_window = [1000, 600]
border_radius_small = 10
border_radius_big = 15
font_big = 18
font_small = 14
font_family = 'Sitka Small'

# Настройки
with open(files['settings_json'], encoding = 'utf-8') as file:
    settings = json.load(file)

# Поддерживаемые сайты
with open(files['sites_json'], encoding = 'utf-8') as file:
    sites = json.load(file)

# История
if not os.path.exists(files['history_json']):
    with open(files['history_json'], 'w', encoding = 'utf-8') as file:
        json.dump({}, file)

with open(files['history_json'], encoding = 'utf-8') as file:
    history = json.load(file)
